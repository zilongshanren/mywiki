---
title: Programming games in the browser – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2014/08/programming-games-in-the-browser/
author: Stefan Trenkel
published: '2014-08-13'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

A programming game is a computer game where two or more programs compete with each other. What are the basic requirements for programming games and can they be realized in browsers? With JavaScript?

## 4 basic claims

There are 4 basic claims. Competing programs:

- must run isolated from the main program.
- must communicate with the main program in a defined way.
- should run parallel. Parallel to the main program and parallel to each other.
- should be injected in the playing environment in an easy way.

The good old JavaScript is running synchronously and there is no way to isolate subprograms. But times are changing and modern JavaScript has a lot more features. What about [Web Workers](https://developer.mozilla.org/en-US/docs/Web/Guide/Performance/Using_web_workers)? They were designed to make JavaScript faster, running expensive calculations in the browser without blocking the user interface. But Web Workers can do more. They meet our claims about programming games! They run isolated from the main program, communicate with the main programs by events, run parallel and thanks to the new File API they can be injected locally.

## WEB WORKER CONTEST

That’s all. It’s really easy creating programming games with Web Workers. To show this idea working in May 2014 I launched a simple programming game based on Web Workers, the [WEB WORKER CONTEST](http://www.webworkercontest.net/). The actual game is a simple mathematical challenge: How to conquer a square of 100×100 fields. Starting from a random point the player must conquer a playing area of 100×100 fields with simple moves (up, down, right, left).

![](../../assets/210e962b082e29bc.png)


A new field can be occupied only if it was not previously occupied by the opponent’s program. The players do not have any information about the playing area. The only information they receive is whether their chosen move is possible or not. So, the Web Worker use `postMessage()`

to send their new move. And with the `onmessage()`

event they receive whether their move was possible or not (a simple `true`

or `false`

). The main program do it vice versa. It receives the move with `onmessage()`

, execute the move on the playing area and send the success with `postMessage()`

.

In the end your code looks like this:

```
// - worker1.js -
// makeMove() calulates the next move
onmessage = function (event) {
var success = event.data.success;
var direction = makeMove(success);
postMessage({
direction: direction
});
};
// - main program -
// makeMoveWorker1() executes the move
var worker1 = new Worker('worker1.js');
worker1.onmessage = function(event) {
var direction = event.data.direction;
var success = makeMoveWorker1(direction);
worker1.postMessage({
success: success
});
};
```

Now, just start the game with

```
// analogously for a second worker
woker1.postMessage({
success: true
});
```

and it’s in full swing.

The [complete code is available on GitHub](https://github.com/strenkel/wwc).

## The main challenge: equal distribution of machine time

The main challenge for programming games with Web Workers is the equal distribution of machine time to both Web Workers. There are 2 separate time problems. One in the loading phase, the other in the playing phase.

Before starting the game, both Web Workers must be loaded (remote or local). So, before starting the game you must wait until both Web Workers are loaded. Unfortunately there is no onload event for Web Workers. Of course we can do something about this: In the beginning the main program sends an ‘are-you-ready’ post to the player and starts the game after both workers confirm this post.

The equal machine time during the playing phase is in general not under the control of the main program. It can happen that one player can do lots of moves before the other player can move. To get equal conditions for both players is a challenge for both the browser engine and the operating system. But it is possible that one player try to block the other by permanent firing (with a `postMessage`

loop). To prevent this the main program send, together with the success information, a random ID. The player must resend this ID with his next move (otherwise he will be disqualified). With this restriction the machine time is sufficiently equally distributed.

More [videos are available on YouTube](https://www.youtube.com/channel/UCNqOUOlC8UOYYLdGHhFbY-Q).

## The contest and programming games

The WEB WORKER CONTEST was very agile. During 4 weeks over 200 programmers with over 700 programs tinkered on the best strategy to conquer the field.

Programming games in the browser works. With the Web Worker technology we have the instrument to realize them. And programming games in the browser are very handy for the participants. No need for installing a playing environment. Just go to the web site, write your code, test and upload it.

## About
[
Stefan Trenkel ](http://www.stefantrenkel.de)

Living in Bremen (Germany), loving JavaScript and working as a software engineer at [team neusta](http://www.team-neusta.de/).

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.