---
title: 'Q & A With Michal Biniek: HTML5 Hacker and Frequent Dev Derby Winner – Mozilla
  Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2012/02/q-a-with-michal-biniek-html5-hacker-and-frequent-dev-derby-winner/
author: Eduardo Bouças
published: '2012-02-29'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*Editor’s Note: Michal Biniek is a frontend developer on the Innogames Lagoonia team, and an enthusiast of JavaScript and new web technologies like HTML5/CSS3, WebSockets, and WebRTC. Back in November, michal.b took 2nd place in the MDN Developer Derby with Rob in Soundland, a fanciful Canvas demo.*

It was the fourth time one of Michal’s demos made to the Derby finals, and it was the third time he’d placed. If you’ve been following Dev Derby since it launched last year, you might remember seeing [Fly, fly!](https://developer.mozilla.org/en-US/demos/detail/fly-fly) or [Too Many Fish in the Sea](https://developer.mozilla.org/en-US/demos/detail/too-many-fish-is-the-sea). Congratulations Michal, we can’t wait to see your next demo! Submissions are now open for upcoming Derbies: CSS 3D transforms, Audio, and the Web Sockets API.

![photo](https://hacks.mozilla.org/wp-content/uploads/2012/02/photo-250x332.jpg)


**Tell us about developing Rob in Soundland and where your idea came from?**

My first idea for the Canvas demo was to prepare some kind of visualization – a sound visualization which could make a nice connection between two senses – vision and hearing. I thought it would be also nice if the user could interact with the application through keyboard or mouse.

Finally I decided to prepare a simple game with third-person view in an infinite world, where the main character – Rob – wanders through the colorful (almost psychedelic) squares which are playing different notes.

Interesting fact is that the game doesn’t contain any external media elements like images or sounds. Everything is generated using HTML5 technologies: Images are pre-generated at the start of the game and sounds are created and played ad hoc using the [Audio Data API](https://wiki.mozilla.org/Audio_Data_API).

**Do you remember your first computer and your first website?**

My first computer was [Elwro Junior](http://pl.wikipedia.org/wiki/Elwro_800_Junior) – the Polish version of a ZX Spectrum computer ([English description here](https://hacks.mozilla.org/www.old-computers.com/museum/computer.asp?st=1&c=951)). A few years later I got my first PC with a 486 25MHz processor inside and a magical ‘turbo’ button.

My history with websites started around 1999 when I prepared a site about my hobbies – skiing and astronomy. I even put some animations using JavaScript and [DHTML](http://en.wikipedia.org/wiki/Dynamic_HTML) (a buzzword from long ago):



How did you get started coding and hacking?

I started coding on [ZX Spectrum](https://hacks.mozilla.org/en.wikipedia.org/wiki/ZX_Spectrum) in BASIC, but shortly after that I moved to Turbo Pascal on the new PC. I think it is also important that my father was an IT teacher at school – so when I had some problems with programming I could always ask him for help.

For me, the visual is one of the most important aspects of an application. That’s why I found Delphi/C++ Builder a really nice solution for building UIs. This is also the reason why I liked HTML from the beginning – as a perfect language for UIs, which with JavaScript is much easier to run animations rather that trying to run it on forms.

**You mentioned you’re from Wroclaw, Poland, and work as a Web developer for Innogames? Do you work remotely? What tools do you use for development?**

Actually, I live in Hamburg, where I got the software developer job at Innogames half a year ago. However, I still quite often visit Wroclaw.

I’m working in team that works on [Lagoonia](http://en.lagoonia.com), one of the latest games developed by Innogames. Modern Javascript engines in browsers enable us to take full advantage of JavaScript (and new features from HTML5 like sound and canvas). We can create games which easily compete with Flash-based games without additional runtime machine!

I usually use [Eclipse](http://www.eclipse.org) to develop JavaScript applications. I find it a quite good code editor (however sometimes slow) with code auto-completion that works quite well. For testing and debugging, I use Firebug and the built-in console in Firefox, one of the best debugging tools for web applications ever.

**Do you play online games? What games influence your work? What do you play the most these days?**

I discovered online games while I was a student. I started with FPS shooters then switched to MMORPGs like MuOnline. I think that multiplayer games are the future of gaming – it is usually much more fun to play with real players rather than against a computer.

My current company – Innogames is also focused on online games (mainly browser games) where the most important part is cooperation with other users.

We can still observe old games (even from the days of the ZX Spectrum) refreshed with new fancy graphics and multiplayer mode which are bestsellers nowadays. However, many indie games show us completely new concepts of games – and I think these types of games influence me the most.

Apart from that, I really like [Valve games](http://www.valvesoftware.com/games/) – especially for great stories in games like Half Life/Portal universum.

**The Nyan Cat version of your August History API demo reminded us how fast memes can travel on the Internet. Tell us about Fly, fly! and how the idea came to you?**

It was quite hard to find an original idea for the usage of History API, which in my opinion is prepared especially for websites using AJAX to set up the content. However, it could also be used as a timeline for virtual travels. The initial idea for this project was a flight by plane through the different cities.

However I found it boring and I decided to add the popular Nyan Cat – one of the most positive memes – as an optional mean of transport. This choice causes the Nyan Cat to leave a rainbow-colored contrail in the sky, instead of leaving white lines, which makes the world more colorful and friendly for people.

In addition, everything was matched to the original concept of the demo, even the different graphics looks much better – dark background, Nyan Cat instead of a plane, and a colorful path for the journey.

**You’ve submitted 7 Dev Derby demos since the program launched, and 4 of them have placed as finalists. Congratulations and thank you! Are you working on another demo? Any other cool projects you want to tell us about?**

Thank you! Currently I’m working on another simple game using [touch events](https://developer.mozilla.org/en/DOM/Touch_events), however a project grew up a bit and I’m not sure if I’ll find enough time to finish it before the deadline.

![zombie-kiwi-touchevents-demo Zombie-kiwi-touchevents-demo screenshot](https://hacks.mozilla.org/wp-content/uploads/2012/02/zombie-kiwi-touchevents-demo1-500x323.png)


In the meantime I’m working with my colleague Barry Nagel on our own framework for HTML5 games, which is named [Machine5](http://machine5.com). The goal of this project is to find the simplest way to create stunning HTML5 games and to provide a simple and easily maintainable project structure for developers.


When you think about HTML5 & new Web technologies what are you most excited about?

I’m really glad that the [Canvas element](https://developer.mozilla.org/en/HTML/Canvas) is currently widely available and I can freely use it. It is a perfect solution for simple games – and I hope soon WebGL will be also available on all browsers, because it is a great feature that allows creating fullscreen games. Using these technologies together with new audio APIs and WebSockets or WebRTC as a communication stream, we can soon expect real FPS games like Counter Strike or a less violent type of game such as Sims MMO version ;)


Anybody else who helps on your demos? Anyone you want to mention?

I’d like to thank to Robert Zatycki for all the brainstorms about possible ideas for games and other applications. Some concepts which we were talking about were used in games.

And I’d also like to thank to my brothers – Paweł and Łukasz who tested carefully my demos before I released them and for their frank feedback.

**What inspired you to participate in Dev Derby? Can you say something more about Open Source, Mozilla and why you contribute?**

Before the Dev Derby contest, I’d prepared some demos for Chrome Experiments and for Opera Widgets websites. Then I got a message from John Karahalis, where he mentioned a new Mozilla project for demos especially for new technologies.

Currently I find the [MDN](http://developer.mozilla.org) is one of the best resources for [JavaScript](https://developer.mozilla.org/en/JavaScript). All the work done by Mozilla to contribute, prepare and promote new technologies is great and really important for the modern internet. Firefox is one of the most popular web browsers, (and in Poland the most popular!) which I think is the best example that users also appreciate Mozilla’s excellent product.

One idea of Open Source is really important: even nowadays when almost every concept can be patented, there are still a lot of people who are open to sharing their experience with other developers without any profit. I find that sharing code can be the best way to get feedback about code quality and to get suggestions for other possible (sometimes better) solutions for an application.