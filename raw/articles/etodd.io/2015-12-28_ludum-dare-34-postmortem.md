---
title: Ludum Dare 34 Postmortem
url: https://etodd.io/2015/12/28/ludum-dare-34-postmortem/
published: '2015-12-28'
source_blog: Evan Todd
source_site: https://etodd.io/
category: game programming
fetched: '2026-04-13'
---

# Ludum Dare 34 Postmortem

### Friday 21:15

Fifteen minutes after the theme announcement, my friend Ben Homan walks through
my front door. Not really *my* front door, I'm just a subletter.
But this is a first. Normally he ignores our instructions to walk in without
knocking. The first time, he texted me from the driveway.

### 21:30

Jesse Kooner walks in, also unannounced, bearing frozen pizza. Before he can even kick his shoes off, I loudly explain the theme: a never-before-seen tie between "growing" and "two-button controls".

### 21:45

Jesse has no laptop. I dig out an old one from my closet. I plug it in and start working on a few Windows updates. 72 to be exact.

Meanwhile, we decide which technology to use. Jesse's less code-focused skillset leads him to prefer Unity, while Ben wants to use the weekend as an opportunity to become more familiar with Node.js. We decide on Node.js. Jesse will provide creative input and artwork.

### 22:30

My roommates, a brother and sister, arrive home from an apparently underwhelming Christmas light show. The concept of a game jam is foreign to them, but they're good sports. We spend a half hour playing QWOP with them.

### 23:00

Our design parameters:

- Multiplayer. Otherwise, what's the point of Node.js?
- Probably 2D due to the limited timeframe. Although Jesse is more comfortable working in 3D.

Jesse originally suggested doing this competition a few weeks ago, when he wanted to create a mash-up of "Cookie Clicker" and a tower defense game. He resurrects the idea now, only halfway joking.

Ben likes the idea of a multiplayer vine growing game. I'm partial to a text-based social game about growing a social media brand. No one commits to anything yet.

Ben is not a big gamer, so I pull up a few famous HTML5 games on his laptop.
[Cursors.io](http://cursors.io/).
[Agar.io](http://agar.io/).
[2048](https://gabrielecirulli.github.io/2048/). This last one
interests me in particular, as it involves growing numbers.

### 23:15

I'm pitching Ben and Jesse on a multiplayer version of 2048. I envision a free-roaming world filled with numbered tiles to collect. Instead of collapsing numbers together against the edges of the board, players would find walls and structures within the world to collapse their numbers against.

### 23:30

- How can two or more games of 2048 occur simultaneously on the same board? In normal 2048, the player controls all tiles on the board. We decide to give each player a unique color, and allow them to assimilate unclaimed, grayed-out tiles.
- What happens when tiles from two players meet? We decide that whoever moves first gets to own the resulting collapsed tile from a move.
- How do players traverse through the world? We toss around the idea of procedural generation, but eventually decide on hand-crafted, linear levels linked together via portals.
- This raises the question: how do the portals work? And what happens to a player's tiles once they exit a level?

![](../../assets/432a75db41fa6593.jpg)


![](../../assets/432a75db41fa6593.jpg)

### Saturday 00:30

We've eaten two pizzas. We have a Git repository and a Slack instance which is ultimately only used to test out amusing Slackbot responses.

Although the game is 2D, we decide on a 3D art style with an orthographic projection, to allow Jesse to use his skills in Maya LT, which he promptly installs on my old laptop.

Ben works on the server with Node.js, while I start on the client with
[Three.js.](http://threejs.org/)

### 02:30

Ben heads home first, then Jesse. I pass out on my bedroom floor.

![](../../assets/3250f627d255f0f2.gif)

### 08:30

I wake to find Ben working in the kitchen. He spends the morning building boiler plate for the server, while I work out some Three.js details.

### 13:30

I return from a run just in time to catch Jesse pulling up with donuts. After lunch, he and I spend the next few hours working out a pipeline between Maya and Three.js.

### 16:00

I tweet our first screenshot, featuring colorized instances of Jesse's tree model displayed in a horribly distorted orthographic projection.

![](../../assets/6c0ec6c127d16055.png)


![](../../assets/6c0ec6c127d16055.png)

### 18:00

Without the server API to code against, I run out of things to do on the client. Ben finishes the data model, but he has trouble conceptualizing the rules for player movement. I haul my laptop over to indulge in some good old-fashioned pair programming.

### 19:00

Break for dinner. Burritos. Jokes.

### 21:00

Jesse continues modelling. With the basic API done, I start working to make the client consume it. Ben works on an image loader. We want to design the levels in GIMP.

### 23:00

Ben takes off. I've got player movement, animations, and tile numbers done.

### Sunday 00:30

Multiplayer works. Jesse and I play a few games against each other. It's fun! It's a game! We work out some issues with the level loading code and try to get an interesting level loaded.

### 02:00

Problem: it's pretty easy for one player to gain the upper hand and quickly assimilate all the tiles on the board, making it impossible for other players to move and grow.

### 02:30

Solution! Players should only control tiles within a certain radius of their "center". Outlier tiles are grayed out, free to be picked up by other players.

### 03:15

Fix implemented. Jesse heads home and I turn in.

### 09:15

Tweet another screenshot before heading to church.

![](../../assets/83baa8c26039ad63.png)


![](../../assets/83baa8c26039ad63.png)

At this point, I'm having an existential crisis about the name. I fire off a few panicked texts about it.

### 12:30

Ben and I are back to the grindstone. Jesse arrives with sandwiches and more donuts! Ben adds a cool username feature, but we eventually axe it to keep things simple.

### 15:00

Tweaks and bug fixes all day. Ben works on the level format, while Jesse lays out some levels in GIMP.

### 17:00

More polish. I put in Jesse's cloud models and a "connecting" spinner.

### 19:00

We finally brainstorm a name: Tile Risers. Jesse whips up a logo in Maya. We go through seven iterations before everything lines up in our janky export pipeline.

### 20:00

I spin up a Digital Ocean droplet, allocate an S3 bucket, commit the production URLs, and start filling out the submission form.

### 21:00

Time's up! Fortunately, we have another hour to submit. I later found out I misread the rules, and we actually had a whole extra 24 hours. At any rate, we were done. I commit two small bug fixes after submission, which is within guidelines.

### Conclusion

![](../../assets/9f715bc1e3f16882.jpg)


![](../../assets/9f715bc1e3f16882.jpg)

![](../../assets/70f67a1853ea2ba7.gif)

- Three.js is easy and fun.
- ES5 causes a lot of pain by continuing silently when we ask it to do ridiculous things like "compare an object to an integer".
- Ludum Dare is a blast and you should do it.
[Play Tile Risers, view the source, and vote for it!](http://ludumdare.com/compo/ludum-dare-34/?action=preview&uid=30952)