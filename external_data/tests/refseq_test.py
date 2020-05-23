import pytest
import external_data.refseq as refseq

db = refseq.RefSeq()
results = db.query_gene('BRCA1')

def test_format():
    first_region = results[0]
    chromosome, start, end, gene, tx, exon = first_region
    print(first_region)
    assert chromosome in [f"{x}" for x in range(1, 23)] + ['X', 'Y', 'MT']
    assert 41100000 < int(start) < 41200000
    assert 41100000 < int(end) < 41200000
    assert tx[0:3] == "NM_"
    assert isinstance(int(24), int)

def test_number_of_nms():
    nm_list = set(i[4] for i in results)
    print(nm_list)
    expected_nm_list = sorted(['NM_007299', 'NM_007294', 'NM_007297', 'NR_027676', 'NM_007298', 'NM_007300'])
    assert sorted(nm_list) == expected_nm_list, "Wrong transcripts"
