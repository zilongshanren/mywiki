---
title: Graphics Programming weekly - Issue 38 — May 13, 2018
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-38/
author: Jendrik Illner
published: '2018-05-13'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

#
Graphics Programming weekly - Issue 38 — May 13, 2018

- experience of using vulkan with AMD drivers (stock and open source)
- comparison of register usage with different shader compilers



- Khronos event focused on experiences of game developers that ship Vulkan versions on May22 in Cambridge


- compressing animation key frames relative to the bind pose and presenting results
- results are data dependent, on Paragon dataset saves 7.9% but increases compression time


- new model for layered materials
- statistical analysis that uses an atomic decomposition of light transport to predict scattering in the layered structure
- per layer statistics are combined into a scattering function as mixture of microfacet models



- in-depth look at the distribution of display resolution across the VR display
- how this influences the mapping of renderer output results to the final display
- physical display resolution is the same on both headsets (1080×1200 per eye)
- Oculus favors resolution over FoV
- Vive has a higher FoV but reduced resolution



- tutorial course covering representation, usage and applications of voxel DAG and multiresolution hierarchies
- voxel DAG take advantage of duplicated data found in voxel data sets
- how to
- compress color information
- construct a DAG using CUDA
- raytrace the structure
- use it for shadows in static environments



- unicode overview
- overview of different font rendering techniques
- look at how Slug renders individual glyphs and what is required to present good results for lines of text



- explanation of rules that apply to shader input structures and interstage linking
- differences between HLSL and SPIR-V semantics
- shows how HLSL semantics are expressed in SPIR-V


- blog series about the mathematics of spherical gaussians
- a gaussian function that is defined on the surface of a sphere

- and how to use the techniques for normal map filtering



- videos from the Montreal Vulkan dev days have been uploaded