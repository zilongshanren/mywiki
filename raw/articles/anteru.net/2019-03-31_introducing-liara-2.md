---
title: Introducing liara 2
url: https://anteru.net/blog/2019/introducing-liara-2
published: '2019-03-31'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

Many years ago, I started to work on [liara](https://sh13.net/projects/Liara), a static page generator. The first commit was made in 2013 (same year as the first production page using it went online), and some maintenance work was done in 2015 , but that was about it for liara. If you wonder what happened in 2015, that was around the time I updated [sh13.net](https://sh13.net), which is essentially a project overview page powered by liara.

Back when I started, static page generators were new, and liara used a different design by providing the functionality for a static page generator in form of a library. You could mix and match what bits you needed, but the build loop was completely under the control of the user, somewhat limiting the usefulness for simple projects. Not to mention it only knew full rebuilds, making template development rather painful.

If you’re a long-time reader, you may remember that I [moved to Nikola](https://anteru.net/blog/2016/moving-from-wordpress-to-nikola) in 2016. You might think that would make liara obsolete. Turned out, it worked well for my blog, but not for everything I wanted to do. Don’t get me wrong – [Nikola](https://getnikola.com/) is a great static page generator and framework, but some of the things I had on my list – extensive redirects, incorporating binary content, running other project pages etc. – were not something Nikola was designed for. Time to revisit liara 😊!

## Towards version 2

In early 2019, I decided to completely rewrite liara from the ground up. It would no longer be a library, but rather a full framework, driven by configuration files and templates instead of code. The goal was to make it easy to create something like this very blog you’re reading (and which will hopefully continue to run on liara for many years to come), but at the same time use it for my other pages as well.

Some of the goals I set out were:

- Instant reload of templates. I want to hack on templates with a fast edit & review loop, and rebuilding the whole page is a no-go. A custom web-server would be required.
- Extremely fast handling of static files – my blog contains various binaries (papers, videos, etc.) and I want those to be handled efficiently.
- Fast builds: liara was no slouch, but I wanted something which could rebuild my blog in approximately one second.

With that, hacking started, and over the last few months I developed liara in conjunction with porting SH13.net and my blog over to it. SH13.net is a small project, so there wasn’t much interesting going on there, the blog however with nearly 400 pages of content created some more interesting challenges.

## Blog update

The biggest action item while converting is getting the content. Thankfully, one major advantage of having moved to Nikola was that all my content was text, and thus easy to batch-process. I have everything in source-control, and for conversion, I wrote a few scripts which would process all files and perform some actions.

The biggest change was the move to [Markdown](https://daringfireball.net/projects/markdown/), instead of [reStructuredText](http://docutils.sourceforge.net/rst.html). I do like the strictness of reStructuredText, but the ecosystem has voted and these days Markdown is far more ubiquitous. For the conversion, I used [Pandoc](https://pandoc.org/) and some scripting.

With that out of the door, I used the chance to cleanup and restructure some content “at large”, with the following noteworthy changes:

- Tags have been re-assigned, there are fewer tags now, but overall search using tags should yield better results now.
- All URLs changed, instead of
`/blog/2016/02/23`

, the URLs now contain a slug of the title. If you still have old URLs – don’t worry, redirections are in place so everything will continue working. - Tons of internal and external links have been fixed.

## New release

With the blog, my personal page, and a test project done, I had a good feeling about the state of liara. As no project is complete without a [release](https://anteru.net/blog/2015/scratching-your-itch-side-projects), I spent the last few weeks and days polishing liara to make it release-ready. This mostly consisted of writing the [documentation](https://liara-web.rtfd.io), but also some code refactoring and testing. If you want to give it a try, you can find it on [PyPI](https://pypi.org/project/Liara/) now and install using `pip`

.

And with that, liara 2.0 is now live! Enjoy!