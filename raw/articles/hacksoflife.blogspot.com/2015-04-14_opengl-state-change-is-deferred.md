---
title: OpenGL State Change Is Deferred
url: http://hacksoflife.blogspot.com/2015/04/opengl-state-change-is-deferred.html
author: Benjamin Supnik
published: '2015-04-14'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

This is totally obvious to developers who have been coding high performance OpenGL for years, but it might not be obvious to newer developers starting with OpenGL or OpenGL ES, so...


In pretty much any production OpenGL driver, the real 'work' of OpenGL state change is deferred - that work is executed on the next draw call (e.g. glDrawElements or glDrawArrays).


This is why, when you profile your code, glBindBuffer and glVertexPointer appear to be "really fast" and yet "glDrawArrays" is using a ton of CPU Time.


The work of setting up the hardware for GL state is deferred because often the state


Let's take as an example, vertex format. You do this:









In pretty much any production OpenGL driver, the real 'work' of OpenGL state change is deferred - that work is executed on the next draw call (e.g. glDrawElements or glDrawArrays).

This is why, when you profile your code, glBindBuffer and glVertexPointer appear to be "really fast" and yet "glDrawArrays" is using a ton of CPU Time.

The work of setting up the hardware for GL state is deferred because often the state

*cannot*be set up until multiple calls come in.Let's take as an example, vertex format. You do this:

```
``````
glBindBuffer(my_buffer);
```

glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 32, (char *) 0);

glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 32, (char *) 12);

glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 32, (char *) 24);


The way this is implemented on modern GPUs is to generate a subroutine or pre-amble code for your vertex shader that "executes" the vertex fetch based on these stride rules.

There's no point in generating the shader until

*all*of the vertex format is known; if the driver went and patched your shader after the first call (setting up attribute 0) using the old state of attributes 1 and 2, all of that work is wasted and would be redone when the next two glVertexAttribPointer calls come in.
Furthermore, the driver doesn't know when you're done. There is no glDoneScrewingAroundWithVertexAttribPointer call.

So the driver does the next best thing - it waits for a draw call. At that point it goes "hey, I

*know*you are done changing state because this draw call uses what you have set now." At that point it goes and makes any state change that is needed since the last draw call.
What this means is that you can't tell how "expensive" your state change is by profiling the code doing the state change. The cost of state change when you call it is the cost of recording for later what needs to be done, e.g.

```
``````
void glBlendFunc(GLenum sfactor, GLenum dfactor)
```

{

context * c = internal_get_thread_gl_context();

c->blend.sfactor = sfactor;

c->blend.dfactor = dfactor;

c->dirty_bits |= bit_blend_mode;

}


In other words, the driver is just going to record what you said to the current context and make a note that we're "out of sync" state-wise. The draw call does the heavy lifting:

```
``````
void glDrawArrays(GLenum mode, GLint first, GLsizei count)
```

{

context * c = internal_get_thread_gl_context();

if(c->dirty_bits & bit_blend_mode)

{

/* this is possibly slow */

sync_blend_mode_with_hardware(&c->blend);

}

/* more check and sync */

c->dirty_bits = 0;

/* do actual drawing work - this isn't too slow */

}


On Apple's OpenGL implementation, the stack is broken into multiple parts in multiple dylibs, which means an Instruments trace often shows you subroutines with semi-readable names; you can see draw calls updating and synchronizing state. On Windows the GL stack is monolithic, stripped, and often has no back-trace info, which makes it hard to tell where the CPU is spending time.

One final note: the GL driver isn't trying to save you from your own stupidity. If you do this:

```
``````
for(int i = 0; i < 1000; ++i)
```

{

glEnable(GL_BLEND);

glDrawArrays(GL_TRIANGLES, i*12, 12);

}


Then

*every*call to glEnable is likely to make the blend state 'dirty' and*every*call to glDrawArrays is going to spend time re-syncing blend state on the hardware.
Avoid calling state changes that aren't needed

*even*if they appear cheap in their individual function call time - they may be "dirtying" your context and driving up the cost of your draw calls.
## No comments:

## Post a Comment