## Requirements

Python 3.7 or above

## How to Run

Using the command to execute Python 3 on your machine, pass the path to "resolver.py" as an argument. Optionally, the path to a text file containing your input can be passed as an additional argument. If this is not provided, standard input is used. Assuming the input is formatted correctly (as explained below), either "The consequent is entailed." or "The consequent is not entailed." is printed to standard output.

## Format

Input should consist of a series of at least two non-empty clauses, one per line, each clause consisting of comma-separated literals. The last clause is assumed to be the negation of the consequent. Lines consisting entirely of whitespace are ignored, as is whitespace between a literal and a comma. A literal should consist entirely of alphanumeric ASCII characters and underscores, possibly prepended by the logical "not" symbol, an exclamation point.
