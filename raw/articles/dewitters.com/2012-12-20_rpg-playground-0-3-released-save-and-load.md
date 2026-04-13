---
title: 'RPG Playground 0.3 released: Save and Load'
url: https://dewitters.com/rpg-playground-0-3-released-save-and-load/
published: '2012-12-20'
source_blog: deWiTTERS
source_site: https://dewitters.com
category: game programming
fetched: '2026-04-13'
---

A lot of you have been waiting for this, so here it comes: You can now save and load your levels in RPG Playground! Currently only 1 level can be saved an loaded again, but hey, you got to start somewhere. I just put the new version online, so go check it out at [http://rpgplayground.com](http://rpgplayground.com).

The next thing on my list is to allow you to save and load multiple levels.

## 9 Comments

## Spencer H · December 20, 2012 at 17:01

Oh noes! I cannot log in or register a new account!

I keep getting a HTTP IO Error when registering a new account and a “could not log in, timeout expired” error when logging in with the previously registered account for (0.2) Still holding onto my excitement, i’m sure this is an easy fix.

## Spencer H · December 20, 2012 at 18:03

things seem to be in working order now.

## Adorna · December 28, 2012 at 05:25

I had the same error, but its solved. Also – (probably no longer an issue) if the menu on the left is active, it overlapps the login and none of them could be closed. Its working now so I guess its not an issue anymore..

I’m very interested in how this turns out.. its seems like such a cool idea. I just wished it would work on my tablet..

## Koen Witters · December 28, 2012 at 06:04

@Adorna

The issue where the left menu overlaps the login popup is indeed fixed in the latest version.

What kind of tablet do you have?

## Adorna · December 28, 2012 at 06:55

Yay 😀 I have a sony Tablet S – but I think its mainly an issue of android not supporting the browser plugin ..

## Koen Witters · December 28, 2012 at 10:48

RPG Playground is written in Flash, so it should work on Android. I have a Samsung Galaxy Tab and it works, only the text input doesn’t :(, so logging in doesn’t work. But creating levels shouldn’t be a problem.

## Fabian · January 3, 2013 at 07:58

Keep up the good work. This is really nice. But do you think, that flash is the right chose? Adobe seems not to develop and support it any further. HTML5 seems their new focus.. Would be a pitty if all your fine work would be ruined by loosing flash as platform.

## Koen Witters · January 4, 2013 at 01:53

@Fabian

I still think I made the right choice by choosing Flash instead of HTML5. The user base of Flash is still way bigger, and I don’t feel that HTML5 is ready for prime time yet. Articles like http://www.gamasutra.com/view/news/172804/Wooga_drops_HTML5_development_but_believes_it_still_has_a_future.php just confirm my thoughts.

But I assume that at some point I will have to port it to HTML5. That’s why my server is written in node.js, so I don’t have to port anything on that side. I’ve ported plenty of games in the past, and it’s not that much work if you know the code and it’s well structured. So don’t worry, once Flash loses its support, RPG Playground will be ported to the best alternative.

## Adorna · January 4, 2013 at 12:22

Seems the problem was not my tablet but using Chrome as a browser – it won’t play flash files onn android…