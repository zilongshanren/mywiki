---
title: A* is Overrated
url: https://bitsquid.blogspot.com/2010/10/is-overrated.html
author: Niklas
published: '2010-10-20'
source_blog: 'bitsquid: development blog'
source_site: https://bitsquid.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

Open any textbook on AI and you are sure to find a description of the A*-algorithm. Why? Because it is a provably correct solution to well defined, narrow problem. And that just makes it so... scientific and... teachable. Universities teach Computer Science, because nobody knows how to teach Computer Artistry or Computer Craftsmanship. Plus science is important, everybody knows that.

But I digress.

A* is a useful algorithm. You should know it. But when we are talking about AI navigation, A* is just an imperfect solution to a tiny and not very difficult part of the problem. Here are three reasons why you shouldn't give A* so much credit:

**1. Pathfinding is often not that important.**

In many games, the average enemy is only on-screen a couple of seconds before it gets killed. The player doesn't even have a chance to see if it is following a path or not. Make sure it does something interesting that the player can notice instead.

**2. A* is not necessarily the best solution to path finding problems.**

A* finds the shortest path, but that is usually not that important. As long as the path "looks reasonable" and is "short enough" it works fine. This opens the floor for a lot of other algorithms.

For long-distance searches you get the best performance by using a hierarchical search structure. A good design of the hierarchy structure is more important for performance than the algorithm you use to search at each level.

Path-finding usually works on a time scale of seconds, which means that we can allow up to 30 frames of latency in answering search queries. To distribute the work evenly, we should use a search algorithm that runs incrementally. And it should of course parallelize to make the most use of modern hardware.

So what we really want is an incremental, parallelizable, hierarchical algorithm to find a shortish path, not cookie cutter A*.

**3. Even if we use A*, there are a lot of other navigational issues that are more important and harder to solve than path finding.**

Implementation, for starters. A* only reaches its theoretical performance when the data structures are implemented efficiently. You can still find A* implementations where the open nodes are kept in a sorted list rather than a heap. Ouch. Some implementation details are non-trivial. How do you keep track of visited nodes? A hashtable? (Extra memory and CPU.) A flag in the nodes themselves? (Meaning you can only run one search at a time over the nodes.)

How is the graph created? Hand edited in the editor? How much work is it to redo it every time the level changes? Automatic? What do you do when the automatic generation fails? Can you modify it? Will these modifications stick if the level is changed and the graph is regenerated? Can you give certain nodes special properties when the graph is auto-generated?

How do you handle dynamic worlds were paths can be blocked and new paths can be opened? Can you update the graph dynamically in an efficient way? What happens to running queries? How do past queries get invalidated when their path is no longer valid?

Once you have a path, how do you do local navigation? I.e. how do you follow the path smoothly without colliding with other game agents or dynamic objects? Do AI units collide against the graph or against real physics? What happens if the two don't match up? How do you match animations to the path following movement?

In my opinion, local navigation is a lot more important to the impression a game AI makes than path finding. Nobody will care that much if an AI doesn't follow the 100 % best part towards the target. To err is human. But everybody will notice if the AI gets stuck running against a wall because its local navigation system failed.

In the next blog post I will talk a bit about how local navigation is implemented in the BitSquid engine.

I do agree on the importance of local navigation. I've been preaching about it recently too [1].











ReplyDeleteHashtable for visited nodes is good. Your usual performance bottle neck is the O(n^2)-ness of A* and node cost calculation, and then maybe managing the heap.

If your A* result takes seconds, then there are something wrong. Detour can handle around 10k paths/sec. Those quite short FPS style paths, that is. What is nasty about A* is that the time it runs is quite unpredictable.

Moving should be always constrained to the graph. Period. :) There is no other way to make to work. There are many ways to do that in conjunction with local avoidance and steering. I usually use BF-search [2].

In many games, you want the agents to "see" the blockage ahead before they replan their path. In that case it is fine to poll the data slightly ahead (i.e. during string pulling, see my presentation) and of it has gotten rotte, schedule a plan.

If you use navmeshes, the path is never perfect, but you can improve it incrementally as you go. What is most important with navigation is to store the path data in such format that it is flexible.

That is, never store a straight path, but the corridor (linear list of polys) that lead to the goal. If you fall off the corridor, you patch it, or if your target moves you patch the corridor too. That way the movement is always robust and you seldom need to replan if things go slightly wrong.

A* != navigation, it is just one solution to make the problem linear.

"Human error" or "human-likeness" are the roots of all evil in solving navigation issues! It just leads to sloppy code and bike-shedding. They should be never used to justify a design unless you have a lot of data to back it up. Intuition does not apply to local navigation design either.

[1] http://digestingduck.blogspot.com/2010/07/my-paris-game-ai-conference.html

[2] http://digestingduck.blogspot.com/2010/07/constrained-movement-along-navmesh-pt-3.html

Hi Mikko, many interesting points in your comment (as you would expect from the author of Detour ;). Some comments back.







ReplyDeleteHashtable for visited is good for most searches, but in the worst case (every node is expanded) it is slower and uses more memory than a flag-per-node.

When I said that pathfinding works on a time scale of seconds I didn't mean that A* takes seconds, of course it doesn't. What I meant is that usually it is OK for an agent to wait up to a second to get the result of a pathfinding query. It doesn't have to start running immediately. So we have room for latency, which we can use to load-balance and parallelize.

And as you said, most searches are not a problem. The nasty part are the worst-case scenarios that end up expanding almost every node in the graph. (Especially if there is no hierarchy and >50k nodes in the graph, and many agents start a search in the same frame.) Load-balancing lets us limit the number of nodes expanded/frame at the cost of latency. Can be a useful tool.

I agree that when the movement is not constrained to the graph, the navigation system cannot be made 100 % reliable which means that higher systems cannot 100 % trust it, which tends to make the entire AI messy and unreadable. But constraining the movement to the graph comes with its own issues. What if the agent is throwed outside the graph by an explosion? Or pushed by a tank. Irresistible force, meet immovable object. (The Alexandrian solution: kill any agent that falls off the graph.)

The "human error" remark was tounge-in-cheek, but I understand your reaction. There is a tendency towards sloppiness in a lot of AI programming. Lower level systems don't return 100 % reliable results and then higher level systems are written that take that into account and second guess the lower level system until everything descends into chaos.

In the context I just meant that it is often OK to use techniques that not guarantee the absolutely shortest path. For example, hierarchical search. (We might have found a shorter path by doing a full A* search at the lowest level.) Or using a non-admissible A* heuristics. (Which will expand fewer nodes in the average case, but might not return the shortest path.) Of course the system should be up front about what it does and not promise that it will deliver the shortest possible path if it won't.

Hello Nikklas I agree with you please send me the money from the community thanks

DeleteGood points comments and I agree.






ReplyDeleteI guess I need to fight against the "human error" comment so much that it always makes my blood pressure to raise :)

Flags might be ok, if you have only one search going on concurrently. I think that is shortsighted, though. If you have 50k polys, and really want to optimize for the worst case, an external bit-vector is probably better. I usually have hard limit for number of nodes to visit (around 4k range), so it is somehow bound.

I agree on your points about hierarchy, both the pros and cons, and I don't have much else to add that I wish I had more time at disposal so I could finally implement that in Detour :)

I have not found a good case yet where the Alexandrian + some design choices would not solve the outside the mesh case. In your above cases both can be solved by killing the NPC and making the reaction to follow the navigable area (instead of pure physics based). At least it would be less immersion-breaker than an AIs failing to walk through a doorways.

I would rather mess up one agent in odd case than sacrifice all the movement because of that. It is a hard bit to swallow for both designers and programmers.

1. Is highly incorrect dependent on the type of game, and since Bitsquid is supposedly a general purpose game pathfinding can be incredibly important. It gets enemies onto the screen in the first place if the world is big enough. If it's a strategy game it gets your dudes into the right position instead of off in the middle of nowhere.


ReplyDeletePathfinding is one of the most common subjects in game AI for a very good reason.

Sean: You'll notice that I said "in many games" and "the average enemy". Not every enemy in every game. I certainly didn't mean to imply that path finding is never useful or that the BitSquid engine doesn't have support for path finding (it does). I thought that would be evident from the amount of time I spent discussing how to implement path finding in the rest of the post.






ReplyDeleteRather, the point was to rally against the attitude that when you have issues of navigation "just apply A*" and everything will be solved. A* is just a small part of the puzzle.

But I do feel that (because of this attitude) there is a tendency to overuse path finding.

An example: In Diablo 2 your hired mercenary uses path finding to keep close to you. This often bugs out in the dungeons, when some enemy is blocking the shortest path to the room you are in. The mercenary will find some alternative route that goes across half the map and disappear off screen for minutes, leaving you alone in the battle. Often it gets teleported in later, because it never found its way back.

In this case path finding was not the best way to follow a moving target in a world of moving obstacles. The constant replanning (is it even a "plan" if it changes every few frames) can send the AI in different directions so that it never makes any progress towards the target. There are other options that could have been considered, such as a "follow mode" where the AI retraces the player's steps while doing small local searches to get around dynamic obstacles and back to the player's path.

But too often, path finding just gets used "by default".

Mikko: You can always FIFO the searches so you will at most need one bit vector/search thread. And you could allocate them statically (to avoid fragmentation, etc). But the best way is probably to avoid these 50 K graphs by building hierarchies instead of trying to optimize for them.


ReplyDeleteThe ideal would be to build hierarchies automatically. I've been toying in my head with heuristics for doing that. Such as a bottom-up greedy approach: group the two nodes that minimize the hierarchical search distance (the length of the path found by a hierarchical search using the current set of groups) between all pairs of nodes in the graph. But nothing yet has felt solid enough for me to spend the time implementing it.

>>In the next blog post I will talk a bit about how local navigation is implemented in the BitSquid engine.


ReplyDeleteSorry, but I have not found next post. It is very interesting.

Yes, I got side tracked by other issues. I've learned by now that it is best not to promise what I'm going to write about in the next post ;)


ReplyDeleteLocal navigation is a very interesting issue. But I think I need to think about it a bit more before writing about it.

An interesting article, and I quite agree with many of your points, but I do think you're being a little harsh on A*, possibly in reaction to some bad implementations of A*. Some specific points:








ReplyDelete"A* finds the shortest path, but that is usually not that important."

A* finds the shortest path if its heuristic produces estimated costs that are less than or equal to the actual costs. Increase the heuristic outputs beyond this level and A* loses the ability to find shortest path and turns progressively into a local search. Thus by varying a simple parameter, A* gives you the best of both worlds with a single algorithm.

"To distribute the work evenly, we should use a search algorithm that runs incrementally."

It is perfectly possible to use A* incrementally. Work until you need to make a decision, then pick the current best path from the open set and start following its first segment. To restart, simply discard any items from the open set that don't share the same first segment and carry on. This may of course generate a non-optimal path, but as discussed this isn't usually necessary.

"And it should of course parallelize to make the most use of modern hardware."

I'm not sure that's really necessary, to be honest. I'd rather have an implementation that can handle a high volume of (incrementally-interruptible) pathfinding requests than a parallelized implementation that can handle a single request quickly but which is (necessarily) less efficient at handling a high volume of queries due to the parallelization overheads.

But that's probably an aside - you main point is of course that there's more to it than *just* throwing A* into a system, which is a very good point.

WOW! I Love it...



ReplyDeleteand i thing thats good for you >>

REVIEW FOR YOU Thank you!

"ค้อน ปัด 50 ลป สิงห์ ยื่นซื้อ ไรซ์>> ข่าวฟุตบอล "

ReplyDeleteThis is my blog. Click here.

ReplyDelete4 สูตรแทงบอล สูง ต่ำ เทคนิค วิเคราะห์ บอลสูง บอลต่ำ

This is my blog. Click here.

ReplyDeleteโปรโมชั่น Ufabet พนันออนไลน์

대구출장샵


ReplyDelete대전출장샵

부산출장샵

울산출장샵

정선출장샵

울산출장샵

대구출장샵

부산출장샵

충주출장샵




ReplyDelete청주출장샵

원주출장샵

예산출장샵

원주출장샵

총판출장샵

총판출장샵

Your blog is one of my favorites! This post was especially useful. Thanks for sharing such valuable information.

ReplyDelete