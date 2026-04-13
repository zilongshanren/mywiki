---
title: Introducing the editors of the Ronitech
url: http://joostdevblog.blogspot.com/2012/11/introducing-editors-of-ronitech.html
author: Joost van Dongen
published: '2012-11-11'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

*If you don't feel like reading through this entire blogpost, be sure to scroll down to*

**the video**in the middle for a demonstration!Those who read my blog from the very beginning, might remember a blogpost that went by the illustrious title

[Designing Levels Without Tools](http://joostdevblog.blogspot.nl/2010/12/designing-levels-without-tools.html). When we made

[Swords & Soldiers](http://www.swordsandsoldiers.com), I was the only programmer at

[Ronimo](http://www.ronimo-games.com), so I had to resort to drastic measures to be able to develop a complete console game in one year. The result was that our designers had a rather odd level design tool: Notepad... So much has changed since then!

[Awesomenauts](http://www.awesomenauts.com)was made with a larger team over a longer period of time and in this time we managed to make top-notch tools. So today, I would like to introduce the editors of the Ronitech!

![](../../assets/6c3ba1cdac20201b.jpg)

We have three in-game editors, plus an in-game AI debugger, which can step through our AI trees. The in-game editors are a Level editor, a Particle editor and an Animation editor. Next to that, we also have an

[AI editor](http://joostdevblog.blogspot.nl/2011/01/ai-in-swords-soldiers-part-2.html)and a Settings editor. The latter is not in-game, but edits can be reloaded in-game at any time, thus still allowing for interactive gameplay settings editing. Note that the animation editor is not used for actual frame-by-frame animation (our artists use After Effects for that), but for adding particles, effects, sounds and game-triggers to animations.

![](../../assets/38461cabf1eaff95.jpg)

At Ronimo we are firm believers in

*iteration*. We think it is impossible to make final designs of any elements beforehand. Everything needs to be tried in the actual game, and then tweaked to make it work best in the game. Of course, if you make a clone of an existing game, it is possible to design everything on paper, but if you want to do any kind of innovation, then iteration is extremely important.

For this reason, one of the core principals of our tech team is that our designers and artist must be able to tweak everything as easily and quickly as possible. Now what is easier than tweaking during gameplay? With this in mind, most of our editors were implemented inside the game, instead of externally as is common for most editors.

When an editor is opened by simply pressing F1, F2, F3 or F4 while in a game, the game pauses and the editor overlays come up. Artists and designers can switch between our editors and the gameplay at any point, and can even continue playing while in the level editor. (This is of course disabled in the released game. We almost forgot about that: the editors were turned off in release versions only one or two days before we launched the beta of Awesomenauts on Steam...)

The editors were made over the course of four years, mostly by interns. I made the core components of the in-game editors myself, but from there our interns Ted, Niels, Bart, Thijs, Eric and Rick worked on them to really turn them into a useful and rich toolset. They did a great job, and Thijs and Ted actually now work at Ronimo.

Our editors have a ton of features, including:

- Game can be played while editing
- Several artists/designers can edit the same level at the same time over the network, seeing each other's edits in real-time
- Complete undo/redo
*Everything*is animateable- Edits to animations or particles are immediately reflected during actual gameplay
- Graphics look exactly the same on all platforms, so artists can comfortably work on their PC and don't need to use the more laborious console devkits
- AI debugger

Of course, none of this is as interesting as actually seeing the editors in motion, so here is a video that demonstrates the core features:

One of the funniest features is in the editing over the network. During a six-player match of Awesomenauts in our office, our designers can open the level editor at any given time and tweak some stuff. This is great to fix a misplaced platform or something like that, but it can also be abused nicely. At one point, one of our designers got bored and started to slowly rotate the entire level

*while the rest was still playing in it*. Chaos and hilarity ensued...

Having the editors in the game does have its downsides. Gameplay code is more complex because editor and game are so intertwined. Another issue is that everything needs to be able to be updated at any time, which makes some optimisations impossible. Building our editors this way definitely cost us some performance, but with a lot of optimisation work I did manage to get proper framerate: Awesomenauts now mostly runs on 60fps on Xbox 360 and Playstation 3, and rather old PCs can still run it fluently.

I expect some Awesomenauts players who read this will wonder why these tools are not available to them to make mods with. The main reason for this is that modding doesn't really work without a proper modding infrastructure. You need to be able to share your levels online, and play with others online. Getting this exactly right is a lot of work, because we need to take care of things like people having different versions of the same level and such. So turning our in-house tools into a functional modding toolset would be an enormous amount of work...

In future blogposts, I will dive into some of the specifics of our editors, explaining the most interesting aspects of how these tools were made and how our artists use them to make animations and such.

As you might have guessed from the text in this post, I am incredibly proud of the tools we have today. I think in the world of 2D games, few companies have better tools than this (of course, the

[Rayman](http://www.youtube.com/watch?v=B_QhZYTukac)folks probably easily beat us there...).

You bunch of tools! ;) As always, a very interesting post to read. Was that animation in the middle made specifically for this blog, or is it part of a pitch to offer your tools as middleware? (The next Call of Duty powered by Ronitech.)

ReplyDeleteMade just for this post! This trailer made me realize again that this blog might be too much work for my own good... Too much fun to make, though!

DeleteCan you re-record voice of Derpl or Raelynn, cause there is same actress voice now, and it’s annoying. Thanks!

ReplyDeleteHaha, lol! Raelynn and Derpl are absolutely not the same actress. They are not even from the same country!

DeleteI meant Coco and Derpl, sorry.

DeleteAnother great post-congratz Joost!





ReplyDeleteI envy your animatorów editor- working on 2D anims in Unity, as we do, just ani't so easy.

Are you planning to sell your engine and tools or this is just a show-Off post ;) ?

We're all great fans of your work at Crunching Koalas, visit our blog it you care!

Cheers!

I heard Unity is undergoing some great improvements for 2D, but I never used it myself, so I have no idea how good it is by now.



DeleteWe are considering selling our engine, but it is not ready for that yet (no documentation and for the moment too interwoven with our games). This post serves mainly as context for future posts about our workflow. And you are right, also to show-off the tools, because I am pretty proud of what we have. :)

I checked your blog, but there is nothing to see there yet, right? Looks like you will be announcing the name of your first game soon? Good luck making something awesome!

Thanks for sharing Joost! I look forward to learn more details on your content and iteration pipeline.

ReplyDeleteVery nice and inspirational. Now I'm more motivated to make a runtime-editable framework for settings and other properties to use in my own code.

ReplyDeleteI'm absolutely in love with the 2D art style you guys produce. I would love to intern with Ronimo but sadly, I have no understanding of the Dutch language.

ReplyDeleteThis is really impressive. Folks, you did an amazing job! A couple of questions if you don't mind :)



ReplyDelete1) Do you use version control for your assets? And if yes, which one?

2) Do you have a central assets/configs repository where changes made in the editor are saved? Or changes are saved into some local developer's repository from where they can be pushed into the central one.

3) How much easily new AI properties can be added in the editor? Are these properties dynamic and can be added by a game designer or there is predefined amount of them and new ones can be added by a request to a programmer?

4) You mentioned it was possible to share the editor over the network. Does it mean it's possible to run the game on the console in the dev. mode and connect to it with the editor client from PC?

Thanks!

1) Yes, we use SVN for everything. We don't just use it for our code, but also for our art assets, so Photoshop files of hundreds of megabytes are also on the SVN. I think a complete checkout of all our projects is currently around 400gb... Works great against artists accidentally overwriting each other's work and such, we can always get everything back from the SVN history! :)




Delete2) Everything goes through SVN. If several artists edit a level together, one of them just saves at the end and submits the result to the SVN.

3) There is an older blogpost about this, about our AI editor in S&S. In short: each type of AI block has an XML definition for in the editor, and a corresponding C++ class that contains the actual behaviour of that block. So designers cannot add new types of AI blocks, but coders can usually add new ones in a couple of ours. There are so many blocks now, though, that they rarely add for new ones. It is rather complete already.

4) The editors don't work on console, since we didn't make a non-mouse interface and we didn't make mouse support on console either. No need for that: console devkits are much slower to use than normal PCs, and the game looks the exact same on all platforms, so PCs are just easier. I spent quite a bit of time making sure all platforms render and play the exact same. The only reason an artist or designer would ever want to run on a console, is because televisions show things different than PC monitors. But it is also possible to just attach a PC to a TV for that.

Hey Joost! Awesome blogs! I was wondering if you could make a future blog about the collision system you guys used for Awesomenauts?


ReplyDeleteI would be very interested in your techniques!

Keep it up!

Hmm, I am not very happy with our collision systems. The collision detection itself is fine, but the way I handle how collisions are solved for characters is very hacky and easy to break. I feel like I still don't understand how to really build a stable system for that. On my blog I usually try to write about topics for which I feel like a have a good grasp of them, so I probably won't tackle that one... If you come across any good articles on how to do 2D platformer collision handling while still keeping good gameplay control (which real physics engines usually don't provide), then please link them here, as I'd love to read more about that!

DeleteYay! Really happy to be named in your blog.

ReplyDeleteVery interesting to know all this stuff !

Hello Joost,




ReplyDeleteI am creating an Unreal Engine 4 plugin for collaborative level editing via network. I noticed that you created the same feature in your editor

and I was wondering if you have some tips for me. For example: what happens when a client in the session disconnects and reconnects?

And how do you solve a situation when multiple clients edit the same object at the same time? Maybe you have some other examples that could be an issue? Would love to hear your knowledge and point of view on this topic!

You can find more info about my plugin in this Unreal Engine forum thread: https://forums.unrealengine.com/showthread.php?50688-MultiEdit-Collaborative-Level-Editing-Plugin&highlight=multiedit

Thanks in advance!

We handled this somewhat naively, which works fine and was really simple and quick to add (a couple of days at most since we already had online multiplayer).





DeleteWhen several people edit the same object, it just ends up in one of their states. The games does not try to resolve this. This means they might end up in different states depending on packet order. We never resolved this because users are in the same room and can easily keep from doing this in the first place. Also, it is not much of an issue because the object ends in a valid state, just not a combined state of both edits.

As for connecting/reconnecting: whenever a user connects he receives a full level update from the host. When someone edits something everyone else immediately receives the edits. When a user reconnects he just gets the latest version from the server again. So reconnecting is not really a very special case.

Important for us is that one of the users need to actually save the file to disc and commit it into our SVN (version management system). They need to coordinate who does this.

The main trick we use is that we just send over the network whatever we would write to a file while saving. An object is saved as an XML so when editing an object I just send the XML for that object over the network. Really simple, that's why we made this feature in the first place.

Thank you for your reply, really helpful!

Delete