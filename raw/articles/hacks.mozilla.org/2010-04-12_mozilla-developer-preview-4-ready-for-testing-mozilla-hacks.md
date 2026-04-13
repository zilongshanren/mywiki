---
title: mozilla developer preview 4 ready for testing – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2010/04/mozilla-developer-preview-4-ready-for-testing/
author: Christopher Blizzard
published: '2010-04-12'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*Note: this is a re-post of the entry in the Mozilla Project Development Weblog. There’s some juicy stuff in here for Web Developers that need testing. In particular, this is the first build with the CSS history changes.*

As part of our ongoing platform development work, we’re happy to announce the fourth pre-release of the Gecko 1.9.3 platform. Gecko 1.9.3 will form the core of Firefox and other Mozilla project releases.

It’s [available for download on Mac, Windows or Linux](http://www.mozilla.org/projects/devpreview/releasenotes/#download).

Mozilla expects to release a Developer Preview every 2-3 weeks. If you’ve been running a previous release, you will be automatically updated to the latest version when it is released.

This preview release contains a lot of interesting stuff that’s worth pointing out, and contains many things that were also in [previous releases](http://developer.mozilla.org/devnews/index.php/2010/03/03/mozilla-developer-preview-now-available-with-out-of-process-plugins/). Here are the things of note in this release:

**User Interface Changes**

- Open tabs that match searches in the Awesomebar now show up as “Switch to Tab.”
- This is the first preview release to contain resizable text areas by default.

**Web Developer Changes**

- This is the first preview release to contain changes to CSS :visited that prevent a large class of history sniffing attacks. You can find more information about the details of why this change is important over on the
[hacks post on the topic](http://hacks.mozilla.org/2010/03/privacy-related-changes-coming-to-css-vistited/)and on the[Mozilla Security Weblog](http://blog.mozilla.com/security/2010/03/31/plugging-the-css-history-leak/). Note that this change is likely to break some web sites and requires early testing – please test if you can. - SVG Attributes which are mapped to CSS properties can now be animated with SMIL. See
[the bug](https://bugzilla.mozilla.org/show_bug.cgi?id=534028)or a[demo](http://people.mozilla.org/~dholbert/tests/smil/compat_tests/xmlVsCssChart_v1.svg).

**Plugins**

-
Out of process plugins support for Windows and Linux continues to improve. This release contains many bug fixes vs. our previous developer preview releases. (In fact, it’s good enough that we’ve ported this code back to the 3.6 branch and have
[pushed that to beta for a later 3.6.x release](http://www.mozilla.com/en-US/firefox/lorentz/).) - This is the first release that contains support for out of process plugins for the Mac. If you are running OSX 10.6
*and*you’re running the latest[Flash beta](http://labs.adobe.com/downloads/flashplayer10.html), Flash should run out of process

**Performance**

- One area where people complained about performance was restart performance when applying an update. It turns out that a lot of what made that experience poor wasn’t startup time, it was browser shutdown time. We’ve made a fix since the last preview release that made a
[whopping 97% improvement in shutdown time](http://autonome.wordpress.com/2010/03/19/firefox-performance-update-startup-and-otherwise-march-19-2010/). (That’s not a typo, it’s basically free now.) - Our work to reduce the
[amount of I/O on the main thread](https://wiki.mozilla.org/Firefox/Goals/2010Q1/IO_Reduction)continues unabated. This preview release will feel much snappier than previous snapshots, and feel*much*faster than Firefox 3.6. - We continue to add hardware acceleration support. If you’re on Windows and you’ve got decent OpenGL 2 drivers,
[open video will use hardware to scale the video when you’re in full screen mode](http://www.basschouten.com/blog1.php/2010/04/07/firefox-video-goes-up-to-11). For large HD videos this can make a huge difference in the smoothness of the experience and how much power + CPU are used. We’ll be adding OSX and Linux support at some point in the future as well, but we’re starting with Windows. - We continue to make improvements and bug fixes to our support for Direct2D. (Not enabled by default. If you want to turn it on see
[Bas’ post](http://www.basschouten.com/blog1.php/2010/03/02/presenting-direct2d-hardware-acceleratio).) If you’re running Alpha 4 on Windows Vista or Windows 7, and you’ve turned on D2D, try running[this stress test example in Alpha 4 vs. Firefox 3.6.](http://www.tapper-ware.net/stable/web.dom.stresstest.transform/)The difference is pretty amazing. You can also see what this looks like compared to other browsers in this[this video.](http://www.tapper-ware.net/files/stresstest.comparison.ogg)(Thanks to[Hans Schmucker](http://www.tapper-ware.net/)for the video and demo.)

**Platform**

-
JS-ctypes, our new easy-to-use system for extension authors who want to call into native code now has support for complex types: structures, pointers, and arrays. For more information on this, and how easy it can make calling into native code from JavaScript, see
[Dan Witte’s post](http://blog.mozilla.com/dwitte/2010/03/12/extension-authors-browser-hackers-meet-js-ctypes/). - Mozilla is now sporting an infallible allocator. What is this odd-sounding thing, you ask? It’s basically an allocator that when memory can’t be allocated it aborts instead of returning NULL. This reduces the surface area for an entire class of security bugs related to checking NULL pointers, and also allows us to vastly simplify a huge amount of Gecko’s source code.

## 8 comments

sombriksApril 14th, 2010 at 16:01Christopher BlizzardApril 14th, 2010 at 17:49Tiago SáApril 15th, 2010 at 10:16Neil | California Web DesignApril 15th, 2010 at 11:18Daniel H.April 18th, 2010 at 12:09Christopher BlizzardApril 18th, 2010 at 18:43Style ThingApril 22nd, 2010 at 06:36YuriKolovskyNovember 11th, 2010 at 08:19