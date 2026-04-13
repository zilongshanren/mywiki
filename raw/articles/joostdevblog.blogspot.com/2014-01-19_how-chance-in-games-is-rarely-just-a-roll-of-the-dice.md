---
title: How chance in games is rarely just a roll of the dice
url: http://joostdevblog.blogspot.com/2014/01/how-chance-in-games-is-rarely-just-roll.html
author: Joost van Dongen
published: '2014-01-19'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[Awesomenauts](http://www.awesomenauts.com)we have experienced this first hand, especially in the various versions of Leon's crits, which has been changed several times in patches during the past 1.5 years. Last week I mostly talked about the

[psychology of crits](http://joostdevblog.blogspot.nl/2014/01/the-surprisingly-many-subtleties-of.html), and today I am going to look at chance in games in general.

When a programmer is told to implement a random for something, he will often simply use

*std::rand()*or something similar and that's it. However, in practice it turns out that both players and designers rarely really want a truly random chance.

A good example of this can be found in level selection in Awesomenauts: in a practice match there are four levels to chose from, and there is a 'random' button to select random levels. With a true random, the random button might result in playing the same level several times in a row. There is a small chance that a player gets the same level 4 times in a row (1.5625%, to be exact), and even 10 times the same level in a row is possible. When this happens, both players and designers start to voice complaints like “the random is not random, it always selects the same map”. Of course, in a truly random dice roll, the chances of throwing a number are completely independent of what was thrown before that, so even a million times the same value in a row can happen. The chance of that happening is just really small.

![](../../assets/5b47f850336e73e3.jpg)

So what every game programmer needs to realise, is that when a designer asks for random, he rarely asks for a complete random. The random usually needs some extra logic to keep unwanted situations from happening. In Awesomenauts, the game remembers which map you last played and does not select it again for the next match (although if you join matches, you might still join several matches in a row with the same map). Similarly the music player remembers the last four songs it played and does not select those again when it chooses the next song to play. And I imagine that in a random dungeon generator it is likely not desirable to put instances of the same room next to each other.

An important part of random is human perception. Humans are exceptionally good at recognising patterns. In fact, humans are so good at this that they often recognise patterns where there are none. Noteworthy situations are remembered, while other situations are not. Astrology is for a large part based on this. If only one out of ten predictions turns out to be correct, many people will tend to remember that one correct prediction and not the nine false ones, making it possible for charlatans to pass for real predictors of the future.

Something similar goes for the perception of random in games. We have had numerous reports from players that the map they dislike most is selected much more often by the random map selection. However, every player who reports this reports it for a different map, and our random is just fine. What really happens there, is that people remember every time they get the map they don't want, and don't really remember what other maps they played recently.

Human psychology is therefore an important part in designing random. A great example of this can be found in one of my favourite game series: Civilization. Sid Meier did a

[hilarious presentation](http://www.youtube.com/watch?v=bY7aRJE-oOY&t=18m24s)on how they modified their random in Civilization Revolution. One of the things they did is that if a unit has 90% chance to win, this is treated as 100%, because it turned out that it always felt unreasonable to lose when the win chance was 90%. Another trick they did is that if a number of 50% battles in a row are all lost, then at some point the next one is automatically won, because it simply feels unfair to lose so often in a row.

Of course, with a mechanic like that it is important to either keep players from knowing it works like that, or to keep a bit of random in there, because otherwise knowing how this works will result in exploitable tactics. If there is one thing we learned during development of Awesomenauts and

[Swords & Soldiers](http://www.swordsandsoldiers.com), it is that if something

*can*be abused, it

*always will*!

![](../../assets/e5aa9da8083b9318.gif)

Inspired by the Civilization article, we started playing with Leon's crit chance. The original implementation we had for this was simply a clean chance. However, this sometimes resulted in having two or three crits in a row, which is incredibly powerful. Dying from this felt unfair, because it did so much damage that there was little opportunity to get away from it.

To solve this we modified the crit chance to never happen twice in a row, and also to never fail ten times in a row. This way the crits are still random, but the situations that feel unfair don't happen anymore.

This worked fine and had the desired result, but what we did not realise is that it massively changes the actual crit chance! With a 15% crit chance, the chance of it missing 10 times in a row is a surprisingly high 19.7%. Adding a guaranteed extra crit so often increases the crit chance significantly! So in that particular patch we accidentally buffed Leon a lot, making him pretty overpowered.

We did not realise we had done this until players started counting. They quickly noticed that Leon had become a lot stronger, but we simply didn't believe them. To convince us that something was wrong, a couple of players performed several hundred attacks in a row and counted how many crits they got. Even then we still didn't believe them at first, but once we understood what was happening here, we modified the crit chances to be the same as before again, including the extra rules for consecutive hits.

![](../../assets/47c0526bc6c64a42.jpg)

*Image by Awesomenauts player 'Offline' (I think).*

This brings me to the end of this blogpost. As the various topics I have discussed today have shown, there is much more to chance, luck and random in games than just using pure random functions. Whenever random is involved, the designer and programmer should always consider what they want exactly, since in practice it turns out that a true random is quite rarely wanted.

well, tbh Joost: You guys still don't get many things in the Awesomenauts-Game. I've seen so many threads in the official message board and still the dev-team seems do not care at all how broken Raelynn and Yuri are because as far as I can judge the whole situation you only prefer to hear Nikos opinion on the matter. Why does Yuri mines still stack? Why is Rae's sniping so powerful? Why not compensate the damage for lenght? Why does have Leon to lose his tongue during cloaking when you could instead give him a timer of 20-30 secs?



ReplyDeleteI've never seen a reaction from you guys to the problem. And yes, I would say that you're as ignorant as you all have been with the Leon-Crits. I think most problems could be easily balanced for the moment until you guys have time to improve the whole AI Station map which is a problem for itself.

thanks for reading

Ironic to say the least.







DeleteAccusing of ignorance when one swims in it.

Compare Awesomenauts with Dota or League.

The balance in Awesomenauts is AMAZING to say the least. You can pick literaly any naut and have a decent chance to win.

Try doing that in the other games. Currently there's a tournament for LoL and out of about 20 matches and 100+ characters a range of 30 has been picked or banned.

Raelynn has a fair cooldown on her snipe. if you stay away from it before she uses it you can capitalize enough.

She is good at pushing. but Lonestar can do just better.

Yuri mines are probably the easiest thing to avoid in the game. "But they block the path!" that's because you let a fragile naut free roam around. Yuri has so many counters it hurts.

I do somewhat agree that AI station feels and plays different than other maps and also favors certain nauts / comps. However it can be fixed by letting you know which map will play before the match starts.

I don't think this is the right place for a discussion like that. This a article about the effect with example of Joost his experience in Awesomenauts. If you want to discuss balance there is a section on the official Awesomenauts forum for that and there are plenty of people in there who can tell you why the Realynn and Yuri comment are not really a problem. Leons tongue is a somewhat more controversial topic.

DeleteOne of the other things we learned is that no matter what we do with balance, players will never agree and it is impossible to make everyone happy. ;)

DeleteAwesome... Awesome... Awesomenauts!!!!!!!! I'M TED MCPAIN!

ReplyDeleteJoost, dont mind the trolls. Awesomenauts is heading in the right direction. Keep up the good work!

ReplyDeleteHow is the Random on character selection handled in Awesomenauts? It feels that I always get Swiggings, Yuri or Vinnie & Spike.

ReplyDeleteIt just picks a random character, there is no tendency towards Swiggins, Yuri or Vinnie. As said in the blogpost, humans are really good at seeing patterns where there are none, you probably just got them a couple of times randomly. :)


DeleteHowever, if you go back from the loadout screen and retry random without first playing with your random character, it will select the same character again to avoid abuse of the random character XP bonus.

I'm sure you know this, but I'm not sure whether it is used in Awesomenauts. Another way to improve the players' perception of randomness is to store every case for a given situation inside an array, shuffle the array, and then popping each case until you reach the end, repeating the process over and over. If you try that, I would like to read your results here. Thanks for the post

ReplyDeleteI know of that method, but I don't really like it all that much, because after a while it starts repeating. I think the method of remembering what was recently played and picking randomly from the rest yields a more random situation with similar benefits of not picking the same thing shortly after each other. I'd say for 10 things to choose from, one should remember 5 and pick randomly from the other 5.

DeleteAn interesting read! I did a series on youtube where I prestiged while only playing random naut and I decided to gather the statistics for it just for some fun. What I found out was fairly interesting. Even though I FELT like I would always play one map or another they turned out fairly even. Even the split between colours was very close to 50%. And that's for a sample size of 63. The selection of nauts still seemed less random but with so many options there's bound to be some repeats :P

ReplyDelete(Statistics if you're curious:

Raw Data - https://drive.google.com/file/d/0B4zRQ3pr3-RpZVZMb29Vbkh4ZFVoWnVNQlhXc0FwemEzeWkw/edit?usp=sharing

Handy Dandy Graphs of crap - http://i.imgur.com/F3W0uaR.png ) I've already gathered the data for my second season but I have yet to analyse it because I am a lazy bum :P But I assume it would be similar to the previous season.

Nice to see: good to hear from an actual user who felt like he got the same map too often but really didn't. Players are really stubborn at this topic. ;)


DeleteThe map you thought you got too often, was that the map you like least?

Its been awhile but it sounds about right. At that time I really disliked Aguilion because of the stealth orb and the frustrations resulting from that. But honestly I don't remember.


DeleteAll this talking has gotten me to finally crunch the numbers from the second season :P Fairly similar results:

52% Red/47% Blue - 20% Agu/23% Sor/30% AI/25% Rib

but again the character randomizing was a little in favor of a few nauts but not as bad as the previous one :P (Plus test size was slightly smaller because I'm so much more pro at the game than the first season ;P)