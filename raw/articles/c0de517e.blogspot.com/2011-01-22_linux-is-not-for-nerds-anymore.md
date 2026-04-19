---
title: Linux is not for nerds anymore?
url: https://c0de517e.blogspot.com/2011/01/linux-is-not-for-nerds-anymore.html
published: '2011-01-22'
source_blog: C0DE517E
source_site: https://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

I've always, always hated Linux. I've never even really loved too much the opensource movement, I really like the idea but in practice most projects end up being tech-oriented piles of "features" with no clear design or user target in mind. It's somewhat ironic, even if totally reasonable, that most of the really usable, great opensource projects are usually derived or inspired by commercial applications (i.e. netscape - mozilla - firefox) or backed by big corporations.

But still I've always been interested in it and how can you not be... An OS that you can hack freely, it's a sexy idea for every programmer.


So time to time I give linux a chance, every couple of years let's say, only to be frustrated by it.

So time to time I give linux a chance, every couple of years let's say, only to be frustrated by it.

At the beginning you needed to recompile the kernel for almost everything. Then it came the time where you could not have a driver for almost any non-obsolete external periphery. Then it was the KDE vs Gnome era, both were ugly and slow and crashed every few minutes so it was really a tough choice between the two. For a while I was into the live-CD craze, with

[Knoppix](http://en.wikipedia.org/wiki/Knoppix)and all the other distributions. They were never really useful to me but I still managed to burn dozens of DVDs with them (we're talking of times before cheap and big USB keys... where people burned CDs!), and it was a way to keep an eye on the progresses made...And then it came...

[Ubuntu](http://www.ubuntu.com/). A serious project, with money behind it and a focus. And everything apparently changed.I'm seriously becoming to think that Linux made it. This might not be a surprise for all of you that work with VIM and love GCC and so forth, but for me and I bet many others, it's news.

I've installed

[Jolicloud](http://www.jolicloud.com/), a netbook, webapp centric ubuntu spinoff on my two netbooks (an ancient EEEPC 901 and a HP Mini 1000) and I'm impressed. My girlfriend is currently away for work and she brought with her the EEEPC. She is not a computer geek (at all) and she is even more conservative than me when it comes to changing user interfaces and trying to not be annoyed by technology, and she is liking Linux...I didn't have to download any driver. I didn't have to download applications from websites. I have a centralized point for the updates. I have a great interface, with great font rendering. Performance is great. It does not crash.

To be totally honest, I've found a small glitch. The USB installer provided through the website did not work, and the more updated one stored on the ISO... was on the ISO. Just plain dumb. But after extracting it, everything went smoothly.

It's the closest thing to having a Mac without paying for it! Some friend of mine also suggested to have a look at

[MeeGo](http://meego.com/devices/netbook), it looks cool from the screenshots but I didn't try it yet. Already the idea of having too much choice between distributions is starting to worry me :)I even tried Ubuntu also on an oldish Acer but it didn't work too great and I've uninstalled it. As you might have understood by the tone of this post I'm really not into fiddling with the machine, so I didn't try to benchmark the system or fix it, it might be something specifically wrong with that machine or just that the default Ubuntu is too heavy for it.


A key to the Jolicloud success is also that it specifically supports a given hardware (netbooks, and it has a long list of compatible ones) so it can be successfully optimized for that target.

A key to the Jolicloud success is also that it specifically supports a given hardware (netbooks, and it has a long list of compatible ones) so it can be successfully optimized for that target.

Could it be that an OS built on a mediocre kernel and outdated, server-centric concepts, evolved so much to really be a viable alternative for the consumers? And not as an embedded thing, but on the PC hardware, competing with Windows? Incredible, but true.

I'm a believer. Now if only they had a decent IDE... Or if photoshop ran on it...



## 40 comments:

Linux is certainly in a much much better shape than it used to. I started using Linux back in 2003 when even playing a god damn MP3 was a major pain in the ass so I gave up soon. I, too, have come back to Linux every or every other year only to be disappointed yet again. But 2009 was the year that Ubuntu hooked me, to the point that I've been running a dual boot system ever since and using Linux for everything except programming.



The only thing that's keeping me away from using Linux almost entirely is the absence of a decent IDE. There are a gazillion IDEs out there, but **ALL** of them have serious shortcomings. And god do I HATE Eclipse. Such a bloated ugly fucking IDE. Netbeans is the best Linux IDE I've come by and even that is a couple years behind Visual Studio.

Only if Linux users would give their nerdish Vims and Emacses up for a modern IDE and open their fucking world to the rest of the world, Linux would have many more users. It took them a decade to come up with Ubuntu, it will probably take them another decade to come by a usable IDE.

As for the previous comment... I know this isn't what you want to hear, but Emacs is about a million times more powerful than visual studios.






There's a hierarchy of editor power and it goes something like:

notepad/gedit->eclipse/visual studios->emacs

Emacs definitely has every feature VS or eclise has... and then some. Yes, of course this includes intellisense/jump to definition stuff for c++/java/whatever. See GNU Global, etags, GCCsense, dabbrev. I use GNU Global and dabbrev for c++, as they are very fast.

I think the issues newbies tend to have with emacs are:

1. emacs is not CUA. This is a good thing... an editor that needs to use a mouse is not ergonomically efficient. You shouldn't need to take you hand off home row when editing. Personally, I use ergoemacs style keybindings to make it even more efficient.

2. Emacs is written/extended/configured in lisp. You need to learn elisp to use/configure/extend it effectively. The upside of this, is that lisp is a flat out awesome dynamic programming language. Because lisp is awesome, emacs extensions are easy to write, so there is an emacs mode for every conceivable task.

3. Emacs is kind of like a hunk of marble you carve your favorite editor out of. It works exactly the way you want, down to the smallest detail, but that means you are responsible for spending some time configuring it to work that way. No one uses the "out of the box" defaults, so newbies are sometimes confused why they are so strange.

1, 2, and 3 mean there's much more ramp up time to get good at emacs than VS. However, I've used both and emacs leads to higher productivity in the long run. Plus, it's free.

I would say emacs is kind of a microcosm of linux in this way. It takes more time to configure, but the end result is more flexible and powerful.

Hmmm ignorance and irrational vitriol, how did this get into my Google Reader? At some point I must've thought this was an interesting programming blog.


Unsubscribe.

Brendan: I can agree that Emacs is good.











I don't know, I've come to accept the fact that VIM is really a good editor. But the learning curve is just unacceptable.

I don't think programming is about being the fastest on the keyboard, thus even if VIM or Emacs can save me some typing I really don't care.

I want something easy and integrated. That just works.

Possibly without needing to customize things in lisp or to read a manual just to save a file. Or to open one. Or to close the editor.

The amount of customization and I can accept is to change my color scheme and install Visual Assist X and metalscroll :D

But seriously, no matter what's your metric to judge an interface, having to read a manual to save a file is a no-no.

By the time a person learns and customizes emacs, I'll have shipped two games :)

That not to account that I don't program in an unix environment at all.

So all these tools would need to interface with a variety of third-party and in-house build systems, compilers and debuggers that are guaranteed only to work out of the box with VS...

I don't want even think about that. Maybe it's possible, but it's simply not an option for me.

I can understand that if you were unlucky enough to _have_ to learn such editors at university or so then it's fine to stick with them, but I won't ever recommend learning them if you don't.

Ash: lol, the first time I had to code in linux (university project) I ended up using Rhide (http://www.rhide.com/), a clone of the Turbo C++ ide done with Curses I think.




KDevelop and CodeBlocks looked promising, I've tried them both a while ago and they were really rough.

SharpDevelop under windows is not bad I think it can run on Mono, but it's C# only... That does not really disturb me though because at home for small experiments I really only code in C# or plain C.

The worse things that are still a problem for me when it comes to using linux on my home desktop is that there's nothing decent for photography and there's nothing decent for shader prototyping.

Anonymous: Bye.

Strange to hear that you do not want to learn the way to learn a new editor since, at some point, you had to learn VS and Visual Assist (with all his great keyboard shortcuts, BTW). Sounds like you did not want to learn anything really new to you. Be aware, you are getting older. ... :)

Anonymous: I'm always learning stuff but I am getting older it's true. I have to select more what it's worth learning. Text editing is not the most interesting part of my job (luckily, I'm not a data-entry guy or a touch typist or something like that).





About VS and VA-X the comparison is really not there. I found VA-X as it was installed by default in one of the companies I was working with, what learning is there?

You press the right mouse button, all the options are there, they are pretty obvious (rename, find definition... duh) and the shortcuts are written next to them...

That's like 10 seconds learning curve... It requires 5 minutes just to learn how to quit VIM... And I know because I know the basics of VIM, so I had to learn them :D

No, I'm sorry, I know that editors are quite a difficult topic and I know how much VIM and Emacs can be loved. But no, in this century, having to read a manual to quit an application is just wrong, people should burn in hell for that.

I guess there is nothing really there to convince to look on the other side (~VS).








Without speaking about strict qualities of all editors (I have mixed feelings about VS anyway since I had to use more or less it for 2 years), with VS you pay the price of the dependency. I mean what would you do:

- if you have to develop on IPhone: basically, drop VS, learn and use xcode?

- if you want to code on Android, use Eclipse?

Saying you want to use any non supported language?

I still do not understand people who wants everything already done except for they are paid to do. You are a renderer guy. So you only program C++/C#/shaders? So, scripting the build is none of your business? Scripting your editor is none of your business?

I guess this why people like to use Emacs or vim.

- For emacs, you configure your own sand box plugging programs into your editor to make your own environment.

- For vim, you use the command line and scripts besides your editor and do whatever you can imagine to do.

This is their power. In one minute. I can play with any exotic language, I can edit anything without losing too much of my regular productivity (like editing C/C++ as I mostly do everyday)

I still do not understand why some people want to be creative for some stuffs (like writing renderers) but absolutely not for others.

VS is OK but being so dependent to this tool would be just scary to me.

Being independent has a price but still, it is worth it.

More seriously, VIM and Emacs are one of the examples of what is wrong and what I hate about most opensource projects and most of the geek/hacking thinking.







It's the idea that features matter more than the user. Or that the user is a sweaty geek that loves convoluted interfaces :D

All the things that I hate most about technology and programming are due to this attitude.

In my work, I see that in rendering engineers that love cycles and cool techniques more than their artists, their clients.

That can't communicate outside binary code and live closed in their little engineering world.

Of course in a company you need this kind of guys too, but really when I see that attitude it annoys me a lot.

And really, going back to the post, this is why Jolicloud is nice. Because it's a project focusing on 0 features and all on user interface. It could have been built on linux or darwin or netbsd and it would have been equally succesful. The only thing linux gave it is a wider hardware support than all the other open OS

VIM / Emacs are tools for programmers by programmers. I do not care about the fact that they are not fancy and easdy to use. Come on. You are a rendering guy! Did you see Maya?? This is a monster not for newbie. A tool for graphists. Not for you. Not for me. Just created to be effective for people who will use it. So not user friendly but the user base DOES NOT want it to user friendly.


As for Linux Desktop. Well. I am a Linux user (full time). And yes this just sucks. I use dwm anyway now which is the best anwser I found in front of the disaster which is (mostly) the Linux desktop situation.

@Brendan:



Could you possibly comment some more on your emacs/global/dabbrev setup?

I am using emacs for quite a while but I never got the code completion etc working the way I wanted.

How do you setup gnu global for a c++ project? I have projects using other projects, does that work? Does it automatically rescan if a file changes? How do you setup a new project?

Thanks.

Anon: no, VIM and Emacs are made by VIM and Emacs guys for VIM and Emacs guys. And it's not that an UI that is productive for experts have to be incredibly ugly and complicated.













I'm a rather experienced photoshop user and I can work in it removing all the toolbars and windows.

That does not mean that you should ship photoshop in such a mode, so people won't know how the fuck to load a file! But surely it's handy that it has shortcuts for everything and a hotkey to go fullscreen...

Moreover I wonder what does it mean "made for programmers". I realize that VIM, being always in "macro-editing" mode really speeds up some editing tasks. But is being a programmer about copy and pasting things fast or stuff like that?

For me, an editor for programmers is first of all an IDE. Because I want to be able to see my code in motion, to run and debug it, to live-modify it, to have maybe a repl window for quick experiments and so on.

Out of the box neither VIM or Emacs are integrated with anything. It's like C++ "designed for performance" that does not have native threads nor SIMD, you need to use libraries for these things... Duh...

Maybe a really really nice "for programmers" editor would show me the declarations of objects as I navigate the source, maybe will compile and highlight errors for me.

Maybe it will be integrated with my SCM.

Now I know that you can add all these things to VIM and Emacs, but the fact that you have to add them does make them look like somewhat less "programmers oriented"

Then if someone asks me how would I imagine the future of code editors I would even less see something like VIM. I would see something heavily graphical, that allows me to jot notes and make sketches and diagrams. That allows me to watch a variable and plot it in real time or show an area of memory as an image, or integrate with PIX and I would see the mouse being used a lot together with the keyboard, and I would see less typing and more reasoning, and drawing and inspecting and thinking.

Really typing text is not a big part of my work day. And 50% of the text I write is emails and MSN :) And yet I think I'm a pretty "hardcore" rendering programmer...

About Maya, last and not least, it's a fitting example. It has a bad interface and most artists actually do not like it. I've seen many artists coming from a gaming background going into movie production that where shocked about having to learn Maya. Maya is a great tool, extremely powerful and customizable, but not friendly and that is a problem.

So much that even if it is technically better, it was crushed by 3dsMax, that was way, way, way inferior to everything else, but way more popular, and so, it won, and now autodesk owns them all...

:-)






I guess this is definitely two worlds clearly (windows and unix..) not coming together. I personally dislike integration. Desktop one. Coding one...

It is not integration itself I dislike. It is that it has a tremendous cost in complexity. As soon as you have kde, VS or windows, developping for it is painful and you definitely always rely on external tools and complex plugins for your job.

I understand your point. You have to spend more time to learn your tools when it is not cleanly integrated with a UI (I recemtly discovered MacOSX and I saw how bad windows UIs were usually BTW).

And the problem is not to learn one tool in particular. Most of them are relatively simple (vim is relatively simple but pretty different. It is like learning dvorak when you come from qwerty). It is just the number of them. I guess this is what unix coders mostly do. Learning tons of small tools.

Still, the combination of all these tools give that pleasant feeling that you can learn more and more. Jumping easily from build system (like android one or Iphone one) to another, one language to another. You want to experiemt ocaml. Paf you open VIM, you edit, Paf, you open your terminal, you compile. What? There is no history in the lua interpreter. Hop, I embed it into rlwrap. Ok, these are rough edges. Ok, you plug tools together inm a hacky way (already tried to send commands from VIM to a terminal through GNU screen). But, damn this is good :)

I like my small tools. I hope not to be a stupid moron. But really, this is pure fun and really productive.

Here's something re: photography on linux: http://darktable.sourceforge.net/

This is anyway a discussion I got so many times. It is hard to give the feeling of unix programming in general. Coding in Unix at the beginning is just a f**** pain.




But so many tools are here. I personnally spent at least 3 or 4 years to be *fully* sastified with the way I am coding. This is a very personal way. Most of my teammates who worked on Unix, all of them, had their very specific own way to work. People using emacs are just aliens to me.

So, unix programming is generally a hard path. But still, I am in peace on Linux never angry due to the system. Windows + VS despite its incredible features still pays the price of its own complexity. Slow, unstable (on vs 2008, I remembered creating a directory to completely disable this stupid and slow intellesense which went crazy with our big code base (it was a video game)), not fully reactive (I always felt this lag with the editor).

Really, Microsoft programmers are good ones. I am sure of it. But, they are creating monsters. They have good reason for that: this is easy to learn, lots of functionnalities. But the drawbacks always killed my patience.

Hi DEADC0DE,







I started using Linux on a daily basic about a year ago. I used to be very dependent on Visual C++.

BTW I hate Eclipse too. I also don't like Code::Blocks and other shitty environments.

On Linux, I discovered Qt Creator and I started to love it. It has everything I needed in Visual C++, especially code indexing (AKA Intellisense) and refactoring (which Visual C++ lacked in 2008). You doesn't have to use Qt if you don't want to. What's really cool about Qt Creator is that it can import any Makefile-based project and you can start coding pretty much immediately, no project configuration needed, all source code is automatically indexed. (assuming you are ok with the fact it runs "make" if you select "Build All")

As a debugger, I often use a stand-alone one called "kdbg", which works well for me.

As profilers, I use valgrind (with kcachegrind to view profile data) and sysprof. These two are superior to anything I've seen on Windows and both are stand-alone as well. (you only need to compile with debug info for it to work, yet you can still enable all optimizations and get good profile data)

All these tools make up a killer development environment and now I have no reason to go back to Windows.

DEADC0DE, I so agree with your gripes about Emacs. Having to RTFM for the most basic functionality is just plain bad UI design. It *may* have been a positive thing of it made power users' lives easier, but it doesn't! C-x C-s is a too complicated key sequence for something you do a hundred times a day. Even if you're an expert!

linux/Documentation/ManagementStyle


"Hint: internet newsgroups that are not directly related to your work are great ways to take out your frustrations at other people. Write insulting posts with a sneer just to get into a good flame every once in a while, and you'll feel cleansed. Just don't crap too close to home."

Oh, this is evolving into a long thread about something I'm not really passionate about (I didn't start this editor topic :D)...



















Anon #1: You have a point but I guess it's a matter of taste. I love integration because I think it's less distracting to have everything in the same environment and with an uniform UI.

Also, being a specialized, integrated environment means it can be more powerful. Yes it can't support all the languages out there, but it can do a better job supporting the ones it does...

For example FX Composer is an IDE for shaders, and it integrates shader editing with some basic 3d scene authoring functionality and so on. OpenCLStudio for OpenCl... there are many examples of things that IDEs do and pure text editor can't.

Also having a graphical UI is really fundamental nowadays. I can't think living without metalscroll for example now that I've discovered it and I think the graphical capabilities in IDEs are still way underdeveloped. I want something like DDD and better...

You won't be able to have that in VIM or in a generic editor. BTW when I need a generic text editor (and I do often) I use notepad++.

Anon #2: I'm pretty sure that an experienced unix hacker can totally crush me when it comes to text editing and breezing through tools. I've seen people using VIM and I'm impressed. I'm not saying that you can't be productive in Unix.

I personally hate it because you have to be an expert in order to be any productive in it!

And I don't want to become an expert in tools. I don't care, I honestly know only the basics of VS as well it's not part of my job to be an expert of such things or not the part of the job I enjoy.

For example I like the processing sketch IDE. It's basic, barebones, simple. I won't use it for large project but it doesn't annoy me, I can see the code and play with it and do my stuff without having to care about the tool. Same for drJava, I find that a LOVELY environment for coding.

Also I'm wondering... What the world would be if people invested the same time they do on learning and customizing unix tools loving the M$ counterparts. There are surely some amazing possibilities (again, see metalscroll)... We'll never know... :D

I have this thought also about the 360, most studios that ship on both platforms spend most time optimizing on ps3 and finding very very clever tricks... I wonder if we spent the same time finding clever 360 tips, really using the "xps" stuff or the memout or the tassellator...

Marek: yep some people told me about QT Creator. I have to give it a try.

Haha, yes this has turned into a long thread.





I do think VS is a pretty decent dev environment, and liked it OK back when I used it. I'm a big emacs nerd these days though, so I felt kind of compelled to spread the gospel :p

On maybe a more useful note. When I transitioned to Linux from Windows development, I didn't go straight to pure emacs.

For a while I used Visual Slickedit, which is a multiplatform commercial editor more similar in design to VS. Actually, it predates VS, and I believe microsoft used to use it internally before their developed VS.

I think that is a good transition editor. I switched back and forth between emacs and that for a while. Once I got more comfortable in emacs, I eventually stuck with it full time. However, I still recommend slickedit to people transitioning from Windows to Linux development.

Even though I spend a great deal of my work time in front of VIM (and used to use Emacs before it), I can't really disagree with DEADC0DE points. GVIM maybe quicker to adopt than VIM alone, but "perverts" the UI philosophy (which, given how much productive it can be, is one of the main reason to use VIM in the first place). Emacs is even less "visual". Both programs are "just" extensible editors and require massive amounts of customization before they can become complete IDEs.




Much has yet to be seen in the field of editor UIs. Code Bubbles is a nice attempt to rethink the editor paradigm. I'd like to see even more experimental UIs for editors...

http://www.cs.brown.edu/people/acb/codebubbles_site.htm

--

Giuliano

Giuliano: yep, codebubbles is a nice example of how code editing could evolve if we stopped thinking in terms of pure textual environments. I think there is a lot to explore there.

Linus *totally* gave him what he deserved!

Christer: you know how much I agree that C++ is ugly, but come on...






Come on! A random guy comes and asks a question, surely not a smart move to make a critique on the fundamental choice of a project when you don't know anything about it (for his own admission) but he didn't say anything outrageous...

He could have been just ignored. Or you could have replied if you wanted to take the effort explaining why you don't like C++. Instead he first attacks the guy and then the strongest reason he throws at him is that C++ programmers are substandard... And this guy is the guy in charge of the biggest and most famous opensource project? Jesus...

Then about GIT. I understand GIT is made for the linux kernel and works wonderfully for it, so it's the perfect tool for the job, congratulations. But it annoys me how cocky Linus is when he presents GIT and says that all the other source control systems are crap. GIT is great for linux but it's retarded for many other jobs.

It gets incredibly slow with big depots, and that is simply unacceptable in many situations, so I think in general he should not brag so much...

Last but not least it might be that I'm an arrogant prick myself, so I really hate to find people that are equally or more arrogant than me :D

@Angelo:



I'm reading Dmity's post like I suppose Linus read it. 1. He's an ignorant idiot, as evidenced by his comments. 2. He has nothing whatsoever to do with the project, but behaves like his opinion should somehow matter. 3. He's a prick.

So Linus ripped the guy a new one - well-deservedly so! I would have too, if Git was my project.

Ultimately, at the end of the day, ignoring the verbiage, Linus is right and the other guy is wrong.

Christer: I agree. In fact an arrogant prick can be right! Being right and being a jerk often go together. I know because often I'm not that nice person I should be too, and I think I would be worse if I was leading an opensource project where most of the interaction with other people happens via internet, and not in person. People tend to be worse over the net. At least I'm self aware of the problem :D

Problem with your post is that you leave the impression that you are a so good programmer that you can easily judge any competent and valuable engineer with a one-liner. Fundamentally, when Linus does something like that, it is just funny.



Problem you do not have such a reputation to do that in a funny way. Therefore, the post just appears as a random rant from a random guy. Just like persons reading tabloids and making useless commments about the guys they see in the paper.

As some point, this post is just sad.

Anon: I really don't care much about this Linus thing.





Obviously my personal opinion about him is not due only to that thread I linked.

But it doesn't really matter I don't think I wrote a rant about a person nor I did want to write one.

Actually let's do this, as I really hate people focusing on the Linus part, I'll go and delete it.

Not really worth for me commenting on the issue further, I would care even having a flame about something I really feel important, but not about this.

I'm curious where the idea that Linux is a 'mediocre kernel' comes from?





I am not a kernel engineer, but there are a whole lot of things that the Linux kernel does better than Windows.

Some of it is due to the Unix architecture and so they focus on different aspects of performance than the Windows guys, but I can't think of one thing that the Windows kernel does better than Linux.

I don't know a great deal of the OS X kernel, so I'm not even going to comment on that.

But claiming the Linux kernel is 'mediocre' seems pretty biased and uninformed. Unless you can back that up?

Kid: my impression from what you write is that you are not referring to the kernel architecture but to some os features. You should have a look at the windows nt kernel design, you'll find it interesting.

Still, could you be more specific? Since you say it is mediocre, why is it mediocre?

By the way, there are only 5 windows HPC in the top 500 supercomputer:





http://www.top500.org/stats/list/36/os

410 are linux.

Why people are not using such a great kernel that NT is?

Maybe all of them are just totally nuts. Also, we may also help google switching from Linux to another OS for their android.

It is so badly mediocre.

Also let's help kernel guys switching to perforce. I am pretty sure that 2,000 developpers who share the same code base will be happy to do so. Perforce is so fast to transfer 1GB binaries. This will definitely help them. I heard the linux kernel is only one big c file of 1GB. Damn, stupid linux nerds, they do not know they can use Makefiles.

Anon/kid: i'm aware that git works well for linux kernel developers. I'm also aware of the top 500 and i don't think these people are stupid. You shouldn,t assume that i am either.





As i don't think gamedevs are stupid as they use c++ even if i hate it and i think its fairly retarded. Don't equate success with quality.

I do't really care to go further in this thread as it seems that its beciming quickly a fanboy matter. I suggested to have a look at the NT kernel not to say that windows is better than linux (in practice this might or might not be true dependin on the usage) but as a hint towards a kernel whose desin I think is more interesting.

When linux came out it didn't really bring anything to the kernel design scene, it was cool because of the license and platform it ran on, not because of its innovative architecture. That's an old topic by the way i.e. http://oreilly.com/catalog/opensources/book/appa.html

So i wrote "mediocre" as when i studied it i didn't find anything too exciting about it. That's all. And i mean it, i won't go further in this discussion, sorry.

(typed on an ipad, many spelling mistakes)

Hmmm. Purely random thoughts based on random articles found on the internet. The debate between Thorval and Tannenbaum? Come on, this is 16 years old.




Damn, it seems you suffered so much on Linux that you spent your time finding some arguments on the net to illustrate how much it is bad before even taking some time coding on it.

Poor and hateful post based on nothing.

Rendering related posts were OK. But, still unsubscribe.

lol, bye

Typing is much more important to programming than most programmers realize. I find it annoying when I know exactly what I want to express but I can't just let it flow. It's not about gaining time with faster input (that's a side bonus), it's about not breaking your focus.







If you watch an intermediate (not expert) vim user, it will immediately be obvious to you how the mundane boilerplate code writing is dealt with much faster and in a much less distracting manner.

The cool thing with vim is you also end up moving around text with a programmer's mindset. :)

It is better than you think, and the integration aspect of Visual Studio gives you less than you think.

There is a lot more mundane text-moving involved in programming than we care to admit. An editor is an investment, it doesn't pay off right away. The cool thing with vim users is they won't lie to you, vim has a brutal learning curve.

Visual Studio is a decent editor and a decent debugger (ProDG on ps3 is much better debugger). There is nothing wrong with settling for it, but don't rise programming to such nobility status that efficient text input is considered unimportant! The best programmers don't just architect, they implement, and implementation means moving text around! It's part of your workflow, and you should seek to improve it just like any other part.

Just in the same way, if you've never used the unix command line tools such as grep, sed, cut, and some minimum bash scripting, etc, I highly suggest investing some time in it. They are a very worth while investment.

Anon: we actually sort of agree. I said that VIM is very cool to do some text operations once you learn it. I've seen people being productive with it and I can understand why it's cool.



I said that programming is not about typing text, maybe I should not have generalized so much. I don't care about how fast I type text, and I most of my day I'm not typing text. Most of my day I'm not even at my desk if I'm really solving hard problems.

Also, even if VIM is indeed nice once you learn it there is no justification for it to be so unfriendly to the new user. A program that requires to open the manual just to close it (or to open the manual! or to save a file) is something I won't consider using. It might be the best thing in the world but it hates me (as a new user) and I hate it back.

Opening the manual to save, true, the first time I opened vim I had to kill my terminal window to close it. :) But once you are done with that you understand everything else. With tools it is sometimes important to get past the first impression if it can be useful to you (not saying gvim is for you).





Another advantage is that your plugins don't rely on being able to generate a visualstudio solution. I find that useful when browsing various source code (including their build scripts, shaders, etc) and quickly setup tags + filetags for everything. So it isn't just for typing, but also for quickly browsing code.

Having said this, it is only useful when typing or browsing code, and it is true that a lot of the problems we solve in games require thinking without a single keystroke involved. But at the same time, I like to get the typing part of work as streamlined as possible!

It doesn't have to be vim though. The point is simply that an editor is a tool like any other and you should seek to get the best tool possible!

P.S: don't want to get too besides the point, but gvim has an "okay" gui interface that will at least allow you to save without reading a manual!

Post a Comment