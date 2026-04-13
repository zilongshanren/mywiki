---
title: 'Proof of Concept: Routing Unreal Engine 4 to Resolume through Spout'
url: https://allarsblog.com/2014/12/13/proofofconceptspoutresolume/
author: Michael Allar
published: '2014-12-13'
source_blog: Allar's Blog
source_site: https://allarsblog.com/
category: graphics
fetched: '2026-04-13'
---

As a silly challenge, I made a solution to what I thought was the unasked question of "How to use UE4 with Spout". I set up a special Camera Actor in the world that would send its render texture target to a Spout listener using some really hacky UE4 RHI calls. To prove that it worked, I used a Spout listener in Resolume to see the live feed. Turns out it worked pretty well and people won't stop asking me about it. Some time I'd like to be able to spruce this up and open source it.