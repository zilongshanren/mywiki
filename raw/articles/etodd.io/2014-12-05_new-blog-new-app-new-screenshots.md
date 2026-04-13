---
title: New blog, new app, new screenshots
url: https://etodd.io/2014/12/05/new-blog-new-app-new-screens/
published: '2014-12-05'
source_blog: Evan Todd
source_site: https://etodd.io/
category: game programming
fetched: '2026-04-13'
---

# New blog, new app, new screenshots

Lots of stuff going on this week.

### New dev blog

First off, my [website](https://etodd.io/) got a much-needed overhaul. The horrible slowness of Wordpress.com was driving me nuts, so I switched to a custom-built site.

I used [Jekyll](http://jekyllrb.com), which is a static site generator. It spits out a bunch of HTML files which you can upload to a server, as opposed to Wordpress, which generates fresh HTML every time someone loads your page.

Advantages:

- Absolute control. You can customize the site theme without dealing with mountains of horrible PHP. And I can finally post HTML5 videos.
- You can host your website on
[Amazon S3](http://docs.aws.amazon.com/AmazonS3/latest/dev/WebsiteHosting.html), which is about 50 cents per month, 10x faster than a normal server, and pretty much guaranteed to never go down. Wordpress absolutely crawls in comparison. - Perfect for coders, because you can write articles in raw HTML or Markdown in your favorite text editor, and you can track your site in a Git repository.

Disadvantages:

- No easy way to offer email subscriptions to readers. RSS is easy to set up though.
- Jekyll is written in Ruby and thus has a bunch of annoying dependencies to install. Still, the whole process is definitely easier than setting up a fresh Wordpress install.

Migrating the comments to [Disqus](http://disqus.com/) was super easy. I use [s3_website](https://github.com/laurilehmijoki/s3_website) to deploy the site to S3. It only updates diff'd files, so it only takes a few seconds in most cases.

Overall I recommend it if you're a coder.

### New app

I got hired this summer to do a mobile game as part of a franchise tie-in. The game is finally out today [for free on Android.](https://play.google.com/store/apps/details?id=com.EndWorld.Shine)

Here's some (raw, uncut) gameplay footage:

### grepr patch

[grepr](http://et1337.itch.io/grepr) has garnered a modest but promising amount of attention. Most notably, iDubbbzTV had some great things to say about it. (warning: language)

I mostly agreed with his bigger complaints, so I made a few tweaks:

- The terminal menu is now more simple and straightforward to operate
- The enemy AWK drone is now larger and easier to spot
- The third level, where the enemy AWK first appears, is now greatly simplified
- Some glitchiness pertaining to the data node collision volume is now fixed

More importantly, the game now runs on Linux! It's 64-bit only at the moment, but everything seems to run just fine. If the game glitches on you, make sure you have libsdl2-2.0.0 installed.

### New screens

Amidst all this craziness you might think I've abandoned Lemma. And you'd be wrong. Here are some fresh new screens:

![](../../assets/0f4f108f8951555b.jpg)


![](../../assets/0f4f108f8951555b.jpg)

I also fleshed out a whole ton of writing:

![](../../assets/3b50f0758e094c2b.png)

So yeah, lots of stuff happening. Stay tuned.

That's it for this week. Thanks for reading!