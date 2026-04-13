---
title: Why I chose IP.Board for Cocos2D Central
url: http://www.learn-cocos2d.com/2011/01/chose-ipboard-cocos2d-central/
author: Joe Says
published: '2011-01-10'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

One of my book readers, Jim, asked me an interesting question. Not about the book but about the [Cocos2D Central](http://cocos2d-central.com/) community website that I’ve installed a few weeks ago. I thought the answers to his questions are of interest to others even though it doesn’t exactly fit the Cocos2D theme of this website. Jim was asking:

(1) Why did you choose IP.Board over something like phpbb or vBulletin and (2) after having it for a while, would you recommend it to others?

### (1) Why I chose IP.Board

The initial starting point of my search was the fact that [bbPress sucks](http://bbpress.org/). That’s my professional assessment, believe it or not. Well, no, don’t believe that, it’s actually a quite nice forum if you are already hosting a WordPress website and you want a forum that integrates well and won’t be receiving much traffic. But as I’m sure many can relate, the bbPress forum software doesn’t scale very well.

But more importantly I wanted a forum that is able to factor in popularity and relevance of posts in searches, and searches over all the content (eg. the wiki area) not just posts. One that allows users to subscribe to threads and forums and receive email notifications. One that makes embedding code and media easy using the most common forum syntax bbCode. One that allows to extract the helpful and relevant articles from threads so they don’t become buried in the thread. One that allows attachments and signatures, which users could use to promote their Website, App, Product, themselves and what not. One that integrates well with social networks, one that let’s you like things, tweet posts and allow users to sign up with their existing Twitter, Facebook or OpenID accounts.

### The usual candidates

Primary candidates were of course [vBulletin](http://www.vbulletin.com/) and [phpBB](http://www.phpbb.com/) which I’ve both used in the past. Especially vBulletin was the first one I looked at but then I learned two things: for one it’s a rather expensive one-time payment of $285 for the full publishing suite, and $195 still for only the forum. And then at least two or three users mentioned that their support or the stability of the software recently went south with version 4. That was enough to let me look around for possible alternatives. I can’t say if version 4 is really that bad and the rumors are true, but I haven’t looked back since.

Beginning my search I quickly came across the [Forum Software Reviews](http://www.forum-software.org/) website. This was initially very helpful to find out about all the various options that exist - and wow, the forum software market is crowded indeed. It was also clear that there was almost no “free” option I could seriously consider. The free forums fell off the grid in two or three categories: they either lacked critical features or they had an impressive feature set but oh boy was it ugly to look at and confusing to use. The third category was when “free” wasn’t really free and there was a strong upsell to the commercial version, respectively on the downside having to rely on voluntary support.

The phpBB software was my second choice in line. Oh yes, it’s free and rather complete but, like I said, I worried about support. I also [wasn’t impressed by its look and feel](http://www.phpbb.com/community/viewforum.php?from=submenu&f=46) at all. It’s hard to tell but … I don’t know, it simply looks cheap and noisy to me. I would certainly prefer the admittedly clean and noiseless look of bbPress. I then came across [FreeForums.org](http://www.freeforums.org/) which are offering a polished version of phpBB and they also host it for you for a small fee. But ultimately I was turned off by the fact that it was still phpBB and still ugly, and they are charging for features I don’t feel comfortable paying for. $10 per year for the removal of the Copyright notice in the footer? $5 per month to remove the ads? $30 per year to allow me to use the recovery console? Some features I pay monthly, some every 6 months and the rest yearly? Come on. Give it to me straight. And I want to pay for features I’m getting, not to disable “features” I don’t want and quite honestly, are nothing but a checkbox in their customer database. If that’s the attitude of the company when it comes to selling, how is their attitude towards supporting me going to be? I decided I didn’t want to find out.

### IP.Board to the rescue

A few people mentioned [IP.Board](http://www.invisionpower.com/products/board/) and even though I skipped it at first, and when I checked it out the first time it didn’t seem like a good fit and more likely to be overkill. Still, after coming back to the website several times, I went ahead and [tried it](http://www.invisionpower.com/suite/demo.php). That’s when all the powerful options dawned on me: what if, instead of adding just a forum and integrating it with the Learn Cocos2D website, what if I made something bigger?

That’s also when the idea for the name “Cocos2D Central” and - being prepared for the future - “GameDev Central” came to be. An external community website that eventually would be the backend for the Learn Cocos2D blog. It made me think about moving everything over to IPS, except for the intro and the blog. I would be able to move my store over to IPS. I liked the [IP.Downloads](http://www.invisionpower.com/products/downloads/) product because managing downloads is “blegh” in WordPress. And generally I could do much, much more to build and grow a community with all the neat social features that are built in.

I quickly decided to start with the [Standard 25](http://www.invisionpower.com/hosting/select_package.php) plan for $20 per month. It was minimal risk because there’s no minimum duration you sign up for. And I quickly added IP.Content and then upgraded to Plus 40 because I wanted to be able to use IP.Nexus, the eCommerce addon. I’m now paying $35 per month to Invision Power and gladly so. I couldn’t be happier with their Hosted Community offer. I could have bought the products, installing and administering them myself, but that task seemed daunting and if I learned anything: services that are good are worth paying for. My time is better spent coding than managing the server, website and forum.

### (2) Would I recommend it?

Definitely a resounding yes!

What really blew me away was the level of support given by Invision Power Services Inc. They are the [Zappos](http://www.deliveringhappinessbook.com/) of community software! Both on [their forum](http://community.invisionpower.com/) and via tickets, they respond fast and I haven’t seen a post that didn’t receive a reply. They do make you feel welcome and supported.

There were a few minor hickups. Shortly after signing up Cocos2D Central experienced frequent downtimes from 10 to 45 minutes each, sometimes several times a day. I asked them about that and they were quite forthcoming to answer this question: communities are hosted on virtual servers, so several communities share the same hardware. If a community gets hacked or attacked or simply flooded with requests ([Slashdot effect](https://en.wikipedia.org/wiki/Slashdot_effect) or a [DOS](https://en.wikipedia.org/wiki/Denial-of-service_attack)) they are moving the affected community to a new server. As I understood it they were in the general process of splitting communities based on the nature of their content, so that those communities more likely to be receiving attacks will be hosted on different servers, so that communities with “regular content” won’t be affected. The downtimes still happen but are now much less frequent and shorter.

How do I know? I monitor the website via [Pingdom](http://www.pingdom.com/), which alerts me via email when Cocos2D Central goes down and when it comes back online, in 5 minute intervals.

So overall, I can certainly recommend the [Invision Power Services](http://www.invisionpower.com/). And just so you know, I wrote this post without any affiliation, I don’t receive any money or other benefits from them for writing this. I’m simply a fan and hopefully for a long time I will be a very happy customer too.

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

That downtime is extremely scary and I’m shocked that you are ok with it. There are numerous studies published regarding online communities and one of the most important things is the uptime… If your forum is down when a new or even ‘newer’ user tries to visit you lose them the vast majority of the time. It was shown that even regular members will start to abandon a community due to downtime once they find an alternative.

I do really appreciate your review though and keep the posts coming! It just tells me to keep with the other packages and hosting them on E3 or Rackspace where we see virtually no downtime at all.

I was very worried when the downtimes happened so frequently during the first two weeks. One reason why I started monitoring it with Pingdom. The downtimes were because of extensively moving communities to new servers. They are rare now.

Nice post. We are not just users of vBulletin; we worked on some high profile vBulletin sites and on dozens of smaller communities as developers. I think few teams have had the level of professional experience we had with the platform. We made customizations that are still powering some of the most popular vBulletin sites, like sportscardforums.com.

Yet, after 4-5 years of work on the platform, vB4 came and it changed completely our idea on the software. We were hoping that with the new MVC framework, development would have been a pleasure, but were we wrong!

Starting from version 4.0.0 which was the first “gold” release but that was actually just a rough beta, each following release included between 300 and 400 bug fixes, while introducing new bugs. Changes to styles and backend made it so that early adopters had to redo some of their customization at each sub-release. Security issues that one would not find in any decent software started spreading also to the usually very stable and secure vB 3.8.6 (I am speaking of a bug were you were able to search for full database information by simply searching for a term in the FAQ - apparently, a developer forgot the code there; imagine what this caused on shared hosting environments). Non-documented changes in the structure of the cookie prefix caused widespread login and logout issues in thousands of forums. And so on, and on. From a developer perspective, the fact that a framework of great, great complexity and dubious standardization did not have a decent documentation after 6 months from the release of vB 4.0 (and that even today, it has a very poor documentation that cannot compare to Codeigniter or WordPress) is also reason enough to question what the guys behind the product are thinking. The fact there is no official mobile skin yet, and that an iPhone app has been released only the past month and it is still in testing phase makes you wonder if the developers are aware of where the market has been going in the past 3 years.

Speaking of real-life effects on communities, I have worked with clients that had a drop in visitors after the upgrade to vB4. The drop was not simply a SEO thing (actually, vB4 should be more SEO friendly, out of the box, than vB3 - if you were not using vBSEO) but was caused by annoyances that users were experiencing with the switch to the new platform and bugs.

vBulletin will survive thanks to their huge popularity, but not thanks to the quality of their product, for the time being. As a development team that made most of their money working for vBulletin communities, and with dozens of clients in our portfolio, I can tell that I am currently no longer recommending vB4 to my clients. Most of them will stay with vB3 or move to other platforms in the next months.

Oooops, should re-read my stuff. Were you were = where you were