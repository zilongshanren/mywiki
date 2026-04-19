---
title: On Witchcraft
url: https://acko.net/blog/on-witchcraft/
author: Steven Wittens
published: '2021-02-10'
source_blog: Hackery, Math & Design — Acko.net
source_site: https://acko.net/
category: graphics
fetched: '2026-04-19'
---

![On Witchcraft](../../assets/0d89688e97858ae4.jpg)

# On Witchcraft

![Cover Image](../../assets/0d89688e97858ae4.jpg)

## Lies, damned lies, and social media

Rhetoric about the dangers of the internet is at a feverish high. The new buzzword these days is "disinformation." Funnily enough, nobody actually produces it themselves: it's only *other* people who do so.

Arguably the internet already came up with a better word for it: an "infohazard." This is information that is inherently harmful and destructive to anyone who hears or sees it. Infohazards are said to be profoundly unsettling and, in [horror stories](http://www.scpwiki.com), possibly terminal: a maddening song stuck in your head; a realization so devastating it saps the will to live; a curse that happens to anyone who learns of it. You know, like the videotape from *The Ring*.

Words of power are nothing new. Neither is the concept of magic: weaving language into spells, blessing or harming specific people, or even compelling the universe itself to obey. Like much human mythology, it's wrong on the surface, but correct in spirit, at least more than is convenient. Luckily most actual infohazards are pretty mundane and individually often harmless, being just dumb memes. The problem is when magical thinking becomes the norm and forms a self-reinforcing system.

This is a weird place to start for sure, but I think it's a useful one. Because that is the concern, right, that people are being *bewitched* by the internet?

![A witch offering a poison apple](../../assets/d3f9ddb3e10e5713.jpg)


## I.

Last year the following was [making the rounds](https://www.wsj.com/articles/facebook-knows-it-encourages-division-top-executives-nixed-solutions-11590507499), about polarization and extremism on Facebook, and their efforts to curb it. Citing work by Facebook researcher and sociologist Monica Lee:


The high number of extremist groups was concerning, the presentation says. Worse was Facebook’s realization that its algorithms were responsible for their growth. The 2016 presentation states that “64% of all extremist group joins are due to our recommendation tools” and that most of the activity came from the platform’s “Groups You Should Join” and “Discover” algorithms: “Our recommendation systems grow the problem.”

It's an extremely tweetable stat and quote, so naturally they first tell you how to feel about it. The article is rather long and dry, so we all know many people who shared it didn't read it in full. The current headline says that Facebook *"shut down efforts to make the site less divisive."* If you look at the URL, you can see it was originally titled: *"Facebook knows it encourages division, top executives nixed solutions."* So pot, meet kettle, but that's an aside.

While they acknowledge that some people believe social media has little to do with it, they immediately drown out the entire notion by referencing the American election and never mention this viewpoint again.

Don't get me wrong, I do think Facebook has problems, which is why I'm not on it. Optimizing mainly for time spent on the site is a textbook case of [Goodhart's law](https://en.wikipedia.org/wiki/Goodhart%27s_law): it's no surprise that it goes wrong. But a) that's not even a big-tech-specific problem and b) that's not what most people actually want changed when they cite this. What they say is that Facebook needs to limit "harmful content": they don't want Facebook to interfere less, they want it to interfere more.

This is in fact a very common pattern in all "disinformation" discourse: they tell you that what you are seeing is *specifically* abnormal and/or harmful, without any basis to actually justify limiting the conclusion. Like that anything about this is Facebook-specific. It's just that it's an easier sell to pressure one platform or channel at a time. It's not about what, but about who and whom.

There's also an assumption being snuck in. If a recommendation algorithm suggests you join a group, does the operator of that algorithm have a moral responsibility for your subsequent actions? If you agree with this, it seems Facebook should *never* recommend you join an extremist group, because extremism is bad. That sounds admirable, but is also not very achievable. It also hinges on what exactly is and isn't extreme, which is highly subjective.

Harmful content is for example *"racist, conspiracy-minded and pro-Russian."* So I doubt that they would consider e.g. the Jussie Smollett hoax or the hunt for the Covington Kid as harmful, seeing as they were sanctioned by both media outlets and prominent politicians. Despite being textbook cases of mass hysteria.

Calls for racially motivated action which result in violence, arson and anarchy under the Black Lives Matter flag also do not seem to count in practice. Facebook in fact placed BLM banners on official projects for most of 2020, as did others. The people who say we need to be deprogrammed seem to be doing most of the actual activism in the first place.

![Facebook's React urging people to donate to Black Lives Matter](../../assets/d3192f1df58ab76f.png)


*Facebook using its open-source projects to urge people to donate to political causes in an election year.*

Like most big social media companies, Facebook's claims of political impartiality ring hollow on both an American and international level. Plus, if you actually read the whole article, the take-away is that they have put an inordinate amount of time, effort and process into this issue. They're just not very good at it.

But it doesn't really matter because in practice, people will share one number, with no actual comparison or context, from a source we can't see ourselves. This serves to convince you to let a specific group of people have specific powers with extremely wide reach, with no end in sight, for the good of all.

Infohazard.

## II.

It's worth to ponder the stat. What *should* the number be?

First, some control. If 64% of members of extremist groups joined due to a machine recommendation, then what is that number for non-extremist groups? It would be useful to have *some* kind of reference. It would also be useful to compare to other platforms, to know whether Facebook is particularly different here. This is not rocket science.

Second, you should be sure about what this number is specifically measuring. It only tracks how effective recommendations are *relative to other Facebook methods of discovering extremist groups*, like search or likes. This is very different from *which recommended groups people actually join*. Confusing the two is how the trick works.

*The difference between P(Recommended | (Joined & Extremist)) and P((Joined & Extremist) | Recommended).*


They're talking about the thing on the left, not on the right.

If ~0% of group joins were due to a recommendation, that would mean the recommendation algorithm is so bad nobody uses it. It's always wrong about who is interested in something. You wouldn't even see this if e.g. right-wing extremism was being shown only to left-wing extremists, or vice versa, because both camps pay enormous attention to each other. You would basically only need to recommend extremist groups to 100% apolitical people. Ironically, people would interpret that as the worst possible radicalization machine.

They do say Facebook had the idea of *"[tweaking] recommendation algorithms to suggest a wider range of Facebook groups than people would ordinarily encounter,"* but seem to ignore that this implies exposing the middle to more of the extremes.

If ~100% of group joins were due to a recommendation, then that would imply the algorithm is so overwhelmingly good that it eclipses all other forms of discovery on the site, at least for extremist groups. Hence it could only be recommending them to people who are extremists or definitely want to hang out with them. This would be based on a person's strong prior interests, so the algorithm wouldn't be causing extremism either.

The value of *this* number doesn't really matter. The higher it is, the worse it sounds on paper: the recommendation engine seems to be doing more of the driving, even though the absolute numbers likely shrink. But the lower it is, the less relevant the recommendations must be, creating more complaints about them. It's somewhere in the middle, so nobody can actually say.

The *popularity* of extremist groups has nothing to do with *what percentage* of their members join *due to a recommendation*. You need to know the other stats: how often are certain recommendations made, and actually acted upon? How does it differ from topic to topic? If a particular category of recommendations is removed, do people seek it out in other ways?

The only acceptable value, per the censors, is if it becomes ~0% *because* Facebook stops recommending extremist groups altogether. That's why this really is just a very fancy call for censorship, using a lone statistic to create a sense of moral urgency. If a person had a choice of extremist and non-extremist recommendations, but deliberately chose the more extreme one... wouldn't that make a pretty strong case that the algorithm explicitly *isn't responsible* and actually just a scapegoat?

The article tells us that *"[divisive] groups were disproportionately influenced by a subset of hyperactive users,"* so it seems to me that personal recommendations have a much higher success rate than machine recommendations. In that case, your problem isn't an algorithm, it's that everyone and their dog has a stake in manipulating this, and they do. They even brag about it in [Time magazine](https://time.com/5936036/secret-2020-election-campaign/).

There's a question early on in the article: *"Does its platform aggravate polarization and tribal behavior? The answer it found, in some cases, was yes."* Another way of putting that is: "The answer in most cases was no."

## III.

The notion that groups are dominated by hyperactive influencers does track with my experience. I once worked in social media advertising, and let me tell you the open industry secret: going viral is a lie.

The romantic idea is that some undiscovered Justin Bieber-like wunderkind posts something brilliant online, in a little unknown corner. A kind soul discovers it, and it starts being shared from person to person. It's a bottom-up grass-roots phenomenon, growing in magnitude, measured by the virality coefficient: just like COVID if it's >1 then it spreads exponentially. This is the sort of thing mediocre marketing firms will explain to you with various diagrams.

![Going viral from one person to many](../../assets/03769924b38a3f17.png)


The reality is very different. Bottom-up virality near 1 is almost unheard of, because that would imply that *every person* who sees it also shares it with someone else. We just don't do this. For something to go viral, it must be broadcast to a *large enough group* each time, so that at least one person decides to repost it to another big group.

Thus, going viral is not about bottom-up sharing at all: it's about content riding the top-down lightning between broadcasters and audiences. These channels build up their audiences glacially by comparison, one person at a time. One pebble does not shift the landscape. It also means the type of content that can go viral is constrained by the existing network. Even group chats work this way: you have to be invited in first.

This should break any illusions of the internet as a flat open space: rather it is accumulated infrastructure to route attention. Everyone knows you need sufficient eyeballs to be able to sell ad space, but somehow, translated into the world of social media, this basic insight was lost. When the billboard is a person or a personality, people forget. Because they seem so accessible.

In the conflict between big tech and old media, you often hear the lament that *"tech people don't like to think about the moral implications of what they build."* My pithy answer to that is *"we learned it from you"* but a more accurate answer is "yes, we do actually, quite a lot, and our code doesn't even have bylines." Though I can't actually consider myself "big tech" in any meaningful way. In this house we hack.

I can agree that large parts of social media are basically just cesspits of astroturfing and mass-hypnosis. But once you factor in who is broadcasting what to whom, and at what scale, the lines of causation look very different from the usually cited suspects.

While there are indeed weird niche groups online and offline, it is the crazy non-niche groups we should be more concerned about. Who is shouting the loudest, to the most people? Why, the traditional news outlets. The ones that 2020 revealed to be far less capable, objective and in-the-know than they pretend to be. The ones who chastised public gatherings as irresponsible only when it was the wrong group of people doing so.

So don't just question what they say and how they say it. Ask yourself what other stories they could've written, and why they did not.

## IV.

What's especially frustrating is that the class of people who are supposed to be experts on media and communication have themselves been bubbled inside dogmatic social sciences and their media outposts. If you ask these people to tell you about radicalization on the internet, you are likely to hear a very detailed, incomplete, mostly wrong summary of pertinent events.

Much of this can be attributed to what I mentioned earlier: telling you how to feel about something before they tell you the details. Sometimes this is done explicitly, but often this is done by way of Russell Conjugation: "I am being targeted, you are getting pushback, they are being held accountable." The phrasing tells you whether something is happening to a person you should root for, be neutral about, or dislike. Given a pre-existing framework of oppressors and oppressed, they just snap to grid, and repetition does the rest.

Sometimes it's blatant, like when the NYT rewrote a fairly neutral article about Ellen Pao into [nakedly partisan hero worship](http://newsdiffs.org/diff/934341/934454/www.nytimes.com/2015/07/11/technology/ellen-pao-reddit-chief-executive-resignation.html) a few years ago.

But most people don't even realize they're doing it. When called upon they will insist *"it's totally different,"* even if it's not. It's judging things by their subjective implications, not by what they objectively are. Once the initial impression of the players is set, future events are shoehorned to fit. The charge of *whataboutism* is a convenient excuse to not have to think about it. This is how you end up with people sincerely believing Jordan Peterson is an evil transphobe rather than a compelled speech objector dragged through the mud.

Information that disproves the narrative is swept under the rug, with plenty of scare quotes so you don't go check. If a reporter embarrasses themselves by asking incessantly leading questions, the story will shift to how [mean and negative the response is](https://www.independent.co.uk/voices/cathy-newman-abuse-channel-4-jordan-peterson-metoo-backlash-latest-a8170031.html), instead of actually correcting the misconceptions they just tried to dupe an entire nation with.

The magnitude of a particular event is also not decided by how many people participated in it, but rather, by how many people heard about it. This is epitomized by the story format that *"the X community is mad about Y"* based on 4 angry tweets or screencaps. It wasn't a thing until they decided to make it a thing, and now it is definitely a thing.

The idea of the media as an active actor in this process is a concept they are quite resistant to. Because if it isn't a story until they write the story, that means they are not actually reporting broadly on what's happening. They're just the same as anyone else.

Part of the problem is that what passes for news about the internet is mostly just gossip. Even if it is done in good faith, it is very hard for an individual to effectively see the full extent of an online phenomenon. In practice they rarely try, and when they do, the data gathering and analysis is usually amateur at best, lacking any reasonable control or perspective.

You will often be shown a sinister looking network graph, proving how corrupting influences are spreading around. What they don't tell you is that this is what the entire internet looks like everywhere, and e.g. a knitting community likely looks exactly the same as an alt-right influencer network. Each graph is just a particular subset of a larger thing, and you have to think about what's *not shown* as well as what is.

It's an even more profound mistake to think that we can all agree on which links should be cut and which should be amplified. Just because we can observe it, doesn't mean we know how to improve it. In fact, the biggest problem here is that so few people can decide what so many can't see. That's what makes them want to fight over it.

The idea that any of this is achievable in a moral way is itself a big red flag: it requires you to be sufficiently bubbled inside one ideology to even consider doing so. It is fundamentally illiberal.

It really is quite stunning. By and large, today the people who shout the loudest about disinformation, and the need to correct it, are themselves living in an enormous house of cards. It is built on bad thinking, distorted facts and sometimes, straight up gaslighting. They have forced themselves on companies, schools and governments, using critical theory to beat others into submission. They use the threat of cancellation as the stick, amplified eagerly by clickbait farms... but it's Facebook's fault. "*They* need to be held accountable."

These advocates only know how to mouth other people's incantations, they don't actually live by them.

Here's the thing about secret police: [when studied](https://onlinelibrary.wiley.com/doi/10.1111/ajps.12475), it is found that it's mostly underachievers who get the job and stick with it. Because they know that in a more merit-driven system, they would be lower on the totem pole.

If the world is messed up, it's because we gave power to people who don't know wtf they're supposed to do with it.