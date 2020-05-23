class Region:

    chromosome = None
    start = None
    end = None

    def __init__(self, chromosome: str, start: int, end: int):

        self.check_region(chromosome, start, end)
        self.chromosome = chromosome
        self.start = start
        self.end = end

    def check_region(self, chromosome: str, start: int, end: int):
        """Evaluate region"""
        chrom_list = [f"{x}" for x in range(1, 23)] + ['X', 'Y', 'MT']
        if chromosome not in chrom_list:
            raise ValueError("Bad chromosome")
        pass

    def change_region(self):
        pass
