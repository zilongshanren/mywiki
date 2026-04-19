---
title: 'Reaction-Diffusion: Gray-Scott on a 2D Grid'
url: https://www.4rknova.com/blog/2026/02/15/reaction-diffusion
author: Nikolaos Papadopoulos
published: '2026-02-15'
source_blog: Nikos Papadopoulos - Portfolio
source_site: https://www.4rknova.com/
category: graphics
fetched: '2026-04-19'
---

Reaction-diffusion systems are a compact way to generate organic patterns from simple local rules. With the right parameters, you get spots, stripes, fingerprint-like flows, and worm-like growth, all from two scalar fields and a finite-difference update.

The demo below uses the Gray-Scott model, simulated on a CPU grid and rendered to a 2D canvas.

# Model Overview

The simulation tracks two chemical concentrations per cell:

`U`

: a base reagent`V`

: an activator/inhibitor reagent

At each step, both fields evolve by:

- Reaction terms (local chemistry)
- Diffusion terms (neighbor mixing)
- Feed/kill terms (continuous forcing)

The Gray-Scott equations are:

\[\begin{aligned} \frac{\partial U}{\partial t} &= D_u \nabla^2 U - U V^2 + f (1 - U) \\ \frac{\partial V}{\partial t} &= D_v \nabla^2 V + U V^2 - (f + k) V \end{aligned}\]```
const uvv = u * v * v;
du[i] = Math.max(0.0, u + Du * lapU - uvv + f * (1.0 - u));
dv[i] = Math.max(0.0, v + Dv * lapV + uvv - (f + k) * v);
```


Where:

| Symbol | Meaning |
|---|---|
`Du` , `Dv` | Diffusion rates for `U` and `V` |
`f` | Feed rate (injects `U` ) |
`k` | Kill rate (removes `V` ) |
`Lap(.)` | Spatial Laplacian operator |

The nonlinear term `U * V * V`

is the core interaction. It consumes `U`

while producing `V`

, and creates the instability that drives pattern formation.

# Discretization on the Grid

The demo stores each field in `Float32Array`

buffers of size `W * H`

:

- current state:
`u0`

,`v0`

- next state:
`u1`

,`v1`


This is explicit time stepping with double buffering. Read from current arrays, write to next arrays, then swap references.

## 9-Point Laplacian Stencil

For each cell, the code computes a weighted 8-neighbor Laplacian:

- axial neighbors (left, right, up, down): weight
`0.20`

- diagonal neighbors: weight
`0.05`

- center subtraction:
`-center`


So:

```
Lap(X) =
0.20 * (X_left + X_right + X_up + X_down)
+ 0.05 * (X_ul + X_ur + X_dl + X_dr)
- X_center
```


The weights sum to `1.0`

before subtracting the center value, which gives a discrete diffusion operator with a reasonably isotropic spread for this style of effect.

In the JavaScript loop, `computeLaplacian(u0, x, y)`

returns that same weighted combination so the familiar equation directly maps to `lapU`

and `lapV`

before the reaction terms run.

## Boundary Conditions

The grid wraps around on both axes, so the domain is topologically a torus. In practice:

`x = -1`

maps to`W - 1`

`x = W`

maps to`0`

- same for
`y`


This removes hard borders and keeps the global pattern flow continuous.

# Per-Cell Update

For each index `i`

:

```
const lapU = computeLaplacian(u0, x, y);
const lapV = computeLaplacian(v0, x, y);
const uvv = u * v * v;
du[i] = Math.max(0.0, u + Du * lapU - uvv + f * (1.0 - u));
dv[i] = Math.max(0.0, v + Dv * lapV + uvv - (f + k) * v);
```


The simulation clamps values to `>= 0`

to avoid drifting into invalid negative concentrations under explicit stepping. The demo also calculates multiple integration steps per rendered frame (see `stepsPerFrame`

) to speed up visual evolution without increasing display refresh rate.

# Initialization and Seeding

The baseline state is:

`U = 1.0`

`V = 0.0`


Then the demo injects one or more noisy circular perturbations where:

`U`

is lowered near`0.5`

`V`

is raised near`0.25`


Those seeded regions act as nuclei. Diffusion and reaction expand and reshape them until stable or quasi-stable structures emerge.

## Interaction

| Interaction | Effect |
|---|---|
| Center seed reset | Reset to baseline, then inject center seed. |
| Random multi-seed init | Clear field, then seed random islands. |
| Interactive brush painting | Paint reagent with pointer or touch input. |
| Right-click erase | Restore local cells to baseline (`U=1` , `V=0` ). |

# Rendering Path

Rendering maps concentration to color via a selected colormap. The implementation uses `U`

for visualization:

```
const t = 1.0 - clamp01(u0[i]);
colormap(t, pixels, j);
```


So cells with lower `U`

generally appear brighter/hotter in the default mapping, which highlights active reaction fronts and pattern boundaries.

Because the simulation and rendering are CPU-side, the full frame is written into `ImageData`

and uploaded with `putImageData`

.

# Parameter Intuition

In Gray-Scott systems, small parameter shifts can move the system between very different regimes.

| Parameter | Effect |
|---|---|
`f` | Sustains more activity and replenishes `U` . |
`k` | Suppresses `V` , which can collapse or simplify patterns. |
`Du` | Smooths and spreads `U` faster. |
`Dv` | Smooths and spreads `V` faster. |

The explicit update in the “Per-Cell Update” section shows how those terms fold into the discrete simulation loop.

The ratio and balance between these terms matter more than any single value. That is why curated preset tuples are useful for jumping into known regimes such as spots, stripes, and spirals.

The visual complexity is emergent. Every cell follows the same local update, but coupled nonlinear reaction plus diffusion creates self-organization across scales:

- fronts split and reconnect
- islands nucleate and disappear
- stripe domains compete and drift

No global shape logic exists in the code. Structure appears from repeated local interaction only.

# Practical Notes

`stepsPerFrame`

is a speed and stability tradeoff. Higher values evolve faster per rendered frame, but can overshoot if parameters are already near unstable boundaries.- Larger grids preserve finer detail but increase CPU cost per step.
- Toroidal wrapping avoids dead border effects when painting near edges.

If you want to experiment, start with a preset and then nudge one parameter at a time. In this model, tiny deltas can produce qualitatively different worlds.