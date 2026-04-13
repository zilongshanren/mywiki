---
title: 'Question: how to synchronise between the game and render thread?'
url: http://joostdevblog.blogspot.com/2012/03/question-how-to-synchronise-between.html
author: Joost van Dongen
published: '2012-03-23'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

*ask you a question*. I know that quite a few of the visitors of my blog are hardcore programmers, and since I have a complex situation for which I would like to improve the performance, I figured I could ask for advice here! :)

The problem is pretty complex, though, so I figured a short blogpost would be needed to really explain it. In short, this is the question:

**What is the most efficient way to synchronise renderable objects between the game thread and the render thread?**

There are a couple of subtleties you need to know to answer this for our situation, though. Let me start with a scheme that shows the approach to threading in the Ronitech (our in-house multiplatform 2D engine), as we use it in

[Awesomenauts](http://www.awesomenauts.com)on the Xbox 360 and Playstation 3:

![](../../assets/2665bf4e53ba67c0.gif)

This works fine and we managed to get 60fps on console this way. However, the copying phase takes relatively long, so I am still wasting a lot of performance there. Since we will also use the Ronitech in all our future games, improving here will pay off greatly in our future projects.

There are a couple of specific requirements that I have to make this work with the rest of our engine:

- The gameplay thread must be able to modify (and even delete!) all renderable objects. At the same time, the renderer must still be able to render each object how it looked during the
*previous*frame. - Within a single frame, the same object might be rendered to different viewports in different ways. For example, a character might be partially transparent in one viewport and fully visible in another. The game can register itself as a PreViewportRenderListener and thus change objects in between the rendering of two viewports.

So, what alternatives are there to just copying

*all*the relevant data for all visible objects every frame? Or should rendering in a separate thread be set up differently all together? Please comment below if you have interesting ideas for this!

What kind of properties are you copying then? Can't you just have a pointer in every clone to the main object and collect info from it when it's needed. The way you're describing them, makes it sound like their already very dependant on it, so nps to crank that dependancy up, right?


ReplyDeleteOr if you can't change the main object because of the whole concurrent update fase, have a master clone instead.

I'm not sure I know enough about the situation to really help but I'll hazard a suggestion anyway.

ReplyDeleteHow about avoiding copying everything by having the rendering thread(s) use the master copies of the objects while the update thread stores a list of changes to be made to those objects. Then, in the "copy objects" phase these changes are all applied to the master objects. This would also make it easy for the update phase to access the previous frame's state as it wouldn't be modified until the current frame had finished being updated.

I dunno how the performance of a solution like that would compare to brute force copying of the world's objects but it might be worth looking into.

I assume the gameplay thread has more time to spare? In that case can't you just do the copying at the end of the gameplay thread so the synchronisation phase is no more than swapping pointers?

ReplyDeleteDon't copy, just swap the buffers. (double buffering)

ReplyDelete@Thijmen:




ReplyDeleteThe properties are things like position, texture, scale and colour. I cannot just "copy when it is needed", because by the time the render thread is about to render the object, the game thread might already have modified the object for the next frame.

@Patrick:

I was indeed thinking about doing a change-list, but I haven't really figured out how to structure this nicely in code. There are a couple dozen variables and adding an enum to say which variable has been changed (and thus needs to be copied) makes this code a lot of work to maintain. How would you structure that?

@Roel:

Interesting idea! However, surprisingly, the gameplay thread takes longer to update than the render thread, so that won't work.

@Anonymous:

The gameplay thread does not set all properties every frame, so if I would do double buffering and set the position in one frame and not in the next, then I have a problem. Also, the gameplay thread often reads back variables through functions like getPosition and this also needs to be consistent.

@Joost

ReplyDeleteThe only other way I could think of would be to make a list of pointers directly to the objects' fields along with their updated values and the length of the data but that would be pretty hacky, not to mention flying in the face of any nice OOP you're doing.

Actually, come to think of it, it might not be too bad if the objects' setter methods add the changes to the changelist directly so there would still be some measure of data hiding. It would require a bit of a shift in thinking, though.

What about a combination of Patrick's and Anonymous' answer:

















ReplyDeleteSomething like this:

[code]

struct Variable;

struct : Variable

{

mName[2]

mWriteIndex;

mRenderIndex;

mIsNotSwappedMask;

};

Player::setName(const std::rstring& name)

{

mName[mWriteIndex] = name;

addVariable(this);

}

const std::rstring& Player::getName() const

{

// returns always the state information of 1 frame back in time

return mName[mRenderIndex];

}

ChangeList::addVariable(const Variable* variable)

{

mChangeList[mTopIndex] = variable;

mChangeList[mTopIndex]->mIsNotSwappedMask = 1; // index not swapped yet, set to 1

mTopIndex++;

}

Now it is possible that, when you alter a variable multiple times per frame it will be added to the changList multiple times.

But the change list serves merely as an optimization so it isnt that much of a deal if it is added multiple times. The amount of variables

that is modified per frame will probably be slight. The important thing is to avoid an if branche (seeing if it was already added) which is a lot slower than just adding

it perhaps a couple additional times.

At the end of the gameplay frame:

ChangeList::swapIndices()

{

// avoiding IF branches

for (mTopIndex - 1; mTopIndex >= 0; mTopIndex--)

{

Variable* variable = mChangeList[mTopIndex];

mChangeList[mTopIndex]->mRenderIndex = (mChangeList[mTopIndex]->mRenderIndex + (variable->mIsNotSwappedMask & 1)) & 1;

mChangeList[mTopIndex]->mWriteIndex = (mChangeList[mTopIndex]->mWriteIndex + (variable->mIsNotSwappedMask & 1)) & 1;

variable->mIsNotSwappedMask = 0;

}

// mTopIndex is now also immediately ready for the new gameplay frame, no need to set back to 0 ;)

}

[/code]

Optimizations applied:

1. Delta compression (only copy what changed).

2. Lower bandwith, copy only an index instead of the actual data (double buffering)

Als je deze methode toepast, reken ik erop dat ik daar enige dankbaarheid van terug zie op mijn bankrekening :P

I'm not sure what anonymous meant by double buffering, but since memory is not an issue, just keep two copies of all your objects. Then switch back and forth between sets as you render. Basically, you are rendering each set at 30 fps and making two frames of changes to each set, with the two sets one frame apart.


ReplyDeleteThen your rendering code can have a set to itself and the update code has a set, and no problems with collision.

@Bart




ReplyDeleteThat's a good point! You could store all data in pointers and then the changelist is simply a list of pointers to those pointers paired with a pointer to the new data. The "copy" phase could then just delete the old pointer and copy the new one in. In retrospect my idea of copying the actual data seems silly.

i.e. (in pseudocode)

/** Update Phase **/

class Foo {

int *x;

void setX( int *newX ){

changeList.add(&x, newX);

}

}

/** Copy Phase **/

void copy(){

for( change in changeList ){

delete *(change.var);

// delete x

*(change.var) = change.val;

// now x = newX

}

}

With this solution the copy phase runs in O(n) time where n is the number of changes made - the size of the changes and the amount of unchanged data are irrelevant. If a value is written twice in one update phase the latter value will simply be used.

@Marries

Thanks for those articles, they were an interesting read. I can't really see the benefit over a simple changelist, though. In both cases the limiting factor is the "copy" or "output" phase but nulstein takes longer in that phase by processing new values there instead of during the "update" or "input" phase.

@Patrick, your code is not going to be easy to work with.





ReplyDeleteYou can no longer just do: setX( constant_value ).

Furthermore, you delete the data (although u call it pointer) which is very slow and this will also make up for awful fragmentation as the data being deleted is very small.

My solution works without having to adjust the existing functions. Only the implementation will change.

So you can fix the functions one by one, no need for massive refactor at once.

@MichaelG That wont work as Joost already mentioned.

Say a name of a Player is changed in Frame 0 and in Frame 1 but not further more then you end up with two versions. On display you will see a flickering screen of 2 names.

@Bart:


ReplyDeleteHmm, that's an interesting alternative! I will have to have two get() functions for everything, though, since both the render thread and the gameplay thread can call get() and they need to get different answers (previous and current frame).

Also, deleting objects becomes interesting that way, but that shouldn't be too difficult to solve: instead of deleting objects from the gameplay thread, I can just move them to a kill-list until the renderer is done.

It depends whether you actually want the most recent updated version, even in the gameplay thread! Lets say you update 3 characters.



ReplyDelete1. Character1 -> getPositionOfCharacter2

2. Character2 -> updates his own position.

3. Character3 -> getPositionOfCharacter2

Now, Character 1 and 3 have used a different version of Character's 2 position. So even in single threaded, it is always possible you use different versions.

Sure, those kinds of situations are problematic and can easily cause bugs, but that's nothing compared to get() not returning what you just set()!



ReplyDeleteActually, this would become really complex to make work correctly, because I also create temporary objects in the render thread, so I need to handle those correctly as well. Not that that's impossible, but it does get more and more messy...

I think Marries' simpler alternative is also worth a try: lots of objects don't actually change, and their setPosition() is called every frame with the exact same value. I could keep a bool isDirty and only copy data for the object if it actually changed. That might already be an enormous improvement, and remain a lot simpler. :)

I've used the state-mind pattern in our own engine but have to say that it is very hard to maintain due to different objects depending on others. The state-mind pattern requires multiple update passes if an object depends on the state of another object in the same frame. Take a box that updates its position based on another box. When the first box moves the second box also has to move. Using the state mind pattern the second box can only update its mind when the first box updated its state. This requires a little more knowledge of the first box that just its position (we need to know when it updates). Don't get me wrong it works fantastic, but it does require a little more bookkeeping. Anyhow, this is a solution for updating objects in parallel not synchronizing them.



DeleteI think double buffering is the way to go. Simply because the synchronization phase (swapping buffers) is extremely fast. In my opinion Bart's solution is the best one seen so far (Although his example is far from thread-safe). You can even go a step further by wrapping those variables in a template class with a get,set and getRender method or something like that. This allows you to just use SyncType variables for instance and the rest of your code is clean of threading stuff.

I'm interested to see what your final solution will be. :)

Hey Joost,

















ReplyDeleteFirstly, I suspect that this blog post may be a little about getting people commenting and getting traffic to your blog :) I'm certain you could handle this and besides, if you are getting 60fps, I think you wouldn't want to improve performance.

That said, I can't resist commenting, it is too juicy.

On an engine a while ago, I abstracted rendering by "generating" render data per frame (rather than "copying" the entire scene, I "generated" specific data that corresponded to the commands used for rendering.

In concept, this divided logic and rendering:

Logic:

game logic

updating units

offscreen culling

physics

generating frame render data

anything else done on the cpu

Rendering:

calling rendering api functions

This mean't that rendering performance was as high as it could possibly be - the rendering code could execute constantly with no time segment given to logic.

Lets look at the implementation:

Logic:

perform_objects_update();

if(it is time to generate a new frame)

{

cull the scene();

for(each culled object)

{

add_culled_object_render_command_object_to_render_data();

}

send_render_data_to_render_thread();

}

The render data may look something like this:

struct sprite_data

{

sprite_resource* p_sprite;

vec2 position;

};

struct render_data

{

// note the structure of this struct should be based on whatever is fast for rendering

std::vector render_sprites;

}

and on the render thread:

get_newest_render_data();

for(each sprite in render data)

{

call_the_api_using_data();

}

That said, one day I woke up and realized that I didn't work for Epic Games, and did not in fact need the most complex and high performance game engine so now my games just use a linear loop on a single thread and game performance is fine.

For me it is a battle between doing cool programming systems and doing what is the most time effective way to add the next most important feature to the product. It is a tough battle but i am winning at the moment :)

Actually, my normal blogposts get way more traffic and this one, so no, that is not why I wrote this post. This really is a topic I am struggling with. In three player splitscreen, Awesomenauts runs at 30fps and fixing this might have brought it to 60fps. Not that 30fps in three player splitscreen is low, but 60fps does play better. And developing future games will be a lot easier if I can get a 20% framerate bonus here.



DeleteI agree that striving to be Epic Games is in general not a good idea, but this whole topic comes from a real problem that I struggle with. Getting 60fps on Awesomenauts has been a lot of work and solving it here would have made a lot of other difficult optimisations unnecessary.

PS. Blogger marked your post as spam, sorry I missed and it didn't unspam it earlier!

Ah ok! Sorry, I didn't mean to be subversive.




DeleteThe stuff I put above is really what works for me. At my level of ability, keeping it simple helps me later on, and with a subject like this where there are so many solutions, I could spend a huge amount of time on it (and have in the past) so what works for me is to avoid these kinds of tasks. That said, different things work for different people. Chris Sawyer programmed most of transport tycoon and rollercoaster tycoon in x86, so crazy!!!!! but it worked for him.

I think part of the problem here is that there are so many solutions that could work but a perfectly elegant and max speed solution probably doesnt exist. With most profiling, it seems to me it is about establishing where the choke points are. If you are getting the drop on the split screen mode, it must be the culling and rendering that is slowing you down. I think this is significant because when diving render and logic, you want to push as much stuff into the logic thread as possible so that the render thread can be as light as possible. This would give the most balanced loading across threads.

Going back to your earlier blog post on responsiveness, threading could give a greater delay between input and screen feedback depending on how you implement it. I thought I would mention this as I know you care about responsiveness, so this could be a big design factor.

I totally agree that keeping it simple is a good idea. We always try that at Ronimo, but when the profiler tells me I have a problem, I do need to solve it in the end. I didn't start messing around with the multi-threaded rendering until it really became needed with the enormous amounts of objects we have on screen in Awesomenauts. Swords & Soldiers was only a single thread for all normal stuff.



DeleteIn practice, we have so much animation, AI and networking going on in Awesomenauts that the render thread has less work to do than the logic thread. So based on performance measurements on PS3 I actually moved stuff from the logic thread to the render thread, instead of the other way around.

It is absolutely true that this threading adds lag to responsiveness. This threading scheme was necessary for the framerate, though, so I had to make sure other things (like in the controls blogpost) didn't add lag as well. And at 60fps one additional frame of lag is not that much of a problem, as long as it does not become a lot more.

My code is reentrent which is sufficient in this case.

ReplyDeleteGood luck with solving the problems :)

The addVariable method in your code is not reentrent. If the method is interupted before setting the mIsNotSwappedMask it may never be set. However using thread-local storage (and assuming incrementing an int is an atomic operation) solves the problem entirely:



DeleteChangeList::addVariable(const Variable* variable)

{

int topIndex = mTopIndex++;

mChangeList[topIndex] = variable;

mChangeList[topIndex]->mIsNotSwappedMask = 1; // index not swapped yet, set to 1

}

Or am I missing the point entirely?

All write operations are only accessed by the gameplay thread.




ReplyDeleteOnly read operations may be accessed by both.

Adding variables to the change list and swapping indices is done in the gameplay thread.

The render thread awaits the swapping indices function to be done and then starts rendering using the data written one frame in the past by the gameplay thread.

@Joost.

A dirtly flag is an option. The more accurate the better but also more administration. That is, you could keep it per object, per variable (like my suggestion + a change list) or per group of objects or section etc.

I have also had to deal with this problem but not by choice. On some of the mobile devices you don't get a large push buffer by the driver that allows the gpu to be more asynchronous. So swapping the buffer turns into a brutal block.





ReplyDeleteWhat I did was make a higher level push buffer for my objects. When the main thread renders a frame, it allocates a SceneJob from a freelist and blocks until it gets one. Then it calls render on the simulation passing around the SceneJob. All the culling and LOD is done here. A SceneJob can also be loading a texture, model. You can also have a nop job that can be used as a fence.

The RenderSceneJob has arrays of stuff it can render. Stuff like a ModelRec that takes a reference to a model and adds stuff like a matrix. This also allows the scene to be sorted for draw order, states etc.

I am now doing a new game and I'm revisiting this model as to whether it's good or not. For the most part it's successful since all your sync problems pretty much go away. The scene rendering does become kind of static. You can't just render some debug lines here and there.

The only other viable option IMHO would be to double buffer some of the data. Often for AI and other stuff you want a previous position anyway. Not sure what I will do. Will likely Google for a couple of hours and then continue with what I have :)

Hmm, interesting approach! If I understand it correctly, this does not actually spread CPU work to use more cores efficiently, right? So this is specifically useful for solving the problem of a really small renderqueue. Or am I misunderstanding this?

DeleteI would say it does off load work. I have a main game thread and a render thread. The game thread won't block unless it's a few frames ahead of the render thread. I have confirmed this.





DeleteI used this on a game called Tank Recon 3D. Now this isn't a huge AAA game by any means but it's also not a trivial game either.

Keep in mind that you're not pushing around much data. To render a model I use a ModelJob that has a pointer to the shared model resource, an LOD index, a local matrix and color. It's crazy fast. The jobs are in a flat array and I just use numModels++ to allocate. When the scene is rendered I reset by setting numModels to 0.

I have arrays of jobs for static meshes, dynamic models, shadows, particle emitters etc. The rendering is pretty optimal since I set most states once and then rip through a batch of jobs. I also sort by models and only upload vertex buffers as needed. The render thread does very little work and tends to just block on the GPU.

Sure this doesn't meet the goals of making an engine that can do everything but these days I tend to just get things done and ship it. Later I fix some of the stink if I just can't stand it.

Hi there Joost, I'm a Java Developer by trade so this isn't really my area of expertise but all the mechanisms explained here are pretty standard so here's my view...







ReplyDeleteHaving read through all of the suggestions whilst trying to contrive my own, I think personally the isDirty flag seems the way to go before exploring other avenues...

Some of the suggestions here imply performance but drastically undermine the ability to manage the code, one actually throws OO out the window alltogether! There are a few massive changes to your entire design pattern suggested too and to be honest nobody seems too confident.

Speaking from experience if you have something that is intensive, avoiding it when possible is one of the first things I look for if alternative solutions aren't forthcoming or promising. The isDirty flag is a modification to existing code which doesn't break your existing patterns and also addresses one of the most classic bang of buck programming rules when it comes to optimising... don't perform unnecessary operations!

I realise this post is more an opinionated breakdown of what others have said but I figured I'd throw it out there anyway lol.

I'd be most interested to read about what you decide to implement and what kind of results this yields.

Liam

fox@pwnz.co.uk

Yeah, I agree that code maintainability becomes really difficult with some of these ideas. The copying in itself already really deteriorated the clarity of this code, and some of the things mentioned here make it a lot worse. The isDirty is also something that can easily be overlooked, introducing difficult to find graphics bugs when it is forgotten in one specific spot.


DeleteSometimes performance might need that, though. The amount of bandwidth optimisation I did for the networking makes that the most complex and least understandable code I wrote so far, but it did manage to decrease the bandwidth of Awesomenauts massively...

This question has kind of been sitting at the back of my mind since I first read this post and I like a lot of the ideas people have suggested. Here's a possible implementation that's a sort of mish-mash of what I've picked up from the whole discussion:










ReplyDeleteEach entity has three methods: think(), act() and render(). It also has two levels of state. Let's call them mind and body. (bear with the awkward names)

Each tick, every entity's think() method called. think() does as much of the entity's tick as it can, based only on other entities' body state and without changing it's own body state, only it's mind.

Next, every entity act()s. During the act phase it finishes off the last little bit of the tick by changing whatever it wants in its body state but without accessing other entities.

Finally, all the entities are render()ed. The render() method, like think(), can't alter the entity's body state.

The result of these restrictions is that think() and render() can both be safely executed at the same time and as concurrently as you like so every entity can think() regardless of whether any other entities are think()ing or render()ing.

Similarly, all entities can act() concurrently though this has to be done in a separate step to the think()ing and render()ing. (the dreaded copy step)

In other words you have one think() & render() step (update) and one act() step (copy).

The pros of such a setup would be:

* Awesome concurrency

* Very quick copy phase (just the act() methods)

* Strictly object oriented

* Every entity can do as much (or as little) as it wants in each stage (within those restrictions) and it can do it however it wants. No need for change lists or dirty flags unless a particular entity wants to.

And the cons would be:

* Entities can't access each other's current state, only the state at the last tick. (though this probably doesn't matter much as it's how the real world works)

* Every entity has to have a "mind" which is essentially a private changelist

* Others?

What are your thoughts on such an idea?

Structuring it like this sounds like something that would work, although it has the big problem that the act-state is pretty similar to the copy-state in my situation. There is still a phase every frame where synchronisation is stopped and most objects need to be touched. I guess the act-state could be synchronised itself, calling act() on different objects from different threads, but the same goes for my copy-state, which is also multi-threaded itself.




DeleteSo although this sounds interesting, I think you would only gain something here if you could somehow make the act-state do very little work.

Also, note that in the specific situation my post was about, there are a lot of limitations, because the game is already finished and I don't want to change any gameplay logic over this. Your idea would be much more feasible on a new code base, but really difficult to apply to an existing code base.

Finally, the big risk in your approach is that it has extra rules that the developer needs to remember. If the programmer accidentally modifies a renderable object during the think state, then it will be difficult to have a compiler error here. Maybe don't give him access to his renderables in think() at all and pass on his renderables in the call to the act function? Something is needed here to protect against difficult to find multithreading bugs, and the solution seems to make the class structure of the gameplay logic a lot more complex and less free.

Yeah, that's basically the point. I don't see any way around having a copy stage so this would allow it to do the absolute minimum. Each class would only do what it needs to.




DeleteOff the top of my head, I can't think of any great way to have the compiler enforce these principles.

One option would be to replace every class with two classes. The first, a body class with private body state, public getters and the public act() method. The second, a class that inherits from the first and contains private mind state and the think() and render() logic. That way the structure would be enforced by the compiler.

Such a solution would have the benefits of having clearly separate body and mind state and looking and acting familiarly to OO programmers. The downside would be that every class has to become two classes. This might not be too unmanagable if every pair of classes is kept in its own file, though.

As for applying this to an existing codebase, I agree that such a big change in structure would probably be impractical. It could work for a new project though...

I'm going to have to try it out sometime! :)

Late to the party, but it's worth mentioning that any sort of lazy copy, especially a changelist that records pointers to memory locations with changes to be applied, is going to KILL your cache performance. Nothing's worse than randomly jumping around in memory setting values. It might end up being faster than a straight copy, but it might not. Modern processors are AMAZING at things like a pure memcpy, since the access pattern is so predictable. It really depends on how many things end up getting changed from frame to frame. Certainly most entity positions get changed.



ReplyDeleteIn terms of cache performance, your best bet is to split your game entities in to the 'state' and 'mind' mentioned previously, and have everyone's state stored in a single contiguous block of memory. Then you can just copy the state block using a memcpy.

Not great from a software engineering standpoint, though. It forces a lot of uncomfortable class design on you for pretty much every single class, and a fair bit of indirection.

So ... how do you solved it ?

ReplyDeleteI left it as is described in the starting post as no golden solution was presented in the reactions. Some might be better but were too much work to try to see whether they really were.

Delete