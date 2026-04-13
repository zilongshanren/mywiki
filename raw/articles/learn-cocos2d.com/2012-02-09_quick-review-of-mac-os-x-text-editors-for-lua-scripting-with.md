---
title: Quick Review of Mac OS X Text Editors for Lua Scripting with Autocomplete
url: http://www.learn-cocos2d.com/2012/02/quick-review-mac-os-text-editors-lua-scripting-autocomplete/
author: Marcus says
published: '2012-02-09'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

I’m looking for a good Text Editor for Mac OS X that supports Lua (preferably without installing any additional files). And I also want the editor to support [autocomplete](https://en.wikipedia.org/wiki/Autocomplete) (aka code completion) for the Lua language, as well as being able to extend the autocomplete keywords.

Much to my dismay this narrowed down the field quite a bit. Therefore I created this list with short (and subjective) reviews of Text Editors for Mac OS X which you may find a good extension to Wikipedia’s [Comparison of text editors](https://en.wikipedia.org/wiki/Comparison_of_text_editors).

But first, I want to be sure we’re all on the same level when we talk about the autocomplete feature. This Qt Creator video with Thorbjørn Lindeijer (of [Tiled Map Editor](http://www.mapeditor.org/) fame) shows you what this feature is all about (beginning at 0:15).

I wanted to find the text editor for Lua that suits my needs. Since there are so many text editors, I quickly dismissed those editors that didn’t support autocomplete. And those whose Lua support needs to be installed manually also took a backseat rather quickly. By all means: please do correct me where I’m wrong, inaccurate, etc. I’m also open to discussing the inception of a flame war, if deemed helpful. ![:)](../../../wordpress/wp-includes/images/smilies/simple-smile.png)



### The Contenders

Without further ado, these are the text editors available as native Mac OS X apps I’ve considered, in no particular order:

* [Smultron 3](http://itunes.apple.com/de/app/smultron/id408831307?mt=12) / [Fraise](https://www.macupdate.com/app/mac/33751/fraise)

* [Smultron 4](http://itunes.apple.com/de/app/smultron-4/id450194894?mt=12)

* [TextMate](http://macromates.com/)

* [TextWrangler](http://www.barebones.com/products/textwrangler/)

* [BBEdit](http://www.barebones.com/products/bbedit/)

* [UltraEdit](http://www.ultraedit.com/products/mac-text-editor.html)

* [Sublime Text 2](http://www.sublimetext.com/2)

* [Komodo Edit](http://www.activestate.com/komodo-edit) / [Komodo IDE](http://www.activestate.com/komodo-edit/compare-with-komodo-ide)

* [Vim](http://www.vim.org/) / [MacVim](https://code.google.com/p/macvim/)

* [GNU Emacs for Mac OS X](http://emacsformacosx.com/) / [Aquamacs](http://aquamacs.org/)

* [Eclipse](http://www.eclipse.org/downloads/) with [LuaEclipse](http://luaeclipse.luaforge.net/)

* [Chocolat](http://chocolatapp.com/)

* [IntelliJ IDEA](http://www.jetbrains.com/idea/) with [Lua Plugin](http://plugins.intellij.net/plugin/?idea&id=5055)

* [IndeEd](http://whiteskygames.wordpress.com/indeed/)

### The Most Impressive Candidates

I think I should start with the text editors that I’m most likely going to use.

#### BBEdit

[ BBEdit has working autocomplete with built-in support for Lua language features. It also shows suggestions from the currently open document, which means autocompletion of local variables and other identifiers. The format for autocomplete definitions is a property list, so it should be fairly easy to edit. Their slogan “It doesn’t suck.®” is a good fit.](http://www.learn-cocos2d.com#)

BBEdit is commercial but $50 seems reasonable.

#### Sublime Text 2

[ Sublime Text 2 positively surprised me instantly. It’s probably the only text editor that defaults to a more sensible dark background with light text, which means I don’t have to fumble with the syntax highlighting at all. The scrollable quick preview of the entire text document in the upper right corner is an ingenious feature I’d love to have in any text editor.](http://www.learn-cocos2d.com#)

Autocomplete works fine and includes identifiers from the current file. Unfortunately it doesn’t provide Lua autocomplete yet (and I didn’t bother figuring out how to install the [Lua package](https://github.com/joshourisman/Sublime-Text-2-Packages/tree/master/Lua)). On the other hand it uses a highly flexible (using regular expressions) and easily editable autocomplete file in JSON format so I’m willing to give it a more in-depth look.

Sublime Text costs $59 but Sublime Text 2 is currently in a beta phase with no trial period time-out.

**UPDATE:** I have since purchased Sublime Text 2. Very happy about it’s not-getting-in-the-way interface.

### Runner Ups

These editors support autocomplete but for one reason or another didn’t quite satisfy.

#### UltraEdit

[ I love UltraEdit! I’m a long-term user of the Windows version. I think I first started working with it around 2000-2002. I’ve also done a great deal of Lua editing with it, and it supports autocomplete although that required extensive wordfile and taglist improvements. Since I know how to do that, I was ready to give the Mac version more than the benefit of the doubt.](http://www.learn-cocos2d.com#)

However the Mac version … it’s different. I didn’t feel at home. It certainly didn’t feel Mac. Not that I would care but somehow I got the impression that UltraEdit isn’t going to be the text editor of choice for me - on the Mac. It also patronized me by defaulting to german language with no apparent way to revert back to english. I ended up deleting the translation files from the app bundle (!) and even then the toolbar icon descriptions remained in german. I hate patronizing apps!

Plus at $60 UltraEdit is one of the most expensive text editors.

#### Komodo Edit

[ I would have given Komodo Edit more time, but didn’t after I found out that ](http://www.learn-cocos2d.com#)[Lua support isn’t a high priority](http://bugs.activestate.com/show_bug.cgi?id=69366). Apparently manually adding Lua autocomplete support is difficult or impossible. I should note though that Lua is recognized and syntax highlighting is correctly applied.

But the default syntax highlighting colors are so that it’s barely noticeable that there’s any syntax highlighting at all. That’s quickly changed however, not so the Windows 3.1 look and feel of the toolbar icons. Visually Komodo Edit really needs an overhaul.

A shame because otherwise it’s a good editor with autocomplete (if it weren’t for lack of Lua autocomplete). And it’s free! The same thing can not be said about Komodo IDE with a price point of well over $300.

### Text Editors without Autocomplete

Those were easy to dismiss as autocomplete was a requirement for me. Still there are a couple good ones for Lua editing, and some of them are free.

#### Smultron 3 (free) / Fraise

Smultron 3 offers no autocomplete but at least has built-in Lua support, which means at least you get Lua Syntax Highlighting out of the box. Smultron 3 has been my trusted companion text editor since I first started working with Mac OS X in 2009, mainly because it’s simple, isn’t cramped with features and implements the basics really well.![Screen Shot 2012-02-04 at 13.38.53](../../../wordpress/wp-content/uploads/Screen-Shot-2012-02-04-at-13.38.53-150x150.png)


Fraise is apparently based on Smultron 3. I haven’t tested it.

#### TextWrangler

[ TextWrangler is the free version of BBEdit. It’s quite suitable if you’re looking for a free text editor, and it’s intended as a stepping stone to learn the ropes of BBEdit until you start wanting more features, at which point you’re probably tempted to buy the commercial BBEdit.](http://www.learn-cocos2d.com#)

Unfortunately TextWrangler doesn’t have autocomplete and a couple other features that make BBEdit great, so I dismissed it quickly.

### Those I didn’t really consider

There are a few editors which I didn’t have to try to know they’re not what I’m looking for.

#### Vim / Emacs / (other Unix editor)

I grew up with MS-DOS Edit and before that, the Amiga CLI. I have no love for Unix-style text editors. Somehow, you have to grow into them, like a root grows into the soil. And then - so I hear - you’ll be forever locked into Vim / Emacs / Whatever.

But I have no interest in dropping every automatism I have acquired over the past 20 years working with MS-DOS and Windows systems and then learn a bunch of new, and awkward keyboard shortcuts devoid of any correlation to the actual function (ie Command+K -> Help or something) which you have to memorize to heart to get all the benefits these Unix text editors have to offer you.

That’s like trying to change an atheist to becoming a religious fundamentalist. Unless I became convinced that using other text editors decreases my life expectancy by 1 minute per keypress or something similarly dramatic, I won’t convert.

#### Eclipse / IntelliJ IDEA / (other IDE)

I want to edit Lua scripts with autocomplete, not an IDE. It seems like overkill unless you’re already quite familiar with that IDE.

In the case of Eclipse it seems as if the LuaEclipse plugin is only compatible with an Eclipse version that’s a few versions older than the latest. Not sure I want to give that a try.

#### Chocolat

Not to be confused with the movie. Chocolat is work in progress, and preorder sales cost $34.

Unfortunately there’s no Lua support yet, and I didn’t bother checking if it is somehow extensible. But it looks like one of those editors that may be worth checking again in about a year from now.

#### IndeEd

IndeEd (terrible name because it’s extremely difficult to find with google) was developed as a Lua text editor specifically for Corona SDK.

I have no idea if it is extensible though. If I were a Corona user, I might like it. Although I would submit a bug report first thing: the text size is too large and the font is ugly, with no apparent way to change that.

### The Fail List

These are text editors which have at least one major defect which seriously compromises its usefulness.

#### TextMate

TextMate does not have ![Screen Shot 2012-02-04 at 13.41.52](../../../wordpress/wp-content/uploads/Screen-Shot-2012-02-04-at-13.41.52-150x150.png)


**auto**complete. It may have code completion, but it is by no means automatic. Watch the Corona SDK TextMate Bundle video from 0:55 on to see what I mean:

You have to press ESC to get a suggestion printed inline. If you don’t like the suggestion, you hit ESC again. And again. And again. Until you get the suggestion you wanted. I have one word for that: terrible! No wait, make that two: **terribly ridiculous**! Sorry TextMate, you have completely missed the point of autocompletion.

Why is this so bad? Because you have to memorize the sequence for each completion. Let’s assume you want to autocomplete **newSprite** after typing **new**. You have to cycle through newImage, newLabel and newPhysics first, thus pressing ESC 4 times to get what you wanted. Suppose one time you type just **ne**, suddenly you get suggestions like negateOption and nestedHawkFlock in between, totally screwing up what you memorized. In that case it is touch and go. And that’s worse than actually typing it out.

Worse, the same thing will happen whenever the underlying API adds, renames or removes functions or members. This sort of code completion can make you more productive if the API is stable and you’re good at memorizing sequences. Otherwise I imagine it’s going to be more frustrating than helpful.

TextMate also doesn’t know about Lua. You can apparently install a Lua bundle but after realizing the autocomplete disaster I didn’t even bother trying.

I would be ok with that if it were free, but TextMate costs about $52 and for that price I expect autocomplete that doesn’t treat me like a button-pusher. Besides that it’s probably a good and reasonable text editor, but multi-ESC-code-guesspletion is just so appalling to me that it went straight to my fail list.

#### Smultron 4

So Smultron decided to go commercial. At $5 it’s still low cost, and it’s a major version increment plus one - so why not give it a spin?

Simple: Smultron 3 is better **AND** free. Most customer reviews on the App Store agree that Smultron 4 is a step backwards. It’s not as intuitive to use, in particular working with multiple windows is painful. Why, oh why?

Well, give it some time maybe but for now, there’s just not a single reason to upgrade to the commercial version. It’s on my fail list because if you have a perfectly good text editor and you want to make it better and commercialize it, you better make damn sure it actually **is** better than the free version.

At the very least I would expect it to be on equal terms, and not fundamentally change the way the user works with the documents just because it’s the new hip thing to have and looks modern. Leave such changes to Microsoft.

### In the End

One thing became clear: if you want autocomplete, you better be prepared to pay for it. With the exception of Komodo Edit, all text editors with autocomplete are commercial or just too specialized (IndeEd). Sadly, the free Komodo Edit lacks autocomplete support specifically for Lua.

If you’re a fan of dark background with light text, do have a look at Sublime Text 2. I’m also impressed by their regular expression code snippet format JSON-style. For everyone else it looks like there’s hardly a way around BBEdit. It certainly seems to be closest to being “the ultimate text editing tool for Mac OS X”, and it’s no more expensive than the rest of the field.

Finally, I know I promised last time to extend the [Cocos2D Webcam Viewer](http://www.learn-cocos2d.com/2012/01/download-modified-files-web-server-cocos2d-webcam-viewer/) with asynchronous file transfers. This was the first time I promised to write about something in particular in two weeks, and then I don’t deliver on that promise because I wanted to write this post while my impressions on the text editors were still fresh, and there were quite a few people interested in hearing about my findings. Still I feel bad, but I’ll deliver it in 2 weeks. I promise!

(Here’s for hoping that this isn’t going to become a running gag.)

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

I know you said no IDEs, but since I suspect this Lua editing has something to do with Kobold 2D, you should look at JetBrains AppCode + Lua plugin. You get a great IDE for your Objective C development that happens to have great Lua support with the plugin installed.

Thanks, haven’t heard that there’s a Lua plugin for AppCode. I will check it out.

Fraise is (was) a bit better than Smultron 3 but sadly no longer in dev or even distributed. No auto complete but is actually my osx “notepad”. Still need some polishing but I’d go for Sublime. I do Lua on it. More “openness”, a lot of packages (auto update of packages with Package Control is awesome), still it will end be paid one day and became the next Textmate.

Hi, Steffen; nice review.

I may suggest adding another product to your list: ZeroBrane Studio Lua IDE (http://studio.zerobrane.com/) I’ve been developing. I know the review is about Lua Editors, and not IDEs, but this product is smaller and more lightweight than many editors on your list. It implements syntax highlighting and auto-complete like you described it (for Lua functions/keywords as well as for custom APIs), but it also supports local and remote debugging, stack view, watches, console and other features and integrates with several mobile and game toolkits: Love2d, Moai, Gideros, and Corona SDK. I have several demos and short tutorials posted here: http://studio.zerobrane.com/tutorials.html.

The IDE is cross-platform (Windows, OS X, Linux), open source and is written in Lua. Thanks. Paul.