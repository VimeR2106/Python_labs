from Lab_1 import _04_my_family

def test_family():
    assert isinstance(_04_my_family.my_family, list)
    assert len(_04_my_family.my_family) > 0
