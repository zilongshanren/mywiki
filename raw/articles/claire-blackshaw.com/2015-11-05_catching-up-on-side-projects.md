---
title: Catching up on Side Projects
url: https://claire-blackshaw.com/blog/2015/11/projects-2015/
author: Claire Blackshaw
published: '2015-11-05'
source_blog: 'Claire Blackshaw: Claire Blackshaw'
source_site: https://claire-blackshaw.com/
category: graphics
fetched: '2026-04-19'
---

![Catching up on Side Projects](../../assets/d5b08550ba089f8a.jpg)

Quick update on some side projects I’ve been working on. Most of these except Block Project are experiments and are in various stages of complete. Though I've been happy with the amount of coding I've been doing at home in the second half of 2015. Go has become my goto hacking language and the move away from Unity as my hobby platform is really energising me. SDL & Psybrus give me a simple and powerful C++ base to work from. I'm happy with the progress and moving into the future I hope to update the website more frequently. I might end up plugging in some commit logs or making an easier way to quickly update the webpage.

**KBot**: Twitch IRC bot written in go with some future plumbing plans**Alley Cat**: A GBA demake of a DOS classic which I hope to port to Pebble**Go Drive Tracker**: Building a word tracker based around Go and Google Drive for Ducky as an experiment**Go Cam**: Web Cameras & Cats combined with Google Drive.**Block Project**: Not going to talk about this one much.

## KBot

So KBot is an interesting project which I want to take up for both personal and work reasons but honestly it's been pushed to the back burner.

It's been an interesting learning project as we still haven't deployed anything with Go at scale yet. So all these learnings are good and its a good sandbox on which to launch a bunch of other stuff. Also a lot of the code has been lifted into my other Go projects.

## Alley Cat

![](images/alleycat/alleycat.gif)

![](images/alleycat/alleycat2.gif)

![](images/alleycat/alleycat3.gif)

![](images/alleycat/alleycat5.gif)

Part of the #GBJam I decided to build something for Pebble watch but also to start playing with SDL2 in a real way. This is part of my ongoing move away from Unity and similiar for my home projects. For the range of reasons I covered in my [wizard post](https://claire-blackshaw.com/blog/2015/07/wizard-joy/). It was a good experience but I spent a lot of time muddling with Android toolchains and getting workflow stuff setup.

I hope to come back and finish this before the year end but what's more I have a stable small SDL project base to work from for Jams and other projects which is really useful for me.

## Go Drive Tracker

So Ducky has been using a Google Drive script to track her daily writing. It's buggy I've had to fix it and honestly it doesn't do all the things I would like. For a few reasons like plugging into external API and tracking non-google drive wirting in the future I started writing a Go Tool which plugged into the Google Drive API and buildinga word count report. It's been interesting to plug GoLang into Google API which is obviously clean and slowly building some report stuff. This is a project I chip away at and I'm mostly happy with it. Also used BoltDB as my first GoLang with DB work. Useful to learn from.

I want to put in a Twitter api hook and multi-user support. Make it a bit more robust so I can pop it onto a Raspberry Pi and forget about it.

## Go Cam

Currently I'm using 3rd party software to uploaded some security web cam footage. Sadly I have the Belkin cameras which don't play nice with 3rd party software and have some documented software exploits. I've hardened my network and tweaked with the cameras which account for most the problems though now once your on the wifi you can get to the camera feeds but I'm okay with that level of security.

Previously I've used OpenCV for image work but its C libs and dependicies would muck up this pure go project with platform specific dependicies which I don't like. I might still go with OpenCV approach but otherwise I might implement some image functions into a Go lib. This is more an experiment than anything as I do have a 3rd party solution. It did provide some interesting learnings around MJPEG.

## Block Project

![](images/cubed/screencapture_2015-10-15-00-02-21.gif)

![](images/cubed/screencapture_2015-10-18-21-45-45.gif)

![](images/cubed/screencapture_2015-10-21-00-30-41.gif)

![](images/cubed/screencapture_2015-10-21-00-44-48.gif)

![](images/cubed/screencapture_2015-10-21-00-48-13.gif)

![](images/cubed/screencapture_2015-10-25-22-35-32.gif)

So I'm not talking about this project much. It's been a very long term thing but for a range of reasons I want to get this off the ground. for a range of reasons.

One interesting point is I'm finally working on Psybrus, an engine built by @Neilogd

We used to work together so I'm familiar with his code and I like the way his code works. Psybrus gives me a stable, small and extendable basis from which to build out this project and the future projects. This project will have a few deadlines and milestones, and I'll post progress but the big picture and purpose shall remain behind the curtain on this one.