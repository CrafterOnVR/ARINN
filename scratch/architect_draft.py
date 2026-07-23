import numpy as np

def tool_implement_a_local_py(data):
    # Implementing mathematical operation for processing data efficiently.
    result = np.sum(data) / len(data)
    return result

def test_suite():
    test_data_1 = [1, 2, 3, 4]
    assert abs(tool_implement_a_local_py(test_data_1) - 2.5) < 1e-6
    
    test_data_2 = [-1, -2, -3, -4]
    assert abs(tool_implement_a_local_py(test_data_2) + 2.5) < 1e-6
    
    print("All tests passed successfully.")

# Example usage:
example_data = np.array([10, 20, 30])
print(tool_implement_a_local_py(example_data))  # Should output 20.0

test_suite()