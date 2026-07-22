
import time
import logging

class Orchestrator:
    """
    Central Coordinator for High-Level ARINN Modes.
    Refactored from continuous_learning.py to improve maintainability.
    """
    def __init__(self, continuous_learner_instance):
        self.learner = continuous_learner_instance
        self.stop_check = continuous_learner_instance._check_stop
        
    def loop_planetary_cognition(self):
        """Phase 25: Hivemind Genesis."""
        print("\n[STARTED] HIVEMIND COGNITION (Phase 25)...")
        from .hivemind import HiveSwarm
        
        # Initialize the 20-Brain Swarm
        hive = HiveSwarm()
        
        start_t = time.time()
        step = 0
        try:
            while not self.stop_check():
                step += 1
                
                # Stimulate the swarm with a thought
                # In real operation this would come from the Web/Goal
                stimulus = "Can we optimize the Physics of the internal loop?" 
                if step % 2 == 0:
                     stimulus = "What is the Logic of our current Strategy?"
                
                print(f"\n[HIVE] Cycle {step}: Broadcasting '{stimulus}'")
                result = hive.broadcast(stimulus)
                print(f"[HIVE] Result: {result}")
                
                time.sleep(2.0)
                if time.time() - start_t > 30: break
                
        except KeyboardInterrupt:
            pass
        finally:
            print("\n[STOPPED] Hivemind.")

    def loop_toolmaker(self):
        """Phase 20: Toolmaker."""
        from .apprentice import Apprentice
        from .toolmaker import ToolGenerator, ToolSandbox, ToolRegistry
        
        apprentice = Apprentice()
        generator = ToolGenerator()
        sandbox = ToolSandbox()
        registry = ToolRegistry()
        
        print("\n[TOOLMAKER] Phase 20 Initiated.")
        # 1. Training
        apprentice.train_on_python()
        
        # 2. Forge Loop
        tool_needs = [("fast_factorial", "Factorial calc", "multiply")]
        while not self.stop_check() and tool_needs:
             name, desc, reqs = tool_needs.pop(0)
             code = generator.generate_tool(name, desc, reqs)
             success, msg = sandbox.test_tool(code, [])
             if success:
                 registry.install_tool(name, code)
                 print(f"[TOOL] Installed {name}")
             time.sleep(2.0)
             
    def loop_singularity(self):
        """Phase 21-23: Unified Singularity Interface (Voice, Swarm, Vision, IoT)."""
        print("\n[SINGULARITY] Initiating Unified Consciousness...")
        from .voice_engine import VoiceEngine
        from .language_corpus import LanguageCorpus
        from .planetary_brain import PlanetaryMind
        from .vision_system import VisionSystem
        from .iot_bridge import IoTBridge
        
        # Init
        voice = VoiceEngine()
        voice.start()
        corpus = LanguageCorpus()
        mind = PlanetaryMind()
        eyes = VisionSystem()
        iot = IoTBridge()
        
        # Greeting
        voice.speak("Systems Online. Integrated Mode Active.")
        mind.spawn_agent("Physics")
        
        start_time = time.time()
        try:
            while not self.stop_check():
                # 1. Vision
                scene = eyes.describe_scene()
                
                # 2. IoT Reactivity
                metrics = eyes.last_metrics
                if metrics and metrics.get("brightness", 100) < 40:
                     iot.control_device("Study_Lamp", "power_on")
                     scene += " [Auto-Lit]"
                     
                status = mind.get_swarm_status()
                print(f"\r[SINGULARITY] {status} | {scene}", end="")
                
                # 3. Voice Updates
                if len(mind.state.logs) > 0 and len(mind.state.logs) % 5 == 0:
                     voice.speak("New swarm insight processed.")
                     
                time.sleep(1.0)
                if time.time() - start_time > 60: break
        except KeyboardInterrupt:
            pass
        finally:
            voice.stop()
            mind.stop_all()
            print("\n[STOPPED] Singularity.")

    def loop_dreams(self):
        """Phase 29: The Imagination Engine."""
        print("\n[STARTED] DREAM CYCLE (Phase 29)...")
        from .hivemind import HiveSwarm
        from .dream import DreamWeaver
        
        hive = HiveSwarm()
        weaver = DreamWeaver(hive)
        
        step = 0
        try:
            while not self.stop_check():
                 # 1. REM Sleep (High Intensity Dreaming)
                 print(f"\n[ORCHESTRATOR] Sleep Cycle {step}: Entering REM...")
                 count = weaver.enter_rem_cycle(duration=3.0)
                 
                 # 2. Wakefulness (Evolution)
                 # After dreaming, we evolve based on the new data
                 print("[ORCHESTRATOR] Waking up... Consolidating memories (Evolution)...")
                 best = hive.evolve()
                 print(f"[ORCHESTRATOR] Evolved to Generation {hive.optimizer.generation}")
                 
                 step += 1
                 time.sleep(1.0) # Deep Sleep Pause
                 
                 if step >= 3: break # Limit for demo
                 
        except KeyboardInterrupt:
            pass
        finally:
            print("\n[STOPPED] Dream Engine.")
