---
title: How a lack of art influences prototyping results
url: http://joostdevblog.blogspot.com/2011/11/how-lack-of-art-influences-prototyping.html
author: Joost van Dongen
published: '2011-11-06'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[Awesomenauts](http://www.awesomenauts.com), I learned that working from such abstract prototypes can also steer your design in certain directions, which is not always an improvement.

What really made me realise this is the jumping mechanics in Awesomenauts. Since we didn't have any art for this new game yet at that point, we made the very first gameplay prototypes for Awesomenauts using characters from

[Swords & Soldiers](http://www.swordsandsoldiers.com). However, these characters don't have any jumping animations, since Swords & Soldiers doesn't feature any jumping.

![](../../assets/a15e8d2310506e5a.jpg)

Now at some point our game designers wanted to add some weight to the movements of the characters, so they proposed that the characters would need to really push off the ground when jumping, and really land after a jump instead of immediately continuing to walk. Since we didn't have any art for this yet, I implemented this by simply adding a short pause before jumping and after landing. So when you press jump, the character takes 0.5 seconds before going up, and after landing he pauses 0.5 seconds before continuing to walk.

In terms of pure game mechanics, this is the entire thing. The only difference between this and what would be in the final game, is that these 0.5 seconds pauses would have specific animations for pushing off and landing. So in terms of abstract game prototyping, this was a complete prototype with all the mechanics in it.

Yet is played horribly: it simply felt like the game's controls were slow and lagging behind, not like the character had more weight and presence in the world. So we threw out the pauses after a couple of short internal playtests.

At this point I realised that the reason these pauses felt bad was

*not*that the mechanic in itself was wrong. The reason it felt bad was that

*there were no animations*. If there is no animations, then the 0.5 seconds pause before jumping is simply a delay on your controls. You press the jump button and nothing happens for a little while. Yet when there are animations, something does happen immediately: the character bends through his knees and pushes off the ground. The delay between pressing the button and moving up is the same with and without animation, yet the feedback is way better when there is animation, because the character immediately reacts to your button press, even though he doesn't immediately start moving up.

To me this was an interesting realisation: it is not always possible to use abstract prototyping to see whether a mechanic works! Sometimes you need proper art and animations to know whether the gameplay is any good.

Note that in this case, squashing the character before and after a jump would already have been a big improvement, because this way at least the graphical feedback would have been immediate.

So the prototype was not a good enough test. But was not having these extra animations a good choice? I still think it was: Awesomenauts is a very fast skill-based game and quick and direct controls are incredibly important, so we would have wanted immediate jumping anyway. So despite the incomplete test, I definitely think we made the right choice.

![](../../assets/08c34c4d789afc93.jpg)

Of course, this is totally different for each game: for a game like Assassin's Creed, the subtle animations really make the game, and make it feel like the character is really climbing those walls and has real weight. So it really depends on the game whether the delay that is added by in-between animations is a good thing or not.

![](../../assets/0f9fd418b0b31471.jpg)

So whether you have animations in your prototype or not greatly influences the core feel of your gameplay. The same applies to many other assets. Here are a couple of examples of situations where prototyping with or without sound and graphics can make a big difference on what the conclusions of the prorotype are:

-Games are way more fun with sound. Half the intensity and thrill you feel while playing a game comes from the audio. However, often sound designers are contracted rather late in development, so you usually don't have the real sound effects during the first half of development. For Swords & Soldiers, we fixed this in an easy way: we simply copied the sound effects from Warcraft III and used those temporarily. As soon as the real sound effects by

[Sonic Picnic](http://www.sonicpicnic.nl/)were created, we threw out all the Warcraft III sound effects. But until that time, we had a much better feel for the actual game, because we actually had any sound at all.

-When looking for the right style of music for a game, a common quick prototyping method is to simply put on the music outside the game and then start playing to see whether it feels right. This is of course a good idea, but it also influences the attachment between the music and the game negatively. The problem is that the timing of the music is not linked to the game when you do this, because you have to start the track outside the game. It works

*much*better if the music is started at the exact same time as a level, because now the music is not part of everything outside the game any more. I noticed this with several games now: music never really feels right until the timing of starting and stopping the music is right. Adding this timing to a prototype is usually really simple and helps a lot.

-A really obvious example is guns in a shooter. The most important thing for a gun in a shooter is that it feels right and has serious impact. Since 80% of the feeling of impact for a gun comes from the graphics and the sound, and only 20% from the actual gameplay and damage of the gun, it is impossible to really prototype guns if you don't add any audio and visuals. However, creating those well is a lot of work, so I guess you have to start without, but until you have sound, I don't think you can really tell whether a certain concept for a gun is an awesome idea or not.

-The Aztec Sun Giant and the Viking Frost Hammer in Swords & Soldiers are rather similar soldiers in terms of abstract game design: slow, specialist units that deal area of effect damage and shortly put the enemy out of battle (through respectively knockback and stun). When playing the game without graphics, one might conclude that they are too similar, except for their large difference in price and health. So maybe more variation is needed? No, not really: when the art is added, these two units feel really unique and different, making them work really well in the game. Again, prototyping without art might not have been a good idea for these two units.

![](../../assets/969f38713114e59f.jpg)

The most important realisation from this whole topic is that the prototyping

*method*greatly determines the outcome. Prototyping gameplay with or without graphics and audio gives different conclusions about which mechanics work, and it is important to realise that this is the case. Of course, I am absolutely in favour of prototyping early and often, even if you don't have any art yet, but I do think trying to add some sound and graphics as early as possible greatly helps, even if they have been ripped from other games for the time being.

There is a more general lesson here as well. This post was just about graphics and audio, but I think the prototyping method

*always*influences the outcome. Paper prototyping, prototyping in editors from other games: always keep in mind that the prototyping method used has some kind of influence on the outcome!

*PS. Woohoo,*three

[Proun](http://www.proun-game.com)has been nominated for the Dutch Game Awards in a whopping*categories: Best Visual Design, Best Original Game Design and Best Audio Design & Music! Incredibly cool! Only one other game was nominated in that many categories: Killzone 3. That is one really big and really good game, so it is an honour to get the same number of nominations! However, since Killzone 3 was developed by something like 200 people, and Proun by only two, Proun has a hundred times more nominations per person than Killzone 3!*[insert evil laughter here]

*Some other awesome games that got nominations are*

This is definitely something worth taking into account when prototyping. Thank you Joost, I found this very enlightening.

ReplyDeleteIt sounds like in this particular case, you did actually identify a valid way to prototype the jump without animation, by squashing and stretching the sprite in code. That seems to undermine your main point a little - there /are/ smart, fast ways to approximate more labor-intensive assets sometimes.



ReplyDeleteIn the case of the FPS weapons, yes a large part of what makes them work is the audiovisual feedback, but what question would such a prototype be trying to answer, besides "Can we make an audiovisually satisfying FPS weapon?" Usually prototypes should be built to answer questions that can't be answered with a simple thought experiment. One can imagine a prototype of the Gravity Gun from HL2 that lacked audiovisual feedback but proved that the basic concept was viable and worth spending art time on. (Of course, the actual history of that gun is that it started life as a debug tool!)

Agree completely that games like Assassin's Creed or Uncharted whose core gameplay depends heavily on intricate character animation state trees need some character animation done to properly assess what's working.

I totally agree that the point is more nuanced than how I wrote it, and you don't always need all kinds of assets for prototyping.


ReplyDeleteNote that ripping assets from other games for prototypes is also not labour-intensive and works really well. :)

As I learnt participating in several Game Jams, there are always ways to get good audio files for prototypes. Internet is full of free databases for things like steps, explosions or shattering glass, and several army webpages have humungous databases of free gunfire recordings.


ReplyDeleteAdd to that old games audio and Creative Commons music (lots of NIN multitracks are available this way) and you can get a pretty good feeling for your game.

With audacity, Myst and Riven' audio -extracted with Riveal- and NIN's multitracks you can have decent audio for your prototype in one morning.

P.S.: I've been unable to post using Firefox (versions 5 to 7.0.1 and Nightly 10.0a1) since I started reading your blog. Today I resorted to Explorer 9 (shiver) and it works.


ReplyDeleteApparently this blogger comment form has some issues with Firefox, and I've found this article (http://outerhoard.wordpress.com/2009/05/15/comments-problem-on-some-blogspot-blogs/) from 2009 regarding the same issue. I'll report the bug to blogger, but you might be losing a few comments because of this.

Cheers

Hmm, interesting, I didn't know about that commenting issue! Thanks for pointing that out to me!



ReplyDeleteI had a look, though, and the alternatives are a lot less inviting for commenting. This is the only way that has the commenting form right on the same page, instead of a small link in a corner to a separate page. So I'll leave it like this, but it is a pity if some people cannot comment because of an issue in Blogger... :(

PS. Interestingly, Blogger marked your post about an error in Blogger as spam... ;)

Another interesting article! :)


ReplyDeleteI'm now using Ogre/ODE (which I believe are the same technologies used for proun and de blob) and if you have time I would like to ask you a couple of questions about them (regarding fixed timesteps in the game loop) as I'm now fighting to get a good simulation with both VSync enabled and disabled. I wanted to ask you because you certainly have more experience than me with these matters. :)

May I ask it here or should I PM you somewhere?

Sure, go ahead! :)


ReplyDeleteUnless you don't want to ask your questions in public, you can just ask them here. If you prefer mail, send me an email to joost -at- ronimo-games.com.

Thank you so much! :)








ReplyDeleteI will ask them here then, as I think it's a problem that may interest others as well ;)

I'm using ODE (no wrappers) with Ogre. The game calls mRoot->startRenderLoop(), then the entire game loop is handled in ogre's frameRenderingQueued method. The game loop is pretty simple. I just use an accumulator adding the evt.timeSinceLastFrame every frame, then run a physics and logic update 60 times per second. (As i think i'm supposed to pass fixed timesteps to ODE to get a stable simulation).

The loop looks like this:

gameplayTS = 1/60.0f;

//Run at fixed framerate!

timeAcc += evt.timeSinceLastFrame;

while (timeAcc >= gameplayTS)

{

dWorldQuickStep(world, gameplayTS);

gameLoop(true, gameplayTS); //Logic update

timeAcc -= gameplayTS;

}

With this approach everything runs well, but ODE meshes don't move smoothly all the time as they sometime "jump" from one position to another creating an unpleasant stuttering. This is because evt.timeSinceLastFrame with VSync enabled isn't very stable. Most of the time is around 0.016 (60FPS) then it suddently jumps to 0.032 (30FPS) then down to 0.002, then back to normal. This causes ODE to stutter a bit, and these fluctuations are totally random. (Sometimes they don't happen at all)

With VSync disabled this problem is less frequent as there aren't noticeable fluctuations.

Since physics simulation in de blob and proun seemed very smooth, I wanted to ask you, are you relying on evt.timeSinceLastFrame for time checking and which kind of fixed timestep are you passing to ODE? Are you doing some kind of interpolation to avoid these problems?

I hope this post isn't too long ;)

The answer is rather simple: I have never used fixed timesteps! I just pass to ODE whatever the frame time is. Physics are supposedly less stable that way, but I have never noticed any problems because of this.





ReplyDeleteI guess this depends on the complexity of the simulation, though. De Blob is really simple in terms of physics (just one ball) and Proun doesn't even have physics: it only uses ODE for collision detection.

If you have lots of CPU time left, you can also simply choose a smaller timestep. If you would change gameplayTS to 1/180.0f, for example, the stuttering would probably be a lot less.

I actually don't know how to do fixed timestep AND efficiency AND smoothness AND handle framerate fluctuations well. However, there is an article that contains a long part on fixed framerate issues here:

http://www.gamasutra.com/view/feature/2280/the_guerrilla_guide_to_game_code.php

Thanks for you answer! I'll try that out. My physics test scene is very simple too, just one ball falling on the floor.


ReplyDeleteYep it's very difficult to handle all those things in a good way.. I'll try to see how variable timestep behaves :) thanks!