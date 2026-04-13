---
title: On pursuit of (good) free mathematics toolbox
url: https://bartwronski.com/2014/01/19/mathematics-toolbox/
published: '2014-01-19'
source_blog: Bart Wronski
source_site: https://bartwronski.com
category: game programming
fetched: '2026-04-13'
---

## Introduction

Mathematics are essential part of (almost?) any game programmers work. It was always especially important in work of graphics programmers – all this lovely linear algebra and analytic geometry! – but with more powerful hardware and more advanced GPU rendering pipelines it becomes more and more complex. 4×4 matrices and transformations can be trivially simplified by hand and using a notebook as a main tool, but recently, especially with physically based shading becoming an industry standard we need to deal with integrals, curve-fitting and various functions approximations.

Lots of this is because of trying to fit complex analytical models or real captured data. Doesn’t matter if you look at rendering equation and BRDFs, atmospheric scattering or some global illumination – you need to deal with complex underlying mathematics and learn to simplify them – to make it run with decent performance or to help your artists. Doing so you cannot introduce visible errors or inconsistency.

However understanding maths is not enough – getting results quickly, visualizing them and being able to share with other programmers is just as important – and for this good tools are essential.

## Mathematica

[Mathematica ](http://www.wolfram.com/mathematica/)is an awesome mathematics package from [Wolfram ](http://www.wolfram.com/)and is becoming an industry standard for graphics programmers. We use it at work, some programmers exchange and publish their Mathematica notebooks (for example last year’s Siggraph course “Physically Based Shading” [downloadable material ](http://blog.selfshadow.com/publications/s2013-shading-course/)includes some). Recently there was an [excellent post](http://www.altdevblogaday.com/2013/10/07/wolframs-mathematica-101/) on #AltDevBlog by [Angelo Pesce](http://c0de517e.blogspot.ca/) on Mathematica usage and it definitely can help you get into using this awesome tool.

However, rest of this post is not going to be about Mathematica. Why not stick with it as a main toolbox? There are couple reasons:

- While this is a great tool and if you work in a decent company you probably can get a licence, it is not free… So lots of people (including me) will look for some free alternatives for their personal use – for example at home or in travel.
- Mathematica syntax can get some time to learn and get used to. I don’t use it daily and every time I do, I have to check “how to do x/y”. Some other languages can be more programmer-friendly – especially if you use them for other purposes.
- Finally, using it for anything other than pure mathematics is not an easy and common thing. You cannot quickly find or write a tool that will load data from obscure file format, interface it with network (to fetch data from internet database) or do something else with generated data.

## Use a programming languages?

For various smaller personal tasks that are not performance-critical like scripting, quickly prototyping or even demonstrating algorithms I always loved “modern” or scripting languages. I find myself coding often in C#/.NET, but just the project setup for some smallest tasks can be consuming too much time relative to the time spent solving problems. Since couple years I used Python on several occasions and always really enjoyed it. Very readable, compact and self-contained code in 1 file were a big advantage for me – just like great libraries (there is even OpenCL / CUDA Python support) or language-level support for basic collections. So I started to check for options of using Python as mathematics and scientific toolset and viola – Numpy and Scipy!

## NumPy and SciPy

So what are those packages?

[NumPy ](http://www.numpy.org/)is a linear algebra package implemented mostly in native code. It supports n-dimensional arrays and matrices, various mathematical functions and some useful sub-packages as for example random number generators. It’s functionality is quite comparable to pure Matlab or open-source [GNU Octave](http://www.gnu.org/software/octave/) (which I used extensively during university studies and it worked quite ok). Due to native-code implementation, it is orders of magnitude faster than the same functions implemented in Python. Python serves only as glue code to tie everything together – load the data, define functions and algorithms etc. So this way we keep simplicity and readability of Python code and performance of native-written applications. As NumPy releases the Python’s GIL (global interpreter lock), its code is very easily parallelizable and can be multi-threaded.

Just NumPy allowed me to save some time, but its capabilities are limited comparing to full Matlab or Mathematica. It doesn’t even have plotting functions… That’s where the [SciPy](http://scipy.org/) comes into play. This is a fully featured mathematical and scientific package, containing everything from optimization (finding function extremes), numerical integration, curve-fitting, k-means algorithms, to data mining and clustering methods… Just check it out on official page or [wikipedia](http://en.wikipedia.org/wiki/SciPy#The_SciPy_Library.2FPackage). It also comes with nice plotting library Matplotlib, which handles multiple types of plots, 2D, 3D etc. Using numpy and scipy I have almost everything I really need.

## My setup

One of quite big disadvantages of Python environment, especially on Windows is quite terrible installation, setup and packaging. Downloading tons of installers, hundreds of conflicting versions and lack of automatic update. Linux (and probably Mac?) users are way more lucky, automatic packaging systems solve most of problems.

That’s why I use (and recommend to everyone) [WinPython package](http://winpython.sourceforge.net/). It is a portable distribution, you can use it right away without installing. Getting a new version is just downloading the new package. If you want, you can “register” it in Windows as a regular Python distribution, recognized by other packages. It has not only Python distribution – but also some package management system, editors, better shells (useful especially for non-programmers who want to use it in interactive command line style) and most importantly [all interesting packages](http://sourceforge.net/p/winpython/wiki/PackageIndex_33/)! Just download it, unpack it, register it with windows in “control panel” exe, maybe add to system env PATH and you can start your work.

I usuallly don’t use the text editor and shell that comes with it. Don’t get me wrong – Spyder is quite decent, it has support for debugging and allows you to work without even setting any directories/paths in system. However as I mentioned previously, one of my motivations for looking for some other environment than Mathematica was possibility to have one env for “everything” and running and learning yet another app doesn’t satisfy those conditions.

Instead I use a general-purpose text editor [Sublime Text](http://www.sublimetext.com/) that I was recommended by a friend and I just love it. This is definitely the best and easiest programmers text editor I have used so far – and it has some basic “Intellisense-like” features, syntax coloring for almost any language, build-system features, projects, package manager, tons of plugins and you can do everything using either your mouse or keyboard. It looks great on every platform and is very user friendly (so don’t try to convert me, vim users! 😉 ). Trial is unlimited and free, so give it a try or just check out its programmer-oriented text-editing features on website – and if you like it, buy the licence.

So basically to write a new script I just create new tab in Sublime Text which I have always opened, write code (which almost always ends up in 10-100 lines for simple math related tasks), save it in my draft folder with .py extension, press ctrl+b and get it running – definitely the workflow I was looking for. 🙂

## Main limitation (?) and final words

One quite serious limitation for various graphics-related work is lack of symbolic analysis comparable to Mathematica in NumPy/SciPy. We are very often interested in finding integrals and then simplifying them under some assumptions. There is [one package and one tool](https://github.com/sympy/sympy/wiki/SymPy-vs.-Sage) in Python to help in those tasks, sympy is even part of SciPy and WinPython package – but I’ll be honest – I haven’t used them, so cannot really say anything more… If I will have any experience with them, I will probably write a follow-up post. For the time being I still stick with Mathematica as definitely the best toolset for symbolic analysis.

To demonstrate usage of Python in computer-graphics related mathematical analysis, I will try to back up some of my future posts with simple Python scripts and I hope this will help at least some of you.

## References

[1] [http://www.wolfram.com/mathematica/](http://www.wolfram.com/mathematica/)

[4] [http://c0de517e.blogspot.ca/](http://c0de517e.blogspot.ca/)

[6] [http://www.gnu.org/software/octave/](http://www.gnu.org/software/octave/)

[9] [http://winpython.sourceforge.net/](http://winpython.sourceforge.net/)

Pingback: Python as scientific toolbox – 8 months later | Bart Wronski