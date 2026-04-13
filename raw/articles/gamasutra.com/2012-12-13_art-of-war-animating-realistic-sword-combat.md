---
title: 'Art of War: Animating Realistic Sword Combat'
url: https://www.gamedeveloper.com/art/art-of-war-animating-realistic-sword-combat
published: '2012-12-13'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

# Art of War: Animating Realistic Sword Combat

This article -- a compilation of two viewpoints on adding authentic sword combat to games -- originally appeared in the December issue of Game Developer magazine -- and explores the idea of using real Medieval techniques as taught by a trained sword master.

December 13, 2012

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

Author: by John Clements

This article -- a compilation of two viewpoints on adding authentic sword combat to games -- originally appeared in the December issue of Game Developer magazine. You can [subscribe](http://gdmag.com/subscribe/) to the print or digital edition at GDMag's subscription page, [download](https://itunes.apple.com/us/app/game-developer/id460170934) the Game Developer iOS app to subscribe or buy individual issues from your iOS device, or [purchase](https://store.cmpgame.com/category.php?cat=18) individual digital issues from our store.

# Eben Bradstreet on Real Combat

The first time I walked into John Clements's Iron Door Studio, I learned how to hold a longsword.

I thought it was obvious: Grip the handle with both hands. That's how I'd always imagined it was done. It's how they did it in the movies, after all. The handle is the comfortable bit between the pommel and the cross-guard. It's large enough to accommodate both hands. So I hold it there, right?

Wrong. The right hand (or the leading hand) indeed goes just below the cross-guard. The left hand should grip the weapon by the pommel -- that's the knob at the end of the handle -- in most circumstances.

At first, I was a little dubious. "Hold it there? Really? I thought that part was just for smashing skulls. Or balance. Or decoration."

My mind drifted to Orlando Bloom in an early scene in Kingdom of Heaven, where it's quite clear that he grips his weapon in the way that seems most harmonious: by the handle, with both hands. Later in the film, he even helpfully confirms my bias by smacking someone in the noggin with his hand-free pommel.

![](../../assets/f569488332383b97.img)


Figure 1: The proper way to hold a longsword.

The reality of the pommel is a little more complicated. It is used to knock sense into your enemies, it does affect the balance of the sword, and sometimes it's even pretty to look at. But, it's also a great place to hold the weapon. And it's a perfect example of how all my assumptions about the sword were challenged when I first set out to learn the reality of the weapon.

# Grounding Fantasy in Reality

As it turns out, how to hold the longsword is also a great place to start talking about what that reality can mean for animators. If a video game character grips the pommel with its trailing hand, the resulting animation will have fewer problems with deformation around the wrist, less clipping between the sword's mesh and the character's mesh, and will display better biomechanics when cutting (which we'll talk about later).

The first two points are subtle improvements, and are best demonstrated by gripping the handle by both hands, then extending the sword forward, holding the weapon at eye-level. From this position, start turning, windmilling, and cutting with the weapon while keeping it in front of you. If you don't have a sword immediately available, you can do this with any wooden or plastic dowel. Just hold the dowel roughly three to five inches from the end in order to simulate the exposed pommel.

As you swing, pay attention to how often the pommel wants to intersect with your wrist, especially when you try to drop the blade to the lower right, and note that in some positions, you can't continue an arc because your trailing wrist simply won't contort enough to facilitate the movement.

As I said, these are subtle points. The real magic happens when you now try the same thing, but grip the pommel, instead of the handle, with your left hand. The first thing you'll notice is just how much more leverage you have. The sword is a lever, after all, and your leading wrist is the fulcrum, so it makes sense that the further back from the fulcrum you're able to grip, the more control you'll exert on the blade. You should also notice that this method is easier on your wrist (which will help with deformation), especially if you allow the pommel to slide and turn freely in your palm. Your wrist can now stay relatively straight through most swings, and there's no longer any danger of the pommel clipping through the wrist's mesh on your character models.

# Bad Sword, Bad Reference, Bad Animation

Inevitably, you'll want to capture some reference. Even if you're using motion capture, it's always good practice to "feel" the movement yourself, or to whip out a camera and go through some of the motions.

The best way to not get good reference, no matter how you decide to hold the sword, is to use a crappy weapon. For most people, the easiest access they have to a generic sword is either through a catalogue, a renaissance faire, or even the odd novelty store. With the rare exception, the weapons you get from these sources are universally terrible for your animations -- they're often much too heavy and poorly balanced.

We have one of these weapons at my workplace, and even after two years of swinging steel as a martial art, I still can't do anything with it. That weight transcends physical reality, and every skilled attempt to mitigate it directly influences how our characters move. It's an awkward and sluggish prop that makes our characters look equally awkward and sluggish. Early on, we decided not to use it.

![](../../assets/188ee70a630d124e.img)


Instead of trying your luck with weapons that will harm your animations, it's almost always better to simply go to a hardware store and buy a wooden dowel, or a length of weighted PVC pipe. If you're feeling crafty, you might even want to make your own wooden sword (historically called a "waster"). Wooden props like these will certainly be much lighter than steel, but they'll be easier to swing in a good way (good for the director, the animator, and the actor). The alternative is a poor knockoff that will cheapen your results by virtue of your trying to use it, rather than just hanging it up and staring at it (as it was made for). Bad swords make your job more difficult than it has to be.

The weapons that John and I are using in these images are made by Albion Swords (www.albion-swords.com). There can be long waiting times for these weapons, so it may not be an ideal solution for gathering good reference quickly or cheaply.

# All About Universal Biomechanics

As I learned more about the art of fighting with the longsword, as Medieval and Renaissance Europeans understood it (and actually chronicled in dozens of study guides), I began to understand how intuitive the whole skill set actually was. There are a few basic guards, roughly nine vectors of attack, and a handful of rules that guide your footwork. The more advanced techniques, while impressive to look at, are largely ancillary: In all the sparring matches I've seen, the flashier techniques are never used. In fact, the more I watched and the more I learned, the more it started to feel familiar.

That sense of familiarity didn't come from the movies or the stage -- and certainly not from the highly sportified world of foil fencing. No, the moves I was seeing in sparring matches, which were reflected in the historical imagery plastered on the walls around me in John's studio, looked more like the close-quarters combat training we'd done while I served in the Army, or mixed martial arts matches on TV. It was savage and in-your-face. There was nothing at all pompous or chivalric about it. This stuff was real, and it was universal -- because no matter what time or place we come from, we're all human and we're all governed by the same biomechanics.

Consider the weapon we've been talking about. If I had been handed this weapon three years ago and someone told me to swing it, I would have done what pretty much anyone would do. Maybe swing it like a baseball bat, or because I used to cut wood when I was kid, I might swing it like an ax. If you were handed that weapon, what would you do? You might try to mimic what you'd seen Conan do, or imitate a samurai.

![](../../assets/1835e5eb4c81453b.img)


What you wouldn't do (at least, what most of us wouldn't do), is swing it like a golf club. But why not? Both are roughly the same length, both are used to hit things, and both do most of their business up to five inches from the end. Certainly, to swing a sword like a golf club and connect would be devastating to your target. So why don't we use it that way?

The answer is biomechanics and perception. Biomechanically, it's not efficient: The target of a golf club is at ground level, where the target of a sword is at eye level. Because the difference in targets is so drastic, we instinctively perceive that to swing a sword like a golf club is wrong.

Now let's use this thought process to delve a little deeper: Think about the target of your animations, and where your character's enemies are located. Is swinging the weapon like a baseball bat the solution? Consider the game you might be working on: In an environment where your character is trying to kill people, the target of your swing is more likely to be the pitcher (in front of you), than the ball (next to you at the moment you swing). Is it still correct, then, to stand like a batter, and swing as though you're trying to hit the ball? Probably not.

So now we can take a step back and ask ourselves: "What is the best practice?" Nothing beats calling in an expert, of course, but even if you don't have the time or resources for that, putting in a little effort in developing your fundamental understanding of human biomechanics with respect to weapons can help clean up your animations in a major way.

# Realism Plays Well with Your IK Rig

As I stated earlier, the basics of Renaissance fencing and martial arts (the discipline we call "MARE," or Martial Arts of Renaissance Europe) are pretty straightforward, and once you understand them, the rest becomes a matter of relentless conditioning and practice.

For the purpose of the animator, however, the basics can be a great starting point that will give your warriors a unique visual silhouette, without requiring the animator herself to become a scion of martial prowess.

Once you're comfortable with holding the sword, the best place to start thinking about animating a swordsman is to understand the basic stances: what we call "tip progressions" or "guards."

For the purpose of our animation, it's best to think of these stances as our idle positions.

As you begin to employ these idles, you'll notice that no matter what sequence of cuts your characters perform or what direction they face, they will always end their movement in one of these poses. They work fluidly and efficiently with each other, and they emphasize control and tactical positioning.

The four primary guards, as illustrated by John in Figure 2, are (from top to bottom) Phlug, Alber, Vom Tach, and Ochs.

![](../../assets/edaceed8a80cb5aa.img)


Figure 2: The four primary guards: Phlug, Alber, Vom Tach, and Ochs.

What you'll also notice is that they play very well with your inverse kinematics rig. Like the algorithms that drive your rig, the weapon leads the motions, just like your IK target leads your animation. You'll also notice that the torso and arms seem to move almost independently of the legs. What's more, as you step through the footwork, you'll find that you can pivot your character around on a single foot, and stepping forward or backward is a simple matter of just mirroring your animation across your center plane.

Of course, these idles require the context of the basic cuts (called "Master Cuts") to be fully appreciated. Rather than go through the entire catalogue of idles, transitions, and cuts, I'd like to illustrate my point with a particular sequence.

In Figure 3, I start at the top in a fifth guard, called Nebenhut. Note how my leading leg is bent, and the trailing leg is straight. Also note how my feet are at a 45-degree angle to each other. Let's pretend that a new enemy has presented itself to my rear, and I want to turn 180 degrees to meet the new threat. Rather than shuffle around and swing my blade awkwardly in an attempt to maintain Nebenhut, I opt instead to hold the sword steady.

![](../../assets/917ca8e31ef1d4c6.img)


Figure 3: Example of turning 180 degrees between two guard positions.

As I begin to turn, my head and torso rotate first, followed by my trailing foot, which ends at 120 degrees (as relates to my left foot). On the third step to this sequence, I shift my weight onto my right leg, which is now my leading leg, and I deliberately bring my trailing foot to its new position. Notice that now our Nebenhut has transformed into Alber. To end the sequence, I lift my weapon out of Alber, and into Phlug.

Despite turning my entire body to face a new direction, my right wrist (the presumed target of our IK), never changed position. Also, until I lifted the weapon at the end, the sword remained almost entirely motionless. Note that for my entire turn, the ball of one foot remained planted in a single position (please ignore the general position shift at step three; a wall was in the way, so I had to move back).

This theme of always returning to our basic guards continues to manifest even as we begin striking. In Figure 4, we see John start in a Vom Tag, and then step forward into a strike. What follows is a rapid rotation of the weapon to strike again from the opposite angle. He repeats this rapid back-and-forth several times, striking at a different angle on each pass.

![](../../assets/337982b9d3ccfb13.img)


Figure 4: A sequence of strikes starting in Vom Tag.

Despite the change in vector for every strike, John always returns to Vom Tag before striking again. He doesn't do this because he's necessarily trained himself to perform this specific transition for its own sake; he does it because it's the most biomechanically efficient way to pass from one strike to the next. This phenomenon is particularly useful for animators, because at any point between strikes we can end our sequence without popping into an idle pose, potentially jarring players out of their immersion.

# Start Real, Then Exaggerate

Exaggeration is, fundamentally, one of our jobs as animators; we make our characters perform like an actor would perform on stage or on camera. Reality is always exaggerated or altered to fit the needs of a production. But whether you're talking about Jade Empire or Call of Duty, you should always start with a solid foundation in reality. For games in medieval or fantasy settings that include sword combat, taking inspiration from the right sources (like MARE) can set your combat animation apart and make the task of animating cleaner and easier.

# John Clements: Give Reality a Chance

Imagine if game designers had never seen or heard of serious Asian martial arts, and never made any game with such influences. Then, one day, a budo master or kung fu expert steps up and says, "Hey, I think you could make some really interesting things using our unique craft as a resource. We move in really neat ways that you haven't explored." I like to think that game developers would quickly see that there was something significant and sophisticated there worth examining. They probably wouldn't respond with conceited indifference -- which I've seen firsthand when I bring up the historical medieval combatives I study, teach, and practice.

# People in The Know

I've been studying Medieval and Renaissance close combat for over three decades. I make my living writing and researching on the subject and operate the world's only private facility dedicated exclusively to the craft. I am no stunt fighter, costumed performer, nor showman entertainer, but an accomplished martial artist who teaches an authentic combative discipline following genuine sources. Study of these historical fighting methods is my life's passion and my career.

Now, I don't think that everyone who makes a game in a medieval or fantasy setting needs to make a 100 percent accurate hand-to-hand combat simulator any more than I want to see the next Call of Duty game stop working forever after your character dies for the first time.

I do think, however, that the hardworking developers who make these games would have an easier time (and make even better games) if they drew from more realistic sources of inspiration when it comes to medieval combat.

The funny thing is, we already know this to be true. Just take a look at the original Prince of Persia, where creator Jordan Mechner filmed his brother actually walking, jumping, and going through some rudimentary fencing motions as the basis for its rotoscoped animations and action. That game was an influential breakthrough, but later titles would essentially copy and embellish upon those sequences, and the titles after that would copy the copies -- and so on until the insightful grounding in realism of the original source was lost.

# Drawing From the Source

This process is common sense; if you are doing a modern special ops game, you consult with authorities of that profession. If you're doing a boxing game, you consult with a professional boxer. If you're doing an aircraft fighter game, you consult with a fighter pilot. If you're making a game about samurai, you certainly want to get the form and movements right by working with budo experts. When you copy the copies of copies, you get ever further from your original realistic base -- which means you're adopting the same embellishments and limitations that each successive generation of copies did without looking back at the real source material to see what your real design and animation options could be.

For example, a designer might see a fighting move in a movie and think, "This looks cool. I wonder how I can devise a mechanic for players to do that?" But what of the possibility that what they witnessed is mere nonsense; an inferior action the game maker is just not qualified to evaluate? What if there are better alternatives? What if the "real thing" -- a general principle of self-defense, or some element of employing a particular weapon, or a specific combination of techniques -- is actually cooler? If the designer doesn't get the move from the right source, with a proper explanation of how it works and why, they will be missing out on how it fits in with the "game" of hand-to-hand combat, and won't be able to use that understanding as inspiration for how it could fit in with the game they're designing.

![](../../assets/bef8e47cc752e261.img)


Yet this is more or less the general process I have seen for devising archaic close combat in games, and when I point this out, developers often feel insulted. Why? Aside from perhaps offending the creative sensibilities of designers, it's because I am suggesting that (gasp!) people who design games are not themselves also experts in the authentic sources of historical close combat. They have not trained long-term with accurate weapons in those methods, and they do not have extensive hands-on experience in striking realistic target materials with sharp weapons using genuine techniques, nor do they usually fit the profile of athletes conditioned to rigorous training in armed fighting skills. It seems like kind of a strange thing to be offended by. After all, most people haven't!

My job is to understand how such weapons handle, how they're maneuvered and manipulated, how they engage one another, what type of techniques and motions the human body is really capable of with said weapons, how physics affects melee combat, and how people respond (physiologically and psychologically) to violent actions. The specifics often include examples of how little-known gripping actions, armor, postures, and different footwork are all interconnected. These elements are ones I can guarantee you have never seen in any movie, TV show, game, renaissance faire performance, or choreographed routine. It's this knowledge and these details which I hope to see developers take inspiration from while building their own games -- instead of copies of copies.

# Correcting Core Assumptions

When you develop a game combat system or a series of combat animations, you do so based upon a certain set of core assumptions: assumptions about how weapons and swords handle, about how armor functions, about what wounds could be causes, about how people respond emotionally to personal violence, how bodies and limbs react to injury, and about how real fighters learned martial skills.

Naturally, if you're building a combat simulator off of a relatively shallow (or even erroneous) set of core assumptions, your game won't feel right. Even if your game intends to take a more stylized approach to its combat mechanics and animations, however, it's worth investing the time to understand how the reality of combat translates into your game's core assumptions, so you at least understand what you're stylizing, and why. The martial knowledge and historical combat skills I've redeveloped permit developers to paint with a far richer palette of colors, if only the effort is made to pay some attention.

Without this realistic base, a video game animator ends up replicating the bad form capture of exaggerated stage combat, accepting impressions from pretend bouts with poor weapon simulators, or copying the ritualized movements of some traditional fighting style. The consumers in turn get simplistic strikes and rigid blocks delivered from static, unwieldy postures combined with incessant spinning, whirling, leaping, and assorted useless (and even suicidal) actions that defy both common sense and basic human biomechanics. Meanwhile, a wealth of more dynamic and sophisticated movements, wardings, and alternative counterstriking actions from genuine fighting methods remain untapped for gamers.

![](../../assets/d0456510f0c52c25.img)


I regularly see weapons, particularly swords, wielded by characters in video games in which the familiar figure animations and fighting motions are primitive and crude. For example, there are 16 possible lines of striking for the typical double-edged European longsword. Yet, players are repeatedly offered only the same standard three or four strokes taken right out of Japanese swordplay or borrowed from modern saber fencing and stage combat. It's little more than how children manipulate Nerf swords. All the diverse dynamic motions and distinct manners of adeptly manipulating a real weapon -- with its wards, cuts, thrusts, slices, closures, and displacements -- are entirely absent.

Certainly, not every game with a sword needs to be a sword-combat simulator, but I am confident the software does not know how to allow players do them because developers themselves aren't aware that these things are interesting -- or even possible -- in the first place. With a little effort and attention, however, I think developers could use these realistic historical combat skills to paint with a richer palette of colors.

# Devs and Demonstrations: A Deadly Combination

Whenever I demonstrate for game developers, the initial reaction is often simply "Whoa!" They've never seen someone move the way I do or wield particular weapons as adeptly, and certainly not in person instead of on YouTube. And when I demonstrate that these movements are universal and apply to all weapons, whether it's a dagger or spear or a sword and shield, something seems to click. Developers tell me, "Wow, we won't have to use the same old things again, I didn't know that you could hold a weapon that way, I didn't know that you could strike with it that way, I didn't know it was possible for someone to step and pose in such a way, moving from one to another in that way."

![](../../assets/fbd181f7de99f93f.img)


Realism doesn't close doors. It opens them. Designers can see that with one kind of weapon, one certain type of move can come after another or that one move has a counter, or a certain position can be interfered with, stifled, or interrupted by another. Combat doesn't have to be the familiar "parry-riposte, parry-riposte, whackety-whack-whack, swirl-swirl" pattern.

Realism is not a dirty word for combat in fantasy games; it's a center point from where everything can and should begin. Realism doesn't lock you in or freeze you in place as a game designer. It's an empowering tool that lets you say, "Wow, I've got a really strong foundation to build on now." Only once your feet are grounded in the right place can your imagination really take off.