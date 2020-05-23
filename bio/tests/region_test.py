import pytest
import bio.region as region

def test_region_method1():
    r = region.Region("1", 100, 200)
    print(r.chromosome)
    assert r.chromosome == "1", "Chromosome does not match expected"

def test_file1_method2():
    with pytest.raises(ValueError) as e_info:
        r = region.Region("Z", 100, 200)