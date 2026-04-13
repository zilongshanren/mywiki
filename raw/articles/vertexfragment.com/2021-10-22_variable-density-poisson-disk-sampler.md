---
title: Variable Density Poisson-Disk Sampler
url: https://www.vertexfragment.com/ramblings/variable-density-poisson-sampler/
author: Steven Sell
published: '2021-10-22'
source_blog: Vertex Fragment
source_site: https://www.vertexfragment.com/
category: graphics
fetched: '2026-04-13'
---

![](../../assets/c47aa813195c0e0e.png)


Poisson Disk Samplers are an approach to generating blue noise which have some very useful properties in graphics and game programming. Perhaps chief among these is the ability to have random point generation while maintaining a minimum distance between points.

In this ramble I will be presenting two C# Poisson Disk Samplers - one with an uniform minimum distance (radius) across its domain, and the other with a variable radius that can be controlled by any sort of input. Naturally the uniform sampler provides better performance but at the cost of control. Both samplers are two-dimensional, [but are easily modified to handle any higher dimensions as needed](https://www.vertexfragment.com#source-code).

The focus will be on the implementation of the samplers, [with details about the underlying maths left to other source](https://www.vertexfragment.com#references).

![](../../assets/d6977c505de4fde8.png)


We will begin with the uniform sampler which uses a single minimum distance between points (sample radius) across the entire domain. This implementation is based on the paper [Fast Poisson Disk Sampling in Arbitrary Dimensions](https://www.cs.ubc.ca/~rbridson/docs/bridson-siggraph07-poissondisk.pdf), and such it can be easily extended to higher dimensions if your use case demands it.

At the risk of parroting the source material, a quick explanation of the algorithm we will use.

**Initialization**

- Initialize a spatial partitioning grid for quick neighbor queries.
- Initialize a
`SamplesList`

which contains all valid generated points. - Initialize an
`ActiveList`

which will contain our sample point candidates. - Generate a random point within our spatial domain (inside the bounds of our grid), and add it to our
`SamplesList`

and`ActiveList`

.

**Generation**

Once initialization is complete, the following steps are repeated until the `ActiveList`

is empty.

- Select a random point within the
`ActiveList`

. - Generate up to
`k`

random points in the annulus around the randomly chosen point. - If one of the
`k`

points is valid (no closer than the minimum distance to another point) then it is added to both lists and the loop exits. - If none of the
`k`

points were valid, then the randomly chosen point is removed from the`ActiveList`

(but remains in the`SamplesList`

).

Lets cover these steps in more detail with code samples.

For some context, our complete class will implement the following methods:

```
public sealed class UniformPoissonSampler2D
{
public UniformPoissonSampler2D(System.Random rng, float sampleRadius, float width, float height, int rejectionLimit = 30);
public bool Generate();
private void GenerateFirstPoint();
private void AddSample(ref Vector2 sample);
private int GetSpatialGridIndex(ref Vector2 sample);
private int GetRandomActiveListIndex();
private Vector2 GenerateRandomPointInAnnulus(ref Vector2 point);
private bool IsSampleOutOfBounds(ref Vector2 sample);
private bool IsSampleNearOthers(ref Vector2 sample);
private bool IsSampleNearSampleInCell(int lookupCell, ref Vector2 sample);
private bool SignalStopGenerating(bool success);
}
```


Our sampler will be using a spatial partitioning grid in the background in order to facilitate spatial queries. Each cell of the grid will be sized so that at most only one sample can inhabit it at a time. This helps reduce the number of intersection queries we have to perform during searches. Plus since we know the grid will be uniformly filled with potentially every cell having a sample within it, then there is no real waste that would normally be solved by a different spatial structure (such as a quadtree).

For our grid we will have the following properties:

`CellLength`

: The length of each side of a cell within the grid. All cells have the same dimension.`CellsPerX`

: The number of cells along the x-dimension of the grid.`CellsPerY`

: The number of cells along the y-dimension of the grid.`SpatialLookUp`

: A one dimensional array which contains our packed two-dimensional grid.

These will be initialized, along with our `ActiveList`

and `SamplesList`

, in an aptly named `Initialize`

method:

```
private void Initialize()
{
IsGenerating = true;
CellLength = Radius / MathUtils.Sqrt2;
CellsPerX = (int)Math.Ceiling(Width / CellLength);
CellsPerY = (int)Math.Ceiling(Height / CellLength);
int totalCells = CellsPerX * CellsPerY;
SpatialLookUp = new List<int>(totalCells);
ActiveList = new List<int>(totalCells);
SamplesList = new List<Vector2>();
CollectionUtils.Fill(SpatialLookUp, -1, totalCells);
}
```


The list representing the spatial grid, `SpatialLookUp`

, stores integers which are indices into the `SamplesList`

. All elements (grid cells) are initialized to `-1`

to indicate that the cell is empty.

`CellLength`

is defined as \(l = {r \over \sqrt{d}}\), where \(d\) is the dimension. This ensures that there will only ever be enough room for a single sample in each grid cell. This formula of course scales to higher dimensions if the sampler needs to be adapted to such purposes.
With the grid initialized we need a way to access the cells within it. This is done in the `GetSpatialIndex`

method where we simply return the cell that contains the requested `(x, y)`

position.

```
private int GetSpatialGridIndex(ref Vector2 sample)
{
int dx = (int)(sample.x / CellLength);
int dy = (int)(sample.y / CellLength);
return (dx + (dy * CellsPerX));
}
```


Next, we need to be able to add a new point to the grid. Adding to the grid indicates that the sample is valid, and as such also needs to be added to our `SamplesList`

. Additionally all new points are added to the `ActiveList`

so that we can attempt to generate more points around them, which is how our points spread across the domain.

```
private void AddSample(ref Vector2 sample)
{
int sampleIndex = SamplesList.Count;
int spatialIndex = GetSpatialGridIndex(ref sample);
SamplesList.Add(sample);
ActiveList.Add(sampleIndex);
SpatialLookUp[spatialIndex] = sampleIndex;
}
```


The last step before our setup is complete is to be able to provide some basic spatial queries for our grid. This will let us check if a new point is valid - that there are no other points within the minimum distance. This is implemented in two functions: `IsSampleNearOthers`

and `IsSampleNearSampleInCell`

.

```
private bool IsSampleNearOthers(ref Vector2 sample)
{
int prospectiveCell = GetSpatialGridIndex(ref sample);
if ((prospectiveCell == -1) || SpatialLookUp[prospectiveCell] != -1)
{
return true;
}
for (int y = -1; y <= 1; ++y)
{
for (int x = -1; x <= 1; ++x)
{
int neighbor = prospectiveCell + x + (y * CellsPerX);
if (IsSampleNearSampleInCell(neighbor, ref sample))
{
return true;
}
}
}
return false;
}
```


So we get the cell that our sample will inhabit via our `GetSpatialGridIndex`

. We first check to make sure that that cell is empty and then we check the immediate neighbor cells. As we sized our grid cells such that only one sample could be in each cell it also holds that each sample can only potentially overlap the immediate neighboring cells. If any of the neighbor cells contains a sample which overlaps our prospective one, then that the new sample is rejected.

```
private bool IsSampleNearSampleInCell(int lookupCell, ref Vector2 sample)
{
if ((lookupCell < 0) || (lookupCell >= SpatialLookUp.Count))
{
return false;
}
int cellSampleIndex = SpatialLookUp[lookupCell];
if (cellSampleIndex == -1)
{
return false;
}
return Vector2.Distance(sample, SamplesList[cellSampleIndex]) <= Radius;
}
```


Here we simply validate the neighbor cell (as we could be looking out-of-bounds) and if it contains a point, checking the distance between that point and the prospective point. Now the spatial grid is fully set up with all needed accessors and spatial queries.

![](../../assets/ab011ef065f6cab9.png)


Before we can implement our generation loop, we need one more method implemented: `GenerateRandomPointInAnnulus`

.

The *annulus* is a ring around a point defined by an inner radius and an outer radius. As we want to ensure that no point is closer than our minimum distance then we use that as the inner radius. The outer radius can really be any value larger than that, and we simply use twice the inner radius for the outer.

For sampling we use two random values:

- Distance from the center, on the range \([r, 2r]\)
- Angle, on the range \([0, 2\pi]\)

With these we have a random point within the annulus.

```
private Vector2 GenerateRandomPointInAnnulus(ref Vector2 point)
{
float min = Radius;
float max = Radius * 2.0f;
float distance = ((float)Rng.NextDouble() * (max - min)) + min;
float angle = (float)Rng.NextDouble() * MathUtils.Pi2;
return new Vector2(
point.x + ((float)Math.Cos(angle) * distance),
point.y + ((float)Math.Sin(angle) * distance));
}
```


We can now move on to the actual noise generation now that all initialization is complete and utilities are ready.

As stated earlier, we begin by generating a random point within our domain. This will be the first entry into both our `SamplesList`

and `ActiveList`

, and the algorithm will build off of this point and spread across the entire domain.

```
private void GenerateFirstPoint()
{
Vector2 sample = new Vector2(
(float)Rng.NextDouble() * Width,
(float)Rng.NextDouble() * Height);
AddSample(ref sample);
}
```


We call this within our `Generate`

method, immediately following initialization.

```
public bool Generate()
{
if (IsGenerating)
{
return false;
}
Initialize();
GenerateFirstPoint();
// ...
return SignalStopGenerating(true);
}
```


With one point in our `ActiveList`

we can begin our main loop.

```
while (ActiveList.Count > 0)
{
bool sampleFound = false;
int activeIndex = GetRandomActiveListIndex();
Vector2 currentSample = SamplesList[ActiveList[activeIndex]];
for (int i = 0; i < RejectionLimit; ++i)
{
Vector2 randomSample = GenerateRandomPointInAnnulus(ref currentSample);
if (!IsSampleOutOfBounds(ref randomSample) && !IsSampleNearOthers(ref randomSample))
{
AddSample(ref randomSample);
sampleFound = true;
break;
}
}
if (!sampleFound)
{
ActiveList.RemoveUnorderedAt(activeIndex);
}
}
```


Breaking the above down, we loop through our `ActiveList`

until it is empty. On each iteration we choose a random sample point and attempt to generate a new valid point around it. If we can successfully generate a new point then that point is added to both the `ActiveList`

and `SamplesList`

and we continue to the next random point. However, if no point was generated within our allowed number of tries then we consider the space around the point to be filled and we remove it from the `ActiveList`

.

And with that, our uniform sampler is complete. Given a domain and sample radius we can fill it with random points that are guaranteed to be a minimum distance from any other point. This can be used in a whole host of applications and can be easily extended to toher domains or adapated to other languages.

For the final complete implementation, see the [source code](https://www.vertexfragment.com#source-code).

![](../../assets/170928763a742f04.png)


While the uniform sampler is fast, it has a distinct lack of control which may hinder it certain applications. This is where the variable sampler comes in, which trades in some performance with a much greater degree of control of the final output by allowing for variable sized sampling radii.

This particular implementation allows for complete control over the radius which can be driven off of a sampled texture, noise generator, or any other control. It is built off of the uniform sampler and uses the same core generation loop, and has the following distinctions:

- The underlying spatial grid is enhanced and moved into its own dedicated class.
- The current radius value is determed by a delegate that is invoked for each point.

The first step could also consist of replacing the grid entirely with another spatial structure, one that you may already have on hand. However it is imperative that the radius of each individual point is tracked and respected.

In order to accomodate variable radii we need a more flexible spatial grid (or other structure).

For this purpose a new class is added, `SpatialGrid2D<T>`

, which is used by our new `VariablePoissonSampler2D`

. However the implementation of this grid is nearly twice the length of our uniform sampler. As such, we will only discuss at a high level the changes made to the grid. The implementation can be seen (or copy+pasted) from [the source code](https://www.vertexfragment.com#source-code).

The key changes being:

- Each cell may now contain more than one sample point. However we try to optimize our cell size based on a provided
`minRadius`

and`maxRadius`

. The minimum and maximum values are not enforced, but accurate values help to create a better fitting grid. - The radius of each point must be tracked in addition to its
`(x, y)`

position. - Depending on the radius of a point, it may be present in more than one cell at a time.
- Depending on the radius of a point, we may check more than 1 depth of neighboring cells for intersections.

This particular grid was also updated to allow a generic object (`T`

) to be stored within the grid alongside each point. While not necessary for our poisson samplers, it does allow the grid to be used for other purposes.

With the `SpatialGrid2D`

, the variable poisson sampler is approximately ~30% less code than the uniform sampler and the majority of the remaining code is nearly identical to the uniform implementation.

If your library already has a QuadTree, BVH Tree (sphere bounds), etc. then go ahead and use it. This spatial grid was whipped up very quickly, and while it works for these samplers there has been no real tests or performance optimizations made to it.

With our new grid in place we can now implement our variable sampling radius.

Within our `VariablePoissonSampler2D`

we want to add a new delegate:

```
public sealed class VariablePoissonSampler2D
{
public delegate float GetRadiusAt(float x, float y);
// ...
```


This defines the function signature used to provide our radius value. Next we modify our `Generate`

and `Initialize`

methods to take in the delegate and a min/max sample radius.

```
public bool Generate(GetRadiusAt radiusFunc, float minRadius, float maxRadius)
{
if (IsGenerating)
{
return false;
}
Initialize(minRadius, maxRadius);
GenerateFirstPoint();
// ...
private void Initialize(float minRadius, float maxRadius)
{
IsGenerating = true;
SpatialGrid = new SpatialGrid2D<int>(Width, Height, minRadius, maxRadius);
ActiveList = new List<int>(SpatialGrid.CellsPerX * SpatialGrid.CellsPerY);
Samples = new List<Vector2>();
}
```


As discussed in the previous section, the `minRadius`

and `maxRadius`

are only used to optimize the cell sizes of our new spatial grid. There is no enforcement on these limits. A couple of modifications to the main generation loop and we will be done with our upgrade to a variable sampler:

```
while (ActiveList.Count > 0)
{
bool sampleFound = false;
int activeIndex = GetRandomActiveListIndex();
Vector2 currentSample = Samples[ActiveList[activeIndex]];
for (int i = 0; i < RejectionLimit; ++i)
{
float radius = radiusFunc(currentSample.x, currentSample.y);
Vector2 randomSample = GenerateRandomPointInAnnulus(ref currentSample, radius);
if (SpatialGrid.AddIfOpen(Samples.Count, randomSample.x, randomSample.y, radius))
{
AddSample(ref randomSample);
sampleFound = true;
break;
}
}
if (!sampleFound)
{
ActiveList.RemoveUnorderedAt(activeIndex);
}
}
```


Much of this is the exact same as the uniform sampler except for two sections:

`float radius = radiusFunc(currentSample.x, currentSample.y);`


Here we call into our delegate to retrieve the sampling radius for the current position. And then,

`if (SpatialGrid.AddIfOpen(Samples.Count, randomSample.x, randomSample.y, radius))`


We use our new spatial grid to check if a potential spot is open, and if so to add the point to the grid.

And that is it!

Our uniform sampler has been upgraded to a variable sampler and is ready to be used. As is evident by now, one way to drive the sample radius is by using an input texture and calculating a radius based on the pixel value. This is how the Stanford Bunny images were produced and an example of such code in Unity is shown below.

```
public List<Vector2> GenerateVariablePoissonSamples(
Texture2D control,
float width,
float height,
int seed)
{
System.Random rng = new System.Random(seed);
VariablePoissonSampler2D sampler = new VariablePoissonSampler2D(rng, width, height, 30);
sampler.Generate((float x, float y) =>
{
float u = (x / (float)Width);
float v = (y / (float)Height);
float r = control.GetPixelBilinear(u, v).r;
return Mathf.Lerp(MinRadius, MaxRadius, r);
}, width, height);
return sampler.Samples;
}
```


Of course textures aren’t the only way to control density. I suggest to play around with other schemes, and even try modifying the sampler to allow for multiple passes and see what sorts of patterns can be generated from that.

![](../../assets/4451522fcf1e261c.png)


![](../../assets/fe5eb4e1b796307e.png)

[https://github.com/ssell/VariablePoissonSampler](https://github.com/ssell/VariablePoissonSampler)

Above is an Unity sample project with the following:

`UniformPoissonSamplerND`

- C# version of the originally described sampler that supports \(n\) dimensions.`UniformPoissonSampler2D`

`VariablePoissonSampler2D`

`SpatialGrid2D<T>`

- Utility script for outputting the generated samples to a texture.

The 2D samplers only use Unity for the `Vector2`

which can be easily swapped out if you are using a different framework.

The code is for reference and educational purposes only. No guarantee is given towards the stability, correctness, or well any other characteristic by which it could be measured.

**Primary Source:**

[Fast Poisson Disk Sampling in Arbitrary Dimensions](https://www.cs.ubc.ca/~rbridson/docs/bridson-siggraph07-poissondisk.pdf)[Accompanying C++ sample code](https://www.cs.ubc.ca/~rbridson/download/curlnoise.tar.gz)buried in the authors[personal webpage](https://www.cs.ubc.ca/~rbridson/).


**References and Further Reading**

[Poisson Disk Sampling](http://devmag.org.za/2009/05/03/poisson-disk-sampling/): Good general purpose information about Poisson-Disk Samplers and discusses variable samplers. Looking back at this, did I really need to make this ramble?[Mitchell’s Best Candidate](https://bl.ocks.org/mbostock/1893974): Minimal poisson demonstration, but the accompanying JavaScript provides some insight. This one uses a quadtree for the spatial structure, but I didn’t have a suitable one at hand to plug in.[Generating Blue Noise Sample Points With Mitchell’s Best Candidate Algorithm](https://blog.demofox.org/2017/10/20/generating-blue-noise-sample-points-with-mitchells-best-candidate-algorithm/): Another good source of general blue noise information which I found helpful when learning all of this the first time.[Efficient Implementation of a QuadTree for 2D Collision Detection](https://stackoverflow.com/questions/41946007/efficient-and-well-explained-implementation-of-a-quadtree-for-2d-collision-det): This is a StackOverflow post that some spatial data structure god decided to deign with their appearance. It is full of information about how to implement a quadtree, loose quadtree, and of course a spatial grid. The legend who posted the information doesn’t even have a real account, and the sample code was posted to Pastebin. The spatial grid used here is influenced by the one they described, but was thrown together over the course of an hour or so.