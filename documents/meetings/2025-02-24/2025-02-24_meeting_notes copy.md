# Meeting Notes:

## Current issues:
1. Annual fluctuation
    - All bands and, by extension, indices contain a component which is periodic over an annual cycle.
    - This annual fluctuation is the major component of the signal—dominating the correlations. 
2. Lag
    - It may be that satellite bands/indices lag behind the JULES signal (or vice versa). 
    - This _may_ make things appear less correlated than they are in reality. 

## Solutions
### 1. Annual Fluctuations 
The time-series for a particular band/index output $ b $, in a particular greenbelt $ g $, is given by some unknown function $ f_{b,g} $:

$$
\mathbf{y}_{b,g} = f_{b,g}(\mathbf{t})
$$

where

$$
\begin{aligned}
    \mathbf{t} &= \{ t_{y} \}_{y=2016,\dots,2025} \\
    \mathbf{t}_y &= \{ t_{m} \}_{m=1,\dots,12}
\end{aligned}
$$
 
and for a single year,

$$
\mathbf{y}_{b,g,y} = f_{b,g}(\mathbf{t_y})
$$

We will compute the average time-series for a particular band in a particular greenbelt:

$$
\bar{\mathbf{y}}_{b,g} = \frac{1}{(2025-2016)} \sum_{y=2016}^{2025} \mathbf{y}_{b,g,y}
$$

Then calculate the deviation from this mean $\mathbf{\hat{y}}_{b,g,y}$ as:

$$
\mathbf{\hat{y}}_{b,g,y} = \mathbf{y}_{b,g,y} - \bar{\mathbf{y}}_{b,g}
$$

Similarly, JULES predictions are given by known functions: 

$$
\begin{aligned}
    \mathbf{y}_{\text{soil}} = h_{s, g}(\mathbf{t}) \\
    \mathbf{y}_{\text{veg}} = h_{v, g}(\mathbf{t})
\end{aligned}
$$

We can compute their means:

$$
\begin{aligned}
    \bar{\mathbf{y}}_{\text{soil}} = \frac{1}{(2025-2016)} \sum_{y=2016}^{2025} h_{s, g}(\mathbf{t_y}) \\
    \bar{\mathbf{y}}_{\text{veg}} = \frac{1}{(2025-2016)} \sum_{y=2016}^{2025} h_{v, g}(\mathbf{t_y})
\end{aligned}
$$

And their deviations:

$$
\begin{aligned}
    \mathbf{\hat{y}}_{\text{soil}} = \mathbf{y}_{\text{soil}} - \bar{\mathbf{y}}_{\text{soil}} \\
    \mathbf{\hat{y}}_{\text{veg}} = \mathbf{y}_{\text{veg}} - \bar{\mathbf{y}}_{\text{veg}}
\end{aligned}
$$

We then compute the Pearson correlations of $ \mathbf{\hat{y}}_{b,g} $ with $ \mathbf{\hat{y}}_{\text{soil}} $ and $ \mathbf{\hat{y}}_{\text{veg}} $, respectively:

$$
\begin{aligned}
c^{\text{soil}}_{b,g} = \operatorname{Corr}(\mathbf{\hat{y}}_{b,g}, \mathbf{\hat{y}}_{\text{soil}}) \\
c^{\text{veg}}_{b,g} = \operatorname{Corr}(\mathbf{\hat{y}}_{b,g}, \mathbf{\hat{y}}_{\text{veg}})
\end{aligned}
$$

where $ \operatorname{Corr} $ is the Pearson Correlation Coefficient, given by:

$$
\operatorname{Corr}(\mathbf{x}, \mathbf{y}) = \frac{\sum (x_i - \bar{x}) (y_i - \bar{y})}{\sqrt{\sum (x_i - \bar{x})^2} \sqrt{\sum (y_i - \bar{y})^2}}
$$

### Output Matrices:

We can then compute and visualize the following matrices:

$$
\begin{array}{ccc}
M_{\text{soil}} & & M_{\text{veg}} \\
\begin{bmatrix}
c^{\text{soil}}_{b_1 g_1} & c^{\text{soil}}_{b_1 g_2} & \cdots & c^{\text{soil}}_{b_1 g_m} \\
c^{\text{soil}}_{b_2 g_1} & c^{\text{soil}}_{b_2 g_2} & \cdots & c^{\text{soil}}_{b_2 g_m} \\
\vdots & \vdots & \ddots & \vdots \\
c^{\text{soil}}_{b_n g_1} & c^{\text{soil}}_{b_n g_2} & \cdots & c^{\text{soil}}_{b_n g_m}
\end{bmatrix}
 & & 
\begin{bmatrix}
c^{\text{veg}}_{b_1 g_1} & c^{\text{veg}}_{b_1 g_2} & \cdots & c^{\text{veg}}_{b_1 g_m} \\
c^{\text{veg}}_{b_2 g_1} & c^{\text{veg}}_{b_2 g_2} & \cdots & c^{\text{veg}}_{b_2 g_m} \\
\vdots & \vdots & \ddots & \vdots \\
c^{\text{veg}}_{b_n g_1} & c^{\text{veg}}_{b_n g_2} & \cdots & c^{\text{veg}}_{b_n g_m}
\end{bmatrix}
\end{array}
$$

where $n$ is the number of bands/indices and $m$ is the number of greenbelts.

---

### 2. Lag
For each band/index, we compute the correlation at different offsets ($\delta t$) and compare the results:

**Algorithmically:**

$$
\begin{array}{l}
\mathbf{c}^{\text{soil}} \leftarrow \text{initialized as empty list/vector} \\
\mathbf{c}^{\text{veg}} \leftarrow \text{initialized as empty list/vector} \\
\\
\textbf{for } \delta t \in \{-l, \dots, l\} \textbf{ do} \\
    \quad \mathbf{y'}_{b,g} = f_{b,g}(\mathbf{t} + \delta t) \\
    \quad \bar{\mathbf{y}'}_{b,g} = \frac{1}{(2025-2016)} \sum_{y=2016}^{2025} \mathbf{y'}_{b,g,y} \\
    \quad \mathbf{\hat{y}'}_{b,g,y} = \mathbf{y'}_{b,g,y} - \bar{\mathbf{y}'}_{b,g} \\
    \quad c^{\text{soil}}_{b,g, \delta t} = \operatorname{Corr}(\mathbf{\hat{y}'}_{b,g}, \mathbf{\hat{y}}_{\text{soil}}) \\
    \quad c^{\text{veg}}_{b,g, \delta t} = \operatorname{Corr}(\mathbf{\hat{y}'}_{b,g}, \mathbf{\hat{y}}_{\text{veg}}) \\

    \quad \mathbf{c}^{\text{soil}} \leftarrow \mathbf{c}^{\text{soil}} \cup \{c^{\text{soil}}_{b,g, \delta t}\} \\
    \quad \mathbf{c}^{\text{veg}} \leftarrow \mathbf{c}^{\text{veg}} \cup \{c^{\text{veg}}_{b,g, \delta t}\} \\
\textbf{end for}
\end{array}
$$

and then analyse $ \mathbf{c}^{\text{soil}}$ and $\mathbf{c}^{\text{veg}} $ for an optimal $\delta t$ and check the consistency across years/greenbelts. 
