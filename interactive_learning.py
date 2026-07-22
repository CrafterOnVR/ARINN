
import sys
import os
from arinn_core.identity import ArinnIdentity
from arinn_core.continuous_learning import ContinuousLearner

def main():
    print("Initializing ARINN for Continuous Learning Mode...")
    arinn = ArinnIdentity()
    learner = ContinuousLearner(arinn)
    
    while True:
        print("\n========================================")
        print("   ARINN CONTINUOUS LEARNING TERMINAL   ")
        print("========================================")
        print("1. Learn how to learn (Meta-Optimization)")
        print("2. Learn how to learn faster (Efficiency/Pruning)")
        print("3. Learning Simple Topics (XOR, OR, AND, MATH)")
        print("4. Learning how to Reasoning (Vocabulary)")
        print("5. Real-World Learning (Verified Sources Only) [NEW]")
        print("6. The Apprentice (Coding Curriculum) [NEW]")
        print("7. Acceleration Curriculum (High-Leverage) [NEW]")
        print("Q. Quit")
        
        choice = input("\nSelect Mode (1-7): ").lower()
        
        if choice == '1':
            learner.loop_meta_learning()
        elif choice == '2':
            learner.loop_efficiency()
        elif choice == '3':
            learner.loop_simple_topics()
        elif choice == '4':
            learner.loop_reasoning()
        elif choice == '5':
            learner.loop_real_world_learning()
        elif choice == '6':
            learner.loop_coding_practice()
        elif choice == '7':
            learner.loop_acceleration_study()
        elif choice == 'q':
            print("Exiting interactive learning.")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
