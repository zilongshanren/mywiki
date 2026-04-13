---
title: Canonical include files for frameworks & libraries
url: https://anteru.net/blog/2012/canonical-include-files-for-frameworks-libraries
published: '2012-03-16'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

My research framework has gotten quite big over the years; the version my clients use at the moment comes with over 400 header files containing nearly 1000 classes. All of this is organized into several libraries (Core, Engine, Image, etc.)

So far, I used one folder for each library, so the user would have to `#include "Core/inc/io/Stream.h"`

or `#include "Image/inc/PngDecoder.h"`

. The main problem with this is that I directly exposed the header structure I used for development for the users; if I renamed a file or folder, all users would have to immediately adjust their code in the next release. Second, it’s difficult to discover where a file lives; if I need the `AxisAlignedBoundingBox3`

, is it in Core or in Engine?

The solution is surprisingly simple and similar to what Qt does or WinRT: Providing “canonical” headers which are stable and easy to discover. While deploying the SDK, I generate an additional set of headers to the users, witch merely redirects to the correct header. Additionally, I flatten the directory structure so all generated headers are in one folder and look like this: `"niven.Core.IO.Stream.h"`

, or `"niven.Image.PngEncoder.h"`

. The fun fact here is that Visual Studio uses string-matching when you type `#include`

, so it’s enough to type #include “PngE`"niven.Image.PngEncoder.h"`

header file. As usual, there ain’t no problem that an additional layer of indirection can’t solve :) It would be better if Visual Studio would do a fuzzy search similar to [Sublime Text](http://www.sublimetext.com/), but just having any search is already a large improvement.

Having now the infrastructure in place to generate those headers, there’s a bunch of cool stuff that is easy to do now:

- Add
`#pragma once`

to each header: Trivial, and saves some compile time for the clients. - Deprecate headers and provide a message where/why something is deprecated.
- Providing “bundle” headers, for instance,
`"niven.Core.IO.h"`

can now trivially include everything related to IO, without having to write and maintain the header manually. - Exclude detail and implementation headers: Throughout my research framework, there’s a bunch of auto-generated detail and implementation headers, which are not designed to be consumed directly but must be shipped as other headers use them. Those are now completely excluded from the generated set, so they are not accidentally used.

Right now, there are only two downsides to this approach: Right-clicking and opening sends you to the redirection header, so you need more clicking; this can be easily resolved with an IDE macro but that needs to be deployed as well then. The second issue is that I don’t have the super-fast-include-goodness when developing the library itself, as they are generated only during deployment. I have a few ideas how to hook this up as a pre-process step – I’m definitely not afraid of generating more code & files during build – but making this clean and keeping the advantages requires some careful thinking.

Having this deployed now, I was really surprised how big the improvement actually is: Typing all required includes is really super-fast now; it’s much easier to find the required functionality and finally it’s also trivial to see which includes are related to my library and which are system includes. The user response was really positive and was quickly adopted for new code.

Overall, a huge win for one-and-a-half hours of effort to get the generation & packaging going!