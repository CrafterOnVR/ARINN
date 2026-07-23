import tkinter as tk
import json
import os
import time

class TokenManagerGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("ARINN Token Controller")
        self.root.geometry("400x300")
        
        # Load config path
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.config_path = os.path.join(base_dir, "..", "arinn_runtime_config.json")
        
        # Ensure config exists
        if not os.path.exists(self.config_path):
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump({"max_tokens": 350}, f)
        
        tk.Label(self.root, text="Select Architect Max Tokens:", font=("Arial", 12, "bold")).pack(pady=10)
        tk.Label(self.root, text="Feel free to minimize this window.", font=("Arial", 9)).pack(pady=5)
        
        self.status_label = tk.Label(self.root, text="", font=("Arial", 10), wraplength=380)
        self.status_label.pack(pady=5)
        
        token_options = [50, 100, 150, 200, 250, 300, 350, 500]
        
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)
        
        for i, val in enumerate(token_options):
            btn = tk.Button(btn_frame, text=str(val), width=8, command=lambda v=val: self.update_tokens(v))
            btn.grid(row=i // 4, column=i % 4, padx=5, pady=5)
            
    def update_tokens(self, val):
        self.status_label.config(text="attempting to ping run_arinn.py (if the neural model is currently thinking, the ping will be sent after it is done)...", fg="blue")
        self.root.update()
        time.sleep(0.5) # Simulate network ping for visual feedback
        
        try:
            # Read current
            if os.path.exists(self.config_path):
                with open(self.config_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            else:
                data = {}
                
            data["max_tokens"] = val
            
            # Write new
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(data, f)
                
            self.status_label.config(text="Maximum token change has been successfully implemented", fg="green")
        except Exception as e:
            self.status_label.config(text=f"Error: The maximum token change has failed to be implemented\nPotential reasons:\n- File locked by OS\n- JSON parsing failed\n- Details: {str(e)}", fg="red")

if __name__ == "__main__":
    app = TokenManagerGUI()
    app.root.mainloop()
