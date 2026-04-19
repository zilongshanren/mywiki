---
title: Learning to teach
url: https://c0de517e.blogspot.com/2016/06/learning-by-teaching.html
published: '2016-06-18'
source_blog: C0DE517E
source_site: https://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

This past couple of months I've been teaching once a week a rendering course at private art school here in Vancouver. It took quite a bit of my time for course preparation (which in turn left this blog dry), but it's a quite nice experience and a small way to contribute to our rendering community, if you can, I wouldn't discourage people into getting involved with teaching.

This is not the first time I held a class, I actually worked for a small professional school in Italy teaching the very basics of computers while I was going to university. But it's the first time I teach rendering in a systematic way, outside sporadic presentations at work and conferences.

So, still lots to learn...

**What to teach?**

The first obstacle actually is to decide what to teach. I had a curriculum for this course as it was taught in previous years, it went through the motions of building an engine in OpenGL, and from what I can tell was fairly extensive, albeit a bit oldschool.

I decided pretty early on to scrap it as I didn't think I could provide enough value that way.

I have to premise that this course takes place over 7x3=21 hours, and it's part of what I imagine is a very intense, packed year of courses in game programming.

It's one of the last courses that the students take, so there is an expectation of a certain level of proficiency with programming and math (I don't cover linear algebra, for example). So you really have to pick your battles and fight for student's attention.

It might be my own bias (as I started programming extremely young and went on towards more theoretical studies in my higher education), but I still think that APIs and frameworks can (and probably should) be self-learned. These are not complicated topics, and while you might pick some bad advice if you mindlessly accept everything the web throws at you, I didn't think going through such things would be the best use of (rather limited) time.

Ok, so I started with a clean slate. What now? This is truly challenging. You can easily talk to people at work, on in a conference, when you have a quite precise idea of what can be assumed to be "common knowledge". But here? Not so much.

So my first decision was to keep it agile... I had from the get go a rough conceptual plan of how to structure the seven lessons and how they could relate to each other, and I discussed it with the head of the faculty, but I did everything one lesson at a time, with a good dose of improvisation.

This is my strategy. I would think and jot down notes (pretty much as I do when I have some thoughts that I think might one day go on the blog...) on where I wanted to go with a lesson, starting with the overall objective (what I wanted the students to achieve).

Then, the day before I would scramble and start laying down some slides, trying to keep them minimal (which is against my instincts), I just make sure I have enough supporting material, diagrams, illustrations, to cover what I wanted.

I post the lesson materials online after the class, by actually pruning out things I didn't end up covering, writing a summary to cover the main points of the lesson and giving links to further resources.

The way I tried to adapt is to slightly over-prepare. Not as in to be very prepared and rehearsed (I don't rehearse), but to have a good amount of options for the class, as it's easier to cut corners in class than to have to scramble to find materials that you didn't expect to need. I never walk in the class thinking that I -have- to go through everything, and I don't have the lesson after the one I'm teaching prepared at all, so I can always adjust.

**How to assess?**

Improvising (to an extent) the lessons gives the freedom to adapt, but you can't adapt if you don't have the pulse of how things are going. And this is probably the hardest thing, ever. It's especially hard when you are very versed in a field, because you totally lose sight of what means not to understand certain concepts.

The more basic the course the harder the task. If you ever teach an introductory class to programming, and have your students problem-solve, you'll see what I mean. It's actually hard to articulate why certain things are solved in a certain way, when for your brain it's just obviously what you need to do...

I'm not great at this yet actually. I waited with anticipation the student's solutions for my first assignment, because I had not a solid idea of it was going to be trivial or daunting, and if really things where coming through (they ended up doing great). Assignments are for teachers! I really don't care about assigning grades, I care about getting feedback!

That said, a few things I can share.

First. Generic "checkpoints" are worse than useless. Asking to an audience how things are going, whenever things are understood, or to ask questions freely, is at best a waste of time, and at worst a way to get a false sense of confidence. Questions have to be real.

Problem solving in class is great. I tried to mix problem solving with in-class assignments, and the reason I think you need both is that if you do only questions you risk engaging always the same people (and pointed questions are a bit more aggressive), while assignments let you walk through desks and see how people are doing individually.

Moreover, as this was a very intensive course, I could not expect really a lot of at-home study from the students (my class ends at 21:30!), and I think working in class goes well with such programs because you need to have the time to come up with solutions by your own, and practice, so if you can't do it at home, at least some degree of that was done during the class itself.

Arguably all the real learning happens not because one memorizes a lesson as a teacher taught it, but by practicing and thinking hard enough that the underlying concepts start to become apparent.


Finally, just asking for guesses and speculations before revealing the next bit of information also just helps keeping people engaged and in general, awake!

Finally, just asking for guesses and speculations before revealing the next bit of information also just helps keeping people engaged and in general, awake!

**The course.**

A few people after learning that I was trying this asked for the course program. I can't share the course materials themselves, both due to contractual restrictions and because they are not polished enough to be comprehensible without me explaining them, but I will go through what ended up being my ideas for the lessons (keeping in mind that if I am to do this again, I will probably change a lot).

Lesson 1: Introduction. My background, how I did things and why that doesn't matter. The course objectives: giving a basic understanding of the field to facilitate further study and practical, hand-on tinkering with GPUs and shaders. Introduction to the "rendering problem". Rendering in a videogame company, what it means to be a rendering engineer, what are the problems we face (spoiler alert: tech is the easier part).

Lesson 2: What's a GPU? Starting from a CPU (serial execution) going towards a GPU (latency, hiding it with data-parallel work...). Going from the rendering equation to rasterization: visibility and shading. Some hand-on time with executing kernels on the GPU: ShaderToy.

Lesson 3: Going from data-parallel processing to 3d scenes. What goes on when we draw an object? Vertex shaders, pixel shaders. Tinkering in Unity.

Lesson 4: "Advanced" shading. Texturing, projections, UV mapping. Some fun examples (reflection mapping with pre-integrated cubemaps in Unity). "Advanced" lighting and back to the rendering equation. Fundamentals of PBR.

Lesson 5: Going past a single draw. Engine and (generic) rendering API concepts. API: resource creation (memory), binding of state (registers), draws -> command buffer. Engine: visibility and sorting. Rendering algorithms: shadow mapping, post-effects, forward and deferred rendering.

Lesson 6: DirectX 11 API in-class "live coding". I downloaded SharpDX (an DX9-10-11-12 C# wrapper) and we went from drawing a single 2D triangle (the "hello world" of rendering) to drawing a 3D quad.

Lesson 7. I haven't actually taught this yet, but I settled now with the idea of going through an actual contemporary game, showing art and rendering choices, workflows, and more advanced rendering algorithms.



**Closing remarks.**

Teaching gives us an unique perspective we don't have writing articles or speaking at conferences. We can see (if we pay attention) what people understand from our words, and we can see if we are boring or engaging. I still have a lot to improve. Especially narrowing down topics is hard! Creating something truly beautiful and to the point.

To a degree I think trying to squeeze too much into a lesson (or as I do in this blog, an article), responds to the same urges that make programmer over-generalize: being concerned about covering all the possible bases even if it comes at a detriment to the overall quality. I'm aggressively against these practices in code, but still not great at exercise the same restraint in lectures.

So, I'd better stop here!

## 3 comments:

Great read, thanks for writing this up!

> Assignments are for teachers! I really don't care about assigning grades, I care about getting feedback!





I'm glad this is working for you. In my case, I teach first year college students on introduction to programming. I find that assignments weren't good metrics for feedback since I had students who copies from other people. Its a tribal practice (I help you, you help me), but it doesn't help me adjust my lessons.

That said, I found that my best feedback are during quizzes and exams. After getting their personalized questions (to discourage cheating and copy-pasting), the entire class becomes quiet as they work on the problems. Later, I'll hear an exclamation that they solved it, and I let them off early. Both to prevent sharing insights (until after the quiz), and to lessen the number of people at the end of the time slot.

A few minutes before the bell rings, I'll sit next to each student (starting from the weakest) and pair program the solution, letting the student explain what they have in mind and gently giving hints.

You mentioned in your post that you are teaching self-motivated students, so my story may not be relevant to your class. But I just want to share it because your post was interesting and relevant to my interest. I would like to hear more on your insights in education. :)

You're right, there is certainly some copying going on, but that also kinda "helps" me. If I see lots of people doing so I'm probably not doing the best job. But yes, being active in class, asking questions, making personalized work, that is all much better. Maybe next time I'll work some way of doing personalized (to some degree) assignments.



This though is a very "intensive" class, so I have to balance the amount of time I can dedicate to that versus going on with the program, that's the main issue (and a thing I don't really love). Maybe next time I'll cut down the program and spend more time on less topics. We'll see!

But thanks for the comment!

Post a Comment