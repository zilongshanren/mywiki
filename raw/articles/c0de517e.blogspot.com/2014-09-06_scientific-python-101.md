---
title: Scientific Python 101
url: https://c0de517e.blogspot.com/2014/09/scientific-python-101.html
published: '2014-09-06'
source_blog: C0DE517E
source_site: https://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

**Introduction to "Scientific Python"**



In this I'll assume a basic knowledge of Python, if you need to get up to speed,

[learnXinYminute](http://learnxinyminutes.com/docs/python/)is the best resource for a programmer.
With "Scientific Python" I refer to an ecosystem of python packages built around

[NumPy/SciPy/IPython](http://scipy.org/). I recommend installing a scientific python distribution, I think[Anaconda](https://store.continuum.io/cshop/anaconda/)is by far the best ([PythonXY](https://code.google.com/p/pythonxy/)is an alternative), you could grab the packages from[pypi/pip](https://pypi.python.org/pypi/pip)from any Python distribution, but it's more of a hassle.
NumPy is the building block for most other packages. It provides a matlab-like n-dimensional array class that provides fast computation via

[Blas](http://en.wikipedia.org/wiki/Basic_Linear_Algebra_Subprograms)/[Lapack](http://www.netlib.org/lapack/). It can be compiled with a variety of Blas implementations (Intel's MKL, Atlas, Netlib's, OpenBlas...), a perk of using a good distribution is that it usually comes with the fastest option for your system (which usually is multithreaded MKL). SciPy adds more numerical analysis routines on top of the basic operations provided by NumPy.
IPython (Jupyter) is a notebook-like interface similar to Mathematica's (really, it's a client-server infrastructure with different clients, but the only one that really matters is the HTML-based notebook one).

An alternative environment is



An alternative environment is

[Spyder](https://code.google.com/p/spyderlib/), which is more akin to[Matlab's](http://www.mathworks.com/products/matlab/)or[Mathematica Workbench](http://www.wolfram.com/products/workbench/)(a classic IDE) and also embeds IPython consoles for immediate code execution.
Especially when learning, it's probably best to start with IPython Notebooks.

**Why I looked into SciPy**

While I really like

[Mathematica](http://www.wolfram.com/mathematica)for exploratory programming and scientific computation, there are a few reasons that compelled me to look for an alternative (other than Wolfram being[an ass](http://vserver1.cscs.lsa.umich.edu/~crshalizi/reviews/wolfram/)that I hate having to feed).
First of all, Mathematica is commercial -and- expensive (same as Matlab btw). Which really doesn't matter when I use it as a tool to explore ideas and make results that will be used somewhere else, but it's



**really bad**as a programming language.
I wouldn't really want to redistribute the code I write in it, and even

Python, in comparison, is very well known, free, and integrated pretty much everywhere. I can

[deploying "executables" is not free](http://www.wolfram.com/player-pro/). Not to mention not many people know Mathematica to begin with.Python, in comparison, is very well known, free, and integrated pretty much everywhere. I can

[drop my code directly](http://docs.autodesk.com/MAYAUL/2014/JPN/Maya-API-Documentation/python-api/index.html)(or any other package really, python is everywhere) for artists to use, for example.**in Maya**
Another big advantage is that Python is familiar, even for people that don't know it, it's a simple imperative scripting language.

Mathematica is in contrast a very odd Lisp, which will look strange at first even to people who know other Lisps. Also, it's mostly about symbolic computation, and the way it evaluate can be quite mysterious.


Lastly, a potential problem lies in the fact that python packages aren't guaranteed to have all the same licensing terms, and you might need many of them. Verifying that everything you end up installing can be used for commercial purposes is a bit of a hassle...

Mathematica is in contrast a very odd Lisp, which will look strange at first even to people who know other Lisps. Also, it's mostly about symbolic computation, and the way it evaluate can be quite mysterious.

[CPython internals](https://github.com/amygdalama/python-internals)on the other hand, can be quite easily understood.Lastly, a potential problem lies in the fact that python packages aren't guaranteed to have all the same licensing terms, and you might need many of them. Verifying that everything you end up installing can be used for commercial purposes is a bit of a hassle...

**How does it fare?**

**It's free. It's integrated everywhere. It's familiar. It has lots of libraries.**


**It works**. It -can- be used as a Mathematica or Matlab replacement, while being free, so every time you need to redistribute your work (research!) it should be considered.

But it has still (many) weaknesses.

As a tool for exploratory programming, Mathematica is miles ahead. Its documentation is great, it comes with a larger wealth of great tools and its visualization options are probably the best bar none.

Experimentation is an order of magnitude better if you have good visualization and interactivity support, and Mathematica, right now, kills the competition on that front.

Manipulate[] is extremely simple, plotting is decently fast and the quality is quite high, there is lots of thought behind how the plots work, picking reasonable defaults, being numerically reliable and so on.


In Python on the other hand you get IPython and matplotlib. Ok, you got a ton of other libraries too, but matplotlib is popular and the basis of many others too.

IPython can't display output if assignments are made, and displays only the last evaluated expression. Matplotlib is really slow, really ugly, and uses a ton of memory. Also you can either get it integrated in IPython, but with zero interactivity, or in a separate window, with just very bare-bones support for plot rotation/translation/scale.


There are other tools you can use, but most are 2D only, some are very fast and 3D but more cumbersome to use and so on and so forth...




Experimentation is an order of magnitude better if you have good visualization and interactivity support, and Mathematica, right now, kills the competition on that front.

Manipulate[] is extremely simple, plotting is decently fast and the quality is quite high, there is lots of thought behind how the plots work, picking reasonable defaults, being numerically reliable and so on.

In Python on the other hand you get IPython and matplotlib. Ok, you got a ton of other libraries too, but matplotlib is popular and the basis of many others too.

IPython can't display output if assignments are made, and displays only the last evaluated expression. Matplotlib is really slow, really ugly, and uses a ton of memory. Also you can either get it integrated in IPython, but with zero interactivity, or in a separate window, with just very bare-bones support for plot rotation/translation/scale.

There are other tools you can use, but most are 2D only, some are very fast and 3D but more cumbersome to use and so on and so forth...

*Update: nowadays there are a few more libraries using WebGL, which are both fast and allow*[interactivity in IPython](https://ipywidgets.readthedocs.io/en/stable/examples/Using%20Interact.html)!
As a CAS I also expect Mathematica


Overall, I'll still be using Mathematica for many tasks, it's a great tool.


As a tool for numerical computation it fares better. Its main rival would be Matlab, whose strength really lies in the great

Even if the SciPy ecosystem is large with a good community, there are many areas where its packages are lacking, not well supported or immature.

[to be](http://www.walkingrandomly.com/?p=5387)[the best](https://www.wikivs.com/wiki/Maple_vs_Mathematica)[CAS in Python](https://github.com/sympy/sympy/wiki/SymPy-vs.-Mathematica)via[SymPy](http://sympy.org/en/index.html)/[Sage](http://www.sagemath.org/)/[Mathics](http://www.mathics.org/)but I don't rely too much on that, personally, so I'm not in a position to evaluate.Overall, I'll still be using Mathematica for many tasks, it's a great tool.

As a tool for numerical computation it fares better. Its main rival would be Matlab, whose strength really lies in the great

[toolboxes Mathworks](http://www.mathworks.com/products/)provides.Even if the SciPy ecosystem is large with a good community, there are many areas where its packages are lacking, not well supported or immature.

Sadly though for the most Matlab is not that popular because of the unique functionality it provides, but because MathWorks markets well to the academia and it became the language of choice for many researchers and courses.

Also, researchers don't care about redistributing source nearly as much as they really should, this day and age it's all still about printed publications...


So, is Matlab dead? Not even close, and to be honest, there





The usual argument is that it doesn't matter at all, because these are scripting languages used to glue very high-performance numerical routines. And I would totally agree. If it didn't matter.

A language for exploratory programming has to be expressive and high-level, but also fast enough for the abstractions not to fall on their knees. Sadly, Python isn't.


Even with simple code, if you're processing a modicum amount of data, you'll need to know its internals, and the variety of options available for optimization. It's similar in this regard to Mathematica, where using functions like Compile often requires planning the code up-front to fit in the restrictions of such optimizers.


Empirically though it seems that the amount of time I had to spend minding performance patterns in Python is even higher than what I do in Mathematica. I suspect it's because many packages are pure python.


It's true that you can do all the optimization staying inside the interactive environment, not needing to change languages. That's not bad. But if you start having to spend a significant amount of time thinking about performance, instead of transforming data, it's a problem.


Also, it's a mystery to me why most scientific languages are not built for multithreading, at all. All of them, Python, Matlab and Mathematica, execute only


Even


Multiprocessing in Python is great, IPython makes it a breeze to configure a cluster of machines or even many processes on a local machine. But it still requires order of magnitudes more effort than threading, killing interactivity (push global objects, imports, functions, all manually across instances).


Mathematica at least does the





Also, researchers don't care about redistributing source nearly as much as they really should, this day and age it's all still about printed publications...

So, is Matlab dead? Not even close, and to be honest, there

[are many issues](http://fperez.org/py4science/warts.html)Python has to solve. Overall though,[things are shifting](http://mathesaurus.sourceforge.net/)already, and I really can't see a bright future for Matlab or its clones, as fundamentally Python is a[much better language](http://www.stat.washington.edu/~hoytak/blog/whypython.html), and for research being open is probably the most important feature. We'll see.**A note on performance and exploration****For some reason, most of the languages for scientific exploratory programming are**

[really](http://arxiv.org/abs/1306.6047)[slow](http://benchmarksgame.alioth.debian.org/u32/benchmark.php?test=all&lang=lua&lang2=python3&data=u32). Python, Matlab, Mathematica, they are all fairly slow languages.The usual argument is that it doesn't matter at all, because these are scripting languages used to glue very high-performance numerical routines. And I would totally agree. If it didn't matter.

A language for exploratory programming has to be expressive and high-level, but also fast enough for the abstractions not to fall on their knees. Sadly, Python isn't.

Even with simple code, if you're processing a modicum amount of data, you'll need to know its internals, and the variety of options available for optimization. It's similar in this regard to Mathematica, where using functions like Compile often requires planning the code up-front to fit in the restrictions of such optimizers.

Empirically though it seems that the amount of time I had to spend minding performance patterns in Python is even higher than what I do in Mathematica. I suspect it's because many packages are pure python.

It's true that you can do all the optimization staying inside the interactive environment, not needing to change languages. That's not bad. But if you start having to spend a significant amount of time thinking about performance, instead of transforming data, it's a problem.

Also, it's a mystery to me why most scientific languages are not built for multithreading, at all. All of them, Python, Matlab and Mathematica, execute only

[some underlying C code](http://www.mathworks.com/discovery/matlab-multicore.html)in parallel (e.g. blas routines). But not anything else (all the routines not written in native code, often things such as plots, optimizers, integrators).Even

[Julia](http://julialang.org/), which was built specifically for performance, doesn't really do multithreading so far, just "green" threads (one at a time, like python) and multiprocessing.Multiprocessing in Python is great, IPython makes it a breeze to configure a cluster of machines or even many processes on a local machine. But it still requires order of magnitudes more effort than threading, killing interactivity (push global objects, imports, functions, all manually across instances).

Mathematica at least does the

[multiprocessing data distribution automatically](http://reference.wolfram.com/language/guide/ParallelComputing.html), detecting dependencies and input data that need to be transferred.**Learn by example:**


**Other resources:**Tutorials

**A Crash Course in Python for Scientists****Scientific Python Lectures****A gallery of interesting IPython notebooks**[Performance Python for Numerical Algorithms](https://ep2014.europython.eu/en/schedule/sessions/64/)- Anaconda's
(also, remember to conda clean unused packages...)**Conda package manager** [Learn about division and future division](http://bfroehle.com/2012/01/06/true-division-in-ipython/)[Numpy performance tricks](https://ipython-books.github.io/45-understanding-the-internals-of-numpy-to-avoid-unnecessary-array-copying/)[General Python performance tricks](https://wiki.python.org/moin/PythonSpeed/PerformanceTips)[Parallel Computing with IPython](http://www.astro.washington.edu/users/vanderplas/Astr599/notebooks/21_IPythonParallel)[Interactivity with IPython](http://nbviewer.ipython.org/github/ipython/ipython/blob/2.x/examples/Interactive%20Widgets/Index.ipynb)

Packages

**Scipy: numpy, scipy, matplotlib, sympy, pandas**- Optimization and learning
, one of**Scikit-Learn**[SciKit](https://scikits.appspot.com/about)packages (scipy extensions)[GPy](https://gpy.readthedocs.org/en/latest/), Gaussian processes.[Scikit-Monaco](http://scikit-monaco.readthedocs.org/en/latest/), Monte Carlo integrators[Cvxopt](http://cvxopt.org/userguide/index.html)/cvxpy, convex optimization[NLopt](http://ab-initio.mit.edu/wiki/index.php/NLopt), more nonlinear optimizers[PyOpt](http://www.pyopt.org/reference/optimizers.html), even more optimizers[DEAP](https://code.google.com/p/deap/), evolutionary algorithms, a package that can serialize/snapshot a python kernel. Useful when one wants to stop working on an iPython session but want to be able to pick it up again from the same state next time.[Dill](https://pypi.org/project/dill/)- Performance
[A comparison](https://www.ibm.com/developerworks/community/blogs/jfp/entry/How_To_Compute_Mandelbrodt_Set_Quickly?lang=en)of Cython, Numba, PyCuda, PyOpenCl, NumPy and other frameworks on a simple problem (Mandelbrot set). Deprecated. Try Cython instead., inlines C code in Python code, compiles and links to python on demand**SciPy Weave**, a numpy "aware" compiler, targets LLVM, compiles in runtime (annotated functions)**Numba**, compiles annotated python to C.**Cython**[Bottleneck](https://github.com/pydata/bottleneck)uses it to accelerate some NumPy functions. (see also[Shedskin](https://github.com/shedskin/shedskin),[Pythran](https://github.com/serge-sans-paille/pythran)and[ocl](https://github.com/mdipierro/ocl))[JobLib](http://pythonhosted.org/joblib/parallel.html#common-usage), makes multiprocessing easier (see[IPython.Parallel](http://ipython.parallel/)too) but still not great as you can't have multithreading, multiprocessing means you'll have to send data around independent python interpreters :/[NumExpr](https://github.com/pydata/numexpr), a fast interpreter of numerical expressions on arrays. Faster than numpy by aggregating operations (instead of doing one at at time)[WeldNumpy](https://www.weld.rs/weldnumpy/)is another faster interpreter, the idea here is to lazy-evaluate expressions to be able to execute them more optimally.[Theano](http://deeplearning.net/software/theano/), targets cpu and gpu, numpy aware, automatic differentiation. Clumsy...[Nuikta](http://nuitka.net/pages/documentation.html), offline compiles python to C++, should support all extensions[PyPy](http://pypy.org/), a JIT, with a tracing interpreter written in python. Doesn't support all extensions (the CPython C library interface)[Python/Cuda](https://developer.nvidia.com/how-to-cuda-python)links- Non-homogeneous data
- Graphics/Plotting
**For 3d animations,**[VisVis](http://code.google.com/p/visvis/)**seems the only tool that is capable of achieving decent speed, quality, and has a good interface and support.**It has a matlab-like interface, but actually creating objects (Line() instead of plot...) is much better/faster.*Update: Its successor is*[VisPy](http://vispy.org/index.html), at the time I first wrote this, it was still experimental. I have not tried it yet, but it seems better now.*Update:*[Ipyvolume](https://github.com/maartenbreddels/ipyvolume)seems viable too., nice plotting library, 2d only, outputs HTML5/JS so it can be interacted with in**Bokeh**[IPython Notebook](http://nbviewer.ipython.org/github/ContinuumIO/bokeh-notebooks/blob/master/index.ipynb). Somewhat lower-level than Matplotlib, albeit it does provide a bunch of plotting functions[Chaco](https://docs.enthought.com/chaco/)is another 2d plot/gui library, very OO, similar to Bokeh it might require more code to create a graph- Matplotlib toolkits (MPL is SLOW and rather ugly, but it's the most supported):
, quite crappy 3d plots**Mplot3d**, good looking 2d plots[Seaborn](http://web.stanford.edu/~mwaskom/software/seaborn/)[mpld3](http://mpld3.github.io/), a matplotlib compatible library that emits HTML5/JS using d3.jsis nifty, and[NodeBox OpenGL](http://www.cityinabottle.org/nodebox/)[DrawBot](https://www.drawbot.com/)is very similar too (but OSX only at the moment). They actually derive from the same base sourcecode.and[Point Cloud Library](http://strawlab.github.io/python-pcl/)[PyGTS](http://pygts.sourceforge.net/), Gnu Triangulated Surface Library- Others:
[Mayavi](http://docs.enthought.com/mayavi/mayavi/)/Tvtk,[3d](http://code.enthought.com/projects/mayavi/m2_tutorial_scipy10.pdf)[visualizations](http://docs.enthought.com/mayavi/mayavi/mlab.html). Usable, but finicky and old (and tends to crash).*Note:*

# mayavi and wxpython, use from command line binstar search -t conda mayavi

%gui wx

%pylab wx

%matplotlib inline

# In Ipython Notebook %matplotlib has to come after pylab, it seems.





# "inline" is cool but "qt" and "wx" allows interactivity

# qt is faster than wx, but mayavi requires wx

## No comments:

Post a Comment