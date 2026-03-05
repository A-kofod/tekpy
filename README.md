# tekpy

A lightweight toolbox for workflow and calculations in introductory engineering fields.
## About
`tekpy` is developed as a collection of useful Python functions and classes for students in marine engineering and technology management (Maskinmester).

The package allows users to integrate Python into common workflows for lectures and training assignments.

`tekpy` is built using the powerful `sympy` library and standard Python tools. It is a "work in progress," with more functionality planned over time.
## How to Install
You can install `tekpy` directly from GitHub using pip:

```bash
pip install git+https://github.com/A-Kofod/tekpy.git
```
Source code is available at the GitHub repository: https://github.com/A-Kofod/tekpy.git

## Scope
`tekpy` is designed specifically for students in marine engineering and technology management.

It is **not** a replacement for professional CAS software but provides a practical bridge between Python and marine engineering assignments, calculations, and workflows.
## Contents

### Complex Numbers in Polar Form
Available via:  `from tekpy import polar_rek, polar_deg, rek_polar`.

`polar_rek(magnitude, angle_degrees)`: returns a `sympy` complex number as `real + imaginary * I`. Supports arithmetic operations. 

`polar_deg(Z)`: Returns a complex number object (like a `polar_rek` object) as a complex number in polar form. Specifically: `magnitude \angle degrees`. Readable output only. Meant for display. 

`rek_polar(real, imag)`:  Returns a complex number object. `.show_polar()` method allows the user to display the complex number in polar form when printed. `.build_comp()` method lets the class create a `polar_rek` compatible object. 

### Business Economics Helpers (Work in Progress)

_Note:_ Some function and class names are in Danish and will be translated in future versions.

`DifferensMetoden`: Assists in standard economics assignments, calculating optimal price/quantity from incremental cost (DOMK).

`TotalMetoden`: Calculates optimal price/quantity given a linear variable unit cost.

### $\LaTeX$ parsing 
The `tekpy` package allows for 1:1 parsing of Python code to LaTeX. 

`TexTree`: Takes a formatted string and returns a 1:1 LaTeX expression. The class relies on a classical shunting yard algorithm, and includes built-in features for typical engineering notation. 
#### Example 1:
```python
a = 12
b = 4
TexTree(f'c = a + b = {a} + {b} res {a+b}')
```
Output:
```latex
c = a + b = 12 + 4 = \underline{\underline{16}}
```
The class supports functions such as: `sqrt, cos, sin` and notation elements like `^{exp}, _{index}`. 
#### Example 2:
Integration with `tekpy` complex number objects:

```python
U = polar_rek(400, 30)
Z = polar_rek(34, -28)
I = U / Z

t = TexTree(f'I = U / Z = {polar_deg(U)} / {polar_deg(Z)} = {polar_deg(I)}')

print(t)

``` 
Output:
```latex
I = \frac{U}{Z} = \frac{400\angle30}{34\angle-28} = 11.76\angle58
```
Here, `polar_rek` serves as the complex number generator, while `polar_deg` displays the number in polar form.

`TexTree` rounds to two (2) decimals by default, but it is possible to round to `n` decimals using the `.round(n)` command.

Besides what's already covered, the class handles `dot` notation for variables, e.g., `dotV` -> `\dot{V}` -> $\dot{V}$, and selected SI units, e.g., `TexTree(f'2300W')` -> `2300\,\mathrm{W}` -> $2300\,\mathrm{W}$.

## License
This package is released under the MIT License.

`tekpy` is primarily an educational project that is free to use and distribute. Please respect the intended educational purpose of the project.


