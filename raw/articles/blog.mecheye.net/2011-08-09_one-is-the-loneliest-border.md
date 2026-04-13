---
title: One is the loneliest border…
url: https://blog.mecheye.net/2011/08/invisible-borders/
author: Jasper St Pierre
published: '2011-08-09'
source_blog: Clean Rinse
source_site: https://blog.mecheye.net
category: graphics
fetched: '2026-04-13'
---

Today is an exciting day for GNOME 3.0! Why? Invisible borders have landed! What does this mean for you? One pixel borders are no longer! No more pixel hunting! The last remnants of the cursor accuracy kingdom have been tore down! Pointer precision, you are —

“What?”

Let me draw you a picture.

## Motivation

In GNOME3 before today, if I wanted to conveniently resize a window, I had to hunt for one-pixel borders. I would finally get my mouse positioned *right* on the border, and then carefully click…![Cursor1](../../assets/48de81f87e504710.png)

![Cursor2](../../assets/0092a6f65b83613b.png)


and then miss… So, it’s not surprising [people are upset about this](https://bugzilla.gnome.org/show_bug.cgi?id=644930). Now, you can go outside the actual visible part of the window, and still resize it!

Now, you have as much space in the world to resize your windows: we extend the resizable area to outside of the actual window. Additionally, the mount of area that is available to resize is a user preference, and completely customizable! That is, the green area in the picture below is completely customizable by a gconf setting.![Cursor3](../../assets/c1bcb36db53f938c.png)


The way I did this was by making every X window a little larger, and use Owen’s existing shaping code to hide the excess area around the borders. This means that **toolkits that use the parent window’s size to find their visible extents are now going to break. Use the _NET_FRAME_EXTENTS X atom as a replacement.**

Oh, and since I’m using Owen’s existing shaping code, and that uses an 8-bit mask to hide the shaped region, this made it quite a bit easier to add a feature that people have been begging for for a little while: [antialiased borders](https://bugzilla.gnome.org/show_bug.cgi?id=628195). This hasn’t landed *quite* yet, but it should be coming soon enough!

Next time, I’ll talk about [SweetTooth](http://live.gnome.org/GnomeShell/SweetTooth) some more!

You rock Jasper!

Life quality +20%.

Thank you.

Pingback: Gnome Shell 3.2 – Kurzer Blick auf die aktuelle Beta | Ganz-Sicher.Net Blog

For this problem exists a good solution already.

Move a window by pressing alt key and left-click on any point in the window to move it.

Resize a window by pressing alt key and middle-click anywhere near the windows corner to resize it.

Open up window menu with pressing alt key and right-click inside the window area.

I can sort and resize my windows quick as hell using the Alt-key.

Sure, but there’s no reason to make it better.

Hi,

Thanks for this, I use Gnome 3 since the first 3.0 release and that’s the first time I see this. But in my opinion, it could be even better, or in other words, it could be implement with a more obvious and clear way for the end user I’m.

I’m not a big fan of Ubuntu Unity at all, I find Gnome-shell way better than Unity. But, the Unity “grab handler” is the perfect way to offer a clean and very simple way to move and resize windows.

A screenshot: https://lh4.googleusercontent.com/_1QSDkzYY2vc/TZOJt_8ZaBI/AAAAAAAADxA/UIGrO-dQ9u4/ubuntu11.04_c.png