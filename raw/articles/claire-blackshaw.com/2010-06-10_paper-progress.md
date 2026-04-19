---
title: Paper Progress
url: https://claire-blackshaw.com/blog/2010/06/paper-progress/
author: Claire Blackshaw
published: '2010-06-10'
source_blog: 'Claire Blackshaw: Claire Blackshaw'
source_site: https://claire-blackshaw.com/
category: graphics
fetched: '2026-04-19'
---

![Paper Progress](../../assets/4e402aebc4c1a4e8.png)

So I was so tired of seeing a computer the last few days I switch to paper notes for a while. Still need to scan / transcribe them to digital format. Here are some highlights

## Key Points

**Goal**: To explore and define a method for game agents to comprehend game objects and events with the ability to query and respond.

**Method**: By implementing a reference scenario in XNA.

The exact **schema** I choose for the implementation is trivial, but the graph Query & Response format is key.

## Systems

These systems are listed in order of implementation. For my dissertation I shall only be doing the first **three**. I do plan to eventually do all of them.

**Knowledge Storage**: Representing knowledge in graph format.

**Query & Response Format**: Query an agent and formulate a response

**Agent to Agent Discovery**: Two agents converse and update their knowledge graph based on response. An agent also needs to resolve data conflicts.

**Chinese Whispers**: An agent mishears or corrupts data on receiving knowledge.

**Lies**:An agent intelligently mutates data on output when certain conditions exists.

**Input & Output Translation**: Data is transformed from graph format to friendlier format. Possible IF parser, GUI system or NL system.