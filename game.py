
from random import *
import numpy as np
from ab import *

infinity = float('inf')


state = {
"team-code": "eef8976e",
"game": "connect_more",
"opponent-name": "mighty_ducks",
"columns": 6,
"connect_n": 5,
"your-token": "R",
"board": [
["R","Y"],
["R"],
[],
["R",],
["Y","Y"],
[],
]
}




def max_col_height(matrix):
    max_length = 0
    for i in matrix:
        max_length = max(max_length, len(i))
    return max_length

def board_to_matrix(matrix, d, consecutive):
    mat = matrix
    max_height = max_col_height(matrix)
    for l in matrix:
        for j in range(max_height+(2*d//len(mat))+consecutive-len(l)):
            l.append(0)
    return mat

def get_move(state):
# Your code can be called from here however you like
# You are allowed the use of load_data() and save_data(info)
    info = load_data()
# But you must return a valid move that looks like the following:

    move = {
        "move": 2, # Column in which you will move (create mark "your-token")
        "team-code": "eef8976e" # Must match the code received in the state object
    }

    return move

#https://codereview.stackexchange.com/questions/39561/searching-a-2d-matrix-for-a-consecutive-sequence
def terminate_game(matrix, consecutive):
    string_matrix = []

    #diags
    for w in matrix_diagonals(matrix):
        string_matrix.append("".join(map(str, w)))

    #cols
    for w in matrix:
        string_matrix.append("".join(map(str, w)))
    #rows
    for w in list(map(list, zip(*matrix))):
        string_matrix.append("".join(map(str, w)))
    print(string_matrix)

    for w in string_matrix:
        if(consecutive*("1") in w):
            return 1
    for w in string_matrix:
        if (consecutive * ("2") in w):
            return 2
    else:
        return 0

# https://stackoverflow.com/questions/6313308/get-all-the-diagonals-in-a-matrix-list-of-lists-in-python
def matrix_diagonals(matrix):
    # Alter dimensions as needed

    # create a default array of specified dimensions
    a = np.asarray(matrix)

    # a.diagonal returns the top-left-to-lower-right diagonal "i"
    # according to this diagram:
    #
    #  0  1  2  3  4 ...
    # -1  0  1  2  3
    # -2 -1  0  1  2
    # -3 -2 -1  0  1
    #  :
    #
    # You wanted lower-left-to-upper-right and upper-left-to-lower-right diagonals.
    #
    # The syntax a[slice,slice] returns a new array with elements from the sliced ranges,
    # where "slice" is Python's [start[:stop[:step]] format.

    # "::-1" returns the rows in reverse. ":" returns the columns as is,
    # effectively vertically mirroring the original array so the wanted diagonals are
    # lower-right-to-uppper-left.
    #
    # Then a list comprehension is used to collect all the diagonals.  The range
    # is -x+1 to y (exclusive of y), so for a matrix like the example above
    # (x,y) = (4,5) = -3 to 4.
    diags = [a[::-1, :].diagonal(i) for i in range(-a.shape[0] + 1, a.shape[1])]

    # Now back to the original array to get the upper-left-to-lower-right diagonals,
    # starting from the right, so the range needed for shape (x,y) was y-1 to -x+1 descending.
    diags.extend(a.diagonal(i) for i in range(a.shape[1] - 1, -a.shape[0], -1))

    # Another list comp to convert back to Python lists from numpy arrays,
    # so it prints what you requested.
    return [n.tolist() for n in diags]

def main():
    mat = [[1, 0, 2],
           [2, 0, 4],
           [2, 4, 5],
           [2, 5, 6]]
    print(terminate_game(mat,3))
    print(max_col_height(mat))
    print(board_to_matrix(mat,7,4))



if __name__ == "__main__":
    main()