---
title: Pyodide Spin Out and 0.17 Release – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2021/04/pyodide-spin-out-and-0-17-release/
author: Teon Brooks
published: '2021-04-22'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

We are happy to announce that Pyodide has become an independent and community-driven project. We are also pleased to announce the 0.17 release for Pyodide with many new features and improvements.

Pyodide consists of the CPython 3.8 interpreter compiled to WebAssembly which allows Python to run in the browser. Many popular scientific Python packages have also been compiled and made available. In addition, Pyodide can install any Python package with a pure Python wheel from the Python Package Index (PyPi). Pyodide also includes a comprehensive foreign function interface which exposes the ecosystem of Python packages to Javascript and the browser user interface, including the DOM, to Python.

You can try out the latest version of Pyodide in a [REPL](https://pyodide.org/en/0.17.0/console.html) directly in your browser.

## Pyodide is now an independent project

We are happy to announce that Pyodide now has a new home in a separate GitHub organisation ([github.com/pyodide](https://github.com/pyodide)) and is maintained by a volunteer team of contributors. The project documentation is available on [pyodide.org](https://pyodide.org).

Pyodide was originally developed inside Mozilla to allow the use of Python in [Iodide](https://hacks.mozilla.org/2019/03/iodide-an-experimental-tool-for-scientific-communicatiodide-for-scientific-communication-exploration-on-the-web/), an experimental effort to build an interactive scientific computing environment for the web. Since [its initial release and announcement](https://hacks.mozilla.org/2019/04/pyodide-bringing-the-scientific-python-stack-to-the-browser/), Pyodide has attracted a large amount of interest from the community, remains actively developed, and is used in many projects outside of Mozilla.

The core team has approved a transparent [governance document ](https://pyodide.org/en/0.17.0/project/governance.html) and has a [roadmap for future developments](https://pyodide.org/en/0.17.0/project/roadmap.html). Pyodide also has a[ Code of Conduct](https://pyodide.org/en/0.17.0/project/code-of-conduct.html#code-of-conduct) which we expect all contributors and core members to adhere to.

New contributors are welcome to participate in the project development on Github. There are many ways to contribute, including code contributions, documentation improvements, adding packages, and using Pyodide for your applications and providing feedback.

## The Pyodide 0.17 release

Pyodide 0.17.0 is a major step forward from previous versions. It includes:

- major maintenance improvements,
- a thorough redesign of the central APIs, and
- careful elimination of error leaks and memory leaks

### Type translation improvements

The type translations module was significantly reworked in v0.17 with the goal that round trip translations of objects between Python and Javascript produces an identical object.

In other words, Python -> JS -> Python translation and JS -> Python -> JS translation now produce objects that are equal to the original object. (A couple of exceptions to this remain due to unavoidable design tradeoffs.)

One of Pyodide’s strengths is the foreign function interface between Python and Javascript, which at its best can practically erase the mental overhead of working with two different languages. All I/O must pass through the usual web APIs, so in order for Python code to take advantage of the browser’s strengths , we need to be able to support use cases like generating image data in Python and rendering the data to an HTML5 Canvas, or implementing event handlers in Python.

In the past we found that one of the major pain points in using Pyodide occurs when an object makes a round trip from Python to Javascript and back to Python and comes back different. This violated the expectations of the user and forced inelegant workarounds.

The issues with round trip translations were primarily caused by implicit conversion of Python types to Javascript. The implicit conversions were intended to be convenient, but the system was inflexible and surprising to users. We still implicitly convert strings, numbers, booleans, and None. Most other objects are shared between languages using proxies that allow methods and some operations to be called on the object from the other language. The proxies can be converted to native types with new explicit converter methods called `.toJs`

and `to_py`

.

For instance, given an Array in JavaScript,

```
window.x = ["a", "b", "c"];
```


We can access it in Python as,

>>> from js import x # import x from global Javascript scope >>> type(x) <class 'JsProxy'> >>> x[0] # can index x directly 'a' >>> x[1] = 'c' # modify x >>> x.to_py() # convert x to a Python list ['a', 'c']

Several other conversion methods have been added for more complicated use cases. This gives the user much finer control over type conversions than was previously possible.

For example, suppose we have a Python list and want to use it as an argument to a Javascript function that expects an Array. Either the caller or the callee needs to take care of the conversion. This allows us to directly call functions that are unaware of Pyodide.

Here is an example of calling a Javascript function from Python with argument conversion on the Python side:

```
function jsfunc(array) {
array.push(2);
return array.length;
}
pyodide.runPython(`
from js import jsfunc
from pyodide import to_js
def pyfunc():
mylist = [1,2,3]
jslist = to_js(mylist)
return jsfunc(jslist) # returns 4
`)
```


This would work well in the case that `jsfunc`

is a Javascript built-in and `pyfunc`

is part of our codebase. If `pyfunc`

is part of a Python package, we can handle the conversion in Javascript instead:

```
function jsfunc(pylist) {
let array = pylist.toJs();
array.push(2);
return array.length;
}
```


See the [type translation documentation](https://pyodide.org/en/0.17.0/usage/type-conversions.html) for more information.

### Asyncio support

Another major new feature is the implementation of a Python event loop that schedules coroutines to run on the browser event loop. This makes it possible to use asyncio in Pyodide.

Additionally, it is now possible to await Javascript Promises in Python and to await Python awaitables in Javascript. This allows for seamless interoperability between asyncio in Python and Javascript (though memory management issues may arise in complex use cases).

Here is an example where we define a Python async function that awaits the Javascript async function “fetch” and then we await the Python async function from Javascript.

```
pyodide.runPython(`
async def test():
from js import fetch
# Fetch the Pyodide packages list
r = await fetch("packages.json")
data = await r.json()
# return all available packages
return data.dependencies.object_keys()
`);
let test = pyodide.globals.get("test");
// we can await the test() coroutine from Javascript
result = await test();
console.log(result);
// logs ["asciitree", "parso", "scikit-learn", ...]
```


### Error Handling

Errors can now be thrown in Python and caught in Javascript or thrown in Javascript and caught in Python. Support for this is integrated at the lowest level, so calls between Javascript and C functions behave as expected. The error translation code is generated by C macros which makes implementing and debugging new logic dramatically simpler.

For example:

```
function jserror() {
throw new Error("ooops!");
}
pyodide.runPython(`
from js import jserror
from pyodide import JsException
try:
jserror()
except JsException as e:
print(str(e)) # prints "TypeError: ooops!"
`);
```


### Emscripten update

Pyodide uses the [Emscripten](https://emscripten.org/) compiler toolchain to compile the CPython 3.8 interpreter and Python packages with C extensions to WebAssembly. In this release we finally completed the migration to the latest version of Emscripten that uses the upstream LLVM backend. This allows us to take advantage of recent improvements to the toolchain, including significant reductions in package size and execution time.

For instance, the SciPy package shrank dramatically from 92 MB to 15 MB so Scipy is now cached by browsers. This greatly improves the usability of scientific Python packages that depend on scipy, such as scikit-image and scikit-learn. The size of the base Pyodide environment with only the CPython standard library shrank from 8.1 MB to 6.4 MB.

On the performance side, the latest toolchain comes with a 25% to 30% run time improvement:

![](../../assets/7270c95c7e75c427.png)


Performance ranges between near native to up to 3 to 5 times slower, depending on the benchmark. The above benchmarks were created with Firefox 87.

### Other changes

Other notable features include:

- Fixed package loading for Safari v14+ and other Webkit-based browsers
- Added support for relative URLs in micropip and loadPackage, and improved interaction between micropip and loadPackage
- Support for implementing Python modules in Javascript

We also did a large amount of maintenance work and code quality improvements:

- Lots of bug fixes
- Upstreamed a number of patches to the emscripten compiler toolchain
- Added systematic error handling to the C code, including automatic adaptors between Javascript errors and CPython errors
- Added internal consistency checks to detect memory leaks, detect fatal errors, and improve ease of debugging

See [the changelog](https://pyodide.org/en/0.17.0/project/changelog.html#version-0-17-0) for more details.

## Winding down Iodide

Mozilla has made the difficult decision to wind down the Iodide project. While [alpha.iodide.io](https://alpha.iodide.io) will continue to be available for now (in part to provide a demonstration of Pyodide’s capabilities), we do not recommend using it for important work as it may shut down in the future. Since iodide’s release, there have been [many efforts](https://pyodide.org/en/0.17.0/project/related-projects.html#notebook-environements-ides-repls) at creating interactive notebook environments based on Pyodide which are in active development and offer a similar environment for creating interactive visualizations in the browser using python.

## Next steps for Pyodide

While many issues were addressed in this release, a number of other major steps remain on the roadmap. We can mention

- Reducing download sizes and initialization times
- Improve performance of Python code in Pyodide
- Simplification of package loading system
- Update scipy to a more recent version
- Better project sustainability, for instance, by seeking synergies with the conda-forge project and its tooling.
- Better support for web workers
- Better support for synchronous IO (popular for programming education)

For additional information see the [project roadmap](https://pyodide.org/en/latest/project/roadmap.html).

## Acknowledgements

Lots of thanks to:

[Dexter Chua](https://github.com/dalcde)and[Joe Marshall](https://github.com/joemarshall)for improving the build setup and making Emscripten migration possible.[Hood Chatham](https://github.com/hoodmane)for in-depth improvement of the type translation module and adding asyncio support- and
[Romain Casati](https://github.com/casatir)for improving the Pyodide REPL console.

We are also grateful to all [Pyodide contributors](https://github.com/pyodide/pyodide/graphs/contributors).

## About Roman Yurchak

Data Scientist and Founder at Symerio

## About Hood Chatham

NSF Postdoc at UCLA working in algebraic topology

## About
[
Teon Brooks ](https://teonbrooks.com)

Public-interest technologist. Product Manager at Mozilla. Executive Director at Computation in Education Labs.

## About
[
Will Lachance ](https://wrla.ch)

Data Engineering @ Mozilla