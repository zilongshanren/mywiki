---
title: Designing against motion sickness in Proun
url: http://joostdevblog.blogspot.com/2010/10/designing-against-motion-sickness-in.html
author: Joost van Dongen
published: '2010-10-30'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[Proun](http://www.proun-game.com)was shown on

[Kotaku](http://kotaku.com/5670563/proun-looks-fast-and-it-looks-gorgeous)and

[Gametrailers](http://www.gametrailers.com/video/debut-trailer-proun/706334). Most reactions were extremely positive (awesome, woohoo! ^-^ ), but there were also quite a few remarks about people fearing motion sickness when playing the game. I totally agree that this is a serious issue with this kind of game, so I constantly took it into account with a lot of design decisions. I tested Proun on large flocks of people at different occasions and the nice result of my work against nausea is that it is pretty rare for people who actually

*play*Proun to get motion sickness.

The emphasis on the word

*play*in that previous sentence is important: watching someone play the game or, even worse, watching a video montage of it, is actually a lot more nauseating then playing yourself. The reason for this is simple: the camera only rotates when you steer, so when you play yourself, you see the camera movement coming. This really makes a huge difference, so playing the game yourself is a lot better than watching that trailer.

Preventing motion sickness was an important argument for a lot of design decisions in Proun, especially concerning the camera. A great help is that I have designed and coded quite a few camera systems in other games already: De Blob, Swords & Soldiers, Ronimo's secret new game and the cancelled 3D game that we were developing at Ronimo before we made Swords & Soldiers. Those camera systems weren't necessarily great, but at least I learned a lot while programming them!

In general, an important cause for motion sickness is camera smoothing. Without smoothing, camera movement may look very blocky and ugly. However, smoothing also means that the camera does not directly follows the player's movements, since it must add a little bit of delay to smooth things out. I experimented with smoothing a lot for Ronimo's cancelled 3D game, and it turned out that certain types of extreme smoothing cause almost instant nausea, but that even the tiniest bit already has this effect to a small extent. With a lot of smoothing, the camera may never stand still. So for Proun, I chose not to have any camera smoothing at all. I did experiments with it, but all the smoothing schemes I applied caused too much nausea for Proun's own good.

The reason motion sickness is so important for Proun specifically, is that there is no up or down. The camera constantly rotates the world around and there is no horizon to focus your eyes on. Even the cable whooshes and curves by real fast. So I chose to position the player's vehicle at the centre of the screen and to always keep it there, without zooming or looking around it. This way the ball replaces the horizon as the stable factor on the screen.

Proun may still result in motion sickness a bit quicker than other games, but because of the counter-measures I took in the camera design, I think this is solved well enough. Playtesting shows that most people can play this crazy rotating game as well as any other 3D game. :)

## No comments:

## Post a Comment