from external_data.ncbi import UCSC

class RefSeq(UCSC):
    def query_full_refseq(self, remove_utr=True):
        # chroms = ['chr' + str(i) for i in range(1, 23)] + ['chrX', 'chrY']

        query = "select * from refGene"

        data = self.execute_query(query)

        if remove_utr is True:
            data, nm_recovered = self._remove_utrs(data)

        return data

    def query_gene(self, gene, remove_utr=True):
        query = f"SELECT * FROM refGene" +\
                f" WHERE name2 = '{gene}'"
        data = self.execute_query(query)
        if remove_utr is True:
            data, nm_recovered = self._remove_utrs(data)

        return data

    @staticmethod
    def _remove_utrs(data):

        regions = []
        nm_list = []
        c = 0

        for line in data:

            nm_list.append(line[1])
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

                # print(line)
                # print(exon_names)
                # c += 1
                #
                # if c == 10:
                #     exit(1)

            if cds_start == cds_end:
                cds_start = int(line[4])
                cds_end = int(line[5])

            for start, end in zip(exons_start, exons_end):
                exon_idx += 1

                start = int(start)
                end = int(end)
                region = list(line)
                exon_id = exon_names[exon_idx]

                region[2] = region[2].strip("chr")
                genename = str(region[12])
                transcript_name = str(region[1])

                # Regions that are 5UTR or 3UTR
                if start < cds_start and end < cds_start:
                    continue
                if start > cds_end and end > cds_end:
                    continue

                # Regions of just one gene
                if start <= cds_start and end >= cds_end:
                    region[9] = cds_start
                    region[10] = cds_end
                    regions.append([str(region[2]), str(region[9]), str(region[10]),
                                    genename, transcript_name, str(exon_id)])
                    continue

                # Cutting in 5'
                if start <= cds_start <= end:
                    region[9] = cds_start
                    region[10] = end
                    regions.append([str(region[2]), str(region[9]), str(region[10]),
                                    genename, transcript_name, str(exon_id)])
                    continue

                # Cutting in 3'
                if start <= cds_end <= end:
                    region[9] = start
                    region[10] = cds_end
                    regions.append([str(region[2]), str(region[9]), str(region[10]),
                                    genename, transcript_name, str(exon_id)])
                    continue

                # Normal Exon
                if start >= cds_start and end <= cds_end:
                    region[9] = start
                    region[10] = end
                    regions.append([str(region[2]), str(region[9]), str(region[10]),
                                    genename, transcript_name, str(exon_id)])
                    continue

            # c += 1

        print("#[LOG]: Extracted " + str(c) + " NMs")
        return regions, nm_list


def main():
    ucsc = RefSeq()
    data = ucsc.query_full_refseq()

    outfh = open("./full_refseq.bed", 'w')
    for d in data:
        # d[3] = '_'.join([d[3], d[4], d[5]])
        outfh.write("\t".join(d) + '\n')
    outfh.close()


if __name__ == "__main__":
    main()
