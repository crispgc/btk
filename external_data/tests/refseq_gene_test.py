import pytest
import external_data.refseq as refseq

db = refseq.RefSeq()
results = db.query_gene('BRCA1')
first_region = results[0]

def test_region_gene():
    expected = ['17', '41197694', '41197819', 'BRCA1', 'NM_007300', '24']
    assert results[0] == expected, "Returned region does not match"

def test_wrong_gene():
    assert "BRCA2" != first_region[3], "Returned region does not match"
