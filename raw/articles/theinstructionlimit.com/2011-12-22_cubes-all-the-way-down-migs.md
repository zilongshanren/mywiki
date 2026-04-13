---
title: Cubes All The Way Down @ MIGS
url: https://theinstructionlimit.com/fez-technical-post-mortem
author: Author Renaud Bédard
published: '2011-12-22'
source_blog: The Instruction Limit
source_site: https://theinstructionlimit.com
category: graphics
fetched: '2026-04-13'
---

Back in November 2011, I gave [a talk at the Montréal International Game Summit](http://sijm.ca/2011/msconference/cubes-all-the-way-down-fez-technical-post-mortem) in the Technology track called “Cubes All The Way Down”, where I talked about how FEZ was built, what’s the big modules, the challenges and intricacies of making a tech-heavy indie game from scratch.

It went *okay*.

I was really stressed, a bit unprepared due to FEZ crunch time, and just generally uncomfortable speaking in front of an audience.

I spoke so fast that I finished 15 minutes early and had 30 minutes for questions, which worked great for me because the relaxed setting of a Q&A session meant better flow, better information delivery, I really liked that part. Also I had friends in the front row that kept asking good questions and were generally supportive, so all in all a good experience. :)

I was asked about giving the slides out, so here they are! Unedited.

[It’s Cubes All The Way Down (Powerpoint 2007 PPTX format)](https://theinstructionlimit.com/wp-content/uploads/2011/12/cubes_all_the_way_down_migs_2011_rbedard.pptx) [(PDF format)](https://theinstructionlimit.com/wp-content/uploads/2011/12/cubes_all_the_way_down_migs_2011_rbedard.pdf)


Enjoy!

Would be great if you could also post the presentation in the pdf format.

Just put the link there! Had trouble with the conversion, which is why it took so long. ^_^

Finally had a chance to look at these slides. Very nice, wish I could see the talk! Btw, what kind of structure/class is int3 (the one you use to index into the trile dictionary)? I use XNA’s point sometimes for indexing an arbitrary-sized 2D grid world so I’m interested how you set the int3 up … hash function overrides and such trickery needed, perhaps?

Cheers, Matej (@retronator)

My “int3” is actually called TrileEmplacement for legacy reasons and unreasonable verbosity, but essentially is a struct that holds three ints called X, Y and Z as public fields, has a handful of conversion/casting functions for ease of use, and here’s the hash code :

public override int GetHashCode()

{

return X ^ (Y << 10) ^ (Z << 20); } I just split the hash space in three, nothing fancy. I tried fancier hash functions, modulos and pseudo-random scramblers, but the time spent calculating the hash was greater or equal to the time won by distributing the hashes better. I remember trying caching the hash but the gains weren't significant and it could be dangerous.

See, this is why I say you don’t write enough on your blog. :) Thanks, it’s great to read hands-on experience from another engineer that knows a little more about how things work under the surface.

Best of luck with QA (unless you’re already finished)! Can’t wait until we can finally play this, but at least Indie Game the Movie should be around soon after Sundance so we can see more of you from behind the scenes. :)

Wow, a dict keyed on tile position? That seems like it would have really bad memory locality. Doesn’t that also mean that getting a consecutive row or column of tiles involves a dictionary lookup for each possible cell, and walking the entire view frustum involves doing a lookup for each cell in the frustum? I’m surprised that worked out – I would have assumed you were doing some sort of subdivision (bsp, quadtree, simple grid subdivision, etc). On the other hand, maybe Fez spends most of its CPU time doing other stuff so it doesn’t matter.

Triles are objects that live on the heap, so memory-locality-wise I’m already screwed there. The dictionary just ensures that at least I’m reaching the instances in O(1) time.

I do get a shitton of cache misses, but it’s not affecting the culling performance that much. I’m only culling the whole screen when coming back from a rotation, or when starting a rotation. When the frustum moves, I know which rows/columns to process so it’s pretty quick.

The memory problems show up especially in collision detection. I always meant to look at my options there, but when the game runs smooth and you’ve got better things to do, you just carry on…

So how did the memory problems show up in collisions? Do you use any profiling tools that also show cache misses in memory?

PIX will tell you if you get a significant amount of cache misses, so there’s that. I get warnings constantly while the game is running on the Xbox, and shrug them off.

You can tell that the collision is taking the most CPU time apart from drawing in a CPU performance profiler (ANTS in my case), and since most time is spent fetching instances from the dictionary (or around that code), one can deduce it’s memory related.

My efforts to optimize that was mostly algorithm optimization, e.g. the fastest code is the one that’s never called. It worked out fine.

Thanks for posting this Renaud! It’s interesting to see your workflow and what your job was during the development of FEZ. After hearing about the recent PEGI rating for the game, I have my fingers crossed for a possible February release date! :D

Hey Renaud,

Thanks for sharing the presentation. I would have loved to be there!

It’s very inspiring. Between XNA changing every now and then, the complexity of the game and writing editors, perf tuning, and the list goes on, you had plenty of stuff to deal with. Were you on your own for the development part?

In hindsight, do you think a simple scripting language would have been better, or are you happy with a klik&play-like action editor?

Did you organize your art pipeline beforehand or plugged stuff in when needed? How was the interaction with the end-users of your editors?

Thanks again!

Hey :)

I was alone on the coding part, but design-wise of course it was a dialogue with Phil, if not top-down dictation. He was to use the tools and it’s essentially his game design, so my job was most of the time to find the most efficient/fast/reliable way to do things. Otherwise, brainstorming help came from friends, forums, etc.

Scripting : I would’ve had to implement scripting to begin with, and have a clear distinction between what’s scripted and what’s engine-side. It would’ve made a very different engine, and probably a different game. What’s also to consider is that I would’ve been the one to write all the script anyway, so why not just hardcode it at this point? The current “action” system works great for the game that FEZ has become, but for next projects, sure I’d like to try a more proper approach.

The art pipeline (for triles) was one of the first things we decided on, but we improved upon it halfway into development. I made a Photoshop script for Phil that slices up a PSD into cubemaps to cut down on repetitive work. Geometric sculpting was worked out very early on too, and hasn’t changed much.

There was typically only one (or two) end-users : Phil and me. Sometimes other people would come in and give us a hand, but not for final content and usually for short lengths of time. Having such a small user base allowed me to put undocumented features that we just agreed upon, the UI isn’t very clear for a new user but it doesn’t matter. Less time documenting means more time producing :)

> What’s also to consider is that I would’ve been the one to write all the script anyway, so why not just hardcode it at this point?

Absolutely – making modding possible just to be the only modder is not exactly productive :p

Thanks for the thorough reply. It’s good to have a glimpse of how it all works – not just the pretty pics but also the people behind the scenes. Game dev is serious business, I just have to convince my country now.

Thanks again and take care!