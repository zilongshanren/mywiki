---
title: Matplotlib slides
url: http://momentsingraphics.de/MatplotlibSlides.html
published: '2021-08-07'
source_blog: Moments in Graphics
source_site: http://momentsingraphics.de/
category: graphics
fetched: '2026-04-13'
---

# Matplotlib slides

I used to make my slides in [Powerpoint](https://products.office.com/en-us/powerpoint). For my presentations at [SIGGRAPH 2021](http://momentsingraphics.de/Siggraph2021.html) and [HPG 2021](http://momentsingraphics.de/HPG2021.html), I tried something different. The whole slide deck is one big interactive [matplotlib](https://matplotlib.org/) plot. Every bit is scripted in Python. They feature lots of animated and interactive plots. I am satisfied with how this experiment worked out. Lazily hacking together slides works better with Powerpoint but if you want a high-quality presentation with the best possible illustrations of mathematical concepts, this approach makes sense. This blog post provides some details about how I did it.

Alongside this blog post, I am publishing the Python source code of these slides and PDF versions. For the [HPG presentation](http://momentsingraphics.de/HPG2021.html) there is also a recording of the talk, for the [SIGGRAPH presentation](http://momentsingraphics.de/Siggraph2021.html) that will be available after the conference on August 14th. [Figure 1](http://momentsingraphics.de#MatplotlibSlideTeaser) shows an example slide from the SIGGRAPH presentation with animations and interactive elements.

## Motivation

[Python](https://www.python.org/) with the [SciPy stack](https://scipy.org/) is my answer to most problems. It is great how effortlessly it lets you accomplish many different tasks. In particular, [matplotlib](https://matplotlib.org/) has become my preferred tool for the creation of vector graphics. Naturally, it makes it easy to plot graphs. More abstractly, it gives you a way to draw lines, filled polygons, text, arrows, raster graphics and so forth. From these primitives, you can script together any figure you like, 2D or 3D. If you are curious how I do that, take a look at `generate_graphics.py`

in the code published with my [latest](http://momentsingraphics.de/Siggraph2021.html) [papers](http://momentsingraphics.de/HPG2021.html).

To get such figures into Powerpoint, I have to rasterize them at high resolution. Powerpoint supports vector graphics but last time I checked, this feature was unreliable and did antialiasing poorly. If I want a step-by-step animation, I export one raster image for each step. If I want a continuous animation, I create a video with a codec chosen carefully for Powerpoint. This process works but it is cumbersome. After changes to the plots, I have to manually update every embedded file in Powerpoint. Precise object placement in Powerpoint is also always a nuisance.

Recently, I realized that I hardly use Powerpoint for anything. I avoid fancy transitions, cluttered backgrounds or overly complicated layouts. My slides are really just raster graphics from matplotlib, screenshots and a few bits of text here and there. Sometimes I draw and animate simple shapes in Powerpoint but there are other ways to get that done. The amount of functionality that I would have to implement outside of Powerpoint to cover my needs is shockingly low. And since most of my figures come from matplotlib, it makes sense to put it at the center of things.

## Slideshow basics

The basic features for a slideshow were quite easy to get. I open a figure with a 1920×1080 client area and create axes without a frame that fill this figure. I chose to use x-coordinates from 0 to 16 and y-coordinates from 0 to 9 because it is easy to reason about that. I changed the default font to [Carlito](https://fontlibrary.org/en/font/carlito) which is an imitation of Microsoft's Calibri under a permissive license. Calibri is the default font of Powerpoint and I have gotten very used to it.

Using [ pyplot.text()](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.text.html?highlight=text#matplotlib.pyplot.text) I can draw text wherever I like. Making a function for bulleted lists or titles is trivial. When

[mathtext](https://matplotlib.org/stable/tutorials/text/mathtext.html)formulas are set to use Computer Modern as font, they look quite good. Sometimes, I placed white space manually, to make them look a bit better. With

[imageio](https://imageio.readthedocs.io/en/stable/),

[and](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.imshow.html)

`pyplot.imshow()`

[, I can draw raster graphics. Inset axes are also useful to place a plot anywhere on a slide.](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.inset_axes.html)

`inset_axes()`

To glue it all together, I use an object-oriented setup, which feels appropriate here. There are classes for presentations, slides and slideshows. Presentations are a list of slides with some layout data. A few methods should be overridden by derived classes. For example, I have a presentation with footer to show a logo and slide numbers. Slides override methods for drawing and to respond to user input. The method for drawing has access to a step index and can plot different elements accordingly (usually through if-statements). The slideshow grabs user input, advances the presentation when certain keys are pressed and invokes methods of the current slide as appropriate. Slides may have some persistent state. When the user changes an interactive slide, this change persists until the presentation ends. There are some specialized slides, e.g. one that displays a list of images. Clicking one of the images, places a magnifier at this location in all images.

PDF export is natively supported by matplotlib. I have a function that draws each slide and stores that plot to a PDF, resampling raster images at 1920×1080 resolution. Then I use [pdftk](https://www.pdflabs.com/tools/pdftk-the-pdf-toolkit/) or [Ghostscript](https://www.ghostscript.com/) to concatenate these PDFs into a single PDF. This function also supports exporting each step of an animation as separate page. Curiously enough, Powerpoint developers never got around to that.

## Real-time rendering with matplotlib

One of the main goals of this approach is to allow for animated and interactive plots. Doing that through videos in Powerpoint is dissatisfactory because it is difficult to sync up your presentation to the video. Besides, Powerpoint frequently fails at smooth video playback. With an interactive plot, you can make any change you like any time you like.

Getting smooth animations out of matplotlib is a bit challenging though. If you want to make things run fast with the SciPy stack, you should work with operations on complete arrays as much as possible. Loops are discouraged. That also helps here but matplotlib internals also take some time. It helps to plot many lines at once and to avoid updating parts of the figure that have not changed. For the most part, the functions that I wrote for static plots in the papers were already efficient enough. In a few spots, I optimized a bit more. It also helps to prepare as much as possible in the constructor of the slide object. This way, I got to frame rates between 10 and 30, which is not great but good enough. For some reason, all of this is much faster under Linux than under Windows.

To make animations, I have two mechanisms. Each slide can have multiple steps. Optionally, these steps have a duration for the transition. During that time, a slide attribute increases from zero to one at constant velocity. A callback of the slide gets invoked regularly through a timer. If a step transition is in progress, the slide uses this callback to redo drawing and takes the step interpolation attribute into account. Besides, I have callbacks for key presses, mouse clicks and mouse movement, which the slide can use to redraw parts.

The cool thing about that is how flexible it is. You can just tie any parameter of your plot to mouse movement to make things interactive. Sometimes, the orthographic camera can be rotated with the mouse, sometimes parts can be clicked to highlight certain aspects or to move around vertices of a polgyon. All these different interactive elements and animations can be defined with very little code and the overhead of exporting and importing stuff is gone.

## Embedding my renderer

Screenshots are nice but live demos are nicer. Since [my toy renderer](http://momentsingraphics.de/ToyRendererOverview.html) has such quick startup, I can easily embed it into the presentation. Upon being shown, certain slides spawn the renderer as subprocess. I have things set up such that the window opens up in the same spot on my screen. The renderer takes a few command line arguments so that it starts out showing the right experiment. Once the renderer terminates, the slide automatically advances.

## Recording presentations

For the virtual conferences, I had to record my presentations in advance. To do so, I used the open source software [OBS Studio](https://obsproject.com/). My experience with it has been pleasant. Setting it up to capture the relevant part of my screen and to overlay my presentation with a webcam image and my microphone input, only took a few minutes. It immediately produced videos with a high quality and encoded them to a reasonable size. In particular, noisy outputs of my renderer are looking good. However, that is accomplished using variable bit-rate encoding, which is not ideal for those who want to stream my video. Anyway, transcoding with [ffmpeg](https://ffmpeg.org/) is also easy.

## Conclusions

I spent a few days setting up the basics of this system and hardly changed them after that. Making the kind of slides that I wanted with Powerpoint, would have been very laborious and certain aspects of interactivity would have been impossible. As I created the slides, I felt productive and never thought that I am missing something from Powerpoint. And I'm happy with the end product. Overall, I would recommend this approach for polished presentations illustrating mathematical derivations. Certainly, similar things could be done with HTML 5 presentations using Javascript. [Immersive Math](http://immersivemath.com/ila/index.html) is a great example. Though, for me Python with matplotlib is more convenient since that's where I create all of my figures anyway.

If you're interested in creating slides the same way, you might find `slide_utlity.py`

useful. These 600 lines of Python code are my replacement for Powerpoint. The code is not specific to a particular slide deck. Like the code for the slides themselves, it's now licensed under [GPLv3](https://www.gnu.org/licenses/gpl-3.0.en.html).