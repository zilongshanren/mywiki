---
title: A Precise Audio Sequencer for Unity
url: https://www.gamedeveloper.com/audio/a-precise-audio-sequencer-for-unity
author: Erdin Kacan
published: '2015-05-20'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

# A Precise Audio Sequencer for Unity

I have started a new project which required a stable Audio Sequencer. Unfortunately and surprisingly I could not found any stable solutions online. So I have decided to create on myself.

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

A couple of days ago I have started a new project which required a stable Audio Sequencer. Since I didn’t had any previous experience regarding Audio Sequencer I have started traversing the Internet to find a clue about how to create one. Unfortunately and surprisingly I could not found any stable solutions online. So I have decided to create one myself.

Unity Audio Sequencer works directly in audio buffer to be able able count the ticks and play the audio precisely. My tests showed that it was able to perform without any problems up to 250-300 bpm with multiple audio files played simultaneously.

I have seen a lot of forum posts and questions about audio sequencers around without any stable solutions, therefore I have decided to make Unity Audio Sequencer open source and free!