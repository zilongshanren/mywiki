---
title: 3D Software Renderer - Adrian Courrèges
url: http://www.adriancourreges.com/projects/3d-software-renderer/
author: Adrian Courrèges
published: '2015-11-02'
source_blog: Adrian Courrèges
source_site: http://www.adriancourreges.com/
category: graphics
fetched: '2026-04-13'
---

This demo is a 3D renderer written from scratch, entirely in software.

It supports vertex transformation, perspective projection, triangle/line rasterization,

lighting (ambient & specular), Z-buffer and a wireframe mode.

Feel free to play with some of the parameters below.

### Demo applet

### Notes

The model is defined by polygon triangulation and is composed of about 3000 vertices, with a color associated to each one.

Segment rasterization is done by using the Bresenham algorithm.

Triangles are filled using linear interpolation based on the color of their 3 vertices. (barycentric interpolation)


The rendering also uses a Z-buffering technique to handle correctly the depth and make the triangle rendering order-independent.


Lightning is computed based on the Gouraud shading algorithm.