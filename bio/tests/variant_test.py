import pytest
import bio.variant as variant

def test_file1_method1():
    v = variant.Variant("1", 10, "C", "T")
    
    assert v.chromosome == "1", "test failed"
