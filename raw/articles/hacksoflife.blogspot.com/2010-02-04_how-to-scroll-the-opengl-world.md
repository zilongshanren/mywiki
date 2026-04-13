---
title: How To Scroll the OpenGL World
url: http://hacksoflife.blogspot.com/2010/02/how-to-scroll-opengl-world.html
author: Benjamin Supnik
published: '2010-02-04'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

The problem is the scrolling world. If you have a 3-d "world" in your game implemented in OpenGL, you're up against the limited (32-bit at best) coordinate precision of the GL. As your user migrates around the world and gets farther away from the origin, you start to lose bits of precision. At some point, you have to reset the coordinate system.

I see three fundamental ways to address this problem:

Stop the world and transform it. This is what X-Plane does now, and it's not very good. We bring multi-core processing into play, but what we're really bottlenecked by is the PCIe bus - many our meshes are on the GPU, and have to come back to the CPU for transformation.

(Transform feedback? A cool idea, but in my experience GL implementations often respond quite badly to having to "page out" meshes that are modified on card.)

Double-buffer. Make a second copy of the world and transform it, then swap. This lets us change coordinate systems quickly (just the time of a swap) but requires enough RAM to have two copies of every scene-graph mesh in memory at the same time. We rejected this approach because we often don't have that kind of memory around.

Use local coordinate systems and transform to them. Under this approach, each small piece of the world is in its own local coordinate system, and only the relationship between these "local" coordinate systems and "the" global coordinate system is changed.


So that's my question: is there a way to connect two meshes under different coordinate transforms without cracking? Is there a limited set of matrix transforms that will, either in theory or practice produce acceptable results? Do game engines just hack around this by using clever authoring (e.g. overlap the tiles slightly and cheat on the Z buffer)?

The problem with 3) is going to be that as you scroll along, the items in the local co-ordinates all have to be scrolled as well to keep the local placements up to date. As you move forwards, the co-ordinates of the objects behind you are going to prevent you from repositioning the new objects towards 0.



ReplyDeleteI think you need to double-buffer the co-ordinates, rather than the world. You don't need to re-load all the objects, you just need to be able to incrementally calculate the new ideal positions (for maximum precision), then switch to the new co-ordinate system at once.

As for why we're reading your blog... you're the guys doing X-Plane, so you could post crap all day long and we'd still read it.

If the meshes are close to the observer, their respective modelview matrices will be relatively close to identity, meaning that any banding errors are likely to be invisibly small.


ReplyDeleteIf the meshes are far away, what does it matter? You can't see them clearly anyway. :)

I might be wrong, but is this not why Tom Forsyth advocates for using integers for representing object locations?


ReplyDeleteHave a look at:

http://home.comcast.net/~tom_forsyth/blog.wiki.html#[[A%20matter%20of%20precision]]

There was a thread in GD-Algorithms back in 2007 on this topic. The name of the thread was "Huge world, little precision".




ReplyDeletehttp://tinyurl.com/ykll2y7

(The link above provides a search from that list instead of the thread view. It seems to me that the thread view "loses" some interesting posts.)

Jeremy Furtek

How Dungeon Seige handled this issue:

ReplyDeletehttp://web.archive.org/web/20080324041816/http://www.drizzle.com/~scottb/gdc/continuous-world.htm

In our engine we store objects in scene graph with double precision, and when drawing we perform multiplication Model*View with double precision, convert result to single precision and then use it in shader. And yes, all lighting calculations are performed in view space. It's probably not the fastest or prettiest method, but it was very easy to implement, and it works for us. At least, we are able to position objects anywhere on virtual earth with no visual error.


ReplyDeleteP.S. Btw, your blog is one of the most interesting ones among those I read ;)

I also think you're missing something here, but I can't quite guess at what exactly it is.




ReplyDelete> I don't see any way to guarantee that two triangles emitted under

> different matrix transforms will have the same final device coordinates,

> and if they don't, there can be mesh artifacts.

I don't see any reason why the final device coordinates of two triangles emitted under different transforms wouldn't be close enough so there aren't any visible artifacts. In terms of device coordinates, the error will be larger the closer to the camera the triangle is, but the closer the triangle is to the camera, the higher is the precision you get.

When I saw yodenss's Dungeon Siege link here, at first I thought, this _has_ to be off topic. But I just read it and it's surprisingly applicable. “there is no world space” — that's a good hint!

Hi Y'all,




ReplyDeleteThanks for the links! I have some reading to do now. :-) Regarding Anon7y5a5YTE's comment, "close enough" is precisely the issue: given two adjacent triangles forming a water tight mesh, if we aren't emitting the same vertex to the same transform, the set of output pixels isn't guaranteed to form a "water-tight" mesh - there can be 1-pixel cracks between the triangles.

It may be that the solution is to eat the error and accept it by being sure the thing behind the mesh crack isn't bright pink.

It did occur to me that if my mesh boundary coordinates were all integral, then perhaps the floating point transform might be vaguely predictable (if not stable :-).

One bit of follow-up from all of the links, etc.: clearly there is a "3a" technique: establish multiple local transforms, but...



ReplyDelete- Tag each vertex with the index number of its local coordinate space, which lets you vary coordinate space per vertex, rather than per triangle.

- The vertex shader simply has access to _all_ transforms and thus can handle a triangle with "heterogeneous" transforms (e.g. different coord systems per vertex).

- For the "edge" triangles between two tiles, simply make sure the "slaved" edge vertices use the coordinate space and transform of the master tile.

The cost: one value per vertex for any batch that might span coordinate systems, plus a more complex shader.

Hopefully, there may be some information to glean here,





ReplyDeletehttp://blogs.agi.com/insight3d/index.php/2008/09/03/precisions-precisions/

I discuss precision issues we've had in our product and have provided links to others that describe their solutions.

Additionally, I discuss a method of using a vertex shader to get higher precision positions. The method uses 24 bytes instead of 12 for a vertex position, which increases the size of your vertex buffers, but you'll never have to touch them again.

Regards,

Deron