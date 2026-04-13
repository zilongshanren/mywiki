---
title: 'Unity games in WebGL: Owlchemy Labs’ conversion of Aaaaa! to asm.js – Mozilla
  Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2014/10/unity-games-in-webgl-owlchemy-labs-conversion-of-aaaaa-to-asm-js/
author: Alex Schwartz
published: '2014-10-14'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

You may have seen the big news today, but for those who’ve been living in an Internet-less cave, starting today through October 28 you can check out the brand spankin’ new [Humble Mozilla Bundle](https://www.humblebundle.com/). The crew here at [Owlchemy Labs](http://owlchemylabs.com/) were given the unique opportunity to work closely with Unity, maker of the leading cross-platform game engine, and Humble to attempt to bring one of our games, Aaaaa! for the Awesome, a collaboration with Dejobaan Games, to the web via technologies like WebGL and asm.js.

I’ll attempt to enumerate some of the technical challenges we hit along the way as well as provide some tips for developers who might follow our path in the future.

## Unity WebGL exporter

Working with pre-release alpha versions of the Unity WebGL exporter (now in beta) was a surprisingly smooth experience overall! Jonas Echterhoff, Ralph Hauwert and the rest of the team at Unity did an amazing job getting the core engine running with asm.js and playing Unity content in the browser at incredible speeds; it was pretty staggering. When you look at the scope of the problem and the technical magic needed to go all the way from C# scripting down to the final 1-million-plus-line .js file, the technology is mind boggling.

![](../../assets/1b9a191054f52e79.jpeg)


Thankfully, as content creators and game developers, Unity has allowed us to focus our worries away from the problem of getting our games to compile in this new build target by taking care of the heavy lifting under the hood. So did we just hit the big WebGL export button and sit back while Unity cranked out the html and js? Well, it’s a bit more involved than that, but it’s certainly better than some of the prior early-stage ports we’ve done.

For example, our experience with bringing a game through the now defunct Unity to Stage3D/Flash exporter during the Flash in a Flash contest in late 2011 was more like taking a machete to a jungle of code, hacking away core bits, working around inexplicably missing core functionality (no generic lists?!) and making a mess of our codebase. WebGL was a breeze comparatively!

## The porting process

Our porting process began in early June of this year when we gained alpha access to the WIP WebGL exporter to prove whether a complex game like Aaaaa! for the Awesome was going to be portable within a relatively short time frame with such an early framework. After two days of mucking about with the exporter, we knew it would be doable (and had content actually running in-browser!) but as with all tech endeavors like this, we were walking in blind as to the scope of the entire port that was ahead of us.

Would we hit one or two bugs? Hundreds? Could it be completed in the short timespan we were given? Thankfully we made it out alive and dozens of bug reports and fixes later, we have a working game! Devs jumping into this process now (October 2014 and onward) fortunately get all of these fixes built in from the start and can benefit from a much smoother pipeline from Unity to WebGL. The exporter has improved by a huge amount since June!

### Initial issues

We came across some silly issues that were either caused by our project’s upgrade from Unity 4 to Unity 5 or simply the exporter being in such “early days”. Fun little things such as all mouse cursor coordinates being inverted inexplicably caused some baffled faces but of course has been fixed at the time of writing. We also hit some physics-related bugs that turned out to have been caused by the Unity 4 to Unity 5 upgrade — this led to a hilarious bug where players wouldn’t smash through score plates and get points but instead slammed into score plates as if they were made of concrete, instantly crushing the skydiving player. A fun new feature!

Additionally, we came across a very hard-to-track-down memory leak bug that only exhibited itself after playing the game for an extended session. With a hunch that the leak revolved around scene loading and unloading, we built a hands-off repro case that loaded and unloaded the same scene hundreds of times, causing the crash and helping the Unity team find and fix the leak! Huzzah!

### Bandwidth considerations

Above examples are fun to talk about but have essentially been solved by this point. That leaves developers with two core development issues that they’ll need to keep in mind when bringing games to the Web: bandwidth considerations, and form factor / user experience changes.

Aaaaa! Is a great test case for a worst case scenario when it comes to file size. We have a game with over 200 levels or zones, over with 300 level assets that can be spawned at runtime in any level, 48 unique skyboxes (6 textures per sky!), and 38 full-length songs. Our standalone PC/Mac build weighs in at 388mb uncompressed. Downloading almost 400 megabytes to get to the title screen of our game would be completely unacceptable!

In our case, we were able to rely on Unity’s build process to efficiently strip and pack the build into a much smaller size, but also took advantage of [Unity’s AudioClip streaming solution](http://docs.unity3d.com/ScriptReference/WWW-audioClip.html) to stream in our music at runtime on demand! The file size savings of streaming music was huge and highly recommended for all Unity games. To glean additional file size savings, Asset Bundles can be used for loading levels on demand, but are best used in simple games or when building games from the ground up with web in mind.

In the end, our final *compressed* WebGL build size, which includes all of our loaded assets as well as the Unity engine itself ended up weighing in at 68.8 MB, compared to a *compressed* standalone size of 192 MB, almost 3x smaller than our PC build!

### Form factor/user experience changes

User experience considerations are the other important factor to keep in mind when developing games for the Web or porting existing games to be fun, playable Web experiences. Examples of keeping the form factor of the Web include avoiding “sacred” key presses, such as Escape. Escape is used as pause in many games but many browsers eat up the Escape key and reserve it for exiting full-screen mode or releasing mouse lock. Mouse lock and full-screen are both important to creating fully-fledged gaming experiences on the web so you’ll want to find a way to re-bind keys to avoid these special key presses that are off-limits when in the browser.

Secondly, you’ll want to remember that you’re working within a sandboxed environment on the Web so loading in custom music from the user’s hard drive or saving large files locally can be problematic due to this sandboxing. It might be worth evaluating which features in your game you might want to be modified to fit the Web experience vs. a desktop experience.

Players also notice the little things that key someone into a game being a rushed port. For example, if you have a quit button on the title screen of your PC game, you should definitely remove it in your web build as quitting is not a paradigm used on the Web. At any point the user can simply navigate away from the page, so watch out for elements in your game that don’t fit the current web ecosystem.

Lastly you’ll want to think about ways to allow your data to persist across multiple browsers on different machines. Gamers don’t always sit on the same machine to play their games, which is why many services allow for cloud save functionality. The same goes for the Web, and if you can build a system (like the wonderfully talented Edward Rudd created for the Humble Player, it will help the overall web experience for the player.

## Bringing games to the Web!

So with all of that being said, the Web seems like a very viable place to be bringing Unity content as the WebGL exporter solidifies. You can expect Owlchemy Labs to bring more of their games to the Web in the near future, so keep an eye out for those! ;) With our content running at almost the same speed as native desktop builds, we definitely have a revolution on our hands when it comes to portability of content, empowering game developers with another outlet for their creative content, which is always a good thing.

![](../../assets/9522a511b2fbd55b.jpg)


Thanks to [Dejobaan Games](http://www.dejobaan.com/), the team at [Humble Bundle](https://www.humblebundle.com/), and of course the team at [Unity](http://unity3d.com/) for making all of this possible!

## About
[
Alex Schwartz ](http://owlchemylabs.com)

Founder, CEO, and Janitor of Owlchemy Labs. http://owlchemylabs.com

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 6 comments

Jay SherbyOctober 14th, 2014 at 13:12Alex SchwartzOctober 15th, 2014 at 09:29Bill LambertOctober 14th, 2014 at 14:01Robert McGovernOctober 14th, 2014 at 14:08DanielOctober 14th, 2014 at 16:47VytenisOctober 15th, 2014 at 05:04