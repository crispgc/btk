class Variant:
    chromosome = None
    start = None
    ref = None
    alt = None

    def __init__(self, chromosome: str, start: int, ref: str, alt: str):
        self.chromosome = chromosome
        self.start = start
        self.ref = ref
        self.alt = alt

    def __repr__(self):
        return f"{self.chromosome}:{self.start}-{self.ref}>{self.alt}"

    def __str__(self):
        return f"{self.chromosome}:{self.start}-{self.ref}>{self.alt}"

    def _check_position(self):
        pass
