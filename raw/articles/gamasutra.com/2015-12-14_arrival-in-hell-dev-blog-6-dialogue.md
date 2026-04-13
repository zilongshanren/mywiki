---
title: 'Arrival in Hell: Dev Blog #6: Dialogue'
url: https://www.gamedeveloper.com/audio/arrival-in-hell-dev-blog-6-dialogue
author: Matthew Shaile
published: '2015-12-14'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)


![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)

**Featured Blog | **This community-written post highlights the best of what the game industry has to offer. Read more like it on the __Game Developer Blogs.__

# Arrival in Hell: Dev Blog #6: Dialogue

This week's instalment goes over dialogue (or dialog to my American cousins).

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

The thing that has always attracted me to point and click adventure game is the dialogue. I love the little quips the protagonist comes out with, often breaking the fourth wall. I knew I wanted Arrival in Hell to follow this style, but there were many different choices to make when deciding how we wanted to present our dialogue.

The first decision was whether to have lip synced models, a ‘talking head’, or no mouth movement at all. Lip syncing models is something which would have been way too time consuming for a tiny team of two, and omitting mouth movement entirely only really works if dialogue is text only. Since we planned on using audio voices, the only option we could feasibly achieve was talking heads.

![Example of a talking head from the excellent Monster Rancher 2 (which I loved as a kid) Example of a talking head from the excellent Monster Rancher 2 (which I loved as a kid)](http://epicindustries.co.uk/wp-content/uploads/2015/12/talkingHeadExample.jpg?width=1280&auto=webp&quality=80&disable=upscale)


Example of a talking head from the excellent Monster Rancher 2 (which I loved as a kid)

This made it much easier to implement some level of lip syncing when talking, however we stumbled across an amazing program, [CrazyTalk](https://www.assetstore.unity3d.com/en/#!/content/19309). Although it’s a little pricey, and their support is awful, the end result is excellent for the amount of effort it takes to implement. Basically you just map a 2D image in their software, then add voice clips. The software automatically adds lip-syncing; you can even choose the characters emotion for each line. You can then export these to be rendered at runtime in Unity, so the file size footprint is tiny too.

![Setting up the Crazytalk mapping on a 2D image Setting up the Crazytalk mapping on a 2D image](http://epicindustries.co.uk/wp-content/uploads/2015/12/CrazyTalkMapping-1024x621.png?width=1280&auto=webp&quality=80&disable=upscale)


Setting up the Crazytalk mapping on a 2D image

![Very fast process for generating lip-sync Very fast process for generating lip-sync](http://epicindustries.co.uk/wp-content/uploads/2015/12/CrazyTalkProcess.gif?width=1280&auto=webp&quality=80&disable=upscale)


Very fast process for generating lip-sync

This is still a laborious process, as just the first couple of rooms include about 70 phrases; imagine having to animate all of those by hand!

Showing the lip-sync animation, playing the audio and printing a subtitle to screen is easy, we just have each [InteractiveObject ](http://epicindustries.co.uk/2015/11/27/arrival-in-hell-dev-blog-4-interactive-objects/)select these by it’s id. When you start a conversation with an NPC however, it becomes a lot more complicated. To keep things consistent, we decided we’d use the same dialogue system for talking to people and commenting on objects. Think of it as a conversation involving one person and an object.

![The main character saying his classic line to the toilet The main character saying his classic line to the toilet](http://epicindustries.co.uk/wp-content/uploads/2015/12/dialogueExample1.gif?width=1280&auto=webp&quality=80&disable=upscale)


The main character saying his classic line to the toilet

When I implemented this system, Unity had just released official support for [non-animation state machines](https://unity3d.com/learn/tutorials/modules/beginner/5-pre-order-beta/state-machine-behaviours) piggybacking on mecanim. This seemed like the perfect thing to use for designing complex conversation trees. However, just before I began implementing my own dialogue system, I decided to check the Unity asset store.

Time and time again in this project I have opted to go for off-the-shelf solutions to problems rather than spending tonnes of my time reinventing the wheel. This is crucial in modern game development as consumer expectations have increased drastically since I first got started making Flash games. Using an already tried and tested system allows me to spend more of my time on the creative aspects of the game.

I decided to use [Dialogue System for Unity](https://www.assetstore.unity3d.com/en/#!/content/11672). I only use it for dialogue trees, localisation, export and saving my place in a conversation, however it can do a lot more, such as quest tracking and camera scripting. Their customer support is also top-notch, which is really important to me.

![Graphical node-based conversation editor Graphical node-based conversation editor](http://epicindustries.co.uk/wp-content/uploads/2015/12/DialogueEditor-1024x605.png?width=1280&auto=webp&quality=80&disable=upscale)


Graphical node-based conversation editor

In the Dialogue System editor, I add a conversation for every interaction in the game, then I simply start that conversation every time I interact with the corresponding object. The “conversation” could just be one line, or it can be a complex tree like above.

The dialogue editor allows you to assign a default script every time a new conversation is triggered, so I simply have that play the right CrazyTalk animation and voice sound based on the id of the conversation.

Finally, the dialogue system includes a multiple choice response UI. You can easily skin the ones they provide or create your own from scratch. Below is an example of our the final product looks in our game at the moment.

![How a conversation looks in the game How a conversation looks in the game](http://epicindustries.co.uk/wp-content/uploads/2015/12/dialogueExample2.gif?width=1280&auto=webp&quality=80&disable=upscale)


How a conversation looks in the game

The last thing I wanted to write about before I wrap up the article is how we went about voicing the game. We tried using whatever microphone we had lying around (a phone, a webcam etc) and it sounded awful. We decided we’d invest in a decent mic. After reading various reviews and testimonials, we decided to get a Blue Yeti. It is excellent quality for an affordable price. Dialogue system also has a really handy export function so we can export the phrases directly from the game and print them out as a script. Currently the game is voiced by a friend of mine; we can’t afford to hire ‘proper’ voice actors, so the game will be voiced entirely by friends and family.

![My desk sometimes doubles as our recording studio My desk sometimes doubles as our recording studio](http://epicindustries.co.uk/wp-content/uploads/2015/12/mic.jpg?width=1280&auto=webp&quality=80&disable=upscale)


My desk sometimes doubles as our recording studio

That about wraps it up. I know there are many alternatives to all of the systems we are using, I’m not saying our choices are better than any others, just that I’m happy with what we’ve chosen and it’s working really nicely for us.