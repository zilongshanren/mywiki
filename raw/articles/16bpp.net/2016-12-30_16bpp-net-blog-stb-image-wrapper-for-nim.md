---
title: '16BPP.net: Blog / stb_image Wrapper for Nim'
url: https://16bpp.net/blog/post/stb_image-wrapper-for-nim
published: '2016-12-30'
source_blog: '16BPP.net: Blog / Page 1'
source_site: https://16bpp.net/
category: graphics
fetched: '2026-04-19'
---

Have you ever used any of [Sean Barret](https://github.com/nothings)'s (a.k.a "nothings") [stb libraries](https://github.com/nothings/stb) at all in a C/C++ program before? They are all really lovely. My favorite part of about them is that they all consist of a single header file. No messy linking commands at compile time, just `#include`

them wherever you want. Nothing could be simpler than that. I was a little surprised that no one had made a Nim friendly wrapper for [ stb_image](https://github.com/nothings/stb/blob/master/stb_image.h) yet. So I made one myself. It can be found

[here](https://gitlab.com/define-private-public/stb_image-Nim), or on nimble as the

`stb_image`

package.If you're not familiar with `stb_image`

, it's a nice little bitmap loading utility. It supports many file formats (or at least the ones people care about,) such as PNG, JPEG, PSD, etc. The API is pretty clean. e.g.:



I designed the wrapper to be easy to use and make it seamless for translating between C and Nim. It uses Nim types (handling all those C conversions for you) and returns data as sequences. This is how that snippet above would look in Nim:



I also spent some time binding the [ stb_image_write](https://github.com/nothings/stb/blob/master/stb_image_write.h) library too:



I also had some plans to bind [ stb_image_resize](https://github.com/nothings/stb/blob/master/stb_image_resize.h) but it looked like a lot of extra work and I thought it would be better to keep this wrapper right now to only image IO. Though if there is some demand for that to be bound I can look into it. Though I'd appreciate some help with it. The only things that haven't been wrapped are the callback functions and the ZLIB client. I have no intention of adding those things in myself, but I'm always open to pull requests. These are the limitations of the wrapper yet it should cover most of your use cases. Before using it I'd also recommend reading through the documentation at the top of

`stb_image.h`

and `stb_image_write.h`

too, so you know what it can and cannot do.As of right now the wrapper uses these versions from stb:

`stb_image`

: v2.13`stb_image_write`

: v1.02

They're hard coded into the `*_header.nim`

files (to make it easier on the user). If there is a version change it should be easy to swap out for yourself, but dropping me a line on the issue tracker so I can update the package would be cool.

Once again, you can find the [repo here on GitLab](https://gitlab.com/define-private-public/stb_image-Nim), but I've got a [mirror on GitHub](https://github.com/define-private-public/stb_image-Nim) too. Enjoy.