---
title: 'A Web for Everyone: Interviews with Web Practitioners — Chris Coyier – Mozilla
  Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2016/09/a-web-for-everyone-interviews-with-web-practitioners-chris-coyier/
author: Justin Crawford
published: '2016-09-01'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

This is the second in a series of interviews about web compatibility with web practitioners. This week we caught up with Chris Coyier ([@chriscoyier](https://twitter.com/chriscoyier)), prolific web developer and writer behind [CSS-Tricks](https://css-tricks.com/), [Digging Into WordPress](https://digwp.com/), and the [ShopTalk Show](http://shoptalkshow.com/). Chris is one of the founders of the code-snippet demo site [CodePen](http://codepen.io/). He recently published [a book about SVG](https://abookapart.com/products/practical-svg). And now he’s here to talk about web compatibility.

These interviews follow up on our recent article, “[Make the Web Work for Everyone](https://hacks.mozilla.org/make-the-web-work-for-everyone/),” urging developers to build cross-browser compatible web experiences in order to [maximize exposure and market size](https://hacks.mozilla.org/2016/07/make-the-web-work-for-everyone/?utm_source=hacks&utm_medium=article&utm_campaign=compat&utm_content=market_size#other_browser);[ prevent interface bugs](https://hacks.mozilla.org/2016/07/make-the-web-work-for-everyone/?utm_source=hacks&utm_medium=article&utm_campaign=compat&utm_content=drive_users_away#wont_change) that drive users away forever; and [demonstrate professional mastery](https://hacks.mozilla.org/2016/07/make-the-web-work-for-everyone/?utm_source=hacks&utm_medium=article&utm_campaign=compat&utm_content=professional_mastery#craft).

In our first interview, Rachel Andrew said [making a website work across browsers is part of doing her job well](https://hacks.mozilla.org/2016/08/a-web-for-everyone-interviews-with-web-practitioners-rachel-andrew/); she said it can even be “fun and liberating” to use new browser features without breaking the web. Let’s see if Chris Coyier agrees.


![Chris Coyier](../../assets/6e4a4b8679b3c7c2.jpg)


**What does cross-browser compatibility mean to you, Chris?**

I think the term itself is pretty clear: Make stuff work in many different browsers. What those browsers are is certainly different from team to team. Even people whose goal is extreme cross-browser compatibility have limits. Not a lot of people worrying about [Netscape Navigator](https://en.wikipedia.org/wiki/Netscape_Navigator) these days.

**How often do you have to think about cross-browser compatibility?**

I think about it less and less over time I think, but that’s not due to my skill in fixing cross browser issues increasing, its more that browsers are more and more consistent all the time. It’s still pretty easy to waggle fingers at certain inconsistencies, but it would be hard to argue we’re worse off now than we were a few years ago.

Still, I’d say in my life of “actually building stuff” it’s at least a weekly occurrence that some cross-browser consideration needs to happen. And because of working on the content on CSS-Tricks, it’s almost a daily consideration. On a reference site, it’s poor form to talk about browser features without mentioning support.

**Last summer, ****Geoff Graham wrote on CSS Tricks**** that, “It’s rather expected of us that we know how to build websites that can work cross-browser.” Do you think employers and the market really demand this knowledge from developers? Do they expect it of junior devs, or is it more of a senior-level skill?**

Front-end web development is a job. Knowing about, testing for, and fixing cross browser issues is part of that job.


Front-end web development is a job. Knowing about, testing for, and fixing cross browser issues is part of that job. I’m not sure I would expect a junior dev to be super skillful at dealing with cross-browser issues out of the gate, but I would expect them to be open to learning about and dealing with those issues. And at levels beyond junior, it would be a pretty big red flag if a front-end dev could or didn’t want to deal with cross-browser issues.

**What motivates you to make the extra effort to build a cross-browser compatible site?**

Money. People pay for websites that work for them. Here’s a little example: Just last week we were working on some drag-and-drop functionality in a new part of CodePen. Worked great in Chrome, didn’t work in either Firefox or Safari. Tim Holman, one of our front-end devs, had to spend a good part of a day implementing different fixes for both. Good thing we did that before launch, otherwise we surely would have turned some potential customers off.

I don’t feel compelled to fix cross-browser issues because of some holy decree that all experiences be created equal. It comes down to money and customer satisfaction.

**Could anything convince you not to make that effort? What?**

If the cost-benefit guess is way off. If I guess that fixing a cross-browser issue will take a month of development and help 0.1% of customers, I can do some scratchpad math and probably come up with a decision not to do it. Thankfully most issues aren’t that far off.

Even though I do believe “it’s part of the job,” I would also say that it’s a rare developer that really loves doing that kind of work. I can say for myself, I enjoy the moment of solving the problem and closing the ticket, but the journey there can be demoralizing. I’d be cautious about doling out too much of that work to any one dev.

**Have you ever had to convince a client or boss that building a cross-browser compatible site was important? How’d you do it?**

It’s usually the other way around. It’s been me making a site only to send it to a client and have it not work the way I thought it would for them. So it’s them schooling me on cross-browser compatibility.

If I had to be part of a “convincing” session, I’d probably approach it as pragmatically as I could. Let’s look at some data and pick a reasonable spread of browsers to support and hit those targets.

**Can you think of a particularly vexing or interesting compatibility bug you’ve encountered? On what site/product? Did it go live, or did you catch it before it went live? **

One came up for me a few weeks ago. A person wrote in to me telling me that CSS-Tricks was very hard to scroll. I’ve never experienced it before and I was having trouble replicating it. I’m aware that I only have one dev machine and it’s a pretty souped up MacBook Pro, so I wasn’t doubting anything, I just couldn’t replicate it or dig into fixing it.

She sent me videos of the issue, which made it very clear. Chrome was fine. Firefox was fine. It was a special browser she was using called [Pale Moon](https://www.palemoon.org/). It’s only for Windows and it’s not available through my normal “test stuff on Windows” tool.

In reading about the browser a little, it talks about how one of its features is optimizing resource usage. I’m sure that’s a great thing in most cases, but it made me think that if somehow CSS-Tricks was asking for more memory than Pale Moon was willing to give it, that might cause the issue. What is painted up and down the entire page? The background! The background on CSS-Tricks is a combination of CSS gradient and SVG. Not particularly memory-light unfortunately. To test, I had her set a user stylesheet to remove the SVG, and it worked great.

I probably won’t change the current design just for Pale Moon, but in a redesign, it will probably push me toward doing something simpler for the background.

**Did you ever have a specific experience that caused you to take cross-browser compatibility more seriously with your next project?**

I feel like every time I run into a cross browser issue, it pushes me toward doing less and less fancy things. I love experimenting with new stuff, then when it comes to production stuff, my typical thought is, “what’s the most basic tried-and-true way we can pull this off?”

**Are there parts of your process / toolchain / etc. that make it easy for you to incorporate or test for compatibility that you would recommend every web dev incorporate into their own?**

Modern browser developer tools have gotten pretty good at simulating different viewports, connection speeds, and emulating mobile headers, but what they support feature-wise is pretty baked in. I know I open up my iOS Simulator a lot to get a “true look” at Mobile Safari quite a bit, and the fact that I can use Safari’s developer tools to poke around in there is great.

I really dig how [BrowserSync](https://www.browsersync.io/) allows me to open a dev site on a local network with any other device, so I use that a good bit.

My main cross-browser testing tool though is [CrossBrowserTesting.com](https://crossbrowsertesting.com/). It’s pretty amazing.

**What would you tell a brand new developer graduating from a coding bootcamp about cross-browser compatibility?**

There is a certain amount of empathy required in all things web


If your job is front-end development, this stuff is definitely your job. If you roll your eyes at it, it might not be the job for you. There is a certain amount of empathy required in all things web, so if you can’t extend yours to understand that people use different browsers/platforms/version, this does not bode well.


**Tips from Chris’s interview**

- When debugging a compatibility bug, the first step is to completely understand the browser environment it appears in. What OS? What device? What screen size/orientation? What browser? What version?
- If in doubt about whether a feature will work for your audience, look for more “tried and true” ways to implement the necessary functionality.
- Learn to use the advanced features of modern browser developer tools. They can emulate connection speed, screen size, and header differences.


## About
[
Justin Crawford ](http://hoosteeno.com)

Justin Crawford is a product engineer at Mozilla, working on developer marketing and growth. He likes thinking about the future, building things and riding bikes.