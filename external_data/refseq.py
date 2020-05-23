import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from external_data.ncbi import UCSC

class RefSeq(UCSC):

    returned_nm = set()
    
    def query_full_refseq(self, remove_utr=True):

        query = "SELECT * FROM refGene"
        data = self.execute_query(query)
        data = self._remove_utrs(data) if remove_utr is True else data
        return data

    def query_gene(self, gene, remove_utr=True):
        query = f"SELECT * FROM refGene WHERE name2 = '{gene}'"
        data = self.execute_query(query)
        data = self._remove_utrs(data) if remove_utr is True else data
        return data

    def query_transcript(self, transcript, remove_utr=True):
        query = f"SELECT * FROM refGene WHERE name = '{transcript}'"
        data = self.execute_query(query)
        data = self._remove_utrs(data) if remove_utr is True else data
        return data

    def _remove_utrs(self, data):

        regions = []
        nm_set = set()

        for line in data:

            nm_set.add(line[1])
            exon_idx = -1

            # Get the start and end of the exons in two lists
            exons_start = line[9].decode('UTF-8').split(',')[0:-1]
            exons_end = line[10].decode('UTF-8').split(',')[0:-1]
            strand = line[3]

            # Get the coding start and the coding end of the transcript
            cds_start, cds_end = int(line[6]), int(line[7])

            # If negative strand, reverse the names of the exons
            exon_names = list(range(1, len(exons_start) + 1))
            if strand == '-':
                exon_names = list(reversed(exon_names))

            if cds_start == cds_end:
                cds_start, cds_end = int(line[4]), int(line[5])

            for start, end in zip(exons_start, exons_end):
                exon_idx += 1

                start, end = int(start), int(end)
                region = list(line)
                exon_id = exon_names[exon_idx]
                chromosome = region[2].strip("chr")
                genename, transcript_name = str(region[12]), str(region[1])
                found = False

                # Regions that are 5UTR or 3UTR
                if start < cds_start and end < cds_start:
                    found = True
                if found is False and start > cds_end and end > cds_end:
                    found = True

                # Regions of just one gene
                if found is False and start <= cds_start and end >= cds_end:
                    found = True
                    region[9], region[10] = cds_start, cds_end

                # Cutting in 5'
                if found is False and start <= cds_start <= end:
                    found = True
                    region[9], region[10] = cds_start, end

                # Cutting in 3'
                if found is False and start <= cds_end <= end:
                    found = True
                    region[9], region[10] = start, cds_end

                # Normal Exon
                if found is False and start >= cds_start and end <= cds_end:
                    found = True
                    region[9], region[10] = start, end

                regions.append([chromosome, str(region[9]), str(region[10]),
                                genename, transcript_name, str(exon_id)])

        print(f"#[LOG]: Extracted {len(nm_set)} NMs")
        self.returned_nm = nm_set
        return regions


def main():
    ucsc = RefSeq()
    data = ucsc.query_full_refseq()

    outfh = open("./full_refseq.bed", 'w')
    for d in data:
        outfh.write("\t".join(d) + '\n')
    outfh.close()

if __name__ == "__main__":
    main()
