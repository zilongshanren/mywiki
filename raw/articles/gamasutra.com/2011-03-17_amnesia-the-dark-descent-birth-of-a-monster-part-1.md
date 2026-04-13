---
title: 'Amnesia: The Dark Descent: Birth of a Monster - Part 1.'
url: https://www.gamedeveloper.com/art/amnesia-the-dark-descent-birth-of-a-monster-part-1-
author: Thomas Grip
published: '2011-03-17'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)


![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)

**Featured Blog | **This community-written post highlights the best of what the game industry has to offer. Read more like it on the __Game Developer Blogs.__

# Amnesia: The Dark Descent: Birth of a Monster - Part 1

This is the first part of two that outlines how one of the enemy creatures for Amnesia: The Dark Descent was created.

![](../../assets/52799623e9e4a077.jpg)

(The following was supposed to be an article in a Russian magazine, but was never published. So because of that, I decided to post it on the blog instead. It was written in June 2010 by myself, Jonas Steinick Berlin and Olof Strand. Jonas and Olof were working as contractors for [Frictional Games](http://www.frictionalgames.com/) at the time. )![](../../assets/7d421c8b06053ffc.jpg)


## Creating Unspeakable Guidelines


by Thomas Grip ([Frictional Games](http://www.frictionalgames.com/))

The following article outlines the process of creating a creature model from scratch for our first person horror game [Amnesia: The Dark Descent](http://amnesiagame.com/). It will go through the basic thinking that went into the design of the enemy, how the concept images where made, how the mesh was built and finally how it was put into the game. For this work we used two extremely talented external artists and they have themselves outlined how their horrific creations came about below and it a future part. Before moving on to their work though, I will detail the thinking that went into the basic design of the creature.

When creating a horror game, making sure that the antagonistic creatures are properly designed is an extremely important issue. One wants to make sure the player faces something that feels frightening and works with the game's atmosphere and story. Another important aspect is to make sure that the enemy fits with gameplay. Certain movements might be required and it needs to fit, size-wise, into certain environments and situations. Finally you need to make sure that it is within the constraints of the available resources, something that is really important for small company such as ours. Having these three guidelines in mind I will now walk through the process of coming up with the core requirements for the enemy codenamed “Servant Grunt”.

My favorite way to go about when creating a creature is to take something normal and then add a disturbing twist to it. I also wanted some kind of character that the player could easily project agency to and believe it has motivations, imagining it more alive than it might actually be. Because of this I decided that we use some kind of human or at least humanoid entity, which is a shape that is easily recognizable (no other animal walks like a human) and which we all assume have feelings, desires and motives.

The problem with having a creature which gets the characteristics of a human projected on to it, is that the player will also assume it is intelligent. Because game AI is notorious for doing stupid things, this could easily break immersion. Having enemies do simple tasks like opening doors, avoiding obstacles and investigating strange noises in a believable human-like way is very hard to do. Hence, we had to have something in the design that hinted of stupidity, making it part of the immersion were the enemy to do something silly. Usually this means making something zombie-like, but I really did not want have something that cliché. This mean that I wanted the creature should look and feel stupid, yet still be as far away from a zombie as possible.

Avoiding clichés is usually something that ones does to keep things fresh, but in horror games a lot more is at stake. It is vital that the player does not feel familiar with the dangers faced as it drastically decreases fear and tension. It is when we are unsure about something and not able to predict or makes sense that true terror really emerges. For example, when building one of the game's maps, there was a vast difference in perceived horror between using an old, familiar enemy model from [Penumbra ](http://www.penumbragame.com/)(our previous game) and the new one discussed in this article.

Gameplay-wise the main constraint was that it had to walk in some human-like fashion and not crawl or move on all fours. This because we wanted to have a base collision that could easily fit into a cylinder, making it easier to code. For the first Penumbra game, we had dogs as the main enemy which, because they where four-legged, caused tons of issues. Something we wanted to avoid that this time around. Making sure implementation of the enemy is simple ties into saving resources. It was crucial that we did not want to have too many unknown factors when making the enemies. By making sure that most of the game's elements where familiar to us, we could much easier assure that we kept to the timetable and could spend time on polishing other parts of the game instead of trying to find AI bugs.

It was actually not until all of the above was determined that I started to figure out the story behind the creatures. This is not always the way we do it in our games, but this time it fit very well. Our basic story designs only referred to the enemies as “the servants” and did not talk much about their appearance or where they came from, so I had a lot of freedom to make a fitting background story to the guidelines. The finalized idea was that these “servants” were actually beings from beyond that had been summoned into bodies of humans. Once inside humans, they did their best to deform the host into a body that they are used to control, shattering bones, tearing flesh and producing cancer-like growths. This in turned resulted in a scene where the player witness how some humans under great pain are taken over, showing how designing graphics can shape the story, as well as the reverse.

With these basic guidelines completed, I contacted Jonas to start on the concept art.

## Conceptualizing the Horror

by Jonas Steinick Berlin (pudjab [at] hotmail [dot] com)

Thomas gave me almost full creative freedom. The basic guidelines were that it had to be a humanoid and nothing like standard zombies, "The Infected" in Penumbra: Black Plague or the creatures in [Dead Space](http://en.wikipedia.org/wiki/Dead_Space_%28video_game%29). It should also fit the the story of demon-like creatures taking over human bodies and be super creepy. Apart from that, I was free to do pretty much what I wanted.

This was my first character design for a commercial game, so I was a little bit shaky. The great freedom was both exciting and quite overwhelming. So many choices! I first researched and got inspiration from unusual anatomy, photos 18- and 19th century clothing (the time in which the game takes place), surrealistic paintings and various disturbing stuff.

I then continued brainstorming and did a lot of small quick sketches of character silhouettes and different faces. I really wanted to avoid stereotypes and do something unique and memorable. Every single doodle got assembled on a collage and I then showed it for Thomas. He said which parts he liked and from that I went on and created something more detailed. At this time I had a design in my head that I really felt would be perfect. I drew it down with details, colors and lots of love. The result was something of a hunchback with interesting clothing fitting the era and a really grim face. This is perfect I said to myself! Excited I showed it for Thomas. However, I quickly got knocked down to earth again when he said that it looked too funky and resembled [“Grodan Boll”](http://www.youtube.com/watch?v=hr5u8O62eCs)(which is a character from a Swedish children's book taking the form of frog). I got instructed that I should avoid the cartoony style and make something more realistic, something that you almost could find in real life. Thomas also thought that it should have a lot less clothes.

![](../../assets/5e07f055a08ca339.jpg)


The first batch of sketches. Contains the infamous “Grodan Boll” (“Frog Ball”) on the right. (Click to enlarge.)

After this setback I started putting a lot of attention on the head of the character. I think this is the part of the human body that you can make the most disturbing because of the emotions it can show. I instantly chose to give him a crushed jaw with parts of skin hanging down and eyes with dilated pupils which pointed in different directions. Thomas approved of this and I moved my focus to the rest of the body. Important here was to get the feeling of a demon possessing a body that it was unfamiliar to. The creature should try to deform the body into a, according to its own twisted standards, more familiar form, breaking bones and bending joins while doing so. It should also have accidental injuries and be held together with bandages and ropes.![](../../assets/edccdd1bd9ae2ad7.jpg)


The create is starting to shape up and the design of the head has been approved. It is not yet decided what to do with the lower jaw though (an issue discussed until the very end). (Click to enlarge!)

Because of the lack of clothes we had a discussion about showing genitals or not, but soon scrapped that idea after we realized that it would be best not to tease the rating systems too much (this turned out to be a non-issue as other part of the game show /Thomas).

![](../../assets/c38111882d956bc1.jpg)



One thing that was hard to decide was the final look of the left hand. It had to be deformed in some way, but yet be usable and able to be used as a weapon. I did at least 10 different arm designs before coming up with something that we could use. For example I did an arm in the shape of snowballs with spider fingers and one arm twisted in a spiral, with its bones pointing out. The final hand-design was more of a claw with bony fingers that we thought would be perfect for both scaring the player and give a good scratch on the back.![](../../assets/267b02c70b4f01e8.jpg)


Before settling on a final design, many different version where tried. The left arm was the most troublesome part and changed a lot. (Click to enlarge.)


When I did the detailed final concept I started by drawing it up traditionally with a pencil. This may not be the most effective way to work (because it makes it harder to do big changes and also caused unwanted coffee stains), but I feel more in control this way and find it easier to do the smaller details. After that I scanned it and quickly colored it in Photoshop using multiply layers. I first tried a bluish skin tone, but it made it feel too much like an alien, so I changed it to a more desaturated one, warmer colors with elements of purple, blue and yellow to create a pale corpse-like look. At this point it didn’t feel too professional and had to go over the concept with Photoshop to add the final touches, such as highlights, noise removal and sharpening. The Photoshop-file ended up having forty plus layers, most of them containing small and unnecessary changes. Nothing I recommend, because of the insane file size, but this time it did the trick and I managed to convince Thomas the concept was completed.

The art was now done and could now be used by the modeler to create the actual 3d asset.

![](../../assets/f66c7fdc5ee88af9.jpg)


This was the final sketch of the enemy. After this was done I started painting it digitally. (Click to enlarge.)

![](../../assets/54063dcf99e204c8.jpg)


Final concept for the enemy. Note how the lower jaw has been removed, something that was made after the entire character was fully colored.


The second part can be found [here](https://www.gamedeveloper.com/art/amnesia-the-dark-descent-birth-of-a-monster-part-2-).

This article was originally published March 17, 2011. It has been updated in 2024 for formatting.