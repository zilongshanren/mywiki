---
title: Introducing kyla - part 1
url: https://anteru.net/blog/2016/introducing-kyla-part-1
published: '2016-09-03'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

Hello and welcome - today I’ll be introducing **kyla**, a tool I’ve
been working on for the last 19 months. Before you ask - no, not
continously, often just one evening a week, with month-long breaks
inbetween. So what is kyla, why am I releasing it, and how did this
happen? Glad you asked, because this is what we’re going to cover
today.

## What? How? Why?

So let’s start with what kyla actually is: Kyla is a low-level
installation framework, which takes care of “installing things”. In
the spirit of [scratching your itch](https://anteru.net/blog/2015/04/19/2819/), kyla
exists because I was really fed up with the status quo. Every time I was
downloading and installing something, I wondered: Does this really need
to download everything first before I can select what features I want?
Why is upgrading some complicated - can’t it just fetch what changed?
Why do I have this downloading, extracting, installing phases and not
everything happening at the same time?

It seemed to me that most installers where stuck in design choices done during the pre-web area, and only a few people dared to do a web-first installation system – Steam being the best example. At the same time, I had to deploy my home framework with some data sets, and this was something that just was way harder using the installation systems I’m familiar with – mostly Windows Installer, and NSIS. While they worked fine for “normal” applications, they started to fall apart for my framework which had many files to install (documentation, headers) and also large files (PDBs, sample data). So I wrote an initial “dumb” installer for my framework which focused on easy-to-create installations, and after a year or two of using it, I’ve decided to do it properly - kyla was born.

## Goals

I was striving to fix the shortcomings of Windows Installer, which I considered – and still consider – the most conceptually sound system. However, Windows Installer is not particularly fast; authoring is hard for simple cases, even when using WiX; it isn’t cross-platform; and web installations were never planned for it apparently. What I wanted was the ability to run an installation from a web source, get only the data actually requested, and have at least as good update & configuration capabilities as Windows Installer. In particular, when updating my framework from version A to B, where several hundred header files didn’t change for example, I’d expect an installer to skip touching them even without a dedicated “patch” installer.

The initial design was quite a bit more involved – I was trying to solve installations in general, and that has actually lots of implications like handling conditions, some way to keep track of registry keys, etc. After a couple of months I realized that for a user-mode only installer, none of this is actually required, and I refined the scope. Kyla would be limited to the file handling part only. Any additional logic would have to go into the host application into which kyla would be embedded – like creating shortcuts, or even just keeping track of the last installation directory.

Changing the focus was critical as it led to the super-clean *unified
repository* concept. Instead of having installation sources and targets,
why not treat everything the same way? It’s all about the contents
anyway. With this conceptual change, I could use an installation target
as a source, and all operations could be expressed in terms of
repository changes.

## The repository idea

So what is the repository idea about? Basically, it means that all the data needed for an application is stored in some kind of abstract repository, with a mapping of contents to file paths. Any operation is defined in terms of what it does to the content – file paths are merely a detail and are just passed around. An installation thus becomes adding contents to an empty repository. An upgrade first computes the difference between the contents stored in the source and target repository, and then transfers the missing bits to get both into the same state. A configuration operation adds or removes contents. The installation forlder itself is also treated like a repository as well, with the only difference that the contents happen to be stored in exactly the file layout requested by the user for deployment. How does a patch look like in this world? Well, it’s a repository which doesn’t store the content which is already available in another repository – and it’s easy to generate, because you can simply run an update, find out which contents were requested, and remove those from the update repository. This also implies that the system doesn’t care whether you’re upgrading, downgrading, or even replacing one application with another, as it will do “the right thing” in any case in terms of minimizing data transfers.

With the design set, I did some initial experiements with SQLite to make sure that the required operations would be fast enough. Turns out, SQLite was more than sufficient for my needs. Now nothing was stopping me from getting my hands dirty!

## The implementation

Over the following months, I implemented the required functionality in
various late evening coding sessions. Mostly after work, some on the
weekends, and thanks to the help of a couple of friends with a sane [C
API](https://anteru.net/blog/2016/05/01/3249/) and a user-friendly documentation. Having
some other people to take a look at what you’re doing, who listen to
your explanations and who provide some feedback turned out to be
invaluable, especially given the very long periods of time where this
project wasn’t making any progress. Without you guys, I wouldn’t have
finished this, so thanks again!

## Does it work?

After I was done with the implementation, I validated the whole thing by
installing some large applications like Boost, Qt, and multiple
revisions of the Linux kernel. Compared to existing installers, **kyla**
did exactly what I wanted it to do. Installations only had to fetch the
database before starting, the preparation time to compute the required
operations were super fast, and the installation itself was done in one
step which covered downloading, extracting and verifying the data.

If you want to try for yourself, grab the source from the repository
(either on [github.com/anteru](https://github.com/anteru/kyla) or
[Github](https://github.com/Anteru/kyla)) and check it out. Once
everything was working as expected, it was time to get this out. One of
the major decisions I delayed until the end was which license to use. I
started with GPL as it seemed like a good idea at the time. After all,
this thing was meant for launchers and similar non-critical parts.
However, thinking more about how this could get integrated, and how I
could get people to contribute I settled with the more permissive BSD
license. There’s quite some neat things you can do by deeply
integrating kyla into an application, and GPL would make that
impossible.

## Wrapping up

Just before release, I spent some time to focus on the “small bits”. A proper documentation, some automated testing, a fully automated build, a sample installation, and so on. Again, thanks a lot to everyone who looked at kyla during that time and provided feedback on what to focus!

With that, I’d like to say thanks for staying with me for so long. In the next (and as it looks right now, the last one as well) post of this series we’ll take a look at what’s there, what’s left to do, and how you can contribute!