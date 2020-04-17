import sys
import re
from dataclasses import dataclass
from typing import FrozenSet, Iterable
from itertools import chain, filterfalse, combinations

DEFAULT_NOT = '!'
DEFAULT_LITERAL_SEP = ','

# TODO: Make configurable via command-line arguments.
not_symbol = DEFAULT_NOT
literal_sep = DEFAULT_LITERAL_SEP

@dataclass(frozen=True)
class Literal:
    """A possibly negated proposition variable. Immutable."""

    @classmethod
    def from_string(cls, string):
        """If `not_symbol` is a prefix of `string`, returns a negated
        `Literal` whose value is the portion of `string` following the
        prefix. Otherwise, returns a `Literal` with value `string`."""
        if string.startswith(not_symbol):
            return cls(string[len(not_symbol):], True)
        else:
            return cls(string, False)

    value: str
    negated: bool = False

    def __invert__(self):
        """Returns the logical negation of `self`."""
        return Literal(self.value, not self.negated)

    def __str__(self):
        """Returns `str(self)`."""
        return not_symbol + self.value

Clause = FrozenSet[Literal]

def resolve(a: Clause, b: Clause):
    """Performs resolution on `a` and `b`, collapsing any tautologies.

    If the disjunction of `a` and `b` contains more than one pair of
    complementary literals, only tautologies will result, and `None` is
    returned. If no resolvents are produced, `None` is returned.
    Otherwise, a single resolvent is produced, and it is returned.
    """
    values = {}
    for x in chain(a, b):
        values[x.value] = values.get(x.value, 0) | (1 << x.negated)
    literals = []
    found_comp_pair = False
    for x, n in values.items():
        if n == 3:
            if found_comp_pair:
                return None
            found_comp_pair = True
        else:
            literals.append(Literal(x, bool(n - 1)))
    return frozenset(literals) if found_comp_pair else None

def is_tautology(clause):
    for literal in clause:
        if ~literal in clause:
            return True
    return False

def entails(kb: Iterable[Clause], a: Clause):
    """Returns whether `kb` entails `a` or not."""
    conjunction = set(filterfalse(is_tautology, kb))
    if not is_tautology(a):
        conjunction.add(a)
    resolvents = []
    while True:
        for a, b in combinations(conjunction, 2):
            x = resolve(a, b)
            if x is not None:
                if len(x):
                    resolvents.append(x)
                else:
                    return True
        former_len = len(conjunction)
        conjunction.update(resolvents)
        if len(conjunction) == former_len:
            return False
        resolvents.clear()

def main():
    clauses = []
    clause_re = re.compile(rf"{not_symbol}?\w+", re.ASCII)
    src = open(sys.argv[1]) if len(sys.argv) > 1 else sys.stdin
    try:
        for line in src:
            if line.isspace():
                continue
            literals = set()
            for token in map(str.strip, line.rstrip().split(literal_sep)):
                if not clause_re.fullmatch(token):
                    raise ValueError(f"\"{token}\" is not formatted correctly.")
                literals.add(Literal.from_string(token))
            clauses.append(frozenset(literals))
    finally:
        if src != sys.stdin:
            src.close()
    if len(clauses) < 2:
        raise ValueError("There are fewer than two non-empty clauses.")
    if entails(clauses[:-1], clauses[-1]):
        print("The consequent is entailed.")
    else:
        print("The consequent is not entailed.")

main()
