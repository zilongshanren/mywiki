---
title: runevision blog
url: https://blog.runevision.com/2017/02/
published: '2017-02-21'
source_blog: Blog - runevision
source_site: https://blog.runevision.com/
category: graphics
fetched: '2026-04-19'
---

Here's the latest updates on the development of my Vive VR game [Eye of the Temple](http://blog.runevision.com/search/label/Eye%20of%20the%20Temple).

![](../../assets/73e011dc41db4484.gif)

New features:

- There are now gems throughout the temple that you can collect.
- Moving platforms have glowing symbols on them.
- Visuals: Intro area has some red stones and some of the dungeons have grittier gray stones and spikes.
- The way the platforms move has been tweaked, hopefully to further reduce potential for dizziness.

### Notes on gems

The gems are found throughout the temple. The exact placement tries to take player proportions into account so that they are at a comfortable distance for reaching. I haven't tested this on different people yet though. If you could let me know how it works for you and how tall you are, that would be helpful. If you don't want to share that, that's ok too.

Right now the gems don't do anything yet. Later I will implement at the minimum a way for you to see how many you collected.

Beyond that I need to decide if the gems have a critical or non-critical function:

A critical function of the gems could be if they are used to unlock new areas in the game and thus are needed to progress. Or an almost-critical function would be to unlock alternative paths or secret rooms not otherwise accessible. This is still fairly critical because it would be annoying if you're trying to see 100% content of a game to find out you can't due to some mistake made earlier that's too late to do anything about. Currently there are one-way platforms that you can take which will prevent you from going back to collect any gems you might have missed. If I make the gems critical, I'd have to find a way to make it possible to always go back to all areas of the temple.

Non-critical functions of the gems could be high-score, achievements, and, I dunno, unlockable hats if I get a selfie stick implemented for the game. :P Old games would typically grant you extra lives, but it doesn't work for modern games with infinite lives.

For now I refrained from placing gems at platforms that only go one way. If there were gems there and you failed to pick one up, you wouldn't have a second chance and I thought that might feel unfair or frustrating.


### Early testers online forum

In order to try to get faster feedback and shorter iteration cycles, I opened up for people to [sign up online to be early testers of the game](https://itch.io/t/59040/early-testers-welcome-thread-introduce-yourself). If you have access to a Vive (and 2.2 by 2.2 meters space) and would like to try out the game and provide detailed feedback based on your experience, please don't hesitate to join!