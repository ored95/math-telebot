import math
def derivative(f, x):
    h=1e-8
    return (f(x+h)-f(x))/h

def solver(f, x0, epsilon, max_iter):
    xn=x0
    for n in range(0,max_iter):
        y=f(xn)
        if abs(y)<epsilon:
            return xn
        slope=derivative(f,xn)
        if(slope==0):
            return None
        xn=xn-y/slope
    return None

def loop(f, L_bound, R_bound, increment):
    solutions=[]
    while L_bound<=R_bound:
        solution=solver(f, L_bound, 1e-10, 1000)
        if solution is not None:
            solution=round(solution,5)
        if solution not in solutions:
            solutions.append(solution)
        L_bound+=increment
    print(sorted(solutions))
    print("we found "+str(len(solutions))+" solutions!")

equation=""
def f(x):
    try:
        y=eval(equation)
    except ZeroDivisionError:
        y= 1e-10
    return y

# e = Equation("7x^2-x+3 = 4x^4+1")
# equation = "7*x**2-x+3-(4*x**4+1)"
# e = Equation("2^x/x^3=x+1")
equation = "2**x/x**3-(x+1)"
loop(f,-1e3, 1e3, 0.5)