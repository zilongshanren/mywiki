---
title: Hey! I was still using that
url: http://c0de517e.blogspot.com/2013/05/hey-i-was-still-using-that.html
published: '2013-05-07'
source_blog: C0DE517E
source_site: http://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

I'm working on a lot of things and this blog has been a bit paying the price, I'll write something serious "soon", but for now, you get this...

Don't install KB2670838. I guess everybody knows, it breaks the old Pix for Windows, and you won't even be able to replay old captures with it. True, we have a new Pix now (graphics debugger) in VS2012 and the old one was well... old. But, I don't care, and I bet not many people do, as the new debugger, for now, is much slower than the old one and more verbose, two very bad things when you have to analyze thousands of draw calls.

Moreover, and this is the point, even if it was equally capable and just "different", that's enough not to kill the old one. People are resistant to change, change alone has a negative impact, see how much turmoil there is for each Facebook update (or iOS firmware update... all of which seem to drain your battery more, if you look at the forums...). So you'd better have a pretty good reason for it.

I don't care about learning a new tool if the old one worked as well or in this case, better. I don't care either, as a user, about the perfectly reasonable motivations you had to invest in this new one.

Now, this is an example (I could have written the same about Apple and the Maps debacle, I didn't update there either), and I'm sure Microsoft doesn't really care much about PC/Dx11 anymore, and it's not making a ton of money on that... People are even going back to OpenGL these days.

Intel is the only company right now that seem to strongly invest in PC graphics, with tools, R&D, demos, lots of activity... GPA is the best debugger today, but I still like Pix, especially on DX10/11 is faster, and navigating it works still better than GPA's erp selection stuff.



*P.S. If you're using VS2012 and you want to capture with Pix for Windows, remember you have to switch your libraries from the Window 8 SDK back to the June 2010 DX SDK ones.*

## 3 comments:

It's not like DX9 tools were better. Basically they all either didn't work with bigger codebases or weren't very useful. Especially when DX10 took off, but most games still had to use DX9 (Windows XP, console compatibility...).

Well, the current tools (But the Intel GPA) are as good as the dx9 ones because they -are- the dx9 ones, since then the interest in Pc gaming has started to slow down.

Dx11 is a good API but arguably not as well supported as Dx9, nowadays it makes sense to use it only because its closer to the consoles and many companies don't car about XP numbers. But most games really are Dx9-class still.

I find NSight to be the best debuggin tool these days. When it doesn't crash of course. Timings occasionally seem a bit wonky, especially when using indirect draws, but overall, the most usable one.

Post a Comment