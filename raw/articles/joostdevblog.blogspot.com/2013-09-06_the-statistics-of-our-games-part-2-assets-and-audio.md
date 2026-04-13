---
title: 'The statistics of our games, part 2: Assets and audio'
url: http://joostdevblog.blogspot.com/2013/09/the-statistics-of-our-games-part-2.html
author: Joost van Dongen
published: '2013-09-06'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[the first part of the statistics from our games](http://joostdevblog.blogspot.nl/2013/09/the-statistics-of-our-games-part-1.html). Today let's look at the second part: numbers about assets and audio. Plus a bunch of (hopefully) interesting contemplations and anecdotes about them. In fact, I had intended to also include stats about code today, but I typed so much text about all of this that I had to split it further. This series is now three blogposts instead of my originally intended two.

Before I continue, let me abuse this moment for a short commercial break by (again) marketing

[our Kickstarter campaign for the Awesomenauts: Starstorm expansion](http://www.kickstarter.com/projects/ronimo/awesomenauts-starstorm)! Including PayPal pledges we have by now reached the first stretch goal (a new map) and are working towards the second stretch goal: Custom Games!

Now, let's get to the actual numbers!

## Assets | ![]() | ![]() | ![]() | ![]() | ![]() | ![]() | ![]() |
| Levels | 1 | 1 | 42 | 42 | 5 | 3 | 4 |
| Skeletal animations | 12 | 82 | n/a | n/a | 0 | n/a | n/a |
| Particles systems | 2 | 10 | 43 | 43 | 2 | 526 | 751 |
| Animation templates | n/a | n/a | n/a | n/a | n/a | 1774 | 5582 |
| 3D models | 835 | 2240 | n/a | n/a | 332 | n/a | n/a |
| Text lines (per language) | ? | ? | 1250 | 1611 | ? | 2200 | 3200 |
| Languages | 1 | 1 | 6 | 6 | 1 | 6 | 6 |
| Settings | 71 | 267 | 2200 | 2200 | 183 | 22500 | 59820 |
| AI/script files | n/a | 6 | 83 | 103 | 106 | 44 | 69 |
| Vertex shaders | 8 | 22 | 0 | 3 | 12 | 3 | 3 |
| Pixel shaders | 7 | 22 | 0 | 14 | 25 | 32 | 32 |
| Materials | 146 | 1038 | n/a | n/a | 283 | n/a | n/a |

Here it becomes immediately obvious how ridiculously large a production

[Awesomenauts](http://www.awesomenauts.com)is. For almost all the numbers here, Awesomenauts is a big factor larger than the other games. That is why it took us a full three years of development to finish that game... Had we known it was such a monster production, we probably wouldn't have started working on it in the first place, but seeing what an enormous success it is now, this makes it totally worth it!

The other thing to notice here is how much Awesomenauts has grown since launch. Going from 8 to 15 characters is a big jump, as is adding a new map and skins. I have seen some questions as to why we are doing a Kickstarter for Starstorm, and I think these numbers make it quite obvious: there is just an enormous amount of work in creating all this new stuff! The 22 major patches we have done since release represent an enormous effort on our side, and to make an even bigger step now with the Starstorm expansion, we need new funding. And we are getting it: the Kickstarter has already achieved the main goal and the first stretch goal, so let's see how much further these numbers will grow in the coming period!

Comparing AI files in these projects is unfortunately pretty meaningless, since their structure and size vary too much. For example, in

[Proun](http://www.proun-game.com)AI files are simply recordings of me racing the track, each AI file costing only a couple of minutes to create. In

[Swords & Soldiers](http://www.swordsandsoldiers.com)and Awesomenauts however these can be

*massive*scripts, made by our designers in our

[AI editor](http://joostdevblog.blogspot.nl/2010/12/ai-in-swords-soldiers-part-1.html)(which has evolved quite a lot since the blogpost in that link, by the way).

The craziest number here is the number of settings in Awesomenauts. Almost sixty thousand! These settings govern the exact behaviour of all gameplay: weapons, skills, characters, turrets, etc. Many of those settings are set to neutral: for example, Lonestar's standard bullets don't have gravity, stun, silence or blind. So a large portion of these settings exist, but are not 'active', so to say. Nevertheless, those settings do exist. Managing so many settings became a big problem for our game designers, so a while ago we built a special dedicated editing tool for them. This greatly simplified categorising, searching and managing settings. This tool was built by our former coding intern Eric Castermans, who got a job at

[Triumph](http://www.triumphstudios.com/)after he graduated. He is now working on the awesome

[Age Of Wonders 3](http://www.ageofwonders.com/), one of the games I am personally looking forward to most at the moment. The guys at Triumph demoed it to us recently and it is looking to be incredible fun, can't wait to play it myself!

## Audio | ![]() | ![]() | ![]() | ![]() | ![]() | ![]() | ![]() |
| Sound effects | 58 | 166 | 89 | 89 | 39 | 288 | 530 |
| Sound effects: size on disk | 3.5mb | 100mb | 1.7mb | 1.7mb | 2.2mb | 37mb | 60mb |
| Voice samples | 0 | 0 | 105 | 105 | 0 | 429 | 1180 |
| Voice samples: size on disk | 0mb | 0mb | 1.6mb | 1.6mb | 0mb | 80mb | 208mb |
| Music: number of songs | 5 | 2 | 4 | 4 | 4 | 32 | 48 |
| Music: total duration | 13:59 | 9:43 | 9:59 | 21:48 | 9:33 | 1:17:35 | 2:03:29 |
| Music: size on disk | 12.7mb | 13.3mb | 2.6mb | 20.6mb | 8.8mb | 97mb | 146mb |

I think the most surprising thing in these audio numbers is how

*short*the soundtracks of Swords & Soldiers and Proun are, while this hardly bothered anyone while playing. If you listen to a lot of game soundtracks, this is something you might have be aware of: game soundtracks are often surprisingly short, without this ever being a problem during the game. For example, a boss fight with a one minute loop is often totally fine. So if you are working on your first game and think you need a full hour of music, then think again: you can probably do just fine with

*much*less. (The more the better, of course, but that goes for many things.)

The duration of the current Awesomenauts soundtrack is quite bloated by the fact that our killing spree songs change into normal songs after about a minute. Those normal songs are also in the soundtrack, causing those parts to be double. So about one hour of music should be deducted from the length of the current Awesomenauts soundtrack for a fair comparison. In the launch version of Awesomenauts about 30 minutes should be deducted for the same reason.

These numbers also show nicely how everything becomes more complex as a game grows. If you make the same game with twice as many assets, it is much more than twice as much work. You can see this here in the size of the voice samples for Awesomenauts. This grew from 80mb to 208mb in the past year. 80mb is still an acceptable size to just put into memory entirely. With 208mb, it is getting to the point where having all of that in memory at once might be problematic for older computers. So as it grows even further, there might come a point where we need to build some dynamic streaming system for voice lines. This would depend on which characters are in a match, just like we have a multithreaded streaming system for character textures. When such a system becomes necessary we will need to store voices differently to make them easily streamable. We will also need to categorise them to know which file belongs to which character, and we will need to built that whole streaming system. A lot of extra work! This makes everything more complex while it remains essentially the same game, just with more voice lines.

One final thing to note here is how ridiculously small the Swords & Soldiers Wii soundtrack is on disk: only 2.6mb for 9:59 minutes of stereo music! And it actually sounded pretty good: we never got a single complaint about low sound quality. This was made possible by the OGG sound format, which can achieve astoundingly good sound quality at ridiculously low file sizes. In general, OGG is smaller and higher quality than MP3. Combine that with the fact that using an MP3 decoder costs licensing money, and I am quite surprised that MP3 is still used so much more than OGG.

![](../../assets/12e777cada0ad468.gif)

That's it for today! Tune in next week for the final part of these statistics: source code!

*Edit: Here are the other parts of this series:*



This made me realise the amount of work that awesomenauts costs, as I thought it to be a 'simple 2D game'.

ReplyDeleteKeep up the good work! (we want those custom games!)

That is a ridiculous amount of animation templates. I can only imagine the process you have to go through in order to create new skins for each of the chars.

ReplyDeleteYeah, most animations go in five directions (up/forward/down/45 degrees up/45 degrees down), so each character and skin already has a big bunch of animations just for the basic stuff (idle/walk/jump/wall/slide).

DeleteYou mentioned OGG, what other Open Source libraries do you use?

ReplyDeleteSDL, FreeType, PThreads, Squish, TinyXML.


DeleteOn Snowball Earth, De Blob and Proun also Ogre and ODE.