import pytest
import external_data.refseq as refseq

def test_file1_method1():
    db = refseq.RefSeq()
    results = db.query_gene('BRCA1')
    print(results[0])
    expected = ['17', '41197694', '41197819', 'BRCA1', 'NM_007300', '24']
    assert results[0] == expected, "Returned region does not match"
