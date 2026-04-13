---
title: Firebug is now on GitHub – go learn and contribute! – Mozilla Hacks - the Web
  developer blog
url: https://hacks.mozilla.org/2012/03/firebug-is-now-on-github-go-learn-and-contribute/
author: Robert Nyman
published: '2012-03-12'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

There is probably not a single web developer out there who haven’t used [Firebug](http://getfirebug.com/) over the years to debug their own code. And now here’s the next step in the evolution!


## Firebug on GitHub

As outlined by Firebug developer [Jan Odvarko](http://www.softwareishard.com/blog/), who truly knows the ins and outs of Firebug, [Firebug is now available on GitHub](https://github.com/firebug/firebug) which offers you the possibility to learn from and tinker with the code. But not only that, you can create your own version of Firebug, do pull requests, fork it, learn how to develop [Firebug extensions](http://getfirebug.com/wiki/index.php/Firebug_Extensions) and much more (having developed a couple of Firebug extensions myself, this is great news and a good learning ground).

## Working with the Firebug repository

In [Hacking on Firebug](http://www.softwareishard.com/blog/firebug/hacking-on-firebug/), Jan outlines the most common things you can do, like:

- Run Firebug From Source
- Build Firebug XPI
- Push to the Firebug repository

Especially the last one there is really interesting and a very simple way for you to contribute to improving Firebug!

This is, in Jan’s words, how the process looks for pushing to the Firebug repository:

- First, you need a
[GitHub account](http://github.com/signup). It’s simple and all the cool kids are already there. :-) - Fork
[Firebug repository](https://github.com/firebug/firebug)(see how to[fork a repo](http://help.github.com/fork-a-repo/)). - Clone your fork onto your local machine (your URL will be different):
$ git clone git@github.com:janodvarko/firebug.git

- After you made your changes, you can stage/add modified files (e.g.
`firebug.js`

) and commit:$ cd firebug/extension $ git add content/firebug/firebug.js $ git commit -m "New API for my extension"

- Push to your public fork:
$ git push -u origin master

- Send a
[pull request](http://help.github.com/send-pull-requests/). We’ll review your changes and accept if all is OK!

## Go learn and contribute!

Now, what are you waiting for? :-)

Go play around with, learn from and start contributing to Firebug!

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 2 comments

SimonMarch 12th, 2012 at 07:17Robert NymanMarch 12th, 2012 at 13:35