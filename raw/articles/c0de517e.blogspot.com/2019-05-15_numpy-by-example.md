---
title: NumPy by Example
url: https://c0de517e.blogspot.com/2019/05/numpy-by-example.html
published: '2019-05-15'
source_blog: C0DE517E
source_site: https://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

*This originally was in my*

[Scientific Python 101](https://c0de517e.blogspot.com/2014/09/scientific-python-101.html)article, I've split it now as it was a long article and sometimes I need just to have a look at this code as a reminder of how things work.*If you're interested in a similar "by example" introduction for Mathematica,*

[check this other one out](http://c0de517e.blogspot.com/2013/10/wolframs-mathematica-101.html).Execute each section in an IPython cell (copy and paste, then shift-enter)

# Set-up the environment:

# First, we'll have to import NumPy and SciPy packages.

# First, we'll have to import NumPy and SciPy packages.

# IPython has "magics" (macros) to help common tasks like this:

%pylab

# This will avoid scientific notation when printing, see also %precision

np.set_printoptions(suppress = True)

# Optional: change the way division works:

#from __future__ import division

# 1/2 = 0.5 instead of integer division... problem is that then 2/2 would be float as well if we enable this, so, beware.

#from __future__ import division

# 1/2 = 0.5 instead of integer division... problem is that then 2/2 would be float as well if we enable this, so, beware.

# In IPython notebook, cell execution is shift-enter

# In IPython-QT enter evaluates and control-enter is used for multiline input

# Tab is used for completion, shift-tab after a function name shows its help

# Note that IPython will display the output of the LAST -expression- in a cell

# but variable assignments in Python are NOT expressions, so they will

# suppress output, unlike Matlab or Mathematica. You will need to add print

# statements after the assignments in the following examples to see the output

data = [[1,2],[3,4],[5,6]]

# if you want to suppress output in the rare cases it's generated, use ;

data; # try without the ; to see the difference

# There is a magic for help as well

%quickref



# Also, you can use ? and ?? for details on a symbol

get_ipython().magic(u'pinfo %pylab')

# In addition to the Python built-in functions help() and dir(symbol)

# Other important magics are: %reset, %reset_selective, %whos

# %prun (profile), %pdb (debug), %run, %edit

1*3 # evaluate this in a separate cell...

_*3 # ...now _ refers to the output of last evaluated cell

# again, not that useful because you can't refer to the previous expression

# evaluated inside a cell, just to the previous evaluation of an entire cell

# A numpy array can be created from a homogeneous list-like object

arr = np.array(data)

# Or an uninitialized one can be created by specifying its shape

arr = np.ndarray((3,3))

# There are also many other "constructors"

arr = np.identity(5)

arr = np.zeros((4,5))

arr = np.ones((4,))

arr = np.linspace(2,3) # see also arange and logspace

arr = np.random.random((4,4))

# Arrays can also be created from functions

arr = np.fromfunction((lambda x: x*x), shape = (10,))

# ...or by parsing a string

arr = np.fromstring('1, 2', dtype=int, sep=',')

# Arrays are assigned by reference

arr2 = arr

# To create a copy, use copy

arr2 = arr.copy()

# An array shape is a descriptor, it can be changed with no copy

arr = np.zeros((4,4))

arr = arr.reshape((2,8)) # returns the same data in a new view

# numpy also supports matrices, which are arrays contrained to be 2d

mat = np.asmatrix(arr)

# Not all operations avoid copies, flatten creates a copy

arr.flatten()

# While ravel doesn't

arr = np.zeros((4,4))

arr.ravel()

# By default numpy arrays are created in C order (row-major), but

# you can arrange them in fortran order as well on creation,
# or make a fortran-order copy of an existing array

arr = np.asfortranarray(arr)

# Data is always contiguously packed in memory

# Arrays can be indexed as with python lists/tuples

arr = np.zeros((4,4))

arr[0][0]

# Or with a multidimensional index

arr[0,0]

# Negative indices start from the end

arr[-1,-1] # same as arr[3,3] for this array

# Or, like matlab, via splicing of a range: start:end

arr = arange(10)

arr[1:3] # elements 1,2

arr[:3] # 0,1,2

arr[5:] # 5,6,7,8,9

arr[5:-1] # 5,6,7,8

arr[0:4:2] # step 2: 0,3

arr = arr.reshape(2,5)

arr[0,:] # first row

arr[:,0] # first column

# Also, splicing works on a list of indices (see also choose)

arr = arr.reshape(10)

arr[[1,3,5]]

# and with a numpy array of bools (see also where)

arr=np.array([1,2,3])

arr2=np.array([0,3,2])

arr[arr > arr2]

# flat returns an 1D-iterator

arr = arr.reshape(2,5)

arr.flat[3] # same as arr.reshape(arr.size)[3]

# Core operations on arrays are "ufunc"tions, element-wise

# vectorized operations

arr = arange(0,5)

arr2 = arange(5,10)

arr + arr2

# Operations on arrays of different shapes follow "broadcasting rules"

arr = np.array([[0,1],[2,3]]) # shape (2,2)

arr2 = np.array([1,1]) # shape (1,)

# If we do arr+arr2 arr2.ndim

# an input can be used if shape in all dimensions sizes, or if

# the dimensions that don't match have size 1 in its shape

arr + arr2 # arr2 added to each row of arr!

# Broadcasting also works for assignment:

arr[...] = arr2 # [[1,1],[1,1]] note the [...] to access all contents

arr2 = arr # without [...] we just say arr2 refers to the same object as arr

arr[1,:] = 0 # This now is [[1,1],[0,0]]

# flat can be used with broadcasting too

arr.flat = 3 # [[3,3],[3,3]]

arr.flat[[1,3]] = 2 # [[3,2],[2,3]]

# broadcast "previews" broadcasting results

np.broadcast(np.array([1,2]), np.array([[1,2],[3,4]])).shape

# It's possible to manually add ones in the shape using newaxis

# See also: expand_dims
print(arr[np.newaxis(),:,:].shape) # (1,2,2)

print(arr[:,np.newaxis(),:].shape) # (2,1,2)

# There are many ways to generate list of indices as well

arr = arange(5) # 0,1,2,3,4

arr[np.nonzero(arr)] += 2 # 0,3,4,5,6

arr = np.identity(3)

arr[np.diag_indices(3)] = 0 # diagonal elements, same as np.diag(arg.shape[0])

arr[np.tril_indices(3)] = 1 # lower triangle elements

arr[np.unravel_index(5,(3,3))] = 2 # returns an index given the flattened index and a shape

# Iteration over arrays can be done with for loops and indices

# Oterating over single elements is of course slower than native

# numpy operators. Prefer vector operations with splicing and masking

# Cython, Numba, Weave or Numexpr can be used when performance matters.

arr = np.arange(10)

for idx in range(arr.size):

print idx

# For multidimensiona arrays there are indices and iterators

arr = np.identity(3)

for idx in np.ndindex(arr.shape):

print arr[idx]

for idx, val in np.ndenumerate(arr):

print idx, val # assigning to val won't change arr

for val in arr.flat:

print val # assigning to val won't change arr

for val in np.nditer(arr):

print val # same as before

for val in np.nditer(arr, op_flags=['readwrite']):

val[...] += 1 # this changes arr

# Vector and Matrix multiplication are done with dot

arr = np.array([1,2,3])

arr2 = np.identity(3)

np.dot(arr2, arr)

# Or by using the matrix object, note that 1d vectors

# are interpreted as rows when "seen" by a matrix object

np.asmatrix(arr2) * np.asmatrix(arr).transpose()

# Comparisons are also element-wise and generate masks

arr2 = np.array([2,0,0])

print (arr2 > arr)

# Branching can be done checking predicates for any true or all true

if (arr2 > arr).any():

print "at least one greater"

# Mapping a function over an array should NOT be done w/comprehensions

arr = np.arange(5)

[x*2 for x in arr] # this will return a list, not an array

# Instead use apply_along_axis, axis 0 is rows

np.apply_along_axis((lambda x: x*2), 0, arr)

# apply_along_axis is equivalent to a python loop, for simple expressions like the above, it's much slower than broadcasting

# apply_along_axis is equivalent to a python loop, for simple expressions like the above, it's much slower than broadcasting

# It's also possible to vectorize python functions, but they won't execute faster

def test(x):

return x*2

testV = np.vectorize(test)

testV(arr)

# Scipy adds a wealth of numerical analysis functions, it's simple

# so I won't write about it.

# Matplotlib (replicates Matlab plotting) is worth having a quick look.

# IPython supports matplotlib integration and can display plots inline

%matplotlib inline

# Unfortunately if you chose the inline backend you will lose the ability

# of interacting with the plots (zooming, panning...)

# Use a separate backend like %matplotlib qt if interaction is needed

# Simple plots are simple

test = np.linspace(0, 2*pi)

plt.plot(test, np.sin(test)) # %pylab imports matplotib too

plt.show() # IPython will show automatically a plot in a cell, show() starts a new plot

plt.plot(test, np.cos(test)) # a separate plot

plt.plot(test, test) # this will be part of the cos plot

#plt.show()

# Multiple plots can also be done directly with a single plot statement

test = np.arange(0., 5., 0.1)

# Notes that ** is exponentiation.

# Styles in strings: red squares and blue triangles

plt.plot(test, test**2, 'rs', test, test**3, 'b^')

plt.show()

# It's also possible to do multiple plots in a grid with subplot

plt.subplot(211)

plt.plot(test, np.sin(test))

plt.subplot(212)

plt.plot(test, np.cos(test), 'r--')

#plt.show()

# Matplotlib plots use a hierarchy of objects you can edit to

# craft the final image. There are also global objects that are

# used if you don't specify any. This is the same as before

# using separate objects instead of the global ones

fig = plt.figure()

axes1 = fig.add_subplot(211)

plt.plot(test, np.sin(test), axes = axes1)

axes2 = fig.add_subplot(212)

plt.plot(test, np.cos(test), 'r--', axes = axes2)

#fig.show()

# All components that do rendering are called artists

# Figure and Axes are container artists

# Line2D, Rectangle, Text, AxesImage and so on are primitive artists

# Top-level commands like plot generate primitives to create a graphic

# Matplotlib is extensible via toolkits. Toolkits are very important.

# For example mplot3d is a toolkit that enables 3d drawing:

from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()

ax = fig.add_subplot(111, projection='3d')

points = np.random.random((100,3))

# note that scatter wants separate x,y,z arrays

ax.scatter(points[:,0], points[:,1], points[:,2])

#fig.show()

# Matplotlib is quite extensive (and ugly) and can do much more

# It can do animations, but it's very painful, by changing the

# data artists use after having generated them. Not advised.

# What I end up doing is to generate a sequence on PNG from

# matplotlib and play them in sequence. In general MPL is very slow.

# If you want to just plot functions, instead of discrete data,

# sympy plots are a usable alternative to manual sampling:

from sympy import symbols as sym

from sympy import plotting as splt

from sympy import sin

x = sym('x')

splt.plot(sin(x), (x, 0, 2*pi))

## No comments:

Post a Comment