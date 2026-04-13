---
title: 'Behind the audio of Total War: Three Kingdoms'
url: https://www.gamedeveloper.com/audio/behind-the-audio-of-i-total-war-three-kingdoms-i-
published: '2019-07-02'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

July 2, 2019

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

Author: by Tom McCaren, Valentin Goellner

By Tom McCaren, Senior Audio Designer and Valentin Goellner, Audio Designer at Creative Assembly

One of the main challenges in creating the audio for strategy games, especially the Total War series, is in creating compelling soundscapes that not only set the mood, but also enhance the visual aesthetic and bring the world to life. All while remaining interesting and immersive to players, even after hundreds of hours of play.

Total War: Three Kingdoms is set in China, a country that is as vast as it is diverse. It is a country rich in history and full of breath-taking scenery, so we wanted to reflect this with the audio. To achieve this, we created many new audio systems for Total War: Three Kingdoms to help us ensure that the sound remains vibrant, feels responsive to player actions and has a level of authenticity that surpasses previous Total War games.

![](../../assets/c1987d2c9b4335c8.img)


Three Kingdoms is the first Total War game to have a continuous day and night cycle, where players can experience an entire 24-hours within a single turn. This was a challenge as it meant creating an audio system that would allow for the ambiences used at the various times of day to blend with each other seamlessly across the entire map, while also sounding coherent and believable.

In a Campaign, players will hear not only the sounds of the wildlife across the map changing over the course of the day, but the sounds of the settlements as well.

Early in the morning, only a minimal amount of activity will be audible within settlements, with the chattering sounds of a few small groups of inhabitants starting their day. As the day progresses, the crowds start to gather and gradually increase in size right up until the early afternoon, when the streets and markets are at their busiest. Players will be able to hear traders trying to sell their wares and tools and weapons being made in workshops for workers and armies. As the day moves on into the evening, the crowds begin to dwindle and gradually become quieter as the inhabitants go home for the night.

The crowd audio varies depending on the size of the settlement, with larger cities having much larger crowds than small villages. This helps to provide a sense of contrast between settlement types and hopefully will enable players to identify these on some level by their sound alone.

![](../../assets/b4b07c1742e728b4.img)



We have around 3000 lines of Walla (background vocalizations) that we trigger from within settlements. These have been performed by native Mandarin speakers, something which we felt was important for authenticity. We created a modular system that triggers combinations of appropriate SFX and lines of Walla depending on certain in-game conditions. Some of these include: the current season, settlement type, the time of day, the public order level and the district buildings that players have constructed within their settlements. This creates a huge amount of variety and enables the settlement audio to react to events and changes in gameplay conditions in real time.

Our main goal with the audio for the settlements was to make them feel alive, dynamic and responsive to certain in-game conditions for an added level of realism. For example, players will be able to hear inhabitants yawning and saying how tired they are in the evening while, during winter, players may hear inhabitants talking about how cold and hungry they are.

As players upgrade their settlements and construct more buildings within them, they’ll start to hear new sounds that are appropriate to that new building type. If players construct a school for example, they’ll hear children laughing and playing. Alternatively, if players construct an Inn, they will be able to hear a few inhabitants enjoying themselves after a few drinks once everybody else has gone to sleep for the night.

![](../../assets/8020df0f88b78f84.img)


Wildlife is another element that adds a lot of flavor to a soundscape and it’s something that we leaned on heavily to create the right feel and characteristics for the sounds of the various regions and seasons. To ensure that the wildlife sounds were accurate both biologically and geographically, we undertook a vast amount of research. We gathered detailed information on many species of animals including their natural habitat, migration and hibernation behaviors, active times of day and mating seasons.

There are wildlife sounds unique to each climate region (Arid, Cold, Subtropical and Temperate) which helps to give each area its own character. Different wildlife sounds are also triggered depending on the current season and time of day. This helps to keep the soundscape interesting and responsive to changes in conditions, which makes the world feel more alive.

We aimed to make the Campaign map a calm, serene and pleasant place for the player to be. We wanted it to be a sharp contrast to the turbulent and often hectic sound of the battles. A large part of how we accomplished this was not only with the sounds that we used, but also with how they trigger in-game and how they blend and interact with one another.

We used a lot of relaxation ambience and ASMR (autonomous sensory meridian response) videos for reference while designing the soundscapes. This is particularly evident in some heavily forested areas during rainstorms, where you can hear the individual raindrops hitting the leaves all around you, creating an oddly satisfying sensation.

![](../../assets/aff70eb72fda4519.img)


The user interface (UI) sounds in previous Total War games have generally comprised of lots of large cinematic sounds such as sword scrapes, anvil hits and so on. However, as much fun as it can be playing with big swords and other weapons in the recording studio, with Total War: Three Kingdoms we wanted the style of the audio to match the abstract visual aesthetic, keeping the UI sounds clean, minimal and refined.

To achieve this, we toned down the big weapon hits and instead opted to use original recordings of traditional Chinese instruments combined with some abstract, non-literal sounds to represent the ink effect used heavily in the UI visuals.

We also wanted the audio to tie in with the elemental theme of Wu Xing (the five-element theory of Chinese philosophy) that is present throughout the game. To do this, we created modular sound kits for each of the Wu Xing elements; Earth, Fire, Metal, Water and Wood.

We added sounds from these kits as sweetener layers to help communicate the link between some actions and the associated Wu Xing elements to the player. An example of this is when you spend character skill points. Upon clicking an elemental skill point button, players will hear a sound that corresponds to the element of the skill point that they have just purchased.

Recreating the sounds of China has been a joy. In the process we’ve managed to develop a lot of new tech, which has enabled us to deliver what we consider to be the most authentically detailed and polished sounding historical Total War game to date.