---
title: Cooking, Documentation, and WordPress Themes
url: https://allarsblog.com/2013/01/04/cooking-documentation-and-wordpress-themes/
author: Michael Allar
published: '2013-01-04'
source_blog: Allar's Blog
source_site: https://allarsblog.com/
category: graphics
fetched: '2026-04-13'
---

Early this morning I had to cook and upload a build of a project for work which hogged a few hours of potential sleep time this morning, so I decided to work today from home.

For those who don't know, "cooking" refers to a process of the Unreal Engine / UDK that strips away a bunch of useless data and creates a set of files representing a compressed minimum to run your Unreal project, and is what you do should do you want to distribute a build of your project. Depending on the project and the cooking process, this could take some time, especially for uploading.

After that I spent my work hours today documenting some things I can't publicly discuss for a few months but I am quite excited about, however documenting sometimes is a tedious and mundane task, although always great to do.

I've decided to put some personal time into my new web platform I want to launch, which is pretty much a revamp of forecourse.com and of this blog as a launching point for new tutorial content I want to make as well as a rapid game prototyping framework I'd like to build as well. A main part of this new web platform is, obviously, the web side of it, and while I know a little about Python, PHP, and other web languages, I am definitely not experienced enough to easily build what I need. I've decided to struggle through it though and am now in the process of building a WordPress Theme based on an HTML-only based template I bought and getting it ready for dynamically displaying content. After trying to make a set of PHP files from the template myself from scratch, I've decided that first converting it to a WordPress Theme would speed things up as it would give me a framework to step into one part at a time.

I started off with the default WordPress Theme and tried figuring out how to port my template to its style, but then I started googling blank HTML5 WordPress Themes. The first one I found was Bones but after more digging I decided to first tackle the task with the [Roots WordPress Theme](http://www.rootstheme.com/?ref=allarsblog.com). Roots looked like it would solve many of my problems but after trying to work with it, it was clearly too overly complex for me to grasp and I needed something simpler and more non-web-programmer-or-designer friendly.

I decided to go back to Bones and it turned out that it is exactly what I'm looking for. I randomly found a tutorial for Bones that I can't seem to relocate that really only went over basic HTML5/CSS3 properties that for the most part I already knew, but it mentioned that Bones also supports CSS3 via [LESS](http://lesscss.org/?ref=allarsblog.com) and that [WinLess](http://winless.org/?ref=allarsblog.com) is a pretty good Windows GUI client for compiling LESS style sheets. I've used LESS in the past before and was greatly pleased at how it transformed CSS into a more programmer-friendly pseudo-inheritance style system but I've always used a JavaScript script that would compile LESS client-side on pages that used LESS style sheets.

After looking at the Bones LESS style sheets and seeing how they are split into many smaller pieces, I decided that WinLess might be the easier way to go and it would cut the amount of scripts my page would have to load as well. WinLess was a very pleasant surprise and after its set up I'm able to rapidly work with my LESS style sheets and have WinLess auto-magically compile them in the background fast enough so that by the time I make a change and save it to the LESS file, I can alt+tab to my browser and hit F5 and instantly see the newly compiled LESS without relying on a LESS JavaScript include.

After working more with the Bones theme, I pretty much established that to do my WP theme creation and to make this HTML template I bought ready for dynamic content, I would have to re-do all the HTML5/CSS markup myself and just use the bought template more for reference than for source code. It seems like it is working out pretty well as the Bones theme is very easy to follow once you learn how to navigate it and for the first time I have faith I'll be able to complete this endeavor myself.

The same article that introduced me to WinLess also introduced me to [Sublime Text 2](http://www.sublimetext.com/2?ref=allarsblog.com), a multipurpose text editor like [Notepad++](http://notepad-plus-plus.org/?ref=allarsblog.com). I'm a big fan of Notepad++ but out of curiosity I decided to give Sublime Text 2 a go and so far I am absolutely loving it. I don't know about its feasibility to replace Notepad++ for my UnrealScript and other generic script-based editing, but it is definitely my go-to text editor for HTML5 and CSS now when not using [Adobe Dreamweaver](http://www.adobe.com/products/dreamweaver.html?ref=allarsblog.com). Sublime Text 2 is just so very slick and it has this feature called Project Folders which has been amazing.

Lastly, I found myself excited about having to write a blog post today, something I didn't expect. Maybe a post every day will be easier than I thought.