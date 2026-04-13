---
title: Global Game Jam 2012 Liveblog
url: https://etodd.io/2012/01/27/global-game-jam-2012-liveblog/
published: '2012-01-27'
source_blog: Evan Todd
source_site: https://etodd.io/
category: game programming
fetched: '2026-04-13'
---

# Global Game Jam 2012 Liveblog

**Update:** Snakes in a Tower is complete! [Downloads with source available for Mac and PC](http://globalgamejam.org/2012/snakes-tower).

**Friday 4:59pm**

This is my first Global Game Jam. Super excited. So I'm going to liveblog it. I'll be working on a MacBook, so I decided to port the essentials of my XNA component entity system over to MonoGame. Here's what I got so far!

![](../../assets/e5e7048d213d8233.jpg)


Breathtaking, I know.

**Saturday 12:20am**

Opening meeting was awesome. Heard some fantastic keynotes from fantastic people. We got to hear some great insight from Ian Schreiber before starting (I'm at the Ohio State jam). The theme has been given to everyone by now, so I'll go ahead and say that the theme is this:

![](../../assets/a425ad3ae4419fee.png)


We heard a lot of great ideas that seem quite achievable. I think we'll see some great things come out of this jam. I had an idea to do a prison game where the goal is to escape and every room is the same, and it turns out the prison is infinite and there's no way to escape. Pretty lame idea, but one of the few artists expressed interest and joined my group.

We brainstormed for a while and came up with some interesting ideas. Most interesting was an idea to make the game a bit like Shutter Island. The player begins by strangling a prison guard until he passes out. As he goes through the prison, he finds clues that suggest things are not as they seem. Eventually he discovers that he's actually a patient at a mental insitution, and all he has to do to escape is talk to the guard at the beginning.

Interesting idea, but not very related to the theme, and probably out of scope of the game jam. Then suddenly my partner had a great idea that's very scalable. It will work with just the basic gameplay elements, but could eventually be expanded to a full-blown title. I won't say too much about it yet, but it takes the theme very literally.

My partner and I got along so well that we actually grabbed some food and talked for over an hour and a half. So not the best start as far as getting work done, but honestly the main reason I wanted to do this game jam was to connect with people, and so far that's gone great.

Now we've gone our separate ways to work on our individual areas. I'll be wrestling with MonoGame and Box2D, and he'll be working on some of the art. Tomorrow we have a room in the Ohio Union from 9:00am to 1:00am, and I think it's gonna be a great day! I'm very excited about our game design.

In other news, apparently MonoGame has XACT support in the works... which might have far-reaching consequences for Project Lemma. But that's for another time! For now I have to get to work.

**Saturday 2:40am**

Box2D.XNA is compiling and I have a sprite displaying. MonoGame is working pretty well. Taking a break from coding to post this masterpiece giving a peek of the final gameplay:

![](../../assets/93a1e45e04ac4045.jpg)


Basically, it's a giant snake tearing through a skyscraper. It lengthens as it eats people. Your goal is to survive and direct the snake by opening doors, building obstacles, etc. Eventually the snake gets long enough that you can trick it into eating its own tail, and then you win!

**Saturday 5:03am**

Bed time. Got Box2D.XNA working and figured out the SpriteBatch weirdities.

**Saturday 12:55pm**

We started around 9:00am today. We have some artwork in progress (although not in-game yet), and a pretty decent snake. I'm planning on implementing all the game logic with Box2D sensors sized automatically to our artwork. Here's a screenshot.

**Saturday 7:49pm**

Hit some frustrating bugs. I was pretty grumpy before I got some Chipotle in me. On the plus side:

- The snake's basic AI is done.
- Stairways are basically implemented.
- The game has been successfully tested on Mac and PC.
- We've got some nifty art now.
- The project is officially entitled "Snakes in a Tower". Yep.

Here's a screenshot:

**Saturday 9:32pm**

Things are finally shaping up! I think I've discovered a fascinating gameplay element. Since the snake gets longer by eating victims, the player has an incentive to feed them to the snake. Originally we were going to have the victims randomly run out of office doors, but now I think it would be better if they only come out when the player actively opens the door. Man, this is going to be a morbid game.

**Sunday 1:24am**

Calling it a night. We added the innocent victims AKA python food. When you open an office door they literally explode outward and basically run around like headless chickens. They also have the ability to traverse stairways, resulting in a lot of random door slamming. The victims also tend to stack up and fall to their death in the elevator shafts. All in all, it's enormously entertaining.

Also, if you leave a door open to a stairwell, the snake will always take it, smashing the staircase and emerging enthusiastically on the other side. Soon the player will be able to repair the staircases so he and the victims can use them again.

Here's a screenshot of the whole fiasco.

Tomorrow I'll finish up the repair functionality, add sounds, a life counter, and polish things like a basic main menu and game over screen. If we have time we'll work on a pistol to fight off enraged PETA supporters.

Also, check out this fantastic logo courtesy of our artist!

**Sunday 9:10pm**

Whoops, I sort of went dark today. Busy polishing!

**Conclusion**

Global Game Jam 2012 has come to a successful end! All the games presented at our local event were fully functional and quite a bit of fun. I ran into some technical difficulties literally at the last minute; we kind of held everyone back. I felt bad, but we were so close to perfection! :P

Here's a screenshot of the final game:

And here's the gameplay trailer:

I learned a lot from this game jam. A lot of people say they learned to start very small and fight feature creep, but I think we had that under control from the get-go. The idea would have been a decent success even with less features than we got done, which is one of the big things I took away from this jam.

If you frequent game development forums, you'll often see new people with great ideas and no experience. And everywhere in the threads, in the stickies, in the FAQs, you'll see little blurbs telling these people that ideas are worthless, and the real value is in the execution. I think I've bought into this mindset a little too much. Before this jam, I didn't realize how long it's been since I've actually made a drop-dead simple game that's just about pure fun mechanics. I spend most of the time on my game projects writing things like voxel renderers, script engines, and nice editors, features that don't directly impact gameplay. I skip right past the gameplay stage and go straight to the hard stuff.

This game jam has taught me how much depth a gameplay mechanic can add to a game. I'm definitely going to revise my techniques in the future because of it.

The one thing I regret is not spending enough time talking to people and helping them out with their games. I think I would have learned even more if I had done that, and I certainly could have helped other people learn more. I spent most of my time dealing with technical issues which taught me nothing I didn't already know. Next time I think I might just float between groups helping people, because if I decide to take responsibility for a project, I now know it will become a matter of personal pride and I'll take it way too seriously. :)

That's all folks! Download the game and source [here](http://globalgamejam.org/2012/snakes-tower). Thanks for reading everyone. Back to Project Lemma next week.