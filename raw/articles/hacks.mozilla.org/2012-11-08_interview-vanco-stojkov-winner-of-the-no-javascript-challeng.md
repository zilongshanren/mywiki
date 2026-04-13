---
title: 'Interview: Vanco Stojkov, winner of the No JavaScript Challenge – Mozilla
  Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2012/11/interview-vanco-stojkov-winner-of-the-no-javascript-challenge/
author: John Karahalis
published: '2012-11-08'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*Vanco Stojkov won the highly contested No JavaScript Challenge with Honey Pursuit: Yet Another Love Saga, his wonderful bee-inspired open Web game. Amazingly, Honey Pursuit does not use a single line of JavaScript, but instead exploits the growing power of HTML and CSS to manage everything from keeping score to hit detection.*

*I recently had the chance to conduct a short email interview with Vanco. In our correspondence, I learned more about his background, his experience building Honey Pursuit, and his thoughts on the future of web development.*

## The interview

### How did you become interested in web development?

I’ve been interested in computers and programming since high school, but it was in my final year of studies that I got interested in web programming. I’d been assigned a web project in one of the courses we’d had and became so excited with it that I decided to focus on web development entirely.

### Tell us about developing Honey Pursuit. Was anything especially exciting, challenging, or rewarding?

First I had serious doubts about finishing the game in the manner I wanted to without using JavaScript. But it turned out that the web technologies, and CSS in particular, have already gone far ahead in making it possible to achieve much more than I could have thought of. The already available demos from the No JavaScript and previous Derbies were very helpful—there were so many stunning presentations and techniques from which one can learn a lot and that were truly inspirational during the development process.

Managing the markup and the CSS code has been the greatest challenge, especially management of the CSS animations—the code turned out pretty long and the animations were all depending on each other, so their synchronization presented one of the greatest problems. Fortunately, PHP coding came pretty handy, and by using PHP control variables and loops for dynamic CSS code and HTML markup generation the development process became much more manageable and faster.

### Can you tell us a little about how Honey Pursuit works?

There are three main user interactions that are required in order for the game to function properly—control of the game flow (start/pause/continue the game), control the hero bee (moving it around the screen), and collecting jars (sort of a collision detection):

- Starting/pausing the game is made possible by the use of the “:checked” pseudo-class. There is a hidden checkbox and two visible labels (start/pause buttons, visible one at a time) associated with that checkbox which enable two states (on/off). Whenever the checkbox is unchecked the animation in charge of the main game flow halts—”animation-play-state” is set to “paused”, otherwise the “animation-play-state” is set to “running”. With the “~” combinator the two states are used for the appropriate elements’ CSS by using the “:checked ~ .class” selector.
- The movement is enabled by the use of the “~” combinator and a grid of invisible divs covering the entire screen. So when these divs are “:hover”-ed the bee moves to the position associated with the appropriate div via the “#div_id:hover ~ #bee” selector. The bee also has a CSS transition applied to itself in order to move smoothly from one position to another.
- Jars collection is also enabled by the use of the “:hover” pseudo-class—on “:hover” the jar is removed, and the paused animation on the jar counter moves a step ahead by changing the “animation-play-state” to “running”.

Everything else is just a simple sequence of synchronized CSS animations: the intro animation ends at the last slide which shows a button that starts the game when clicked on; the “start” button triggers the hidden checkbox and, by that, the start of the main game animation; once the main game animation ends the outro animation begins which displays the outro slides sequence.

A nice touch are the two repeating CSS animations applied to each of the bees that mimic the bee flight (smoothly going up and down) and wings flap, respectively. I also think that the look and feel of the bees has a great (visual) impact to the overall experience, for which I’d like to thank [@kosturanov](https://twitter.com/kosturanov) for all the help and guidance with the design.

### What makes the web an exciting platform for you?

Openness, accessibility and platform-independence—these three are why I like the web. Openness in terms of not only being able to develop freely and without any limitation, but also of the ability to contribute to the community and standards, and make it an even better platform. And accessibility and platform-independence in terms of being able to access a web application from anywhere and virtually any device without any special requirements.

### What up-and-coming web technologies are you most excited about?

I really look forward to using mobile devices functionality within HTML5 apps via JavaScript, things that so far have been available to native apps only: camera, contact lists, sensors etc. It’s something that will give great power to the mobile web apps.

### If you could change one thing about the web, what would it be?

I love the web as it is, and the way it constantly evolves. But I think it would be great if web browsers implemented the standards faster and in a much more unified manner. During the past few years there has been a lot of frustration during development with the implementation of the new CSS3 features. But even when implemented they are supported with a CSS prefix for each specific browser.

### What advice would you give to aspiring web developers?

As in any other profession web developers also face a few occupational hazards, most of them being related to sitting in front of a computer for too long :), but apart from that it’s an extremely fun and creative occupation. The continually evolving nature of the web requires developers to constantly improve and try out new things. So my advice is to never stop experimenting, and never stop learning—from the standards and from other developers as well. Oh, and learn how to use and reuse techniques from other developers, it saves tons of time and nerves—there are very good odds that what you need is already done by someone else.

### Is there anything else you would like to share?

I would like to thank Mozilla for making available products and services that I’ve been using for years, and of course for organizing the Dev Derby challenges because these and similar events are really pushing the web ahead.

## One comment

Eduard GotwigNovember 8th, 2012 at 12:25