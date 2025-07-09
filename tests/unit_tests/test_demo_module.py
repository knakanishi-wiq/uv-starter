from uv_starter.demo_module import add


def test_add_should_return_the_sum_of_two_numbers():
    assert add(1, 2) == 3
