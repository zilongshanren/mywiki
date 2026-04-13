---
title: People of HTML5 – Rob Hawkes – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2011/01/people-of-html5-rob-hawkes/
author: Chris Heilmann
published: '2011-01-27'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

HTML5 needs spokespeople to work. There are a lot of people out there who took on this role, and here at Mozilla we thought it is a good idea to introduce some of them to you with a series of interviews and short videos. The format is simple – we send the experts 10 questions to answer and then do a quick video interview to let them introduce themselves and ask for more detail on some of their answers.

![Rob Hawkes](../../assets/391d85b2cb6e9601.jpg)

[Rob Hawkes](http://rawkes.com/) author of [Rawkets](http://rawkets.com/), a multiplayer game using canvas and websockets.

Rob was one of the presenters at the Game On 2010 event in London, England where he showed off his game. The video and his slides are [available on the Mozilla Games Blog](http://mozillalabs.com/gaming/2010/12/09/game_on-2010-150-gamer-geeks-pack-out-london/). He is currently busy working on [a book about Canvas](http://amzn.to/gzQMHp). You can find Rob on Twitter as [@robhawkes](http://twitter.com/robhawkes).

The message I really loved getting from Rob was that it is OK to use any technology you want and that there is a benefit to people messing around with your code – even if it is to game the system.

## The video interview

You can [see the video on any HTML5 enabled device here](http://vid.ly/0n4g0t) (courtesy of vid.ly).

## Ten questions about HTML5 for Rob Hawkes

### 1) So, you’ve been fiddling around with Canvas for gaming a lot – why the fascination? Did you write games in other environments before?

I sure have. My life has practically revolved around making games of some sort for the past year or two now. I just love the concept of using games to experiment with a programming languages and really learn everything I can about them. It’s a good way to try out most of the features involved in visual programming as well, particularly with harder concepts like physics, which I’m still no expert in. My fascination with games programming started out of necessity really; I had to create a game in my second year of university, so I co-created an [augmented reality game](https://github.com/robhawkes/sushi-roboto) using Papervision3D and ActionScript. From there I co-created another game of sorts in Adobe Flex that allowed people to [play against each other using a webcam](http://www.chromacam.co.uk/), which was fun. And now I’m making games in canvas; partly because it’s fun, and partly to learn everything I can about it. I get a kick out of the interactivity and playability factor that games bring, which I think hooks into my addiction for visual programming in general.

### 2) The cool thing about open technologies is that it is easy to see what is going on under the hood. View source and you get the picture. For gaming, isn’t that a problem? To “game” a highscore for a Flash game at least you need to do some HTTP sniffing – with Canvas it must be even easier. How do you protect yourself from that?

The fact that canvas is so open is something that makes me interested in it. I’m usually pretty open about programming and I’d love it if people can learn from my code, so being able to view the source code directly within the browser is amazing for that. However, the major drawback is that your code is open for everyone to see, so security becomes a pretty big issue.

You’re right though, this is particularly troublesome with gaming, and I’m inclined to say that there isn’t much that you can do about it. In fact, is wasn’t long after I released the first version of [Rawkets](http://rawkets.com/) that people started to poke around the code and manipulate the game to their advantage.

In all honesty, I actually see it as a good thing, as it showed me where my code was weak, and highlighted the areas that I needed to secure. You can obfuscate and minify your code as much as you want, but people can still get access to it because it’s just the way JavaScript works. However, there are a few ways to mitigate the problem, like passing core logic for the game to a remote server and communicating to it via restrictive and secure API calls. This is a good method for multiplayer games, where data received from the server is seen as trustworthy, and where as data on the client side is not. Or, you can wrap sensitive code in closures and take advantage of local variables to hide away data that you don’t want people to easily access. Another option is to just not worry about it. So long as you don’t let the hackers ruin the game for other players, does it really matter if they screw it up in their own browser?

In reality, none of these methods will 100% protect you, but they’ll certainly make things harder for would-be hackers.

### 3) Talking about open. Isn’t Canvas just a Java applet with a predefined API and no need for a slow JVM? You still only have a rectangle somewhere in the page you can manipulate…

If you mean that canvas is like a sandbox that you can only access via a specific set of API calls, then yes, pretty much. Then again, the API calls allow you to do a hell of a lot, and couldn’t you say the same about Flash and all the closed methods of creating graphics?

I suppose when you say canvas is open; you’re mainly talking about the development behind its creation (ie. the W3C), and the fact that the code to draw elements on it isn’t hidden away from prying eyes. Canvas is definitely not open in the sense that you are free to extend it and do whatever you want with it. So long as you abide by the API calls, which is fine for 99% of the time, then you’ve not got a problem.

As you say, canvas is effectively just a rectangular area that the browser allows you to draw into. Once you’ve drawn a few shapes into it, you can’t access them individually, but then again, that’s exactly how canvas is meant to work. It’s not like SVG, where every element that you’ve drawn can be accessed from the DOM and edited. Canvas is a bitmap system that has no concept of individual elements. It’s a destructive system that basically just changes the colour of pixels within its rectangle, based on the API calls that you give it. In that way, it’s just like Microsoft Paint from back in the day.

### 4) What about accessibility? Can assistive technology access canvas content? How about keyboard access?

To put it bluntly, not really. At least, not yet.

Canvas does have fallback content, which is placed between the canvas tags and shows up when a browser doesn’t support canvas, but it doesn’t have much else to aid with accessibility. The cool thing about the fallback content is that it’s possible to place content in there for keyboard access. I believe IE9 already has this functionality, which lets you show the canvas, but still give keyboard access so you can describe what’s going in within the canvas in text, or something like that. The problem with methods like this is that you effectively duplicate all of your content; you draw everything on the canvas, and then you have to write it all up within the canvas tags to explain what you’ve drawn.

What you can’t do yet is give assistive access to individual elements within the canvas, simply because canvas is just a big rectangle of pixels with no concept about what’s bee drawn. This is the major drawback with using a bitmap system that has a pretty closed API. There is talk about using something called the shadow DOM, to open up the canvas and allow some sort of access into the elements that have been drawn, but I don’t believe much has been done about this yet.

It’s definitely an area that I’m interested to see progress, but in the meantime, [Bruce Lawson highlights a couple of the proposals](http://www.brucelawson.co.uk/2010/html5-video-canvas-accessibility-microdata/) that are floating around to sort out the accessibility issue with canvas.

### 5) What about performance? What are the hot tips to keep a canvas game run smoothly?

This is a massive sticking point with canvas at the moment; it can be so god damn slow! Actually, this isn’t really a problem with canvas, but rather the fact that canvas uses the browser process to draw everything, which in turn uses the processor (CPU).

Some browsers are introducing something called hardware acceleration, which passes off canvas and graphical processes to the graphics card (GPU). This simple feature really speeds things up, and allows you to do some pretty intensive stuff. Still, hardware acceleration isn’t a magic bullet; you still need to program defensively and be aware of potential bottlenecks and performance issues with your code.

The most common issues arise around unnecessarily extravagant timers and loops. For example, animating in canvas usually requires the use of a JavaScript timeout, which runs a function that draws everything onto the canvas 30 times a second; fast enough to look like things are moving. This is great, but what about if you’re not animating things any more? I’ve made the mistake of not turning off the animation timer, and inherently sucking precious CPU juice for no good reason.

Another example is that of collision detection, or any other check that has to be performed on a large amount of objects. The bad way of doing this is to loop through every object, and then loop through every object a second time on each iteration of the original loop. The problem with this is that you end up checking some objects twice, or more, and basically wasting resources. Instead, you can optimise your loops to ignore objects that you’ve already checked, which can cut the amount of loops down considerably.

There are countless ways to optimise your code, and most won’t achieve much on their own, but together they can add up to save a pretty significant amount of resources.

### 6) Your game uses Web sockets for communication. How did you find that to work with? Does it scale well? Are there any things you don’t like about the technology?

You mean that it used to use WebSockets? It’s a shame FireFox and others decided it would be a great idea to drop support for them for the time being. Jesting aside, the game is built atop WebSockets, and it’s been an interesting journey. I love WebSockets, and I think that having a full-duplex method of communicating within a browser is fantastic. The fact that the data is streamed live opens up a whole range of possibilities for games and Web apps.

I didn’t find too many issues with WebSockets regarding stability and scalability, as in reality most of the problems lay with the code on the server that deals with sending information back and forth. I found that one thing you need to be aware of is that the amount of data being sent back and forth can increase at an exponential rate if you’re not used to optimising communication for a large amount of users.

I have to admit though, my biggest bug bear with WebSockets is that it sends data as text, and it doesn’t support the UDP protocol. Right now, WebSockets sending everything as text data is great because it’s dead simple, but it sucks because it can potentially take a lot of precious bandwidth, especially when you’re sending data many times a second to hundreds of different players in a game.

The UDP problems relates to how canvas currently only supports the TCP protocol. What this means is that every piece of data that is sent back and forth between a server and a client has to be received in order. This is not good for gaming, where a bit of lag can end up causing a backlog of messages that have to be sent in order before any new messages can be sent. UDP on the other hand would allow you to send messages as and when they occur, without worrying about order. This is very good for games that rely on precise data that is time-sensitive, like the movement of a player in an FPS game.

You have to remember that WebSockets is something new, and it’s likely to have some teething troubles at the beginning; hence it being disabled temporarily. Still, it’s got a bright future, and I’m looking forward to seeing how it progresses.

### 7) Have you played with SVG, too? If so, when would you use what and is there a chance to use the strong parts of both technologies together?

Admittedly, I’ve not played with SVG as much as I’d like to. I’ve just become so caught up in the world of canvas in recent months. However, it’s something that I strongly believe should be used instead of canvas in particular circumstances, like when dealing with the conversion of existing HTML data into a graphical format (eg. creating graphs from a table).

SVG is also great because it’s accessible via the DOM, but it falls down with animation and gaming. It was never built with this kind of use in mind, and it’s exactly why canvas exists. Canvas is perfect for fast and dynamic animations, and it’s particularly perfect for creating games.

Fortunately, it isn’t always a case of being either or with SVG and canvas. It’s completely [possible to draw SVG shapes within canvas](http://wiki.whatwg.org/wiki/SVG_and_canvas), which has the added benefit of letting you have all the vector goodness of SVG within a bitmap system. I’ve heard of people using techniques like this for sprites within games, and for drawing images onto canvas that need to be resized a lot.

### 8) What’s the next barrier you’d love to see opened up? What features of closed technology are there that are beyond your reach but you are itching to try out?

I’m really interested in seeing the Device APIs (DAP) being supported in the major browsers. One of the things that is lacking in browsers at the moment is support for external devices like webcams and microphones. I can just see canvas and DAP being used together for some pretty awesome Web apps and visualisations. Imagine being able to create an avatar for a website by using a bit of canvas with an attached webcam. Or, what about live video chat through the browser with WebSockets and canvas/HTML5 video? That would be JavaScript awesomeness right there!

### 9) Currently you’re writing a book on Canvas. As not everybody has time to wait for this, where could people go in the meantime to get the real info about starting with canvas?

It’s not a massive wait (it’ll be out in May), but in the meantime I’d suggest going to the [Mozilla Developer Network](https://developer.mozilla.org/en/HTML/Canvas). It’s where I learnt how to use canvas, so it must be good! Apart from that, there really is a lack of decent resources for learning canvas at the moment, but I predict that changing for the better over the next year.

### 10) Where could people go to get inspiration? What other uses of Canvas have you seen that made you go “woooo I want that!”?

There are some fantastic projects being created with canvas at the moment. I could create a massive list, but here are some of my favourite:

Some particularly impressive uses of canvas that have got my juices flowing are projects that really push the pixel manipulation features of canvas, like using it to [detect faces in images](https://github.com/liuliu/ccv/tree/current/js/), or [nudity](http://www.patrick-wied.at/static/nudejs/). Weird, but pretty impressive stuff!

Do you know anyone I should interview for “People of HTML5”? Tell me on Twitter: [@codepo8](http://twitter.com/codepo8)

## About
[
Chris Heilmann ](http://christianheilmann.com)

Evangelist for HTML5 and open web. Let's fix this!