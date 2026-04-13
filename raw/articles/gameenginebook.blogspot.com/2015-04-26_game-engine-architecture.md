---
title: Game Engine Architecture
url: http://gameenginebook.blogspot.com/2015/04/from-peter-a.html
author: Jqgregory
published: '2015-04-26'
source_blog: Game Engine Architecture
source_site: http://gameenginebook.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

**From**

*Peter A. Felvegi*, here's an in-depth list of errata, suggestions, and a few opinions. Note that I don't agree with*all*of Peter's opinions. I've added my own comments throughout his post, where I think that additional clarification or a differing point of view may be of value. Thanks Peter for taking the time to write up this super valuable in-depth feedback!Page 65, Git: I think you missed the main point of Git: it is a

distributed version control system. This means you can work offline most

of the time, commit, merge, etc. Merging is a bliss, compared to cvs and

svn, and has a lot of useful features that support usual real-life

scenarios, eg commiting only selected hunks from files, stashing,

bisecting, and is quite fast. Also, it is excellent for one-man small

projects, as no server setup is needed at all. Moreover, thanks to its

compressed version database, the checked out project with full history

occupies usually less disk space than the current checkout in svn. I

used cvs for years, had to seriously prepare for tagging and branching.

Used svn for years, and had hard times merging feature branches back if

there were more than one stages. This involved manually tracking the

commits that were already merged, lest I wanted them merged again which

resulted in wild conflicts. This was years back, maybe they improved

upon that, I don't care anymore, since I switched to git, and it just

works. This is probably has a lot to do with the fact that it was

developed for tracking the Linux kernel, which is a large scale,

distributed effort. It must be admitted, however, that the distributed

nature and having 40 digit hex numbers instead of integer version

numbers takes a little time to wrap one's head around.

**True enough, and I should have mentioned git's distributed nature as well as its diff-centric design.**

Page 79: I find your 'Release' build a bit confusing. 'Release' means

getting out something from somewhere, so I'd consider this the

production, final version, but what you describe is actually a

developer/internal build.

**Most companies use the terms Debug and Release because those are the defaults provided by popular IDEs like Visual Studio. However, in our case at Naughty Dog (and at EA, actually) we started with Release and then realized that we needed additional optimizations. So Release became a fast internal build, and the term Final or Production was used to refer to the highly optimized build. So you're quite right, at that point the term "Release" became a bit of misnomer.**

Page 105: constexpr should have been mentioned, as it helps

optimization, and simplifies the code for some calculations that

required earlier template metaprogramming. Also, variadic templates are

extremely useful.

Page 106: nullptr is cool, but NULL is still used in later code fragments.

Page 108: the way you initialize the output vector will make it equal in

size to the input, with 0.0 elems, then you append the calculated

values, making it twice the size of the input. Should have called

reserve() after default construction.

Page 110: since later you frown upon exceptions (which I will address

separately), I suppose you planned the code with exceptions turned off,

but this should have been said explicitly, because otherwise:

- new[] might throw, but it's OK

- since you're writing a template, memcpy() is a rather bad choice.

std::uninitialized_copy() should have been used

- but then, T's copy ctor might throw, leaking the allocated array

I'd suggest to rewrite the example as either an exception/leak safe

generic version, or name it IntVector which works only for ints and

malloc()/memcpy() is OK and there can be no exceptions.

**Yes, this code assumes exceptions are disabled... as is common practice in every game engine I've ever worked with.**

Page 111: operator=() leaks memory, since it doesn't free the already

allocated block. The notes about memcpy/exceptions from the previous

page apply here, too. The rvalue version also leaks, but that can

elegantly fixed by swapping m_array with original.m_array, so that the

old array will be freed when the temporary's dtor is run.

Page 117: 3.2.1.5 'atomic data types' is misleading, since atomic types

are related to concurrency and r-m-w operations. What you describe are

built-in types. The same applies to page 119, 'OGRE's atomic data types'.

**The term "atomic data types" is sometimes used loosely in the industry to refer to the built-in types provided by the compiler, or more generally the set of simple (non-struct/class) types. But you're quite right, the term is a misnomer and should not be confused with the concept of an atomic CPU instruction such as compare-and-swap.**

Page 122: regarding writeExampleStruct(): it would be more elegant and

better style to have (or at least, this is how I do binary I/O;):

- the endianness policy should be a template of the stream class

- operator<< instead of a named fn, parametrized with the endianness policy

- there are builtins for byte-swapping, eg __builtin_bswap16/32/64 for gcc

**I'm not a big fan of operator<< for file I/O. I feel it is a misuse of operator overloading, because it completely changes the**

*meaning*of the operator, rather than simply extending its range of applicability to new data types.**Page 125: max() and min() : it might worth mentioning that**


- C++11's constexpr can help optimize these kinds of functions if the

args are constants

- with variadic templates, any number of arguments can be easily supported

- noting that with templates, one can't separate declaration and

definition, compilation unit-wise.

Page 148: I think your treating of exceptions are quite biased, and

quoting Joel Spolsky telling that exceptions are worse than gotos should

be a joke, unfortunately, I missed the smiley. Yes, exceptions have some

overhead, but a good exception handling runtime implementation has only

data overhead and no runtime overhead on the error-free path. Compare

this with checking error codes, which also has data/code overhead, and

additionally, has runtime overhead even if there is no error.

Additionally, it's more error prone, easier to leak resources. About 14

years ago, I read an article, Exception Handling: A false sense of

security (

http://ptgmedia.pearsoncmg.com/images/020163371x/supplements/Exception_Handling_Article.html

), which is now more than 20 years old. It made some good points, so I

used error codes at that time in the projects I was involved with.

However, it proved to be a burden: must use a common large enum for all

the subsystems, which glue them together. Otherwise, with separate error

code groups, without context a single int error code can't be

interpreted. Also, the code had lots of boilerplate cleanup parts. With

time, I learned about the exception safety guarantees, RAII, and

switched over completely. In some cases there were significant reduction

in code complexity and size (my external db sort comes to mind), and

resource leaks practically ceased to exist. Switching to exception

handling won't work without switching of thought, however, but the

guidelines are few and simple: decide the safety guarantees you wish to

implement, and regard any fn call (including operators) as they might

throw, don't pepper the code with try/catch, instead use RAII.

I agree, that mileages might vary, and that there might be good reasons

not to use exceptions, but telling that 'there are some pretty strong

arguments for turning off exception handling' (page 149), without

providing any seems a little biased to me. The main problem with this

omission is that the novice programmers who take your advice without

adequate weighting of the pros and cons might go on a path they will

later regret. I'd suggest some pros/cons table regarding exceptions vs

error codes, including data/code size, runtime overhead,

maintainability, legacy code support, platform constraints, etc. I, for

one, am really curious what were those pretty strong arguments in favor

of not using exceptions in your projects.

**The debate over whether or not to use exceptions is an ongoing and wide-ranging one, with strong arguments to be made on both sides. All I can really offer here is the fact that at every game company**

*I've*ever worked for (covering 16 years), and in every non-game software company I worked for before I got into games (covering 7 years prior to that), exceptions have either been forbidden in all code, or only permitted in offline tools, but never in the engine runtime. The reasons for this prohibition are many, but include:**Exceptions obfuscate control flow by introducing invisible function exit points. To understand a single function in the presence of exception throwing, one needs to wrap one's head around literally***all*of the downstream functions and*all*of the exceptions each one might throw, all the way to the leaves of the call tree. For example, if function a() calls b() which in turn calls c(), and c() throws an exception caught by a(), the implementer of b() must take care to ensure that resources are cleaned up properly during the stack unwind. The problem is that the implementer of b() may not*know*a priori that a downstream function such as c() might throw an exception. (A similar argument can be made for the avoidance of very deep class hierarchies.)**Corollary to #1: Retrofitting exceptions into an existing codebase is extremely difficult to do properly.****Exceptions can lead to resource leaks in a language like C++, which has no support for garbage collection or***finally*clauses.**Exceptions are easily abused/misused. Writing exception-safe code is difficult, in much the same way writing safe concurrent code is difficult. In the case of concurrent programming, the advantages clearly outweigh the costs. However I don't believe the same can be said for the benefits of exceptions over their costs.****RAII (resource acquisition is initialization) is very often not desirable in high-performance game engine code. For example, one often wants to acquire a pool of resources and then initialize and free them individually, on an as-needed basis. Special care would need to be taken to manage such resources correctly in the presence of exceptions.****In a command-line or GUI based tool, exceptions can certainly be a useful way to report error conditions to the end user without crashing the program outright (allowing the user to save his or her work and/or address the problem gracefully). But in a game engine, if a fatal error occurs, there's often no point in trying to recover gracefully -- the game often can't continue anyway. So it's usually best to simply assert-fail with a useful message right then and there, where the root cause of the problem is most clearly evident (breaking out into the debugger if one is attached).**

If you search online I'm sure you'll find no shortage of arguments both for and against the use of exceptions. Ultimately, it's up to each software company and game studio to make its own judgment on the matter. Here are a few articles on the topic for further reading:

**http://www.codeproject.com/Articles/38449/C-Exceptions-Pros-and-Cons****http://google-styleguide.googlecode.com/svn/trunk/cppguide.html#Exceptions****http://www.codergears.com/Blog/?p=835**

just superscalar, but excecute out-of-order also, with hundreds of insns

in flight in a given moment, and that can make suprises when one wants

to naively optimize.

**So true.**

**Page 179: Clifford should have been mentioned along with Grassman. Eric**


Lengyel made a fine presentation on the subject:

http://www.terathon.com/gdc12_lengyel.pdf

Page 258: postincrement vs preincrement: since the guideline goes

opposite to the common C++ idiom, some finer analysis would be needed I

think. Unfortunately, I couldn't quite follow the reasoning, could you

please elaborate? Since the example code on the previous page has for()

loops, the increment and the loop condition are separate expressions.

Either post or pre increment, the condition will use the incremented

value. For lightweight iterators, ints/ptrs pre/post increment won't

make a difference. For complex types, postincrement must make a copy,

which might have some overhead. How is this compared to the data

dependecy? Any real world examples?

**You are exactly right that pre-increment and post-increment offer the same performance when applied to basic data types, all other things being equal. When an increment operation is applied to an instance of a class with a non-trivial copy constructor (such as some iterators), pre-increment can be faster because we avoid calling the copy constructor to hold the original value prior to incrementing it. As such, you're quite right,**

**the example I cited as a segue into the discussion of pre- versus post-increment was misleading and wrong. Because the example deals with incrementing an iterator, pre-increment would be faster (or certainly no slower) than post-increment in that context.**



**My point about preferring pre-increment in high-performance code has to do with creating a data hazard for a pipelined CPU. If you calculate the value A based on the result ++B (e.g. A = ++B * C;) then the CPU pipeline must stall waiting for the value of ++B to be computed, before it can be multiplied with C to produce the final result A. If you reorganized your logic, you might be able to write this expression as A = B++ * C; which would eliminate the data hazard. That's all I was trying to get at. In the third edition, I'll clarify this and use some better examples.**

Page 261: STL drawbacks: one mayor drawback of the containers that the

memory management can't be easily customized. Yes, there are the

allocators concept, but that was invented to overcome the DOS memory

models, regarding to Stepanov:

http://en.wikipedia.org/wiki/Allocator_%28C%2B%2B%29

https://www.sgi.com/tech/stl/drdobbs-interview.html

and not to customize raw memory allocation. Allocators are passed by

value and should be interchangeable by the std: this means you have to

make extra efforts to use dedicated pools, and also write boilerplate

code that has nothing to do with allocation. There are a lot of rants

about allocators, and the genereral consensus seems to be 'roll your own

framework'. Which is quite unfortunate, since the std lib should solve

frequently occuring problems.

Page 266: the Link struct should have the element by value, and not as a

ptr. That way, small value types can be embedded, and the lifetime tied

to the link. And if multiple lists reference the same element, you can

use Link<T*> instead of Link<T> to have a ptr instead of the value. This

way the same link type can be used for both cases.

**Agreed.**

Page 267: With intrusive lists, the link type is:

template<typename E>

struct Link

{

Link<E>* prev;

Link<E>* next

};

struct SomeElement : Link<SomeElement>

{

int i;

};

note that Link<E> never mentions E, just itself. This unfortunately

means, that code can't navigate SomeElements, just Links. If you follow

the links, you can't access SomeElement's members:

SomeElement* e;

int i1 = e->i; // OK

int i2 = e->next->i; // Ooops, e->next is not of type SomeElement, but

Link<SomeElement>

So Link should be

template<typename E>

struct Link

{

E* prev;

E* next

};

This way navigation preserves the type. I see that you made Link as is

to use it also as the root of the circular list (with my version this is

not possible, since then root must be of type SomeElement, which might

not be applicable), but being unable to access the members after

navigation is a serious drawback which might outweigh the simplicity of

the insert()/remove() functions.

Anyway, if the way to go is the circular list, then the Link need not be

a template.

**At Naughty Dog we do it the way I show in the text, and it works well because, as you rightly point out, the Link struct can be used as the head of a circular linked list. The template is useful so we can re-use this code for myriad unrelated data types.**

Page 269: LinkedList::remove() it might worth asserting that one doesn't

try to remove the root node



than 10 times faster than crc32 and better quality), also has 64 bit

version:

https://code.google.com/p/xxhash/

Page 274: might worth noting, that std::string has the problem that it

not only represents the character sequence but it also owns it. Because

of that, const substrings can't be freely passed around, because a new

string will be allocated and characters copied. string_ref is designed

to solve this performance issue:

http://www.boost.org/doc/libs/1_57_0/libs/utility/doc/html/string_ref.html

Page 290: 5.5.1 text config files: json should be mentioned also, as

it's fully hierarchic as opposed to ini files, and has much less noise

and is more human friendly compared to xml. I think it would be nice to

have some pros/cons section about the choice of the options file format

/ method. like

- text or binary? data size is an issue? human readibilty / editability?

- flat or hierarchical?

- visible or hidden (files vs win registry)

A good hierarchical format can also be used to describe UI structures,

without having to write specific code.

**Yes. We have started to use JSON extensively at Naughty Dog. I'll include a discussion of it in the 3rd ed.**



strongly recommend against using it. Windows tends to be reinstalled. If

your game settings were in the registry, they will be lost. I also

recommend against putting options / save games / etc under the user's

home folder, for the same reason. Some of those folders are hidden, and

usually they contain an incredible amount of junk. Having to salvage

saved games, options, etc after a reinstall from that pile is a pain in

the A. I speak from bitter experience. I lost all of my wonderful record

times in Max Payne 2's New York Minute game mode due to a reinstall.

Because of this, my suggestion would be to place all the stuff in the

game's install folder. If per user config is needed, subfolders can be

created for each user. This way if the game's folder is saved,

everything is saved, no matter how badly windows screwed up itself and

had to be reinstalled. Of course, there is the issue of file permissions

in multi-user OS'es, but on windows it's less of a problem, and on

unix'es the main profile folder can be created with world rw

permissions, so new profiles can be created, but then each profile

belongs to its own user.

**Agreed.**



task, but luckily there are a bunch of libraries that help the parsing,

or even generate all the parsing code and even the help from a textual

description.

Page 299: an important difference is file name case sensitivity /

insesitivity. This, coupled with the path separator multiplicity has

some implications for the resource manager: if only one instance of each

resource is desirable in the memory, what happens if "Fonts/Arial18.dat"

and "fonts\\arial18.dat" are loaded? On Windows? On Linux? Obviously

some file name normalization is needed in the resource manager,

converting the case and the path separator. Which might be again

converted if opening the file from the native filesystem, eg on old macs.

Page 305: async i/o: C++11 defines a memory model and the primitives for

concurrent programming. This is an important feature set, and the async

code you provided might use it, or at least this feat of the new C++ std

be noted. Futures/promises lend themselves to the kind of task where you

start the async job, do something else, then use the result of the async

job (or wait until it's finished).

Page 321: on resource files: having a single (or a few) large files

containing the resources are indeed preferable as they stress the

filesystem less, and can be also compressed. Another important feature

is that the data can be optimized if needed for optical storage (where

seek times are large), based on profiling: eg gathering the access

patterns (offset, size pairs of reads) can help rearrange the data

inside the archive file to have no seeks at all while loading the level.

The drawback is that a specific order probably won't work for all the

levels (shared resources), and using one reordering for another level

might result in more seeks, ie worse loading times than without

rearranging. One solution could be to duplicate the data, but obviously

this will have storage costs. Whether it is feasible and woth it is

rather situation dependent. As a generic advice, don't take generic

advices, but judge wisely knowing your application needs :) If the

resource loading can be done async, the loader can batch up requests,

sorting them based on the data offsets inside the archive, and load them

in that order to minimize the seeks.



and store subfolder hierarchies. BUT the compression algorithm is old,

and not too strong in today's standards. It is especially bad for many

small files, as each file is compressed individually. Also, the ZIP's

directory is not compressed, which means a lot of wasted space for a big

game with many files. Creating an own format is easy. Then stronger

compression algos can be used like bzip2 or lzma. You can even encrypt

your data to protect it from prying eyes.

If compression is to be used on the archive level, then don't

pre-compress the assets, only if the generic compression algorithm is

inadequate. This can happen: about 13 years ago I was involved in a

project where a 3d scene was rendered over a high quality, pre-rendered

background. The only problem was that the background had complex

textures, so the zlib compression didn't compress it well. In the jpeg

format it was either too big (over a megabyte :D but that was a lot when

the download speeds were about 32K/s), or too blocky due to the

compression artifacts. So I made a custom wavelet compressor that

produced about 1/3 of the size of the jpeg, with similar subjective

quality. Having dedicated compression algorithms for audio, video,

textures, meshes, animations can be an option even today, but one must

consider whether the increased complexity of the asset pipeline,

packaging, loading worth the reduction in the size of the data, compared

to a single generic compressor.

Another issue is (probably less on consoles than on PC's) patching. If

you have a large compressed file, and only a really small part of the

raw resources change, the compressed representation might have great

differences. This means if you naively generate the patch from the two

versions of the archive files, without any consideration to the inner

structure and contents, you will get larger patches than possible,

meaning longer download times for the players and more bandwidth cost

for your servers. The solutions is obviously to generate the patch based

on the raw uncompressed resources, not on the monolithic compressed

archive files. Another approach is that the changed files are packaged,

and layered above the original archive in the resource manager, so the

new versions hide the old versions when loading. The feasibility depends

on the size of the data set mainly.

Page 322: in point 4, you take on the issue of separating the localized

assets into dedicated archive files. However, I missed the discussion of

the real-life patterns of file management in games. You talked earlier

about the usefulness of wrapping the OS specific I/O interface into a

unified one, isolating the generic code from the platform's specifics,

you talked about the ZIP archives, but there's no advice how the

archives should be organized and used. Especially, how you use the

localized assets once they are in their dedicated archive?

I'd give this kind of advice:

- abstract the raw file handling of the platforms to a unified

interface, let's call it IFile, as file interface, for

creating/writing/reading files

- implement IFile for the platforms' native files

- also implement it for memory files, where raw buffers are read/written

- implement a mapped file, that maps a region (offset, size) of another

file, which looks like a separate file to the user

- abstract the interface of handling collections of files: listing,

opening, reading. let's call it IPakFile. Opening a file returns an IFile

- implement this collection interface for simple filesystem directories

- and also for the archive formats of your choice, opening them from IFile's

- implement a virtual file system (VFS) manager, that is just an ordered

collection of collections which support opening files. Opening works by

searching the file in reverse order in the collections.

With this toolset, a game would do i/o like this:

- create the VFS singleton on startup

- open all common resource archive files, add them to the VFS

- OR, alternatively, especially in developer mode, add one or more

filesystem directories as collections, so free-standing files can be

used without having to package them all the time

- open the language specific common files, based on the current

language, add them to the VFS

- OR, similarly as above, add filesystem directories

- if the level data are in dedicated archives, only add the current

level's archives / directories (common & language specific) to the VFS

- add any patch archives at the end, if applicable

- then, when opening a file thorugh the VFS, it will search it in the

reverse order of the addition. So patches are searched first, any file

that is there, ie the new, fixed version will be used. Then the level

specific files, language specific files, etc.

The power of this organization comes from that once the VFS is

initialized, all the other code needs to talk only to the VFS. No need

to care for details as whether it's a production or a developer build,

whether there are patches, which language is active, etc.

Opening a file from a resource will have this sequence:

- locate the collection in the VFS which has the file

- open through the collection

- if it's a filesystem directory, open the file from the native

filesystem, return the proper IFile implementation

- if it's an archive file, create a mapped file over the archive

file's IFile, with the (offset, length) of the file within the archive,

return the mapped file as an IFile implementation. If the archive is

compressed, things will be a bit more complex as the IFile

implementation must handle decompression: the stored file is probably

sliced into blocks and the blocks compressed individually, the last

block cached in memory.

Managing the lifetime of the IFile instances can be done by hand, but

probably a better idea is to have some handle which manages the lifetime

automatically, avoiding resource leaks.

**All excellent points, and a great discussion of the topic of file I/O and resource organization. I'll try to incorporate some of these ideas into the 3rd ed.**



is also important on the server side of the games (if any): if for some

reason there is a temporary stall, eg the sql server had a bad moment,

the elapsed time must be adjusted lest we want certain events to fire

off too early, before the players had a chance to react, or rather,

before the server had a chance to process their reaction message, which

is probably in the input queue already.



**Agreed.**



'core 0'. Between the two figures, in the text, you write 'the PS3 has

six coprocessors known as...', but on the figure, there are 7 SPU's

numbered form 0 to 6. To the best of my knowledge, there are 8 SPUs in

the CELL. In the PS3, of which 7 is available for the programmer, one is

reserved for Sony's OS. I read somewhere that the 8th SPU is kept as a

backup/redundancy. I must admit I have no hands-on experience with the

CELL, so I might be quite wrong, I only quote what I read.

Page 364: 7.6.1.3 end of line two: 'six coprocessors' is written again,

referring to the PS3 CELL.

Page 366 & 368: in the figures, both 4 core blocks are labeled 'CPC 0'

Page 372: 'six SPUs are used as job processors' six or seven?

**Yes, all of these are typos. The Xbox 360 cores should have been numbered 0, 1 and 2 of course. On the PS4 and Xbox One, the figures should read CPC0 and CPC1, obviously. And the PS3 SPUs should have been numbered 0 through 5 (or 1 through 6, take your pick). There are only 6 usable SPUs on the PS3. The die actually has 8 SPU cores, but one is locked out during the test process to increase yields, and one is reserved for use by the OS, leaving a consistent 6 SPUs for use by games. (And no, it's not possible to "unlock" the 7th SPU for a performance boost... although we certainly have talked about trying!)**



## No comments:

## Post a Comment