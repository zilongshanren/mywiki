---
title: People of HTML5 – John Allsopp – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2011/08/people-of-html5-john-allsopp/
author: Jay Patel
published: '2011-08-25'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

HTML5 needs spokespeople to work. There are a lot of people out there who took on this role, and here at Mozilla we thought it is a good idea to introduce some of them to you with a series of interviews and short videos. The format is simple – we send the experts 10 questions to answer and then do a quick video interview to let them introduce themselves and ask for more detail on some of their answers.

![John Allsopp](../../assets/c36146e28876fc45.jpg)

[John Allsopp](http://johnfallsopp.com/), author of [Developing with Web Standards](http://www.amazon.com/Developing-Web-Standards-John-Allsopp/dp/0321646924/ref=sr_1_1?ie=UTF8&s=books&qid=1257918404&sr=8-1) and organiser of the [Webdirections](http://www.webdirections.org/) conferences.

As you will see in the video, John is neither mincing his words nor does he hold back in spreading good messages about the web as a whole and independent of technology. He has been around since connecting to the web meant enduring bleeping noises and has spent quite some time building software and online generators to allow people to build for the web.

He has been very outspoken about the lack of semantic improvement in HTML5 and you can count on him to speak up every time somebody claims that native apps on mobiles will always be better than web standards based apps.

## The video interview

You can [see the video on any HTML5 enabled device here](http://vid.ly/5w5w0p) (courtesy of vid.ly).

## 10 Questions for John Allsopp

**1) You’ve been around this internet thing quite a while and seen a lot of things come and go. What makes you believe in HTML5?**

Well, interestingly I’m probably known by some people for being the anti-HTML5 guy. I’ve been quite [critical in particular of the semantics in HTML5](http://www.alistapart.com/articles/semanticsinhtml5), both about some of the specific decisions made, but more importantly the approach to extending semantics in HTML5.

My particular interest in HTML5 in the broadest sense (so, including CSS3, related extensions to the DOM, geolocation, DAP etc) is seeing the web become an increasingly powerful application platform.

Over the last 20 years or so, we’ve seen the web revolutionise publishing, journalism, and other essentially text based media. This emerging generation of technologies promise to revolutionise much more.

**2) What are the things in HTML5 that still need tweaking in your book? Anything that ails you about the current state of the spec?**

Well, I still think the ball has been dropped when it comes to increasing the semantic richness and expressibility of the language in any genuinely useful way. And I sadly don’t really see anything happening there.

I also think HTML needs to take a leaf from the CSS book – CSS2, a monolithic specification became increasingly bogged down in minutiae, and the failure to finalise it became a kind of running joke.

With CSS3, we saw the modularisation of the specification, with much more rapid innovation, much more experimentation. In truth, it was the experimental CSS3 features that I think ignited the excitement around what we call HTML5, far more than a new DOCTYPE and things like the header element.

The core of the HTML5 specification is really monolithic, and is suffering much the same way CSS2 did. We’re even seeing the same sort of glib jokes about how it’s going to be finished in 2020, which impacts on whether many developers will adopt something perceived (mistakenly, though somewhat understandably) as unready for commercial use. Some aspects of the initial monolithic HTML5 spec have been modularised, while related technologies like geolocation, which is widely considered to be part of HTML5 have always been their own small, independent activities.

So, if anything, I’d like to se the increasing modularisation of the HTML5 spec.

**3) You seem to spend quite some time building code generators at the moment. The CSS gradient generator and the audio embed generator being just two of them. Do people use them a lot? And why the separation between Firefox and Webkit rather than generating both?**

Just to clarify, all my new tools (audio, video, and some others in the pipeline), as well as the upgrades to existing ones (linear and radial gradients) are cross browser – they work in all browsers that support the technology they’re focussed on, and create code for all modern browsers (in some cases where they don’t even yet support the particular functionality – for example Opera and radial gradients).

In the past (and some of these are 2-3 years old now), I decided to focus only on those browsers which supported a particular technology. I had separate Firefox and Webkit versions of the gradient tools because they supported quite radically different models of gradients, which made a single interface to producing two separate versions of a gradient confusing, as well as essentially impossible.

It’s important to note that the primary motivation for these tools is to help people learn the concepts and syntax for these various features. I think many CSS3 features in particular are really quite complex, and learning them in the more traditional text oriented way is becoming increasingly difficult. For example, you can generate a radial or linear gradient with my tools for all modern browsers in a few seconds, even if you have no idea about how CSS gradients work. But the two articles I wrote on gradients in total come to nearly 10,000 words, and a couple of dozen or more illustrations.

Do many people use them? – they certainly generate quite a bit of traffic. They’re definitely popular – and I think as importantly, people really appreciate them – even really well known CSS experts let me know they really appreciate having them there, and I know others are using them to actually test browser implementations. So I think they are well worth doing.

The last thing I’ll say on them is I also build them to let *me* learn – I’ve been developing tools for web developers for 15 years, all the way back to the earliest days of CSS, and I find the best way to know a technology (and its and your limitations) is to build a tool to work with it.

**4) You are also a conference organiser and run workshops. What are the current hot topics in those related to new, open web technology and are there things you’d like to cover more that are not yet requested?**

New CSS3 features definitely get a lot of interest – animations, shiny effects like gradients and so on. And we’re definitely seeing a lot more interest across the board in the app development related technologies – offline webapps, geolocation, JavaScript more broadly. Im a sense I think a lot of more traditional web design is “done”. There are widely accepted and understood markup practices, patterns and techniques. There are page architecture patterns that we increasingly build page and site designs out of. But the area of web application development is really uncharted territory by comparison.

**5) A sure-fire way to tick you off and get you to blog seems to be to say that native experiences on devices will always be better than using open web technology. If you look at it straight from an end user perspective, this seems to be the case though – things look smoother in native apps. How can we make standards-based development more interesting for developers when the lure of native apps with a money-making store is that big? How can we break the notion of open tech apps being of lesser quality?**

There’s a lot going on with this question, so let me begin by stating my basic case. I call BS on the argument that native apps are intrinsically better looking, have better UX, and so on, simply because they are built with say objective-c (when people say native, they almost invariably mean apps for iOS they *think* are built with cocoa touch).

Your observation that many “native” apps are slicker, etc than web apps is a fair one. I think that it *is* somewhat easier to create a cookie cutter native app for say iOS using CocoaTouch, and the really excellent tools Apple has been working on since the NeXT days. But it’s also important to note that for many categories of applications, for example games, these apps use technologies like Unity3D, so in a sense many of the most successful, most engaging applications people use on say iOS aren’t native. I think it really comes down to the tools – and for developing apps using web technologies, these are far less sophisticated on the whole than those like Apple’s. Which to me presents an opportunity.

As to the lure of big money – it’s again one of those myths that get repeated ad nauseam. In fact it started even before there were any apps in Apple App Store! Now we’ve seen several years of activity, what have wen learned? There are doubtless a small number of big winners – but all indications are that almost no one makes any more selling apps on app stores.

There’s a whole industry in app discovery, so the supposed bon to developers that the App Store was going to provide in allowing the little guys to get their apps discovered by users really isn’t panning out.

As soon as you start looking at any sort of numbers objectively, it’s hard to see business case for building a native iOS app and selling it on Apple’s App Store, compared with simply taking that money to Las Vegas for the weekend. You’re going to waste far less of your life.

Finally, the single best way we can address the challenge web technology based apps have of being perceived of inferior quality is to continue building apps that are of superior quality. There are plenty out there – and often you don’t know it, because they are packaged up as native apps.

**6) I am worried about showcases these days. The latest “Chrome experiment” (the collaboration interactive video with OK Go) didn’t even work on my Macbook Air with Chrome and let my fan do the impression of an aircraft taking off (it also, ironically, doesn’t work on my Chromebook). There seems to be a – to me – dangerous move towards experimental web sites expecting certain browsers and even hardware. Are we facing a new “best viewed with IE6 and 1024×786 resolution”?**

I understand the concern, but don’t think we’re seeing, or will see a return to those bad old days. The “best viewed in” was seen on many many production sites back in the day. Experiments are just that – something at the bleeding edge, pushing the technology to the edges of its capability. So, I love seeing these experiments. We’ve been involved in some ourselves. We typically kick off our conferences with an opening title sequence (we started this a long time ago, but we’re seeing loads of folks doing it now). In the last year or so, we’ve been commissioning people to create these sequences using web technologies – and we’ve got no trouble with them targeting even a really, really specific setup – after all, it’s being designed for a very specific circumstance.

I honestly don’t think we’ll head back to the best viewed in days. Developers and browser makers have learned the lesson of just how bad that is for everyone.

**7) Whilst there is a lot of uptake on cool CSS3 transitions, animations, 3D transformations, WebGL and video it seems to me that the semantics of HTML5 and the forms get a bit forgotten. Even more so, it seems like a scam to tell people that there is a need for sections, articles and time elements when no browser uses them to create an outline or syndicates them. Do you see that changing? How can we make it more real for people? Haven’t we used the “use this and that markup as it is the right thing to do” argument too often?**

I tend to think the use of various new HTML5 elements as something of a cargo cult. I don’t really see any practical benefit, and there’s still legacy browser challenges (IE6 and 7) to deal with there. And I doubt there’s ever really going to be particular benefits – there’s ultimately very little additional information we’re providing by saying “this is a section”, “this is navigation”, and so on. If the semantics were richer, there would potentially be much more browser developers, search engine developers and so on could do with the richer markup, but as I’ve mentioned, I think we’ve got what we’ve got.

As for forms, now, there’s a lot more going on here of practical use today, and into the future. We can use new elements like number, email and url, and attributes like required right now (I’m doing it myself), as these fallback nicely in older browsers.

In fact, it’s one of my next big areas of focus after I finish a little project involving animations! HTML5 forms stuff is awesome!

**8) Let’s talk accessibility a bit. I get the feeling that right now the accessibility world is falling immensely behind. Whilst HTML5 and jQuery tells people to “write less and achieve more” it seems that ARIA roles are ridiculously verbose and rather tough to add. A lot of the needs of mobile and touch interfaces overlap with the needs of disabilities. However, it seems to me there is not enough interest in the a11y world for new technology as it is not proven. Do you find it hard to connect the two?**

I’m very far from an accessibility expert, so there’s probably not a a great deal I can add to this particular area of any real value.

ARIA roles are how I’d actually go about enriching the semantics of HTML5, rather than adding a small number of new elements as is the current state of play.

There’s two aspects to ARIA roles. First is the role attribute, initially introduced in XHTML as a means for adding additional semantic information about an element – the role that element is playing. For example, we have a common markup pattern of a div element, playing the role of the page header. We can mark this up with the role attribute like so <div role=”header”>

role is actually quite separate to ARIA. What ARIA brings to the role attribute is a vocabulary, a number of possible values for role, that we can use to add further semantic information to our pages. But you aren’t restricted to ARIAs vocabulary, and indeed can define your own. ARIAs vocabulary is actually far more extensive than HTML5’s.

I think the markup pattern, of using an attribute with a value to give additional information about an element, is really well known and widely used by developers – who doesn’t use class more or less like this?

So, I don’t see the use of role as a particular challenge for developers to adopt.

Then, role has the advantage that you can style it in every browser from IE7 up, using CSS with no JavaScript as well. For HTML5 elements, we need JavaScript for IE7 as well as IE6.

It has to be noted that he ARIA vocabulary is a generic one for rich internet applications, not specifically designed for apps developed using HTML. And sadly the ARIA vocabulary, and HTML5 semantics don’t map onto each other well.

I guess the biggest challenge for web accessibility into the future is that while making essentially text based and static content accessible is not overly challenging, and is now well understood, making applications, dynamic media, and rich interactive content accessible is a far more significant challenge.

**9) To me it is high time we stop doing showcases and demos and instead start documenting what people can do themselves and build real products with open web technologies.**

I love the showcases, the demos, the proofs of concept, but I agree, I also think it is time to really draw attention to the real world examples. I guess with my articles and tools, what I’m trying to do is help developers adopt these technologies today. As are many other folk as well.

**9) (ctd) Sadly, when it comes to conferences though a lot of the things shown on stage were written as a demo for the talk. Are there any exceptions you found? I remember some @media had a great talk on how Blogger saved money by moving to CSS for layout. We need more hard evidence talks like that. Do you actively try to find real life showcases?**

Absolutely – one of our goals is to have people who walk the walk. We actively look for folks who go beyond the opinions, and can speak with experience about projects, showcase successes, talk about the challenges they face, and the solutions to those.

**10) What’s the next big challenge? Where would you like the web to go and what are the next things that browser makers should agree on?**

Those of us old enough will remember when suddenly everything had an LED then LCD screen – things that were once analog, with mechanical dials and the like, things like microwave ovens, suddenly had displays, for time, temperature settings, and so on.

I think far sooner than we realise, there’ll be high resolution touchscreens everywhere, on almost every device.

Not all these devices will necessarily be connected to the web, but many of them will be. But their UIs will be essentially browser technology.

So, there’s going to be huge opportunity to develop user experiences for all kinds of devices using HTML, CSS, JavaScript and related web technologies.

Another really significant trend we’ve seen faltering steps toward, but which I think will genuinely be a paradigmatic change in technology use is “boot to web”.

Think back 3 or 4 years. The hardware, chip, motherboard, RAM speed of your laptop was a big deal. People really cared. They bragged about this stuff! Apple went through 2 incredibly complex expensive CPU architecture changes over about 12 years because of it. Now virtually no one cares. Hardware doesn’t matter any more. It’s been commodified.

The next layer to be commodified will be the OS. It may seem unimaginable now with iOS so dominant in the mobile, not to mention tablet space, but to me this is a very transitional period. The web will commodify operating systems. ChromeOS is a commercial example of this. Boot to Gecko, something Mozilla IMO should have been working on a long time ago is a more experimental example.

The technologies we currently call HTML5 will be the building blocks of the applications which run on these devices.

The as yet missing piece of this puzzle is the emerging Devices API standard, which exposes hardware and system APIs like the camera, address book, calendar, messaging services (for example SMS) to the browser. We’re already seeing support for aspects of this, such as the camera in Android 3 devices. I’m sure this is a big part of the “Boot to Gecko” project too.

Do you know anyone I should interview for “People of HTML5”? Tell me on Twitter: [@codepo8](http://twitter.com/codepo8)


## About
[
Chris Heilmann ](http://christianheilmann.com)

Evangelist for HTML5 and open web. Let's fix this!

## 6 comments

Muaz KhanAugust 25th, 2011 at 04:48CraigAugust 25th, 2011 at 12:57john allsoppAugust 29th, 2011 at 16:10john allsoppAugust 29th, 2011 at 16:11JoleSeptember 17th, 2011 at 03:11suregeekNovember 6th, 2011 at 05:43