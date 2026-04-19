---
title: A Kiss is always harder than a Kill
url: https://claire-blackshaw.com/blog/2011/05/a-kiss-is-always-harder-than-a-kill/
author: Claire Blackshaw
published: '2011-05-27'
source_blog: 'Claire Blackshaw: Claire Blackshaw'
source_site: https://claire-blackshaw.com/
category: graphics
fetched: '2026-04-19'
---

![A Kiss is always harder than a Kill](../../assets/4e402aebc4c1a4e8.png)

*Originally written for #AltDevBlog:*

[Link to Original Post](http://altdevblogaday.org/2011/05/27/a-kiss-is-always-harder-than-a-kill/)Games let us craft interactive systems in which we can play and explore. We play with limited rule-sets, physics, combat, squad based AI, and a million other complex systems which give us a world to explore. Why then is one of the core human experiences, our social nature, all but missing from games?

Delete several paragraphs explaining where we are and why – assume audience knowledge

It all boils down to the fact in many ways the dialogue tree system we are so comfortable with is a local maxima in evolution of social interactions and needs to be discarded to make progress.

![](/images/Blog/agent.jpg)


Let’s take a brutal approach to a social interaction with a game agent. Now if we look at the three stages we can separate them nicely. Currently Inputs are stupidly simple, the game-pad offers the emotional range Morse code, no wonder the agent has trouble interacting. I’m less concerned here because of Kinetic and the brilliant academic research being conducted in this field.

Our outputs however are extremely high quality with amazing voice acting, great visuals and delivery in our high end products. Though the methods we use aren’t scalable, and impractical for dynamic systems. Again there is great research in text-to-speech, automated lip syncing and similar technologies. So great strides being made in this area, but it will be the most painful transition to make as early version of this technology just can’t compete with the pre-baked polished deliveries we have at our disposal.

While challenging I think both of those areas are moving forward at a good pace and will be solved in the near future.

Then we get down to the gritty problem of the agent itself and the formulation of a response. Something we are getting very good at for say tactical combat simulation, where the inputs are better and the outputs rule governed. The dialogue tree however is at the end of the day a static graph (path manipulation through skill rolls or simple scripting doesn’t count) which creates a dumb but effective reflex agent.

How can we grow this agent into a more intelligent system which allows for play and exploration? Can we make an agent who processes and develops an opinion of our actions rather than simply reacting to them by a cast iron static reflex system?

Now while research is going on in this area its super fluffy and long range and does not get as much funding, mostly due to past developments in academia (see [AI Winter](http://en.wikipedia.org/wiki/AI_winter)). One of the trickiest areas with an intelligent response is it requires some degree of knowledge, and knowledge representation is a damn tricky problem in the AI world.

### Nuts & Bolts

The key point to the entire problem is that the agent in a game-world, unlike an agent trying to exist in “reality”, lives in a world where we know everything. Using this we can seed them with knowledge they require and a basic relationship network. Through this they can perceive and understand any event which is within the scope of the game world as we have provided them with a working knowledge base from which to understand it.

This will allow us to make advances faster than our “reality” counter parts with quicker results as we have limited the scope of the problem space. Game developers like to cheat :) . It would also help if for the short term if we allow ourselves to use clunky or unappealing input or output systems which would not be acceptable in a commercial product :(

Now I know this all sounds very fluffy and I sound like a crazy newbie who has discovered neural nets for the first time and has a naïve grin ear to ear. Though I do acknowledge the scope of this problem and I know the way forward is solving a lot of smaller problems to construct the tools to solve the larger. My dissertation which focussed on building a query/response framework along with the concept of 2nd degree authorship was the umpteenth step for me but the 1st solid piece of results.

2nd Degree authorship had to be proven because I know that at the end of the day we do still want to write and construct narratives, rather than pure random simulation situations. I proved this with a fairly simple rule-based modifier system, one possible solution to procedural authorship of social interactions.

Another requirement is data model which was generic enough to be expanded without being reworked. Again I manage to propose a fairly simple atomic model which would work for several game systems.

Finally I looked at building a query response model which could hold context and remain fairly generic. My research mostly hit dead ends until I considered representing a conversation as a tree, which provides context and a query as a path through that tree with null nodes. Response then could be sub-trees. XPath nicely fitted to this concept and I’m quite happy with the flexibility of the resulting system.The full details up to this point can be read in [my dissertation here](https://docs.google.com/document/pub?id=1uxffH9h2Rt0_yhAmV27gZ3LHvDilgNLPFwiScy6v-i4).

The next step is build a system in which agents can observe a self-contained play session, discuss it with a player entity or another agent and have a personality persists over multiple sessions. I had two possible planned prototypes to explore this concept. This is the thing I was struggling over for the last week.

The detective prototype was appealing due to its lack of what we will call secondary work (not directly pertaining to the research). In this scenario we would use 2nd degree authorship aided by some procedural systems to generate a crime scenario. The player would then interrogate several agents to try build a picture of the truth. The agents would of course have a personal partial vision of the situation and be manipulating their responses to remove the appearance of guilt.

This is an appealing prototype firmly built on my previous work with little need for secondary work. The two key concerns however were that it strongly depended on the strength of my generation algorithm and would therefore possible reach a dead-end or be handicapped if that system were inferior. It also caters to a fairly narrow spectrum of games, not having many traditional games systems interaction with the social model.

So the second prototype is a tactical turn based shooter. A game I’ve been throwing around for the last year or so, in which the world is persistent but the missions are throw-away and players build reputation. The idea is that the agents (in this case infiltrating squad members, or defence agents) can debrief their controller after the mission about the events. These agents would be persistent over the game world getting hired, fired and killed.

The main point here is the social information is mostly being scraped from a “live” game session in which one side (the defender) is not actually present. The downtime between missions however can be used to de-brief and casually talk about items. This means the game itself is not reliant on the social system, making it easier to have multiple versions, swap out or rewrite the social component without altering the game itself.

Also the persistent nature of the agents mean if I leave a server running long enough distinct social ecosystems should hopefully evolve.

Well that’s the plan; I’ll discuss more details in future posts and as the project advances. If you have any interest in this field or my research please do contact me I’m always looking for people to bounce ideas off and just share my crazy dream to cut-down the dialogue tree and burn its pitiful remains in the fires of progress.

Further ramblings on the matter are on my site,[FlammablePenguins.com](https://claire-blackshaw.com/)