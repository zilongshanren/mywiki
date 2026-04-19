---
title: Getting into C# and Feeling Stupid
url: https://claire-blackshaw.com/blog/2010/04/getting-into-c-and-feeling-stupid/
author: Claire Blackshaw
published: '2010-04-18'
source_blog: 'Claire Blackshaw: Claire Blackshaw'
source_site: https://claire-blackshaw.com/
category: graphics
fetched: '2026-04-19'
---

![Getting into C# and Feeling Stupid](../../assets/4e402aebc4c1a4e8.png)

Today’s Goals

- Build World Manager
- Make base Hand & Frank
- Get Hand to Pick up Frank

So currently I’m doing one of the things I like least. Building low-level systems and technical plumbing. General I like to work one of two ways. On the bone raw api’s dirty and fast, or working on a high level system.

The building of engines and low-level framework style system is a crucial element which I never enjoy doing. Also my unfamiliarity with C# and XNA is a big slow down.

Transforms: Target or Moving?

The question has arisen about whether target transform or moving transform is better. I’ve used both system in the past.

Target Transform: Lerps between previous and target to return the current transform.

Moving Transform: A relative transform which is applied to current transform.