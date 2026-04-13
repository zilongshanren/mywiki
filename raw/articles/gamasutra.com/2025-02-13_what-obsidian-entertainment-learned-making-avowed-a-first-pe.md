---
title: What Obsidian Entertainment learned making Avowed a first-person fantasy RPG
url: https://www.gamedeveloper.com/art/what-obsidian-entertainment-learned-making-avowed-a-first-person-fantasy-game
author: Bryant Francis
published: '2025-02-13'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![Kai, a washbuckling blue-skinned companion from Avowed, wields a blunderbuss and saber. Kai, a washbuckling blue-skinned companion from Avowed, wields a blunderbuss and saber.](../../assets/2d85cde9f5d9dbbf.jpg)

## At a Glance

- Avowed, Obsidian Entertainment's new fantasy RPG, is a first-person fantasy RPG set in the world of Pillars of Eternity.
- The Pillars of Eternity series was a top-down computer RPG, and played very differently than Avowed.
- Nailing the first-person view meant prioritizing visual effects, animation, and gameplay for close-range combat.

This week Microsoft-owned Obsidian Entertainment is releasing Avowed, a first-person fantasy role-playing game set in the same universe as the Pillars of Eternity series. Though the studio is no stranger to making first-person RPGs like Fallout: New Vegas and The Outer Worlds, bringing the Pillars series to first-person is a hefty challenge. The existing audience is used to turn-based combat and top-down exploration. And when it comes to first-person fantasy—well, every game in the field is likely to be compared against Bethesda Softworks' The Elder Scrolls V: Skyrim, the 800lb gorilla of the genre.

It's a tall task to be sure. Game Developer previously spoke with game director [Carrie Patel](https://www.gamedeveloper.com/design/avowed-director-carrie-patel-explains-how-obsidian-pushes-boundaries-in-the-fantasy-genre) about translating the wild world of the Pillars series to first-person fantasy, but we had more questions about the technical nitty gritty of the transition. When you play Avowed, you quickly notice it feels distinctly different from the fantasy epic made by Obsidian's cousins at Bethesda. There's a certain snappiness to how the player animations feel, and the use of "hit stops" supercharges the impact of every swing of a sword, axe, mace, or other melee medium for violence.

The details are dense—but luckily gameplay director Gabe Paramo, lead VFX Artist Ash Kumar, and senior animator Seth McCaughey had answers for us and fellow developers. In a conversation earlier this month, the trio broke down how those hit stops—alongside carefully-crafted motion trails, 60 FPS source animations, and player response to the 2023 Xbox Showcase—were all key parts of making the game's combat so punchy and unforgettable.

## Early multiplayer design had long-term payoff

You might recall that when Obsidian first teased Avowed, it mentioned the game would include optional co-op multiplayer. That feature was cut later in development (in [a 2023 documentary](https://youtu.be/Oo9ZYDRQkbg) the team explained designing for multiplayer was interfering with single-player pipelines), but elements of its design were "foundational" for the first-person combat of Avowed.

Paramo broke down how in a rather technical explanation, beginning with how the team was designing animations in Unreal 4 (and later Unreal 5). Paramo set up much of the initial combat design. The goal, he said, was to make sure a player's console or PC could replicate the third-person view on another player's machine during multiplayer gameplay.

"We needed to be able to utilize Unreal's [slot system](https://dev.epicgames.com/documentation/en-us/unreal-engine/animation-slots-in-unreal-engine) in their [[animation] montages](https://dev.epicgames.com/documentation/en-us/unreal-engine/animation-montage-in-unreal-engine), so that you'd basically have two tracks simultaneously going on. Then, depending on whether you're in first or third-person view, they're in that perspective, running that animation tree, and running that slot," he said.

Translation: In order to design Avowed's first-person view, Obsidian needed a functional third-person camera that could capture the animations of another player and let a player in first-person see what the other player was doing in third-person. That made the third-person camera that ships with Avowed (useful for players who might get motion sick in a first-person view) a "foundational" part of the game.

Developers familiar with multiplayer animation know there are inherent limitations to animating objects and characters in a way that can be efficiently tracked by two machines across great distances. Even with the multiplayer features removed from Avowed, the work put into the Unreal slot systems was also "foundational" for the final game. "The constraints of animation timing and keeping those things in sync—if you don't do that, the gameplay feels off-sync on another person's machine," Paramos continued. "I think that's where it all started from."

![A beautiful view of The Living Lands in Avowed. A volcanic landscape, coral-looking plants, and ancient buildings dot the world. A beautiful view of The Living Lands in Avowed. A volcanic landscape, coral-looking plants, and ancient buildings dot the world.](../../assets/598a85efce31ee83.png)

Image via Obsidian Entertainment/Microsoft.

Throughout that process, the team began reckoning with the challenges of a first-person combat system that would be dominated by melee attacks. Players can use guns, bows, and magic pepper enemies from a distance, but in the fantasy world of Pillars of Eternity, enemies are always rushing toward the player with a violent urge to be smacked upside the head. McCaughey explained that melee animation is "a lot more difficult in first-person to make it readable and feel comfortable."

He called out how much time the animation team spent on "motion trails"—subtle animations that follow the movement of the players' weapons as they attack. They're not generally visible to the human eye, but their presence tricks the brain into getting a more clear sense of how objects move in the game. It's the equivalent of adding "woosh" noises to swords in fantasy movies. Swords may not make those sounds in real life, but it helps the viewer sense how heavy a swing is.

"We pushed the source animations of those to up to 60 frames per second to get good, clean motion trails and good readability," he said, adding that Avowed's motion trail rendering is calculated in real-time. "You need lots of samples so they aren't taking a strange path through the frame as they go."

If the motion trail animations don't work properly, they might render in a completely different direction from where the player swings. Imagine swinging your sword left-to-right, but an animation appears showing from right to left. "Or in a loop de loop," McCaughey said with just a hint of exasperation.

## Making visual effects that play up-close and personal

A number of weapons and magical spells in Avowed generate a mix of flashy, colorful visual effects. You've got fireballs, chained lightning, sparks of energy shooting out of a wand, and more. In a strictly third-person game, those effects would render in the midground of the environment. When you're in first-person view, those big effects are playing front-and-center.

According to Kumar, that means the fidelity of the animations needed to be "way higher" while being careful about how much space they took place on the screen. What helped, in part, was the creation of "hit stops" on all the weapons that play on the animation as the player makes contact with the enemy.

"Hit stops" for the uneducated (like I was before this conversation) are brief pauses in an animation where an object freezes, then accelerates to mimic the feeling of colliding objects. Kumar said combat designer Max Matzenbacher was the one responsible for implementing them in Avowed, and explained those brief pauses were a huge opportunity for the VFX team to spice up the combat visuals.

"On the effects side, we try to underline it with different bludgeoning, slashing, or piercing effects," he explained—largely referring to blood spatters. Those spatters, he said, also had to play differently between first-person and third-person view, because the different camera position would automatically make the effects play at different distances.

McCaughey said Avowed's hit stops have another interesting feature. "They're not just a pausing of the animation," he said. "It actually branches to [another] unique animation where the weapon hits and draws through—the blade hits, is deflected, and pulls through the cut so you can feel the difference between swinging at air and swinging and hitting the target."

![The player character swings a melee weapon to hit a lizardlike Xaurip. The player character swings a melee weapon to hit a lizardlike Xaurip.](../../assets/2faa2716584c1ed7.png)

Image via Obsidian Entertainment/Microsoft.

The system also accounts for attacks on enemies whose defenses are too strong for the player's current power level. Different animations play on those attacks that show the player's weapon bouncing off the target instead of powerfully swinging through.

That's a new trick for Obsidian—if you study the animation of The Outer Worlds, you'll notice it has conventional swinging animations for melee weapons, with no fancy redirects based on where the blow lands.

Tuning all of these animations and effects, as always, demanded hours and hours of staring at fast-moving loops to assess if what they'd created felt good for players. With so many different moving parts, we wanted to know how Mcaughey, Kumar, and Parano could keep track of the different variations and figure out what worked and what didn't.

It turns out they had an unusual reference point. Parano explained that after the Avowed gameplay reveal trailer shared in the [January 2023 Xbox Showcase](https://youtu.be/HvNw8a0ls3Q?si=7JfyTIS7aoGyjPNw), Obsidian spotted critical feedback from some prospective players worried about the feel of the first-person combat. The studio already planned to polish up what was in the trailer, but now they had a precise reference point of what didn't feel good to compare and contrast against.

"That kind of kept me sane at least," he admitted. It was a strong baseline to make incremental adjustments against—a video that could answer the question "does this feel better or worse?"

Of course Obsidian is in a rare position to take advantage of a preview like that. Microsoft's interest in promoting its own games means they got a premiere opportunity to put the game in front of thousands (millions?) of eyeballs and see what players thought. They also had time to react to that feedback. Developers with less marketing power and shorter runways don't have that opportunity, but those working on Early Access games or building closed beta programs have a chance to learn from Obsidian's experience here.

## Animation bugs can be extra fun

Because animation and visual effects are such a—well, visual—experience, it's where developers can encounter a battery of bizarre bugs, the kind that break your workflow because you just stop and laugh. So, which bugs are currently living rent free in the heads of Obsidian's dev team?

First there was the "giant sword" bug. "Certain enemies, if they were standing around you and then you engage them in combat, would just come at you with a weapon three times the size as they are," Mcaughey said. "There was an animation bug where some of the scales on the weapon joints had accidentally been set to zero during the idle animations. If that got interrupted the game miscalculated how big those bones should be."

Parano said facial animation bugs are the ones that always stick out to him—prompting Mcaughey to bring up a bug where he accused a non-playable character of being a "coward," and that NPC reacted by shoving his arms through his own torso.

Apparently the team at Obsidian are big fans of what you might call the "mouse door" bug. "What the issue was," Parano explained "is that we made a very systemic game where lots of things share properties." And because mice have the same "AI brain" as other NPCs, they would sometimes have access to the same properties as humanoid creatures wandering the city.

And so you might be testing a build of Avowed, round a corner, and see a tiny mouse walk up to a door, open it, and walk through like it owns the place.

With Avowed, the longtime RPG studio is once again showing how developers can push the technical boundaries of games without compromising on core gameplay or ambitious storytelling. First-person fantasy games are going on three-decades old, but Mcaughey, Kumar, Parano, and their colleagues show there are still incredible ways for developers to innovate in the space.