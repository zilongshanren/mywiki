---
title: GPU Accelerated Diamond-Square Generation
url: https://www.vertexfragment.com/ramblings/diamond-square/
author: Steven Sell
published: '2022-10-31'
source_blog: Vertex Fragment
source_site: https://www.vertexfragment.com/
category: graphics
fetched: '2026-04-13'
---

![](../../assets/26d8ccd0f7c07797.png)


The Diamond-Square algorithm is a bounded noise algorithm that provides an equal balance between user controlled and random output. It takes in a 2D grayscale texture as its seed and generates a heightmap from it. First presented in 1982, it has the following characteristics:

- High level of user control of the output. Many noise algorithms provide only nominal control. With Diamond-Square the user can directly specify that they want a mountain here, or a lake there, even at a high level.
- It is finite in size and must be generated ahead of time. Many other noise algorithms operate over a theoretically infinite domain, whereas Diamond-Square is bounded to a square of size
`(2^n)+1`

. - Requires state, and thus has a potentially high memory requirement and is not suitable for on-the-fly queries or a pure-GPU implementation.
- It is relatively slow as it performs a large volume of self-sampling.

It is best used for generating a base heightmap which then other noises and effects (such as erosion) are applied on top of.

As noted above, one of the main downsides to Diamond-Square is its speed, making it unsuitable for real-time generation for larger domains. In this ramble I present two different implementations: multi-threaded C# and a GPU-accelerated version.

Unfortunately even the GPU-accelerated version is not fast enough to be run on a per-frame basis, but it is plenty fast enough to be run in a heightmap-generation situation that is run once (or at least infrequently). The table below shows the average amount of time, in milliseconds, for the Diamond-Square implementations to generate values over the specified texture dimensions.

| Implementation | 512 x 512 | 1024 x 1024 | 2048 x 2048 | 4096 x 4096 | 8192 x 8192 |
|---|---|---|---|---|---|
| Single-threaded C# | 38.3 | 161.6 | 740.2 | 2987.3 | 13042.1 |
| Multi-threaded C# | 26.7 | 67.9 | 224.4 | 823.9 | 3121.5 |
| GPU-Accelerated | 2.1 | 9.3 | 41.7 | 211.6 | 778.2 |

![](../../assets/84a525f05ce7dd1f.png)


The algorithm for Diamond-Square is relatively simple and is covered in detail in numerous other sources, [such as Wikipedia](https://en.wikipedia.org/wiki/Diamond-square_algorithm). It was one of the first noise algorithms I learned, originally coming across it [on GameDev.net](https://gamedev.net/) 15+ years ago.

It is run as [a fairly standard FBM](https://iquilezles.org/articles/fbm/), however unlike most noises we do not touch every pixel each iteration.

```
int stepSize = Dimensions / 2;
float amplitude = 0.5f;
float persistence = 0.5f;
while (stepSize > 0)
{
float offsetModifier = clamp(amplitude, 0.0, 1.0);
RunDiamondSteps(stepSize, offsetModifier);
RunSquareSteps(stepSize, offsetModifier);
stepSize /= 2;
amplitude *= persistence;
}
```


Instead, each pixel is set only once and instead we iterate over the domain at fixed step sizes: `Dimensions / 2`

, `Dimensions / 4`

, `Dimensions / 8`

, etc. For each iteration we perform all of the Diamond samples and then we perform the Square samples.

- Diamond: Samples from corner neighbors (upper left, upper right, lower left, lower right), average the samples, and then offset by a random value.
- Square: Samples from adjacent neighbors (left, right, above, below), average the samples, and then offset by a random value.

The random values should be on the range `[-1, 1]`

and decrease in size each iteration, according to the FBM amplitude and persistence values.

But what is sampled? Well, the noise values are seeded from a seed texture that must also be square and `2^n + 1`

in dimensions but may be smaller than the final noise dimensions. This allows for the user to specify a general high-level shape or design to the final heightmap but still allowing for a procedural and randomized output.

![](../../assets/784ef68449282fc7.png)


See [DiamondSquare.cs](https://github.com/ssell/GPU-Accelerated-Diamond-Square/blob/main/Assets/Source/Noise/DiamondSquare.cs)

As described in the above [Algorithm](https://www.vertexfragment.com#the-algorithm) section, the code takes the following steps:

- Initialize the
`Noise`

buffer from the provided seed texture. - Run a standard FBM where each iteration we
- Diamond steps, sampling the corner neighbors. The samples are averaged and offset by a random value.
- Square steps, sampling the adjacent neighbors. The samples are averaged and offset by a random value.
- Cut the step size in half, and multiply the amplitude by the persistence which reduces random offset.


And that is it.

The only wrinkle is that the steps are executed in the corresponding `DiamondStepJob`

and `SquareStepJob`

background jobs. These are run in [a custom self-processing thread queue](https://github.com/ssell/GPU-Accelerated-Diamond-Square/blob/main/Assets/Source/Utils/Threading/ThreadPool.cs), though one can easily substitute in [the .NET thread pool](https://learn.microsoft.com/en-us/dotnet/api/system.threading.threadpool?view=net-6.0) or a different custom solution.

See [DiamondSquareGPU.cs](https://github.com/ssell/GPU-Accelerated-Diamond-Square/blob/main/Assets/Source/Noise/DiamondSquareGPU.cs) and [DiamondSquare.compute](https://github.com/ssell/GPU-Accelerated-Diamond-Square/blob/main/Assets/Resources/Shaders/Compute/DiamondSquare.compute).

This implementation performs the heavy lifting on the GPU via [a Compute Shader](https://learn.microsoft.com/en-us/windows/win32/direct3d11/direct3d-11-advanced-stages-compute-shader). The Unity APIs around compute shaders make them very easy to work with, and they excel in situations such as this.

- Initialize the Compute Shader and corresponding Compute Buffers.
- Run a standard FBM where each iteration we
- Execute the Diamond Step on the GPU.
- Execute the Square Step on the GPU.
- Cut the step size in half, and multiply the amplitude by the persistence which reduces random offset.

- Marshall the final noise buffer from the GPU to the CPU.

That final step of moving the data to the CPU can actually constitute up to half the runtime of this implementation!

This was actually my third attempt at performing Diamond-Square on the GPU. My first was in a failed [ShaderToy](https://www.shadertoy.com/user/ssell) many years ago, but the requirement of maintaining state proved difficult using only a Fragment shader. I then had another go at this using Unity and a double-buffered render target used to track both noise values and “is set” values.

That attempt was nearly a success except for the “fuzziness” of working within a Fragment shader and interpolated float values. Diamond-Square requires selecting exact pixels within the data buffers/textures, and I found myself constantly being just off and so the result would be near to but not an exact match to the CPU-only implementation.

Then I remembered Compute Shaders, which admittedly I have not touched in ten years. These worked beautifully and the code ended up being very neat and clean. The results speak for themselves: 17x faster than the single-threaded C# implementation and 4x faster than the multi-threaded implementation running a worker for every 128x128 chunk.

![](../../assets/fe5eb4e1b796307e.png)

[https://github.com/ssell/GPU-Accelerated-Diamond-Square](https://github.com/ssell/GPU-Accelerated-Diamond-Square)