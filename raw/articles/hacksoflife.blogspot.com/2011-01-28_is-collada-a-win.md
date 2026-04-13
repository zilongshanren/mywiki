---
title: Is COLLADA a Win?
url: http://hacksoflife.blogspot.com/2011/01/is-collada-win.html
author: Benjamin Supnik
published: '2011-01-28'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Is COLLADA a win?

Like most games, X-Plane has the problem of needing to get content from commercial 3-d modeling programs into our proprietary engine format, with annotated data attached that is specific to X-Plane. We need to give our artists a way to attach such data (E.g. billboard properties, hard surface attributes, etc.) natively in their 3-d program and have that data make it into X-Plane.

In fact, the problem is a bit worse for X-Plane because we are effectively an open platform for a whole range of third party developers; thus the world of artists are not on any one 3-d program.

There are three ways I can see to solve this problem:

Write a lot of export scripts. This is the path we're on now. We have full featured scripts for AC3D and Blender, and there are a lot of other scripts out there for other modelers.

The obvious problem with this approach is scalability. Every new modeling feature in X-Plane has to be separately built into every single exporter; the result is invariably inconsistent support for the "full" file format, due to high development costs. (I maintain one of the exporters, the AC3D one myself, and I am not up-to-date on my own modeling formats.)

Create a common, simple, proprietary interchange format. One of the problems with writing X-Plane models is that you have to optimize them to maximize sim performance. The idea of creating a more simple format that feeds into a processing tool would be to lower the cost of writing the actual modeling-program-specific export scripts. Exporters would simply dump out a stream of "stuff" and the post processing tool would clean it.

We already do this with DSF, our scenery file format. DSF is a horribly complex bit-packed format, but a tool (DSF2Text) will convert a simple text stream to the final binary using LR's libraries to do the compression and encoding. While the DSF code itself is open source, a text file represents an easier API for a wide variety of languages, including scripting languages.

Use an off-the-shelf interchange format, hence the question about COLLADA. In theory, the win would be that there would be existing export scripts for the interchange format, greatly reducing the time to implement support for a particular modeler. A common COLLADA -> OBJ converter would then do the final encode once for all programs.

In practice, the devil would be in the details: COLLADA is a very general, rich format; do all modelers support exporting to all COLLADA idioms? Would there be appropriate 1:1 mappings from the 3-d program to X-Plane?

My concern is that it's bad enough trying to find ways to represent X-Plane concepts in a 3-d program; in order to use existing COLLADA code those concepts would have to be in the 3-d program in a way that is compatible with existing COLLADA export code.


I think that the win is that even though you have to deal with 3dsmax's Collada and Maya's Collada and Blender's Collada, it's still way less work to deal with all those options than to write full on plugins/scripts for each one. It would be like if they all supported the same plugin API (with variations) - you'd end up ahead cuz of the commonalities even though you have to pay the differences.


ReplyDeleteAt least that's how it worked on our current project.