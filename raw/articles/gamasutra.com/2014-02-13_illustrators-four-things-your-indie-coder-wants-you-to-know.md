---
title: 'Illustrators: Four Things Your Indie Coder Wants You To Know About Game Art'
url: https://www.gamedeveloper.com/art/illustrators-four-things-your-indie-coder-wants-you-to-know-about-game-art
author: Rodain Joubert
published: '2014-02-13'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)


![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)

**Featured Blog | **This community-written post highlights the best of what the game industry has to offer. Read more like it on the __Game Developer Blogs.__

# Illustrators: Four Things Your Indie Coder Wants You To Know About Game Art

A rough startup guide for illustrators and "classically trained" artists who want to move towards the exciting and intense field of in-game assets. Written by some indie dude who has worked with several people going through exactly this transition.

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

The following was originally posted on our [QCF Design blog](http://www.qcfdesign.com/?p=835).

Over the years, I’ve learned a bit about the diversity of the drawy-artstuffs field. I speak from the outside, of course – the closest I’ve come to being an artist myself is a one year communication design course (read: layout and colour theory) and the occasional desperate move with game prototypes where I simply couldn’t find anybody to draw things for me.

However, while I cannot tell anybody how to “do” art, I am sympathetic to some of the difficulties that visual creatives have when they’re forced to operate in the weird and wondrous framework of a programmer’s code base. None more so than classically-trained artists, who usually operate in environments which have loose constraints (or none at all) in areas that happen to be of absolutely vital importance to the average programmer.

Sometimes a situation emerges where talented artists in the wrong category hop onto an indie project: the devs are hoping for a particular style, perhaps, or the project exists in a territory where game development is still getting its legs and the required specialists are rare. Or maybe some friends just wanna work together on something regardless of the hurdles.

This can be pretty cool in the long run – particularly if said illustrator is excited and enthused about learning a new form – but there’s a few growing pains that need to be worked past. In my experience, practically all classic artists will need to learn the following:

(1) You’re working under the most demanding constraints possible

If you’re a freelance illustrator or concept artist, you’re used to getting briefs with the necessary provisions: it needs certain dimensions, subject matter, format and all the usual trimmings. But if we assume a non-painful client, external constraints won’t matter much when you start putting pen to paper. You have thousands of pixels to work with in either direction and smaller details only matter when it comes down to your own style and standards (again, oversimplifying and assuming that your client isn’t an asshole).

When you start working with coders, your open playfield pretty much vanishes. Sure, you can comfortably send the first draft of your work in whatever style you prefer – a good team will provide valuable discussion points and feedback for that – but sooner or later, you’re going to lose your ability to play with broad strokes. You’ll be told that your work needs to fit strictly into however many pixels (and exactly that many pixels, mind). You won’t be allowed to use particular colours. You’ll have to draw sprites that will stand out against every conceivable background in multiple resolutions and lighting situations. Things need to mirror in sneaky ways. Your work needs to hue shift gracefully. And we won’t event go into animation!

In many instances, you’ll be forced to change your approach from “whichever style feels best” to “whichever style actually works”. And in any realistic setting, that’ll be downgraded to “start hoping that you can find a style that works”. Because while you may be an architect, the engineers you’re working with have a whole lot of immutable constraints that they’re trying to tell you about, based on the strength and availability of materials and components. And given the special hazards of a typical programming environment, such construction projects can often feel like building a house of cards.

Pushing back against your engineers and insisting on your vision usually won’t yield much – in some cases, a talented and accommodating coder can move virtual mountains to give you more wiggle room with a particular variable or especially important style hook, but that’s about the best you can hope for. And they’re not trying to be dicks. They’re just as bound to the rules as you are, if not moreso. You can always bend your style to suit their constraints. But the other way around? Usually impossible. Flatly, literally impossible.

So, this first point is the longest, but it’s also the most important: change your philosophy and learn to make project constraints your bread and butter. Breathe in specs and exhale precision work. Continue to think outside the box, but understand that your final product needs to exist firmly inside it, no matter how tiny that becomes. You won’t be making your best work – you’ll be making your best work for a particular situation.

If you can just get into this mindset, the rest will come far more easily.

(2) Your game dev clients tend to know more than the others

I’ve never met a professional indie coder who didn’t have at least a passing literacy in tools like Photoshop and GIMP. Reality often bumps into us and demands that we take up cross-class skills, and you’ll find that more experienced coders actually have a track record of meeting their artists halfway on concepts that are difficult to understand or implement precisely (everyone at QCF has spent countless hours cleaning up edge pixels and aligning tilesets at various points).

We also come pre-packaged with a certain technical understanding that other clients usually lack – we know what antialiasing is and how it works. We understand image channels, RGB, HSV, WTF and all the other delightful acronyms out there. And then there’s the ultimate fact that every bit of magic which goes into art software has to be coded and mathematically signed off by programmers, so there’s a lot of relatable language and understanding in there for us.

This is idealised, of course. Some coders are as thick as two bricks being rubbed together when it comes to graphics lore, and there’s a lot of savvy clients that exist outside our bubble, but unlike a lot of other people who usually need art from you, our job regularly forces us to dip into your world and understand things. Not enough that we can go without artists entirely, but enough to make your life easier.

Use this. Speak to your team and find out exactly how much they know, then take advantage. If it’s easier for you to send a PSD with unbaked layers, fixed alpha masks, grouped shapes, unrasterised text and a box of rabid gerbils, perhaps you can do just that! We’re not going to be stumped and panic the moment you give us something that isn’t a web-ready PNG. Better still, we may even be able to edit it and send back a revision showing you what we want more clearly!

(3) You’ll have to build a more technical understanding of your own tools

I have, on rare occasions, had to point artists towards bits and pieces of Photoshop business that they knew nothing about. More than once, I’ve worked with people (directly and indirectly, formally and informally) who didn’t understand how image layers worked or why they were important.

It makes a lot of sense, especially when modern art tablets allow you to treat digital projects almost exactly like your physical medium of choice. Tools that don’t assert their importance won’t be learned because there’s no obvious need for them and no damage done by ignoring them. This can be a shock for people the first time they transition to a more demanding environment.

Do you understand feathering, anti-aliasing and tolerance when selecting or filling a region? Perhaps so, perhaps not – but the important thing to realise is that a lot of people don’t have to understand, and thus never learn. This is by no means a condemnation – default values tend to be good fits for a lot of situations and it can feel almost absurd the first time a coder has a frothy fit because you gave hir a 50% alpha-edged sprite baked on a black background. Especially – especially – when just about any other client wouldn’t actually give a shit or even notice that the situation exists in the first place.

But as a good yardstick: if any terminology mentioned in this article is unfamiliar to you, look it up and learn how to control that variable, because a coder at some point will probably make a demand related to it. If you demonstrate confidence with these things, you’ll be thanked with genuine emotion and possible tear-shedding because you’ve saved some poor engineer several hours (even days) of work trying to reprocess your graphics for you.

(4) You’ll need diversity (and to look at what others have done)

I left this semi-obvious point until last because I reckon that the other ideas needed more screentime, but it’s always worth restating somewhere: learn from your digitally inclined peers! Some artists have been dealing with curmudgeons and coders for most of their careers and have super-helpful advice about all the small things that each specific task requires.

Game art is such a diverse field that even those within it tend towards radically different specialisations. Making a tileset requires its own considerations. Building a 32x32 sprite animation is a particular kind of art, even when compared to doing the same at double the resolution. And 3D stuff? Well, even if you never lay a hand on a modelling program, being asked for a 256x256 wall texture requires a quick look at some important points.

The simplest game projects can draw upon multiple art styles and types of challenges, and unless you have the luxury of working with a team where individual artists can focus on just one aspect of the game, you’re going to find yourself performing a lot of radically different – and equally demanding – tasks. Even Desktop Dungeons required our artists to switch approaches between tiny pixel sprites, tilesets, detailed portraits, double-sized elements, and screenwide backgrounds. All of these had their own art considerations while still needing to click in with each other for the same “overall feel”. And that shit is hard. Or so I’ve observed.

But hey, that’s the glorious part of the job: game art is diverse and interesting and don’t let anybody tell you otherwise! The challenge and variety, at least on an indie level, is a fantastic experience for even the most poorly-equipped artist and the skills you gain will be invaluable.

Ultimately, you can view it as an exchange of one priority for another: you’ll lose a bit of freedom, but in return your work will come to life in a way that lets people experience it more deeply over greater sessions of exposure. In contrast, the equivalent effort on a piece of promo material, a once-off splash image or even some concept art will earn glances from the majority and focused attention from only a precious few – if you’re lucky. Or as an actual artist once put it to me: “You’ll never see a dedicated Let’s Play video of someone’s box art.”

So if this life appeals to you, dear illustrator, and you want to try something new … come join us! It's new, it's interesting and you'll be doing your bit to save the world from the scourge of Programmer Art.