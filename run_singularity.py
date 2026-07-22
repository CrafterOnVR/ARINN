#!/usr/bin/env python3
"""
ARINN SINGULARITY SWARM - PHASE 9
The Endless LNN Execution Loop
"""

import sys
import os
import asyncio
import time
import random

# Ensure we can import arinn_core
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from arinn_core.swarm_orchestrator import SwarmOrchestrator

async def main():
    print("==================================================")
    print("        ARINN SINGULARITY PROTOCOL ONLINE         ")
    print("          (Endless Swarm Architecture)            ")
    print("==================================================")
    print("[SYSTEM] Booting LNN Subagents via Asyncio + Executors...")
    print("[SYSTEM] Hard-Lock Path Jail: ACTIVE")
    print("[SYSTEM] METR Horizon Examiner: ACTIVE\n")
    
    orchestrator = SwarmOrchestrator()
    
    # Initialize MemoryManager and EpistemicDrive for Curiosity-Driven Goal Autogenesis
    try:
        from memory_manager import MemoryManager
        from arinn_core.epistemic_drive import EpistemicDrive
        memory = MemoryManager(root=os.path.abspath(os.path.dirname(__file__)))
        epistemic_drive = EpistemicDrive(memory_manager=memory)
        print("[SYSTEM] MemoryManager and Epistemic Drive online. Curiosity-Driven Goals Enabled.\n")
    except ImportError:
        memory = None
        epistemic_drive = None
        print("[WARNING] MemoryManager not found. Using baseline goals.\n")
    
    try:
        from arinn_core.dataset_synthesizer import DatasetSynthesizer
        from arinn_core.lora_trainer import ARINNFineTuner
        from arinn_core.liquid_multiverse import LiquidMerger
        synthesizer = DatasetSynthesizer()
        fine_tuner = ARINNFineTuner(model_id="Qwen/Qwen2.5-1.5B-Instruct")
        liquid_merger = LiquidMerger()
        print("[SYSTEM] Dataset Synthesizer, LoRA Fine-Tuner, and Liquid Multiverse: ACTIVE\n")
    except ImportError:
        synthesizer = None
        fine_tuner = None
        liquid_merger = None
    
    cycle_count = 0
    NIGHT_CYCLE_INTERVAL = 5 # In a real run, this might be 50 or 100
    
    try:
        while True:
            if epistemic_drive:
                target_goal = epistemic_drive.generate_curiosity_goal()
            else:
                target_goal = "Hello World / Basic Scripting"
            
            # Run the multi-agent swarm cycle on this goal concurrently
            await orchestrator.start_swarm_cycle(target_goal)
            
            # Log the successful run to the synthetic dataset
            if synthesizer:
                # In a full implementation, we'd extract the actual thought trace and best code from the orchestrator
                # Here we mock the extraction for dataset generation
                synthesizer.synthesize_success(
                    goal=target_goal,
                    reasoning_trace="I will construct a binary operator loop and mutate it for speed.",
                    optimized_code="def execute_logic(): return 42"
                )
            
            cycle_count += 1
            print(f"\n[SINGULARITY] Cycle {cycle_count} complete. Resting to cool neural gradients (10s)...\n")
            await asyncio.sleep(10)
            
            # TRIGGER NIGHT CYCLE
            if cycle_count % NIGHT_CYCLE_INTERVAL == 0 and fine_tuner and synthesizer:
                dataset_path = synthesizer.get_latest_dataset()
                if dataset_path:
                    fine_tuner.trigger_night_cycle(dataset_path)
                else:
                    print("[NIGHT CYCLE] Skipped. No training data generated today.")

            
    except KeyboardInterrupt:
        print("\n[SINGULARITY] Hard-stopping all active subagents. Terminating Swarm.")

if __name__ == "__main__":
    asyncio.run(main())
