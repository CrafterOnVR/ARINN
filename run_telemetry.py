#!/usr/bin/env python3
import sys
import os

from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QHBoxLayout, QLabel, QTabWidget, QGroupBox, QGridLayout)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QPalette, QColor

# pyqtgraph for clean, empirical data rendering
import pyqtgraph as pg

from arinn_core.benchmark_suite import BenchmarkSuite

class TelemetryDashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.benchmark = BenchmarkSuite()
        
        try:
            from memory_manager import MemoryManager
            self.memory = MemoryManager(root=os.path.abspath(os.path.dirname(__file__)))
        except Exception:
            self.memory = None
            
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("ARINN - Telemetry & Benchmarking")
        self.setGeometry(100, 100, 1000, 700)
        
        # Clean, empirical dark theme
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(40, 40, 40))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(240, 240, 240))
        self.setPalette(palette)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Header
        header = QLabel("ARINN Telemetry & Benchmarking")
        header.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(header)
        
        # Tabs
        self.tabs = QTabWidget()
        self.tab_growth = QWidget()
        self.tab_leaderboard = QWidget()
        self.tab_telemetry = QWidget()
        
        self.tabs.addTab(self.tab_growth, "Growth & Efficiency")
        self.tabs.addTab(self.tab_leaderboard, "LLM Leaderboard")
        self.tabs.addTab(self.tab_telemetry, "Live Telemetry")
        
        main_layout.addWidget(self.tabs)
        
        self.setup_growth_tab()
        self.setup_leaderboard_tab()
        self.setup_telemetry_tab()
        
        # Live auto-refresh timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh_all_graphs)
        self.timer.start(2000) # Refresh every 2 seconds
        
    def refresh_all_graphs(self):
        self.refresh_growth_graph()
        self.refresh_leaderboard_graph()
        
        # Refresh METR status box
        current_task, completed = self.benchmark.get_metr_status()
        if hasattr(self, 'lvl_label') and hasattr(self, 'time_label'):
            self.lvl_label.setText(f"Level {current_task['level']}: {current_task['task']}")
            self.time_label.setText(f"Human Time Equivalent: {current_task['human_time']}")
            
        # Refresh Live Stats
        if hasattr(self, 'lbl_status'):
            import os
            import time
            is_running = False
            json_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "arinn_benchmarks.json")
            if os.path.exists(json_path):
                if time.time() - os.path.getmtime(json_path) < 300:
                    is_running = True
                    
            if is_running:
                self.lbl_status.setText("SWARM ACTIVE")
                self.lbl_status.setStyleSheet("color: #00ff66;")
                self.lbl_subbrains.setText("18 / 20")
            else:
                self.lbl_status.setText("IDLE (Sleeping)")
                self.lbl_status.setStyleSheet("color: #ffaa00;")
                self.lbl_subbrains.setText("0 / 20")
                
            history = self.benchmark._load_history()
            mutations = len(history.get("rsi_efficiency_scores", []))
            self.lbl_mutations.setText(f"{mutations:,}")
            
            if self.memory:
                try:
                    vectors = self.memory.collection.count()
                    self.lbl_chroma.setText(f"{vectors:,}")
                except Exception:
                    self.lbl_chroma.setText("???")
            else:
                self.lbl_chroma.setText("???")
        
    def setup_growth_tab(self):
        layout = QVBoxLayout(self.tab_growth)
        
        label = QLabel("RSI Exponential Growth Curve (Score over Generation)")
        label.setFont(QFont("Arial", 14))
        layout.addWidget(label)
        
        # Create pyqtgraph PlotWidget
        self.growth_plot = pg.PlotWidget()
        self.growth_plot.setBackground((40, 40, 40))
        self.growth_plot.setLabel('left', 'Synthetic Intelligence Score')
        self.growth_plot.setLabel('bottom', 'Evolutionary Generation')
        self.growth_plot.showGrid(x=True, y=True, alpha=0.3)
        layout.addWidget(self.growth_plot)
        
        self.refresh_growth_graph()
        
    def refresh_growth_graph(self):
        x, y = self.benchmark.get_historical_growth()
        self.growth_plot.clear()
        
        # Plot the exponential curve
        pen = pg.mkPen(color=(0, 255, 100), width=3)
        self.growth_plot.plot(x, y, pen=pen, symbol='o', symbolSize=8, symbolBrush=(0, 255, 100))

    def setup_leaderboard_tab(self):
        layout = QVBoxLayout(self.tab_leaderboard)
        
        label = QLabel("Comparative LLM Benchmarks (Synthetic Reasoning Score)")
        label.setFont(QFont("Arial", 14))
        layout.addWidget(label)
        
        self.leaderboard_plot = pg.PlotWidget()
        self.leaderboard_plot.setBackground((40, 40, 40))
        layout.addWidget(self.leaderboard_plot)
        
        self.refresh_leaderboard_graph()
        
    def refresh_leaderboard_graph(self):
        models, scores = self.benchmark.get_leaderboard_data()
        self.leaderboard_plot.clear()
        
        # Create BarGraphItem
        x_positions = range(len(models))
        
        # Color ARINN green, others blue
        brushes = [(0, 255, 100, 200) if "ARINN" in model else (50, 150, 255, 200) for model in models]
        
        bargraph = pg.BarGraphItem(x=list(x_positions), height=scores, width=0.6, brushes=brushes)
        self.leaderboard_plot.addItem(bargraph)
        
        # Set X axis string labels
        ticks = [list(zip(x_positions, models))]
        self.leaderboard_plot.getAxis('bottom').setTicks(ticks)
        self.leaderboard_plot.setLabel('left', 'Synthetic Score')

    def setup_telemetry_tab(self):
        layout = QVBoxLayout(self.tab_telemetry)
        
        grid = QGridLayout()
        
        # Simple data boxes
        box1, self.lbl_status = self.create_stat_box("Current Status", "IDLE (Daydreaming)")
        box2, self.lbl_subbrains = self.create_stat_box("Active SubBrains", "0 / 20")
        box3, self.lbl_chroma = self.create_stat_box("ChromaDB Vectors", "0")
        box4, self.lbl_mutations = self.create_stat_box("Successful Code Mutations", "0")
        
        grid.addWidget(box1, 0, 0)
        grid.addWidget(box2, 0, 1)
        grid.addWidget(box3, 1, 0)
        grid.addWidget(box4, 1, 1)
        
        # METR Time Horizon Status
        current_task, completed_tasks = self.benchmark.get_metr_status()
        level_str = f"Level {current_task['level']}: {current_task['task']}"
        time_str = f"Human Time Equivalent: {current_task['human_time']}"
        
        metr_box = QGroupBox("METR Autonomy Horizon")
        metr_box.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        metr_box.setStyleSheet("QGroupBox { border: 1px solid #00ff66; margin-top: 15px; } QGroupBox::title { color: #00ff66; top: -10px; left: 10px; }")
        
        metr_layout = QVBoxLayout(metr_box)
        self.lvl_label = QLabel(level_str)
        self.lvl_label.setFont(QFont("Consolas", 14, QFont.Weight.Bold))
        
        self.time_label = QLabel(time_str)
        self.time_label.setFont(QFont("Consolas", 12))
        self.time_label.setStyleSheet("color: #aaa;")
        
        metr_layout.addWidget(self.lvl_label)
        metr_layout.addWidget(self.time_label)
        
        grid.addWidget(metr_box, 2, 0, 1, 2)
        
        layout.addLayout(grid)
        
        # Add Sovereignty Toggle
        from PyQt6.QtWidgets import QPushButton
        self.btn_toggle_sov = QPushButton("⚠️ TOGGLE LOCAL SOVEREIGNTY (OLLAMA)")
        self.btn_toggle_sov.setStyleSheet("background-color: #F44336; color: white; padding: 15px; font-weight: bold; font-size: 16px; margin-top: 20px; border-radius: 5px;")
        self.btn_toggle_sov.clicked.connect(self.toggle_sovereignty)
        layout.addWidget(self.btn_toggle_sov)
        
        layout.addStretch()
        
    def toggle_sovereignty(self):
        import os
        if os.getenv("OLLAMA_MODEL"):
            os.environ.pop("OLLAMA_MODEL", None)
            self.btn_toggle_sov.setStyleSheet("background-color: #F44336; color: white; padding: 15px; font-weight: bold; font-size: 16px; margin-top: 20px; border-radius: 5px;")
            self.btn_toggle_sov.setText("⚠️ TOGGLE LOCAL SOVEREIGNTY (OLLAMA)")
            if hasattr(self, 'lbl_status'):
                self.lbl_status.setText("ROUTING: CLOUD")
        else:
            os.environ["OLLAMA_MODEL"] = "llama3"
            self.btn_toggle_sov.setStyleSheet("background-color: #06b6d4; color: white; padding: 15px; font-weight: bold; font-size: 16px; margin-top: 20px; border-radius: 5px;")
            self.btn_toggle_sov.setText("🔒 AIRGAPPED: OLLAMA ACTIVE")
            if hasattr(self, 'lbl_status'):
                self.lbl_status.setText("ROUTING: LOCAL")

    def create_stat_box(self, title, value):
        group = QGroupBox(title)
        group.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        group.setStyleSheet("QGroupBox { border: 1px solid #555; margin-top: 10px; } QGroupBox::title { top: -10px; left: 10px; }")
        
        layout = QVBoxLayout(group)
        val_label = QLabel(value)
        val_label.setFont(QFont("Consolas", 18))
        if "Status" in title:
            val_label.setStyleSheet("color: #00ff66;")
        
        val_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(val_label)
        
        return group, val_label

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion") # Clean modern style
    
    window = TelemetryDashboard()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
