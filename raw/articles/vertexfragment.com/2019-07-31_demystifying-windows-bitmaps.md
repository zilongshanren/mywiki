---
title: Demystifying Windows Bitmaps
url: https://www.vertexfragment.com/ramblings/demystifying-windows-bitmaps/
author: Steven Sell
published: '2019-07-31'
source_blog: Vertex Fragment
source_site: https://www.vertexfragment.com/
category: graphics
fetched: '2026-04-13'
---

For the vast majority of my career I have spent my time intentionally *avoiding* using GDI(+).

For that matter, I have avoided any platform-specific functionality, regardless of whether it is WIN32 or POSIX, as much as possible. This has had the pleasant result of writing clean, platform independent code for my projects. But has also had the more unpleasant effect of me being woefully unaware of some common functionality when I run into code whose authors didn’t (or could not) follow my personal philosophy.

This has led me to my recent experiences with the GDI Bitmap object, and what should have been a simple affair turned out to be a journey through confusing nomenclature and antiquated documentation whose details do not always match the behavior of the implementation.

It is my goal in this ramble to try to collect together some disparate knowledge of the various forms a simple bitmap takes on Windows into a central location.

To begin, a bitmap is a bitmap is a bitmap unless of course you are on Windows where it is a DIB1 or a DDB or a DIBSection or a … you get the point. I will not go into details about the official bitmap format, what you would expect to see when using a hex editor on a `.bmp`

file, as the [Wikipedia page](https://en.wikipedia.org/wiki/BMP_file_format) on the topic does a wonderful job of explaining it already.

A DIB is a Device-Independent Bitmap and contains precisely the information that is contained within the binary `.bmp`

file, excluding the initial 14-byte bitmap header block. It is represented partially in code as a [ BITMAPINFO](https://docs.microsoft.com/en-us/windows/win32/api/wingdi/ns-wingdi-tagbitmapinfo) structure which contains the following:

- Bitmap Info Header (aka a DIB Header)
- Color Table

The bitmap info header is represented as a `BITMAPINFOHEADER`

and comes in multiple versions:

In this structure is where all of the useful metadata about the bitmap is stored, such as the width/height, bits-per-pixel, and if it is RLE compressed.

Following the info header is the color table which represents either an array of colors that define the bitmap Color Table or an array of indices correlating to the [current logical palette](https://docs.microsoft.com/en-us/windows/win32/gdi/logical-palette).

These two structures, the `BITMAPINFOHEADER`

and the Color Table, make up the `BITMAPINFO`

which when combined with a pixel buffer comprise the DIB. Alternatively, certain GDI functions make use of the [ BITMAP](https://docs.microsoft.com/en-us/windows/win32/api/wingdi/ns-wingdi-bitmap) structure, which is a compacted marriage of the bitmap metadata (width, height, stride, etc.) and the pixel buffer.

With the DIB defined we can now look at the Device-Dependent Bitmap (DDB).

Whereas it is very clear and well-defined what a DIB is, the exact implementation of a DDB is unknown even to GDI itself. It is important to remember at this point what GDI is, which is an interface to hardware devices (printers, monitors, graphics cards, in-memory DC, etc.). In it’s most basic form, GDI is merely the glue connecting your software application to the hardware on your machine without your application having to have any real knowledge of the hardware.

It is on these hardware devices that the DDB is defined, and theoretically each device may have it’s own definition. Because each device has it’s own implementation, GDI provides functions that allow one to query the bitmap data in specific formats.

Because of this, one can call [ GetDIBits](https://docs.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-getdibits) specifying the result to be a 24 bpp, single plane, uncompressed bitmap even if the device on which it lives implements it as a 1bpp bitmap.

To quote the wonderful book [ Windows Graphics Programming: Win32 GDI and DirectDraw](http://www.fengyuan.com/),

The funny thing about DIB section is that it does not have a proper name. Probably an engineer who did not even bother to name it properly implemented it first, and then the technical writing community did not have a clue how to document it properly.


In essence, a DIB Section is a DIB that both the user application and GDI has read/write access to. This is opposed to normal DIBs and DDBs as shown below.

| Object | User Read/Write | GDI Read/Write |
|---|---|---|
| DIB | ✓ | |
| DDB | ✓ | |
| DIB Section | ✓ | ✓ |

The only other difference is that the pixel data for a DIB Section has the option to be from a memory-mapped file, which is known as a “section” in Windows lingo. Of course this feature can be ignored by providing `NULL`

for the `hSection`

parameter of [ CreateDIBSection](https://docs.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-createdibsection).

While `CreateDIBSection`

returns a `HBITMAP`

(which is detailed in the next section), there is additionally a rarely used [ DIBSECTION](https://docs.microsoft.com/en-us/windows/win32/api/wingdi/ns-wingdi-dibsection) structure. In fact, the only GDI function which actually makes use of this structure is when calling

[and passing an](https://docs.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-getobject)

`GetObject`

`HBITMAP`

that was generated by the `CreateDIBSection`

function.The `DIBSECTION`

structure however does highlight the fact that a DIB Section is merely a DIB with an optional memory-mapped section backing it.

Both DDBs and DIB Sections are passed by GDI using a `HBITMAP`

.

If you perform a preliminary search, it will turn up that a `HBITMAP`

is a [“handle to a bitmap."](https://docs.microsoft.com/en-us/windows/win32/winprog/windows-data-types) Ok cool, but what is it really?

If you search a bit deeper (say within `windef.h`

) we see that `HBITMAP`

really is a

```
DECLARE_HANDLE(HBITMAP);
```


… handle. Ok, so it is an opaque pointer but what does that pointer point to? Well if we dig a bit deeper we can see hints as to what a `HBITMAP`

actually is. Specifically, if we look within [libgdiplus](https://github.com/mono/libgdiplus/blob/fe8e0bf2f76b50c18580be11d01bbfe576456f82/src/bitmap-private.h#L106) we find the following structure.

|
|

Of course that snippet should have a bunch of notes attached to is, such as:

- libgdiplus is not GDI or GDI+, however it is used by .NET Core 3 on Linux so it must be doing
*something*right (and they try very hard to be binary compatible with the ‘real’ data objects) - The last two properties,
`cairo_format`

and`surface`

, are most definitely not present in Windows as[libgdiplus offloads much of the heavy lifting](https://www.mono-project.com/docs/gui/libgdiplus/)to the[Cairo graphics library](https://cairographics.org/). - On Windows, the
`active_bitmap`

equivalent property (or perhaps the entire handle) likely points to data outside of process memory, and into kernel space2.

Even if the `_Image`

structure above, which is cast to a `HBITMAP`

higher up within libgdiplus, is simply a imitation mask of what GDI+ actually does it is nice to have some sort of face on what it is other than going with “it is a handle to a bitmap.”

While not necessarily another type of bitmap, the stock bitmap (as returned by [ GetStockObject](https://docs.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-getstockobject)) is a special case within GDI.

It is a single, shared bitmap object which can not be freed, though you are more than welcome to try. In terms of it’s contents, it is a 1x1 monochrome image that GDI uses when it has nothing better. For example when a new memory device context is created the currently selected bitmap will be the globally shared stock bitmap.

For all intents and purposes it can be considered equivalent to a NULL bitmap.

This object is explored in a bit more detail in the article *The mysterious stock bitmap: There’s no way to summon it, but it shows up in various places*

Fortunately, in my personal journey I was able to largely ignore bitmap color tables, and their mapping with GDI Palette objects. It should be noted that they are really only ever relevant for 4, 8, and 16 bpp formats. In 1 bpp a palette is techincally used, but it simply maps to white and black where the binarization threshold from higher formats, such as 24 bpp, appears (through experimentation) to be approximately whether the average of all components is less or greater than half the range. The 24 and 32 bpp formats thankfully do not support color tables.

The topic of compression should also be of little concern to one that is using the GDI(+) APIs, as it is already handled internally. In fact, libraries such as libgdiplus only deal with compression in their encoders/decoders and everywhere else a bitmap is treated and stored as uncompressed.

The resources listed below were used during my own research into this topic (in no particular order):

[MSDN: Windows GDI](https://docs.microsoft.com/en-us/windows/win32/gdi/windows-gdi)[Windows Graphics Programming: Win32 GDI and DirectDraw](http://www.fengyuan.com/)[The Old New Thing](https://devblogs.microsoft.com/oldnewthing/)(various articles)[libgdiplus](https://github.com/mono/libgdiplus)

**1** Admittedly, the term DIB isn’t unique to Windows. But the rest of the mess is.

**2** *Windows Graphics Programming: Win32 GDI and DirectDraw*, pg 618:

For NT-based systems since Windows NT 4.0, DDBs are allocated off the paged-pool, which lives in kernel address space.