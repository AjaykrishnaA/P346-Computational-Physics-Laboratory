import csv
import copy
from math import sqrt

###########################################################


def getMatFromFile(mat_name: str):
    # opening the file containing matrix to read its contents
    with open(f'{mat_name}.csv', newline='') as file:

        reader = csv.reader(file, quoting=csv.QUOTE_NONNUMERIC, delimiter=' ')

        # storing all the rows in an output (2-D)list
        output = []
        for row in reader:
            output.append(row[:])

    return output


def displayMat(mat):
    if mat:
        for rows in mat:
            print([float('{:.2f}'.format(elem)) for elem in rows])
    print()


def nrow(mat):
    return len(mat)  # returns the no. of rows of a matrix


def ncol(mat):
    return len(mat[0])  # returns the no. of columns of a matrix


def matTranspose(mat):
    return [[mat[j][i] for j in range(nrow(mat))] for i in range(ncol(mat))]


def matMult(matA, matB):
    if ncol(matA) == nrow(matB):
        return [[sum(matA[i][k]*matB[k][j] for k in range(ncol(matA)))
                 for j in range(ncol(matB))] for i in range(nrow(matA))]
    else:
        print("\nIndexes do not match for matrix multiplication of %s and %s!" % (
            str(matA), str(matB)))

###########################################################


def swapRows(A, r, i, ncols):
    temp = [x for x in A[r]]
    A[r] = A[i]
    A[i] = temp


def partialPivot(A, r, nrows, ncols):
    pivot = A[r][r]
    newSwap = 0
    if abs(pivot) > 10 ** (-12):
        return ("success", newSwap)
    else:
        for i in range(r+1, nrows):
            if A[i][r] != 0:
                pivot = A[i][r]
                swapRows(A, r, i, ncols)
                newSwap += 1
                return ("success", newSwap)
    if pivot == 0:
        return ("failed", newSwap)


def guassJordan(mat, nrows, ncols):
    A = mat
    for r in range(nrows):
        x = partialPivot(A, r, nrows, ncols)[0]
        if x == "failed":
            return "No solution exists"
        else:
            for c in range(ncols-1, r-1, -1):
                A[r][c] = A[r][c]/A[r][r]
            for row in range(nrows):
                if row != r and A[row][r] != 0:
                    factor = A[row][r]
                    for c in range(r, ncols):
                        A[row][c] -= factor*A[r][c]
    return A


def solve(mat, nrows, ncols):
    print("\nYour input system of equations in augmented matrix format is:")
    displayMat(mat)
    res = guassJordan(mat, nrows, ncols)
    print("\nYour matrix after GaussJordan Elimination is:")
    displayMat(res)
    if res == "No solution exists":
        print("No solution exists")
    else:
        print("The solutions are:")
        var_holder = {}
        for i in range(nrows):
            var_holder['x_' +
                       str(i+1)] = float('{:.2f}'.format(res[i][ncols-1]))
        locals().update(var_holder)

        for i in range(nrows):
            print(f"x_{i+1} =", vars()[f'x_{i+1}'])


def gjInverse(mat):
    print("\nYour input matrix for finding inverse is:")
    displayMat(mat)
    A = [mat[i]+[1 if i == j else 0 for j in range(len(mat))]
         for i in range(len(mat))]
    print("The augmented matrix is :")
    displayMat(A)
    A = guassJordan(A, len(mat), 2*len(mat))
    print("\nYour matrix after GaussJordan Elimination is:")
    displayMat(A)
    res = [[A[i][j] for j in range(len(A), 2*len(A))] for i in range(len(A))]
    print("Hence, the solution is:")
    displayMat(res)


def gjDeterminant(mat, ncols):
    print("\nYour input matrix for finding determinant is:")
    displayMat(mat)
    A = mat
    swapCount = 0
    for r in range(ncols):
        x = partialPivot(A, r, ncols, ncols)
        swapCount += int(x[1])
        if x[0] == "failed":
            return "No solution exists"
        else:
            for row in range(r+1, ncols):
                if A[row][r] != 0:
                    factor = A[row][r]/A[r][r]
                    for c in range(r, ncols):
                        A[row][c] -= factor*A[r][c]
    k = 1
    for i in range(ncols):
        k *= A[i][i]
    return ((-1) ** swapCount)*k

###########################################################

# Creating augmented matrix


def aug_Mat(A, b):
    for i in range(len(A)):
        for j in range(len(b[i])):
            A[i].append(b[i][j])
    return A


def doolittle(mat: list, b: list, nrow: int):
    Ab = aug_Mat(mat, b)
    ncols = ncol(Ab)
    for i in range(nrow):
        x = partialPivot(Ab, i, nrow, ncols)[0]
        if x == "failed":
            return "No solution exists"
        else:
            for j in range(nrow):
                # Upper Triangular
                if i <= j:
                    s = sum([Ab[i][k]*Ab[k][j] for k in range(i)])
                    Ab[i][j] = Ab[i][j] - s
                # Lower Triangular
                else:
                    s = sum([Ab[i][k]*Ab[k][j] for k in range(j)])
                    Ab[i][j] = float((Ab[i][j] - s) / Ab[j][j])
    return Ab


def crout(mat: list, b: list, nrow: int):
    Ab = aug_Mat(mat, b)
    ncols = ncol(Ab)
    for i in range(nrow):
        x = partialPivot(Ab, i, nrow, ncols)[0]
        if x == "failed":
            return "No solution exists"
        else:
            for j in range(nrow):
                # Lower Triangular
                if i >= j:
                    s = sum([Ab[i][k]*Ab[k][j] for k in range(j)])
                    Ab[i][j] = Ab[i][j] - s

                # Upper Triangular
                else:
                    s = sum([Ab[i][k]*Ab[k][j] for k in range(i)])
                    Ab[i][j] = float((Ab[i][j] - s) / Ab[i][i])

    return Ab


# Combined forward and backward substitution to solve the system or find inverse; in case of doolittle
def substitution_doolittle(Ab):
    Arow = nrow(Ab)
    bcol = ncol(Ab)-Arow
    y = [[0 for y in range(bcol)] for x in range(Arow)]
    for i in range(Arow):
        for j in range(bcol):
            s = sum(Ab[i][k]*y[k][j] for k in range(i))
            y[i][j] = (Ab[i][j+Arow]-s)
    x = [[0 for y in range(bcol)] for x in range(Arow)]
    for i in range(Arow-1, -1, -1):
        for j in range(bcol):
            s = sum(Ab[i][k]*x[k][j] for k in range(i + 1, Arow))
            x[i][j] = (y[i][j]-s)/Ab[i][i]
    return x


# Combined forward and backward substitution to solve the system or find inverse; in case of crout
def substitution_crout(Ab):
    Arow = nrow(Ab)
    bcol = ncol(Ab)-Arow
    y = [[0 for y in range(bcol)] for x in range(Arow)]
    for i in range(Arow):
        for j in range(bcol):
            s = sum(Ab[i][k]*y[k][j] for k in range(i))
            y[i][j] = (Ab[i][j+Arow]-s)/Ab[i][i]
    x = [[0 for y in range(bcol)] for x in range(Arow)]
    for i in range(Arow-1, -1, -1):
        for j in range(bcol):
            s = sum(Ab[i][k]*x[k][j] for k in range(i+1, Arow))
            x[i][j] = (y[i][j]-s)
    return x


def cholesky(mat: list, b: list, nrow: int):
    Ab = aug_Mat(mat, b)
    ncols = ncol(Ab)
    for i in range(nrow):
        x = partialPivot(Ab, i, nrow, ncols)[0]
        if x == "failed":
            return "No solution exists"
        else:
            for j in range(i+1):
                # for diagonals
                if i == j:
                    s = sum([Ab[j][k]**2 for k in range(j)])
                    Ab[j][j] = float(sqrt(Ab[j][j] - s))
                # for non-diagonals
                if i > j:
                    s = sum([Ab[i][k]*Ab[j][k] for k in range(j)])
                    if Ab[j][j] > 0:
                        Ab[i][j] = float((Ab[i][j] - s)/Ab[j][j])
                        Ab[j][i] = Ab[i][j]

    return Ab

# Combined forward and backward substitution to solve the system or find inverse; in case of cholesky


def substitution_cholesky(Ab):
    Arow = nrow(Ab)
    bcol = ncol(Ab)-Arow
    y = [[0 for y in range(bcol)] for x in range(Arow)]
    for i in range(Arow):
        for j in range(bcol):
            f = sum(Ab[i][k]*y[k][j] for k in range(i))
            y[i][j] = (Ab[i][j+Arow]-f)/Ab[i][i]
    x = [[0 for y in range(bcol)] for x in range(Arow)]
    for i in range(Arow-1, -1, -1):
        for j in range(bcol):
            f = sum(Ab[i][k]*x[k][j] for k in range(i+1, Arow))
            x[i][j] = (y[i][j]-f)/Ab[i][i]
    return x


# solve a system of linear equations using the input method given as a parameter(defaulted to doolittle)
def solve_LU(mat: list, b: list, nrow: int, method="doolittle"):
    A = copy.deepcopy(mat)
    globalsParameter = globals()
    localsParameter = locals()
    codeInString = 'print(dir())\nA = {m}(A, b, nrow)\nx = [substitution_{m}(A)[i][0] for i in range(nrow)]'.format(
        m=method)
    codeObejct = compile(codeInString, '', 'exec')
    exec(codeObejct)
    """ if method == "doolittle":
        A = doolittle(A, b, nrow)
        x = [substitution_doolittle(A)[i][0] for i in range(nrow)]
    elif method == "crout":
        A = crout(A, b, nrow)
        x = [substitution_crout(A)[i][0] for i in range(nrow)]
    elif method == "cholesky":
        A = cholesky(A, b, nrow)
        x = [substitution_cholesky(A)[i][0] for i in range(nrow)] """
    for i in range(len(x)):
        print("x_"+str(i+1)+" = "+str('{:.2f}'.format(x[i])))


# for finding inverse of a matrix using doolittle's decomposition
def lu_Inverse(A, nrow):

    # Creating the identity matrix:
    identity = []
    for i in range(nrow):
        row = [1 if (i == j) else 0 for j in range(nrow)]
        identity.append(row)

    return(substitution_doolittle(doolittle(A, identity, nrow)))
