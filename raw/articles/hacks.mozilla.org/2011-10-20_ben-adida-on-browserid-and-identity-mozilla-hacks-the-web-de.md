---
title: Ben Adida on BrowserID and identity – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2011/10/ben-adida-on-browserid-and-identity/
author: Tristan Nitot
published: '2011-10-20'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

This is the second installment of Mission:Mozilla, a series of interviews that link Mozillians, the technology they produce and the Mozilla mission. Today Ben Adida is in the hot seat to discuss [BrowserID](https://browserid.org/), Mozilla’s identity initiative.

*Tristan Nitot – Hi Ben, can you briefly introduce yourself?*

Ben Adida – I’ve been hacking since high school and, since college, I’ve been fascinated with cryptography, security, and controlling my data. I built my first DB-backed web site before cookies. I ran my own IMAP mail server starting in 1997 because no one else was doing it the way I wanted it. I started an open-source web dev shop in 2000, went back to grad school in 2003 to work on secure voting, explored security and privacy of health data at Harvard Med for a few years, and joined Mozilla in March 2011. I’m now Tech Lead on Identity and User Data, and I’m having a blast.

*TN – Oh my… running your own IMAP server in 1997? That’s the kind of thing that gives instant nerd credibility ;-)*

BA – Oh yes, big nerd and proud of it!

*TN – So you’re now with Mozilla, focusing on Identity and User data. Can you update us on what’s Mozilla is doing on these fronts?*

BA – Everyone I talk to within Mozilla realizes that the Open Web depends on more than just the Firefox web browser. People are storing massive quantities of their personal data online, using dozens of services, and an open browser is not enough to ensure that they have true choice, true control, that they can shape the Web to their liking. So we need to be working towards providing user choice in web-based services, too. The first piece of the puzzle is a usable, federated, and distributed identity system. That’s what we’re doing with BrowserID.

*TN – “federated, distributed”, with users having control… Sounds like the original pillars of the Web, right? I mean, as opposed to what we tend to see these days, with identity being concentrated into the hands of very large commercial organizations… How do you plan to achieve this?*

BA – That’s right, distributed/federated *is* the way of the Web, but when you look at today’s identity solutions, most are incredibly centralized, and those that are more distributed in terms of protocol tend to become centralized in implementation because of the so-called NASCAR problem: you get to log in with Google or Yahoo, and if you’re *really* knowledgeable then maybe you can log in with your own Identity Provider. We think we can do better for users and developers in terms of ease of use and adoption.

*TN – And what about privacy?*

BA – We’ve specifically designed BrowserID to reduce the amount of private data that changes hands to the bare minimum required for authentication. For example, in every other web-based identity system today, the site you log into phones home to your identity provider. In the real world, the equivalent is: you check into a hotel, present your ID to confirm your name, and the receptionist calls the issuing government agency and says “Hi, this is the Hyatt San Francisco, Tristan is checking in just now, is that okay?” Why does the government agency or, in the case of a privately issued identifier, the commercial entity, need to know where and when you’re checking in? In the real world, the receptionist just checks the seal on the ID without phoning anyone. BrowserID recreates this more restrained, more privacy-protecting data flow for web logins.

*TN – So how do you manage to get the best of both worlds: user experience and user control?*

BA – First we’re making the browser an important part of the protocol. After all, the browser is the User’s Agent. Isn’t it a little bit silly on today’s Web that you typically have a tab open to your gmail, and then another site asks you to log in with Google or Yahoo? Why can’t the browser help coordinate those two tabs? You’re logged into gmail, of course you have a gmail email address you can use to authenticate! And in the enterprise setting, you’re logged into your company webmail, of course you can authenticate using that enterprise identity! The browser can help reduce user complexity significantly.

*TN – But I could want to use another email address, than the one I use for my Webmail…*

BA – Right, so we’re always going to give users a choice. Users can choose exactly which persona they want to present. And one major BrowserID design point is simply that users understand email addresses as personas. They typically have home and work email addresses, and they don’t use them the same way. If they have a moonlighting job, they often have a separate email address for that. So BrowserID is based on this concept users already understand: logging in is simply delivering an email address to a web site in a way that the web site can easily verify.

*TN – Cool. Say I’m a Web developer that wants to use BrowserID on my site. How hard is that? How much do I have to relinquish control of my users to Mozilla?*

BA – It takes about 5 lines of JavaScript and 10 lines of backend code to integrate BrowserID, and it works today. It’s by far the easiest of the available identity solutions. In the short term, it means you’re relying on Mozilla servers to provide the BrowserID interface and verify users’ email addresses. That said, this is only temporary scaffolding for our distributed system.

*TN – But as BrowserID becomes native in browsers and identity providers appear, this will change?*

BA – We’ve taken great care to design the system so that, as browsers begin to support the BrowserID APIs natively, we can remove our scaffolding and leave standing a truly distributed protocol. Best of all, web sites don’t have to change a line of code for that to happen: as the identity providers and browsers start supporting BrowserID, our scaffolding automatically fades away. And let’s say you’re a web developer and you want to stop using BrowserID for whatever reason: just send your users an email with their new password, and you’re done. No other identity system minimizes lock-in this much, for both users and web developers.

*TN – So minimizing lock-in is part of the BrowserID design goals?*

BA – Absolutely! This is part of our mission and [manifesto](https://www.mozilla.org/about/manifesto.en.html). We don’t want to own users, we want to empower them. Mozilla is in a unique position to build this kind of identity system because, as we all like to say, Mozilla answers only to users, and we can leverage Firefox to deploy these pro-user designs.

*TN – Fantastic! What would you recommend to Websites who want to do a test-run on their site? And for users who want to experience BrowserID right away?*

BA – Web developers can check out our [documentation](https://github.com/mozilla/browserid/wiki/How-to-Use-BrowserID-on-Your-Site). Users can check out [http://current.openphoto.me](http://current.openphoto.me/), a very promising distributed photo storage system shepherded by [WebFWD](http://webfwd.org/) that chose BrowserID. Just click the distinctive BrowserID login button to get a taste of the user experience.

*TN – I’m sure our readers will try it right away! Thanks a lot Ben for your time. Long live BrowserID!*

## 9 comments

pdOctober 20th, 2011 at 08:36zoulouOctober 20th, 2011 at 10:37Stephan SokolowOctober 20th, 2011 at 15:07Ben AdidaOctober 20th, 2011 at 18:09Stephan SokolowOctober 21st, 2011 at 00:50Stephan SokolowOctober 21st, 2011 at 00:52Ben AdidaOctober 21st, 2011 at 09:43Stephan SokolowOctober 21st, 2011 at 17:08R StephensJanuary 21st, 2012 at 12:35