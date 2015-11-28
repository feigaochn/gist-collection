import pytest

def test_obvious():
    assert True == True

def test_fail():
    assert True == False

if __name__ == '__main__':
    pytest.main()
