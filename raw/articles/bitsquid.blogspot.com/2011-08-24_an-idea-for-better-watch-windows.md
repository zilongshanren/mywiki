---
title: An idea for better watch windows
url: https://bitsquid.blogspot.com/2011/08/idea-for-better-watch-windows.html
author: Niklas
published: '2011-08-24'
source_blog: 'bitsquid: development blog'
source_site: https://bitsquid.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

Visual Studio’s watch window is one of the better ones, but it still has many issues that make the debugging experience a lot less pleasant than it could be.

- Custom data types such as
*MyTree*,*MyHashSet*and*MyLinkedList*are difficult to look at. To get to the content you have to understand the internal data layout and expand the links by hand. - I like to pack my resource data into
[tight static blobs](http://bitsquid.blogspot.com/2010/02/blob-and-i.html)--*file formats for memory*. A simple such blob might have a header with a variable number of offsets into a buffer of tightly packed strings. Such memory layouts cannot be described with just C structs and the watch window can’t inspect them. You have to cast pointers by hand or use the*Memory*view.

*I don’t even see the code. All I see is a hermite curve fitted, time key sorted, zlib compressed reload animation.*

- If I have an array with 10 000 floats and one of them is a
*#NaN*, I have no way of finding out except to expand it and scroll through the numbers until I find the bad one. - The watch window can’t do reverse lookup of string hashes, so when I see a hash value in the data I have no idea what it refers to.

Yes, I know that some of these things can be fixed. I know that you can get the Visual Studio Debugger to understand your own data types by editing

*autoexp.dat*. And since I’ve done that for all our major collection types (

*Vector*,

*Deque*,

*Map*,

*SortMap*,

*HashMap*,

*Set*,

*SortSet*,

*HashSet*,

*ConstConfigValue*and

*DynamicConfigValue*) I know what a pain it is, and I know I don’t want to do it any more. Also, it doesn’t help the debuggers for the other platforms.

I also know that you can do some tricks with Visual Studio extensions. At my previous company we had reverse hash lookup through a Visual Studio extension. That was also painful to write, and a single platform solution.

So yes, you can fix some things and will make your work environment a little better. But I think we should aim higher.

Consider this: The variable watcher has access to the entire game memory

*and*plenty of time to analyze it. (Variable watching is not a time critical task.)

Imagine what a well written C program that knew the layout of all your data structures could do with that information. It could expand binary trees and display them in a nice view, reverse lookup your hashes, highlight uninitialized

*0xdeadbeef*variables, spell check your strings, etc.

## The idea

So this is my idea: instead of writing plug-ins and extensions for all the IDEs and platforms in the world, we write the watcher as a separate external program. The user starts the program, connects to a process, enters a memory address and a variable type and gets presented with a nice view of the data:

￼

The connection backend would be customizable so that we could use it both for local processes and remote devices (Xbox/PS3). The front end sends an

*(address, size)*request and the backend replies with a bunch of data. So the platform doesn’t matter. As long as there is some way of accessing the memory of the device we can connect it to the watcher.

We can even use it to look at file contents. All we need is a backend that can return data from different offsets in the file. This works especially well for

[data blobs](http://bitsquid.blogspot.com/2010/02/blob-and-i.html), where the file and memory formats are identical. The watcher would function as a general data viewer that could be used for both files and memory.

For this to work, we need a way to describe our data structures to the program. It should understand regular C structs, of course, but we also need some way of describing more complex data, such as variable length objects, offsets, choices, etc. Essentially, what we need is a generic way to describe blobs of structured data, no matter what the format and layout.

I’m not sure what such a description language might look like (or if one already exists), but it might be something loosely based on C structs and then extended to cover more cases. Perhaps something like:

```
struct Data
{
zero_terminated char[] name;
pad_to_4_bytes_alignment;
platform_endian unsigned count;
Entry entries[count];
};
```

The program also needs an extension mechanism so that we can write custom code for processing objects that can’t be described using even this more advanced syntax. This could be used for things like reverse hash lookups, or other queries that depend on external data.

Going further the program could be extended with more visualizers that could allow you to view and edit complex objects in lots of interesting ways:

I think this could be a really useful tool, both for debugging and for inspecting files (as a sort of beefed up hex editor). All I need is some time to write it.

What do you think?

Sounds cool. In the cases where it would make sense, the watcher program could also be used to maintain a persistent palette of sample/test values for each data type that could be swapped in.

ReplyDeleteThis would be really useful for debugging (not to mention spelunking undocumented file formats). Heuristics for automatically guessing plausible type structures would be great, too — use the Unix 'file' command's Magic database, and a variety of other tests/swatches ("Does this group of 32 bits represent a plausible x86 floating-point value? If so, and if there are other nearby 32bit floats, what would these look like if plotted as XYZ points? What color would it be if interpreted as 8bpc RGBA?").


ReplyDeleteLike Wireshark, but for memory instead of Ethernet.

@frou @smokris Yes, those are both good ideas.

ReplyDeleteYou may end up implementing your own debugger :( Thats why there is a trend to augment existing debuggers like gdb and windbg with scripting facilities. Scripts dont need to be relinked and as you said there is plenty of time so speed is not an issue.

ReplyDeletethe problem with own debugger that you will need a way to explore running image to get those hex addresses. This means a lot of work like stack walking. Visual studio is my favorite tool too but its kind of black box.

I was sort of hoping to side-step that issue and just assume that we "somehow" get addresses and types from an external source (either user copy/paste or some plug-in to an existing debugger). But I'm not sure how that would work in practice... maybe it would be too cumbersome to be useful...


ReplyDeleteAs you say, stack walking, symbol lookup, etc is probably a lot of work. Especially since I want this to work across platforms...

Niklas, since you use lua anyway you will need some debugger for it. Default approach is to add it to visual studio. This will allow debug of scripts and binary together. I am not sure what people use on ps3 though and I was lazy enough to debug scripts through logging of its effects. That logging was part of C code on each entry point from lua.

ReplyDeleteI definitely need and would love a visual extension or whatever that could allow me to see memory as picture (givving the pixel depth, chanel swizzling and other format information manually at debug time of course) but each time I've looking for it, I failed !

ReplyDeleteThe 010 Editor may connect to process:

ReplyDeletehttp://www.sweetscape.com/010editor/manual/EditingProcesses.htm

google 313

ReplyDeletegoogle 314

google 315

google 316

google 317

google 318