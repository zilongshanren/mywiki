---
title: 'Codebender: physical programming on the web – a WebFWD project – Mozilla Hacks
  - the Web developer blog'
url: https://hacks.mozilla.org/2012/11/codebender-physical-programming-on-the-web-a-webfwd-project/
author: Tzikis
published: '2012-11-27'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

## What is codebender? What problem does it solve?

Whereas the cloud-based, software-as-a-service development has made it easy to develop by reading some tutorials and start hacking, physical computing is lacking far behind. This used to be in part due to the difficulty of designing hardware, but platforms such as the [Arduino](http://arduino.cc) have made this a thing of the past. Instead of looking for the right components (out of thousands) and trying to connect them without frying any, there’s a large number of circuits designed to work great with each other.

We still have a long way to go, though.

Unfortunately, most of the tools still live in the 90s. New users have to install unintuitive applications or various command-line tools and platform-specific programs. That’s where [codebender](http://codebender.cc) comes in. It is an embedded development platform with an emphasis on the Arduino and it’s completely web-based, so you don’t have to install, manage and update anything. Essentially, we are bringing physical programming and the physical world to the cloud.

## New development tools for the embedded software developers

As I mentioned, we start by being completely cloud-based. This essentially starts with storing your code on the cloud, and we also store various settings, libraries and hardware configurations as well. We’re working on storing additional info like circuit schematics and images of the final products as well. So instead of having all these resources scattered around, every bit of your project is bundled together.

This makes even more sense when coupled with our collaborative and social tools. If you want to build something that’s already out there, you don’t need to reinvent the wheel. You just clone an existing project, and you get the code, the schematics, the instructions and anything else you might need.

On the coding front, we’re bringing syntax highlighting, indentation, auto-formatting, and soon, code completion. And since you’re bound to make a mistake, we’re topping it up with a state-of-the-art compile output, that lets you identify the issues faster and easier.

Our next plans are, of course, some kind of versioning, and integration with tools like [GitHub](http://github.com), [Dropbox](http://dropbox.com), etc. Further down the road, we plan to add more collaboration tools to promote the exchange of knowledge and ideas between users. Things like group projects and project discussions for example.

## The ultimate goal is to empower people to build more

We aim to promote the maker and hacker culture and get more and more people to look at the world as something to be hacked, modified and transformed. We strongly believe in the open-source ideals and in constructing/developing stuff rather than consuming endlessly. It is important for people to realize their ability to interact with their environment and better their everyday lives (or just build cool stuff) without being professional software/hardware engineers and we hope codebender will help them do that. This is our reason to get up in the morning (and stay up until the morning).

We also think codebender is a valuable tool in a seasoned developer’s toolkit and a welcoming place for the newcomers that doesn’t scare them off, but rather guides them into the exciting world of physical hacking. In that sense, we want codebender to evolve into a community driven hub of exchanging ideas and knowledge with a diverse audience of makers, developers/engineers, instructors and artists actively participating in what, in our opinion, will be the future of programming embedded devices.

## Our open source projects

We’ve released a lot of open source projects in the past, both personally and as a team. As far as codebender goes, we’re taking care to design the whole system as a number of independent subsystems. So we have released the [cloud compiler](https://github.com/codebendercc/compiler), the [cloud uploader](https://github.com/codebendercc/cloud-uploader) which allows you to program your embedded devices remotely through the network (TFTP-only for now but other protocols coming soon), the [device firmware](https://github.com/codebendercc/Ariadne-Bootloader) (bootloader) which adds remote network programming support to Arduino, the [browser plugin](https://github.com/codebendercc/npapiPlugins) which allows your browser to communicate with your programmable usb devices, and the code for the [website](https://github.com/codebendercc/codebender.cc) itself. It’s all open source.

Want to get a better idea of how these projects are use and how they all fit together? Then watch this short screencast:

[codebender tutorial](http://vimeo.com/54210291) from [codebender](http://vimeo.com/user14870685) on [Vimeo](http://vimeo.com).

## We also use a lot of other open source projects, and contribute back

On the front-end, we use [jQuery](http://jquery.com/), the venerable javascript library, [Twitter’s Bootstrap](http://twitter.github.com/bootstrap/) for the fancy UI stuff, the [Ace](http://ace.ajax.org) editor, which is an awesome pure HTML5 editor and [beautify.js](http://jsbeautifier.org/) for auto-formatting code.

On the backend, we use [Symfony 2](http://symfony.com/) for the website and store user’s info and projects on [MySQL](http://www.mysql.com/) and [MongoDB](http://www.mongodb.org/) respectively. As for the compiler, we use [gcc-avr](http://www.nongnu.org/avr-libc/), the GCC port for Atmel’s AVR architecture to build the binaries, but we use the state of the art [Clang](http://clang.llvm.org/) C/C++ compiler to perform advanced syntax analysis. Clang is awesome in that it provides really great error output. Here’s a good example (prepare for I-love-Clang-it-is-awesome rant):

`#include `
int myfunc(float first, float second)
{
return 0;
}
int main(void)
{
int variable1, variable2;
if(variable1 = variablr2)
{
printf("hello guys")
}
myfunc(variable1);
myfunc((float) variable1,);
myfunc((float) variable1, &variable2);
}

Let’s explain the errors. First of all, we have a typo (“variablr2” instead of “variable2”) on line 11. Next, we forgot to add the infamous semicolon on line 14. And finally, on lines 15-17, we are calling myfunc() in 3 wrong ways.

Here’s what gcc has to say about this:

```
test.c: In function ‘main’:
test.c:11: error: ‘variablr2’ undeclared (first use in this function)
test.c:11: error: (Each undeclared identifier is reported only once
test.c:11: error: for each function it appears in.)
test.c:14: error: expected ‘;’ before ‘}’ token
test.c:15: error: too few arguments to function ‘myfunc’
test.c:16: error: expected expression before ‘)’ token
test.c:17: error: incompatible type for argument 2 of ‘myfunc’
```

Pretty decent, right? It finds all the errors, and is kind of helpful in some cases. For example, we can infer that the error in line 11 is a typo, we know the error in line 14 is a forgotten semicolon (except it’s really on line 13), and the errors for lines 15 and 17 do give us some hints. The error report for line 15 is slightly less stellar since there are two closing parentheses, but that’s because of the casting and it won’t take long to figure our the issue (most of the times).

Let’s see what clang has to say about it:

```
if(variable1 = variablr2)
^~~~~~~~~
variable2
test.c:10:17: note: 'variable2' declared here
int variable1, variable2;
^
test.c:11:15: warning: using the result of an assignment as a condition without parentheses [-Wparentheses]
if(variable1 = variablr2)
~~~~~~~~~~^~~~~~~~~~~
test.c:11:15: note: place parentheses around the assignment to silence this warning
if(variable1 = variablr2)
^
( )
test.c:11:15: note: use '==' to turn this assignment into an equality comparison
if(variable1 = variablr2)
^
==
test.c:13:23: error: expected ';' after expression
printf("hello guys")
^
;
test.c:15:18: error: too few arguments to function call, expected 2, have 1
myfunc(variable1);
~~~~~~ ^
test.c:16:27: error: expected expression
myfunc((float) variable1,);
^
test.c:17:28: error: passing 'int *' to parameter of incompatible type 'float'
myfunc((float) variable1, &variable2);
^~~~~~~~~~
test.c:3:31: note: passing argument to parameter 'second' here
int myfunc(float first, float second)
^
1 warning and 5 errors generated.
```

This is really much more verbose, but it’s also much more helpful. For starters, Clang recognized that we have a variable with a really similar name, and suggests that. Not only that, but it assumes that’s what we meant in the first place, and carries on. It’s not uncommon to get 100 false errors from gcc and have them all disappear when you fix the first one. Clangs assumptions greatly help in that, but it would take a huge example to show that.

Next, we have a warning. One of the most common mistakes both rookies and seasoned developers do is the assignment operator instead of the equality on (“=” instead of “==”). You probably didn’t notice, did you? I thought so :) So, Clang will warn you if you assign inside if() statements. Don’t worry, if you do want to assign, you can either wrap that in another parenthesis (which has no effect in your code) or you can silence these warnings altogether.

It will also give you a more precise report on the forgotten semicolon of line 13, but that’s a minor improvement. The real fun starts in lines 15-17. The error report on line 15 is quite better, since it gives us the number of arguments needed. Line 16 is more or less the same, but line 17 is a nice improvement. Not only does it state the nature of the error, it also gives us the type of the parameter we are passing, the expected type, and the prototype of the function! Now that’s the kind of stuff people like!

## Users First

If I would like to end with something, that would be it. You do know the “customer is always right” motto, but it goes way beyond that. In this era, it’s really about the user. If you build something, make sure the people who use it (for example, in the case of a library, other developers) like it, and figure out what they need. I always say, if you’re going to make something, make something people are eager to use every day. Not something they use out of necessity..

## About
[
tzikis ](http://tzikis.com)

I'm a student at the Computer Engineering and Informatics Department in Patras, Greece. When I'm not studying (aka all the time), I like to develop FOSS projects and promote the Open Source hardware & software movement. I also work as a researcher at the Computer Technology Institute and Press "Diofantus", and I'm the co-founder of P-Space, our local hackerspace in Patras, organizer of the local Patras LUG, and lately, lead developer of codebender, a web-based IDE and collaboration platform for makers.

## 2 comments

DaveNovember 27th, 2012 at 03:30tzikisNovember 27th, 2012 at 13:49