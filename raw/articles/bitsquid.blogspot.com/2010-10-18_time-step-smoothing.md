---
title: Time Step Smoothing
url: https://bitsquid.blogspot.com/2010/10/time-step-smoothing.html
author: Niklas
published: '2010-10-18'
source_blog: 'bitsquid: development blog'
source_site: https://bitsquid.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

float dt = elapsed_time(); dt = filter(dt); update_game(dt);

This assumes of course that you are using a variable time step. A fixed time step is always constant and doesn't need smoothing.

Some people will say that you should always use a fixed time step, and there is a lot of merit to that. A stable frame rate always looks better and with a fixed time step the gameplay code behaves more deterministically and is easier to test. You can avoid a whole class of bugs that "only appear when the frame rate drops below 20 Hz".

But there are situations where using a fixed frame rate might not be possible. For example if your game is dynamic and player driven, the player can always create situations when it will drop below 30 fps (for example, by gathering all the physics objects in the same place or aggroing all the enemies on the level). If you are using a fixed time step, this will force the game into slow motion, which may not be acceptable.

On the PC you have to deal with a wide range of hardware. From the über-gamer that wants her million dollar rig to run the game in 250 fps (even though the monitor only refreshes at 90 Hz) to the poor min spec user who hopes that he can at least get the game to boot and chug along at 15 fps. It is hard to satisfy both customers without using a variable time step.

The BitSquid engine does not dictate a time step policy, that is entirely up to the game. You can use fixed, variable, smoothed or whatever else fits your game.

So, why am I arguing for smoothing variable time steps? A basic update loop without time smoothing looks something like this:

float dt = elapsed_time(); update_game(dt);

Each frame, we measure the time that has elapsed and use that to advance the game timer.

This seems straight forward enough. Every frame we advance the game clock by the time that has elapsed since the last frame. Even if the time step oscillates you would expect this to result in objects moving in a smooth and natural manner:

Here the dots represents the times (x-axis) at which we sample an object's position (y-axis). As you can see the samples result in a straight line for objects moving at a constant velocity, even though the time steps vary. All seems well.

Except this graph doesn't tell the entire truth. The time shown in this graph is the time when we start simulating a frame, not when that frame is drawn on screen. For each frame we simulate, there is an amount of latency from the point when we start simulating the frame until it is drawn. In fact, the variation in that latency is what accounts for the varying elapsed times that we measure. (Well not entirely, there can be GPU latency that doesn't show up in the delta time, but for the sake of simplicity, let's assume that the latency of the current frame is the delta time we measure in the next frame.)

If the take the latency into account and offset each time value in the graph above with the latency (the elapsed time of the next frame), we get a truer representation of what the player actually sees in the game:

Oops, the line is no longer straight and there is a good chance that the user will notice this as jerky motion.

If we could predict perfectly what the latency of the next frame would be, we could use that rather than the elapsed time of the last frame to advance our timers. This would compensate perfectly for the latency and the user would again see a straight line.

Unfortunately, perfectly predicting how long the next frame will take to simulate and render is impossible. But we can make a guess and that is one of the goals of our time step filter:

- To make a better guess of how long it will take to update and draw the next frame.

Here is the same graph again, but here we have smoothed the time step that we use to evaluate the object's position.

As you can see, we get a straighter line than we got by using the "raw" variable time steps.

Can we do anything to improve the prediction even further? Yes, if we know more about the data we are predicting. For example, on the PC, you can get occasional "glitch" frames with very long update times if you get interrupted by other processes. If you are using a straight mean, any time you encounter such a glitch frame you will predict that the next few frames will also take very long to update. But the glitch frame was an anomaly. You will get a better predictor by ignoring such outliers when you calculate the mean.

Another pattern in the frame rate that is quite common is a zig-zag pattern where the game oscillates between two different frame rates:

You could make a predictor for this. The predictor could detect if there is a strong correlation between the delta times for even and odd frames and if so, it could use only the even/odd frames to calculate the mean.

But I don't recommend doing that. For two reasons. First, the zig-zag pattern is usually a result of a bad setup in the engine (or, if you are unfortunate, in the driver). It is better to fix that problem and get rid of the oscillations than to work around them. Second, heavily oscillating time steps, which you would get if you tried to follow the zig-zag pattern, tend to make gameplay code behave badly.

So this gives us a second goal of time step filtering:

- Keep the time step reasonably stable from frame to frame.

s = s + v*dt

Yes, it is easy to make the update code for a single object frame rate independent in this manner. But once you start to have complex interactions between multiple objects, it gets a lot more difficult.

An example: Suppose you want a camera to follow behind a moving object, but you don't want it to be completely stiff, you want some smoothness to it, like maybe lerping it to the right position, or using a dampened spring. Now try to write that in a completely time step independent manner. I.e., an oscillation in the time step should not cause the camera to oscillate with respect to the object it is following.

Not so easy.

Game play code faces many similar issues. With 20+ game play programmers banging a way at the code base you can be quite certain that there are several places where oscillations in the time step lead to badly looking oscillating visuals in the game. And the best way to prevent that, in my opinion, is to smooth the time step so that it doesn't oscillate.

In summary, this is our default method for time step smoothing in the BitSquid engine (though as I said above, you are of course free to use whatever time step you want):

- Keep a history of the time step for the last 11 frames.
- Throw away the outliers, the two highest and the two lowest values.
- Calculate the mean of the remaining 7 values.
- Lerp from the time step for the last frame to the calculated mean (adding more smoothness)

Here is an example of the filter in action. The yellow line in this graph shows the raw time step. The red line is the smoothed time step.

One last thing to mention. This calculation can cause your game clock to drift from the world clock. If you need them to be synchronized (for network play for example) you need to keep track of your "time debt" -- i.e., how far your clock has drifted from the world clock and "pay off" that debt over a number of frames by increasing or decreasing your time step, until you are back at a synchronized state.

Nice post. I might try this.


ReplyDeleteHowever, I believe you've made a slight typo: 11 - (2 + 2) does not equal 9.

Ah, you are correct of course. I have fixed it.

ReplyDeleteThis comment has been removed by the author.

ReplyDeleteGreat post Niklas!

ReplyDeleteI had some fun in our last game dealing with frame time and GPU presentation time. To avoid screen tearing, we need to lock the framebuffer while it's being presented to the display hardware for the whole duration of the vsync interval. It can be done explicitly by the engine or in the driver. The engine might have a new buffer ready by the time the current vsync is done, or not. When the game can't maintain a steady rate of updates, triple buffering can be used to ensure both that there's a new buffer available for the renderer and that the buffer already presented is left untouched. This adds a new layer of uncertainty in the determination of the duration the frame. It's not uncommon that a frame prepared to last 33ms ends up being displayed 16ms, while the next frame prepared to last 16ms ends up being displayed 33ms. It's easy to make that happen if the graphics rendering time is used as game update step increment which a lot of games tend to do. Your description of what happens next was spot on. Trying to account for that is really really hard even on a controlled environment like a console.

I experimented with multiple ideas on God of War 3. The first thing to know is that our PPU, SPUs and RSX had a relatively lose synchronization between each other, they could each slide by 16ms easily. It allowed for some cost amortization. So our CPU time is pretty much independent of our graphics time.

And that's exactly the big secret to the relative smoothness of the God of War 3 framerate, despite of being triple buffered and vsync locked. We intentionally used the unfiltered CPU frame duration as animation increment. It was varying wildly from frame to frame, sometimes by 2, 4 or 8ms even. This is completely counterintuitive and should have resulted in a completely wild animation on screen. But I think it gave us a random distribution of errors, which somehow cancelled out better the "zigzag" GPU presentation rate for which we can't do anything about. As you pointed out, it is not so random, yet next to impossible to predict. Averaging our CPU time perfectly was alright, but somehow not as good as having this random distribution of errors. I thought I'd mention it, it was a fun anecdote and is worth a try :)

Yes, it's a tricky thing. Especially since the "smoothness" or "jerkiness" is really hard to quantify. There is not much you can do except to play the game and see what "feels best".



ReplyDeleteI should probably add that this entire article is an after-the-fact-rationalization. I'd noticed that our games felt better with a little time step smoothing and then I sat down and thought about why that would be so.

So now you have to write an article explaining why GoW3 works better with unfiltered time steps :)

Hey Niklas, I know this blog is old but I absolutely love it! I ended up devoting the last month straight to logic update and time smoothing debugging so it was a joy to see this (I almost thought it was some kind of hallucination) I'm still having some troubles though. Is there any place you know of for more info like this?


ReplyDeleteI tried implementing your BitSquid time smoothing method in Unity and so far I'm not having much luck :(

I forgot to ask:



ReplyDeleteWhat kind of lerping do you do between the timestep and mean timestep and how do you keep track of time debt?

I'm trying to develop a good method to smoothly pay the debt without just nullifying all the smoothing I've done so far.

No sorry, I don't know any other place to find out information, I'm just writing down what I have thought about for myself.










ReplyDeleteFor lerping I just use a general lerp, like:

step = p*mean_timestep + (1-p)*last_timestep

Where p is the weight of this timestep... a value of p=0.2 is perhaps good, but all this is experimental anyway.

Each frame I add to the time debt like this:

debt += actual_time_elapsed - time_step_taken;

So when ever I take a smaller time step than the elapsed, I acquire debt and I pay it back when I take larger timestep.

I pay back the debt by adding some fraction of it to the timestep every frame:

time_step_to_take += f * debt;

Here maybe f=0.1, depending on how quickly you want to pay back your debt. Again, you need to experiment.

You could also use a moving average to implement the lowpass filter(especially if using integer times)



ReplyDeleteon each frame, you remove a small portion of a running mean, and add on the same portion from the new value(for instance, remove 1/8th from the current value, and add on 1/8th of the new value)

For doing the time debt and removing the outliers, you could change it to a weighted moving average(where the weighting is determined by time debt and the delta between the mean and current value).

Yes, there are many different ways of doing this, and hard to say what is right, since it depends on how you want the game to FEEL. In the BitSquid Tech we have a function set_time_step_policy() that gives detailed control over exactly how the time step is smoothed.

ReplyDeleteI've given this a lot of thought, and delta time is fundamentally a flawed concept because information about how long the previous frame took isn't useful in determining how long the current frame will take. No matter how much you smooth it. You are correct that fixed time is better but you still face the problem of behaviour when that time isn't met being undefined.



ReplyDeleteThe solution that I've dreamed up is this: predetermine frametimes. You set a target for how long a frame is going to take before generating it, and ensure the frame takes exactly that long. Mainly you look at how close the previous frame was to overshooting and increase the target frametime by some threshold. Likewise you would decrease the target frametime if you have too much wasted time. This still leaves unexpected spikes however, but you can deal with those using a timer based interrupt that enforces the target frametime even if the frame overshoots. It would cause tearing but the time domain is completely preserved in all cases.

You could also maybe do some sort of dynamic quality adjustments based on performance estimates but that's a little more advanced and maybe not desirable.

Stardust Boutique is a Jovani prom dresses company. If you are looking for a prom dress, we are a Jovani dress store and stockist supplying UK, USA, Canada, Australia, internationally.We stock all kinds of Jovani if you want a Jovani prom dresses, Jovani short dress, Jovani evening dress, Jovani pageant dress, jvn prom dress, jvn short dress and pageant dresses.

ReplyDelete

ReplyDeletecheck gamehackerapk.info

Looking for best game hacking apps for Android 2019 with no root access required? check out these android game hackers without or no root access required.

ppsspp ios games

ReplyDeletePPSSPP Gold APK:- Emulation is a very excellent strategy in the tech world to battle against any obsolescence, emulating apps and games have become less

an internet connection. It ensure comfort Bsnl speedtest.

ReplyDeletebroadband speed test bsnl

WOW! I Love it...



ReplyDeleteand i thing thats good for you >>

LOVE TATTOO Thank you!

google 1839

ReplyDeletegoogle 1840

google 1841

google 1842

google 1843

google 1844

This is an informative post and it's very useful and informative. So, I want to thank you for the effort you put into writing this article. Here are some articles about the How to Get Better at Using a Mouse. Check out my latest post on Computer Mouse Tips. Please visit my site as well and let me know what you think.


ReplyDeleteThank you, for publishing this post. I hope we will get a more useful post like this in future from you. Image Editing Service that consists of for Image Clipping Path Service, White Background for Image, Shadow | Reflection, Masking, Color Adjustment, Coloring, Mannequin, Retouching, Jewelry Image Editing, Product Image Editing, Image Cropping | Resizing all types image editing service


ReplyDelete