---
title: Creating a 3D Game Engine (Part 5)
url: https://cybereality.com/creating-a-3d-game-engine-part-5/
author: Cybereality
published: '2013-05-21'
source_blog: cybereality » the matrix was a documentary
source_site: https://cybereality.com/
category: graphics
fetched: '2026-04-19'
---

So far I have mostly been talking about plans and theories, not much meat. Today I hope to remedy that with a discussion on main loops. Surely there are tons of different ways a main game loop can function, and I will explain a few of those methods. Keep in mind, I am still developing the architecture for this engine, so anything can change at this point. But this is, at least, the direction I am heading and hopefully it will prove useful as a learning exercise.

The first loop I am going to show is super basic, but should get the job done. Essentially it’s just a few global functions that get called in a while loop. For the sake of illustration I am leaving out the complexity of the Windows message pump you would have in a real application, but you get the idea.

while(running){ handleInput(); physicsTick(); updatePlayer(); processAI(); }

I will be honest. I have shipped more games than I care to admit with naive loops like seen above. Granted, for some simple games a loop like this can actually work OK. But what is wrong with it? Well first off, we have a bunch of global functions. Surely that can’t be good. I also don’t particularly like how the functions don’t seem to follow a standard naming convention, though this isn’t the end of the world. Also, as the game becomes bigger this list of functions can grow out of control. So while it might work, it’s not very pretty.

What I would like to have is some standard way of updating each of these systems, maybe with a function called “update()”. I think this would streamline everything and make it more clear what was happening. So to do this I will create an abstract interface class with a virtual “update()” function, like so:

class IUpdatable { public: virtual void update(void) = 0; };

Then we can define classes for each one of the game elements that need to be updated.

class InputHandler : public IUpdatable { public: virtual void update(void){ DO_WORK }; }; class PhysicsWorld : public IUpdatable { public: virtual void update(void){ DO_WORK }; }; class Player : public IUpdatable { public: virtual void update(void){ DO_WORK }; }; class EnemyAI : public IUpdatable { public: virtual void update(void){ DO_WORK }; };

Once that is setup, we’ll just need to create those elements somewhere above the loop in the same scope.

InputHandler input; PhysicsWorld world; Player player; EnemyAI ai;

Finally we will call the respective “update()” functions from our revised main loop.

while(running){ input.update(); world.update(); player.update(); ai.update(); }

While this is certainly a lot better than before, it can still be improved. What I like is that all the elements are being called in a standard way, the code looks cleaner, and I have removed the global functions. What I don’t like is that it seems there is a lot of repetition calling “update()” four times in a row. Lets see how we can fix that.

One solution is to place those components in an array, and the use a for loop to cycle through the elements. We’ll see how to do that below.

IUpdatable* items[] = {&input, &world, &player, &ai}; int length = sizeof(items)/sizeof(IUpdatable);

Now that we have the pointers in an array, we can run our main loop much more compactly.

while(running){ for(int i = 0; i < length; i++){ items[i]->update(); } }

OK, this is certainly better but I’m still not sure I like it. While it does streamline the update process a bunch, and will definitely come in handy if you are updating dozens of elements, it’s still a bit rigid. Since it’s using an array, that means elements can’t be added or removed dynamically, which is a bummer. Lets see how the loop could be improved with a vector.

First we’ll have to initialize the vector from the same array we were using above.

vector updaters(items, items + length); vector::iterator it;

Now the main loop becomes a little better, and more dynamic.

while(running){ for(it = updaters.begin(); it != updaters.end(); ++it){ (*it)->update(); } }

Still, we have a lot of variables in the global namespace and ideally we would want a class that can encapsulate this logic. We can do just that, and define an “Engine” class. For now it will just hold instances of our engine components, and have it’s own “update()” method. We’ll also want to define a “running()” function, rather than having this global Boolean value. Since this is similar to what’s already been shown, I’ll just post the code for the class below.

class Engine : public IUpdatable { public: InputHandler input; PhysicsWorld world; Player player; EnemyAI ai; vector subsystems; vector::iterator it; Engine(){ IUpdatable* parts[] = {&input, &world, &player, &ai}; int length = sizeof(parts)/sizeof(IUpdatable); subsystems.assign(parts, parts + length); } virtual void update(void){ for(it = subsystems.begin(); it != subsystems.end(); ++it){ (*it)->update(); } } bool running(void){ return true; } };

We can instantiate our class in the main function like so:

Engine engine;

Now here comes the beauty. Our main loop has been reduced to the following:

while(engine.running()){ engine.update(); }

I think you will agree this is far more elegant than the previous attempts, and loads better than the original naive approach. The best part is that the updates can cascade down recursively just like in the Engine class. For example, the EnemyAI component could have a list of enemies that need their update functions called, etc. Seems to be like a robust solution to me. Of course in a real application there may be other things to handle (like I mentioned, the Windows message pump) but this covers the core of the logic. As I get further into creating this engine I will probably refine this architecture as needed, so don’t think this is the best a game loop can get. It’s just where I am at now, and I will continue to post updated code in future episodes of the series. Stay tuned.