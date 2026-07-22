
import unittest
from arinn_core.hivemind import HiveSwarm  # type: ignore
from arinn_core.evolution import Genome  # type: ignore

class TestEvolution(unittest.TestCase):
    def test_01_natural_selection(self):
        print("\n[TEST] Verifying Darwin Engine...")
        hive = HiveSwarm()
        
        initial_gen = hive.optimizer.generation
        initial_genome = str(hive.brains[0].genome)
        print(f"  > Gen {initial_gen} Genome: {initial_genome}")
        
        # Run Evolution Loop
        print("  > Simulating 5 Generations of Natural Selection...")
        for _ in range(5):
            best = hive.evolve()
            
        final_gen = hive.optimizer.generation
        final_genome = str(hive.brains[0].genome)
        print(f"  > Gen {final_gen} Genome: {final_genome}")
        
        self.assertEqual(final_gen, initial_gen + 5, "Generations did not advance")
        self.assertNotEqual(initial_genome, final_genome, "Evolution failed to mutate genome")

if __name__ == '__main__':
    unittest.main()
