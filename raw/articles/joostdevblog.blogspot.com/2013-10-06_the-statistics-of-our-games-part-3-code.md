---
title: 'The statistics of our games, part 3: Code'
url: http://joostdevblog.blogspot.com/2013/10/the-statistics-of-our-games-part-3.html
author: Joost van Dongen
published: '2013-10-06'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[files and textures](http://joostdevblog.blogspot.nl/2013/09/the-statistics-of-our-games-part-1.html)and about

[assets and audio](http://joostdevblog.blogspot.nl/2013/09/the-statistics-of-our-games-part-2.html). Today we get to the final part of this short series: code!

Code is where size matters most. Not because creating 751 different particle systems wasn't a lot of work for our artists, but because unlike with particles, every additional line of code makes every existing line of code more complex. No matter how many particle systems there are, when creating one, an artist only has to care about that single particle system. The rest hardly matters. With code, the opposite is true: the larger a codebase, the more complex it all becomes. Of course, object oriented design principles say everything should be separated as much as possible, and this is a goal we work hard for, but in practice that is just not always doable.

For example, the 15 characters in

[Awesomenauts](http://www.awesomenauts.com)all need to interact with each other. Any skill from any character needs to be able to handle interfering with any other skill correctly. With weird stuff like timebubbles, cocoons and chains, and more weird stuff for every new character, it becomes nearly impossible to truly untangle all the code into small, clear subsystems that don't suffer from the complexity of the rest of the code. Now add to that our goal to make everything editable by our designers in real-time while playing, and it just explodes.

This is why the 290.156 lines of code in current Awesomenauts looks like so much to me. Handling gameplay complexity in code is to me the biggest challenge in coding. It is something that is hardly taught at computer science schools and of all coding topics, this is the most difficult thing to do well, in my opinion. We have tons of discussions internally on how to structure gameplay code as well as possible, and it remains a fascinating and interesting topic that with experience can be done better and better, but always remains a complex challenge.

Note that another reason why Awesomenauts is so many lines of code, is that most of our tools are in-game, and are thus part of this count. Having in-game tools gives great features and a much better workflow, but also inflates the codebase quite a bit.

![](../../assets/b10819fe4ae8159f.jpg)

Let's have a look at the actual statistics:

## Source code | ![]() | ![]() | ![]() | ![]() | ![]() | ![]() | ![]() |
| Programming language | C++ | C++ | C++ | C++ | C++ | C++ | C++ |
| Number of files | 153 | 385 | 717 | 1077 | 215 | 2495 | 3221 |
| Code lines (excluding comments / whitelines) | 12814 | 35000 | 67790 | 112096 | 19220 | 216572 | 290156 |
| Lines of comments | 1067 | 3331 | 3568 | 7108 | 1530 | 12423 | 16986 |
| Whitelines | 2926 | 8356 | 14280 | 24977 | 4504 | 56457 | 73547 |
| Total size | 436kb | 1204kb | 2241kb | 3866kb | 712kb | 7877kb | 10912kb |
| Classes/structs/enums (approximately) | 70 | 180 | 190 | 500 | 100 | 1050 | 1350 |
| Average lines per file | 109,85 | 121,26 | 119,44 | 133,87 | 117,46 | 114,41 | 118,19 |
| Percentage comments | 6,35% | 7,13% | 4,17% | 4,93% | 6,06% | 4,35% | 4,46% |
| Percentage whitelines | 17,41% | 17,90% | 16,67% | 17,32% | 17,83% | 19,78% | 19,32% |

An interesting thing here the difference in code size between Swords & Soldiers Wii and Swords & Soldiers HD. That is 65% extra code for essentially the same game! This extra code is spread out over three different topics: new platforms (PC/Mac/PS3), new control schemes, and, above all: online multiplayer. I have said it before and I'll say it again: adding online multiplayer as a feature to a game makes it twice as much work to program. These numbers show it, and our experience building online multiplayer in Swords & Soldiers and Awesomenauts

*definitely*shows it. Online multiplayer is really complex and a lot of work to create! No matter how complex you think it is, if you have never made a commercially released game with proper online multiplayer (including invites and all that kind of stuff), then no matter how much work you think it is, you are probably underestimating it.

One thing I think is quite funny here, is how constant the number of white-lines is in all of these projects, despite having various different programmers working on them and many years in between. The reason for this is that we still use most of the coding standard I designed early, and this explicitly states how white-lines are used, since they are a form of communication and can be used to structure code. So no matter who codes at Ronimo, the pattern in using white-lines is always quite similar.

(As you might have guessed from this, our coding standard is very strict in comparison to what most other companies use. This is a very deliberate choice I made, so I might get back to why that is and share our complete coding standard in a future post at some point.)

This ends my analysis for today. As I said last week, I'd love to see such numbers from other games! So if you are a professional game developer and would like to share your stats, please do so! I'll collect whatever people send me and post the results here in a future article (assuming anyone sends their stats, of course). My email-address is at the top of the spreadsheet. If you don't feel like sharing specific things, then just leave those out, and only share whatever you are willing or allowed to. I did the same with some of the extra stats I added to the document. You can download the spreadsheet, just fill it in and send it back to me. I have added some extra fields for those who wish to share more. If you have extra categories you'd like to add, feel free to add them at the bottom. Here's the document:


[Statistics Spreadsheet.xls](http://www.proun-game.com/Oogst3D/BLOG/Statistics%20Spreadsheet.xls)I counted my source lines and such with

[Microsoft Line Of Code (LOC) Counter](http://archive.msdn.microsoft.com/LOCCounter/Release/ProjectReleases.aspx?ReleaseId=115). This tool does not give a whole lot of data, so if anyone knows a tool that can actually give more stats on code, then please let me know! I'd love data like number of classes, number of variables per class, average function length, number of functions per class, etc. I couldn't find a tool to get that kind of information, so let me know in the comments below if you do.

That's it with the numbers for now! I hope you enjoyed viewing these as much as I have! ^_^

Very interesting post (as ever!). Would love to read about the complete coding standard :)

ReplyDeleteHi! There is an open source project that extract code metrics from java, C and C++ code. It's name is Analizo. He goes the site: http://analizo.org/

ReplyDeleteHope it helped! I love Awesomenauts and follow your dev blog, because I'm Software Engineering student and love those kind of info. Keep up with the great work guys!

Maybe a tool like sonar is what you are looking for?



ReplyDeletehttp://www.sonarqube.org/

My experience with it at work is quite positive. It can do all the statistics you mentioned above, but also checks for complex methods, duplicate code etc. It also integrates really nicely into most builservers.