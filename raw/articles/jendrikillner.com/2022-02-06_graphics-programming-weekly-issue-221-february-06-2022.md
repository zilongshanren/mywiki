---
title: Graphics Programming weekly - Issue 221 - February 06, 2022
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-221/
author: Jendrik Illner
published: '2022-02-06'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the article presents a walkthrough of the process that leads to the blender obj exporting being sped up by 10x
- shows how to use the Superluminal profiler to spot the problems and iteratively improve the exporter

![](../../assets/30f710a77dda00e6.jpg)


- the article provides an overview of how SIMD execution models evolved over GPU generations
- presenting how the changes in architecture affect the way shaders would be authored to provide better performance mapping onto the hardware
- defines the standard terms such as swizzling/component masking and wave operations

![](../../assets/a1ab6b40c77a89a5.png)


- the article provides an overview of the state of 16-bit floating-point support in drivers, compilers tools, and hardware
- discusses how to take advantage of the hardware feature
- shows effects and tradeoffs to consider when moving shaders to use 16-bit floats

![](../../assets/7abb39f36adf7b16.jpg)


- the article discusses more noise distributions functions, presents grid-based noise definitions based on pixel positions alone
- shows the derivation of the noise function
- compares the function against White, Blue, Bayer, and more noise functions
- presents strengths and weaknesses of the distribution

![](../../assets/914eb79f0d9ccb67.png)


- the article presents why direct lighting computation should be separated from emitted light
- an approach to separate light emitters from other objects without tracking additional ray logic booleans is presented in the comments

![](../../assets/532bd1ee0cf20454.png)


You are helping our core team to develop cutting-edge 3D data optimization technology, being used in production pipelines to process millions of 3D data sets each year, fully-automatically. You are performing research on 3D mesh processing, texture baking, UV mapping, optimization algorithms and ML-based algorithms for 3D data optimization and QA.

![](../../assets/e1093cad59141f24.jpg)


- the article presents components are defining the direct lighting component
- shows the integral that needs to be solved, a brief explanation of the different aspects
- discusses problems with the presented technique
- additionally provides suggestions on how to deal with multiple lights

![](../../assets/20d48678d70ca630.png)


- the Vulkan survey presents a summary of the results and presents what next steps will be taken to address the feedback
- more investment into the Validation layer, macOSX support, more complete learning materials, and dropping VS2015 support

![](../../assets/3ece7b3db9ffb88e.jpg)


- the developer interview answers a large number of user questions
- discussing the status of the new Vulkan based renderer, dealing with the constant evolution of graphics requirements and effects on the art pipeline,
- many more topics, such as HDR motion blur, are covered

![](../../assets/872a4f6ff750e0f2.png)


- video lecture presents an introduction explaining how surfaces are light from lights
- shows the components that affect the calculation
- covers the Lambertian, Phong, and Blinn material model
- explains the transformations required to move between spaces, explaining how normals need special treatment

![](../../assets/c3fe967af16e8a73.png)


- the final video of the skeletal animation series using OpenGL and Assimp
- the tutorial series explained the whole process required to load information from the file format, interpret the data, and apply the necessary transformations to get animations in an OpenGL example application
- the last part discusses how to integrate the animation updating into the runtime

![](../../assets/2255c3c1de228030.png)


- 4 slides for a brief summary of the 4 common anti-aliasing techniques
- presenting the technique summary, discussing strengths and weaknesses

![](../../assets/0a774da5f5bef6de.jpg)

Thanks to [Panagiotis Tsiapkolis](http://panagiotis.tsiapkolis.com) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.