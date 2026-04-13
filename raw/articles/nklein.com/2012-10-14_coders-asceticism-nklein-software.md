---
title: 'Coder’s Asceticism :: nklein software'
url: http://nklein.com/2012/10/coders-asceticism/
author: Pat
published: '2012-10-14'
source_blog: nklein software
source_site: http://nklein.com
category: game programming
fetched: '2026-04-13'
---

A month or two ago, I watched a bunch of videos of [Uncle Bob](http://en.wikipedia.org/wiki/Robert_Cecil_Martin) speaking at various conferences. He’s thought a lot about what makes code testable and maintainable, and he’s an excellent speaker. I’ve even paid to watch some of his hour-ish videos at his [Clean Coders](http://cleancoders.com) site.

In [Clean Code, Episode 3 – Functions](http://http://www.cleancoders.com/codecast/clean-code-episode-3/show), he makes the case that we should be striving to keep each function under five lines long. So, over the past month or so, I’ve been trying this out in all of my Scala and Lisp endeavors.

Once you get each function down to four lines or fewer, you start running into symbol-proliferation. You pretty much throw out `(LABELS ...)`

and `(FLET ...)`

unless you need the closure (and then try to say that when you can’t that it’s good enough to just keep the subfunctions under five lines and the body under five, too). You create bunches of functions that should never be called anywhere except the one place it’s called now.

### Enter Package Proliferation!

Then, I remembered some Lisp coding style guidelines that I read early this year sometime. Those guidelines advocated having one package for each Lisp file and explicitly making peer files have to import or qualify symbols used from other peer files. This will help me with the symbol-proliferation! Let’s do it!

### Enter File Proliferation!

After two weeks of that, I woke up yesterday morning realizing that I wasn’t getting the full benefit

from this if I was exporting more than one symbol from each package. If keeping each function tiny is Good and limiting a package to one file is Good, then it is certainly Bad to have one file’s package exporting eight different functions.

So, today, I reworked all of the [UNet](http://nklein.com/software/unet/) that I wrote in the last couple of weeks to have one package per file and as few exported symbols per package as possible.

In the interest of testability and modularity, I had broken out a subpackage of UNet called UNet-Sockets that is to be the interface the UNet library uses to interact with sockets. I had realized that I had a file called *methods.lisp* with four different publicly available `(DEFMETHOD ...)`

forms in it. Now, each is in its own file and package. I did the same for various other declarations.

Now, there is a top-level package which uses Tim Bradshaw’s [Conduit Packages](http://www.cliki.net/conduit-packages) to collect all of the symbols meant to be used externally from these packages. If there is an exported function in a package, that is the only exported symbol in that package. If there is an exported generic function declaration in a package, that is the only exported symbol from that package. If there is an exported method implementation in a package, there aren’t any exported symbols from that package. If there is an exported condition in a package, that condition and its accessors are the only exported symbols from that package. If there is an exported class in a package, that class and its accessors are the only exported symbols from that package.

### Example

The top-level package of the *UNET-SOCKETS* system, that defines the interface that UNet will use to access its sockets, consists of just a `(DEFPACKAGE ...)`

form. You can see the full package on [github](https://github.com/nklein/unet/tree/trying-package-per-file) in the *unet-sockets.asd* and the *sockets/* directory.

(:use :cl)

(:extends/including :unet-sockets-interface

#:sockets-interface)

(:extends/including :unet-sockets-base-socket

#:base-socket)

(:extends/including :unet-sockets-hostname-not-found-error

#:hostname-not-found-error

#:hostname-not-found-error-hostname)

(:extends/including :unet-sockets-get-address

#:get-address)

(:extends/including :unet-sockets-address+port-not-available-error

#:address+port-not-available-error

#:address+port-not-available-error-address

#:address+port-not-available-error-port)

(:extends/including :unet-sockets-create-datagram-socket

#:create-datagram-socket)

(:extends/including :unet-sockets-send-datagram

#:send-datagram)

(:extends/including :unet-sockets-poll-datagram

#:poll-datagram))

### Conclusion?

The jury’s still out on this for me. On the one hand, the self-flagellation is an interesting exercise. On the other hand, if I’m going to have to export everything useful and import it in multiple places then I’m taking away some of the [fun](http://nklein.com/2009/02/sapir-whorf-wit-programming-languages/). I feel like I’m maintaining C++ header files to some extent.

I think I’ll keep it up for the UNet project, at least. It makes good documentation to have each exported symbol in a package and file named for that exported symbol. You can open up any file and read the three-to-four line exported function in it. You can see, right there with it, any supporting function it uses that no other files need to use. You can see from the `(DEFPACKAGE ...)`

form at the top where any other supporting functions came from. And nothing else is cluttering up the landscape.

We’ll see if I develop religion on this topic. At the moment, I think it’s eventually going to fall into the *moderation in all things* bucket. Time will tell.

I looked at those guidelines for one package per file, looked at a current project consisting of five packages and 160+ files, and decided not to follow those “modern” guidelines.

Certainly, retrofitting existing code would be a pain. My experiment was starting from empty files. It has merits, but I’m not sure they’re worth the effort.

Frankly, this reads like satire. I don’t know if that was intended…

There was to be a bit of humor, I suppose. It feels like a silly idea, to me. But, I am giving it an honest try. And, there are things that I like about it.

Patrick do you like it for finished products more or during development?

It reads to me like something that is good for a finished product, but not for “exploratory” development.

Uncle Bob’s advice has percolated through the Java world too, no import foo.*! lol

I think it would be a pain to retrofit a package this way. For exploratory coding, it definitely would kill the mood. I’ll probably do exploratory coding in CL-USER for awhile until I’m starting to solidify.

For UNet, I have hammered it out enough on paper and during car trips that I am pretty clear on what I want the globally exported functions to be. There may be some give-and-take in what functions need to be shared under the API level to make it all go.

And, I’m firmly against a “using” line outside of the current file or a Java import foo.*. I want to be able to tell (without the IDE) where each function comes from.

I really don’t understand why such a retrofit would be a pain in Lisp. For God’s sake, it’s Lisp! It ought to be less painful (in the long run, how long I don’t know)to write some Lisp code to introspect the target code and re-write it to those guidelines.

Indeed. And, after reading Sabra’s comment above, I have been considering writing such a restructurer to see how bad it would be for some big packages. I am still stymied by source code comments being ignored by the reader. But, even if I had to make a careful reader, it may be tough to always move comments appropriately in an automated way, but that’s minor.

So what benefit am I actually getting from turning 160 source code files and five packages into 700 source code files and 700 packages? Just the exercise of having carefully looked at each function and determined whether I can structure the program so this particular function is not exported?

I suppose if I was going to try to consider writing a restructurer, I’d start by considering http://ryepup.unwashedmeme.com/blog/2012/01/03/visualizing-call-graphs-in-lisp-using-swank-and-graphviz/ and how to do a traveling saleman’s solution. Maybe when I retire.

The benefit, as I see it, is for someone trying to navigate the code later. You open the api.lisp which conduit-packages all of the library exports. You go to the one you want. You have all of the function and the support functions unique to it right there. You have import lines showing where all non-unique support functions came from. You have meaningfully subsets of symbols to iterate over for internal docs vs. external docs.

Beyond that, I don’t know. Those are the benefits I’d be hoping for. That’s what I’m hoping for in my current endeavor. I still don’t know if it’s worth it. Some of my hopes may fizzle. Some unforseen benefits might emerge. And, what have I got to lose beyond a few extra weeks of development on a personal project I hoped to have done 15 months ago? 🙂

You are going in the wrong direction. Look at literate programming.

Write your code as you would write a book. You only need 1 file.

Write code for people, not for machines.

Include files, makefiles, and the horrible idea of making class names

and filenames the same, are all ideas from the 1970s. They were based on

hardware limitations. For instance, my PDP-11/40 limited files to 1/2 of

available memory (8k). Which meant that a file could only be 4 kilobytes.

Thus was born the ideas of include files, linkage editors with overlays,

segments and segment registers, makefiles, etc. All of this nonsense is now

papered over with IDEs. Uncle Bob is selling you ideas from the 1970s.

I am a big fan of LP.

I don’t have the time/energy/drive to make the LP tools jive with SLIME or generate code someone could look at without the doc.

The file-per-package-with-one-export-per-file thing then just becomes chapter-per-exported-symbol-or-symbol-used-in-more-than-one-chapter. The goal is not to make the compiler happy. The goal is to make the reader not have to look very hard for what she needs.

None of my past LP endeavors have given me something easier to debug/maintain than a grep-friendly source tree.