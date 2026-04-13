---
title: Alex Fowler about DNT and online privacy – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2011/09/alex-fowler-about-dnt-and-online-privacy/
author: Robert Nyman
published: '2011-09-08'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

This is the first of an interview series conducted by Tristan Nitot, long-time Mozilla contributor and one of the founders of Mozilla Europe. Today, Tristan interviews Alex Fowler, Global Privacy and Public policy lead for Mozilla.

*Tristan Nitot – Alex, could you briefly introduce yourself? When did you start working for Mozilla?*

Alex Fowler – I’m Mozilla’s chief privacy friend, where I oversee privacy and policy for the organization. I started here earlier this year in January.

*TN – Does that mean that Mozilla did not care bout privacy before that? ;-)*

AF – No, far from it. Mozilla has a long history of working on privacy through its products and services. It was more that the organization had reached a point where there were many internal activities underway and also that the external discussions on the topic that required a full time team be put in place.

*TN – So you’ve just announced the DNT (Do Not Track) Field Guide. Can you tell us a little more? What is it about? Who should read it and why?*

AF – We’ve written a guide for developers on how to change their web sites to respond to their users/visitors who have enabled DNT in their browsers. Our intention behind the guide is to share some early best practices that other developers have come up with in implementing technical measures for DNT in their systems. The guide includes four case studies and then several tutorials and simple code samples.

*TN – For those who do not yet know what DNT is, can you let us know what it’s about? What problem is Mozilla trying to fix with this?*

AF – Sure. There are two sides to Do Not Track that people should be aware of. First, there’s a broad public debate underway about providing people on-line with a way to opt-out of the unwanted tracking and profiling activities undertaken by myriad players, including advertisers, publishers and data brokers. This debate took off here in the US with a report published by our Federal Trade Commission and it has focused primarily around opting out of behavioral advertising. The recent implementation of the ePrivacy Directive in the EU has now pushed the debate into other parts of the world, as well as other types of tracking. Second, DNT is a browser setting available to users of Firefox, Firefox Mobile, IE9 and Safari that, when enabled, turns on a new HTTP header and begins broadcasting that signal to all first party and third party sites and service providers via the browser. Basically, any one with whom a user is interacting on-line has the ability to see the header and start to respect it. Make sense? From Mozilla’s perspective, we see DNT as an important step towards providing people on-line with control over their on-line experience and the underlying data practices that increasingly shape that experience.

*TN – Yes, this sounds a lot like the third principle of the Mozilla Manifesto: “The Internet should enrich the lives of individual human beings.” Do you think that other browser vendors or other organizations could have led the DNT effort like Mozilla did?*

AF – People are living more of their lives on-line, sharing personal information with friends, family and also the companies enabling these interactions. Mozilla is a nonprofit with a mission to make the web better. We believe it’s important to put users in control of their data and create transparency into where and how their information is handed on-line.

*TN – But do you think people realize that they’re being tracked? Do they actually care?*

AF – These are great questions, Tristan. There is no question that people are increasingly becoming more aware of being tracked. I believe much of the debate over DNT at the policy level could have been avoided if the industry had been more thoughtful in helping people to understand that their activities were being profiled and would show up later in other contexts. Instead, we saw many reports of people being surprised later to see the exact pair of shoes they were looking at on-line at one site appear in ads on another site, for example. In the US, the public policy debate happens because there is a public outcry that crosses broad political demographics and parties. So, that is one indicator of public concern.

*TN – Do people actually take actions to protect their privacy?*

AF – I think we’ve learned over the years that yes, people do act when it is easy to do and the cost of protecting their privacy doesn’t come at some other cost, like breaking their web experience or preventing them from fully participating in those services being utilized by their peers, for instance. Watching people finding and enabling DNT in Firefox has pointed out a few things that we got right. It’s easy to enable and it doesn’t interfere with the user’s browsing experience. Also, it’s narrowly crafted such that DNT doesn’t represent anti-advertising nor anti-commercial values; it’s about privacy. Also, I think it’s been interesting to see that not all opt-outs are created equal. What I mean by that is up until DNT, opt-outs have been under the control of those players who provided them for their users. They controlled all the parameters for where, when and how a user could elect to opt-out of a data handling practice, and they also designed how easy or hard that process could be. The overall effect, from my perspective, was to render these privacy settings mostly meaningless to the user. Putting DNT in the browser and creating a easy-to-set signal changes that dynamic and puts the power back into the people’s hands.

*TN – Do you know if people actually change the preference in their browser to stop being tracked?*

AF – Yes, one of the interesting things about the DNT browser signal is that anyone with a web site can start to count how many of its visitors have DNT turned on. A site just needs to start look for the HTTP header: DNT:1. A study that was released a few weeks ago by Krux Digital measured the privacy options of more than 100 million Firefox users worldwide and found that [usage of DNT in the new version of Firefox has increased to more than 6% of the user-base](http://paidcontent.org/article/419-new-study-shows-use-of-do-not-track-is-on-the-rise/). We will be releasing our own numbers along with the DNT Survival Guide in a few days, but they are mostly in the same ballpark.

*TN – What’s the future of Privacy on the Net?*

AF – A recent publication from the IDC, called the 2011 Digital Universe Study, really highlights for me the future of privacy on-line. The study found that…

- While 75% of on-line information is provided by people, 80% of that information is under the control of businesses, organizations and governments.
- The ability of these entities to appropriately staff, manage and protect this information as it grows exponentially (by a factor of 8 over the next 5 years!) is not keeping pace.

What this tells me is that efforts to put controls into people’s hands over the collection, use, sharing and security of their own personal information on-line is critically important to the future of the web. But also that this issue isn’t going away anytime soon.

*TN – So Mozilla’s role in this field is getting more and more crucial?*

AF – Absolutely! And not just in the context of Firefox or Thunderbird. We have to take our mission into the cloud and start to change industry practices, standards, developer tools, and help revolutionize privacy and data governance for the web.

TN – who, besides Mozilla, can help there?

AF – The challenge before us is certainly huge. First, I do think people need to become much more aware of this issue. Not so much as a “privacy” in the sense of being anonymous online. We need to change the debate to be more about individual information management or data governance. I’m not quite sure, yet, of the right formulation. It feels to me like the public debate does get bogged down in the discussion of the right to privacy. While this is understandable and very important, I think people also need more pragmatic ways to think about and control their day-to-day online interactions. So when a user moves from one social network to her cloud storage music provider to then do some on-line banking, her data settings follow her and are consistently respected by these providers.

*TN – What you’re saying reminds me of Mitchell Baker’s notion of User Sovereignty : people should be able to control their own data and what’s being made on-line with it.*

AF – I think that’s right. Data is everything in the 21st century! Those who control user data will have the power to shape the future of the web.

*TN – Thank you very much Alex for your time, and congratulations for releasing the DNT guide. Keep up the good work on privacy and information management / data ownership!*

AF – My pleasure, Tristan! This was fun; let’s do this again sometime soon!

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.