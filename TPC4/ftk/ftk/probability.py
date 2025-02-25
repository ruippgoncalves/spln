import math
from abc import ABC


class Probability(ABC):
    def __init__(self, count: int, total: int):
        if not (0 <= count <= total):
            raise ValueError("Count must be between 0 and total.")
        self.count = count
        self.total = total

    @property
    def value(self):
        return self.count

    def __add__(self, other):
        if not isinstance(other, Probability):
            return NotImplemented
        return self.__class__(self.count + other.count, self.total + other.total)

    def __sub__(self, other):
        if not isinstance(other, Probability):
            return NotImplemented
        return self.__class__(max(self.count - other.count, 0), max(self.total, other.total))

    def __repr__(self):
        return f"{self.value:.2f}"

class AbsoluteProbability(Probability):
    pass

class RelativeProbability(Probability):
    @property
    def value(self):
        return self.count / self.total if self.total > 0 else 0.0

class LogarithmicProbability(Probability):
    @property
    def value(self):
        return math.log(self.count / self.total) if self.count > 0 and self.total > 0 else float('-inf')
