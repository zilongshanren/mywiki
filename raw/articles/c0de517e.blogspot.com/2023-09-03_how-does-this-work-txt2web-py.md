---
title: How does this work? txt2web.py
url: http://c0de517e.blogspot.com/2023/09/how-does-this-work-txt2webpy.html
published: '2023-09-03'
source_blog: C0DE517E
source_site: http://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

**Read the following article here:**


Below you will find a draft version of the post, all images, formatting and links will be missing here as I moved to my new system.


[https://c0de517e.com/001_txt2web.htm](https://c0de517e.com/001_txt2web.htm)This blog is dead! Update your links (and RSS!) to c0de517e.com.Below you will find a draft version of the post, all images, formatting and links will be missing here as I moved to my new system.

(tl;dr: badly)

The common wisdom when starting a personal website nowadays is to go for a static generator. [LINK:https://gohugo.io/ Hugo] seems particularly popular and touted as a simple, fast, no-brainer solution.

OMG! If that's what simplicity looks like these days, we are really off the deep end. Now, I don't want to badmouth what is likely an amazing feat of engineering, I don't know enough about anything to say that... But, tradeoffs, right? Let's not just adopt some tech stack because it's "so hot right now". Right? [LINK:http://c0de517e.blogspot.com/2016/10/over-engineering-root-of-all-evil.html Overengineering is the root of all evil].

[IMG:hot.png]

I had to interact for the first time with hugo for REAC2023, as I was trying to style a bit more our homepage with the graphic design I made this year, and that was enough to persuade me it's not made for my use-cases. I can imagine that if you are running a bigger shop, a "serious" website, handled by professionals, perhaps it makes sense? But for personal use I felt, quite literally, I could be more efficient using raw HTML. And I don't know HTML, at all!

Indeed in most cases for a blog like this, [LINK:https://fabiensanglard.net/html/index.html raw HTML is all you need] (exhibit [LINK:https://motherfuckingwebsite.com/ B]). But I'm a programmer, first and foremost, and thus trained to waste time in futile efforts if they promise vague efficiency improvements "down the line" (perhaps, in the next life).

Bikeshedding, what can go wrong? In all seriousness though, this is a hobby, and so, everything goes. Plus, I love Python, but I don't know much about it (that's probably why I still love it), so more exercise can only help.

From the get go, I had a few requirements. Or anti-requirements, really:

1) I don't want to build a site generator, i.e. my own version of hugo et al. I'll write some code that generates the website, but the code and the website are one and the same, everything hardcoded/ad-hoc for it.

2) I don't want to write "much" code. Ideally I aim at fewer lines in total than the average Hugo configuration/template script.

3) I don't want to use markdown. Markdown is great, everyone loves it, but it's already overengineering for me. I just need plain text, plus the ability to put links and images.

4) I don't want to spin a webserver just to preview a dumb static website! Why that's a requirement is puzzling to me.

5) I want to be able to easily work on my articles anywhere, without having to install anything.

6) No javascript required. Might add some JS in the future for fun stuff, but the website will always work without.

This is actually how I used to write my blog anyways. Most of my posts are textfiles, I don't write in the horrible blogspot editor my drafts, that would be insane. The textfiles are littered with informal "tags" (e.g. "TODO" or "add IMAGE here" etc) that I can search and replace when publishing. So why not just formalize that!

That's about it. "txt2web" is a python script that scans a folder for .txt files, and convert them mechanically to HTML, mostly dealing with adding "br" tags and "nbsp". It prepends a small CSS inline file to them for "styling", and it understands how to make links, add images... and nothing else! Oh, yeah, I can **bold** text too, this is another thing I actually use in my writing.

Then it generates an index file, which is mostly the same flow converting an "index.txt" to web, but appending at the end a list of links to all other pages it found. And because I felt extra-fancy, I also record modification dates, so I can put them next to posts.

Yet, in its simplicity it has a few features that are important to me, and I could not find in "off the shelf" website builders. As of "v0.1":

- It checks links for validity, so I can know if a link expired. Maybe one day I could automatically link via Internet Archive, but I don't know if that's even wise (might confuse google or something?).

- It parses image size so the page does not need to reflow on load. Maybe one day I'll generate thumbnails as well. In general, the pages it generates are the fastest thing you'll ever see on the web.

- It reminds me of leftover "TODO"s in the page.

- The 10-liner CSS I added should correctly support day/night modes, and it should be mobile-friendly.

- It generates a good old RSS feed! I personally use Feedly/Reeder (iOS app) daily, after google killed its reader product.

If you want to check out the code (beware, it's horrible, I always forget how to write good "pythonic" code as I use it rarely), you'll find it [FILE:txt2web.py here.]

Also, for each .htm there should be on the server the source .txt, as I upload everything (the source and the "production" website are one and the same). For example [FILE:001_txt2web.txt]!

Enjoy!

**Appendix:**

What about gopher/the tildeverse/smol-net/permacomputing?

I like the idea. A lot. I believe there is more value to the individuals in being in smaller communities than in "megascale" ones. I believe that there is more value in content that is harder to digest than in the current "junkfood for the brain" homogenized crap we are currently serving.

I suspect Twitter and TikTok "won" because they are exploiting evolutionary biases - which make sense and we have to accept, but that do not necessarily serve us the best anymore. And I suspect that the most value of world-scale anything is extracted by celebrities and advertisers, to have a platform with a wide reach, not by most of the people on the platform.

But, needless to say, this is bigger topic for another time! BTW, if you don't know what I'm talking about, let me save you some google: [LINK:https://tildeverse.org/], [LINK:https://communitywiki.org/static/SmolNet.html], [LINK:https://100r.co/site/uxn.html]

What's relevant to this post is that yes, the fact I have control over the website and I chose a minimalistic, text-based format, would allow me to output to other representations as well... Maybe one day I'll have a gopher page for work-in-progress stuff, for few people who care to lurk those kind of things.

[IMG:libretto.jpg Achievement unlocked?]

[IMG:cafe.jpg Hipster coffee, hipster writing.]

## No comments:

Post a Comment