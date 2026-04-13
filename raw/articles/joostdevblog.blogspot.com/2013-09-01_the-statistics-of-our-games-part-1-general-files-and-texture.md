---
title: 'The statistics of our games, part 1: General, files and textures'
url: http://joostdevblog.blogspot.com/2013/09/the-statistics-of-our-games-part-1.html
author: Joost van Dongen
published: '2013-09-01'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[Kickstarter campaign](http://www.kickstarter.com/projects/ronimo/awesomenauts-starstorm)for our big Starstorm expansion to Awesomenauts. While we were preparing for that, I was thinking about how much Awesomenauts has grown since launch, and how much further it would grow by creating the Starstorm. Being a programmer, I love numbers and started collecting data on just how much Awesomenauts has been growing. Today I would like to share the first half of those with you! Since I like comparing, I have also added the other games I have worked on: De Blob, Snowball Earth, Swords & Soldiers and Proun. Hopefully you will find this as fascinating to look at as I do!

But first, let me abuse this moment to blatantly market

[our Kickstarter campaign](http://www.kickstarter.com/projects/ronimo/awesomenauts-starstorm)... ;) We have already reached our main goal, and there are still tons of fun things in the stretch goals, including releasing our

[editors](http://www.youtube.com/watch?v=41CCE3BFiqA)for modding. So please help make those features possible by backing the Starstorm, and scoop up lots of goodies in the reward tiers!

Below are just our own statistics, so since I love comparing numbers, I would love to see what went into other games! If you are a professional game developer and would like to share your stats, please come back next week to download the complete spreadsheet, fill in any details of your own games you would like to share, and send them back to me! If enough people do this, I will do another blogpost in a while with all the stats that we will have collected.

Enough talk, let's get to The Big Table Of Data!

![](../../assets/b10819fe4ae8159f.jpg)

## General | ![]() | ![]() | ![]() | ![]() | ![]() | ![]() | ![]() |
| Developer | pre-Ronimo | Ronimo | Ronimo | Ronimo | me | Ronimo | Ronimo |
| Release date | 30-06-06 | cancelled May '08 | 15-05-09 | 02-12-10 | 22-06-11 | 01-08-12 | 28-08-13 |
| Graphics type | 3D | 3D | 2D | 2D | 3D | 2D | 2D |
| Platforms for this version | PC | PC | Wii | PS3 PC Mac Linux | PC | PC PS3 Xbox360 | PC Mac Linux |
| All platforms this game was released on at some point | PC | none | Wii PS3 PC Mac Linux iOS Android 3DS | Wii PS3 PC Mac Linux iOS Android 3DS | PC | PS3 Xbox360 PC Mac Linux | PS3 Xbox360 PC Mac Linux |
| Time between first version and final version (might contain long inactive periods) | 5 months | 1 year | 1 year | 2.5 years | 6 years | 3 years | 4 years |
| Active development duration | 5 months | 1 year | 1 year | 2 years | 3 years | 3 years | 4 years |

Let's first have a short look at what games we are comparing here exactly:

[De Blob](http://blob.oogst3d.net/): This is the original student project that the later console games by THQ were based on. We made De Blob with a team of 9 students, of which 5 are among the 7 founders of Ronimo.[Snowball Earth](http://www.proun-game.com/Oogst3D/Blog.php?page=2012/10/the-history-of-snowball-earth-now.html): This was to be the first big project by Ronimo. We intended for it to be released as a disc-based console game, but we never found a publisher and it was cancelled after working on it for one year.[Swords & Soldiers Wii](http://www.swordsandsoldiers.com/): Our first real game! This is the original version of the game as it launched on the Wii.[Swords & Soldiers HD](http://www.swordsandsoldiers.com/): This is the port of Swords & Soldiers to Playstation 3, PC and Mac. It added HD graphics and online multiplayer.[Proun](http://www.proun-game.com/): This is my personal hobby project, so this is not a game by Ronimo Games.[Awesomenauts console, with patch 1.1](http://www.awesomenauts.com/): Awesomenauts as it is on console right now. This is not the launch version of the game: Coco and Derpl were added after launch in patch 1.1 and this version includes them. That makes this version functionally the same as the PC launch version of the game.[Awesomenauts current version](http://www.awesomenauts.com/): Awesomenauts as it is right now on Steam, on PC, Mac and Linux, with patch 1.22.

*not*simply equal how much work was spent making the game. Team sizes have varied enormously for these games. For example, Proun was mostly made by just me, and in my spare time, so Proun's 3 years of development are only a fraction of the 3 years of Awesomenauts development time.

## Files | ![]() | ![]() | ![]() | ![]() | ![]() | ![]() | ![]() |
| Size of all files in repository | ? | 5.5gb | 7.4gb | 28.3gb | 40.3gb | 97.4gb | 200gb |
| Files in repository | ? | 17979 | 18723 | 36219 | 31050 | 34957 | 98288 |
| Installed game size | 235mb | 426mb | 17mb | 282mb | 347mb | 500mb | 879mb |
| Files in installed game | 1331 | 10582 | ? | 801 | 974 | 550 | 716 |

As you can see here, our repositories are huge. 200gb for just the current version of Awesomenauts! The reason for this is that we store all files in the repository, not just source code. Photoshop files are often hundreds of megabytes and we store it all in the repository. This way everyone has quick access to everything, and it gets backed up automatically. When we started doing this during De Blob, over 7 years ago, SVN was still painfully slow, but by now computers have become so fast that we can do a repository of hundreds of gigabytes easily.

Size is hardly related to amount of work here: Proun has a 40gb repository because of the footage I captured for trailers, but in reality Swords & Soldiers is of course a much bigger production than Proun.

Note how few files the installed version of Awesomenauts has compared to all the other projects, especially taking into account that it is a much larger production (probably as large as all the others combined). Having few files in the installed game is a really good thing: reading 100 files of 10kb each is

*much*slower than reading 1 file of 1mb, so the small number of files in Awesomenauts represents a big optimisation that made loading much faster.

The question marks, by the way, are simply because those games are pretty old and I don't have all the data at hand anymore. I might have been able to dig it up, but that just took too much time.

## Textures | ![]() | ![]() | ![]() | ![]() | ![]() | ![]() | ![]() |
| Textures | 260 | 1188 | 587 | 634 | 317 | 3250 | 4800 |
| Total texture size | 72mb | 201mb | 55mb | 183mb | 210mb | 350mb | 833mb |
| Maximum simultaneous texture usage in video memory | 72mb | 201mb | 55mb | 183mb | 106mb | 200mb | 332mb |
| Sprite sheets (one sheet often contains several animations) | n/a | n/a | 67 | 68 | n/a | 125 | 255 |

These numbers nicely show how little relation there is between megabytes and actual amount of work. Swords & Soldiers on the Wii uses only one third of the texture memory of Swords & Soldiers HD on PC and PS3, but these are in fact the same textures, only saved at a higher resolution and with a different compression algorithm. Since our artists had drawn the textures for the Wii version at a much higher resolution than what went into the game, doubling the resolution for the HD version cost very little time. So the numbers are much higher, but the actual amount of work is not. Keep this in mind for all the numbers in these tables: comparing them without context can result in some very wrong conclusions!

Another interesting thing here is the difference between 2D games and 3D games. I am a big fan of the subtle lighting one can get using pre-baked lightmaps, and these have been used in all 3D games here: De Blob, Snowball Earth and Proun. So of the 317 textures in Proun, 275 are actually lightmaps, totalling 150mb. It is important to keep that in mind when comparing to Awesomenauts, where textures are mostly hand-painted. So although Awesomenauts 'only' has 70% more texture megabytes than Proun, those probably correspond to 100x more work!

Since launch, the total texture size in Awesomenauts has increased much more than the texture memory usage. This is because most of those new textures are sprite sheets for characters and skins and we have a dynamic texture streaming system in place that only loads those textures that are actually being used. A whopping 500mb of all textures in current Awesomenauts are character sprite sheets that are streamed this way.

That's it for today! I have collected many more numbers, so next week I will be back with the second half of this post, elaborating on assets, sound and source code. See you then!

*Edit: Here are the other parts of this series:*



## No comments:

## Post a Comment