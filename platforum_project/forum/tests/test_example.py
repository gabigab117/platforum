# import pytest
#
#
# @pytest.fixture(scope="session")
# def fixture_1():
#     print("run-fix 1")
#     return 1
#
#
# def test_example(fixture_1):
#     print("ex 1")
#     assert 2 == 2
#
#
# def test_example2(fixture_1):
#     print("ex 2")
#     num = fixture_1
#     assert num == 1
