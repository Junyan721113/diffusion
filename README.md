# iGEM Diffusion Modeling

## Principles

### Thermal Diffusion
$$
\frac{dc}{dt} = \alpha \frac{d^2c}{dx^2}
$$

### 1-Dim Discrete Form
$$
c_{x,t+1} - c_{x,t} = \frac{\alpha}{2}((c_{x+1,t} - c_{x,t}) - (c_{x,t} - c_{x-1,t}))
$$

$$
c_{x,t+1} - c_{x,t} = \frac{\alpha}{2}(c_{x+1,t} - 2c_{x,t} + c_{x-1,t})
$$

$$
c_{x,t+1} = \frac{\alpha}{2} c_{x+1,t} + (1 - \alpha) c_{x,t} + \frac{\alpha}{2} c_{x-1,t}
$$

$$
K_\alpha = \begin{bmatrix}
\frac{\alpha}{2} & 1-\alpha & \frac{\alpha}{2}
\end{bmatrix}
$$

### 2-Dim Discrete Form
$$
G(x) = \frac{1}{\sqrt{2\pi}\sigma}e^{-\frac{x^2+y^2}{2\sigma^2}}
$$

$$
K_\alpha = \begin{bmatrix}
w_2 & w_1 & w_2\\
w_1 & 1 - \alpha & w_1\\
w_2 & w_1 & w_2\\
\end{bmatrix}
$$

$$
e_1 = e^{-1}, e_2 = e^{-2}
$$

$$
w_1 = \frac{\alpha}{4} \frac{e_1}{e_1 + e_2}, w_2 = \frac{\alpha}{4} \frac{e_2}{e_1 + e_2}
$$

### Translation
$$
V_x = \begin{bmatrix}
1 + v_x & 1 & 1 - v_x\\
\end{bmatrix}
$$

$$
V_y = \begin{bmatrix}
1 + v_y \\ 1 \\ 1 - v_y\\
\end{bmatrix}
$$

### Formula All-in-one
$$
K_{t} = \begin{bmatrix}
w_2 (1 + v_x) (1 + v_y) & w_1 (1 + v_y) & w_2 (1 - v_x) (1 + v_y)\\
w_1 (1 + v_x)           & 1 - \alpha    & w_1 (1 - v_x)          \\
w_2 (1 + v_x) (1 - v_y) & w_1 (1 - v_y) & w_2 (1 - v_x) (1 - v_y)\\
\end{bmatrix}
$$

$$
C_{t+1} = C_{t} * K_{t}
$$

## Display Logarithmically

$$
p(0) = 0, p(1) = 1
$$

$$
p(x) = \ln(x * (exp - 1) + 1)
$$
