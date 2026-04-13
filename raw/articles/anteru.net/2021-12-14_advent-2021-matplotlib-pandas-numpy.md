---
title: 'Advent 2021: Matplotlib, Pandas & Numpy'
url: https://anteru.net/blog/2021/advent-2021-matplotlib-numpy-pandas
published: '2021-12-14'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

Given I do like [Python](https://anteru.net/blog/2021/advent-2021-python) it should come at no surprise that I’ve also bought into the broader Python ecosystem. As a researcher and engineer, I regularly have to deal with large data sets and I can’t imagine handling them with anything but the combination of [Matplotlib](https://matplotlib.org/), [Pandas](https://pandas.pydata.org/) and [Numpy](https://numpy.org/). While it may make sense sometimes to plot a graph or do some calculation in an office spreadsheet application, it – in my experience – literally never pays off for anything automated. If you have a tool producing data, and you evaluate the data in a spreadsheet, you should do yourself a favor and look at those three libraries.

Matplotlib is a one-stop shop for getting anything plotted. It has all the plot types you’ll ever need and is highly customizable on top. I’ve yet to see a data set that I can’t sensibly visualize with Matplotlib, and if you’re wondering what you can do with it, take a look at the [gallery](https://matplotlib.org/stable/gallery/index.html). The fact that it’s super powerful is however only a small part of the story. It’s also easy to use and has a stable API – I’ve been running scripts from several years ago on the latest version and things just work. That gives me a lot of peace of mind when spending time writing elaborate visualizations. Finally, it can also produce print-quality illustrations for usage in papers. I’m speaking from experience here – all papers I wrote had all their plots done with Matplotlib!

Where Matplotlib is fantastic for plotting, Pandas is *the* best way to represent data at runtime in my experience. It’s Python and anything that looks like a list or dictionary can be plotted, but Pandas provides you with tons of utility functions which makes it feel like using a database backend without having to set one up. Do you want to select all rows within a particular range and then project down to a few columns? It’s a few lines of surprisingly readable code in Pandas. Especially when used in conjunction with Jupyter it’s a fantastic way to deal with large data sets.

Sometimes however you have too much data for Pandas to filter or Matplotlib to plot. A series of images rendered in 3840×2160 and you want to extract some information from there? That’s a job for Numpy, which is actually a numerical processing library written in C with a Python interface. Where Python will eventually slow down doing lots of math, Numpy will allow you to run with optimal efficiency and use the minimum amount of memory. The key feature of Numpy is that it never feels out of place doing so – you’re writing normal Python code and under the hood they execute it using super-optimized C kernels. It always looks and feels like “normal” Python.

The best part of those three tools is that you can combine them, as they all work together. With that, you can pre-process your data in Numpy, use Pandas to filter it, and Matplotlib to visualize it, all from one script, and without having to do complicated conversions. It’s a super powerful toolkit for data analysis – and I can’t imagine living without those tools any more!