---
title: Treat Open Source Like a Startup – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2014/05/open-source-marketing-with-velocityjs/
author: Julian Shapiro
published: '2014-05-22'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

## What am I getting myself into?

I was never an open source contributor. I had never even filed a GitHub issue. I considered myself an entrepreneur who simply happened to be technical.

But when the startup I wanted to build needed something that didn’t exist, I followed an unprecedented whim and paused everything I was working on. I pulled a hard left, and I wound up spending three months working full-time on a project that I needed ASAP. Equally as motivating, I knew that other developers needed it too.

So, I switched hats. I became an insanely focused, sleeping-isn’t-allowed developer.

The outcome was an animation engine that drastically improved UI performance and workflow across all devices. See it at [VelocityJS.org](http://VelocityJS.org). It’s a powerful JavaScript tool that rivals the performance of CSS transitions. The trick? Simple: In contrast to jQuery (which was initially released in 2006), I was building an engine that incorporated 2014’s performance best practices from the ground-up. No legacy layers; no bloat. Not a Swiss Army knife; a scalpel.

But, throughout my solitary confinement, I was genuinely concerned that I was building something for a customer base of one — myself.

I eventually came to realize that *switching hats* was actually the wrong approach. I was never supposed to take my startup hat off. (Since normal people don’t wear two hats at once, this is where my metaphor breaks down.)

This is the story of that realization.

## Success

Let’s momentarily jump ahead three months — to the time of Velocity’s release. Pardon me for a moment while I gloat:

- Within three days, Velocity reached the top of Hacker News and programming subreddits a total of four times.
- Within nine days, Velocity amassed
[2400 GitHub stars](http://github.com/julianshapiro/velocity). - Within two weeks, Velocity topped the CodePen charts with multiple demos reaching 10,000 views each (
[codepen.io/rachsmith/pen/Fxuia](http://codepen.io/rachsmith/pen/Fxuia),[codepen.io/okor/pen/fJIEF](http://codepen.io/okor/pen/fJIEF), and[codepen.io/sol0mka/full/kzyjJ](http://codepen.io/sol0mka/full/kzyjJ)). - Countless business, front-end platforms, and web agencies migrated to Velocity (examples: everlane.com, discover.typography.com, apartmentlist.com).

How was this possible? **Because I treated Velocity like I treated my businesses: First, there’s development. That’s 10%. Then, there’s marketing. That’s 90%.**

The perspective shift I underwent midway through development was to commit to the following mantra: However much time I wound up spending on development, I would spend even more time on marketing.

After all, that was the time-split I experienced with my startups. I didn’t see a single reason why it should be different for this project. User acquisition is user acquisition.

Ultimately, if you develop a startup or an open source project intended for public use, and nobody uses it… you failed. It doesn’t matter how clever it was. It doesn’t matter what technical challenges you overcame.

Unfortunately, however, the peculiar reality of OSS growth hacking is that there’s a stigma attached to it: The act of marketing invokes pitching, rubbing shoulders, begging, and bribing. It’s stereotypically personified as an overeager, two-bit hustler wearing a cheap shirt and an even cheaper tie. This clashes with our ideals of open source — which itself is stereotypically personified as a headstrong and idealistic code warrior wearing a cheap shirt and an even cheaper haircut.

I’ll quote GitHub’s Zach Holman to get to the root of the dichotomy, “We like to think that open source is pure; that it’s unadulterated. That marketing an open source project is silly. *That’s* just silly.” – [ZachHolman.com](https://hacks.mozilla.org/ http:/zachholman.com/posts/open-source-marketing/)

To put it bluntly, if you want your open source project to have an impact, you need to step out of your coder bubble. After all, if you build something amazing — and you market it effectively — you’re doing *everyone* a favor. Not just yourself.

The best part is, the more people that know about your work, the more people there are to contribute: Bugs get discovered sooner. Useful features get pitched more often.

And don’t worry — being seen publicly marketing your project doesn’t frame you as an egotistical developer. It frames you as someone who’s passionate. If you take the time to appreciate the fact that more people benefiting from your hard work is a major motivation in your pursuit of open source, then you’ll realize that hustling on behalf of your project fits *exactly *within your pre-existing ideals.

## Open source growth hacking

If you look closely at the current open source landscape, those who most often reach the top of GitHub’s charts are developer figureheads with pre-existing followings, and major companies sharing components of their internal stack.

Looking at this month’s GitHub’s trending chart, the top ranking projects that aren’t educational resources (link collections, tutorials, etc.) include: Pop (*Facebook*), Atom (*GitHub*), Quill (*Salesforce*), Velocity (*Me!*), Mail-in-a-Box (*individual*), Famous (*Famous*), syncthing (*individual*), betty (*individual*), Isomer (*individual*), Bootstrap (*Twitter*), Angular (*Google*), PourOver (*NY Times*).

There’s a fair representation of individuals in there, but it’s typically corporations that dominate open source marketing. The reality, however, is that these corporations employ developers that are no better than you or I. There’s no inherent natural selection driving the popularity of their projects versus yours

Fight to get your project out there. Or sit back and watch the marketing teams of huge companies drown your voice out.

That’s enough with waxing poetic and analyzing the current landscape. Let’s dive into the meaty details: How exactly did I market Velocity?

- I pre-wrote advanced drafts for major web development blogs to consider publishing. By presenting the editors with the full goods upfront — not a pitch, not an outline — I minimized their workload, making it very easy for them to say “yes.” I also made sure to wait until I had enough GitHub stars (from Hacker News coverage, etc.) before pitching. And, most importantly, I had a strong thematic focus for each article: One article was exclusively about performance, and the other was exclusively about UI workflow. In both cases, I minimized the amount of attention spent pitching Velocity, and focused instead on educating readers about the respective topic. Blogs don’t want to publish a giant ad on your project’s behalf; they want content that their readers will thank them for.
- I found out where my power-users were. This advice is common in the startup world: Find your core 1,000 early adopters. It’s no different with open source. Who were the users that craved for a performant animation engine — that would do amazing things with it then show off their exploits to the world without me prompting them to? Web animation demo-sceners — that’s who; the passionate, hard-core devs who explore the intersection of technology and design. And, where do they hang out?
[CodePen.io](http://codepen.io). I reached out to the demoers whose work I greatly admired, and I gave them access to a pre-release version of Velocity. Sure enough, they eventually pumped out something amazing for me to share. - To ensure that new developers always stumble into Velocity.js — even far past the point that I’m still proactively marketing the project — I embedded Velocity into every popular web developer resource that I could find. I pull-requested
[BentoBox.io](http://bentobox.io)and the popular[GitHub repo for front end bookmarks](https://github.com/dypsilon/frontend-dev-bookmarks). I pitched the Treehouse[video blog](https://www.youtube.com/watch?v=ONi6xhy2KTQ)guys. That was all just the start. I also have upcoming codecasts on Velocity’s workflow that code schools will be presenting to their students. Simply put, I made sure that every developer trying to master web animation would at some point hear about Velocity. - Most importantly, I wrote great documentation. To quote GitHub’s Zach Holman once again,
*“Documentation is marketing. The best part is that documentation is linkable. It’s indexable. It’s tweetable. Particularly if you have a nice, coherent one-page overview of your project that lets people jump in and immediately ‘get’ it.”*To expand on Zach’s thoughts, I would frame an open source project’s documentation as what a landing page is to a startup. And make no mistake, you*do*have to pitch; you can’t merely document your API and call it a day. The developers reading your documentation are no different than anyone else; they have limited time, and they need to be convinced that your project is worth considering.

When you have great documentation, posting to Reddit and Hacker News will take care of itself. Developers recognize their peers’ hard work, and they’re happy to spread the word.

On this topic, do you know what the best-kept secret about open source marketing is? That it’s 100x times easier than startup marketing. It’s less work, and you’ll see success with a much greater degree of certainty. Why? Because developers — as compared to the average web user — are more willing to listen, are more willing to retweet, and are generally less skeptical of your marketing claims. Whereas most web users are tired of being pitched with trite social media products, developers are always on the hunt for better tools. Similarly, the web development press is much easier to get a response from than the mainstream tech news press is. The former is scrounging for good content to share with their users whereas the latter is drowning in a sea of half-backed startup pitches.

**Because** of the marketing efforts I put into Velocity, and because of the project’s **ensuing success,** I have become highly motivated **to continue working** on open source projects.

I am only just getting started: Velocity is the first in a trilogy of libraries that aim to change the way we visually interact with software. If you’re interested in staying on top of my UI exploits, say hello on Twitter: @[Shapiro](http://twitter.com/shapiro).

## About
[
Julian Shapiro ](http://julian.com/)

Julian Shapiro is a technical founder. His first startup, NameLayer.com, was acquired by Techstars. His current focus is on UI animation. He's working to bring us one step closer to Minority Report. Read more at Julian.com.

## 2 comments

AdamMay 23rd, 2014 at 15:07SkyulJune 3rd, 2014 at 07:24