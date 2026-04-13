---
title: Python as scientific toolbox – 8 months later
url: https://bartwronski.com/2014/09/16/python-as-scientific-toolbox/
published: '2014-09-16'
source_blog: Bart Wronski
source_site: https://bartwronski.com
category: game programming
fetched: '2026-04-13'
---

I started this blog [with a simple post](https://bartwronski.com/2014/01/19/mathematics-toolbox/) about my attempts to find free Mathematica replacement tool for general scientific computing with focus on graphics. At that time I recommended scientific Python and [WinPython](http://winpython.sourceforge.net/) environment.

Many months have passed, I used lots of numerical Python at home, I used a bit of Mathematica at work and I would like to share my experiences – both good and bad as well as some simple tips to increase your productivity. This is not meant to be any kind of detailed description, guide or even tutorial – so if you are new to Python as scientific toolset, I recommend you to check out great [Scientific Python 101 by Angelo Pesce](http://c0de517e.blogspot.ca/2014/09/scientific-python-101.html) before reading my post.

My post is definitely not exhaustive and is very personal – if you have different experiences or I got something wrong – please comment! 🙂

## Use Anaconda distribution

In my original post I recommended WinPython. Unfortunately, I don’t use it anymore and at the moment I definitely can vote for [Anaconda](https://store.continuum.io/cshop/anaconda/). One quite obvious reason for that is that I started to use MacBook Pro and Mac OSX – WinPython doesn’t work there. I’m not a fan of having different working environments and different software on different machines, so I had to find something working on both Win and MacOSX.

Secondly, I’ve had some problems with WinPython. It works great as a portable distribution (it’s very handy to have it on USB key), but once you want to make it essential part of your computational environment, problems with its registration in system start to appear. Some packages didn’t want to install, some other ones had problems to update and there were conflicts in versions. I even managed to break distro by desperate attempts to make one of packages work.

[Anaconda ](https://store.continuum.io/cshop/anaconda/)is great. Super easy to install, has tons of packages, automatic updater and “just works”. Its registration with system is also good and “works”. Not all interesting packages are available through its packaging system, but I found no conflicts so far with Python pip, so you can work with both.

At the moment, my recommendation would be – if you have administrative rights on a computer, use Anaconda. If you don’t (working not on your computer), or want to go portable, have WinPython on your USB key – might be handy.

## Python 2 / 3 issue is not solved at all

This one is a bit sad and ridiculous – perfect example of what goes wrong in all kinds of open source communities. When someone asks me if they should get Python 2.7+ or 3.4+, I simply don’t have an easy answer – I don’t know. Some packages don’t work with Python 3, some others don’t work with Python 2 anymore. I don’t feel there is any strong push for Python 3, for “compatibility / legacy reasons”… Very weird situation and definitely blocks development of the language.

At the moment I use Python 2, but try to use imports from __future__ and write everything compatible with Python 3, so I won’t have problems if and when I switch. Still, I find lack of push in the community quite sad and really limiting the development/improvement of the language.

## Use IPython notebooks

My personal mistake was that for too long I didn’t use the [IPython ](http://ipython.org/)and its amazing notebook feature. Check out [this presentation](http://serialized.net/ipython_notebook_talk/#/), I’m sure it will convince you. 🙂

I was still doing oldschool code-execute-reload loop that was hindering my productivity. With Sublime Text and Python registered in the OS it is not that bad, but still, with IPython you can get way better results. Notebooks provide interactivity maybe not as good as Mathematica, but comparable to and much better than regular software development loop. You can easily re-run, change parameters, debug, see help and profile your code and have nice text, TeX or image annotations. IPython notebooks are easy to share, store and to come back to later.

Ipython as shell is also quite ok itself – even as environment to run your scripts from (with handy profiling macros, help or debugging).

## NumPy is great and very efficient…

NumPy is almost all you need for your basic numerical work. SciPy linear algebra packages (like distance arrays, least squares fitting or other regression methods) provide almost everything else. 🙂 For stuff like Monte Carlo, numerical integration, pre-computing some functions and many others I found it sufficient and performing very well. Slicing and indexing options can be not obvious at beginning, but once you get some practice they are very expressive. Big volume operations can boil down to a single expression with implicit loops over many elements that are internally written in efficient C. If you ever worked with Matlab / Octave you will feel very comfortable with it – to me it is definitely more readable than weird Mathematica syntax. Also interfacing with file operations and many libraries is trivial – Python becomes expressive and efficient glue code.

## …but you need to understand it and hack around silent performance killers

On the other hand, using NumPy very efficiently requires quite deep understanding of its internal way of working. This is obvious and true in case of any programming language, environment or algorithm – but unfortunately in case of numerical Python it can be very counter-intuitive. I won’t cover examples here (you can easily find numerous tutorials on numpy optimizations), but often writing efficient code means writing not very readable and not self-documenting code. Sometimes there are absurd situations like some specialized functions performing worse than generic ones, or need to write incomprehensible hacks (funniest one was suggestion to use complex numbers as most efficient way for simple Euclidean distance calculations)… Hopefully after couple numerically heavy scripts you will understand when NumPy does internal copies (and it does them often!), that any Python iteration over elements will kill your perf, that you need to try to use implicit loops and slicing etc.

## There is no easy way to use multiple cores

Unfortunately, multithreading, multitasking and parallelism are simply terrible in Python. Whole language wasn’t designed to be multitasked / multithreaded and Global Interpreter Lock as part of language design makes it a problem almost impossible to solve. Even if most NumPy code releases GIL, there is quite a big overhead from doing so and other threads becoming active – you won’t notice big speed-ups if you don’t have really huge volumes of work done in pure, single NumPy instructions. Every single line of Python glue-code will become a blocking, single-threaded path. And according to [Amdahl’s law](http://en.wikipedia.org/wiki/Amdahl's_law), it will make any massive parallelism impossible. You can try to work around it using multiprocessing – but in such case it is definitely more difficult to pass and share data between processes. I haven’t researched it exhaustively – but anyway no simple / annotation based (like in [OpenMP ](http://openmp.org/wp/)/ [Intel TBB](https://www.threadingbuildingblocks.org/)) solution exists.

## SymPy cannot serve as replacement for Mathematica

I played with SymPy just several times – it definitely is not any replacement for symbolic operations in Mathematica. It works ok for symbol substitution, trivial simplification or very simple integrals (like regular Phong normalization), but for anything more complex (normalizing Blinn-Phong level… yeah) it doesn’t work – after couple minutes (!) of calculations produces no answer. Its syntax is definitely not as friendly for interactive work like Mathematica as well. So for symbolic work it’s not any replacement at all and isn’t very useful. One potential benefit of using it is that it embeds nicely and produces nice looking results in IPython notebooks – can be good for sharing them.

## No very good interactive 3D plotting

There is [matplotlib](http://matplotlib.org/). It works. It has [tons of good features](https://www.wakari.io/sharing/bundle/ijstokes/pyvis-1h)…

…But its interactive version is not embeddable in IPython notebooks, 3D plotting runs very slow and is quite ugly. In 2D there is beautiful [Bokeh](http://bokeh.pydata.org/) generating interactive html files, but nothing like that for 3D. Nothing on Mathematica level.

I played a bit with [Vispy](http://vispy.org/) – if they could create as good WebGL backend for IPython notebooks like they promise, I’m totally for it (even if I have to code visualizations myself). Until then it is “only” early stage project for quickly mapping between numerical Python data and simple OpenGL code – but very cool and simple one, so it’s fun to play with it anyway. 🙂

## There are packages for (almost) everything!

Finally, while some Python issues are there and I feel won’t be solved in the near future (multithreading), situation is very dynamic and changes a lot. Python becomes standard for scientific computing and new libraries and packages appear every day. There are excellent existing ones and it’s hard to find a topic that wasn’t covered yet. Image processing? Machine learning? Linear algebra? You name it. Just import proper package and adress the problem you are trying to solve, not wasting your time on coding everything from scratch or integrating obscure C++ libraries.

Therefore I really believe it is worth investing your time in learning it and adapting to your workflow. I wish it became standard for many CS courses at universities instead of commercial Matlab, poorly interfaced Octave or professors asking students to write whole solutions in C++ from scratch. At least in Poland they definitely need more focus on problems, solutions and algorithms, not on coding and learning languages…

Nice post! My sentiments exactly across the board 🙂 +100 on using Anaconda (my first post was on trying to convince people to switch to it). Kudos!