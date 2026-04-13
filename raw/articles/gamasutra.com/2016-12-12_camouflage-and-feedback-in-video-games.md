---
title: Camouflage and feedback in video games
url: https://www.gamedeveloper.com/audio/camouflage-and-feedback-in-video-games
author: Kevin Sultan
published: '2016-12-12'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

# Camouflage and feedback in video games

This article summarizes the main principles of camouflage and makes a short assessment about how video games use it to create interesting stealth gameplay - or deliberately ignore it to provide better feedback in any genres.

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

I played Tom Clancy's The Division a lot. As my friends couldn't match my rhythm, I used to spend many hours roaming alone in the Dark Zone. Yet, it constituted a quite painful experience: groups of players never hesitate to assault you and single players are greatly encouraged to do so as soon as you are looking away. The more I was playing, the more I developed habits to remain as invisible as possible from other players and realized these habits were directly inspired by my training as an Alpine Hunter in the French Army. Of course, I can’t speak about some aspects dealing with squad tactics and overall strategy as it would transgress military NDAs. However, camouflage techniques are worldly known and most specialized websites already speak about it. I would like today to share this knowledge and make a short assessment about how video games exploit it to create stealth gameplay or, at the contrary, deliberately ignore it to provide better feedback in any genres. |
|


# A BIT OF HISTORY


Wikipedia defines the camouflage as « the use of any combination of materials, coloration, or illumination for concealment, either by making animals or objects hard to see (crypsis), or by disguising them as something else (mimesis) ».

[Most animal species have acquired crypsis or mimesis](http://www.boredpanda.com/animal-camouflage/) during Evolution to avoid getting spotted by predators or prey. There are few examples of military use of camouflage before the 19th century – the oldest one refers to recon ships painted in venetian blue during the Gallic Wars to better merge into the sea.

During the 19th century, the British Army was the first to officially abandon shimmering uniforms in favor of khaki ones which were more appropriate for the hot climate in its colonies. It turned out to also better conceal its units. However, camouflage techniques only generalized when the French Army formed its own camouflage corps during the First World War. According to Wikipedia, the term camouflage incidentally comes from a Parisian slang term meaning “smoke blown in someone’s face”.


# PRINCIPLES


The French Army uses the mnemonic term FOMECBOT to teach the main principles of camouflage. Several variations have been established since my duty ended, I will only speak about the original principles I learned. Feel free to share the English equivalent, I couldn’t find it.

![FOMECBOT FOMECBOT](../../assets/818c852e89a0f543.img)



# SHAPES AND COLORS


Principle:

Former military uniforms were dyed in bright colors to glorify soldiers and more easily enroll new recruits. Yet, each environment is composed of a specific color palette which rarely matches these uniforms and soldiers were remaining easily identifiable – even in a dense forest. The human shape easily also stands out from the background – no matter the color of our outfit – as we naturally recognize the features of other human beings. This is why most of the uniforms are not only based on a single color matching the environment but also include several patterns to break the human shape. |
|


Creating stealth gameplay:

Most stealth games base the visual detection of an NPC on a cone sensor which can be more or less long and wide. Some games, however, go further into the simulation. Several episodes from the Metal Gear series offer, for example, concealing bonuses according to the patterns and the environments the character progresses through. The choice of the pattern then directly affects the route the player is encouraged to follow – enhancing his [Autonomy](http://www.gamasutra.com/view/feature/130155/rethinking_carrots_a_new_method_.php), the tactical aspect of the game and its replayability.

Metal Gear Solid 3: Snake Eater |
|

The Metal Gear series is also well-known for his camo devices which makes the player character [(almost) invisible](https://www.youtube.com/watch?v=vadHJc7pXZ8) in the same way animals uses mimesis. This mechanism is also part of many games such as Ghost In The Shell: First Assault or the Aliens vs Predator series. It became some kind of “special mode” obviating most of shape and the color principles of the camouflage. Yet, restrictions always compensate the use of such devices as becoming invisible offers a considerable advantage – especially in multiplayer games:

The player character remains clearly visible at short range

The player character remains invisible only for few seconds, the device being subject to a cooldown

The player character remains invisible only while idling

The player character remains easily detectable by infrared devices

The player character cannot use another item

The device can be short-circuited with EMP

Ect.


The Hitman series - which I especially like - also plays on a narrative dimension. The context assumes the role of the environment while the outfit worn by Agent 47 defines the shape and the color of his camouflage. A black-suited stranger transporting a briefcase and wandering in a villa would catch the guards' attention. Disguised as a repairman, his presence could be justified. In his blog article, Stanislav Costiuc names this kind of gameplay "[social stealth](https://stanislavcostiuc.com/2016/08/28/why-assassins-creed-series-isnt-social-stealth-and-what-to-do-about-that/)" and analyzes its use in the Assassin's Creed series.


Breaking the stealth for better feedback:

The simplest way to emphasize an element of interest consists in painting it in a contrasting color to make it stand out from the scenery. The player consequently can see it from a greater distance and easily guess the element is interactive - even before knowing what the interaction is.

I especially like the example of the contaminated bag from Tom Clancy’s The Division that player characters use to stock the items looted in the Dark Zone. Going rogue is always risky - even while playing in a group. Yet, the contamination bag explicitly indicates if a player has looted items and so assaulting him could be rewarding. As a player trying to remain as invisible as possible, this feature also encouraged me to ignore low-interest items and kept me under pressure while trying to extract high-end ones. |
|

Note however that, as Peter Angstadt underlines, allocating a color to an element of interest is usually not enough to [reduce the visual confusion](http://www.gamasutra.com/blogs/PeterAngstadt/20150312/238446/How_to_Reduce_Visual_Confusion_in_Your_Game.php). For example, the explosive barrels (red) greatly stand out from the snowed environment but are difficult to see in dark interiors. This is why he recommends to also adjust the saturation and the luminosity of each asset.


# MOTION, SHADOWS AND GLARES


Principle:

Although shapes and colors constitute the main principles of camouflage techniques, the other visually-based principles – motion, shadows and glares – should not be underestimated.

Indeed, we instinctively get attracted by the sight of movements as anything moving could constitute a threat. Sudden or large movements can then reveal a unit - no matter the color/patterns of its uniform. Remaining as static as possible is then desirable. It may sound pretty easy but I assure you it requires way more self-control than you think. There is always a great temptation to further conceal while facing enemies. However, any movement could catch the enemy attention.

Concealing doesn’t only concern the body, but also its shadow which can easily betray a soldier’s position. This is especially true while standing behind a tree or in the corner of a street. Contrary to the popular belief, shadows are also visible in most of interior/night environments. There is always a source of light. Finally, soldiers often forget that some equipment such as scopes, metallic watches or badges can emit glares by reflecting the light and can catch the enemy attention. Think about Indiana Jones getting spotted on a hill in The Last Crusade. |
|


Creating stealth gameplay:

In video games, motion is often bound to the noise emitted by running characters as I will later speak about. Many games offer concealing bonuses – or even a total invisibility like mimesis – as long as the character remains static. Examples are plentiful from Elves in the RTS Warcraft III to camo devices in Metal Gear Solid V: The Phantom Pain. This last game incidentally provides additional bonuses while playing dead thanks to a "stealth mode" which is automatically disabled when the character starts moving again.

Note, however, that the player is the main driving force while infiltrating enemy positions. He can put his controller down, peacefully plan his next actions and could even have a break if his character is concealed enough. The experience is completely different when he gets tracked by opponents: they are aware of his presence and actively look for him. The player must then decide either to remain concealed or to move away. The experience in stealth survival games such Alien: Isolation is very immersive as the player character is especially weak and the [Alien’s behavior unpredictable](http://kotaku.com/alien-isolations-worst-aspect-the-unpredictable-alien-1607096520). Now imagine a VR game based on the player's actual motion such that any head movement could betray his position. The experience would be then extremely close to the real life.

Shadows, as described in the camouflage principles, are rarely used to encourage the player to remain concealed. Indeed, the camera point of views usually prevent the player from seeing his character’s own shadow. Affecting the gameplay according to an element the player can’t see would be extremely frustrating. Let’s, however, note that many games include interior or night sceneries to play with light and shadow areas. The shadow areas then match safe areas where the player character can rest and plan his next actions while the opponents patrol in the light areas where the player can easily spot them.


Breaking the stealth for better feedback:

As previously stated, we instinctively get attracted by the sight of any movement. This feedback can then be used to point out locations of interest: birds flying away in the distance, shaking bushes, blinking lights, even the animated coins from Super Mario Bros easily catch the player’s attention.

Likewise, plays of light can be exploited to encourage the player to follow specific routes. For example, Left 4 Deadonly includes night and interior maps. This choice certainly adds to the ambient atmosphere but also allows the developers to orient the player throughout the map. Here an example from No Mercy:

![Click to enlarge! Click to enlarge!](http://www.kevinsultan.fr/autres/nomercy_small.png?width=500&auto=webp&quality=80&disable=upscale)

[ ](http://www.kevinsultan.fr/autres/nomercy_large.png)

Left 4 Dead (click to enlarge)

Tom Clancy's The Division also exploits shadows and glares from a gameplay point of view. For example, spotlights in the [Lincoln Tunnel](https://www.youtube.com/watch?v=8iivsSNaIY8&feature=youtu.be&t=799) greatly help the player to anticipate incoming enemies thanks to the shadows it projects on the walls. Likewise, the sniper rifles in the game usually deal very high damage. However, a [glare explicitly appears](https://youtu.be/13QL7bgjLrk?t=1478) on the rifle's scope every time a character aims through it - betraying the sniper's position and alerting the player about the danger such that he is encouraged to find cover.


# TRACKS, HEARING AND SMELL


Principle:

The term tracks refer to any elements which could betray your earlier passage: footprints, bullet shells, detritus, campfires, cracked branches, open doors, ect. This principle adds a temporal dimension to the camouflage which should never be neglected: infiltrating enemy positions or escaping pursuers are long-term objectives which can last hours or days. Many tracks could be left behind during this lapse of time.

Camouflage is not only based of the visual detection, but also relies on the hearing and the sense of smell. Soldiers must always watch out for noisy elements such as detritus in urban environments or twigs in forests. Likewise, food, powder and sweat can easily betray their position. Beware of dogs: a [study from the CIA](https://www.cia.gov/library/center-for-the-study-of-intelligence/kent-csi/vol5no2/html/v05i2a04p_0001.htm) estimates that they can hear a sound 4 times the range humans do and have about 25 times more olfactory receptors than us.


Creating stealth gameplay:

Tracks add a temporal dimension to the camouflage. Opponents react while discovering dead bodies, blood pools or snow footprints in most stealth games. It both emphasizes the Level Design and encourages the player to think twice before acting. Killing a target and vanishing back to a safe position is one thing, slowly transporting his body to a hideout while patrols could spot the player character is another. Once again, Hitman is an excellent example illustrating original ways to implement such a feature. Hitman: Blood Money greatly encourages the player to remain unnoticed thanks to a notoriety system. A newspaper is displayed at the end of each mission and summarizes the player performance. The overt he plays, the more accurate the identikit is and the harder the game becomes during next missions as opponents would more easily recognize Agent 47 – no matter his disguise. |
|

Hearing in stealth games is logically transposed as a simple radius of sound that can be heard in 360 degrees. According to the complexity of the game, opponents can have one of several radii detecting different sound intensities. It encourages the player to move slower, to preferably use blades/silenced weapons and to avoid noisy surfaces – directly affecting his route.

But hearing can also be easily exploited to distract opponents. Throwing a kunai in Mark of The Ninja, a stone in Far Cry 4, a bottle in Rise of the Tomb Raider or an empty clip in Metal Gear Solid V: The Phantom Pain are indeed easy ways to force an opponent to investigate at a specific position – making him more easy to kill or freeing the way for the character to advance.

Mark of The Ninja |
|


As previously stated, animals have better senses than humans. Implementing this in gameplay is always quite tricky: animals shouldrepresent a greatest challenge than humans but overly realistic tuning could considerably increase the game difficulty. This is why some games such as Cabela’s Big Game Hunter take in consideration the strength and direction of the wind. The detection radius is then dynamically shaped into a cone which greatly encourages the player either to wait for the wind to shift or to find a better route to approach his prey. This system certainly offers a good alternative but is also quite difficult to expose and requires important real-time feedback.

As far as I know, Tenchu Z is the only game where humans are actually able to smell the player character as a full gameplay feature. The more violent he kills, the more he reeks of blood and gets easily spotted by opponents. This feature is especially interesting as it combines both an under-exploited sense and the temporal dimension of tracks.


Breaking the stealth for better feedback:

From these three aspects, hearing is undoubtedly the one able to provide the most efficient feedback - based on sound effects or the music (or, at the contrary, the absence of sound effects or music). The player can then anticipate opponents or events even before seeing them. This is the case, for example, of all uncommon Infected in Left 4 Dead.


The information they provide is just as important as their position: NPC opponents can reveal information about the Level Design, their weaknesses or – during combat – the tactical moves they are going to perform (“I’m reloading!”, “Cover me, I overflank him!”).

There are examples of tracks implemented as gameplay. In [The Witcher 3: Wild Hunt](https://youtu.be/z6TbWp-j930?t=149), Geralt Of Rivia is for example able to use his mutant vision to highlight the footprints of all kinds of creatures. The designers then play on the Level Design to take him throughout difficult locations. Tracks can also be exploited as simple feedback: blood trails, corpses, burn marks on the floor, ect. All of them can alert the player about imminent dangers in a very efficient way while enhancing the atmosphere by inferring short stories.

Dead Space |
|


Earlier this year, Ubisoft revealed the [Nosulus Rift](https://www.youtube.com/watch?v=kqMehNbzICQ) – a parodic version of the VR headsets that would make the player able to smell his character farting in South Park: The Fractured But Whole. This obviously was a joke. But think about the gameplay based on the scent that we could create in stealth games: detecting enemies by smelling fire camps, cigarettes, vehicles or trying at the contrary to conceal the player’s own smell while being tracked, ect.


# SUMMARY


To summarize, camouflage techniques include several principles relating to many human senses - not only vision. It only developed as a military discipline from the end of the 19th, century although animals have use it to chase or evade predators since the dawn of time.

Video games obviously use camouflage techniques to emphasize stealth gameplay. However, some principles such as the sense of smell still remain quite difficult to transpose as gameplay mechanism.

Designers can also voluntary ignore the camouflage principles to provide further feedback to the player in any genres. I strongly recommend taking a look at the following video by Clément Melendez to demonstrate how this feedback is efficiently exploited in F.E.A.R. 2.

Scientists are close to a breakthrough in camouflage techniques by creating mimetic devices. But like I previously stated, this mechanism already exists in video games for a long time and has always been subject to balancing compensation. I am convinced that VR headsets could be the answer for renewing stealth gameplay and creating more immersive experiences. What is your opinion about it? What other examples of original gameplay do you have in mind?

Food for thought: