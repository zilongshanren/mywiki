---
title: Monitoring your game
url: https://bitsquid.blogspot.com/2011/05/monitoring-your-game.html
author: Niklas
published: '2011-05-26'
source_blog: 'bitsquid: development blog'
source_site: https://bitsquid.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

*see*with such tools. I'm thinking of things like frame rate hitches, animation glitches and camera stutters. You can't put a breakpoint on the glitch because what constitutes a glitch is only defined in relation to what happened in the frame before or what will happen in the next frame. And even if you are able to break exactly when the glitch occurs, you might not be able to tell what is going on from the call stack.

In these situations, some way of monitoring and visualizing your game's behavior can be invaluable. Indeed, if we graph the delta time for each frame, the hitches stand out clear as day.

*Delta-time graph with frame rate drops.*

A graph like this opens up many new ways of attacking glitch bugs. You can play the game with the graph displayed and try to see what game actions trigger the glitches. Do they happen when a certain enemy is spawned? When a particular weapon is fired? Another approach is to draw the total frame time together with the time spent in all the different subsystems. This immediately shows you which subsystem is causing the frame rate to spike. You can constrain the problem further by graphing the time spent in narrower and narrower profiler scopes.

Visualization tools like these can help with many other issues as well. Want to find out where a weird camera stutter comes from? Plot the camera position, the position of its look-at target and any other variables that may influence its behavior to pin down the source of the problem. Draw a

[graph representing your memory fragmentation](http://altdevblogaday.org/2011/05/17/a-birds-eye-view-of-your-memory-map/)to find problematic allocations and get an overall feeling for how bad the situation is. Does something look slightly off with the animations? Graph the bone rotations to make sure that you don't have any vibrations or discontinuities. Graph your network usage to make sure you stay below the bandwidth cap.

*Rotation of a bone during a jump animation.*

When you study your game in this way, you will most likely learn things that surprise you. Games are highly complex systems built by a large number of people over a long period of time. As all complex systems they show emergent behavior. You can be quite certain that at least someone has done at least done something that is

*completely unexpected and totally weird*. You can't hope to discover these things using just a bottom-up approach. There is too much code and too much data. Instead you must study your game as if it was an alien organism. Prod it and see how it reacts. Keep the graphs on screen and make sure that they look sane.

There are many different kinds of data that can be interesting and many ways of visualizing them - graphs, bars, charts, etc. But in all cases the pattern is pretty much the same. We have some data that we record from the game and then we have a visualizer that takes this data and draws it in some interesting way. Schematically, we can represent it like this:

*Basic monitoring system schematic.*

I will refine this picture shortly, but first lets do a little data-oriented design and ask ourselves how we can best store and process this data.

If you have read any of my earlier blog posts you will know that I'm a fan of big dumb continuous memory buffers and data structures that look like "file formats for memory". And this approach works perfectly for this problem. We can just store the data as a big block of concatenated structs, where each struct represents some recorded data. We begin each record with an enum specifying the type of recorded event and follow that with a variable sized struct with data for that particular event.

*Data buffer layout.*

The event types might be things such as ENTER_PROFILER_SCOPE, LEAVE_PROFILER_SCOPE, ALLOCATE_MEMORY, FREE_MEMORY, RECORD_GLOBAL_FLOAT, etc.

RECORD_GLOBAL_FLOAT is the event type used for all kinds of data that we want to draw in graphs. We record the data with calls like these:

```
record_global_float("application.delta_time", dt);
record_global_float("application.frame_rate", 1.0f / dt);
```

The corresponding data struct is just:

```
struct RecordGlobalFloatEvent {
const char *name;
float value;
};
```

Note that there is an interesting little trick being used here. When we record the events, we just record the string

*pointers*, not the complete string data. This saves memory, makes the struct fixed size and gives us faster string compares. This works because

*record_global_float()*is called with static string data that is always at the same address and kept in memory throughout the lifetime of the application. (In the rare case where you want to call

*record_global_float()*with a dynamic string, you must allocate a copy of that string at some permanent location, i.e. do a form of

[string interning](http://en.wikipedia.org/wiki/String_interning).)

Now, let's refine the picture slightly. There is a problem with recording all data to a single memory buffer and that is multithreading. If all threads record their data to the same memory buffer then we need lots of mutex locking to make sure they don't step on each other's toes.

We might also want to add support for some kind of off-line (i.e., not in-game) visualization. Off-line visualizers can take advantage of the full power of your development PC to implement more powerful visualization algorithms. And since they have near unlimited memory, they can record the entire data history so that you can explore it back and forth after the game session has ended.

With these refinements our monitoring system now looks like this:

*Advanced monitoring system schematic.*

Each thread has a small TLS (thread-local-storage) cache with 64 K or so of debug memory where it records its events. When the cache gets full or we reach the end of the frame, the thread acquires the lock to the global event buffer and flushes its data there.

The active on-line visualizers process the events in the buffer and visualize them. Simulatenously, we send the data over TCP so that it can be processed by any off-line visualizers. In the process we consume the buffer data and the buffer can be filled with new data from the threads.

(We allocate all the buffers we use on a special debug heap, so that we separate the allocations which we only do for debugging purposes from the allocations done by the main game.)

Recording float data requires just a few lines of code.

```
enum RECORD_GLOBAL_FLOAT_EVENT = 17;
enum THREAD_BUFFER_SIZE = 64*1024;
__thread char *_thread_buffer;
__thread unsigned _thread_buffer_count;
inline void record_global_float(const char *name, float value)
{
if (_thread_buffer_count + 12 > THREAD_BUFFER_SIZE)
flush_thread_buffer();
char *p = _thread_buffer + _thread_buffer_count
*(unsigned *)p = GLOBAL_FLOAT;
*(RecordGlobalFloatEvent *)(p+4).name = name;
*(RecordGlobalFloatEvent *)(p+4).value = value;
thread_buffer_count += 12;
}
```

When you have the data, writing the graph visualizer is not much work. Just save the data over a couple of frames and plot it using a line drawer.

In the BitSquid engine, we also expose all the data recording functions to Lua scripting. This makes it possible to dynamically create graphs for all kinds of data while the game is running.

As an example of this, a couple of days ago a game programmer suspected that some problematic behavior was caused by a low update frequency in the mouse driver. We quickly bashed out a couple of lines in the game console to produce a graph of the mouse data and could immediately confirm that this indeed was the case:

```
Core.Debug.add_updator(
function ()
Profiler.record_statistics("mouse", Mouse.axis(0))
end
)
graph make mousegraph
graph add_vector3 mousegraph mouse
graph range mousegraph -20 20
```

*Graph of mouse input showing frames with no input.*

Do you try to preserve the temporal order between events recorded by different threads during the same frame?

ReplyDeleteNot in general, but for the events where we care about that (e.g., profiler scopes) we record a timestamp (QueryPerformanceCounter, rdtsc or similar) together with the event data so that we can sort the events later.

ReplyDeleteThis comment has been removed by the author.

ReplyDeleteThe part I am having trouble with when trying to implement this is how to handle processing events.



ReplyDeleteHow can you make a process that only handles SOME of the event types? After it processes the event, you need to delete it in some way so it is not processed again, but won't that leave holes in the "big block of memory" used to hold events?

What happens if you have more events in your queue than you have space for? Does it just drop them so you lose events? Do you loop around and start overwriting earlier events? How does the processing system know you looped around, know to skip over these holes, ect, ect.

I see no need for deleting events that are processed. The way I see it all readers get access to the full stream. They read the stuff they are interested in and skip over the other stuff.



ReplyDeleteIf you have events that CAN be processed by multiple subsystems but SHOULD only be processed by one of those, you will need some coordination between the subsystems. I would do that by having a master system that read the events and sent them to the "right" subsystem for processing.

The event buffers are reset every frame. They are stored in a vector so they grow as needed.

Thanks for you reply, it helped me a lot. I absolutely love your blog by the way. :)



ReplyDelete"I see no need for deleting events that are processed... The event buffers are reset every frame. They are stored in a vector so they grow as needed."

Aah, these were some major pieces that weren't clicking with me when I initially read your article. That actually makes a lot more sense now, although it then requires all the "event generating" processes to run before the "event processing" processes.

"...you will need some coordination between the subsystems. I would do that by having a master system that read the events and sent them to the "right" subsystem for processing."

So, each individual subsystem would have an individual event buffer that the master system forwarded the appropriate events to?

Each system has a buffer for "outgoing" events polled by a higher level system. That also takes care of the synchronization issues, because the higher level system knows when the low level system is "done" and it can poll its events.


ReplyDeleteThere are typically no buffers for "incoming" events. For that I just use function calls because that is a lot easier to work with. (The system might of course put those function calls in a queue on the "inside" if it needs to.)

I reply to a 3 year old article, sorry about that, but I was reading through it lately, and I totally love the method (everything can be simply and elegantly fixed by a chunk of raw memory =D)




ReplyDeleteBut I have a little question, concerning the string pointer. The trick is pretty sweet and clever, but it work only for in-application visualizer that have access to that memory? When sending the data buffer over TCP/IP to a connected visualizer, you need to send the whole string no?

So how to you fix that? Going through the buffer, copying every string to a big chunk of memory, assigning the pointer to an offset in that chunk, and sending it along the data buffer? Appending at the end of the data buffer the string? (but you then need to stock somewhere the offset to that particular string)...In every ways, you have to do a parsing of the buffer once to handle those string before sending it to the visualizer, re-parsing it there...

I fail to say how the trick is carried over networking...

Whenever I encounter a new string pointer, I record it in a separate buffer, storing the pointer and the string value, i.e.: something like:





ReplyDelete0x40ff7318 | "application.delta_time"

The off-line tool can use these messages to build a table that translates string pointers to string values. I use a hash to record already-encountered string pointers, so I don't have to send them more than once to the offline tools.

Your blog always provides such valuable insights. I learn something new every time I read it!

ReplyDelete