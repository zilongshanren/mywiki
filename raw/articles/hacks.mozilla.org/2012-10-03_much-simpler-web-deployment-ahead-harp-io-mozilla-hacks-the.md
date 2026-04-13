---
title: 'Much simpler web deployment ahead: Harp.io – Mozilla Hacks - the Web developer
  blog'
url: https://hacks.mozilla.org/2012/10/much-simpler-web-deployment-ahead-harp-io/
author: Chris Heilmann
published: '2012-10-03'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

There is a gap in the toolset of aspiring web makers and professional web developers at the moment: simple deployment. While it is easy to create a web site, set up a blog or even build your first HTML5 app, the deployment is still not as easy as it should be in this day and age. In the past we had to FTP, SCP or upload our content to a cloud provider. Nowadays systems like GitHub pages and Dropbox make the “putting things on the web” much easier, but still not quite a task that just happens without us having to put some effort in.

One of the companies in [Mozilla’s WebFWD portfolio](https://webfwd.org/portfolio/), [Harp](http://harp.io) wants to change that. As mentioned on the portfolio:

From the creators of PhoneGap comes a new kind of development platform that leverages the power of Dropbox to give you the easiest development solution imaginable. Simply edit your HTML, CSS, and JavaScript files in your Dropbox folder and the Harp Platform does the rest. Harp is perfect for mobile applications, documentation sites, blogs, and HTML5 presentations. Regardless of your technical acumen, you will find harp to be an indispensable tool.


Harp is built by Rob Ellis, Brock Whitten and Jorge Pedret. In order to learn more about Harp, Chris Heilmann set out to interview Brock about the upcoming product. The [video is available on YouTube](http://www.youtube.com/watch?v=kkT0tB2gpBs
) and following are questions and answers with more details.

**1) The site for harp.io is quite full of good promises, can you tell us in a nutshell what problem you are trying to solve with it?**

Even for simple tasks todays development environments tend to be complex and more removed from the production system than it should be. Harp changes this by making development and production nearly one and the same so you can focus on shipping the next release of your application. It gives you an environment that doesn’t require any maintenance while still being sufficiently robust for most situations.

**2) I’ve seen a lot of similar ideas offered on GitHub and blogs but a lot of them are not that easy to set up for non-developers. Are you trying to fill that gap?**

It’s great to see this trend but removing the setup and maintenance process is the most important part in my opinion and these scripts don’t cover that. I feel people have been waiting for someone to take it to the next level and so thats what we’re doing, giving people a service to trust that takes care of this for them.

**3) It seems to me that what you do relies heavily on Dropbox. What happens if they drastically change their API or approach? Just last year the whole “everything can be a link” replaced the old public folder.**

Harp’s architecture has a clean disconnect from Dropbox and it was actually a somewhat recent decision not to offer Git as an alternate deployment mechanism in Harp. We have decided to start by testing how people respond to using Dropbox but we are prepared to adjustment to adding other tools if need be.

**4) Are you thinking of expanding the idea to also allow for collaboration for designers? Seems to me that just using Dropbox is not working really for that.**

I’m confident Harp will appeal to the designer crowd though we are not making many assumptions until we get feedback from our users during the public beta. I think we have come up with a core offering that will appeal to many people and we will have to wait and see where to take it from there.

**5) What about native app development and packaging? Something like Google’s Yeoman or Twitter’s Bower? Maybe a collaboration with PhoneGap?**

Absolutely. We are heavily exploring these sorts of ideas. Tools like Dropbox open up all sorts of new possibilities of automation in the cloud while still keeping things approachable for beginners. Initially though, we are focused on delivering a core product that will facilitate these sorts of features and partnerships moving forward.

**6) You claim on the site that you also can “Learn to program” with harp. How does that work?**

Harp doesn’t have anything specific for learning to program so that may have been unintentionally misleading. Harp is great though for someone getting started with HTML, CSS, and JavaScript because it removes everything else out of the way. This was an unintended but pleasant side effect.

**7) Will any of your code be available as open source as well? Can people contribute?**

Definitely. Not being a “lock-in” solution is an explicit goal of the Harp Platform and we love writing open source software. We want people to be able to easily run their applications on their own so we will facilitate that use case by opening up these core components. Actually, some of tools we use already are open source and have contributors. For example “[node-dbox](https://github.com/sintaxi/node-dbox)“, our library for speaking to the Dropbox API, is on GitHub and has 260 watchers, 44 forks, and 17 contributors.

## About
[
Chris Heilmann ](http://christianheilmann.com)

Evangelist for HTML5 and open web. Let's fix this!

## 2 comments

Chris MorganOctober 3rd, 2012 at 01:48Robert NymanOctober 3rd, 2012 at 12:31