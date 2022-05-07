import streamlit as st
from config import *
from handler import *
import matplotlib.pyplot as plt

def equation_handler(txt):
    try:
        # [txt] equation
        st.write('## Solution')
        methods = [binary_searching, secant, brentq]
        msg = ['Binary searching algo', 'Secant algo', 'Brent algo']
        solution = eq(txt, methods)
        ans = 'Error code: 400. Bad request: can not recognize that function'
        if solution is not None:
            roots, runtimes = solution[0], solution[1]
            def roots_to_str(roots):
                if len(roots) > 0:
                    return '\n'.join([f'X{j} = {roots[j]}' for j in range(len(roots))])
                return 'No roots.'
            ans = '\n\n'.join([
                f'##### {i+1} {msg[i]} ({runtimes[i]*1e3:.2f} ms):\n\n{roots_to_str(roots[i])}' 
                for i in range(len(methods))
            ])
            a, b = -1e2, 1e2
            if Equation.fType(txt):
                a, b = -pi, pi
            plt1 = Graphic.plotFunc(plt, Equation.func(txt), a, b, title='Equation')
            if len(roots) > 0:
                point = roots[1]
                plt1.plot(point, 0, 'r*', markersize=10)
            st.pyplot(plt1)
        st.write(ans)
    except Exception as e:
        st.warning(e.args)

def integral_handler(txt):
    try:
        # [txt] function, low_border, high_border
        st.write('## Integral')
        tmp = Integral(txt)
        methods = [Integral.simpson, Integral.trapezoid, Integral.lrectangle, Integral.rrectangle]
        results = integ(tmp.func, tmp.a, tmp.b, methods)
        ans = '\n\n'.join([
            f'##### {i+1} {results[i]["rule"]} ({results[i]["runtime"]*1e3:.2f} ms):\nReturn: {results[i]["value"]}' 
            for i in range(len(results))
        ])
        plt1 = Graphic.plotFunc(plt, tmp.func, tmp.a, tmp.b, title='Integral')
        st.pyplot(plt1)
        st.write(ans)
    except Exception as e:
        st.warning(e.args)

def checkbox_handler():
    ne = st.checkbox('Newton')
    cs = st.checkbox('Cubic Spline')
    lm = st.checkbox('LSM')
    algos = []
    minrange, maxrange = 1, 7    # as default
    if ne == True:
        algos.append('ne')
    if cs == True:
        algos.append('cs')
    if lm == True:
        algos.append('lsm')
        minrange = st.slider('Choose LSM min level:', min_value=1, max_value=5)
        maxrange = st.slider('Choose LSM max level:', min_value=minrange, max_value=10)
    return algos, minrange, maxrange

def approximation_handler(txt):
    try:
        # [txt] x: x1, x2,... y: y1, y2, ...
        app = Approximation(txt)
        algos, minrange, maxrange = checkbox_handler()
        if len(algos) > 0:
            value = st.text_input("Input x-value to calculate")
            ans = ''
            for item in app.interp(value, algos, minrange, maxrange):
                ans += f'##### {item["algo"]}: \nY({value}) = {item["value"]}\n'
            plt1 = Graphic.plotApp(plt, app.X, app.Y, legends=algos, minN=minrange, maxN=maxrange)
            st.pyplot(plt1)
            st.write(ans)
            pass
        else:
            st.warning('Please choose algorithm first!')
    except Exception as e:
        st.warning(e.args)

if __name__ == '__main__':    
    st.title('Math bot')
    st.date_input(f'Application (v.{BOT_VERSION}) by **@{BOT_AUTHOR}** is running..')
    st.balloons()
    
    txt = st.text_input("Input an expression here").lower()
    if txt.find('x:') != -1 and txt.find('y:') != 1 and txt.find('v:') != 1:
        approximation_handler(txt)
    elif txt.find('=') != -1:
        equation_handler(txt)
    elif txt.find(',') != -1:
        integral_handler(txt)
    else:
        st.warning('Error code: 400. Bad request: can not recognize that expression')
        