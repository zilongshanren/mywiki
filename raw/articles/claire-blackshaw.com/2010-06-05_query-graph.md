---
title: Query Graph
url: https://claire-blackshaw.com/blog/2010/06/query-graph/
author: Claire Blackshaw
published: '2010-06-05'
source_blog: 'Claire Blackshaw: Claire Blackshaw'
source_site: https://claire-blackshaw.com/
category: graphics
fetched: '2026-04-19'
---

![Query Graph](../../assets/4e402aebc4c1a4e8.png)

Okay so loads of code written, which has really found holes and helped smooth out the model.

## Query Graph

Okay so the most basic Query format is a Graphed Query.

### Pop-able Context

Any item which is pop-able can throw away it’s parents without loss of information. You may want to keep the context if you want to use a “previous topic” action. If the depth is becoming unmanageable however you can slice off the top at Pop-able joints.

Items which are not popable require their context to make sense.

### Current Context

The current context is the Query which was passed in, we can then pass out the response nodes.

If you have a general query then an outline will be provided on the context item.

If you have a specific query, for instance the above query could be expressed as.

Object(Knife) -> Event(Stabbing #2) -> Actor( NULL )


## Agent Data

What data does each agent hold, well coding really shone light on the dark places and showed up the cracks.

### Atom

The Atom element indicates **time-sensitive** data. It can be attached to anything, to contain a time sensitive element. AtomCollection was a break through, it smooths out the accessing of Time Sensitive data.

Atoms cannot be a child of Event Node.

### Talk Base

Person, Place, and Event all inherit from Talk Base.

Talk Base has a list of status which allow generic attachment of time-sensitive data.

### Data Groups

At first I was look at expanding the data model but then I thought of data groups. So the Graph provides context.

### Verb

I’m still not happy with the verb declarations, the model needs some revision.

I’m thinking of having a dictionary of possible game verbs.