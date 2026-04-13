---
title: Simonschreibt.
url: https://simonschreibt.de/wft/open-assets-with-notepad/
author: Simon
published: '2015-10-12'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

![](../../assets/7bfda7715e41ec77.png)


![](../../assets/375ce1b14641e276.png)


![](../../assets/375ce1b14641e276.png)

I didn’t embed the video directly to avoid any tracking from Google and complications with the DSGVO.

# Not only for Notepad++!!

[ ëRiC](http://goodsoul.de/) pointed out that there are ways to use this functionality with every selected text. Independent from any text editor!

[.](http://simonschreibt.de/wft/open-assets-with-notepad#update1)

**Click here to read how**This article is about an easy-to-use plugin for [Notepad++](https://notepad-plus-plus.org/) which makes it possible to work in a TXT or XML and **directly** open files (which are mentioned with their filepath) without the need for opening a file explorer and go file-hunting.

While working on games I often had to work with textfiles like for example material-, effect- and sound-libraries which contain information where the specific assets lay in our asset directory.

![](../../assets/a274dc36ebc34385.png)


When I wanted to look at the texture, I had to look at the filepath, open a windows explorer, click through the folder-structure and finally open the texture.

I don’t like that.

In a dreamworld a click on the filepath in the XML editor would open the file but in our case (developing [X:Rebirth](http://store.steampowered.com/app/2870/)) we used **relative paths** so Notepad++ would have no idea where to look at for the file.

![](../../assets/cecc2fdca0aa7d23.png)


But there’s a great solution coming as plugin to Notepad++!

If you don’t have **NppExec** already in the Plugins-menu, use the built-in Plugin-Manager and install it. It’s really easy. :)

What you have to do first is to press **F6**, admire the small opened window and paste this code into it:

npp_run $(CURRENT_WORD)

**npp_run** is a command and will execute (or “open”) what you tell it to.

**$(CURRENT_WORD)** represents what you currently have **selected** in your textfile.

![](../../assets/875f602b18411ccd.png)


You can **save** your magic script as preset and close the window. What now happens is, that if you select some text, hit **F6** and just press **Enter** (or click “OK”) the program will try to open the file which you’ve selected:

Great thing is, if you have **relative paths** like we did during our work on X:Rebirth, you can just add what’s needed. Here’s an example of what a path in our material library looks like:

assets\textures\argon\ar_hulls_02_diff

Some information are missing like the beginning of the path and of course the file extension.

D:\Simon\Projekte\Egosoft\XR\[assets]\**assets\textures\argon\ar_hulls_02_diff**.tga

No problem! Just add what you need around the **$(CURRENT_WORD)** and you’re perfectly fine!

From now on you can open **every** file within a blink of an eye and if you want to open WAV, Particles, MP3 … just add another line to your script, adjust the path and you’re done!

Here’s a multi-line script-example. It tries to open **several** files and when it has success with **one** of them, it will open it. That’s why you only need one script for everything. :)

npp_run D:\project1\workfiles\$(CURRENT_WORD).psd

npp_run D:\project1\assets\$(CURRENT_WORD).dds

npp_run D:\project1\assets\$(CURRENT_WORD).fbx

npp_run D:\project1\sfx\$(CURRENT_WORD).wav

Also it helps a **huge deal** if there’s a error in the filepath like a missing “\” and you wonder why the game can’t find your asset. With this plugin you just do your selection press F6+Enter and know 100% if the path to your file is fine.

I hope soon you’ll experience too how drastically this small plugin improved my workflow and removed the annoying part of crawling through file structures to almost zero.

Feel free to drop any feedback in the comments, [mail](mailto:simon@simonschreibt.de), [twitter](https://twitter.com/simonschreibt) or [facebook](https://www.facebook.com/simonschreibtblog)!

![](../../assets/ba0680151067ebbc.png)

[ëRiC](http://goodsoul.de/)asked in the comments very good question:

**“Why not use**(not only with Notepad++).

[AutoHotKey](http://ahkscript.org/)to make it generally work?”Because of this I copied [this code](http://autohotkey.com/board/topic/66718-how-to-get-selected-text-without-using-the-clipboard/), extended it and if you now press **Ctrl+J** the currently selected text (doesn’t matter **where** you select it!) is taken as relative path and executed:

^j::

WinActive(“A”) ; sets last found window

ControlGetFocus, ctrl

if (RegExMatch(ctrl, “A)Edit\d+”))

ControlGet, **text**, Selected,, %ctrl%

else {

clipboardOld := Clipboard

Send, ^c

if (Clipboard != clipboardOld) {

**text** := Clipboard

Clipboard := clipboardOld

}

}

**PSD** := “D:\project1\workfiles\” **text** “.psd”

**DDS** := “D:\project1\assets\” **text** “.dds”

**FBX** := “D:\project1\assets\” **text** “.fbx”

**WAV** := “D:\project1\sfx\” **text** “.wav”


Run **%PSD%**,,UseErrorLevel

Run **%DDS%**,,UseErrorLevel

Run **%FBX%**,,UseErrorLevel

Run **%WAV%**,,UseErrorLevel

- ^j:: means, that you have to press Ctrl+J to execute the script (learn more in the
[official documentation](http://ahkscript.org/docs/Tutorial.htm)) - The following code gets the currently selected text.
- Then the paths are build together from static paths like “D:\project1\workfiles\” and the currently selected text in form of the
**text**-variable. - After this every variable is executed (UseErrorLevel means, that no error pops up, if the file doesn’t exist)

Hey Simon! Awesome video and explanation!!! :D whoww!

I’m a hard core np++ fan! And use it every day. Although I moved coding Python to a real IDE such as Eclipse with PyDev I still like the simplicity, fast response of Notepad++. I never used nppExec so far! But seems interesting!

Actually I wrote a similar thing some time ago for my Autohotkey scripts. It could even look up multiple paths one by one to see if the relative path fits and it works from anywhere, not just np++.

Well.. I really need to catch up with this and make it “vorzeigbar” But here is a snippet about it:

github.com/ewerybody/a2/wiki/winr

so

winris a little module for this AHK-script-collection and frameworka2.I wrote about it here on my blog.

As I did not yet implement controls to set a list of those paths this functionaliity is not yet on the frontend of this winr thing… I still have too little time to develop a2. But every now and then… Actually I just want to code some right now :D

other np++ Plugins I can recommend:

* ScrollPastEOF !!! to not have the bottom of the file at the bottom of the screen.

* Language Help !!! to connect any language to its online help or offline CHM..

Cool tip.

I found out that the path cannot contain any ()-brackets though or the path will not work.

If you can still use () in your folder names but then you need to make sure that the path is treated as a string. Example:

npp_run “c:\Program Files (x86)\”$(CURRENT_WORD)

Very good observation! First I thought “who uses ( or ) in pathnames?!” but the program files example shows that brackets are used very commonly :) Thank you!

Superb tip Simon! I’ve been muddling through for so long I’d forgotten the pain, now I’ve no idea how I got by without this :)

Top tip to suppress the annoying Console window when using your original (as posted) tip… prefix your script with;

NPP_CONSOLE 0

wow that’s an awesome tip! cool, thank you!

If you use VsCode

https://marketplace.visualstudio.com/items?itemName=Fr43nk.seito-openfile

This can solve that problem as well and you can feed it a list of paths to look underneath. Works pretty great!