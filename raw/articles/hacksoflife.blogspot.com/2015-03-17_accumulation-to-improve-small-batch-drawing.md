---
title: Accumulation to Improve Small-Batch Drawing
url: http://hacksoflife.blogspot.com/2015/03/accumulation-to-improve-small-batch.html
author: Benjamin Supnik
published: '2015-03-17'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

I sometimes see "casual" OpenGL ES developers (e.g. users making 2-d games and other less performance intensive GL applications) hit a performance wall on the CPU side. It starts with the app having something like this:



The results are correct drawing - and truly awful performance.






```
````class gl_helper {`

void draw_colored_triangle_2d(color_t color, int x1, int y1,

int x2, int y2, int x3, int y3);

void draw_textured_triangle_2d(color_t color,

int x1, int y1, int x2, int y2,

int x3, int y3,

int tex_x, int tex_y, int tex_width, int tex_height);

void draw_textured_triangle_3d(color_t color,

int x1, int y1, int z1, int x2, int y2, int z2,

int x3, int y3, int z3, int tex_x,

int tex_y, int tex_width, int tex_height);

};


You get the idea. OpenGL ES is "tamed" by making simple functions that do what we want - one primitive at a time.The results are correct drawing - and truly awful performance.

### Why This Is Slow

Why is the above code almost guaranteed to produce slow results when implemented naively? The answer is that 3-d graphics hardware has a high CPU cost to set the GPU up to draw and a very low cost per triangle once you do draw. So creating an API where each triangle comes in differently and thus must be individually set up maximizes the overhead and minimizes throughput.

A profile of this kind of code will show a ton of time in the actual draw call (e.g. glDrawArrays) but don't be fooled. The time is really being spent at the beginning of glDrawArrays synchronizing the GPU with the type of drawing you want.*

### Cheaper By the Dozen

The Mike Acton way of fixing this is "where there's one, there's many" - this API should allow you to draw

*lots*of triangles, assuming they are all approximately the same. For example,```
````void draw_lots_of_colored_triangles(color_t color, int count, float xyz[]); `


would not be an insane API. At least if the number of triangles gets big, the overhead gets small.


One thing is clear: if your application can generate batched geometry, it absolutely should be sending it to OpenGL in bulk! You never want to run a for-loop over your big pile of triangles and send them one at a time; if you have a wrapper around OpenGL, make sure you can send the data in without chopping it up first!




The idea of accumulation is this: instead of actually drawing all of those individual triangles, you stash them in memory. You do so in a format that makes it reasonably quick to both:




The accumulator also gives you a place to collect statistics about your application's usage of OpenGL. If your app is alternating colored and textured triangles, you're going to have to change shaders (even in the accumulator) and it will still be slow. But you can record statistics in debug mode about the size of the draws to detect this kind of "inefficient ordering."


Similarly, the accumulator can eliminate some calls to the driver to setup state because it




(Maybe your level's building block consists of a textured square background with an additively blended square on top, and this means two triangles of background, state change, two triangle of background, state change again.)


I am assuming that you have already combined your images into a few large textures (texture atlasing) and that you don't have a million tiny textures floating around. If you haven't atlased your textures, go do it now; I'll wait.



Okay welcome back. When your drawing batch size is











The point of the above paragraph is: measure carefully first, then merge state second; merging state can be a win or a loss, and it's very dependent on the particular model you're drawing.



One thing is clear: if your application can generate batched geometry, it absolutely should be sending it to OpenGL in bulk! You never want to run a for-loop over your big pile of triangles and send them one at a time; if you have a wrapper around OpenGL, make sure you can send the data in without chopping it up first!

### When You Can't Consolidate

Unfortunately there are times when you can't actually draw a ton of triangles all at once. It's cute of me to go "oh, performance is easy - just go rewrite all of your drawing code", but this is time consuming and in some cases the app structure itself might make this hard. If you can't design for bulk performance, there is a second option: accumulation.The idea of accumulation is this: instead of actually drawing all of those individual triangles, you stash them in memory. You do so in a format that makes it reasonably quick to both:

- Save the triangles (so you don't waste time saving and)
- Send them all to OpenGL at once.

*one*state setup (for non-textured triangles) and then a single 200-triangle draw call. This is about 200x more efficient than the naive code.The accumulator also gives you a place to collect statistics about your application's usage of OpenGL. If your app is alternating colored and textured triangles, you're going to have to change shaders (even in the accumulator) and it will still be slow. But you can record statistics in debug mode about the size of the draws to detect this kind of "inefficient ordering."

Similarly, the accumulator can eliminate some calls to the driver to setup state because it

*knows*what it was last doing. The accumulator does all of its drawing in one shot; if you draw two textured triangles with different textures, the accumulator must stop to change textures (not so good), but it can go "hey, another textured triangle, same pixel shader" and avoid changing pixel shaders (a big win).### Dealing With Inefficient Ordering

So now you have an accumulator, it submits the biggest possible batches of the same kinds of triangles, and it makes the minimum state change calls when the drawing type changes. And it's*still*slow. When you look at your usage stats, you find the average draw call size is still only two triangles because the client code is alternating between drawing modes all of the time.(Maybe your level's building block consists of a textured square background with an additively blended square on top, and this means two triangles of background, state change, two triangle of background, state change again.)

I am assuming that you have already combined your images into a few large textures (texture atlasing) and that you don't have a million tiny textures floating around. If you haven't atlased your textures, go do it now; I'll wait.

Okay welcome back. When your drawing batch size is

*still*too small even after accumulation, you have two tools to get your batch size back up.### Draw Reordering

The first trick you can try (and you should try this one first) is to give your accumulator the freedom to

*reorder*drawing to achieve better performance.
In our example above, every square in the level had two draws, one on top of the other, and they weren't in the same OpenGL mode. What we can do is define each draw to be in a different layer, and let the accumulator draw all of layer 0 before any of layer 1.

Once we do that, we find that all of layer 0 is in one OpenGL state (big draw) and all of layer 1 is in the other. We've relaxed our ordering by giving the accumulator an idea of the real draw ordering we need, rather than the implicit one that comes from the order our code runs.

We actually had just this problem in X-Plane 10 Mobile's user interface; virtually every element was a textured draw of a background element (which uses a simple texturing shader) followed by a draw of text (which uses a special font shader that applies coloring from a two-channel texture).

The result was two shader changes per UI element, and the performance was awful.

We simply modified our accumulator to draw all text after all UI elements; there's a simple "barrier" that can be placed to force stored up text to be output before proceeding (to get major layering of the UI right) but most windows can draw all of their UI elements before any text, cutting down the number of shader changes to two changes total - a big win!

### Merging OpenGL State

If you absolutely have to have the draw order you have (maybe there's alpha blending going on) the other lever you can pull is to find ways to make disparate OpenGL calls use more similar drawing state. (This is what texture atlasing does.) A few tricks:- Use a very small solid white texture for non-textured geometry - you can now use your texturing shader at all times.
- You don't need to get rid of color application in a shader - simply set the color to white opaque.
- If you use pre-multiplied alpha, you can draw both additive and non-additive alpha from the same state by varying how you prepare your art assets. Opaque assets can be run with the blender on.

The point of the above paragraph is: measure carefully first, then merge state second; merging state can be a win or a loss, and it's very dependent on the particular model you're drawing.

* Most drivers defer the work of changing the GPU's mode of drawing until you actually say draw. This way it can synchronize the

*net*result of all changing, instead of making a single change each time you call an API command. Since the gl calls you make don't fit the hardware very well, waiting until the driver can see all changes is a big win.
Ah yes... the Minecraftian "tessellator" approach. Sometimes, just sometimes, I wish I could go back to such simplicity... but then I remember that pointless complexity is why I get paid.

ReplyDelete