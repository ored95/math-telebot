"""
Approximation algos handler
"""
import numpy as np

def bsearch(value, v):
    """
    binary searching to identify index of the following neighbor to 'value' in vector
    """
    b, e = 0, len(v) - 1
    m = (b+e) // 2
    while b != e - 1:
        if value <= v[m]:
            e = m
        else:
            b = m
        m = (b+e) // 2
    return e

class Newton:
    def __init__(self, x, y):
        if len(x) != len(y):
            raise ValueError('Newton: Can not execute interpolation in case of different input-sizes')
        # Preprocess to claim that x is in ascending order
        idx = np.argsort(x)
        self.x = [x[i] for i in idx]
        self.y = [y[i] for i in idx]
        self.n = len(x)
        
    def ntab_diff(self):    # Newton difference table
        """
        polynomial to calculate the divided differences table
        """
        coef = np.zeros([self.n, self.n+1])
        # the first two column is y
        coef[:,0] = self.y
        for j in range(1, self.n):
            for i in range(self.n - j):
                coef[i][j] = (coef[i+1][j-1] - coef[i][j-1]) / (self.x[i+j] - self.x[i])
        return coef[0]

    # Newton interpolation
    def interp(self, x_value):
        """
        To compute the interpolated function at x = x_value 
        """
        coef = self.ntab_diff()
        n = self.n - 1
        p = coef[n]
        for k in range(n, 0, -1):
            p = coef[k-1] + (x_value - self.x[k-1]) * p
        return p
    
    def get_plot_points(self, npt=1000):
        """
        To plot an interpolated function by Newton interpolation
        Input: npt - number of points
        return a list of interpolated points (x, y)
        """
        px = np.linspace(min(self.x), max(self.x), npt)
        py = [self.interp(xi) for xi in px]
        return px, py
    
class CubicSpline:
    def __init__(self, x, y):
        n = len(x)
        if n < 3:
            raise ValueError('Cubic Spline: Too short an array')
        if n != len(y):
            raise ValueError('Cubic Spline: Can not execute interpolation in case of different input-sizes')       
        idx = np.argsort(x)
        self.x = [x[i] for i in idx]    # input (xi, yi)
        self.y = [y[i] for i in idx]
        self.n = n-1            # number of combination (ai, bi, ci, di)
        self.h = self.compute_changes()
        self.compute_spline_coefficients()

    def interp(self, x_value):
        """
        To compute the interpolated function at x = x_value 
        """
        i = bsearch(x_value, self.x)
        z = x_value - self.x[i]
        p = self.coefficients[i-1]
        # print(f'[z={z:.2}]\tF(z) = {p[3]/6:.3f} * z^3 + {p[2]/2:.3f} * z^2 + {p[1]:.3f} * z + {p[0]:.3f}')
        return p[3] / 6 * z ** 3 + p[2] / 2 * z ** 2 + p[1] * z + p[0]

    def get_plot_points(self, npt=1000):
        """
        To plot an interpolated function by Cubic spline
        Input: npt - number of points
        return a list of interpolated points (x, y)
        """
        px = np.linspace(min(self.x), max(self.x), npt)
        py = [self.interp(xi) for xi in px]
        return px, py

    def compute_changes(self):
        """
        To find ∆x as h[i] = x[i] - x[i-1]
        """
        return [0] + [self.x[i] - self.x[i-1] for i in range(1, self.n + 1)]

    def compute_spline_coefficients(self):
        """
        To find 4n spline coefficients
        """
        A, B, C, D = self.create_tridiagonal_matrix()
        M = self.TDMA_solver(A, B, C, D)
        self.coefficients = [
            [
                self.y[i],
                (self.y[i] - self.y[i-1]) / self.h[i] + (2 * M[i] + M[i-1]) * self.h[i] / 6,
                M[i],
                (M[i] - M[i-1]) / self.h[i]
            ]
            for i in range(1, self.n+1)
        ]

    def create_tridiagonal_matrix(self):
        """
        To identify the tridiagonal matrix
        """
        A = [self.h[i] for i in range(1, self.n)] + [0]
        B = [1] + [2 * (self.h[i] + self.h[i+1]) for i in range(1, self.n)] + [1]
        C = [0] + [self.h[i+1] for i in range(1, self.n)]
        
        d1, d2 = 0, 0   # standard cubic spline boundary condition (g"(x[0]) = 0, g"(x[n]) = 0)
        D = [d1] + [((self.y[i+1] - self.y[i]) / self.h[i+1] - (self.y[i] - self.y[i-1]) / self.h[i]) * 6 
            for i in range(1, self.n)] + [d2]
        return A, B, C, D

    def TDMA_solver(self, a, b, c, d):
        """
        TriDiagonal Matrix Algorithm (a.k.a Thomas algorithm) solver
        refer to http://en.wikipedia.org/wiki/Tridiagonal_matrix_algorithm
        and to http://www.cfd-online.com/Wiki/Tridiagonal_matrix_algorithm_-_TDMA_(Thomas_algorithm)
        Input: a, b, c: lower, main and upper diagonals corresponding in system linear equation Ax = d
        """
        n = len(d) # number of equations
        for i in range(1, n):
            w = a[i-1] / b[i-1]
            b[i] = b[i] - w * c[i-1] 
            d[i] = d[i] - w * d[i-1]

        x = b
        x[n-1] = d[n-1] / b[n-1]
        for i in range(n-2, -1, -1):
            x[i] = (d[i] - c[i] * x[i+1]) / b[i]
        return x

class LSM:
    """
    Least Squares Method Implementation
    n: degree of polynomial f(x)
    x, y: points
    w: weights
    Provide switching case: y = f(x, a0, a1, ...) and x = f(y, a0, a1, ...)
    """
    def __init__(self, x, y, n=1):
        if len(x) != len(y):
            raise ValueError('Wrong number of coordinates array lengths')
        elif n < 0:
            raise ValueError('Incorrect degree of approximated polynomial f(x)')
        self.x = x
        self.y = y
        """
        By default, w(i) = 1.0
        See more: http://www.mathnet.ru/links/cd52fe1c5a8ae572255006c283e0a286/mm297.pdf [p.8-9]
        """
        self.w = np.ones(len(x))
        self.n = n
        self.c = self.get_coefficients()

    def interp(self, x_value):
        """
        To compute the interpolated function at x = x_value by formula
        y = c[0] + c[1] * x + c[2] * x^2 + ... + c[n] * x^n
        """
        y = self.c[-1]
        for k in range(self.n-1, -1, -1):
            y = y * x_value + self.c[k]
        return y

    def mse(self):
        """
        Calculate minimum squared error
        """
        _y = np.array([self.interp(x) for x in self.x])
        return np.dot(np.power(_y - self.y, 2.), self.w)

    def get_coefficients(self):
        """
        LSM solution by System of Linear Equations
        """
        wx = np.zeros(self.n * 2 + 1)
        for k in range(self.n*2+1):
            wx[k] = np.dot(self.w, np.power(self.x, k))
        A = np.zeros((self.n+1, self.n+1))
        for k in range(self.n+1):
            A[k,:] = wx[k: k+self.n+1]
        
        wy = self.w * self.y
        b = np.zeros(self.n+1)
        for k in range(self.n+1):
            b[k] = np.dot(wy, np.power(self.x, k))
        
        return np.linalg.solve(A, b)

    def get_plot_points(self, npt=1000):
        """
        To plot an interpolated function by LSM
        Input: npt - number of points
        return a list of interpolated points (x, y)
        """
        px = np.linspace(min(self.x), max(self.x), npt)
        py = self.interp(px)
        return px, py
