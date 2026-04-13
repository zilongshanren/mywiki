---
title: Automated testing on my latest research project
url: https://anteru.net/blog/2010/automated-testing-on-my-latest-research-project
published: '2010-11-01'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

During the last months, I implemented lots of different graphics algorithms with many settings. One core theme that appeared throughout this project was testing: Both how to prevent regressions, as well as how to build a framework that new algorithms can be added quickly to it and compared against others. Of all that of course without excessive programming effort :)

## Automation

Pretty early on in the project I decided to have all testing be fully automated. That is, with one single command line I wanted to be able to re-run all tests and get a quick yes/no overview which showed me if there are any regressions. Looking at my [previous post-mortem](https://anteru.net/blog/2009/10/19/621/), I started by adding [Lua](http://lua.org) into the UI to make it scriptable. Via the Lua script interface, I could run the application, move to any position, save every buffer and change the settings. This interface was very thin and most Lua-scripts where only a few lines long. What turned out to be pretty useful is to be able to pass command-line options into the Lua environment, so I could run for instance `app Width=1920 Height=1080 Fast`

and read those variables from the Lua script.

Adding Lua to the application turned out to be very straightforward. Most of the calls went from Lua to the application, so there was no object sharing or so which would make stuff complicated. However, I occasionally called back to Lua for filters (for instance, I had a mode to store the image in tiles and this called back into Lua so I could select the interesting tiles from script.)

However, while Lua is very easy to use, I had more complex requirements for the testing:

- Needed to run lots of tests as fast as possible. The machine has multiple cores, so parallelisation was crucial to cut down test times.
- Compression: The tests would generate large amounts of data – a full test run could easily produce 20 GiB of raw files. These files compressed all pretty well, so I had to get some compression either into the app or into the test framework.
- Easy-to-browse output: Ideally some HTML file or so where I can quickly find the results.
- Diff reports: Did the latest changes improve the algorithm, or did it regress?

I’m pretty sure of all this can be coded up with Lua, but it’ll require lots of searching around for libraries and documentation. As this was research, and time was critical, I opted instead for [Python](http://python.org) (3.1).

## Test infrastructure

The final infrastructure I came up with looked like this:

- A bunch of very low-level Lua scripts to perform animations and the rendering itself. All output images would be stored directly to disk.
- Python would call the Lua-scripts with different settings as needed. Comparing the images to the reference was done via
[pdiff](http://pdiff.sourceforge.net/)and[ImageMagick](http://www.imagemagick.org/). Other operations used a custom tool which was driven by command line and[JSON](http://json.org)setting files. - Python would then pack all resulting images into a .zip file and pickle the results into it as well. Pickle turned out to be all I needed here; I wrote a small tool to quickly investigate the contents of any given test pack file for debugging. The pack files were versioned, so I never had issues with loading wrong stuff – in that case, the pack was simply regenerated (always remember to store all settings necessary for that inside the pack :))
- A final Python script merged results together and produced nice HTML output using my custom template engine (Miranda, closely modeled after
[Google’s CTemplate](http://code.google.com/p/google-ctemplate/)engine but written in Python.)

The last merging step turned out to be crucial. During development, I often wound up tweaking one particular algorithm, but I still wanted the complete comparison. Of course, this required some kind of “delta” packaging which I did via merging. The script loaded both results, and tried to unify them. If a previous entry was already existing, it would create a diff (i.e. new algorithm version is better/worse than before.) If no previous entry existed, it would just copy. This gave me very fast turnaround times and didn’t require any changes to the on-disc storage format.

Small note on the JSON parsing: Due to lack of time, I used [boost::property_tree](http://boost.org/doc/libs/release/property_tree). It’s ok for reading JSON, but the JSON it generates looses all type information. Next time I’ll be likely using a full-blown JSON parser to have “loss-less” JSON transformation.

## Performance tuning

While this framework was all nice, the performance was not that great at first so I opted for a few optimisations. First of all, I made extensive use of Python’s multiprocessing module to run all tests in parallel. This already provided a huge benefit, as I could overlay very compute intense parts (pdiff in particular) with lots of I/O.

The second, not-so-obvious optimisation was to overwrite files all the time. In particular, for ImageMagick, most operations where compare *A* to *B* and save to *C*. At first, I always used different file names for *C* before packing them. It turned out that overwriting *C* all the time was much faster. I suspect that Windows flushes file creation to disk, which totally makes sense – but I was surprised to see how much faster it became once I just overwrote the same file. Side note: As I used multi-processing, I had of course one file per process.

## Caveats

Some warnings: If you use Python’s multiprocessing, always remember to use

```
if __name__=='__main__':
doTheFork()
```


Otherwise you have a fork-bomb which will immediately freeze your system. The multiprocessing error handling is not that great either. In particular, you should avoid throwing exceptions and instead just pass around some result which indicates an error, and do the error handling in the host process.

Python’s zip module is pretty decent, but there’s not streaming reads from it. This turned out to be pretty bad at first as I stored PPM images (huge!) which I wanted to stream out of the archive directly instead of storing them on disk. I later switched to PNGs, which were easier to manage. It was still beneficial to pack the files into a single .zip, once because of less clutter with hundreds of test-files and second because I could version complete packs.

Next week, we’ll take a look at the animation backend – old-school command-line magic for producing nice-looking videos.