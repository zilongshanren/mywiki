---
title: Replay system using Unity
url: https://www.elopezr.com/replay-system-using-unity/
author: Redorav
published: '2014-06-15'
source_blog: The Code Corsair
source_site: http://www.elopezr.com
category: game programming
fetched: '2026-04-13'
---

Unity is an incredible tool for making quality games at a blazing fast pace. However, like all closed systems there are some limitations to how you can extend the engine and one such limitation is developing a good **replay system** for a game. I will talk about two possible approaches and how to solve other issues along the way. The system was devised for a [Match 3 prototype](https://www.elopezr.com/match-3/), but can be applied to any project. There are [commercial solutions ](http://u3d.as/content/soft-rare/ez-replay-manager/1QY)available, but this post is intended for coders.

If the game has been designed with a deterministic outcome in mind, the most essential parts of recording are **input events, delta times **(optional) and **random seeds**. What this means is the only input available to the game will be the players’ actions, the rest should be simulated properly to arrive at the same outcome. Since storing random seeds and loading as appropriate is more or less straightforward, we will focus on the input.

1) The first issue is how to capture and replay input in the least disturbing way possible. If you have used Unity’s Input class, **Input.GetMouseButton(i)** should look familiar. The replay system was added after developing the main mechanics, and we didn’t want to go back and rewrite how the game worked. Such a system should ideally work for future or existing games, and Unity already provides a nice interface that other programmers use. Furthermore, plugins use this interface, and not sticking to it can severely limit your ability to record games.

The solution we arrived at was shadowing Unity’s Input class by creating a new class with the same name and accessing it through the UnityEngine namespace inside of the new class. This allows for conditional routing of Unity’s input, therefore passing recorded values into the Input.GetMouseButtonX functions, and essentially ‘tricking’ the game into thinking it is playing real player input. You can do the same with keys.

1 2 3 4 5 6 7 8 | public class Input { public Vector3 GetMouseButtonDown(int i) { if(recording) return record.position(currentTick, i); else UnityEngine.GetMouseButtonDown(i); } } |

There are many functions and properties to override, it can take time and care to get it all working properly. Once you have this new layer you can create a RecordManager class and start creating methods that connect with the new Input class.

2) The second issue is trickier to get properly working, due to common misconceptions (myself included) about how Unity’s Update loops work. Unity has two different Update loops that serve different purposes, Update and FixedUpdate. Update runs at every frame, whereas **FixedUpdate updates at a fixed, specified time interval. **FixedUpdate has absolutely nothing to do with Update. No rule says that for every Update there should be a FixedUpdate, or that there should be no more than one for every Update.

Let’s explain it with two use cases. For both, the FixedUpdate interval is 0,017 s (~60 fps).

a) Update runs at 60 fps (same as FixedUpdate). The order of updates would be:

1 2 | T1: Update + FixedUpdate T2: Update + FixedUpdate |

1 2 3 4 | T1: Update T2: Update + FixedUpdate T3: Update T4: Update + FixedUpdate |

c) Update runs slower (30 fps). Same rule as above, but 30 = 60/2

1 2 | T1: Update + FixedUpdate + FixedUpdate T2: Update + FixedUpdate + FixedUpdate |

Since FixedUpdate can’t keep up with Update, it updates twice to compensate.

This brings up the following question: where should I record input events, and where should I replay them? How can I replay something I recorded on one computer on another, and have the same output?

The answer to the first question is **record in Update**. It is guaranteed to run in every Unity tick, and doing so in FixedUpdate will cause you to miss input events and mess up your recording. The answer to the second question is a little more open, and depends on how you recorded your data.

One approach is to record the **deltaTime in Update for every Update**, and shadow Unity’s Time class the same way we did with Input to be able to **read a recorded Time.deltaTime** property wherever it’s used. This has two possible issues, namely **precision** (of the deltaTime) and **storage**.

The second approach is to save events and link them to their corresponding FixedUpdate tick, that way you can associate many events to a single tick (if Update goes too fast) or none (if Update goes too slow). With this approach **you can only execute your code in FixedUpdate**, and execute as many times as recorded Updates there are. It’s also important to save the average Update time of the original recording and set it as the FixedUpdate interval. The simulation will not be 100% accurate in that Update times won’t fluctuate as they did in the original recording session, but it is guaranteed to execute the same code.

There is one last setting that’s needed to properly record events, which is set the RecordManager to record **all input at the beginning of every frame**. Unity has a Script Execution Order option under Project Settings where you can set the RecordManager to run before any other script. That way recording and replaying are guaranteed to run in the correct order.

Hello Code Corsair,

Looks like a great article. Any example code for this?

Have a great day!

I love the way things are motivated. Same like Code master do you have example code for this

Hi Avatarum,

Sorry for the late reply, I really need to make wordpress send me e-mails whenever there’s a new comment. Another person also got in contact with me with regards to code. I have some bits and bobs that I never had time to put together, I was actually surprised to get interest in this. My email is redorav gmail. I should be able to at least forward you that email and hopefully I can maybe clean it up and revisit the post.