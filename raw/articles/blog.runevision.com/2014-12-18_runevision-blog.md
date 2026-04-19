---
title: runevision blog
url: https://blog.runevision.com/2014/
published: '2014-12-18'
source_blog: Blog - runevision
source_site: https://blog.runevision.com/
category: graphics
fetched: '2026-04-19'
---

The development of my exploration game The Cluster, that I'm creating in my spare time, marches ever onwards, and 2014 saw some nice improvements to it.

Let's have a look back in the form of embedded tweets from throughout the year with added explanations.

### Worlds and world structure

During the end of 2013 I had implemented the concept of huge worlds in the game, and I spent a good part of 2014 beginning to add more structure and purpose to these worlds.

Each world is divided into regions with pathways connecting artefacts, connections to neighbor regions, and the region hub. I used a minimum spanning tree algorithm to find a nice way to determine nicely balanced connections, and tweaking the weights used for the connections to change the overall feel of the structure is always fun.

### New name

In the early 2D iteration of my game, it was called [ Cavex](http://runevision.com/multimedia/cavex/), because it had caves and weird spelling was the thing to do to make names unique. Then since 2010 I used the code name

*EaS*after the still undisclosed names of the protagonists, E. and S. This year I decided to name the game

*The Cluster*as a reference to the place where the game takes place.

### Spherical atmosphere

The game takes place on large (though not planet-sized) floating worlds. Skyboxes with fixed sky gradients don't fit well with this, but finding a good alternative is tricky. I finally managed to produce shaders that create the effect of spherical fog (and atmosphere is like very thin fog), which elegantly solved the problem.

The atmosphere now looks correct (meaning nice, not physically correct) both when inside and when moving outside of it. The shader was a combination of existing work from the community and some extensive tweaks and changes by myself. [I've posted my spherical fog shader here.](http://forum.unity3d.com/threads/spherical-fog-shader-shared-project.269771/)

### Integrating large world structures with terrain

The game world in The Cluster is consists of a large grid of areas, though you wouldn't be able to tell where the cell borders are because it's completely seamless. Still, the background hills used to be controlled by each area individually based solely on whether each of the four corners where inside or outside of the ground. I changed this to be more tightly integrated with the overall shape of the world and some large-scale noise functions.

The new overall shapes of the hills have greater variety and also fit the shape of the world better.

I also re-enabled features of the terrain I had implemented years ago but which had gotten lost in some refactoring at some point. Namely, I have perturbation functions that take a regular smooth noise function and makes it more blocky. I prefer this embracing of block shapes over the smooth but pixelated look of e.g. Minecraft.

### Tubes

As part of creating more structure in the regions, I realized the need to reduce boring backtracking after having reached a remote goal. I implemented tubes that can quickly transport the player back. I may use them for other purposes too. Unlike tubes (pipes) in Mario, these tubes are 100% connected in-world, so are not just magic teleports in tube form.

### What's next?

It's not a secret that most aspects of The Cluster gameplay are only loosely defined despite all good advise of making sure to "find the fun" as early as possible. Being able to ignore sound advice is one of the benefits of a spare time project!

However, after the ground work for fleshing out the structure of the world regions this year, I've gotten some more concrete ideas for how the core of the game is going to function. I won't reveal more here, but stay tuned!


I'm very sad to have seen the way the [GamerGate](http://en.wikipedia.org/wiki/Gamergate_controversy) controversy has been evolving and the way it has been tackled by both sides.

I should say that I don't support GamerGate myself, though I'm not particularly against it either. I *am* completely against threats of death, rape, harm of family and other harassment of course, but I'm not against everything that everyone using the GamerGate hashtag stand for, because that is a whole lot of different things.

The harassment is more important than anything else in this controversy. I'm absolutely not apologizing or defending it, if anyone should be in doubt. On the contrary I want the fight against harassment intensified and made more effective - I just believe that fighting GamerGate as a whole is actually counter-productive to that end. Hear me out...

![](../../assets/a3c0c9291d9439c9.png)

### Several different subjects

I can't claim to have a complete overview of the GamerGate controversy, but from what I've understood so far, it encompasses many different separate subjects (though they get ever-so-easily entangled). On each subject, different people express a wide range of different opinions.

#### Harassment

A sample of possible stances:

- Harassment in the form of threats of death, rape, harm to family etc. are never ever justified. The widespread harassment of women and those supporting them must stop now!
- Harassment is not okay, but some or all the harassment in this controversy was faked by those claiming to have been harassed
*(ugh, ugly conspiracy theory!)* - Harassment is justified when the game culture we identify with is threatened
*(just ugh!)*

I've seen people using the GamerGate hashtag argue all of these points.

#### Journalistic integrity

All people who claim to represent GamerGate seem to claim it's about journalistic integrity, but the specifics of what it is they actually want is quite diverse.

- Some people ask for game news sites to adopt a set of ethical guidelines similar to
[that of The Escapist](http://www.escapistmagazine.com/articles/view/video-games/editorials/12224-The-Official-Ethics-Policy-of-The-Escapist). - Some ask for the abolishment of using numerical scores in game reviews, since scores can have a very direct effect on bonuses for game development studios. This, they argue, increases the temptation and risk of bribes (e.g. journalists receiving swag for certain minimum scores).
- Some claim that game critics such as Anita Sarkeesian are representing games in a distorted way, showing things out of context.
- Some claim that there are too strong ties between game journalists and game developers, and that these ties are used to obtain favorable coverage of certain games.
*(People behind the hate campaign against Zóe Quinns argued this. I've seen people who are outspoken against harassment also making these claims.)*

You can agree or disagree with these points, but they are all points that can be discussed in a civil manner. Needless to say, turning to harassment is absolutely a horrendous tactic. Accusing all people who want to discuss any of these points of harassment is not helping anything either though.

I've seen the argument made that GamerGate people can't point to any specific thing they want changed, and this presented as indication that it's all about harassment. Even if we ignore the request for ethical guidelines etc. and assume they can't point to anything, I don't think that a lack of a clear solution or the inability to express it, is any proof that they really just want to push for harassment when it comes down to it.

#### Depiction of women in games

Anita Sarkeesian's video series on [Tropes vs Women in Video Games](http://www.feministfrequency.com/tag/tropes-vs-women-in-video-games/) has a significant role in the GamerGate controversy. I personally think there are a lot of misunderstandings involved.

Anita's videos mainly criticize games without proposing specific solutions, and this leads to some people assuming the worst and thinking that she wants to take the games they love away from them, or is just hateful against people who play these games.

In reality, Anita makes clear that "it's possible to enjoy a game while simultaneously being critical of elements of it", e.g. no one is taking them away. What should be done is still ambiguous though and largely up for discussion. Various possible standpoints:

- The industry should aim to create games with a broad representation of people and represent them respectfully. It should also realize the role games have in broader society in creating the cultural ideas we live by, and take on that responsibility.
- Any legal game has its right to exist if there are people who want to buy them, regardless of what it depicts. Artistic freedom, freedom of speech and so on. Games representing women more broadly is fine; go ahead and make those games, but don't dictate that the other games shouldn't be made.
- The industry should strive towards more balance as a whole, but no individual game should be held accountable for not living up to certain imposed standards.

#### Gamer as a term and assertions about gamer culture

In August, [a](http://arstechnica.com/gaming/2014/08/the-death-of-the-gamers-and-the-women-who-killed-them/) [handful](http://dangolding.tumblr.com/post/95985875943/the-end-of-gamers) [of](http://www.gamasutra.com/view/news/224400/Gamers_dont_have_to_be_your_audience_Gamers_are_over.php) [articles](http://kotaku.com/we-might-be-witnessing-the-death-of-an-identity-1628203079) [on](http://www.gamasutra.com/view/news/192107/Opinion_Lets_retire_the_word_gamer.php) game news sites announced that the term "gamer" is becoming irrelevant; that "gamer" is dead. Some people who considered themselves gamers and in love with gamer culture were offended by that. This is another case of different sides trying to "own" what the meaning of a word is, which I personally consider pointless. It sure did add fuel to the fire though. Different standpoints in the controversy:

- As videogames became mainstream, the male-dominated gamer identity clung on to its idea of hardcore gaming being the only true form of it, and had no room for people playing match-three games, games with no challenge, and so on. Becoming a smaller part of a growing and diversifying culture, these gamers fight against the change with hatred and a sense of entitlement. So let's stop the use of the irrelevant term 'gamer' and talk about 'players' from now on.
- "'Gamer' isn’t just a dated demographic label that most people increasingly prefer not to use. Gamers are over. That’s why they’re so mad. These obtuse shitslingers, these wailing hyper-consumers, these childish internet-arguers -- they are not my audience (at Gamasutra). They don’t have to be yours." (From
[this Gamasutra editorial](http://www.gamasutra.com/view/news/224400/Gamers_dont_have_to_be_your_audience_Gamers_are_over.php)) - "'Gamer' as a label can stretch, can evolve. It's not something you are born with, or even forced upon you. It's a choice. You label yourself a gamer because of a passion for games. Don't want to be label one? Good, you are not! This is a label you choose for yourself, not one applied to you by others. Claiming 'gamers are dead' is simply having no idea what this label is about in the first place." (From
[this Gamasutra member blog post](http://www.gamasutra.com/blogs/MarcAndreJutras/20140828/224454/Gamers_are_dead_Really.php)) - Gamer culture is vile and toxic space of privileged white males that creates the kind of threats we've seen.
- Gamer culture is a wonderful space for people of all ages, genders, ethnicities and sexual orientations to share their love of games.

The articles arguing for the "end of gamers" is probably some of the most direct attempts at linking "gamer culture" and "harassment" intrinsically together, and in doing so, most likely alienated a large group of diverse self-proclaimed gamers, the majority of whom is opposed to harassment.

You can civilly argue for or against the relevance of gamer as a term, but to claim that people who consider themselves gamers are also the people who harass or support harassment is not going to help anything.

### What GamerGate really means

I've covered four distinctly different subjects above and a list of different stances for each. Different people assume all kinds of different stances on these different subjects - any talk of there being "two sides" to this controversy is failing to understand the complexity and nuances of it.

Yet many people are claiming to have the truth about what GamerGate really means.

Some GamerGate people say that they were around (under different banners perhaps) arguing for reforms in game journalism long before the harassers used the GamerGate term for pushing an agenda of harassment.

Some anti-GamerGate people say that [GamerGate was orchestrated by harassers from the very beginning](http://arstechnica.com/gaming/2014/09/new-chat-logs-show-how-4chan-users-pushed-gamergate-into-the-national-spotlight/), and that harassment is thus the true purpose of GamerGate.

The only objective truth as I see it is that GamerGate means different things to different people. Who cares what the history of it is; we know that there are lots of GamerGate people who are for inclusion, against harassment. In particular, [the NotYourShield hashtag was created to put emphasis on that](http://www.cinemablend.com/games/-NotYourShield-Hashtag-Shows-Multi-Cultural-Support-GamerGate-67119.html). How is them using the GamerGate hashtag supporting harassment when they are speaking out directly against it?

The fact that people against GamerGate are constantly trying to educate the moderate people under the GamerGate banner that supporting GamerGate is supporting harassment seems to point to an acknowledgement that not everyone may share that view from the start. You could say that the anti-GamerGate people are helping creating and reinforcing the notion that GamerGate equals harassment, and that while other people are trying to break down the links between GameGate and harassment, anti-GamerGate people are constantly working to reinforce those links in the public perception.

Regardless though, I'm not seeing any signs of either side budging. I think that the fight over owning the meaning of GamerGate is a lost cause regardless of what side you're on.

### What you may inadvertently communicate

GamerGate as a term is meaningless since it represents many people with completely opposite standpoints.

#### Representing more than you meant to

Claiming to be part of or in support of GamerGate will be interpreted by many as supporting harassment against women regardless of whether you agree with that or not.

Claiming to be against or fight GamerGate will be interpreted by many as being against making any changes to improve journalistic integrity, and against contemporary gamer culture, gamer as a term, and as being scornful towards people creating or enjoying certain types of games, whether you agree with that or not.#### Pushing different agendas

Insisting on using the GamerGate hashtag will be perceived by many as complying in pushing an agenda of harassment under the ostensible agenda of journalistic integrity. Whether that's correct or not doesn't matter, the damage to the GamerGate word is done and beyond repair unless you're only addressing people who considers themselves part of GamerGate too. On the flip side, insisting on antagonizing people using the GamerGate hashtag will be perceived by many as complying in slipping in an agenda of deriding gamers and certain types of games together with the agenda of stopping harassment. Whether that's correct or not doesn't matter; hordes of people supporting GamerGate will interpret it that way. After all, if it's only the harassment part of GamerGate you're against, why don't you just oppose harassment directly instead of opposing GamerGate as a whole?For anti-GamerGate people, it may just happen that you in fact *do* agree with those other agendas too. Maybe you do think we should retire the word gamer and so on. But if you're taking the opportunity to push those other agendas together with the agenda against harassment, then you're responsible for adding more fuel to the fire and pitting people against each other who are all against harassment, just because of those other less important differences.

### What to do

GamerGate is pointless to fight both for and against. All it does it create enemies out of people who would otherwise be on the same side on the subject of fighting harassment.I suggest for all involved to drop the focus on GamerGate if you want to be taken seriously as a person who wants real change rather than just mudslinging. So stop using #GamerGate and stop using #StopGamerGate2014, but on the other hand, don't waste time scolding other people for using them. Just drive the conversations towards the real issues.

To put focus on non-harassment related issues, use other hashtags to discuss that under, whether it's about journalistic integrity, depiction of women in games, gamer culture, or other.

For the fight against harassment, I'd suggest to use the hashtag **#UniteAgainstHarassment** - this is meant to indicate stark opposition to threats of death, rape, harm to family, and other harassment, while acknowledging that people are most welcome to join regardless of their stance on GamerGate, as long as they're against harassment.


I love exploration in games! I like platforming, and I like puzzles, and I can deal with a little combat, but the biggest reason I play games at all is to experience and explore *strange, beautiful, mystical* places, and unravel the secrets they contain.

![](../../assets/d174ee56b04a070f.jpg)

Though many games have elements of exploration, there's not that many I know of that has it as a major focus and really get it right. It doesn't help that some otherwise good exploration games are also very difficult. Being stuck at the same hardcore challenge for ages can get in the way of the joy of exploration.

In order to bring more focus on games where exploration is a major element, I created this Steam curated group:

`Great games where exploration is a major focus, taking place in worlds that are non-linear yet structured. Also: Secrets and mystery!`

Games in this group may have limited but not excessively challenging puzzles, combat, and platforming. They will often have maps.

They may have gated progress based on ability upgrades ("MetroidVania" games), collected items, completed goals, or similar, as long as the progress is not mainly linear.

The word "structured" is also important. The group is not for games that allow you to dig or build anywhere, since it's at odds with structured level and world design. MineCraft, Terraria, and similar are great games that arguably have strong exploration elements, but not of the type this group promotes.

Also, although the group welcomes easy games with practically no challenging elements, it's not for what some would call "non-games" that contain no gameplay at all (not that there's anything wrong with that).

The best exploration games not only let you explore interesting places, but also let you uncover secrets and gradually gain a better understanding of the mystical world around you.

### Yes, yes, this is exactly the types of games I love too!

Are you among the niche that are thinking that? If you are*, *[follow the Exploration Games curated group on Steam](http://store.steampowered.com/curator/6862928-Exploration-Games/)!

If you know some great games on Steam in this genre, let me know in the comments. And if you like, get in contact with me about becoming a member of the curated group who can add new recommendations to it.


The game I'm working on has a new name: The Cluster

![](../../assets/b4f54c9058d92c51.png)

This replaces the previous working title "EaS". The full final name is likely going to be something along the lines of "Explorers of The Cluster", "Adventurers of The Cluster", "Enigmas of The Cluster" or similar, but I haven't decided on that yet. "The Cluster" is the defining part, and would be the recurring part if there should ever be more than one game in the series.

(For the sake of coherence I've retroactively updated past blog posts to use the new name.)

*This post is about The Cluster, my 2.5D platform game under development with focus on non-linear exploration, set in a big, continuous world. You can read all the posts about The Cluster here.*


*This post is about The Cluster, my 2.5D platform game under development with focus on non-linear exploration, set in a big, continuous world. You can read all the posts about The Cluster here.*

Okay cheesy title aside, this trick really did make debugging much easier for me, though the trick really is also very basic in retrospect. But it took me years to realize this, so maybe it will help somebody else too.

*TLDR; freeze the generation at the exact point you encounter an error, but let the game continue running so you can inspect the frozen generation state with full visual context, turning various in-game debug visualizations on and off, and moving the camera around as needed.*

A problem I've had for a long time is that errors in the procedural generation of my game can be hard to debug. The game have many sub-systems dependent on each other. When the player approaches an area that hasn't yet been generated, it will be generated by the various sub-systems on the fly with the various dependencies respected. Terrain info needs to be generated before path-finding info for instance.

The complexity of the dependency relations can make it hard to keep track of exactly how something went wrong, and whether an issue was caused by a bug in generation code itself, or a bug in the dependencies code that meant some needed information wasn't yet available.

Add to that the challenge that many of the generation algorithms modify data in several passes, and just looking at a visualization of the data at the end of the generation may not be sufficient to see how the data was wrong at some step in the middle of the process.

The normal way to inspect data in the middle of a process is by using breakpoints. But breakpoints only let you inspect data in your text/debugging IDE as numbers, and data for procedural generation is often incomprehensible at that low of an abstraction level. The custom-made visual debugging tools are really needed, but they can't be enabled and manipulated while the entire game is paused. And according to StackOverflow, [individual threads can't be paused selectively](http://stackoverflow.com/questions/5818391/breakpoint-a-multi-thread-application).

![](../../assets/355457df4a4655ea.png)


![](../../assets/355457df4a4655ea.png)

For the trick to work, your procedural generation needs to fulfill these criteria:

- The generation should not happen on the main thread where the game loop and logic runs. This means you need to perform the procedural generation in one or more threads dedicated to that. This is pretty much needed anyway if your game generates new parts of the world on the fly without pausing the play. In my game I run all the generation in just one thread.
- Make your life simpler by making it easy to switch various debug visualizations on and off at any point while running the game.
- Obviously, have places in your code (such as asserts) where you check if what you take for granted is true and print a helpful error otherwise with as much info about the problem as possible. In addition to messages that are just printed in the console, I also have positional logging which shows up in the game world at a specific 3D position if the relevant debug visualization is enabled.

The trick is to implement your own breakpoints that pause the generation thread. I did it like this:

Whereever I have detected a problem that I want to pause the game, I just call

` Debugging.GenerationBreakpoint();`


In the Debugging class I have this code:

```
static bool waitForBreakpoints = false;
static bool breakpointPaused = false;
public static void GenerationBreakpoint () {
if (!waitForBreakpoints)
return;
breakpointPaused = true;
while (breakpointPaused)
System.Threading.Thread.Sleep (5);
}
```


I then have some debugging UI with a setting to turn *waitForBreakpoints* on and off, and a Resume button that is only shown when *BreakpointPaused* is true, and which sets it to false again when clicked.

That's it!


Two weeks ago I was a week in Seattle for Unity's Unite conference. While in the city, I also had a chance to visit the [Valve](http://www.valvesoftware.com/) offices and try out their famous VR demos. The headset we tried was [the one using QR codes](http://www.roadtovr.com/hands-valves-virtual-reality-hmd-owlchemy-labs-share-steam-dev-days-experiences/) to track alignment - not the newer ["polka dots" headset](http://techcrunch.com/2014/06/03/valve-shows-off-its-polka-dot-vr-headset/) they've been showing off too this summer, though I suspect the difference is not in performance but just in demands on the physical environment.

![](../../assets/7d61775e26209cc3.png)

The guys from Valve were not only brilliant but also very friendly. We talked with them at length, and we were impressed with how they patiently and tirelessly showed the demos to each of us in turn, as well as taking us on a tour of the sizable office.

![](../../assets/3ba830cc096d1fb8.jpg)

Like everyone else who have seen their VR have already said, the demos are amazingly effective. Though the pixels are visible if you look for them, the resolution is easily high enough to not be a problem. The world around you doesn't seem pixelated either; just a tiny bit blurry. Before I go on to praise the head tracking, let me get my one reservation out of the way.

### Eye distance calibration and sense of scale

One reservation I have about the demos I was shown was that I felt only a limited sense of grand scale in those demos that were meant to showcase that. Most of the demos took place in virtual spaces of limited size (nothing was further away than about 10 meters) and those worked really great. The environment in those felt tangible and I felt a strong presence. However, a few demos placed me in environments with towering structures extending for what should amount to hundreds of meters, and those felt less real for me. In those environments it felt like objects that were supposed to be hundreds of meters away were maybe only 10 or 20 meters away, though it's very hard to judge when the perspective cues don't match the stereoscopic depth perception cues at all.

I suspect that lack of eye distance calibration (or interpupillary distance (IPD) to use the technical term) was the cause. The demos were setup to be easily viewed by many people in a row, and IPD calibration was not part of the process since it was deemed to not make a large difference. I would agree with that for the most part, though I think it does have a significant effect on the large-scale virtual environments and was the cause of the weaker sense of presence I felt in those.

Normally when a virtual object is supposed to be near-infinitely far away, the distance between it's left eye depiction and its right-eye depiction on the screen(s) of the headset should be the same as the distance between the centers of the eyes, so that the eyes will look out in parallel in order to focus on the two respective images. This will match what the eyes do in reality when converging on objects nearly infinitely far away. (For the purposes of human stereoscopic vision, anything further away than just about a hundred meters is practically infinitely far away.) If a person's actual IPD is larger than what is assumed in the VR setup (hardware and software), then the eyes will not be looking out in parallel when focusing on a virtual object nearly infinitely far away, but rather look a bit inwards. This will cause the eyes and brain to conclude that the object is in fact nearer, specifically at the distance where the focus lines of the two eyes converge and meet each other in a point.

What's worth noting here is that no amount of up-scaling of the virtual world can compensate for this. If the "infinite distance" makes the focus of the eyes converge 10 or 20 meters away, then that will be the perceived distance of anything from structures a hundred meters away to really distant objects like the moon or the stars. A corollary to this is that things in the distance will seem flattened, since an infinite amount of depth is effectively compressed into a few meters. This too matches my impression, though I didn't have much data to go on. One huge virtual object I encountered in one of the demos was of roughly spherical shape. However, it appeared flattened to me at first while it was far away, and then felt increasingly round as it came closer to me. You might say that things very far away also technically appear flat to us in reality, but in practice "flat and infinitely far away" doesn't feel flat, while "flat and 10 meters away" does.

![](../../assets/84f177af62c48d21.jpg)

Luckily, eye distance calibration is not a hard problem to solve, and Tom Forsyth from Oculus [points out that the Rift comes with a calibration utility](http://www.oculusvr.com/blog/vr-sickness-the-rift-and-how-game-developers-can-help/) for this that people are encouraged to use. I should also say that none of my colleagues who tried Valve's demos had the same reservation as me about sense of scale. It could be that their IPD better matches what was assumed in the VR setup, or it could be that potential IPD discrepancies were just less apparent to them.

### Approaches to head tracking

What I found most impressive about Valve's VR technology was that the head tracking and stabilization of the virtual world is basically solved. Unlike Oculus' Development Kit 1, the world doesn't blur at all when turning the head, and it feels completely stable as you look and move around. This makes the virtual world feel very tangible and real. You can read more about the technical details elsewhere, but it's basically achieved with a combination of low latency, high frame-rate, and screens with low persistence of vision, meaning that for every frame the screen only shows an image for a very brief period, being black the rest of the time. (Old CTR monitors and TVs were all like this, but it's not common for LCD screens.)

The tracking using QR codes worked very well then, except when it didn't. If you get close enough to a wall that the head-mounted camera can't see any one QR code fully, the positional tracking stops abruptly at that point. The effect is that of the world suddenly moving forward together with your head, until your take your head back far enough that the tracking resumes. This happened quite often during the demo and every time broke the immersion a lot while also being somewhat disorienting. Together with QR codes having to be plastered everywhere on the walls, going away from that approach is probably a good idea.

"For Crystal Cove, it's going to be just the seated experience"Nate Mitchell, Oculus

I haven't tried the Oculus Rift Development Kit 2 (at least not its tracking), but from what I've heard, it's based on a kind of camera in front of the player, recording the movement of the headset. And supposedly, it only works while approximately facing that camera. Oculus have also been issuing comments that [the Rift will be meant to be used while sitting](http://www.polygon.com/2014/1/11/5298510/oculus-rift-crystal-cove-intended-as-a-seated-experience), which matches up with that limitation. Having tried a few different VR demos, that seems awfully restricting. It will work mostly fine for cockpit-based games taking place inside any kind of car, spaceship, or other vehicle with a "driving seat" you stay in all the time. But for a much broader range of games and experiences, having to face in one direction all the time will be severely limiting or directly prohibitive. It's currently unclear whether the limitation is only for the Crystal Cove headset (Development Kit 2) or also for the final consumer version.

### Freedom of head and body movement

Luckily there seems to be hope yet that even Oculus' headsets can be used for experiences with more free movement, whether Oculus themselves will end up supporting it or not. I had a chance elsewhere in Seattle to try out a demo of [Sixense](http://sixense.com/)'s tracking and motion controller technology (also described in [this article on The Verge](http://www.theverge.com/2014/8/18/6030935/motion-controllers-make-great-virtual-reality-lightsabers)). Basically they had slabbed their own motion tracker onto the Rift headset, replacing the Rift's own head tracking, as well as equipping the player with two handles that are also motion tracked.

![](../../assets/ba4b2056f264c7d9.jpg)

The VR demo to show it off with was one of being a Star Wars Jedi training with lightsabers against that Remote sphere that hovers and shoots lasers - albeit without being blindfolded as in the original movie. The tracking of both head and hands worked wonderfully, and allowed all the attention to be on the quite engaging gameplay.

While Valve's demos were the visually most impressive spaces to be inside, the Sixense demo was easily the most overall engaging VR experience I've had. Sony have sold one-to-one motion-tracking Move Controllers with the PlayStation for years, but solid motion tracking controllers combined with VR combines into an experience that's feels real and is intuitive at a whole different level.

The promise of waving stuff around with your own hands got mainstream with the Nintendo Wii, but the tracking was crude, and only mapped on a gestural level. You swung your hand to indicate swinging a racket, and the in-game avatar would trigger a racket-swing as well, but only with the approximate same direction and not with the same timing at all. Sony's Move Controllers fixed that, but still the sense of depth was missing and it still felt more like remote-controlling a utility rather than actually holding it in your hand, and you have only very little sense of whether your aim might be correct. This limitation will always exist as long as the visuals are not in stereoscopic 3D.

![](../../assets/ac8af3e2d82ac11f.jpg)

Using accurate motion tracking of the hands in VR produces an entirely different sensation. When I tried that lightsaber demo I felt like I was really holding those lightsabers, and swinging and turning it to block the incoming lasers felt like the most intuitive thing, even though I've never - eh - blocked lasers with a lightsaber in real life, or handled any kind of sword for that matter.

### Personal style in VR

Equally impressing, when watching others play the lightsaber demo, it became apparent how much the demo and technology let people approach the gameplay with their own style and personality. Some would move the lightsabers only just enough to block the lasers, others would be swinging them more gracefully around, while yet others moved with big and stiff robotic-like moves. As the interfaces to VR begins to imitate and approach the way we move and interact with the real world, our mannerisms and ways of movement from the real world will begin to translate there as well.

To go back to the technical side of things, the Sixense technology is based on magnetic fields. A Valve employee said they'd been experimenting with tracking based on magnetic fields as well, but hadn't found it to be very reliable. Whether it's because they didn't account for disturbances in the magnetic fields as the people from Sixense claim to do, or whether it really is less reliable but just wasn't a noticeable problem in the demo in question is hard to say. What seems clear though is that there is loads of promise in these new forms of interaction, and that it will be very exciting to see what kind of experiences and interactions in VR we'll be having in the coming years.

### Dulling of reflexes

While the advances in VR have made huge strides now in a very short time towards eliminating simulator sickness and making the virtual environments appear much more real to our senses, this potentially can have a negative side as well.

As the way the virtual worlds appear to our senses get increasingly closer to how the real world does, our motor skills, reflexes, and other instincts are also increasingly transferable from one to the other. While people don't have any problem having their avatar walk off the ledge of a cliff in a traditional 3D game, many people feel physically unable to walk off the ledge of a cliff in VR, while other can, but have a hard time forcing their body to do it. A positive side of this is that VR can be used to treat a variety of physical and physiological illnesses by performing training in VR where the results transfer to the real world.

Consider though that many game scenarios tasks players to be daring and bold, subjecting themselves to hazardous environments to overcome impossible odds. And consider that failing repeatedly without real consequence is a normal part of playing such games. In a VR game, a scenario might see you dodging large rocks being hurled towards you, and failure to do so might see you die in the game, but physically being unharmed in the real world. The natural reflex for most people in such a game will be to dodge the rocks not just for gameplay reasons but even purely instinctual as well. However, one might speculate that the more times the body and brain experiences being hit by a rock in the game with no physical consequence, the more the reflex to avoid the rocks will be weakened.

Imagine too that the game is hard and won't let you win if you duck and avert the rocks too aggressively, thus loosing focus on what's going on elsewhere around you. Instead you'll need to adapt to only just avert the rocks with minimal expenditure. Your chances of averting the individual rock will be a bit lower, but your chances of winning the scenario increases.

As reflexes and adaptations to stimuli can transfer between the real world and VR, can this adaptation towards ignoring the body's natural reflexes also accidentally transfer to the real world? Will people navigating hazardous virtual environments haphazardly have a risk of reacting less acutely to hazards in the real world as well?

As far as I have gathered, this is something we don't yet know very much about. [Some studies have been made decades ago](http://www.agocg.ac.uk/reports/virtual/37/report37.htm), but based on VR technology nowhere in the same league as what we're beginning to have available today. It seems to be an important area of study though, and I'll be curious to see what the findings will be.

In the mean time I will probably lean towards indulging mostly in VR experiences that let me peacefully enjoy strange and beautiful places and use some serious moderation with experiences that will put me in a sense of danger and test my survival instincts. Deflecting lasers will be exempt from this.


In the past few weeks I've been implementing incremental changes to the design of my website. Generally I still like the overall aesthetic and layout of the design made in 2008, but I wanted to tweak it to bring it more in line with modern web design ideals.

Here's the new design next to the old:

![](../../assets/5ed690a9b67b2eda.png)

![](../../assets/d83ff635b80a6607.png)

The goal has been to move the design more in the direction of minimalism (not that I've striving for absolute minimalism) and to make the layout responsive so it works better on mobile devices and can take better advantage of wider screens.

### Minimalism

There has long been a trend in web design, and in recent years in application design too, towards minimalism in UI aesthetics. The reasoning goes that the content should be the primary focus with little else to distract from it. This has often been implemented in the form of flat designs. Though ubiquitous today, flat redesigns have sometimes been controversial, especially when used in applications, and when taken to an extreme. I have certain reservations myself, but that's a discussion for another time.

In any case, minimalism certainly have some merit to it. Since all the texture and shading in my old web design was purely cosmetic and wasn't used for aiding usability, I could see the point in getting rid of some of that to produce a cleaner design.

I've worked with a process of implementing the low hanging fruit first. Just removing the background pattern and the background spark image already made the design feel a bit more clean, but it left an awkward empty gap to the left of the title. I didn't want to move the menu sidebar upwards, but placing the menu sidebars at the right side instead of left fixed the problem, and has been a general trend for a long time anyway.

![](../../assets/9f2e95c2b49e67a0.png)

Next step was trying out getting rid of the shading. To begin with I simply replaced the shaded graphics files with flat versions to be able to test it without touching the HTML and CSS - well, except for changing the colors of the box headers and timestamps.

For a long time I had disliked the headers being confined to thin colored bars, so I wanted to get rid of that at the same time.

![](../../assets/a789843853c31845.png)

This change basically took the graphical look 90% of the way, but as everyone knows, the devil is in the details, and there was still many small tweaks needed.

What came next though were not more visual design changes but rather technical changes to the implementation.

### Modern styling and responsiveness

Now that the general flat look was validated, I could proceed to implement it in a smarter way. Modern CSS can draw rounded borders fine without any image files needed. This required quite some changes to the HTML and CSS. Most of it was removing a lot of cruft of nested divs that used to control the image-based borders, but some rethinking of the margin and padding values was also required.

Before I could begin implementing responsiveness, I also needed the header to be horizontally resizable. The header was one big image, which made resizing tricky. In order to make it resizable, I split it up into multiple parts: One background image for the box itself, one semi-transparent image with the portrait and left side text, and one semi-transparent image with the site name. Now I could make a resizable box in CSS with the new background image as background, rounded corners handled by the browser, and additional image elements layered on top.

With all boxes now being resizable, I could implement media queries to support multiple layouts of the site suited for different screen resolutions. The original design was designed for a minimum browser width of 800 pixels. I kept that one since it's still good for old monitors, browsers that are not full-screen, and now also for tablets. I added a wider but otherwise identical version for wider screens. Finally, I added a narrower version suitable for mobile browsing.

![](../../assets/11558aed5ec2c82e.png)

![](../../assets/3d64d6b53bcf6676.png)

![](../../assets/9a1c097a2d3496fe.png)

The mobile layout is significantly different from the others. The menu sidebars are absent since there's no room, and the header doesn't have links for each main section in the orange bar. All the text is also larger.

### Text scaling in CSS

For a long time I was seriously confused at the results I got when trying to scale all the text up or down, especially in how it interacted with line height. The best practices I arrived at is:

**Use rem unit for font sizes**

Use not *%*, *pt*, *px*, or *em* for specifying text sizes, but rather the new unit *rem* (root em). Probably obviously, *px* and *pt* are not suitable for scaling at all since they're absolute units. What's more tricky is that *%* and *em* are not easy to use for specifying sizes either. Since they specify sizes relative to the parent element, font sizes can end up being affected in non-trivial ways by the amount of nested elements the text is inside. By contract, the *rem* unit is not relative to the parent, but to the root element (the html tag), so nested elements have no effect on font sizes. Still, the overall scaling of all text can be controlled by setting a *%* font size in the style for the html element. My mobile layout has font-size: 140% for the html element.

**Use unit-less numbers for line height**

Line height should be specified using numbers with no units, except for exotic use cases where you want the same distance between lines regardless of font size. For a long time I assumed line height should be specified in either *%* or *em*, but that will calculate the physical line height in the context of the element it's specified for, and nested elements will then inherit that *physical* line height regardless of whether they use a smaller or larger font. Specifying the line height as a number with no unit prevents that.

I still have some confusion left over how some mobile browsers (such as iOS Safari) scales text up in ways that are inconsistent or ill-explained, but it's not a big issue.

### Mobile menu

There's no room for the sidebar menus in the mobile layout, so I opted for a drop-down menu instead. The menu is expanded and collapsed using jQuery (no surprises there).

![](../../assets/aeba323b98ae7445.png)

### Viewport logic

Modern browsers can scale pages arbitrarily, and mobile browsers scale them all the time by default. When a page can be scaled arbitrarily up or down, the question is how much room it should have available. Mobile browsers let pages decide that using the *viewport* meta information, where the width and height of the viewport can be specified.

The viewport width and height can be set to either constant values, or set to certain variables such as the device-width. The problem is that this doesn't always provide enough control.

In my responsive design, the minimum (mobile) width layout fits 600 pixels and the narrow layout fits 800 pixels. There is no reason a mobile or tablet browser should use a viewport of a different width than either 600 or 800 - it would just be wasted space.

To use the space optimally, I used JavaScript to query the device width, and set it to either 600 or 800 depending on the current screen width. You'd think it should choose the 800 width version only if the screen is at least 800 pixels wide, but that's not actually the intended behavior. Instead it chooses the 800 version of the screen is at least 480 pixels wide, otherwise the 600 version. You see, even for a screen with only 480 pixels width, it works better to use the 800 version scaled down than using the 600 version (scaled down less). Like I said, pages can be scaled arbitrarily, and there's no reason that a 1:1 scale is necessarily the optimum to strive for.

Why use exactly 480 to determine whether to use the 600 or 800 version? Well, supposedly that's about the size that divides the phones from the tablets (in most cases), and I want the 600 mobile-optimized version to be used for phones only; not tablets.

I'm sure this simple logic doesn't cover all cases, but it "works for me" (tested on iPhone 5, iPad retina and Nexus 7) and should be good enough for my personal site.

### Going forward

So far I'm happy with the revised design, though I'm sure there's still many things that could be improved. For example, I didn't look into using more modern fonts at all; it's still using "good old" Verdana/Arial. I also haven't gone through *all* the old content on my site and made sure everything looks good and isn't broken. Let me know if you spot any issues.

Generally my experience getting re-acquainted with HTML / CSS is that it's become a lot nicer to use in the past half decade since I did the original design. Fewer hacks are needed and stuff feels more consistent.

That said, I still find many things in the layout model annoying, and by fewer hacks I definitely didn't mean no hacks at all. I keep Googling for solutions to simple problems and find only partial, yet overly complicated solutions. One issue I didn't solve yet is that boxes with no multi-line paragraphs don't expand to the full available width (like on [this](http://runevision.com/multimedia/mazeraiders/) or [this](http://runevision.com/about/map/) page). Don't think it's simply a matter of setting width: 100%, oh no, that will expand it *beyond* the available width (because of the silly CSS box model where box sizes excludes padding and borders)...

Beyond that, is there any low-hanging fruit I've missed? Some further big improvements I could implement with little effort? If you have any tips, let me know.


For the past two weeks I've been trying out and evaluating Substance Designer in some of my spare time. Substance Designer is a tool for generating procedural materials. Really what this means is that it generates a set of procedural textures (such as diffuse map, normal map, specular map, and others) which many tools can then combine into a material.

![](../../assets/09f01b6f2a16855d.png)

Why is this useful? Substance Designer can export generated textures, but the more interesting part is that some other tools support the proprietary Substance format, which allows generating variations of procedural materials at runtime. So for example in Unity, which support Substances, a Unity game can include a Substance file for a stone wall, and then at runtime, while the game is running, an unlimited number of variations of it can be generated. This means you can have stone walls with different colors, different amount of dirt, different amounts of moss growing on them and whatever other variations this stone wall Substance exposes. Including all these variations (including all the possible combinations) in the game as regular textures would have taken up a ton of space, but instead a single Substance file can generate them all, and it usually takes up less space than even a single set of textures. That's a pretty cool way to get a lot of variety.

I'm working on and off on a procedural game in my spare time, and I would like to use procedural materials in it. I recently finally got around to evaluating if this would be feasible using Substance Designer. I know the runtime part in Unity works well, and since they added an Indie license, the price is feasible too, even for a game created on the side. Their Pro license is at the time of writing $449 while their Indie license (which has all the same features, just some restrictions on the license) is just $66. More details on the [Allegorithmic website](http://www.allegorithmic.com/). So the remaining questions was how easy or hard it would be to author the procedural materials in Substance Designer. Luckily they have a 30 day evaluation period that let me find out about that.

### The Test

I learned recently that Allegorithmic have begun downplaying the procedural aspect of Substance Designer and instead marketed it as an advanced compositing tool for textures (imported from e.g. Photoshop or similar) with emphasis on non-destructive workflows and on nodes being a superior alternative to layers. Nevertheless, my own interest in Substance Designer is for it's hardcore procedural features, and that's what I wanted to evaluate it based on.

I was pretty sure Substance Designer would make it easy to just combine various noise functions, but how did it fare with creating more structured man-made patterns such as a brick wall? To what degree would these things be hard-coded in the engine and to which degree would the design tool let me create something completely custom? I decided to use an existing material I had created before as reference and try to recreate a material in Substance Designer with a look as close as possible to this reference.

One of the best-looking materials I've created myself is a sort of ancient temple brick wall. It has rows of different heights, a different number of bricks per row, subtle variations of brick widths, and subtle random rotations of each brick. Furthermore it has erosion of the bricks as well as small cracks here and there.

![](../../assets/a2a87ee702237be6.png)

This material was created procedurally in the free raytracer 3D software [POV-Ray](http://povray.org/), so it's already procedurally created, but it can't be altered at runtime. In POV-Ray I created this brick wall by using a physical rounded box for each brick, and then the rest was done with procedural texturing of these bricks. In Substance Designer I would have to find a way to get the same end result purely with 2D texture tricks, without using any physical 3D objects.

### The Main Graph

Substance Designer is a graph based authoring tool. You author materials by visually creating and connecting various nodes that each manipulate a texture is various ways. For example, a blend node takes two textures as input and provide a new texture as output which is the blended result. The node has settings for which blend mode to use. Eventually, the graph feeds into the output textures, such as diffuse map, normal map etc. Here's my main graph from a point in time early into my attempt:

![](../../assets/c99702f8b91f7046.png)

In this graph I'm using some "Brick Pattern" nodes as input and some noise functions and then combining these in various ways. The brick pattern used here comes with the tool and does not support variable row height, variable number of bricks per row, etc.

In short, the main graph works well. It's fairly intuitive to work with and quick to make changes to. If you want a new node in between two other nodes, it takes about five seconds to create and reconnect. In fact, the tool tries to be smart about it and can do the reconnection automatically based on the currently selected node. Sometimes this can be a bit annoying when it's not what you want, but once you learn to take advantage of it, it's actually quite nice.

You can also easily see the intermediary results in each node since they show a small preview of the output texture they produce. If you want to see it larger, you can double-click on the node, which shows its output in a texture preview window. At the same time you can have the final output of the graph shown in a different 3D preview window at all times, so you easily keep track of how your changes affect the final result.

![](../../assets/843cf917adacba79.png)

In the depicted graph, I had just figured out how to obtain an effect of erosion of the bricks. The normal map is generated from a depth texture where darker shades are deeper depth. It would be easy to roughen up the surface by blending the depth texture with a noise texture, but this would make the surface rough everywhere. I wanted primarily the edges of bricks to be affected by this roughness.

The brick pattern I used for the bricks depth texture has a bevel size setting which is used to define the rounding size. I had used this pattern with a very small bevel for the depth texture itself, since the bricks should have fairly sharp edges. However, by using the same pattern with a much larger bevel, I got a texture which was darker near the edges of bricks and hence could be used as a mask for the noise texture. By subtracting the large-beveled brick pattern from the noise pattern, I got a texture that was only noisy at the edges of bricks. Well, it would have been noisy everywhere, but since all texture outputs have values clamped between zero and one, the negative values of the noise near the center of bricks becomes clamped to zero and thus not visible.

This kind of clever manipulation and combination of different patterns is what the main graph is all about. This is not specific to Substance Designer either - arguably this is how procedural textures are created regardless of the tool used. Through my previous work with POV-Ray, I already had extensive experience with thinking in this way, even though procedural materials in POV-Ray are defined in a text description language rather than a visual graph based tool. Compared to someone with no previous experience with creating procedural textures of any kind, this probably gave me an advantage in being able to figure out how to obtain the results I wanted.

There are some fundamental differences though. Some procedural material approaches are based on function evaluation. This includes the procedural materials in POV-Ray, or patterns defined in pixel shaders. These methods are not rasterized except at the very last stage. This means you can always easily scale a pattern up or down, even by factors of 1000 or more, without any loss of quality. They are perfect mathematical functions of infinite resolution. On the other hand, nodes in Substance Designer are rasterized textures. There are nodes that can be used to scale the input up or down, but up-scaling creates a blurry result as with any regular rasterized image. Some pattern nodes have a setting that can be used to scale the pattern up or down without loss of quality, but many other patterns have a hard-coded scale that you're basically stuck with. The rasterized approach has the advantage though that blurring operations can be done much cheaper than with a function evaluation based approach.

### Function Graphs

As mentioned earlier, each node in the main graph have various settings. Each of these settings can either be set to a fixed value in the user interface, or they can be setup to be driven by a function. Editing this function is done in a new window where you build up the function as a function graph.

![](../../assets/dee06eb5d5c6dfc0.png)

The function graphs look very similar to the main graph but the node types and connection types are different. Where the connections in the main graph are always either a color image or a gray-scale image, the connections in the function graphs are things such as floating point numbers, integers, and vectors.

In this case we're looking at a function driving the "Level In Mid" setting of a Levels node in the main graph. The very simple function graph I created looks like this:

![](../../assets/4427811e1e5f533b.png)

If you look at this simple graph, you might not know what it's doing despite the simplicity. It's subtracting some float from some float and using the result as the value for this setting. But which floats? The nodes show no preview information at a glance like the nodes in the main graph. Instead you have to click on a node to see in the settings view what it does.

In this graph the Float node contains a value of 1. And the Get Float node gets the value of the variable called ColorVariation. The code equivalent of the graph would be *outputValue = 1 - ColorVariation*. It's unfortunate that the content of the nodes, such as constant values and variable names, is not shown in a more immediate way, because this makes it pretty hard to get any kind of overview, especially with larger graphs.

That said, the ability to use a graph to drive any node settings you can think of is really powerful.

### Discovering FX-Maps

I mentioned earlier that I was most curious about the extend of the ability to define structured man-made patterns. It took me a while to figure out how to even access the part of the software needed to do that.

First of all, the software contains a "Generator" library with a collection of pre-built noise and pattern nodes. At one point I found out that these are all "main graphs" themselves and that the nodes can be double-clicked to inspect the main graph that makes up the generator for that node. The graph can't be edited right away, but if it's copied, the copy can be edited.

The next thing I found out - and this took a bit longer - was that the meat of all patterns eventually came from a node type called FX-Map. The FX-Map looks like it's a hard-coded node and it's functionality is impossible to understand based on looking at its settings. Eventually I found out that you have to right-click on an FX-Map node and choose "Edit Fx-Map". This opens a new window with a new graph. This is a new graph type different from the main graphs and the function graphs.

The FX-Map graph is the strangest thing in Substance Designer. It has three node types - Quadrant, Switch, and Iterate. The connections represent parts of a texture being drawn I think.

![](../../assets/e03e30854712053d.png)

Everything in FX-Maps boils down to drawing patterns repeatedly. A pattern is drawn inside a rectangle and can be either one of a set of hard-coded patterns (like solid colors, linear gradients, radial fills, etc.), or a specified input image.

Confusingly, drawing this pattern is done with a node called Quadrant. The Quadrant node can itself draw one pattern and it has four input slots that can be connected to other quadrants which will each draw in one quadrant of the main image. This is useful if you want a pattern that's recursively composed of quadrants of smaller patterns, but for everything else, having to draw patterns with a node called Quadrant even when no quadrant-related functionality is used is somewhat weird.

Anyway, if you want a pattern that's composed of patterns in a non-quadrant way, you'll need an Iterator node that takes a Quadrant node as input. The Iterator will then invoke the Quadrant repeatedly. The Quadrant node has settings for the pattern drawing and for the placement of the rectangle the pattern is drawn inside. By varying these settings (using function graphs) based on a hard-coded variable called "$number", the patterns can be drawn next to each other in various ways.

So far so good. But how would I create a nested loop in order to draw my brick wall with multiple bricks in each of the multiple rows? When programming a nested loop in a programming language, I'll normally have the outer iterator called *i* and the inner called *j* or something like that. But here, since the Iterator node is hard-coded to write the index value into a variable called "$number", the inner loop index overwrites the outer loop index. I looked at the FX-Map for the Brick pattern in the library, but it used a single iterator only. This can be done when all the rows have the same number of bricks by using division and modulus on the iteration value, but when each row have a random number of bricks, this trick doesn't work and a proper nested loop is needed.

### Getting Stuck With Advanced Stuff

Google was not of much help finding information on nested iteration. Searching for variations of "substance designer" together with "nested loop", "nested iterator" or similar would at best point to arbitrary release notes for Substance Designer, and at worst to pages not related to Substance Designer at all.

This is a general trend by the way. More often than not, when I needed details about something in Substance Designer, they were nowhere to be found whether looking in the documentation or using Google. Take the Blend node in the main graph for example. It has different blend modes such as "copy", "add", "subtract", "add sub", "switch", and more. I didn't quite understand all of those just from the names. The [manual page about nodes](http://support.allegorithmic.com/documentation/display/SD43/Nodes) only describe the blend node with two sentences and doesn't cover the various blend modes. If there's one thing Substance Designer really needs, it's to make sure all features and settings are documented.

In the end I had to write a mail to Allegorithmic support and ask them how I could do a nested loop. The first answer didn't contain concrete help with my problem, but there was an interesting snippet I found illuminating:

Before going into details, I think you experienced Substance Designer in the hardest possible way, trying to use FXMaps and functions for procedural textures. Although that was the case 3 years ago, and although you can still make procedural textures, Substance Designer is now more a kind of "compositing" tool for your texturing work. I would say that the procedural part of Substance Designer barely didn't evolve since that time, on the contrary to all the rest.

This is where I realized they're focusing on compositing over procedural, and upon reinspecting their website, it's hard to find any use of the word "procedural" at all today. I wrote a reply back explaining that my interest is in the procedural aspects regardless, and my aim to recreate my reference brick material as a procedural material in Substance Designer.

The second answer was a bit more helpful. It pointed to a [forum post](http://forum.allegorithmic.com/index.php/topic,1084.msg5777.html#msg5777) where community members had made experiments with advanced FX-Maps that contained nested loops among other things. But they were very complex and I had a very hard time understanding those without any kind of proper introductory explanation of the basics.

![](../../assets/507f05db5b81944c.png)

At this point Eric Batut, Development Director at Allegorithmic, came to my help. He had been reading my support email as well, and he replied with detailed explanations including an attachment with a basic example graph. The graph contained an FX-Map with nested Iteration nodes, all well commented using comments embedded in the graph.

I should say that I know Eric and other guys from Allegorithmic. We worked together in the past on implementing support for Substances in Unity (I worked on the UI for it). They might very well provide the same level of support for everyone though; I really can't say.

Part of my confusion had also been about a node type in the function graphs called Sequence, and this was explained as well. With my new found insight, I was ready to tackle implementing my own custom brick pattern with random widths and heights, and random number of bricks per row.

### Working With FX-Maps

FX-Maps get gradually easier to work with as you get used to them, but they're still a bit strange. Most of the strangeness is related to the way of controlling which order things are executed in.

If we look at the Quadrant node again, which is used for drawing patterns inside rectangles, there's a number of settings in it.

![](../../assets/e59f9472b8798553.png)

The thing to learn about these settings is that a function graph for a given property often doesn't just contain logic needed for that setting itself, but also logic needed for settings below it. You see, the graphs for the settings are evaluated in order, and whenever a node in one of those graphs is used to write a value to a variable, that value can then be read in graphs of the subsequent settings too, because all variables are global - at least in the scope of the main graph.

So in the example graph I was given, the Color / Luminosity setting's function graph doesn't just have logic for determining the color of the pattern being drawn; it also has logic that read the "$number" variable and saves it into a variable called "y". And the Pattern Offset setting's function graph calculates and saves a vector values called "BoxSize" which is then used both by the graph of the Pattern Offset setting itself as well as by the graph of the Pattern Size setting.

The execution order of nodes within the function graphs themselves are controlled using Sequence nodes.

![](../../assets/80c2c56f12d2405b.png)

Sequence nodes have two input slots that are executed in order - first the sub-graph feeding into the first slot is evaluated, then the sub-graph feeding into the second slot. The sequence node itself returns the value from the second slot, while the value of the first slot is simply discarded.

Again, the approach works once you get used to it, but it's still somewhat strange. It means function graphs are even harder to get an overview of, because you can't assume that the nodes in it are related to the settings this graph is for. Some or all nodes might be just some general-purpose calculations that needed to be put into this graph for timing purposes. Nevertheless, it can get the job done.

One last strange thing about FX-Maps. Like I mentioned earlier, what an FX-Map node does can't be gathered from its settings at all. I learned that the FX-Map instead has direct access to the variables defined in the main graph - basically there's zero encapsulation. This makes FX-Maps very tied to the main graph they're inside. Normally this would be very bad, but it does seem like FX-Maps are not designed for reuse at all anyway. An FX-Map is always embedded inside a main graph, even if the FX-Map is the only thing in it.

### Reuse of Graphs

Now for some good news. Like mentioned earlier, all the noise and pattern nodes in the built-in library are their own main graphs, and it's very easy to make new custom nodes as well. In fact, nothing needs to be done at all. Any main graph can be dragged into another main graph and then appears as a node. The output maps of that graph automatically appear as output slots on the node, and the settings of the graph automatically appear as setting of the node. Though I haven't used the feature myself yet, graphs can also define input images, and these, I'm sure, will appear as input slots on the node.

Function graphs can also be reused. FX-Maps can't, but this is probably ultimately a good thing, since it's easier to make everything be able to connect together when there is only two types of graph assets that can be referenced.

In my own material I ended up with a design with three different main graphs

**VariableRowTileGenerator**

An FX-Map that draws patterns in a brick formation. The patterns can be set to be gradients (in 90 degree intervals) or solid color. Randomness can be applied to the luminosity of each pattern.

![](../../assets/d99eb0e3c1766505.png)

**VariableRowBrickGenerator**

More high level processing built on top of the VariableRowTileGenerator. This includes bevels and slopes (gradients at random angles not constrained to 90 degree intervals).

![](../../assets/17859a55fa4a09fa.png)

**VariableRowBricks**

The is the final material. It references nodes both of type VariableRowTileGenerator and VariableRowBrickGenerator as well as some noise nodes. Lots of custom processing on top.

![](../../assets/e6c9804e6f431161.png)

Actually I used a few more main graphs. I ended up copying and customizing some noise graphs from the library because I wanted them to behave slightly differently.

The ability to super easily reuse graphs inside other graphs is very powerful and definitely a strong point of Substance Designer, both usability wise and in terms of raw functionality.

### Limitations

I'm almost towards the end of my impressions, but they wouldn't be complete without some thoughts about what it is possible to achieve and what simply isn't possible, since that's what I set out to find out about.

Basically, Substance Designer is not Turing complete, and as such you can't just implement any pattern you can think of an algorithm for. Specifically the lack of being able to work with arrays means that some common patterns are out of reach. Sometimes there will exist some workaround that produces a very similar result though.

One example is Perlin noise. The library in Substance Designer contains patterns called Perlin noise but they're not really Perlin noise. Nobody would ever care that it doesn't use the correct algorithm though - it easily looks close enough.

Another example is a pattern often called crackle or voronoi crackle. It's a very versatile and useful pattern that is defined as the difference between the closest and second closest point out of a set of randomly distributed points. It's great for cracks, angular bumps, and many other things, and I happened to need this pattern for the cracks in my brick wall.

![](../../assets/b6e336327c150801.png)

I don't think it's possible to generate a crackle pattern in Substance Designer. There's a pattern in the library called Crystals which seems to be very inspired by it both in looks and implementation. I tweaked it a bit to be even closer to crackle, but it still doesn't quite have the same properties. In the original crackle pattern, each cell is convex and has only a single peak. In the Substance Designer substitute some cells are partially merged together which gives a non-convex shape with multiple peaks. The workaround just about worked all right in my use case, but it's enough visibly different that it might not work out for all use cases.

### Results

All right, let's have a look at how close I got to the reference material I was trying to recreate in Substance Designer.

![](../../assets/c59515300bfb2d03.png)

I think it got very close! Don't pay attention to specific rows having different heights or number of bricks than in the original, or other specific differences like that. I designed that to be determined by the random seed, so I have no direct control over that. The important part was that it should look like it could have been a part of the same brick wall, just somewhere else. It's close enough that I'll happily use this substance instead of the original material.

![](../../assets/a2069872d07748cd.gif)

![](../../assets/02887e93466df0f1.gif)

The substance material of course has the advantage of being able to recreate randomized variations of itself on the fly where the random widths and heights and locations of cracks are different. This on its own is already pretty nice, but with some additional work I can implement support for qualitative variations too. I could add sliders for varying the bricks between shiny new and old and crumbled. I could add fields for specifying the main color, and a slider for the amount of color variation of the bricks (right now there's always just a tiny bit). I have some other ideas as well, but I'm sure your imagination is as good as mine.

I hope you found these impressions useful or interesting, and that you may have learned something new about Substance Designer, whether you knew nothing about it before or was already using it. Are you considering using Substance Designer for your game, or are you already using it? I'd like to hear about your impressions as well!