def tool_implement_a_local_py(data):
    # Example local processing function (replace this with actual computation)
    return [x**2 for x in data]

def test_suite():
    assert tool_implement_a_local_py([1, 2, 3]) == [1, 4, 9], "Test failed for input [1, 2, 3]"
    assert tool_implement_a_local_py([-5, -4, -3]) == [25, 16, 9], "Test failed for input [-5, -4, -3]"
    print("All tests passed!")

test_suite()