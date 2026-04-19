---
title: My Kingdom for a Team
url: https://claire-blackshaw.com/blog/2010/05/my-kingdom-for-a-team/
author: Claire Blackshaw
published: '2010-05-08'
source_blog: 'Claire Blackshaw: Claire Blackshaw'
source_site: https://claire-blackshaw.com/
category: graphics
fetched: '2026-04-19'
---

![My Kingdom for a Team](../../assets/4e402aebc4c1a4e8.png)

My Kingdom for a Team

What’s the best tool to explore and solve problems? Explain it to someone else. It’s good enough for Sherlock Holmes and its good enough for me. I hate working in isolation because you don’t need to justify or explain yourself to people. So massive gaping holes form in your logic.

Long story short is explain in the picture. WRONG! It took me a few experiments to realise this but I finally did.

- Radial Menus are conceptually complex
- This makes them good to manage large amounts of choices
- ONE BUTTON!!!

Okay this game is focused on being simple and broad age range according to the brief. So one button is good. This combined with the mantra, “*You can do what Frank can do*”. A break through moment I had on the bus which confused many people last week.

So whenever you push the button on something you activate the action Frank would. The only additional actions are, Highlight, Pick-up (optional) & Customize(optional).

When interacting with Frank the actions are Praise / Scold, and Pick-up.

Now there are other actions. Like looking at stats, buying things from the shop, selling things, ect… But I realised I should bake these into the world as objects. That way they are easier to identify and interact with (kids prefer less abstraction). They are self-contextual and tbh look cooler.

### The Other Problem

So what have I been wrestling with all day other than my own stupidity. Well a design choice and some coding issues.

The design choices involve things like.

- Camera Facing / World Orientated (see last post)
- Facing: Cleaner Smoother Fonts (made less of an issue by HD)
- World: Feels more part of the world
- World: Able to animate in 3D and look cooler (sounds stupid but cool is a test)
- Floating above, fixed location or surrounding

Anyway they are game specific and rather dull. I want to talk about a code issue.

### You want HOW MANY!

Beginners and hackers will always dynamically allocate verts and primitives. THIS IS BAD! I know it’s convenient but it’s wrong. Resources should be compiled and processed by the content pipeline or equivalent. This allows unified buffers, optimisation of vertex declarations and lots of other neat things which make the Tech Trolls happy, otherwise they club you with a big stick.

This applies to the UI because well I was looking at generating the menu based on X choices which means generating verts based on splits… blah blah blah.

**Caveat**: *Rules are made to be broken! Truly dynamic objects, like water simulations for instance may need to be altered. However try move choices like vert declarations and number verts to pack time. Understand why you are breaking the rule before breaking it. Remember over assigning a large pool on a loose fit is often better than a dynamic solution which fits better but restrains you more.*

Wow that was a long post.