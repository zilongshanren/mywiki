---
title: When Not To Serialize
url: http://hacksoflife.blogspot.com/2018/08/when-not-to-serialize.html
author: Benjamin Supnik
published: '2018-08-08'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Over a decade ago, I wrote a blog post about WorldEditor's


That was a good design decision. I have no regrets! The only problem is: the whole premise of the post is quite misleading because:


While WorldEditor does not use its in memory format as a direct representation of objects, it absolutely does use its in-memory linkage between objects to persist higher level data structures. And this turns out to be just as bad.





In a WorldEditor document, a taxiway is a cluster of things with various IDs; to rebuild the full geometric information of a taxiway (which is a polygon) you need to use the parent-child relationships and look up the contours and vertices.


For WorldEditor, the in memory representation is


This seems like a win! Until...



Things get ugly when we want to select edges. WorldEditor's selection model is based on an arbitrary set of selected things. But this means that if it's not a thing, it can't be selected. Ergo: we can't select edges. This in turn makes the UI counter-intuitive. We have to go to bind-bending levels of awkwardness to pretend edges are selected when they are not.


The obvious thing to do would be to just add edges: introduce a new edge object that references its vertices, let the vertices reference adjacent edges, and go home happy.


This change would be relatively straight forward...until we go to load an old document and all of the edges are missing.






To be clear: serializing your data structures is


But if you need a file format that you will be able to continue to read after changing your code, serializing your containers is a poor choice, because the only way to read back the old data into the new code will be to create a shadow version of your data model (using those old containers) to get the data back, then migrate in memory.



If you don't write that translation layer for the file format version 1, you'll have to write it for the file format version 2, and the thing you'll be translating won't be designed for longevity and sanity when parsing.



* We had to do this when migrating X-Plane 9's old binary file format (which was a memcpy of the actual airplane in memory) into X-Plane 10. X-Plane 10 kept around a straight copy of all of the C structs, fread() them into place, and then copied the data out field by field. Since we moved to a key-value pair schema in X-Plane 10, things have been much easier.

[file format design](https://hacksoflife.blogspot.com/2007/01/why-not-binary-blobs.html)and, in particular, why I didn't reuse the serialization code from the undo system to write objects out to disk. The TL;DR version is that the undo system is a straight serialization of the in-memory objects, and I didn't want to tie the permanent file format on disk to the in-memory data model.That was a good design decision. I have no regrets! The only problem is: the whole premise of the post is quite misleading because:

While WorldEditor does not use its in memory format as a direct representation of objects, it absolutely does use its in-memory linkage between objects to persist higher level data structures. And this turns out to be just as bad.

### What Not To Do

WorldEditor's data model works more or less like this (simplified):- A document is made up of ... um ...
*things.* - Every thing has an optional parent and zero or more ordered children, referred to by ID.
- Higher level structures are made by trees of things.

In a WorldEditor document, a taxiway is a cluster of things with various IDs; to rebuild the full geometric information of a taxiway (which is a polygon) you need to use the parent-child relationships and look up the contours and vertices.

For WorldEditor, the in memory representation is

*exactly*this schema, so the cost of building our polygons in our document is zero. We just build our objects and go home happy.This seems like a win! Until...

### Changing the Data Structures

As it turns out, polygon has contours has vertices is a poor choice for an in-memory model of polygons. The big bug is: where are the edges??? In this model, edges are implicit - every pair of vertices defines one.Things get ugly when we want to select edges. WorldEditor's selection model is based on an arbitrary set of selected things. But this means that if it's not a thing, it can't be selected. Ergo: we can't select edges. This in turn makes the UI counter-intuitive. We have to go to bind-bending levels of awkwardness to pretend edges are selected when they are not.

The obvious thing to do would be to just add edges: introduce a new edge object that references its vertices, let the vertices reference adjacent edges, and go home happy.

This change would be relatively straight forward...until we go to load an old document and all of the edges are missing.

### The Cost of Serializing Data Structures

The fail here is that we've serialized our data structures. And this means we have to parse legacy files*in terms of those data structures*to understand an old file at all. Let's look at all of the fail. To load an old file post-refactor we need to either:- Keep separate code around that can rebuild the old file structures into memory in their old form, so that we can then migrate those old in-memory structures into new ones. That's potentially a lot of old code that we probably hate - we wouldn't have rewritten it into a radically different form if we liked it.*
- Alternatively, we can create a new data model that can exist with both the layout of the old and new data design. E.g. we can say that edges are optional and then "upgrade" the data model by adding them in when missing. But this sucks because it adds a lot of requirements to an in-memory data model that should probably be focused on performance and correctness.

*designed*- it's just whatever you had in memory dumped out. That's not going to be a ton of fun to parse in the future.### When Not To Serialize

The moral equivalent of this problem (using the container structures that bind together objects as a file format spec) is dumping your data structures directly into a serializer (e.g. boost::serialize or some other non-brain-damaged serialization system) and calling it a "file format".To be clear: serializing your data structures is

*totally fine*as long as file format stability over time is not a design goal. So for example, for undo state in WorldEditor this isn't a problem at all - undoes exist only per app run and don't have to interoperate between any instance of the app (let alone ones with code changes).But if you need a file format that you will be able to continue to read after changing your code, serializing your containers is a poor choice, because the only way to read back the old data into the new code will be to create a shadow version of your data model (using those old containers) to get the data back, then migrate in memory.

### Pay Now or Pay Later

My view is: writing code to*translate*your in-memory data structure from its native memory format to a persistent on disk format is a feature, not a bug: that translation code provides the flexibility to allow your in-memory and on disk data layouts change*independently*- when you need to change one and not the other, you can add logic to the translator. Serialization code (and the more automagic, the more so) binds these things together tightly. This is a problem when the file format and the in-memory format have different design goals, e.g. data longevity vs. performance tuning.If you don't write that translation layer for the file format version 1, you'll have to write it for the file format version 2, and the thing you'll be translating won't be designed for longevity and sanity when parsing.

* We had to do this when migrating X-Plane 9's old binary file format (which was a memcpy of the actual airplane in memory) into X-Plane 10. X-Plane 10 kept around a straight copy of all of the C structs, fread() them into place, and then copied the data out field by field. Since we moved to a key-value pair schema in X-Plane 10, things have been much easier.

## No comments:

## Post a Comment