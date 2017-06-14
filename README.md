This is a basic example of a genetic algorithm solving the 8 queens puzzle.
It can be easily expanded to solve the N queens puzzle problem.

Some assumptions I made:

- At least on column from each parent is transferred to the child.
- The mutation percentage is applied to each individual column.
- One cannot select the same parent, though I learned that this was still possible
in the case that two or more of the lists in the parent set are identical.