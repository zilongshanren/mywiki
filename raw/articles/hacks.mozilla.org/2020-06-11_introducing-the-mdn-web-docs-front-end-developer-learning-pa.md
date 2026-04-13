---
title: Introducing the MDN Web Docs Front-end developer learning pathway – Mozilla
  Hacks - the Web developer blog
url: https://hacks.mozilla.org/2020/06/introducing-the-mdn-web-docs-front-end-developer-learning-pathway/
author: Chris Mills
published: '2020-06-11'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

The [MDN Web Docs Learning Area](https://developer.mozilla.org/en-US/docs/Learn) (LA) was first launched in 2015, with the aim of providing a useful counterpart to the regular MDN reference and guide material. MDN had traditionally been aimed at web professionals, but we were getting regular feedback that a lot of our audience found MDN too difficult to understand, and that it lacked coverage of basic topics.

Fast forward 5 years, and the Learning Area material is well-received. It boasts around 3.5–4 million page views per month; a little under 10% of MDN Web Docs’ monthly web traffic.

At this point, the Learning Area does its job pretty well. A lot of people use it to study client-side web technologies, and its loosely-structured, unopinionated, modular nature makes it easy to pick and choose subjects at your own pace. Teachers like it because it is easy to include in their own courses.

However, at the beginning of the year, this area had two shortcomings that we wanted to improve upon:

- We’d gotten significant feedback that our users wanted a more opinionated, structured approach to learning web development.
- We didn’t include any information on client-side tooling, such as JavaScript frameworks, transformation tools, and deployment tools widely used in the web developer’s workplace.

To remedy these issues, we created the [Front-end developer learning pathway](https://developer.mozilla.org/en-US/docs/Learn/Front-end_web_developer) (FED learning pathway).

## Structured learning

Take a look at the Front-end developer pathway linked above — you’ll see that it provides a clear structure for learning front-end web development. This is our opinion on how you should get started if you want to become a front-end developer. For example, you should really learn vanilla HTML, CSS, and JavaScript before jumping into frameworks and other such tooling. Accessibility should be front and center in all you do. (All Learning Area sections try to follow accessibility best practices as much as possible).

While the included content isn’t completely exhaustive, it delivers the essentials you need, along with the confidence to look up other information on your own.

The pathway starts by clearly stating the subjects taught, prerequisite knowledge, and where to get help. After that, we provide some useful background reading on how to set up a minimal coding environment. This will allow you to work through all the examples you’ll encounter. We explain what web standards are and how web technologies work together, as well as how to learn and get help effectively.

The bulk of the pathway is dedicated to detailed guides covering:

- HTML
- CSS
- JavaScript
- Web forms
- Testing and accessibility
- Modern client-side tooling (which includes client-side JavaScript frameworks)

Throughout the pathway we aim to provide clear direction — where you are now, what you are learning next, and why. We offer enough assessments to provide you with a challenge, and an acknowledgement that you are ready to go on to the next section.

## Tooling

MDN’s aim is to document native web technologies — those supported in browsers. We don’t tend to document tooling built on top of native web technologies because:

- The creators of that tooling tend to produce their own documentation resources. To repeat such content would be a waste of effort, and confusing for the community.
- Libraries and frameworks tend to change much more often than native web technologies. Keeping the documentation up to date would require a lot of effort. Alas, we don’t have the bandwidth to perform regular large-scale testing and updates.
- MDN is seen as a neutral documentation provider. Documenting tooling is seen by many as a departure from neutrality, especially for tooling created by major players such as Facebook or Google.

Therefore, it came as a surprise to some that we were looking to document such tooling. So why did we do it? Well, the word here is **pragmatism**. We want to provide the information people need to build sites and apps on the web. Client-side frameworks and other tools are an unmistakable part of that. It would look foolish to leave out that entire part of the ecosystem. So we opted to provide coverage of a subset of tooling “essentials” — enough information to understand the tools, and use them at a basic level. We aim to provide the confidence to look up more advanced information on your own.

### New *Tools and testing* modules

In the [Tools and testing Learning Area topic](https://developer.mozilla.org/en-US/docs/Learn/Tools_and_testing), we’ve provided the following new modules:

[Understanding client-side web development tools](https://developer.mozilla.org/en-US/docs/Learn/Tools_and_testing/Understanding_client-side_tools): An introduction to the different types of client-side tools that are available, how to use the command line to install and use tools. This section delivers a crash course in package managers. It includes a walkthrough of how to set up and use a typical toolchain, from enhancing your code writing experience to deploying your app.[Understanding client-side JavaScript frameworks](https://developer.mozilla.org/en-US/docs/Learn/Tools_and_testing/Client-side_JavaScript_frameworks): A useful grounding in client-side frameworks, in which we aim to answer questions such as “why use a framework?”, “what problems do they solve?”, and “how do they relate to vanilla JavaScript?” We give the reader a basic tutorial series in some of the most popular frameworks. At the time of writing, this includes[React](https://developer.mozilla.org/en-US/docs/Learn/Tools_and_testing/Client-side_JavaScript_frameworks#React_tutorials),[Ember](https://developer.mozilla.org/en-US/docs/Learn/Tools_and_testing/Client-side_JavaScript_frameworks#Ember_tutorials), and[Vue](https://developer.mozilla.org/en-US/docs/Learn/Tools_and_testing/Client-side_JavaScript_frameworks#Vue_tutorials).[Git and GitHub](https://developer.mozilla.org/en-US/docs/Learn/Tools_and_testing/GitHub): Using links to Github’s guides, we’ve assembled a quickfire guide to Git and GitHub basics, with the intention of writing our own set of guides sometime later on.

## Further work

The intention is not just to stop here and call the FED learning pathway done. We are always interested in improving our material to keep it up to date and make it as useful as possible to aspiring developers. And we are interested in expanding our coverage, if that is what our audience wants. For example, our frameworks tutorials are fairly generic to begin with, to allow us to use them as a test bed, while providing some immediate value to readers.


We don’t want to just copy the material provided by tooling vendors, for reasons given above. Instead we want to listen, to find out what the biggest pain points are in learning front-end web development. We’d like to see where you need more coverage, and expand our material to suit. We would like to cover more client-side JavaScript frameworks (we have already got a Svelte tutorial on the way), provide deeper coverage of other tool types (such as transformation tools, testing frameworks, and static site generators), and other things besides.

## Your feedback please!

To enable us to make more intelligent choices, we would love your help. If you’ve got a strong idea abou tools or web technologies we should cover on MDN Web Docs, or you think some existing learning material needs improvement, please let us know the details! The best ways to do this are:

- Leave a comment on this article.
- Fill in our
(it should only take 5–10 minutes).**questionnaire**

So that draws us to a close. Thank you for reading, and for any feedback you choose to share.

We will use it to help improve our education resources, helping the next generation of web devs learn the skills they need to create a better web of tomorrow.

## About Chris Mills

Chris Mills is a senior tech writer at Mozilla, where he writes docs and demos about open web apps, HTML/CSS/JavaScript, A11y, WebAssembly, and more. He loves tinkering around with web technologies, and gives occasional tech talks at conferences and universities. He used to work for Opera and W3C, and enjoys playing heavy metal drums and drinking good beer. He lives near Manchester, UK, with his good lady and three beautiful children.

## 65 comments

Saboya GustavoJune 11th, 2020 at 14:30Chris MillsJune 12th, 2020 at 03:44C BrennanJune 18th, 2020 at 20:06MohamadJune 11th, 2020 at 16:38Chris MillsJune 12th, 2020 at 03:44Nishant SinghJune 12th, 2020 at 00:02Chris MillsJune 12th, 2020 at 03:44popJune 12th, 2020 at 02:57Chris MillsJune 12th, 2020 at 03:44shabbirJune 12th, 2020 at 03:02Chris MillsJune 12th, 2020 at 03:47JeanJune 12th, 2020 at 08:36Chris MillsJune 12th, 2020 at 10:17BuddhikaJune 12th, 2020 at 11:13RkJune 12th, 2020 at 19:04thel0nerJune 12th, 2020 at 21:12Chris MillsJune 13th, 2020 at 05:41TejJune 12th, 2020 at 22:24Chris MillsJune 13th, 2020 at 05:41gregJune 15th, 2020 at 05:19Andrew AbbottJune 13th, 2020 at 22:43Chris MillsJune 14th, 2020 at 09:01JeretiJune 14th, 2020 at 22:27Chris MillsJune 15th, 2020 at 01:32Yoel TorresJune 15th, 2020 at 00:13Chris MillsJune 15th, 2020 at 01:33Sergo GabuniaJune 15th, 2020 at 11:52Chris MillsJune 16th, 2020 at 00:22Sergo GabuniaJune 17th, 2020 at 06:40sourabh sharmaJune 17th, 2020 at 23:26Chris MillsJune 18th, 2020 at 06:18Sam KimJune 18th, 2020 at 00:46Chris MillsJune 18th, 2020 at 06:23Sam KimJune 18th, 2020 at 20:36Flores PintoJune 18th, 2020 at 03:47Chris MillsJune 18th, 2020 at 06:28Michael WagenerJune 18th, 2020 at 04:46Chris MillsJune 18th, 2020 at 06:33Bernard PalmerJune 18th, 2020 at 05:45Chris MillsJune 18th, 2020 at 06:36Javier Molina RiveroJune 18th, 2020 at 08:32DaveJune 18th, 2020 at 08:34EstuardoJune 18th, 2020 at 08:41Himanshu MauryaJune 18th, 2020 at 08:54Chris MillsJune 18th, 2020 at 09:02Chris JohnsonJune 18th, 2020 at 09:11Chris MillsJune 18th, 2020 at 11:17matjungJune 18th, 2020 at 09:18Chris MillsJune 18th, 2020 at 11:46Mahmoud U.SJune 18th, 2020 at 09:48Chris MillsJune 18th, 2020 at 11:19Peter DelfJune 18th, 2020 at 10:02Chris MillsJune 18th, 2020 at 11:19Hugh MosnoJune 18th, 2020 at 12:47TobiasJune 18th, 2020 at 12:58SpandanJune 18th, 2020 at 13:21Ekejimbe Chijioke SundayJune 18th, 2020 at 14:24Doug DyerJune 18th, 2020 at 16:07ChrisJune 18th, 2020 at 19:57FranderJune 19th, 2020 at 12:14WolfgangJune 20th, 2020 at 08:59Baha HijaziJune 21st, 2020 at 07:57BonghwanJune 23rd, 2020 at 00:47Jai Ganesh PrakasamJune 28th, 2020 at 06:14Sunakshi JainJune 28th, 2020 at 23:53