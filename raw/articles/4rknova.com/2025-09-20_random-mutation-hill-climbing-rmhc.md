---
title: Random Mutation Hill Climbing (RMHC)
url: https://www.4rknova.com/blog/2025/09/20/rmhc
author: Nikolaos Papadopoulos
published: '2025-09-20'
source_blog: Nikos Papadopoulos - Portfolio
source_site: https://www.4rknova.com/
category: graphics
fetched: '2026-04-19'
---

# Evolving Images with Random‑Mutation Hill Climbing

I wanted to see how far I could get toward approximating a target image using nothing but overlapping translucent shapes and the Canvas 2D API. No machine learning, no long startup times, just something that kicks in instantly, stays responsive, and feels alive as you watch it evolve. The approach I settled on is called Random-Mutation Hill Climbing (RMHC), or the (1+1) Evolutionary Strategy. The idea is simple: Keep a single best-so-far solution, make one random change, and keep that change only if it reduces the error.

Frame by frame, that greedy loop slowly transforms a randomly initialized canvas into something that begins to resemble the target image. Because we only ever evaluate one candidate per iteration, it’s easy to budget computation per frame and keep the whole experience smooth and interactive.

Below you can play with the live demo. Click on ‘start’ to begin the simulation. Make sure to experiment with the parameters to see how they affect convergence.

# Why RMHC and not a Genetic Algorithm?

Genetic Algorithms (GAs) evolve a population of candidates, mixing them via crossover and pruning with fitness‑based selection. That design preserves diversity and explores the search space widely. That is great for rugged landscapes but very expensive per generation. RMHC is a population of one, no crossover, no diversity book keeping, and no per‑generation tournament. For browser‑based, frame‑budgeted rendering, where each evaluation means drawing and comparing pixels, the cheaper RMHC loop wins.

| Aspect | RMHC / 1+1 ES | Genetic Algorithm |
|---|---|---|
| Population | A single candidate | Many candidates |
| Variation | Mutation only | Crossover plus mutation |
| Selection | Accept if better | Fitness‑based over population |
| Diversity | None | Maintains diversity, avoids premature convergence |
| Parallelism | Sequential | Naturally parallel |
| Cost per generation | Very low | Higher |
| Best for | Smooth landscapes, tight compute budgets | Rugged landscapes, need for global search |

Because we can render only one candidate per frame, RMHC is ideal, it greedily climbs toward better images without the overhead of managing a population.

# What counts as DNA here?

The DNA is a plain array of shape objects. Array order is draw order (z‑index), so swapping two entries changes occlusion. Each shape stores its geometry (positions, radii, angles) and its color and alpha. To reduce per‑frame work, I cache a prebuilt `rgba(...)`

string and update it only when color changes.

Supported shapes include: triangles, rectangles (axis‑aligned and rotated), circles, ellipses, lines, quads, and cubic Béziers. The user can toggle which types are allowed, and future mutations respect those choices.

# Measuring Fitness with Mean Squared Error

Fitness is measured by how close the rendered candidate image is to the target. I use Mean Squared Error (MSE) over pixel intensities. Formally, if we have \(N\) pixels, each with RGB components, the MSE is:

\[\text{MSE} = \frac{1}{N} \sum_{i=1}^{N} \Big[(R_i - R'_i)^2 + (G_i - G'_i)^2 + (B_i - B'_i)^2\Big]\]where \(R_i, G_i, B_i\) are the target’s pixel values and \(R'_i, G'_i, B'_i\) are the candidate’s pixel values. Lower MSE means the candidate more closely matches the target. MSE is a standard choice in image processing because it penalizes larger errors quadratically, encouraging the algorithm to reduce big differences first.

A naïve full‑frame comparison on every mutation is too slow, so I use a two‑ stage check: first compute a sampled MSE over a fixed subset of pixels, only if that sample looks promising do we pay for a full‑image MSE to confirm improvement. This preserves the strict “only accept if better” property while cutting most of the work.

```
function imageDiffMSE_Sampled(a, b, idx) {
let sum = 0;
for (let k = 0; k < idx.length; k++) {
const i = idx[k];
const dr = a[i] - b[i];
const dg = a[i + 1] - b[i + 1];
const db = a[i + 2] - b[i + 2];
sum += dr*dr + dg*dg + db*db;
}
return sum / idx.length;
}
```


# Mutations that actually move the needle

Most iterations nudge a single parameter: a vertex shifts by a few pixels, a radius grows, a color channel changes slightly, or alpha is adjusted within a global cap. Two additional moves help escape plateaus: a type switch (keep color, respawn geometry as a different shape) and a z‑order swap (swap two genes so one shape draws above the other). Because translucency matters, changing draw order can unlock sudden fitness gains.

# The step loop, budgeted for the browser

I render the mutant on a working canvas and only copy to the best canvas when the change is accepted. A frame‑time budget determines how many mutations we can attempt before yielding back to the browser, so UI stays responsive even at thousands of tries per second.

```
function step(){
if (!running) return;
const start = performance.now();
const budget = Math.max(1, params.frameBudgetMs | 0);
const deadline = start + budget;
while (performance.now() < deadline) {
const mutation = proposeMutation();
const work = renderAndGetImageData(ctxWorking);
const sampled = imageDiffMSE_Sampled(work.data, target.data, sampleIdx);
let improved = false;
if (sampled <= bestFitness * 1.05) {
const exact = imageDiffMSE(work.data, target.data);
if (exact < bestFitness) {
bestFitness = exact;
improved = true;
drawDNA(ctxBest, dna, W, H);
}
}
if (!improved) rollback(mutation);
generation++;
}
requestAnimationFrame(step);
}
```


# Rendering and feedback loops

There are four canvases working in concert: the target (resized image), the best (accepted state), the working (mutant under test), and the error heatmap, which renders bright red values where the current image differs most from the target. A small fitness plot shows the downward trend of MSE over time as an indicator of progress even when the visual impact is small.

# Small engineering choices that make it fast

I preallocate and reuse the heatmap ImageData buffer to avoid allocating large arrays each update. I cache color strings per shape and flip a dirty bit only when needed, which cuts string creation and GC churn. To respect the frame budget without paying a syscall on every mutation, performance.now() is called only every n iterations. Sample pixel set is recalculated only when the canvas size or target changes, keeping the acceptance test stable from frame to frame.

# Closing thoughts

The charm of RMHC here is its ratio of simplicity to effect: mutate, test, keep only if better. Coupled with careful budgeting and a few pragmatic mutations. That is enough to grow a picture from noise directly in your browser, no models, no training, just pixels and patience.