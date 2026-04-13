---
title: Making 2D art for an indie game
url: https://www.gamedeveloper.com/art/making-2d-art-for-an-indie-game
author: Harri Jokinen
published: '2015-02-02'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)


![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)

**Featured Blog | **This community-written post highlights the best of what the game industry has to offer. Read more like it on the __Game Developer Blogs.__

# Making 2D art for an indie game

This blog post deals with prerendered 3d sprites, hand-painted 2d sprites and hand-made animation. Tools of the trade are Photoshop, 3ds Max and photobashing. The case game is our demo of retro 2D RPG 'Neurotron'.

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

Getting Started

Creating game art, as we all know, is a very, very, diverse field of art. My goal is to share my experiences with a certain game project which I've created. This is also my first blog post to Gamasutra, so forgive my non-consistent narrative and stumbling with words. This blog post is by no means a codex of ultimate wisdom, just a collection of my own personal thoughts.

Okay, so we have this sample case : A retro, 2D, role-playing game, which is nonetheless based on an earlier board game concept. There's already a few quite defining key elements for creating your art. Laying out these simple keywords in the beginning is very important. They can, of course, vary during the gamemaking process (hopefully not much though).

2D / 3D is the biggest thing you lock in the beginning. If you switch from two-dimensional to three-dimensional in the middle of the development, you're going to face a whole lot of trouble. And you're going to end up throwing many of the game's graphical assets away. Same goes for the other way around.

![](http://rayhouseproductions.com/gamedev/neurotron/Ad.jpg?width=384&auto=webp&quality=80&disable=upscale)


RPG or role-playing game also tells a lot of the art. It also gives us a lot of questions to answer: What kind of a world are we portraying? How many player characters are there going to be in the party / squad? Do they all have to be visible and focused all the time? Is this sci-fi, postapocalyptic or fantasy rpg? As an artist and as a creative indie developer you're going to have to answer these questions.

With Neurotron we wanted to go with this classic RPG / real-time strategy perspective, or the 'bird's eye perspective' opposed to the now-standard isometric view. The reason most 2D rpg developers go with the isometric view is because it simulates the three-dimensional perspective more accurately. On the other hand, the distances can vary when doing the game from an isometric view, and the graphical layer order can be quite tricky to handle in code. I was very intrigued by the idea of doing Ultima 1-5 style block graphics with a more modern look and in a sci-fi world.

![](http://rayhouseproductions.com/gamedev/neurotron/Charcreation.jpg?width=562&auto=webp&quality=80&disable=upscale)


The retro sets its own challenges and possibilities. When we say retro, we know the game isn't trying to be triple-A or state-of-the-art graphical candy. But what do we mean? Does it mean an actual 8-bit game or a game straight from the year 1992? Usually, it's not the case. The idea is to invoke the feeling of nostalgia, but not to do a game REALLY from the past. In Neurotron I struggled with this thing a lot. I wanted to use the tools I have at my disposal, but not to do the game art with a straight 2014 mentality.

The game mechanics also are affected by this genre, of course. You can draw a lot of inspiration from older games, comic books and art, not that you couldn't with next-gen graphics, but in this case the results are going to be even more apparent. Homage, pastiche, nods to the past, these are all reasonable and accepted when you're making a retro game. This type of genre is now very popular especially among the indie and mobile game developers.

Okay, so this isn't 2,5D, and this isn't 3D and this isn't an arcadey shooter game, so we can put a lot of detail into the game art. And this brings us to our next point:

How Much Detail?

If you're creating a fast-paced SHMUP or arcade shooter, there's no reason for you to put your energy into incredibly detailed game art. In the case of fast-scrolling games your art has quite little screen time, except for the player character. The background tiles, environments, power-ups and enemies don't have to be so delicately created, if they can impress the player with a quick glance. In those cases it's more about the shapes and graphics as a whole.

In adventure games and role-playing games, when you're exploring the game world and getting immersed in it, you also have more time to admire the art. In this case it would be a good thing for the art to be coherent and made with a consistent art style.

The one thing which I feel we kinda failed with Neurotron was the fact that we mixed a bit too many different styles. It could have benefitted from a one consistant guideline. It mixed painted, prerendered and photobashed images, which absolutely shows. In a projects where there's more than one guy making the art, it's going to be increasingly difficult to keep the coherent style. Just keep that in mind! Communication is the key in all game development of course, but it's especially important with the stuff that's going to be on the screen.

![](http://rayhouseproductions.com/gamedev/neurotron/Death.jpg?width=555&auto=webp&quality=80&disable=upscale)


Prerendered vs. hand-painted vs. "pixel art"

The look for the game is a huge deal. In the beginning of the Neurotron demo project I thought about doing the character art with digitizing hand-made latex rubber puppets. Yes, you read that right.

So, okay, that may have not been as crazy as it sounds. It's been done way back in the nineties; Doom had digitized puppets and Blood also used those, not to mention the digitized actors of Mortal Kombat and Rise of the Triad. But, considering that this is not a 2,5D shooter which doesn't use "sidescroller" style projection, it was not viable. The bird's eye view + keeping the character art consistent would have been pure madness! Not to mention keeping the lighting coherent and just handling the overall difference between real physical world vs. the "perfect" digital world.

![](http://rayhouseproductions.com/gamedev/neurotron/NomadSoul1B.jpg?width=560&auto=webp&quality=80&disable=upscale)


So, I ultimately chose to do the character art prerendered in 3Ds Max. I made hires models which wouldn't really be considered for a realtime 3D game. It gave me freedom for the characters, and removed much of the technical limitations, and in the end the character art ended up being 64x128 px sized.

![](http://rayhouseproductions.com/gamedev/neurotron/Botti.jpg?width=560&auto=webp&quality=80&disable=upscale)


The backgrounds and UI we're a different story however. I began with the first mission backgrounds, from a clean slate. I made those in Photoshop, and used some photobashing. Later on, when I combined the characters to the backgrounds it seemed that the styles didn't quite mix. When I kept doing more photobashing and simulated the "3D look" for the BGs and scenery objects also, it started to fall into place.

Okay, then the route which I didn't take was the pixel art. Why? The resolution of the game was 1280x720, so reasons were obvious. Making a coherent look with 64x128 sized characters and doing everything by hand would have taken literally forever. This is the thing which I did want to compromise when choosing between "retro" and a "real game from 1992".

![](http://rayhouseproductions.com/gamedev/neurotron/3Dbed.jpg?width=431&auto=webp&quality=80&disable=upscale)


First I started doing the UI icons of the items by shooting real-world objects with my camera and touching it up in Photoshop. In the end, I just prerendered most of those objects too to keep the consistant look. The pieces of scenery, like the toxic barrels, storage cubes and hovership, I also did with prerendered 3D.

Wrapping up

The demo was completed by the end of July 2014, and it participated in the Assembly Computer Festival's gamedev competition. It didn't do well there, mainly because of the really hard and little bit too retro UI. The audiovisual side of it was praised though, and that was our goal actually. The incoherent art style was mentioned though, which put some players off. Neurotron was made mainly for a portfolio and showcase purposes anyways, more as a test inside the team.

After that we've moved on to our first actual commercial PC game, Kalaban. Many of the lessons which I learned in making the demo I'm using right now. The current project of ours is a 2D survival horror from a bird's eye view but not with a blocky tile graphics style and a more coherent overall look.

If you have more questions about this project, or have an interesting opinions about this text, hit me with an email: [[email protected]](https://www.gamedeveloper.com/cdn-cgi/l/email-protection#84ece5f6f6edaaeeebefedeae1eac4f6e5fdecebf1f7e1f4f6ebe0f1e7f0edebeaf7aae7ebe9)

![](http://rayhouseproductions.com/gamedev/neurotron/LoadingScreen.jpg?width=563&auto=webp&quality=80&disable=upscale)