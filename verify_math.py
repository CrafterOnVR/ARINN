
from arinn_core.math_cortex import MathCortex

def run_math_test():
    print("\n[PHASE 54] Testing Calculator Protocol...")
    cortex = MathCortex()
    
    # 1. Simple Test
    q1 = "Calculate 12345 * 67890"
    expected = 12345 * 67890
    print(f"  > Query: {q1}")
    print(f"  > Expected: {expected}")
    
    res = cortex.process(q1)
    print(f"  > Result: {res}")
    
    if res == expected:
        print("  > Success: Exact Match.")
    else:
        print("  > Failure: Math Mismatch.")
        exit(1)
        
    # 2. Complex Test (Float)
    q2 = "Calculate 100 / 3"
    print(f"  > Query: {q2}")
    res2 = cortex.process(q2)
    print(f"  > Result: {res2}")
    if abs(res2 - 33.333333333333336) < 0.0001:
        print("  > Success: Float Precision.")
    else:
        print("  > Failure: Precision Error.")
        exit(1)

    print("[PHASE 54] Calculator Verified. Agent is using Tools.")

if __name__ == "__main__":
    run_math_test()
