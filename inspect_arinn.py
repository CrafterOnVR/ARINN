import os
import torch
from arinn_core.identity import ArinnIdentity
from arinn_core.bootloader import Phase

def inspect():
    print("==================================================")
    print("      ARINN NEURAL & MEMORY INSPECTION TOOL       ")
    print("==================================================")
    
    if not os.path.exists("bootloader_state.json"):
        print("ERROR: No bootloader state found. Run 'python test_arinn_core.py' or 'python __main__.py' first.")
        return

    # Initialize Identity (loads brain, memory, bootloader)
    arinn = ArinnIdentity()
    
    # 1. Inspect Bootloader Phase
    print(f"\n[GROWTH STATUS] Current Phase: {arinn.bootloader.current_phase.name}")
    if arinn.bootloader.current_phase == Phase.AUTONOMOUS_SCHOLAR:
        print(">> STATUS: FULLY GROWN. Ready for research.")
    else:
        print(">> STATUS: GROWING. Please run agent to continue growth.")

    # 2. Inspect Secure Memory (Proof of Meta-Learning & Internal Voice)
    print("\n[SECURE MEMORY DUMP]")
    keys = arinn.memory.list_keys()
    print(f"Index Keys Found: {keys}")
    
    lr = arinn.memory.retrieve("optimized_learning_rate")
    print(f">> LEARNING RATE (Meta-Learned): {lr}")
    
    cmap = arinn.memory.retrieve("compression_map")
    if cmap:
        print(f">> INTERNAL VOICE (Compression Map):")
        for k, v in list(cmap.items())[:5]: # Show first 5
            print(f"   '{k}' -> '{v}'")
        print("   (etc...)")
    else:
        print(">> INTERNAL VOICE: Not yet developed.")
        
    opt = arinn.memory.retrieve("optimization_applied")
    print(f">> SYSTEM OPTIMIZATION: {opt}")

    # 3. Inspect Brain (Proof of Logic Gates / Efficiency)
    print("\n[NEURAL BRAIN DIAGNOSTICS]")
    print(f"Device: {arinn.brain.device}")
    
    # Check for quantization
    is_quantized = False
    for name, module in arinn.brain.model.named_modules():
        if isinstance(module, torch.nn.quantized.dynamic.modules.linear.Linear):
            is_quantized = True
            print(f">> DETECTED QUANTIZED LAYER: {name} (qint8)")
            
    if is_quantized:
        print(">> BRAIN EFFICIENCY: QUANTIZED (INT8 Mode Active)")
    else:
        print(">> BRAIN EFFICIENCY: STANDARD (FP32 Mode)")

    # Run Inference Test (XOR)
    print("\n[LOGIC GATE TEST (XOR)]")
    inputs = [[0,0], [0,1], [1,0], [1,1]]
    outputs = arinn.brain.infer(inputs)
    print(f"Input: {inputs}")
    print(f"Raw Output: {outputs.flatten()}")
    
    # Interpret
    correct = True
    preds = []
    expected = [0, 1, 1, 0]
    for i, val in enumerate(outputs.flatten()):
        pred = 1 if val > 0.5 else 0
        preds.append(pred)
        if pred != expected[i]:
            correct = False
            
    print(f"Predictions: {preds} (Expected: {expected})")
    if correct:
        print(">> COGNITIVE CHECK: PASSED (Logic Verified)")
    else:
        print(">> COGNITIVE CHECK: FAILED (Retraining Needed)")

    print("\n==================================================")

if __name__ == "__main__":
    inspect()
