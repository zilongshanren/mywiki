---
title: People of HTML5 – Divya Manian – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2011/08/people-of-html5-divya-manian/
author: Chris Heilmann
published: '2011-08-30'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

HTML5 needs spokespeople to work. There are a lot of people out there who took on this role, and here at Mozilla we thought it is a good idea to introduce some of them to you with a series of interviews and short videos. The format is simple – we send the experts 10 questions to answer and then do a quick video interview to let them introduce themselves and ask for more detail on some of their answers.

![Divya Manian](../../assets/7b18468ed6249fc2.jpg)

[Divya Manian](http://nimbupani.com/), Web Opener at Opera Software.

Most likely you came across Divya because of her involvement in [HTML5 readiness](http://html5readiness.com/) and [HTML5 Boilerplate](http://html5boilerplate.com/). She is available on Twitter as [@divya](http://twitter.com/divya) and is very much involved in the [CSS standards working group](http://www.w3.org/Style/CSS/members).

As you will see in the interview, Divya is a very pragmatic person when it comes to web standards and has a big passion for educating developers instead of woo-ing them.

## The video interview

You can [see the video on any HTML5 enabled device here](http://vid.ly/3e6t7n) (courtesy of vid.ly).

## 10 Questions for Divya Manian

**1) I feel that right now is a terribly exciting time to be a web developer. Would you agree? What gets you really excited about the new tech we have to play with?**

Definitely. These are exciting times for a web developer. You have new tools to work with almost every other week and what your page is capable of doing has expanded significantly from just delivering static content to enabling real-time media streaming and more. We also have very strong developer tools for each browser: Opera’s Dragonfly, Chrome’s Developer Tools, IE Developer tools in addition to the original trail blazer Firebug. So, it is simultaneously easier and harder to develop for the web.

**2) Back in the days we very much preached separation of concerns as the right way to build web products. HTML is for structure, CSS for look and feel and JavaScript for behaviour. It seems to me that with new technologies this strict separation is blurring a bit. We can generated content in CSS and animate and transform. Some HTML5 elements do nothing without JavaScript (canvas being the big example). Do you think we need to re-visit our best practices?**

Yes, the new features do definitely make you think harder about what you put where, but they do enable a similar separation still, except there are nuances to be aware of when you do the separation.

For example, I would consider animation with JavaScript as a way around the roadblock of not being able to do natively. Browsers are in a better position to control most of the animations that we require (animations for gaming are slightly different ballgame), and doing them natively would get us better performance in the long run.

Personally, for me maintainability and writing something readable and that works well and efficiently is more important than just being driven to compartmentalise your code into HTML/CSS/JS.

And definitely we do need to revisit our best practices every so often because technologies change and our best practices need to change with them, none of them are enshrined in stone and we should keep them relevant to our current set of features/technologies.

**3) In your post “ This revolution needs new revolutionaries” you point out that a lot of the people who drive the web today are not the known luminaries of web design. Do you see a complacency in our advocacy of web standards?**

There are two concerns for me in that post:

1. we are not hearing enough from people who have to deal with creating web applications that work in areas with poor internet connections, censorship, with content in languages that are not popular.

2. There are not enough do-ers who are talking, we are hearing from the same people again and again on similar topics.

I feel strongly about both, but more so about #2 because it impacts every web developer all over the world. There are changes that are occurring that most of them are unaware of, because word does not get out. I think we should do our best to encourage those who do actively seek to create tools, and help fellow web developers or work on interesting challenges for the web to speak and inspire rather than those who are known for their speaking abilities because ultimately we want people to use/work with what is best for the web and not just be informed of what was news 5 years ago.

**4) I found lately that collaboration is getting easier and easier. Tools like github, JSBin and JSFiddle allow you to talk about code and get your readers to fix and change things with you. I did that lately with getting bullet proof 90 degrees turned headlines for example. Why do you think not that many take advantage of that opportunity?**

I would be hesitant to say not many are taking advantage of these tools. They are, but it is true that not everyone is on the bandwagon yet. Github is certainly the most gentle and social introduction to version control you can get, but a lot of web developers are not programmers and have not seen enough pain and horror to know why version control systems are useful. It also requires knowing about what version control systems are, and how to use the command line (a bit), which might be scary for those who are just used to designing with IDEs or TextMate.

**5) CSS seems to be moving in leaps and bounds right now. I for one am very excited about the CSS element property which allows to take screenshots of elements. Are there any lesser known extensions you are fond of and use?**

I am not a big fan of vendor prefixes, and would rather see them quickly unprefixed rather than see more of the prefixes populating stylesheets more and more.

That said, I do like a lot of the new properties that we are experimenting with. We have the obscure tab-size which allows you to control the width of the ‘tab’ character in your content. Pretty useful when you are displaying code.

Opera also introduced the @viewport which will let you set the viewport from within your CSS rather than using meta tags (like <meta name=”viewport” content=”width=320″>). I think viewport belongs to CSS rather than markup, so I would love to see it gain adoption.

Some of the less known properties such as box-sizing (unprefixed in Opera, IE 8+, Safari 5.1+, Chrome, prefixed in Firefox) are also invaluable, as they let you control your box model, which is definitely a revolutionary step from the dark days of trying to work with separate box models.

**6) When we had a longer chat before this interview we discussed that there seems to be a disconnect between what people show on stage at conferences and what people can use these days in their day-to-day jobs. Do you think we should remedy this? More hands-on stuff for people to use now rather than a “look what is possible” approach?**

I think what gets shown on stage is partly entertainment and partly information. I think it is hard to show “real hands-on” stuff without diving deep into it and losing half the audience while doing so. We need a balance for sure.

**7) When writing CSS these days I get very annoyed about having to repeat a lot of code with different browser prefixes. Animations are the worst with all keyframes having to be repeated. Do you use any preprocessors like SASS or LESS? What do you think of that approach**?

Yes, I was/am an early fan of Sass. I have been using it for 2.5 years (a lot less now as I do not deal with as much CSS as I would like to). I certainly think Sass/LESS would be the way to go forward for any web developer right now. They make CSS a lot more powerful and attempt to bring in programming paradigms that CSS sorely lacks. Attempts are being made by Tab Atkins at Google to bring these in a form of a proposal to the CSS WG, and hopefully we should see some form of support in the browser.

I would definitely recommend doing it on the server side though, doing JIT compiling of such code would be such a disaster for performance.

Especially today with so many vendor-prefixed extensions, not using such preprocessors would only cause more harm than not.

**8) You work for Opera, the browser that did implement the most of the HTML5 form elements. Why do you think others are reluctant to do the same? Do you think HTML5 forms are ready for prime time yet?**

It is certainly not true that others are reluctant. Chrome is pretty close to Opera in terms of support, and Firefox and IE10 are have various levels of support too. Yes, HTML5 forms need to be used with polyfills as of the moment, but I cannot wait for full support to land on all browsers so we can get beyond validating forms on the server.

**9) I get a feeling that there is a general fatigue of semantic matters in the HTML5 world. Showcases have no HTML at all or meaningless elements like DIVs as buttons and so on. Is it just not sexy enough when we can rotate things in 3D and make sounds?**

I am tired of semantics, too, really :) I think there is more to HTML5 than discussing when to use a section or a div or an article or an aside. Semantics are good to know about and learn to use, but we have had 15 years of talk about semantics surely we can go beyond that and learn about all the new stuff that occurs in HTML5 that will allow faster/more performant way to provide better experiences for your users.

**10) If you have a friend who just wants to start with web development, what would you tell them to do and go to? What is the most efficient way to get people hit the ground running these days?**

I would ask them to first hit the [Opera Web Curriculum](http://www.w3.org/wiki/Web_Standards_Curriculum) which has now moved to W3C – it is a wiki now so everyone is welcome to contribute to keep it up-to-date and relevant. Then I would highly recommend they refer to explanations and tutorials at the Mozilla Developer Center!

Do you know anyone I should interview for “People of HTML5”? Tell me on Twitter: [@codepo8](http://twitter.com/codepo8)


## About
[
Chris Heilmann ](http://christianheilmann.com)

Evangelist for HTML5 and open web. Let's fix this!

## 30 comments

AshishAugust 30th, 2011 at 06:31John FoliotAugust 30th, 2011 at 11:26Paul IrishAugust 30th, 2011 at 13:34karlSeptember 6th, 2011 at 00:26karlSeptember 6th, 2011 at 00:27JoeyAugust 30th, 2011 at 18:10olivvvAugust 31st, 2011 at 06:30Allan HansonAugust 31st, 2011 at 07:52John FoliotAugust 31st, 2011 at 08:56fpiatAugust 31st, 2011 at 11:20DivyaAugust 31st, 2011 at 15:17Allan HansonSeptember 1st, 2011 at 05:57John FoliotSeptember 1st, 2011 at 06:34Allan HansonSeptember 1st, 2011 at 07:05Allan HansonSeptember 1st, 2011 at 10:47Paul IrishSeptember 1st, 2011 at 10:57Paul IrishSeptember 1st, 2011 at 11:12John FoliotSeptember 1st, 2011 at 13:37Allan HansonSeptember 2nd, 2011 at 19:53Allan HansonSeptember 2nd, 2011 at 20:02Thierry KoblentzSeptember 3rd, 2011 at 09:49John FoliotSeptember 6th, 2011 at 08:56John FoliotSeptember 6th, 2011 at 08:58Thierry KoblentzSeptember 7th, 2011 at 18:28Allan HansonSeptember 5th, 2011 at 12:54Allan HansonSeptember 6th, 2011 at 02:59Thierry KoblentzSeptember 6th, 2011 at 07:58Allan HansonSeptember 6th, 2011 at 10:42Allan HansonSeptember 8th, 2011 at 22:21Allan HansonSeptember 18th, 2011 at 07:01