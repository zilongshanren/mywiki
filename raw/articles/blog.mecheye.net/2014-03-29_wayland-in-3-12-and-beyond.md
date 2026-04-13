---
title: Wayland in 3.12, and beyond
url: https://blog.mecheye.net/2014/03/wayland-in-3-12-and-beyond/
author: Jasper St Pierre
published: '2014-03-29'
source_blog: Clean Rinse
source_site: https://blog.mecheye.net
category: graphics
fetched: '2026-04-13'
---

First, an apology. At the end of [the last post introducing Xplain](https://blog.mecheye.net/2013/12/xplain/), I promised I’d have a new article out once a month. I had a lot of fun working on it, but Xplain has taken a backseat to real work. It’s on one of those “indefinite hiatuses” you hear about which are really just codenames for “eh, I should finish it, but I’ve got so much to do and staring quizzingly at the XKB protocol specification is not the best use of my spare time. I’m just going to let it die.” Yeah…

Sorry.

Ahem. “Real work?”

## Wayland

For most of GNOME’s development, I’ve mainly been working on GNOME Shell and mutter, our desktop shell and window manager systems. I’ve always had [somewhat of an interest in Wayland and graphics plumbing](https://blog.mecheye.net/2012/06/the-linux-graphics-stack/). So when we started to ramp up our Wayland efforts in GNOME, I jumped at the opportunity to work on it.

Over the course of the past nine months, I’ve been busy full-time on our Wayland support in GNOME. I haven’t spoken about Wayland much except in footnotes of [Xplain](https://blog.mecheye.net/2013/12/xplain/) and [The Linux Graphics Stack](https://blog.mecheye.net/2012/06/the-linux-graphics-stack/). I’ve mostly tried to stay out of the political battles surrounding display server technologies and instead tried to focus on working hard building something awesome.

So that’s why I’m really excited about GNOME 3.12. *We built something awesome*.

For the first time, we now have an easily accessible Wayland session for testing. And now that I’ve broken my vow of silence, I’m going to try to blog a lot more about the progress we’ve made for Wayland in GNOME.

## Sounds exciting! Now how do I test it‽

You want to try out Wayland? Awesome! Note, though, that it’s still very a preview, so lots of stuff won’t work. That said, lots of extensive testing is the only way we’re going to be on top of all the bugs and all the crashers. Your help testing and filing bugs *will* make GNOME on Wayland a success!

Wayland session support has been added to gdm. Once you have a distribution that ships GNOME 3.12, it should be fairly simple to try a Wayland session by simply selecting the new **GNOME on Wayland** option at the login screen.

![Wayland GDM Integration](../../assets/263be9d6fa85abc7.png)


It’s supposed to behave mostly like a regular GNOME session! If there’s any crashes, hangs, rendering artifacts, behavior differences, missing features, etc. you encouter, please, *please* [file a bug](https://bugzilla.gnome.org/enter_bug.cgi?product=mutter). I personally look at every single piece of bugmail I get. Even if it seems obvious and dumb, file it. It takes us two seconds to mark a bug as a duplicate, so don’t feel bad about reporting too many bugs.

You might notice that the transition from gdm to Wayland isn’t perfect: the screen goes black, and there’s a blinking cursor for a few seconds when you log in. This is, at least for now, intentional. With the Linux APIs we’re given, at least as far as I’m aware, there isn’t a way to prevent this console showing up without also locking up your machine entirely if something goes wrong and nothing starts: the switch that controls whether the console should be shown is also the same switch that prevents the default VT switching keybindings from working.

For 3.14, we’ll be using [logind to do session switching](http://dvdhrm.wordpress.com/2013/08/25/sane-session-switching/), so hopefully a lot of these issues we’re having with VTs will just go away.

## But I tried Wayland during 3.10 and it crashed, burned my house down, and killed my pet Bengal tiger Leonard! And there’s no remote display support! Wayland sucks!

If GNOME 3.10’s Wayland preview was crashing for you beforehand, please give it another shot. I worked very hard making the Wayland port in GNOME 3.12 fairly stable, and I’ve used it for half a day without being able to make it crash. Obviously, I’m not perfect, so if your session goes down or does something funny, again, please [file a bug](https://bugzilla.gnome.org/enter_bug.cgi?product=mutter) and I promise I’ll take care of it.

Also, there is remote display support.

## What we’ve done

There’s been a full six months of effort in between GNOME 3.10 and GNOME 3.12 in order to make it polished and complete. There really isn’t a major list of features I can point you to as a reason Wayland is better in 3.12. Here’s an incomplete list of things we’ve done, though:

We’ve been working on a more flexible, desktop-specific Wayland protocol, [xdg-shell](http://cgit.freedesktop.org/wayland/weston/tree/protocol/xdg-shell.xml), built to replace the old wl_shell protocol. This new protocol provides atomic state change events, so that you don’t ever see a flicker when maximizing or full-screening a window. This protocol is still under heavy development, and we have plenty of ideas about how to make it better and more featureful than ever. We hope to have a first version of it stabilized for other application developers to port to midway through the GNOME 3.14 release cycle.

We’ve pushed ahead on GTK+’s Wayland backend to make it stronger than ever. It’s been surprisingly smooth: Wayland really is a fairly well-designed protocol that’s a good fit for a modern application toolkit.

Plenty of small bugs since 3.10 have been fixed: windows no longer flicker when they resize. Typing and input method support has gotten a lot stronger. Xwayland windows no longer hang or freeze when you drag them around. There’s no longer an “invisible box” around windows when you drag them around; they line up to the edges of the screen. Keybindings now work. Menus finally stay on top and don’t get occasionally stuck. Submenus are placed in the right spot. I could go on. It’s all the little things that account for 90% of the frustration and crashes.

## Why Wayland matters

Our dedication towards Wayland has pushed us to build a cleaner architecture overall. What used to be a proliferation of X-specific [video and input drivers](http://cgit.freedesktop.org/xorg/driver/) is mostly culminating in centralized, standardized code. For input, we have [libinput](http://cgit.freedesktop.org/wayland/libinput), which we’re using from Weston, mutter, and [Xorg](https://github.com/whot/xf86-input-libinput) as well. What used to be a collection of chipset-specific video plugins for doing accelerated rendering have now been replaced by [glamor](http://keithp.com/blogs/glamor-hacking/), a credible chipset-independent acceleration architecture. What used to be large monolithic components heavily tied to Xorg and the Xorg input and video architectures have now been split out into separate, easily-reusable libraries with separate, easily-maintainable codebases. New, experimental features can be prototyped faster than ever before.

David Herrmann’s work on logind session support mentioned above was originally envisioned for Wayland, but it turned out to be such a great idea that my colleague [Hans de Goede](http://hansdegoede.livejournal.com/) ran with the idea and integrated them into the X server, allowing us to run [the X server without root privileges](https://fedoraproject.org/wiki/Changes/XorgWithoutRootRights), a huge win for security.

Our work on GTK+ is also very much applicable to Win32, Quartz, and Broadway backends as well. A lot of the bugs that we’ve had to fix were bugs on other platforms. GTK+, somewhat unfortunately, was primarily developed as an X11 toolkit and that means our APIs often match up to X11, rather than a more modern system. When redesigning our APIs to support Wayland, we often find that X11 is the special case, and the new code is more portable and flexible than before.

The spoils of Wayland reach far and wide.

## What we’re doing now

It can’t stop here.

For 3.14, we’re going to continue with Wayland development, and we’re all hoping to give a solid Wayland session that can be used for real work. No promises; six months is not a lot of time, and we have plenty to get done. Your testing *will* make it go faster, so if you get the opportunity, please start finding those bugs!

GTK+ is still missing lots of features in the Wayland backend. Most notably, we’re still lagging behind on drag-and-drop and clipboard support. Unfortunately, the APIs we currently provide to developers for these things are old and rusty and aren’t that great. A set of new APIs to make clipboard and drag-and-drop support more sane in GTK+ has been in the works since 2011, and Wayland is a great motivation to finish it off.

mutter’s codebase is almost 20 years at this point, and it’s somewhat surprising that it still has the same code structure as it did when Havoc Pennington started it as an X11 window manager. We’ve bolted additional features and functionality on: an X11 compositor here, a display server there, a Wayland protocol implementation sure why not, a nested testing mode, it goes on. I’ve already started hacking on a large-scale refactoring of mutter, “NWO”, that will restructure the entire program to help fix small nits in behavior and make it easier to add new features.

Right now, my current project and goal is that by the end of April, I’m hoping to ship mutter as a Wayland compositor *without any X11 code running at all*.

It’s pretty exciting stuff! I’m really looking forward to sharing more and more of our progress over the next few months. I’ll heading to San Fransisco in a few weeks for the [West Coast Hackfest](https://wiki.gnome.org/Events/Hackfests/WestCoastSummit2014) where I expect a lot of Wayland hacking will be done. Feel free to stop by if you’re in the area; we’d love to see you there!

As always, questions about our plans, or Wayland tech / Linux graphics tech in general are welcome. Feel free to leave a comment.

Also, excuse me while I get back to watching [The Genius](http://bxrme.tumblr.com/post/69603754319/the-genius-1-2-subbed). You should go watch that too.

that genius thing reminds me of liar game.

also, wayland support is really awesome.

You said: “For input, we have libinput”. Does this apply to GNOME-3.12, or to the future direction only?

libinput is in 3.12, as part of Clutter. It’s in the “evdev” backend for legacy reasons:

https://git.gnome.org/browse/clutter/tree/clutter/evdev/clutter-device-manager-evdev.c

We’re actually planning on moving that into mutter for 3.14.

Mutter’s codebase is nearly 20 years old? It’s old, but not that old :-) First commit in metacity was from 2001: https://git.gnome.org/browse/metacity/commit/?id=287b6b15d3840d6546bbc55f9dbd7b3d098429c3

A bit of an exaggeration, but it gets the point across. metacity started being written when when Windows ME was released. Times were different, both tech-wise and UI-wise.

Do you know if the gnome 3.12 corp packages for fedora 20 include all the bits and pieces to test wayland? When I log on wayland session all I get is gdm’s grey background and the pointer and nothing else happens.

Ditto

I experience the same issue.

Btw. if I encounter problems to which program should I address them in bugzilla?

Yes, I also see the same thing. Journalctl gives me this: gnome-session[1787]: WARNING: App ‘gnome-shell-wayland.desktop’ exited with code 1

WARNING: App ‘gnome-shell-wayland.desktop’ exited with code 1

Unrecoverable failure in required component gnome-shell-wayland.desktop

Me Too [tm]

Me three. Any idea for a fix? ._.

Great status update, thanks for your work.

I’m interested in Wayland as well but I get the same experience. Just ends up displsying a grey background and a pointer. And the rawhide live cd doesn’t have any wayland options. Tried logging out and there was no wayland option in gdm. No option menu at all in fact. And gnome-session –session=gnome-wayland doesn’t work, don’t know what kind of godlike ninja I have to be to try wayland out.

I’ve only been testing on Rawhide at this point. I’ve heard issues with the F20 COPR. I’ll look into it next week.

Great job!

I was kind of hoping sandboxed applications and kdbus would take main focus as they could possibly fix the mess that stops most regular people from being able to use Linux. Developers are not able to finesse the user experience of their apps right now. Too many distro differences and bugs that upstream can’t asses reliably. People just want new stable software the day its released with as little middlemen causing issues. Linux will always be a difficult outdated experience until then.

Getting Wayland ready is a big part of doing application sandboxing, since X11 is insecure and broken out of the box.

When reporting bugs in Gnome Wayland, which component should I choose for reporting session crash? And which logs will probably be useful for this?

Many thanks

File them under mutter. I’ll reassign them if they’re in the wrong spot.

Nice estatus update. I’m intrested con wayland since ever! And to see Gnome working con a wayland session is great. I have only one question, it only works on Intel hardware?

Best regards!

Ah, I forgot to mention that. It does work on all platforms, but right now we only build the XWayland driver for Intel in F20. This is going to change in the coming months.

Thanks! I’ll try to make it work on Arch Linux.

awesome!!!

I am also getting the grey background screen and cursor whenever I select “gnome on wayland” from the GDM. Is there a fix for this?

Same for me intel i7-4702MQ with nvidia gtx 760 optimus, fresh fedora install

Good news!! Thanks for all the effort, us the community will sure appreciate it!

I know it’s not a real bug report, but I can’t log into gnome-wayland on Archlinux with [gnome-unstable] repo (it’s not in [main]/[extra] yet). It blanks and you can see the cursor as if it was attempting to log in, but then it just drops back to gdm.

This is with an A10-6800k (integrated graphics disabled) and Radeon HD7770, 8GB of system RAM. For what it’s worth, it also takes two attempts to log into the Gnome Shell and Gnome Classic sessions, but at least it’s successful on the second attempt. I’ll wait until it hits the stable repos to see if it’s a bug in the packaging or Gnome itself before I file a bug, I guess.

Pingback: News About Desktop Environments: Enlightenment, KDE, GNOME, and Others | Techrights

Sounds great! Care to elaborate on the “remote display” support? Is it related to Weston’s RDP backend and “screen sharing?” (linked below)

http://cgit.freedesktop.org/wayland/weston/commit/?id=47928d8715038e7a5fd7fd383dc3ec2c185ddd23

Yes. We can use

`wl_fullscreen_shell`

to run a nested compositor under Weston, which lets us do stuff like RDP without having any of the code for it ourselves.Pingback: Xwayland | Clean Rinse

Hello, I’m just wondering if there has been any progress made on the grey background with a cursor when trying Wayland? I’m using Fedora 20 with the copr mesa 10 and gnome 3.12 repositories if that is of any help.

Also, for the record I forgot to mention that I am using an Nvidia card with nouveau as well.

Wow! you are doing a fantastic job with Wayland on Gnome, I know you have a lot to do, but one great feature for 3.14 would be a virtual screen mode, with session recording. Musicians and artist open many applications at one time, and it would be of great bennefit to be able to set up a virtual screen to display all of these apps on one screen. It would also be great to be able to arrange your apps on this virtual display just like the Gnome overview. linux multimedia studio does this to a piont, but if this was Gnome wide, it would realy allow people to use thier destops in a more natural way., Thanks for your fantastic work, I am running Gnome 3.12 with Wayland on Archlinux for everyday work, it is very nice.

I’ve got it working on Gentoo. I’ll put it into a public overlay some time next week. Until then, is it expected that XWayland OpenGL uses llvmpipe rather than the accelerated DRI drivers? Am I missing something?

Also, EGL_PLATFORM doesn’t get set to wayland, but to drm, which causes EGL apps (eglinfo) to fail due to access permissions from a running gnome-shell-wayland session. Setting EGL_PLATFORM=wayland manually from a running session works:

EGL API version: 1.4

EGL vendor string: Mesa Project

EGL version string: 1.4 (DRI2)

EGL client APIs: OpenGL OpenGL_ES OpenGL_ES2 OpenGL_ES3

EGL extensions string:

EGL_MESA_drm_image EGL_MESA_configless_context

EGL_WL_bind_wayland_display EGL_WL_create_wayland_buffer_from_image

EGL_KHR_image_base EGL_KHR_gl_texture_2D_image

EGL_KHR_gl_texture_cubemap_image EGL_KHR_gl_renderbuffer_image

EGL_KHR_surfaceless_context EGL_KHR_create_context

EGL_EXT_create_context_robustness EGL_EXT_buffer_age

EGL_EXT_swap_buffers_with_damage EGL_EXT_image_dma_buf_import

Configurations:

bf lv colorbuffer dp st ms vis cav bi renderable supported

id sz l r g b a th cl ns b id eat nd gl es es2 vg surfaces

———————————————————————

0x01 16 0 5 6 5 0 0 0 0 0 0x00– y y y win

0x03 16 0 5 6 5 0 16 0 0 0 0x00– y y y win

0x05 16 0 5 6 5 0 24 8 0 0 0x00– y y y win

0x07 32 0 8 8 8 8 0 0 0 0 0x00– y y y win

0x09 32 0 8 8 8 8 24 8 0 0 0x00– y y y win

0x0c 16 0 5 6 5 0 16 0 0 0 0x00– y y y y win

0x0e 32 0 8 8 8 8 24 8 0 0 0x00– y y y y win

0x0f 16 0 5 6 5 0 0 0 4 1 0x00– y y y win

0x10 16 0 5 6 5 0 0 0 8 1 0x00– y y y win

0x11 16 0 5 6 5 0 16 0 4 1 0x00– y y y win

0x12 16 0 5 6 5 0 16 0 8 1 0x00– y y y win

0x13 32 0 8 8 8 8 0 0 4 1 0x00– y y y win

0x14 32 0 8 8 8 8 0 0 8 1 0x00– y y y win

0x15 32 0 8 8 8 8 24 8 4 1 0x00– y y y win

0x16 32 0 8 8 8 8 24 8 8 1 0x00– y y y win

Yes. XWayland is in the process of getting DRI3 support, but until that happens, we can’t do anything but use software rendering.

I’m running git versions now, and it’s *mostly* working. gnome-shell is very fast. The EGL_PLATFORM issue has been fixed and I have DRI3 GLX XWayland.

There are still a few bugs, obviously, but it’s pretty damn good. SDL2 OpenGL games are very fast (yes, faster than GLX) and completely tear free which is a huge bonus! :-)

Currently Gtk+ apps default to using XWayland unless GDK_BACKEND=wayland is set, I can’t find an obvious way to set GDK_BACKEND in the environment used by apps launched from gnome-shell (short of changing the Exec line in their .desktop file which will break non-Wayland GNOME!) “.profile” only affects the command-line, and it can’t be set system-wide because then gdm* won’t start…

totem/gnome-videos doesn’t seem to be working with Wayland a the moment, even though I’ve upgraded to the git version.

* it should force x11 backend only until it runs under a Wayland system compositor.

Just discovered GDK_BACKEND can take a list, which means I can set it system-wide. It doesn’t help with setting it in the initial environment for launched apps since it doesn’t get inherited by the gnome-shell app launcher.

I’ve recently installed F20 and thought I would add gnome 3.12, but like others here, once I attempt to login, I get a cursor in upper left corner then blank screen. Been sitting here looking at it for last 15 min while reading this page and nothing has occurred. I’m running a Lenovo T-400. Any ideas on what I should do or how to fix? I’m looking at the Xorg.1.log file now and see various errors regarding “wayland” with some entries stating “matched wayland as autoconfigured driver 2, loading /usr/lib64/xorg/modules/extensions/libxwayland.so, and Module xwayland: vendor:”X.Org Foundation, compiled for 1.14.4, module version = 1.0.0 ABI class: X.Org Server Extension, version 7.0. Later on in the log, I get the following entry: Loading /usr/lib64/xorg/modules/drivers/modesetting_drv.so (II) LoadModule “wayland”, (WW) Warning, couldn’t open module wayland (II) unloadModule: “wayland”, (EE) failed to load module “wayland” (module does not exist, 0) (II) Loadmodule “vesa”

lspci = Mobility Radeon HD 3450/3470

Any ideas how to fix this?

Thanks

You’re using the old Xwayland. Waiting until F21 with GNOME 3.14 comes out is going to be your best bet.

Wayland cannot seem to be able to tell which monitor is primary. Anyone know how to force it to put the logon screen on the primary monitor instead of elsewhere? Wayland ignores the /var/lib/gdm/.config/monitors.xml file on my system that used to keep gdm from doing that in Xorg. Whenever I logoff, Wayland slaps the GDM logon screen back to the secondary monitor.