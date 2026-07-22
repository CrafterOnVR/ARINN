
import sys
import os

print("Testing Imports...")
try:
    print("1. Importing NeuralCore...")
    from arinn_core.neural_core import NeuralCore  # type: ignore
    print("   Done.")
    
    print("2. Importing HiveSwarm...")
    from arinn_core.hivemind import HiveSwarm  # type: ignore
    print("   Done.")

    print("3. Importing GenesisEngine...")
    from genesis import GenesisEngine  # type: ignore
    print("   Done.")
    
    print("4. Initializing GenesisEngine...")
    engine = GenesisEngine()
    print("   Done.")
    
    print("SUCCESS: Genesis V1.3 Components are healthy.")
except Exception as e:
    print(f"CRASH: {e}")
    import traceback
    traceback.print_exc()
