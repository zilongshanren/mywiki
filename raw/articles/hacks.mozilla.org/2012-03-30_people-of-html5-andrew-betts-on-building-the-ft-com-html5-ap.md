---
title: 'People of HTML5: Andrew Betts on building the FT.com HTML5 app – Mozilla Hacks
  - the Web developer blog'
url: https://hacks.mozilla.org/2012/03/people-of-html5-andrew-betts-on-building-the-ft-com-html5-app/
author: Chris Heilmann
published: '2012-03-30'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

HTML5 needs spokespeople to work. There are a lot of people out there who took on this role, and here at Mozilla we thought it is a good idea to introduce some of them to you with a series of interviews and short videos. The format is simple – we send the experts 10 questions to answer and then do a quick video interview to let them introduce themselves and ask for more detail on some of their answers.

![Andrew Betts](../../assets/ad8b9e11ceab1b0b.jpg)

[Andrew Betts](http://assanka.net/), director of Assanka.

We came across Andrew because of his talk “[We’ve Got a Website for That – The FT Web App and the Future of the Mobile Web](http://www.blackberrydevcon.com/europe/content/speakers/community/6451/andrew-betts)” at the BlackBerry Devcon in Amsterdam where he did a great job allowing us to peek under the hood of the [Financial Times web app](http://apps.ft.com/ftwebapp/). You can reach Andrew on Twitter as [@triblondon](http://twitter.com/triblondon).

## The video interview

You can [see the video on any HTML5 enabled device here](http://vid.ly/3t9t9l) (courtesy of vid.ly).

## 10 Questions for Andrew Betts

### 1) You worked on the HTML5 application for the financial times. What made you go HTML5 and not native? How many people were involved at all?

The FT has an agnostic approach when it comes to the formats and technologies we can use to display our content. The choice has to suit the content, the reader, and our business model. Before we launched the HTML5 app there was already an FT native app on iOS, and it received an Apple design award, but HTML5 offered several significant benefits, the most important of which was to allow us to maintain a direct relationship with the reader. Secondary benefits include a faster update process, an investment in future cross-platform compatibility (HTML5 is yet to fully realise the dream of write-once, run everywhere), and freedom from restrictions and rules that are (or may be in future) imposed by app store operators.

### 2) What would you say was the easiest part and what was the thing that you had to spend the most time on to make it work?

Interactions are the hardest thing to crack. Matching behaviour to user expectations is frighteningly complex, especially when you realise that instinctive expectations of swipe behaviour is actually quite varied and inconsistent. One example of this complexity is swiping horizontally from the bottom of a section page, which takes you to the top of the next one. If you then swipe back, do you end up where you were, or at the top? So dealing with interactions is both technically hard and architecturally challenging.

Offline behaviour is also very tough. We get a lot of “User x can’t use the app offline” style support requests, and those are very hard to debug. We log every report but the priority is to figure out the scale of the problem.

The easiest thing to deal with is probably layout. We send all legacy browsers to m.ft.com so we only have to cope with the most recent major versions, and that means that generally we get good standards support for CSS.

### 3) How did you deal with the differences in interfaces? A mobile has much less space than a tablet and again less than a desktop. Are you using mediaqueries to give different experiences?

We group devices into one of four sizes based on media queries, and we vary which resources we use slightly based on the reported DPI, but most of our responsive layout logic is done in JavaScript. We make a few assumptions right now to make development easier, such as that the user cannot change the size of the browser window, except by rotating the device, so we only need to change the layout on orientation change, not in response to arbitrary resizing of the window. We also currently assume the user has no mouse cursor, so there are no hover effects.

### 4) How does input get into it? Is it simple enough to build touch interfaces in HTML5 or did you have to use some trickery?

Quite a lot of trickery is involved, unfortunately. The browser has to tread a fine line between on the one hand offering a touch API to web developers and getting out of their way to let them use it, and on the other, dealing with the fact that almost all websites are still built for keyboard and mouse, so the browser needs to help the user deal with that. We developed a [polyfill called Fastclick](http://assanka.net/fastclick) which makes click events fire as fast as touch events, and that certainly helps us provide an experience that is as snappy as using a native app.

We also deal with swiping in a few quite distinctly different ways. Swiping between sections is an endless carousel, and we implement the tracking and sliding ourselves, by maintaining hidden page containers to the left and right of the current view and applying CSS 3D transforms. But paging through an article requires different scroll mechanics – it has a fixed length, and we have to lay out the whole article in one go to know how many pages there are. Pages that scroll vertically are a different challenge again, and there we use a combination of leaving the browser to do scrolling natively, and simulating it where we need slightly different behaviour.

You’ll also notice that the pages don’t ‘bounce’ when you hit the top and bottom of the page, despite that being the normal behaviour in the iOS browser. We’ve gone to quite some lengths to ensure that the user experience mirrors an app and doesn’t feel like the device ‘coping’ with a site that hasn’t been designed to be viewed using a device with touch input.

### 5) You said in your talk at Blackberry Devcon that you are using localStorage to cache your JavaScript libraries and some of the images. Why not use WebSQL or IndexDB for that? Isn’t the synchronous nature of localStorage slowing things down?

No, actually localStorage is considerably faster than WebSQL (we are yet to use IndexedDB because it’s not supported on some of our target platforms). The time required for a lookup by key in localStorage is many times less than the equivalent SELECT statement on a WebSQL table. It’s true that it’s synchronous, but if the critical aspect affecting perceived performance is the time required to fetch data, which it often is, then localStorage offers a much faster response. it’s also typically reliable and relatively stable compared to the behaviour of WebSQL and particularly the HTML5 app cache.

### 6) You also said that localStorage uses UTF-16 instead of UTF-8. This means you can store two ASCII characters in one UTF-16 one and thus double the storage capacity, right? Can you share some code? This would be incredible to use for everybody out there.

Both localStorage and WebSQL use UTF-16 in webkit browsers, it’s one of many aspects of the implementation of these technologies that don’t make a lot of sense! We’re experimenting with some algorithms for compressing our data so we can make more efficient use of that storage, and one of those is to combine two characters into a single UTF-16 one. We’re not using that in production yet, but when we do we’re certainly hoping to open source it.

There are simpler things to be done as well. A cursory poke and prod of WebSQL tables suggest that column names are stored along with the value in every cell, so some attempts to increase efficiency are as simple as using single character column names. Clearly we ought not to have to do all this, but it’s the price you pay for dealing with bleeding edge features in browsers.

### 7) What would you consider the best start for someone when they want to build an HTML5 app? What are the first things to get sorted?

Decide ahead of time what you’re trying to achieve. I could be a pedant and say that making your site HTML5 is really just a matter of changing the DOCTYPE, so an ‘HTML5 app’ is really whatever you define it to be, and having a clear idea of that is a good place to begin. Are you building something just for touch, or for keyboard and mouse as well? Does it need to work offline? Will it be crawlable by search spiders? Will it work with JavaScript disabled?

There are some great resources like MDN, but we often find ourselves reading the HTML5 specs, and sometimes even the webkit source code to find out how something is actually implemented.

### 8) Can native and web apps be the same thing?

Technically, I guess not – strictly speaking a native app is complied code running directly on a platform, but the hybrid model seems to be getting ever more popular, and I often see apps which are thinly veiled web browsers. If you look at it from the user perspective and say, can a web app feel exactly like a native app, I don’t see why not. The challenges are greater because of the diversity of uses that web technologies are designed for, and the diversity of platforms on which they are used. And for uses such as gaming, native code is always likely to run faster and have deeper access to the OS.

But for applications like publishing, which after all was the original purpose of the web, web technologies do provide support for most of the user experience concepts that we need.

### 9) What about testing? How did you approach this? Do you have an array of hardware to play with?

It’s a nightmare. We had a local electrician built us a charging station where we could store all our devices and keep them charged all the time. We have around 45 individual devices in our team (that’s around 4 times more devices than we have people). We’re constantly looking at ways of improving our testing process, and we keep revisiting automated, on device testing, but we’re not using it in our build cycle as yet. Right now we have a team of very dedicated testers who poke and prod devices all day.

### 10) As someone who went through the process of building a big HTML5 app, what would you like to have from browser vendors to make your life easier?

A blithe answer is ‘How long do you have’, but in practice we have to accept we’re using freshly minted technologies and there might be teething troubles. The main things on our shopping list are: more frequent and aggressive browser updates (especially on Android, where the browser is the problem child of the mobile web world), a better and more reliable app cache, and hardware acceleration of CSS transforms.

## About
[
Chris Heilmann ](http://christianheilmann.com)

Evangelist for HTML5 and open web. Let's fix this!

## One comment

Aaron T. GroggApril 1st, 2012 at 03:33