---
title: 'People of HTML5: Joe Lambert unshredding images in Canvas – Mozilla Hacks
  - the Web developer blog'
url: https://hacks.mozilla.org/2011/11/people-of-html5-joe-lambert-unshredding-images-in-canvas/
author: Chris Heilmann
published: '2011-11-28'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

![Joe Lambert](../../assets/4d2956f48b0a4cef.jpg)

[Joe Lambert](http://blog.joelambert.co.uk/), a web developer from Southampton, England working for Rareloop took on the [Instagram engineering challenge of un-shredding a shredded image](http://instagram-engineering.tumblr.com/post/12651721845/instagram-engineering-challenge-the-unshredder) but instead of using server-side code, he used HTML5 canvas. Here’s a screencast of [his solution to the problem](http://www.joelambert.co.uk/unshred/):

And here we are in a quick interview, chatting about how he approached the problem and why he used web technologies:

## 1) The specs of the competition said you can use Python, Ruby or C++ and you went instead for JavaScript and Canvas. Why?

JavaScript is my language of choice and what I use most of the time. I also find it the most fun as its easy to post your creations online and show people immediately, no downloads or dependencies to worry about. I wasn’t really looking to get hired by Instagram so adhering strictly to the rules wasn’t a big deal. Essentially it was an appealing problem that I thought could be solved in a browser, so wanted to prove that was the case.

I actually knew from the start that creating the algorithm to unshred the image was only half of what I wanted to do. That in itself was going to be a challenge and quite satisfying to solve but I really wanted to get to a point where I could make the slices move into the right place. I wouldn’t have been able to create this effect as quickly in any other environment.

## 2) How did you approach the problem of unshredding the images? Did you do similar things before? What is the logic you use?

I wasn’t too worried about the most efficient algorithm so I just started by thinking about how a human might solve this type of problem. I’ve played around with image data a little before but nothing that would have been directly useful to this particular problem.

If I were solving this in the physical world I’d start by picking up a slice at random then pick up each other shredded slice and see if it looked like it fitted to the left or right of the piece in my hand. I’d then repeat this till the image was back to its original state.

This gave an indication of the kind of structure my code should have, I just needed to work out how to computationally measure whether two strips ought to be next to one another. For this I just compared the pixels closest to each edge and measured the euclidean distance between the colour values. It seemed to work pretty well!

## 3) I see you are not using typed arrays in your solution yet. It seems to perform well the way it is now, do you think they’d make a difference?

I’m not sure, efficiency wasn’t high on my priorities for this challenge so I didn’t really look to optimise it but as you mention it seems to perform quite well. I haven’t tried the algorithm with larger images but I suspect it would perform not so well.

## 4) What was the feedback so far? Has Instagram contacted you?

The feedback has been really positive, especially via Twitter. I think generally the competition has had quite a high profile which certainly helped.

Instagram haven’t been in contact yet but it would be good to hear from them. I suspect they’re focusing on all the people who used the recommended languages

## 5) Seeing how easy this was can you see other challenges with images and canvas? Could you think of ways how to make it easier for developers, for example by extending the API?

The way you access pixel data in Canvas is a little complicated, it might be useful to have some helper functions to let you get access to a single pixel via X/Y coordinates. I ended up writing a little helper function to do this for this challenge, I’m going to try get the code up on GitHub shortly so this might be of use for others.

It would also have been useful to have been able to call `toDataURL()`

on a `CanvasPixelArray`

object. My implementation used the DOM and CSS3 transitions to move the images into their correct places after the algorithm had solved the order, being able to access a Data URI for each slice would have be handy.

If you want to chat with Joe, he is available on Twitter as [@joelambert](https://twitter.com/joelambert).

## About
[
Chris Heilmann ](http://christianheilmann.com)

Evangelist for HTML5 and open web. Let's fix this!

## 2 comments

ShekharNovember 28th, 2011 at 23:17Brian EnriquezNovember 29th, 2011 at 08:36