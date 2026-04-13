---
title: 'NeHe Tutorials for CL-OpenGL :: nklein software'
url: http://nklein.com/2010/06/nehe-tutorials-for-cl-opengl/
author: Pat
published: '2010-06-01'
source_blog: nklein software
source_site: http://nklein.com
category: game programming
fetched: '2026-04-13'
---

The Neon Helium Productions (NeHe) online tutorials ([http://nehe.gamedev.net/](http://nehe.gamedev.net/)) are the best resources available for coders trying to learn specific OpenGL rendering techniques in C/C++. The CL-OpenGL library ([http://common-lisp.net/project/cl-opengl/](http://common-lisp.net/project/cl-opengl/)) is, to my mind, the most straightforward mapping of the OpenGL, GLU, and GLUT APIs into Common Lisp. In this series, I hope to combine the best of both so that the aspiring Lisp coder can quickly access these OpenGL techniques.

I am aware that someone else reworked the first six tutorials for CL-OpenGL. However, I can’t track those down any longer. The original website is gone. I am also aware that I won’t have a great deal of time for this sort of coding in the near future, but I hope to tackle a bunch of these this summer. Most of the tutorials are fairly short.

In this first tutorial, we’re going to generate a simple template file that opens an OpenGL window.

#<:use "glut-template.lisp">

Here is the resulting: [intro.lisp](http://nklein.com/wp-content/uploads/2010/06/intro.lisp).

To get started with CL-OpenGL, you will need a Lisp implementation that supports ASDF and CFFI, a git client, and OpenGL libraries. I will probably flesh this section out at some later date. For now, I am just barely going to touch on the prerequisites.

**Lisp implementation.**

**CFFI.**

**git client.**

**OpenGL libraries.** (Under Windows, you may need FreeGlut.dylib.)

Once you have all of the above, you will need to clone the CL-OpenGL repository so that you have the sources on your machine. The CL-OpenGL git repository is [http://github.com/3b/cl-opengl.git](http://github.com/3b/cl-opengl.git).

% cd /where/you/want/to/put/the/cl-opengl/sources

% git clone http://github.com/3b/cl-opengl.git

You need to ensure that the `cl-opengl/`

directory that you just created is included in your `asdf:*central-registry*`

list. For example, I have this in my `~/.sbclrc`

file

(dolist (subdir (list ;; ... some other packages ...

#P"cl-opengl/"))

(push (merge-pathnames subdir #P"/usr/local/asdf-install/site/")

asdf:*central-registry*))

Once you have CL-OpenGL installed, you’ll be able to use the following template.

#<:use "load opengl">

(defclass my-window (glut:window)

()

(:default-initargs :width 400 :height 300

:title "My Window Title"

:x 100 :y 100

:mode '(:double :rgb :depth)))

#<:use "initialization method">

#<:use "additional glut methods">

#<:use "create an instance of our window">

Usually, we’re going to load OpenGL, GLU, and GLUT.

(require :asdf) ; need ASDF to load other things

(asdf:load-system :cl-opengl) ; load OpenGL bindings

(asdf:load-system :cl-glu) ; load GLU bindings

(asdf:load-system :cl-glut) ; load GLUT bindings

Our initialization method can do anything we need to do in terms of loading textures or fonts or what-have-you. We could do some with the normal CLOS `initialize-object`

method if it is stuff we can do before OpenGL is initialized. For our purposes though, we need to wait until after OpenGL is ready but before our window is displayed so we make sure to go before the `glut:display-window`

call.

(defmethod glut:display-window :before ((win my-window))

#<:use "prepare opengl">

)

To prepare the default OpenGL environment that we’re going to use, we’re first going to turn on smooth shading. This allows colors to blend across our polygons. Later tutorials will go into more detail about smooth shading.

(gl:shade-model :smooth) ; enables smooth shading

The next line here sets the color used to clear the screen. OpenGL color values range from zero to one with zero being the darkest and one being the brightest. The parameters here are (in order) the red, green, blue, and alpha channels. The alpha channel doesn’t really come into play when clearing the screen, so it doesn’t much matter in this instance. We’re going to use a black background.

(gl:clear-color 0 0 0 0) ; background will be black

The next several lines prepare the depth buffer. OpenGL keeps a variety of buffers that are the same dimensions as your window. You were probably expecting the color buffer that stores the actual pixel values that are rendered on the screen. The depth can be used to keep track of the depth of the last item drawn to the screen or to prevent an object from drawing if it doesn’t have a depth thats less than the current value of the depth buffer for the current pixel.

(gl:clear-depth 1) ; clear buffer to maximum depth

(gl:enable :depth-test) ; enable depth testing

(gl:depth-func :lequal) ; okay to write pixel if its depth

; is less-than-or-equal to the

; depth currently written

We are also going to tell OpenGL that we’d like it to make things in perspective look as nice as possible.

; really nice perspective correction

(gl:hint :perspective-correction-hint :nicest)

Almost all applications will need at least a GLUT display function. Usually, they will do more than this, but this will get us started.

(defmethod glut:display ((win my-window))

(gl:clear :color-buffer-bit :depth-buffer-bit)

(gl:load-identity))

The following method gets called when your window is first created and any time your window is resized. We will use it to prepare our projection matrix.

(defmethod glut:reshape ((win my-window) width height)

#<:use "glut reshape -- prepare viewport">

#<:use "glut reshape -- prepare projection">

#<:use "glut reshape -- switch to model view">

)

To initialize the viewport, we simply take the given width and height and use them as the horizontal and vertical extents of our coordinate system.

(gl:viewport 0 0 width height) ; reset the current viewport

Next, we’re going to prepare the projection matrix. We’re going to set things up for a perspective view so that distant objects appear smaller than closer objects. We’re going to assume that the window accounts for a 45-degree field of view from left to right. We’re going to assume that objects in our scene can be anywhere from 1/10 to 100 units in front of our viewpoint.

First, we switch into the mode where matrix commands will change the projection matrix. Then, we make sure we’re starting from the identity matrix. Then, we prepare our perspective transformation assuming 45-degrees from left-to-right and a proportional amount from top-to-bottom (taking care not to divide by zero in the proportion).

(gl:matrix-mode :projection) ; select the projection matrix

(gl:load-identity) ; reset the matrix

;; set perspective based on window aspect ratio

(glu:perspective 45 (/ width (max height 1)) 1/10 100)

Once we are done setting up the projection matrix, we need to switch back to the model-view matrix so that further transforms will affect the space we’re viewing rather than where we are viewing things from.

(gl:matrix-mode :modelview) ; select the modelview matrix

(gl:load-identity) ; reset the matrix

To create and display an instance of our window, we simply go ahead and create and instance and pass it to `glut:display-window`

.

(glut:display-window (make-instance 'my-window))

Nice. You should turn this into a cl-glut tutorial and contribute it to cl-opengl. 🙂 It turns out, though, that NeHe’s tutorial are grossly outdated and don’t quite reflect modern OpenGL programming practices.

*nod* I know that OpenGL practices have moved forward quite a bit. I still think the NeHe tutorials are very good at the basics.

[…] the previous tutorial, we made a basic shell of a CL-OpenGL application. I have slightly modified it for this tutorial so […]

Nehe tutorials were always crap and full of misinformation and horrible code, but as luis said, today they are also outdated. Tutorials based on shaders are the way to go.

Also the # scheme is needlessly confusing and takes up space. I suggest you find another way to present your information.

Sure, the NeHe tutorials necessarily gloss over some things that an OpenGL guru would need to understand, but I’ve not found anything that felt was flat out wrong in any of the ones that I’ve read through so far. And, it’s true… much stuff is done with shaders today. Those don’t make an appearance in the NeHe tutorials until up around #47, I believe. But, I think there’s lots you need to get comfortable with in OpenGL before you start worrying about shaders.

I’ll revisit the

notation. Do you have a recommendation? Would something like this work better?;;;; glut reshape -- prepare viewport >>

;;;; glut reshape -- prepare projection >>

;;;; glut reshape -- switch to model view >>

)

And then later, something more like this?

glut reshape — prepare viewport >>I found the old NEHE examples. They are in the CL-SDL library under “\examples\nehe\”

I don’t understand the people who commented. I don’t understand their ungratefulness.

One thing is to note that the tutorial is outdated, but why insult the author? He has taken his personal time to write these tutorials if someone needed it.

And if it’s wrong, why don’t any one of you point out to a better tutorial or example?

And I didn’t find the tutorial useless. That’s how I’d write an OpenGL tutorial, albeit in C. He has explained simple things that a starter needs to understand.

This was super useful! The only trouble I’ve been having is I can’t figure out how to integrate it with SLIME. The process keeps running after I close the window down…

Indeed, OpenGL doesn’t get along too easily with REPL development. There were some strategies that I had when I developed Roto Mortar, but I can’t recall what they were.

I believe explicitly calling close-window ratger than closing the window by X-ing it at the OS level allowed better restarting. It also varied a bit on Mac OS X from release to release (of Mac OS X and of cl-opengl).

In case anyone else stumbles on this, it might be worth trying the following

http://roguebasin.roguelikedevelopment.org/index.php?title=Common_Lisp#Can_I_use_Curses_on_Lisp.3F

Also, you should consider doing a similar article for OpenGL 3+.

Thanks for great introductory tutorials!

How do you start this program in slime? Do you use load file (Ctrl-C, Ctrl-L) or what? I can not find a convenient way to compile it and run. Ctrl-C, Ctrl-K seams to not work because things like “(asdf:load-system :cl-opengl)” are not executed. Any advices?

I use Ctrl-C Ctrl-L when I want to load a whole file. For single forms, I use Ctrl-C Ctrl-C. I also make .asd files for anything bigger than one file so that I can I load the whole thing at once with ql:quickload or asdf:load-system.