# math-telebot
Telegram bot for some mathematical problems

### Build and run
```sh
    pip install -r requirements.txt
    [for Telegram] python bot.py
    [for WebApp]   streamlit run app.py
```
### Clean trash
```sh
    sh clean.sh
```
### Table of command instructions

|No.|Usage|Description|
| :---: | :--- | :--- |
|#1|/start|start bot|
|#2|/help|show all instructions|
|2.1|/help `eq`, help `equation`|show all EQ-instructions|
|2.2|/help `integ`, /help `integral`|show all INTEG-instructions|
|2.3|/help `app`, /help `approximation`|show all APP-instructions|
|#3|/eq `equation`|solve equation by 3 algos: Binary searching, Secant and Brent|
|3.1|/eqb `equation`|solve equation Binary searching algo|
|3.2|/eqs `equation`|solve equation by Secant algo|
|3.3|/eqt `equation`|solve equation by Brent algo|
|#4|/integ `function, left_border, right_border`|calculate integral by 4 rules: Simpson, Trapezoid, and Rectangle (left, right)|
|4.1|/integs `function, left_border, right_border`|calculate integral by Simpson rule|
|4.2|/integt `function, left_border, right_border`|calculate integral by Trapezoid rule|
|4.3|/integl `function, left_border, right_border`|calculate integral by Left Rectangle rule|
|4.4|/integr `function, left_border, right_border`|calculate integral by Right Rectangle rule|
|#5|/app `x: x1, x2, ... y: y1, y2, ...`|find approximated value for 2D functions|
|5.1|/appx `x1, x2, ...`|set X-coordinate values|
|5.2|/appy `y1, y2, ...`|set Y-coordinate values|
|5.3|/appv `value`|get interpolated value at `x = value`|

### WebApp version instruction
+ Input example
```sh
[Equation]
    equation

[Integral]
    function, low_border, high_border

[Approximation]
    x: x1, x2,... y: y1, y2, ...
```
+ Error code
```js
    Error code: 400. Bad request: can not recognize that expression
```