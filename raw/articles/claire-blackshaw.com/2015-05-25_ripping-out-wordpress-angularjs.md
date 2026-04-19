---
title: Ripping out Wordpress & AngularJS
url: https://claire-blackshaw.com/blog/2015/05/go-blog-generate/
author: Claire Blackshaw
published: '2015-05-25'
source_blog: 'Claire Blackshaw: Claire Blackshaw'
source_site: https://claire-blackshaw.com/
category: graphics
fetched: '2026-04-19'
---

![Ripping out Wordpress & AngularJS](../../assets/6db2c283d81210de.jpg)

I don’t have much time to maintain this site my primary requirements are

- Simple to maintain
- Easy to post blogs
- Host about me, cv ect...
- Low Cost
- Easy to index

Previously I was using Wordpress with some custom JS, it was clunky but it worked. Wordpress requires constant updates I was constantly getting comment spam, even with filtering tools. Wordpress worked but it was a nightmare to maintain.

I’m also a big believer in structured data and making data open. Wordpress doesn’t play well with the various structure data formats and it's also very propriety.

I looked at exporting to Squarespace but the export wasn’t fully supported and the price isn’t that cheap, also with the custom tweaks I wanted it didn’t seem worth the extra cost. I looked at Jekyll and a few other options but I wasn’t won over.

This does involve ripping out comments but I don’t believe in their value. With Twitter, Facebook, Google+ and everything else people don’t really need another way to graffiti their opinion on my domain.

At the time I was doing a bunch of AngularJS for work so I thought of just moving everything over to that. It worked well enough. The blog data was exported as XML and run through a small script to convert it to JSON. The website was largely unchanged except that it was fully automatic, and very lightweight.

Though when I started moving structured data into the website and checking it out with google webmaster tools, and other structured data tools it was failing. Yes Google can index dynamic websites but not every site can. Also to fully support google indexing with NodeJS you have to escape hash content. Which long story short means generating a bunch of static version of the site to point the crawler at. Which honestly is almost as much work as just statically generating the site in the first place.

I was fed up and left it for a month or so because work was taking over and technically the site was functional. By the time I got back to looking at it I had got angry at NodeJS, AngularJS and javascript in general due to certain production nightmares at work, which I will go into another time. We are moving over some of our tools to Go, look at the templating facilities in Go and generally how easy it is to write good command line tools I thought about quickly throwing together my own website manager to generate the static content.

I started with the blog which considering it was generated dynamically by javascript it was trivial to move over to Go. This step went pretty much without a hitch. The next step was moving it into a root template. I started with using sub templates but I get getting processing errors I couldn’t overcome. So I moved it to a two step process and this did the trick.

The category pages were a bit harder but once I remember memory is cheap I just generated a static page for every category. I may move this over to a more dynamic system in time when polymer and components are more production stable. Though for now I’m happy with the result.

The last step was moving over the other pages. I’m not 100% happy with everything. The schema and h-card doesn’t play super nice but it works.

Overall I’m much happier with where the site is and it indexes well. Also building new features into it is quite easy. Also it's not taken much time, at all. If you're curious about the code behind the site its all on [github](https://github.com/Kimau/FPWebTool) though I warn you it's built for purpose and not clean at all.