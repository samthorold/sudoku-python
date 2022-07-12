"""

https://en.wikipedia.org/wiki/Dancing_Links

- 9 columns for the cell values
- 81 columns for the cells
- 9 columns for the rows
- 9 columns for the columns
- 9 columns for the boxes

Columns as elements of a universe and rows as subsets and the problem is to
cover the universe with disjoint subsets.

Choose a subset of rows such that the columns have a single 1.

x11, x12, 013, ..., x97, x98, x99, xr1, xr2, ..., xc1, xc2, ..., xb1, ..., xb9
"""


from sudoku.solve.dlx.solve import solve
