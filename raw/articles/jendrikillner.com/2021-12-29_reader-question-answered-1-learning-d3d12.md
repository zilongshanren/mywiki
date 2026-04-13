---
title: Reader Question Answered 1 - Learning D3D12
url: https://www.jendrikillner.com/post/d3d12-learning-plan/
author: Jendrik Illner
published: '2021-12-29'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

There are a lot of tutorials and articles on Vulkan. I found very few tutorials for D3D12. Do you have some recommendations on how to start learning D3D12?


## Quick Start

To get started with the API quickly, I can recommend the following resource: [Raw DirectX 12](https://alain.xyz/blog/raw-directx12)

Provides a starting point repository that implements all the necessary elements to render a triangle into a window. The blog post walks through the code and briefly explains all used concepts.

If you have experience with other APIs, keep [A Comparison of Modern Graphics APIs](https://alain.xyz/blog/comparison-of-modern-graphics-apis) bookmarked to compare as you go along.

## API detailed walkthrough

If you enjoy reading an in-depth walkthrough of the API and concepts, I recommend the [3dgep](https://www.3dgep.com) series.

Part 1 and 2 give an introduction to the D3D12 API itself and how it interacts with the Windows environment.

Part 3 builds on top and presents possible implementations for higher-level abstractions. This also covers several related topics, such as memory management and resource state management.

Part 4 explains texturing in detail. This does not only cover the API but also explains related concepts such as texture filtering. Additionally presents how to use compute-shaders to generate mipmaps (smaller versions of textures) using the GPU.

## API specification

Questions about the specifics of the API? Or what the intended behavior should be? Start by looking into the official specification. These are available on GitHub.

What isn’t covered in the D3D12 specification can typically be found in the [Direct3D 11.3 Functional Specification](https://microsoft.github.io/DirectX-Specs/d3d/archive/D3D11_3_FunctionalSpec.htm) as many concepts still apply.

## Applied uses

Interested in how others applied the concepts for their own engines and frameworks?

Articles about the D3D12-based implementation of [Diligent Engine](http://diligentgraphics.com/diligent-engine/architecture/d3d12/).

The Microsoft Samples contain several samples to learn more about specific features you might be interested in the [DirectX-Graphics-Samples](https://github.com/Microsoft/DirectX-Graphics-Samples)

Especially the [mini-engine](https://github.com/Microsoft/DirectX-Graphics-Samples#miniengine-a-directx-12-engine-starter-kit). This provides a good starting point for experimentation as well as looking into how aspects got implemented.

## Performance Best Practices

With the power of the API also comes the responsibility to think about performance. Each manufacturer has recommendations on how best to take advantage of their hardware.

Below is a collection of some resources:

| Manufacturer | Link |
|---|---|
| AMD |
|

[Game Works - DX12 Do’s And Don’ts](https://developer.nvidia.com/dx12-dos-and-donts)[Optimization Guide for Graphics Gen11](https://www.intel.com/content/www/us/en/developer/articles/guide/developer-and-optimization-guide-for-intel-processor-graphics-gen11-api.html)## The road ahead

This should give an excellent starting point to keep you busy on your D3D12 learning journey. There is a lot more information out there. But I hope with the provided information it will be easier to find.

For example, take a look at my [Graphics Programming Article Database](https://www.jendrikillner.com/article_database/) to find some of them.

Is anything missing, or do you have a question about something else?
Feel free to reach out on Twitter [@jendrikillner](https://twitter.com/jendrikillner), and I will try to find the information and expand the guide so everyone can benefit.