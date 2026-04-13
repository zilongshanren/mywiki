---
title: People of HTML5 – Remy Sharp – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2011/01/people-of-html5-remy-sharp/
author: Chris Heilmann
published: '2011-01-11'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

HTML5 needs spokespeople to work. There are a lot of people out there who took on this role, and here at Mozilla we thought it is a good idea to introduce some of them to you with a series of interviews and short videos. The format is simple – we send the experts 10 questions to answer and then do a quick video interview to let them introduce themselves and ask for more detail on some of their answers.

Today we are featuring ![Remy Sharp](../../assets/d475783b2e68fcaf.jpg)


[Remy Sharp](http://remysharp.com)co-author of

[Introducing HTML5](http://introducinghtml5.com/)and organiser of the

[Full Frontal](http://2010.full-frontal.org/)conference in Brighton, England.

Remy is one of those ubiquitous people of HTML5. Whenever something needed fixing, there is probably something on GitHub that Remy wrote that helps you. He is also very English and doesn’t mince his words much.

You can find Remy on Twitter as [@rem](http://twitter.com/rem).

## The video interview

[Watch the video on YouTube](http://www.youtube.com/watch?v=fWwTv_AhFgw) or Download it from [Archive.org](http://www.archive.org/details/PeopleOfHtml5-RemySharp) as [MP4 (98 MB)](http://www.archive.org/download/PeopleOfHtml5-RemySharp/remy_512kb.mp4), [OGG (70 MB)](http://www.archive.org/download/PeopleOfHtml5-RemySharp/remy.ogv) or [WebM (68MB)](http://www.archive.org/download/PeopleOfHtml5-RemySharp/remy.webm)

## Ten questions about HTML5 for Remy Sharp

### 1) Reading “Introducing HTML5” it seems to me that you were more of the API – focused person and Bruce the markup guy. Is that a fair assumption? What is your background and passion?

That’s spot on. Bruce asked me to join the project as the “JavaScript guy” – which is the slogan I wear under my clothes and frequently reveal in a superman ‘spinning around’ fashion (often at the surprise of clients).

My background has always been coding – even from a young age, my dad had me copying out listings from old spectrum magazines only to result in hours of typing and some random error that I could never debug.

As I got older I graduated to coding in C but those were the days the SDKs were 10Mb downloaded over a 14kb modem, and compile in to some really odd environment. Suffice to say I didn’t get very far.

Then along came JavaScript. A programming language that didn’t require any special development environment. I could write the code in Notepad on my dodgy Window 95 box, and every machine came with the runtime: the browser. Score!

From that point on the idea of instant gratification from the browser meant that I was converted – JavaScript was the way for me.

Since then I’ve worked on backend environments too (yep, I’m a Perl guy, sorry!), but always worked and played in the front end in some way or another. However, since started on my own in 2006, it’s allowed me to move focus almost entirely on the front end, and specialise in JavaScript. Basically, work-wise: I’m a pig in shit **[Ed: for our non-native English readers, he means “happy”)]**.

### 2) From a programmer’s point of view, what are the most exciting bits about the HTML5 standard? What would you say is something every aspiring developer should get their head around first?

For me, the most exciting aspects of HTML5 is the depth of the JavaScript APIs. It’s pretty tricky to explain to Joe Bloggs that actually this newly spec’ed version of HTML isn’t mostly HTML; it’s mostly JavaScript.

I couldn’t put my finger on one single part of the spec, only because it’s like saying which is your favourite part of CSS (the :target selector – okay, so I can, but that’s not the point!). What’s most exciting to me is that HTML5 is saying that the browser is the platform that we can deliver real applications – take this technology seriously.

If an aspiring developer wanted something quick and impressive, I’d say play around with the video API – by no means is this the best API, just an easy one.

If they really wanted to blow people away with something amazing using HTML5, I’d say learn JavaScript (I’m assuming they’re already happy with HTML and CSS). Get a book like JavaScript: The Good Parts and then get JavaScript Patterns and master the language. Maybe, just maybe, then go buy Introducing HTML5, it’s written by two /really/ good looking (naked) guys: [http://flic.kr/p/8iyQTE](http://flic.kr/p/8iyQTE) and [http://flic.kr/p/8iy6Z1](http://flic.kr/p/8iy6Z1) **[Ed: maybe NSFW, definitely disturbing]**.

### 3) In your book you wrote a nice step-by-step video player for HTML5 video. What do you think works well with the Video APIs and what are still problems that need solving?

The media API is dirt simple, so it means working with video and audio is a doddle. For me, most of it works really well (so long as you understand the loading process and the events).

Otherwise what’s really quite neat, is the fact I can capture the video frames and mess with them in a canvas element – there’s lots of fun that can be had there (see some of [Paul Rouget’s demos](http://people.mozilla.com/~prouget/demos/) for that!).

What sucks, and sucks hard, is the spec asks vendors, ie. browser makers, *not* to implement full screen mode. It uses security concerns as the reason (which I can understand), but Flash solved this long ago – so why not follow their lead on this particular problem? If native video won’t go full screen, it will never be a competitive alternative to Flash for video.

That all said, I do like that the folks behind WebKit went and ignored the spec, and implemented full screen. The specs are just guidelines, and personally, I think browsers should be adding this feature.

### 4) Let’s talk a bit about non-HTML5 standards, like Geolocation. I understand you did some work with that and found that some parts of the spec work well whilst others less so. Can you give us some insight?

On top of HTML5 specification there’s a bunch more specs that make the browser really, really exciting. If we focus on the browser being released today (IE9 included) there’s a massive amount that can be done that we couldn’t do 10 years ago.

There’s the “non-HTML5” specs that actually were part of HTML5, but split out for good reason (so they can be better managed), like web storage, 2D canvas API and Web Sockets, but there’s also the /really/ “nothing-to-do-with-HTML5” APIs (NTDWH5API!) like querySelector, XHR2 and the Device APIs. I’m super keen to try all of these out even if they’re not fully there in all the browsers.

Geolocation is a great example of cherry picking technology. Playing against the idea that the technology isn’t fully implemented. Something I find myself ranting on and on about when it comes to the question of whether a developer should use HTML5. Only 50% of Geolocation is implemented in the browsers supporting it, in that they don’t have altitude, heading or speed – all of which are part of the spec. Does that stop mainstream apps like Google Maps from using the API? (clue: no).

The guys writting the specs have done a pretty amazing job, and in particular there are few cases where the specs have been retrospectively written. XHR is one of these and now we’ve got a stable API being added in new browsers (i.e. IE6 sucks, yes, we all know that). Which leads us to drag and drop. The black sheep of the APIs. In theory a really powerful API that could make our applications rip, but the technical implementation is a shambles. [PPK (Peter-Paul Koch) tore the spec a bit of a ‘new one’](http://www.quirksmode.org/blog/archives/2009/09/the_html5_drag.html). It’s usable, but it’s confusing, and lacking.

Generally, I’ve found the “non-HTML5” specs to be a bit of mixed bag. Some are well supported in new browsers, some not at all. SVG is an oldie and now really viable with the help of JavaScript libraries such as [Raphaël.js](http://raphaeljs.com) or [SVGWeb](http://code.google.com/p/svgweb/) (a Flash based solution). All in all, there’s lots of options available in JavaScript API nowadays compared to back in the dark ages.

### 5) Let’s talk Canvas vs. SVG for a bit. Isn’t Canvas just having another pixel-based rectangle in the page much like Java Applets used to be? SVG, on the other hand is Vector based and thus would be a more natural tool to do something with open standards that we do in Flash now. When would you pick SVG instead of Canvas and vice versa?

Canvas, in a lot of ways is just like the Flash drawing APIs. It’s not accessible and a total black box. The thing is, in the West, there’s a lot of businesses, rightly or wrongly, that want their fancy animation thingy to work on iOS. Since Flash doesn’t work there, canvas is a superb solution.

However, you must, MUST, decide which technology to use. Don’t just use canvas because you saw a [Mario Kart demo](http://blog.nihilogic.dk/2008/05/javascript-super-mario-kart.html) using it. Look at the pros and cons of each. SVG and the canvas API are not competitive technologies, they’re specially shaped hammers for specific jobs.

Brad Neuberg did a superb job of summarising the pros and cons of each, and I’m constantly referring people to it (here’s the [video](http://www.youtube.com/watch?v=siOHh0uzcuY#t=17m00s)).

So it really boils down to:

- Canvas: pixel manipulation, non-interactive and high animation
- SVG: interactive, vector based

Choose wisely young padawan!

### 6) What about performance? Aren’t large Canvas solutions very slow, especially on mobile devices? Isn’t that a problem for gaming? What can be done to work around that?

Well…yes and no. I’m finishing a project that has a large canvas animation going on, and it’s not slow on mobile devices (not that it was designed for those). The reason it’s not slow is because of the way the canvas animates. It doesn’t need to be constantly updating at 60fps.

Performance depends on your application. Evaluate the environment, the technologies and make a good decision. I personally don’t think using a canvas for a really high performance game on a mobile is quite ready. I don’t think the devices have the ommph to get the job done – but there’s a hidden problem – the browser in the device isn’t quite up to it. Hardware acceleration is going to help, a lot, but today, right now, I don’t think we’ll see games like Angry Birds written in JavaScript.

That said… I’ve seriously considered how you could replicate a game like [Canabalt](http://www.adamatomic.com/canabalt/) using a mix of canvas, DIVs and CSS. I think it might be doable ::throws gauntlet::

I think our community could actually learn a lot from the Flash community. They’ve been through all of this already. Trying to make old versions of Flash from years back do things that were pushing the boundaries. People like Seb Lee-Delisle ([@seb_ly](http://twitter.com/seb_ly) / [http://seb.ly](http://seb.ly)) are doing an amazing job of teaching both the Flash and JavaScript community.

### 7) A feature that used to be HTML5 and is now an own spec is LocalStorage and its derivatives Session Storage or the full-fledged WebSQL and IndexedDB. Another thing is offline storage. There seems to be a huge discussion in developer circles about what to use when and if NoSQL solutions client side are the future or not. What are your thoughts? When can you use what and what are the drawbacks?

Personally I love seeing server-less applications. Looking at the storage solutions I often find it difficult to see why you wouldn’t use WebStorage every time.

In a way it acts like (in my limited experience of) NoSQL, in that you lookup a key and get a result.

Equally, I think SQL in the browser is over the top. Like you’re trying to use the storage method *you* understand and forcing it into the browser. Seems like too much work for too little win.

Offline Apps, API-wise, ie. the application cache is /really/ sexy. Like sexy with chocolate on top sexy. The idea that our applications can run without the web, or switch when it detects it’s offline is really powerful. The only problem is that the events are screwed. The event to say your app is now offline requires the user to intervene via the browser menu, telling the browser to “work in offline mode”. A total failure of experience. What’s worse is that, as far as I know, there’s no plan to make offline event fire properly :-(

That all said, cookies are definitely dead for me. I’ve yet to find a real solution for cookies since I found the Web Storage API – and there’s a good decent number of polyfills for Web Storage – so there’s really no fear of using the API.

### 8) Changing the track a bit, you’ve built the HTML5shiv to make HTML5elements styleable in IE. This idea sparked quite a lot of other solutions to make IE6 work with the new technologies (or actually simulate them). Where does this end? Do you think it is worth while to write much more code just to have full IE6 support?

There’s two things here:

- Supporting IE6 (clue: don’t)
- Polyfills

IE6, seriously, and for the umpteenth time, look at your users. Seriously. I know the project manager is going to say they don’t know what the figures are, in that case: find out! Then, once you’ve got the usage stats in hand, you know your audience and you know what technology they support.

If they’re mostly IE6 users, then adding native video with spinning and dancing canvas effect isn’t going to work – not even with shims and polyfills. IE6 is an old dog that just isn’t up to doing the mileage he used to be able to do back in his prime. But enough on this subject – the old ‘do I, or don’t I developer for IE6’ is long in the tooth.

Polyfills – that’s a different matter. They’re not there to support IE6, they’re there to bring browsers up to your expectations as a developer. However, I’d ask that you carefully consider them before pulling them in. The point of these scripts is they plug missing APIs in those older browsers. “Old browsers” doesn’t particularly mean IE6. For example, the Web Sockets API has a polyfill by way of Flash. If native Web Sockets aren’t there, Flash fills the gap, but the API is exposed in exactly the same manner, meaning that you don’t have to fork your code.

I don’t think people should be pulling in scripts just for the hell of it. You should consider what you’re trying to achieve and decide whether X technology is the right fit. If it is, and you know (or expect) your users have browsers that don’t support X technology – should you plug it with JavaScript or perhaps should you consider a different technology?

This exact same argument rings true for when someone adds jQuery just to add or remove a class from an element. It’s simply not worth it – but clearly that particular developer didn’t really understand what they needed to do. So is education the solution? I should hope so.

### 9) Where would you send people if they want to learn about HTML5? What are tutorials that taught you a lot? Where should interested people hang out?

[HTML5 Doctor](http://html5doctor.com) – fo sho’. :)

I tend to also direct people to my [http://html5demos.com](http://html5demos.com) simply to encourage viewing source, and hacking away.

Regarding what tutorials taught me – if I’m totally honest, the place I’ve learnt the most from is actually HTML5Doctor.com. There’s some pretty good JavaScript / API tutorials coming from the chaps at [http://bocoup.com](http://bocoup.com). Otherwise, I actually spend a lot of time just snooping through the specifications, looking for bits that I’ve not seen before and generally poking them with a stick.

### 10) You have announced that you are concentrating on building a framework to make Websockets easy to work with. How is that getting on and what do you see Websockets being used for in the future? In other words, why the fascination?

Concentrating is a strong word ;-) but it is true, I’ve started working on a product that abstracts Web Sockets to a service. Not the API alone, since it’s so damn simple, but the server setup: creating sessions, user control flow, waiting for users and more.

The service is called Förbind. Swedish for “connect”, ie. to connect your users. It’s still early days, but I hope to release alpha access to [forbind.net](http://forbind.net/) this month.

I used to work in finance web sites and real-time was the golden egg: to get that data as soon as it was published. So now that it’s available in a native form in the browser, I’m all over it!

What’s more, I love the idea of anonymous users. I created a bunch of demos where the user can contribute to something without ever really revealing themselves, and when the users come, you start to see how creative people are without really trying. Sure, you get a lot of cocks being drawn, but you also see some impressive ideas – my business 404 page for example allows people to leave a drawing, one of the most impressive is a Super Mario in all his glory. Anonymous users really interest me because as grey as things can seem sometimes, a stranger can easily inspire you.

Do you know anyone I should interview for “People of HTML5”? Tell me on Twitter: [@codepo8](http://twitter.com/codepo8)

## About
[
Chris Heilmann ](http://christianheilmann.com)

Evangelist for HTML5 and open web. Let's fix this!

## 3 comments

Ludvig LindblomJanuary 12th, 2011 at 04:40Jeff JJanuary 16th, 2011 at 09:44JD GauchatFebruary 19th, 2011 at 00:17