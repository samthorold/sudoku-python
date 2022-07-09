"""

https://en.wikipedia.org/wiki/Dancing_Links

- 9 columns for the cell values
- 81 columns for the cells
- 9 columns for the rows
- 9 columns for the columns
- 9 columns for the boxes

Columns as elements of a universe and rows as subsets and the problem is to
cover the universe with disjoint subsets.
"""


from sudoku.solve.dlx.solve import solve
