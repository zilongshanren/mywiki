---
title: Poisson disk/square sampling generator for rendering
url: https://bartwronski.com/2014/08/08/poisson-disksquare-sampling-generator-for-rendering/
published: '2014-08-08'
source_blog: Bart Wronski
source_site: https://bartwronski.com
category: game programming
fetched: '2026-04-13'
---

I have just [submitted onto GitHub small new script – Poisson-like distribution sampling generator ](https://github.com/bartwronski/PoissonSamplingGenerator)suited for various typical rendering scenarios.

Unlike other small generators available it supports many sampling patterns – disk, disk with a central tap, square, repeating grid.

It outputs ready-to-use (and C&P) patterns for both hlsl and C++ code. It plots pattern on very simple graphs.

Generated sequence has properties of maximizing distance for every next point from previous points in sequence. Therefore you can use partial sequences (for example only half or a few samples based on branching) and have proper sampling function variance. It could be useful for various importance sampling and temporal refinement scenarios. Or for your DoF (branching on CoC).

*Edit: I added also an option to optimize sequences for cache locality. It is very estimate, but should work for very large sequences on large sampling areas.*

## Usage

Just edit the options and execute script: “*python poisson.py*“. 🙂

## Options

Options are edited in code (I use it in Sublime Text and always launch as script, so sorry – no commandline parsing) and are self-describing.

# user defined options disk = False # this parameter defines if we look for Poisson-like distribution on a disk (center at 0, radius 1) or in a square (0-1 on x and y) squareRepeatPattern = True # this parameter defines if we look for "repeating" pattern so if we should maximize distances also with pattern repetitions num_points = 25 # number of points we are looking for num_iterations = 16 # number of iterations in which we take average minimum squared distances between points and try to maximize them first_point_zero = disk # should be first point zero (useful if we already have such sample) or random iterations_per_point = 64 # iterations per point trying to look for a new point with larger distance sorting_buckets = 0 # if this option is > 0, then sequence will be optimized for tiled cache locality in n x n tiles (x followed by y)

## Requirements

This simple script requires some scientific Python environment like Anaconda or WinPython. Tested with Anaconda.

Have fun sampling! 🙂