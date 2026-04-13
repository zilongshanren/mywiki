---
title: Objectively comparing Unity and Unreal Engine
url: https://gametorrahod.com/objectively-comparing-unity-and-unreal-engine/
author: Sirawat Pitaksarit
published: '2019-01-16'
source_blog: Game Torrahod
source_site: https://gametorrahod.com/
category: game programming
fetched: '2026-04-13'
---

I have been wanting to be able to objectively compare feature parity between different engines for sometimes. Most devs I encountered are too “cultist”, worshipping only their own is not enough but must try to obliterate the other side.. or just simply throw this line “try it and you’ll know why it is better” rather than addressing a specific advantage.

I have experience in Unity for 6–8 years, while Unreal Engine is just started around January 2019. It will come in handy when I see things in Unreal Engine that is sorely missing in Unity, or just recently added but in preview status, or in a development road, etc.

**This article is not for Unreal Engine user**, because I did not spend time explaining Unity terms. Unity user will be able to follow because you are just as new to Unreal as me while knowing what’s available in Unity.

**This article is in-progress. **Because I can’t know Unreal throughly to judge objectively overnight. It will probably takes years to complete and make a completely fair judgement.

**This article is biased towards bad stuff in Unity.** Because I already know what’s not so good in Unity side but not so much on UE side. Also I notice something that generally UE user are very loyal to the engine and try to convert Unity users, while Unity users actively trash talking their own engine.. I think I am becoming one of them.

How I get used to Unreal will be via smaller side projects.

I will not provide verdict like who wins and scores on each aspect like those phone review websites either, I don’t want you to be “too long didn’t read” on stuff.

### Changelog

- 28/08/2019 : Practicality of animation system
- 22/10/2019 : Cons of Unity packages added. Unity ECS updated. A new section called "naysayer not welcome".
- 23/10/2019 : Added Netcode section based on Unite Copenhagen talk. Better introduction to DOTS section. Added Visual Effects section.
- 25/10/2019 : Packages section rewritten.
- 27/10/2019 : Added UI design section.
- 25/07/2020 : Add additional comments section at the end, add section about QA brickwall, update UE's more friendly revenue sharing model.

### Duplicates / outdates

I add things to different sections as I learn over the years and I may not realize I have already said it somewhere. When I have time to re-read I maybe able to remove duplicates, but if you found them please put up with that. Also something like "previously mentioned" may not exist anymore when I edit out something and forgot that the next topic has reference to it. (Null reference exception IRL)

The same for outdated section but I usually say Unity version along with it, so if it is kinda old compared to the current date then maybe trust it less?

## "Objectively"

It is to prevent ambiguous claim. If I say "Unreal is much more powerful in 3D rendering" (this is one of the most popular claim) I would have to say exactly what is it that make the difference, that make it more powerful. If it is "just" better but I am not able to know why, I will state that explicitly.

Otherwise this article will become like fanboy VS articles out there. These are some of classic claims I keep seeing over and over, without reasons :

- Unity can't make beautiful game. The rendering is not powerful enough as Unreal. (What technology in the pipeline made that difference? Why is it higher or lower "grade"?)
- Unreal Engine is not suitable for small studio. Unity is better and friendlier for indies. (Why? What is that friendliness?)
[Fuck Epic](https://www.reddit.com/r/fuckepic/)(Why?)- Unity-made game is not scalable. You simply can't make AAA games in Unity. (Why? Where's the blocker? It would be better if you says Unity terrain system is not good because xxx, and large scale games uses terrains a lot, therefore Unity is not for large scale games. That would be objective.)
- C++ performance is better than C#. Why? Aren't they just languages? All things became assemblies? Didn't UE also has garbage collector? Magic? Could you tell where is the actual cost of C#, how Unity use it inefficiently, instead of attacking the language?
- Unity is slow, Unreal is fast. Why? If you can point out that UE's blueprint generated code is fast because instantiation of each uses C++ object pool, you are an intelligent UE user. If you can point out that Unity is slow because
[IL2CPP surprises](https://jacksondunstan.com/articles/4545), you are an intelligent Unity critic. If not, you are not objective enough. We will avoid fanboying behaviour.

## A thing about naysayers

I know some UE devs with this mindset. He didn't appreciate technology and just want to bite Unity at any given opportunity. (Actually the same for Unity devs that targets Epic's vast fortune and attacking the CEO for throwing money at everything.) This "faction/categorization" mindset seems to be innate in human. One use Apple and automatically hate Android. One is with this skin color and hate the other color. One hate a person from this country because someone else in the country/historically did something bad. If you are in group A then you fight with group B. esports is not sports. But isn't it funny that all the problem came from just that you are being named/categorized as something? Naming and words are human's creation and we artificially did this to ourselves. Why not move the category one step back to just "technology" instead of Unity and Unreal?

- When I was trying to present the new Data-oriented tech stack in Unity which is exciting, he came to say UE
**also**has the kinda same thing (baseless claim) and is also performant (is true). I have to go all the way to Unreal C++ source code even if I am no Unreal developer to show him that it is not the case while explaining where UE performance actually came from (automatic object pooling, efficient Blueprint codegen, and so on). He then completely ignores his previous claim and turns "Oh really? WOW that's amazing! Then UE must be really good that without all the DOD crap it is still fast! See!" I have nothing more to say that the whole point of him is just claim that UE is superior "overall" no matter what, and no longer related to anything I presented. He can just say this without any context on his own timeline and it still make sense. It doesn't have to be a comment to my DOTS related post at all! - I simply say that the new beta is available and you also have a chance to win a sweepstake on submitting new bugs. He came to say "oh, so Unity have to beg user to test for them now?" The "for them" is alluding to how superior UE devs took care of all possible bugs and each releases are 100% clean, only waiting for user to use it free of worries, where Unity put out broken product with zero test and let user do all the work.

We know that's not how beta testing works, and public testing is always a good practice for any software development. It is more likely that he never taken part of modern software development and provides feedback (UE is even open sourced, which he often claims to be a superior thing to Unity since you can modify anything, but ignores the fact that it opens way to contribute back even more than Unity which likely he never did or interested in wasting time to it.)

He even adds that "it is strange for a company having to bait the test with prize advertisement". Most normally minded dev (or even my mom who knows nothing about Unity) could just view it as a nice bonus. (There are only 5 chances of winning even! You cannot even reliably get it to call that an "incentive"!) You see this kind of fanboy can turn absolutely anything to negative side as he wish. Public beta testing became laziness and ignorance. Giveaways now a dirty bait. Humans, how?? (One saner UE dev came to help in the comment and says "I think you should report problems on what you use no matter the tool or company." which I appreciate and applauds. This is the UE dev I am looking for!) - I simply says a Unity package X is now available in preview and is really interesting. I added the "in preview" fully expecting him to take the bait and he did, "An another broken piece of software half-ass shipped. When will Unity stop doing this and let user easily access their junks?" Since I am still interested in his further replies, I added that he was wrong on the "easily" part that you have to turn on the PREVIEW MODE, that is hidden in the little hard-to-click dropdown, to access it. I was too tired to fix his other part "broken" vocabulary to a proper meaning of "preview software" so I let that slide and make him feel like he won half of the argument. He replied to my "easily" comment as simply "oh, I see.", and this happened in the past where I say the same thing that preview mode had to be opened first and he says the same "oh, I see".

By the way other softwares including UE has preview technologies. As in it could not have worked as expected and disappear at any moment, or if it goes well then it becomes a beta. Microsoft's[Blazor](http://blazor.net)was a preview and became beta on 2019 too, for example. He simply wants to excert supremacy when opportunity arises and that's not constructive. He could instead says UE has this equivalent thing, not as a package but built-in, and is far better because X and Y, in which case I would be very happy because I love tech and it is always nice to know what to use and what to improve. - I was talking about Quick Search package, a "go to anything" type popup in IDE now in Unity. He still says "Oh SO you have to install packages to make Unity at least usable." (alluding that UE has it all "from the beginning" and require you to do nothing) This is completely off the point of packaged design. Look how even a somwhat innocent technology like packages could be villainized by this guy! Why don't you say this to Node.js and the NPM community too? Node.js can do nothing useful by itself and therefore sucks.
- Any acquisition by Unity that I present is replied as "Look how desperate they are trying to replace their own broken internals." instead of strengthen the team that it supposed to mean.
- Even a straight upgrade in Unity (that's really good, and I didn't say "preview") could still be replied as "Finally catching up huh, Unity." The answer is yes. But he just want to say that Unity was behind and is still behind, which is off-topic but benefitting his praise UE agenda.
- I recently said how the talks in Unite Copenhagen suddenly shows that everything Unity broke for the last few years finally bears fruit, suddenly multiple new techs became tangible. This is due to dependency problems and Unity had to bite the bullet, now things could be built over those properly. He still came to say "The problem is, we still have to put up with instabilities for the time being." Yes, that's what a beta software means... basically a tautology of what I just said in a way that makes Unity looks a little worse for making new things? "We have to see how stable they are." This applies to everything. "But personally I was confused by Unity's UI and already used to Unreal's cleanliness." It's great that you have already found a design language that sparks creativity for you. Also there are big design change in 2019.3, it's unfair if you are not evaluating this again and refer to old Unity. This needs more elaboration as it depends on personal preferences in a large part.
- There are good sides about him too. If I present something
**really**good (the most recent was UI Builder for generating`UIElements`

components and finally editor tools development is WYSIWYG) that there is no possible openings to say any bad things, he will still come to say he is happy that Unity is now getting smarter that the era he was using (around Unity 5). It still has a slight shade throwing in a "finally catching up, huh" way but everytime this happens I know this is a good direction for Unity.

I am aware I am giving him these opportunities, it is just a little addicting and fun that he always come to bite my bait every time perfectly when I am expecting, that I still keep doing it to see what he will come up next... (I will continuously add to this list as I collect the replies) Anyways! Don't be like that here.

## Iteration flow

Right off the bat, I will start with one thing super notorious in Unity, **assembly/domain reload time**. If anything is a reason to stay away from Unity, this is it.

That is the time it takes to enter play mode. What domain? This is not a compile time that you see the spinner, but it is the time that C# reset its state which is the pause after that spinner. And it is the pause before entering, and also after recompiling script each time. No, [asmdef](https://docs.unity3d.com/Manual/ScriptCompilationAssemblyDefinitionFiles.html) will not help you, that only helps with the spinner and not the freeze afterwards.

At first it is not much, but as you give in to Unity and grow your project.. years passed and now to enter play mode it takes 20 seconds!! And it even doesn't have to take that long, [my stupid-looking game](http://exceed7.com/duel-otters) is already taking 11 seconds to enter play mode.

It is a lot, it adds up the more you want to do iterative design and it throws you off the flow, most importantly.

And what’s worse,** it depends on the project not the scene.** If I create an absolutely empty scene in a heavy project, to enter play mode on that scene would take as long as the other scene.

Judging from this thread it seems UE can iterate pretty dang fast. It is one thing that make or break the engine choice to be honest. I can see myself choosing UE just because of this.

**The most painful** however, it feels like you are “tricked” into Unity by its deceptively friendly entry, but revealed later that the performance degenerates as you goes on at the same time you think you cannot go back now that you got this far. And no one could tell you about this. It may increasingly be the case that everyone has his first project in Unity and learned the lesson, and now sticking with Unreal because there is no hidden problem waiting at the very end. (Is it true?)

If you ask me if I can migrate project instantly without any time cost (but you cannot come back to Unity again ever) would I move this project to Unreal? No, I still value Unity's interface. For others, I can see that this is a sound option given how important it is to quickly iterate on the play mode.

This is worse than bugs which are quite rampant in Unity. Bugs could be reported and fixed. This is **by design **and unfortunately not a good design.

### How to avoid entering play mode

It is ironic that I have to avoid entering play mode when I am using a game engine. This area makes Unity sounds like a still in-development engine rather than a complete one.

What is the solution then? **Make a new project**, lol. It's not a joke however as recently with Unity Package Manager you could link packages from other places. If you make your game in pieces, and use a new project to edit those pieces, then the project that contains each individual pieces will have an acceptable iteration time. (Pieces inside the same project is useless against domain reload.) And Unity Hub now could quite easily open multiple instances of Unity. Fortunately multiple Unity instances is not costing much. I could have up to about 3 Unity on my MBP Early 2015 open at the same time.

Some other way to fight with this, for example, exploiting `[ExecuteAlways]`

but it comes with its own challenge to make it works in both prefab stage and normal scene.

Unity's Timeline feature is also a good solution because you could preview time-sentitive things like UI transition without entering play mode. (As opposed to `Animator`

which its state machine is only available in play mode) Imagine games made before Timeline's addition that is trying to time some explosion effect together with some other event.. how many play mode enter-exits... after 2019.1 you could add signals which emits events. It could trigger in edit mode too but it may link with other play mode only things that you have to enter play mode anyways.

Each play mode is rage inducing because I then found some little bugs that prevents it from going further, I feel stupid and also have to wait more 30 seconds for script compile x1, then it reloads after the script compile and also again when entering play mode. (Fortunately exit play mode won't reload)

If they add some button I could press in play mode so that it **restart **play mode instead, I could save 1 domain reload on entering. Unfortunately, no option here is comparable to that.

- Recompile and continue playing : 99% of the time everything breaks. You will want to exit and reenter anyways.
- Recompile after finished playing : my default option, but takes 2x domain reload for after recompilation and on entering play mode.
- Stop playing and recompile : only if this option enter the play mode automatically again and suspend it until the script finishes recompiling, so 1 reload for both after-compilation and after-enter play mode, it would have been great. But currently it is not like that and works just like you stop the play mode by hand. So you pay one reload after the compolation, then you pay another on pressing the play mode button by hand.

![](../../assets/94afa98c8698e07e.png)

When it is a phase to iterate by entering play mode, I have to work laying down on bed so I could recover my back spine while it reloads. (It takes that much time that my back actually recovers) Also it helps to close my eye in between each play mode. The time taken to enter could save my eye sight in the long run rather than having to look at freezing Unity editor.

There is an urban myth that “Ori and the blind Forest”, a beautiful game which used Unity, take 1 minute to enter the play mode! Imagine getting a runtime error on the first frame after that wait...

### This affects integration test badly

Or called “Play mode test” in Unity. "Play mode"... oh no. Now even if I have a proper TDD design to automate testing of my scenes, I feel reluctant to click on the integration test because it would take so long to start one. The only remedy is to run multiple tests in a row as entering play mode is only once. But that also has its own challenge as the test “spill over” to the next, because the “sandboxing/clean up” you got from enter-exit play mode is now gone. (Also it is usually the case that you run individual test at first and fix problems, you run them all after your game shipped and test for regressions.)

UE also has “Automation System” to run integration tests. Still not using it yet, but it better be faster than Unity. In fact from Unity’s entering play mode performance, I **guess **it should be faster than Unity.

**Automation System User Guide***A guide to using the Automation System for Running Tests.*docs.unrealengine.com

### 500ms

This is a now famous number from Unity at GDC 2018, where the company start pushing the "Performance by Default" motto. Which gives everyone hope. The clip has been fast forwarded to that time :

What's reassuring is that the CTO himself is feeling the same pain as you! He's saying it. Changing C# script in a large project file, reimporting, or anything, should cost less than 500ms, but it didn't! **He said it made him angry. **To be honest that sentence made me happy.

But what's worrying is that how could Unity get there? Currently it is like.. 20-50 times of that time. It will be damn great to create in Unity once all the pieces assembled together.

I could see some of the pieces previously, even though it is not explicitly stated in the patch note that these are the part of 500ms plan :

- Incremental compiler integrated to take advantage of
`asmdef`

. - Unity Package Manager (UPM) system, works well together with
`asmdef`

. - Shaders compiles and applied to the scene asynchronously. (The blue flash you see briefly when changing materials)

## Scaling problems

Instead of just entering play mode we can more generally define that Unity got scaling problems (that may or may not related to that 500ms). Likely a big consideration factor for AAA companies, hench why so many AAA Unreal games. These are not advertised, of course. It's painful to run into later in your game and having to make a life or death decision of do I want to continue with Unity or not. Here are some from top of my head, with mini sections about them after.

- A lot of scripts added results in longer domain reload and longer enter play mode time. You fear of adding scripts liberally. Fixed when DOTS in place because then you can safely remove domain reload, there is no data to reload in systems. (Coming soon)
- A lot of hierarchy which you thought are friendly helper to both organize or move things together, has performance implication.
[You can intentionally try to work around it](https://youtu.be/W45-fsnPhJY?t=805). But ultimately would be fixed with DOTS transform system which effectively linearize everything, while kinda keep them hierarchical at much cheaper price . (Coming soon) - When lots more assets and dependencies added to your project, you now add more time required to switch platforms (all of them must be reimported to the platform's format) or even work on those object then switch back to Unity to iterate the content. Fixed with new asset database system (Coming soon fully in 2020)
- When you add more languages to the game to globalize it, there is no built-in solution to handle it other than having to write your own. Fixed with
[Localization package](https://docs.unity3d.com/Packages/com.unity.localization@0.2/manual/index.html). (Coming soon) - Many more?

### Unity 2019.3

![](../../assets/d379f66bfbabc49f.png)

I am thinking of printing this and frame it, because finally we could do something about this dang curse. So the domain reload is not going anywhere, but we could turn it off!!! If you sure you don't have `static`

variable junk from the last round of play or you design them properly that old value has no effect, then this... is the future.

![](../../assets/e6c935e3ad5235d1.png)

[https://www.youtube.com/watch?v=hRJUt3voDHQ](https://www.youtube.com/watch?v=hRJUt3voDHQ)

[Unity team said that](https://forum.unity.com/threads/editor-domain-reload-and-or-scene-reload.680347/#post-4560043) resetting all the `static`

is the big part of time taken. So if you ended up hand-resetting all of them later then no gains. But it is better to design without `static`

in the first place just for this feature. Here's where you could try it if you are on alpha version.

![](../../assets/1dc9fe527cc6e7b7.png)

By the way, my game that was 11 seconds to enter playmode is reduced to only ~0.5 seconds! That surprise me not in just that the number is so low, the number arrives at around 500ms, so it looks like CTO had measured a theoretically possible time before making that announcement?

See this document : ** Entering PlayMode faster without domain and scene reloads. **It's a very big deal that we have to change how we program things to accommodate this.

In that docs it even said the combined domain reload time of all Unity users in the world is about 8~9 years per month, which would be saved by this upgrade. Holy cow.

### TypeCache API

C# reflection system may looks evil but it is actually the base of many important systems in Unity, particularly the **type **information which we need to constantly ask **the whole assembly **what it got right now. Many editor code and of course ECS need to be kickstarted somewhere with a list of all possible types defined. Serialization too, so it knows the structure of that type.

In 2019.2, Unity made a move to address this. This blog post summarize very well what is the problem and it is closely related to play mode iteration time. Check it out :

(You can see it is becoming a theme with Unity and later in this article as well, that you will see they **openly say what went wrong, **and not afraid to say "so we are scrapping this and that". I love this. No other company's patch note talks like this and just talk about improvements.)

### Better imports

There are other wasted time that is not just entering play mode. We iterate when going to external creative program and back. We iterate by switching export platforms. Better system started coming in 2019.3 with a new serialization rework, and then beyond that, watch this talk about the roadmap. (Again, still long way to go)

My game is relatively small (~2GB total) and it took about 10-20 minutes to import when switching from iOS to Android. I am willing to wait but I could imagine nightmares other big games will face.

### Unity Live Link

This is a futuristic feature enabled by DOTS, that let you change the game running on an actual device from editor instantly. Wow, how is this possible? Without diving too deep into DOTS, because "it's just data™". So if your game is made with DOTS, the changed data can easily be "diffed" to the device, and the replacement is instantly read by the systems without any problems because... "it's just data™". (Or should I say because system is just logic).

### Meanwhile in Unreal...

Blueprint is a visual scripting system in Unreal (before UE4 it was using a system called Kismet). Many compare Blueprint with Prefabs in Unity, but it's more than that. It is a **codegen**. So the graph you design could be individually compiled into C++ code. And in the context of play mode iteration, this means the compile time will not expands exponentially like Unity because each one compiles individually.

Ok, the compile time is equal to the spinner in Unity but we were talking about that freeze afterwards. I think there is no domain to reload in UE. It is so damn fast to enter play mode. Unity's disable domain reload added in 2019.3 is at best a band aid compared to this.

But Unity with DOTS is equivalent to Blueprint since "system" code is equally isolated and could be codegen-ed. Via graph visual scripting tool in the future, same purpose as Blueprint graph but output a different kind of thing. Blueprint outputs OOP-like instantiable code. System has no data, it's just workers that are waiting to work on data. Therefore in the future iteration time could be eliminated with DOTS thanks to more isolatable compiles and less dependency on reloading domain (that you could just disable it).

### Meanwhile in Unreal (2)...

![](../../assets/b364b0fd4794a24c.png)

With tech from [https://molecular-matters.com/](https://molecular-matters.com/) UE had licensed, now C++ could be hot reloaded. Not that entering play mode is fast, now you don't even have to exit. Meanwhile in Unity you must exit, wait for spinner, wait for domain reload freeze (out of edit mode), wait for domain reload freeze **again **(on enterint play mode).

All these affect your game shipping date directly, so UE feels like an engine that could get a job done thanks to this alone.

In my opinion, the upcoming Unity Live Link is overall superior. But that's not now, plus your game must be built with DOTS.

## Interface

![](../../assets/1c85b9411cb9a7c7.png)

We have arrived as a subjective thing is interface design (if you "like" it or not), but I am going to turn this into an objective discussion as promised at the beginning. In UI world we are able to compare their function and how it affects the workflow. We touch the UI at every moment. And so this is the objective part of UI. What's the resulting speed of work from using the UI? Turning from likings to measurable "time".

There are papers and text books that compare usability of UI regardless of you like it or not. And in some case if both application could perform the same result, all the difference are in UI design.

Unreal looks quite dated in my opinion, where the world had already moved on to “flat design”. It uses gradients, a lot of 3D in the UI that’s not the viewport, and a lot of curves/rounded corners. Thankfully, the UI color is industry-standard dark. But overall, too busy UI for my taste.

It’s funny that Unity’s UI can only get dark after being “professional”, I saw someone refused to use Unity because it couldn't get dark for free, a valid reason. (He opt for [Godot](https://godotengine.org/) instead.) Well I'm fine with grey-white and value my workflow more than colors, but if you are that kind of color-sensitive person then Unity is not suitable for you.

Unity hasn’t update its own UI that flat either (though that’s coming soon in 2019/2020 or so they say with their new UI Elements system?) but default Unity is still flatter, with less 3D icons and less colors.

Unity had major update once where it became compatible with Retina display but that’s about it. The font is also pulled from the OS, if I run Unity on Windows the font would be different.

![](../../assets/2116319b02c8c296.png)

Well, this is a personal preference but I like Unity’s design better. I like things that looks “techy” and if I may put it in the worst wording “boring”. Like minimal/techno (many normies called bigroom, dubstep, trap, EDM as “techno”, it is wrong) /drone/noise music, not a single of my friend said they like minimal music when I introduce it to them. (some said is this even music??) So “boring” is not a negative to me but more skewed towards “playful”. I feel like I want to play around with it.

Unity’s UI is “tame and clean”. The most important strength is in my opinion **fixed line height**. (This goes long way into when making a custom inspector) Also Unity’s dark is darker, similar level to Adobe CC’s dark. For example Clip Studio Paint one is not dark enough that it makes the white them actually looks better. But actually I like Unity's free white theme better. (And it is kinda funny that you have to subscribe to use "easy-on-the-eye" dark theme, as stated on the pricing page.)

To draw a comparison to other program, in a DAW (program for making audio for the game, etc) I liked Ableton Live’s design.

![](../../assets/61680b393f466c60.png)

Other programs that I don’t like as much looks like this :

![](../../assets/c2429a0aa905774d.jpeg)

Am I nitpicking things? I think not at all. If I am going to use one mechanical pencil every day, I would also complain about the material it was made of instead of functions (so all could write almost equally) as I have to touch it every day. GraphGear1000 is awesome by the way, just the right weight and good finishes on the barrel.

In the DAW business, almost all DAW is capable of doing the same thing. But the difference is the feel they give, how they present the feature and keep the flow. Making music is very spontaneous, **speed **of getting to your idea became more important than features because you could make music otherwise not possible if the DAW is not inspiring you. For example Ableton Live I am using cannot do “prefab” equivalent kind of thing in music making, but in turn that encourage slice and dicing clips without worry about reuse. It encourages experimentation and mesh well with other “dirty” nature of that program. There are other DAWs suitable for more organized composers. I got the same feel from Unity, while feeling incomplete and wonky it encourage experimentation. (Something that usually waste my time on actually shipping the game to be honest.) But unfortunately, all advantages I like are nullified with Unity's notorious assembly reload time.

## Performance

Unreal Engine is very resource intensive! I got a warning dialog on opening up about UE is best on quad core something something, but I didn’t think it would be this intensive. On the default scene with 2 chairs, rotating the viewport with a mouse already present some lags. (Around 0.3–0.5s, imagine I rotate quickly and 0.3s after I have already let go of the mouse the screen is still spinning, catching up with the remembered “motion” I did.)

Here’s the spec that is not enough.

![](../../assets/dae3cf46272f3621.png)

I will get a new desktop computer later, then I will be able to evaluate UE more.

I have no problem in Unity so far with this spec. (Also I could open 3 Unity instances at the same time) But however I read from [multiple](https://www.reddit.com/r/gamedev/comments/byh2te/throne_of_lies_post_mortem_dump_years_of_knowledge/) [places](https://www.reddit.com/r/Unity3D/comments/byag2c/an_everlasting_cry_for_editor/) that even with decent i7 computer the reload and compilation time didn't improve. So it appears that if you have powerful computer you may want to go with Unreal.

## How they take your cuts

The most well known difference and therefore I won't talk about it much. Unity has subscription with additional services/features, along with some revenue threshold you can use Free or Plus (100K$ and 200K$ annually as of 2019, but those thresholds are so high that the price for Pro wouldn't matter anymore)

Since Unity 5 the engine is no longer gibbed functionally if you go free (..other than DARK THEME), just that online services (that requires Unity server running and serving you at some point, editor or live.) that are locked behind Plus/Pro.

Unreal take your game's revenue 5% per calendar quarter over 3000$ earned. Most common misconception by overly biased Unity fans is that UE always take your revenue no matter how small you are and therefore greedy and evil. But there is this 3000$ quarterly threshold. (In my country if I solo dev and get 3000$ quarterly, that's already a ridiculous amont of money.) Also you get more advantages [if you publish in Epic Games Store](https://www.unrealengine.com/en-US/blog/announcing-the-epic-games-store).

And just announced in an article about [Unreal Engine 5](https://www.unrealengine.com/en-US/blog/a-first-look-at-unreal-engine-5)'s first look, your first 1 million gross revenue is now waived! If you are indie, you are very likely be already well-off even before you could get 1 million dollar. It's perfect for indie game now. **It's basically free.**

![](../../assets/e09ef1ffe56af4d3.png)

It's more interesting what compromises you get when not paying. Unity is infamous for locking the DARK THEME behind paywall. Everyone make fun of it because of how ridiculous it sounds. Anyways [there are hopes waiting in 2020??](https://blogs.unity3d.com/2019/10/17/pricing-for-unity-pro-and-plus-subscriptions-to-change-on-january-1-2020)

![](../../assets/f12b3c450841929b.png)

Unity has a one more separated subscription worth mentioning which is [Teams](https://unity3d.com/teams), you do not get this along with main program subscription. Instead of services given for your game from Plus/Pro subscription, Teams gives your actual team new abilities. The most important being Cloud Build to complete the continuous integration flow, it's not available in free Teams. This build server can run tests written in Test Runner in Unity, so you can get a very extensive test (where it actually play your game reasonably) with this subscription.

### Splash screen

Lastly you have splash screen saying made with Unity on start with Personal edition. I think it backfired somewhat when this should either entice upgrade or spread awareness of Unity, but rather the devs who use Personal may not have advanced skills and it instead spread awareness that Unity-made games are not looking good. Meanwhile UE don't require you to display the logo, but seems like all the big games do. I think there is a separated terms like custom engine license which requires you to put the logo, which is great, because only big studios do that and it says Unreal-made game is high quality.

Made in Unreal AAA titles are countless, like Monster Hunter World and Kingdom Hearts 3, which I know because of splash screen thing I mentioned earlier. Unity seems to be go-to choice for mobile indie devs but those game rarely advertises that it was made by Unity if they are competent (because they paid subscription and removed the splash screen) as compared to Unreal. This makes Unreal’s public face very strong, as it is “trusted” by big games. At the same time it unfortunately make Unity feel like a “less professional” choice. (Of course you could make your Unity knowledge a profession!)

## Company maturity

Epic is no doubt a very successful company that throws money left and right.

Epic Store is using money to yank games from Steam with exclusivity deal like the case of [Shenmue 3](https://www.reddit.com/r/pcgaming/comments/bz5k1g/shenmue_iii_is_now_epic_exclusive_and_no_refunds/). [Smaller devs](https://steamcommunity.com/games/785790/announcements/detail/1606010497772063337) too, however games like Terraria [refused](https://www.gamespot.com/articles/terraria-dev-comes-out-strong-against-epic-games-s/1100-6466920/) to "sell their soul" no matter amont of money.

And yes, Fortnite. Read [this interesting article](https://venturebeat.com/2018/09/15/john-riccitiello-interview-how-unity-ceo-views-epics-fortnite-success/) how Unity CEO talks about it. The company's wide reach is impressive. There is even a Reddit sub called [Fuck Epic](https://www.reddit.com/r/fuckepic/). Everything will eventually be hated by someone out there, but when you got a sub devoted to hating you, you know you are very popular!

And let's not forget the drama between Unity-Improbable-Unreal. As a person that witness the event unfolds (from home), the entire drama still remains an impressive business lesson to me, and show Epic's business character very well.

Initially it's between just Unity and Improbable, then Unreal CEO from nowhere [tweeted to his advantage](https://twitter.com/TimSweeneyEpic/status/1083407460252217346). The tweet wasn't wrong even though Unity's term wasn't clear, because it starts with "did" as a question. Follow up tweets describe Epic's own strength, again not wrong, but it reads like Unity didn't have these features (I guess as an intended effect of the tweeting). As when I thought that's all the win-win Epic could reap in this event, overnight, the [25 million$ funding](https://www.unrealengine.com/en-US/blog/epic-games-and-improbable-working-together-for-developers?sessionInvalidated=true) blog post appears and Improbable is now strongly sided with Epic. It's just... wow. You should Google to read more by yourself, it's already out of topic enough.

Now the game engine. Unreal Engine has about a decade more development time in it compared to Unity. Both engine had transitioned licensing scheme to become more indie-friendly as it is today. UE take game's revenue, but at the same time big games are trusting Unreal.

Unity needs more time to make up for those dev time difference. Not to mention there are a lot more breaking changes recently as opposed to the rock solid foundation of UE. Unity is now building that foundation, a new engine that is no longer have to carry any weight from 15 years ago, with their Data Oriented Tech Stack (DOTS) movement. The first sign of the end of this tunnel can be seen on [Unite Copenhagen 2019 playlist of over 90 video clips](https://www.youtube.com/playlist?list=PLX2vGYjWbI0RzLRaqsqcgnuc2RvLPTUmi), each one with unbelievable features. I can really feel this one is different than previous. Not Unreal-level solid and stready, everything starts to click.

If you enjoy underdog story or something in-development you may like Unity. I also liked Unity because it's fun to follow what the company will come up next against the big giant UE, in addition to extensible UI that I like. (Or as Unity says it in their UI redesign goal in 2019.3 version : "feels unlimited")

See these posts which summarize quite well.

### Credibility with existing games

In [Monster Hunter GDC presentation](https://www.youtube.com/watch?v=9YWQ2TCupXA), there is one point where the dev shows an early build and says this is an "old engine" before they moved to Unreal. From the looks I think it is likely Unity. I wonder what the dev discovered that made the switch. Is it some bugs? Integration with Speedtree or Havok? Or play mode iteration time that builds up? But even looking at the graphic I could get a feeling that it is "kinda Unity", just because Unreal Engine is so often associated with beautiful graphics. ..where actually the dev may not have put in proper lighting or proper terrain yet, Unity did made a project like [Book of the Dead](https://unity3d.com/book-of-the-dead) or [The Heretic](https://unity3d.com/the-heretic) precisely to dispel this kind of myth, and I think terrain of those demo doesn't "looks Unity". In fact the Heretic demo has that Unreal characteristic.

If you use `adb logcat`

while starting a mobile phone game and see a log from Unity then you know that game is one. Almost all mobile music games I know was made by Unity.

## Bug report QA brick wall of hopelessness

I strongly believe that the bad rep that Unity accumulated, that it is full of bugs, stems from the bug QA people. It is extremely hard to get them to fix the bugs you found. Each bug submission "failure" that shows up as a reply in your mailbox adds up every morning ruining your breakfast coffee. And I am saying this as the winner of bug submission sweepstakes twice. I still have so many bug report graveyard that fails to get to them but I have to move on and live with the bugs.

Why? I have summarized here in this thread already :

[Criticism on the QA team about CRASH bug reportingI have read from Unity Blog long time ago that talks about project stripping, explaining reproduce steps, making it easier for the QA team to make it...](https://forum.unity.com/threads/criticism-on-the-qa-team-about-crash-bug-reporting.931104)![](https://unity3d.com/files/images/ogimg.jpg)


![](../../assets/65a62093edb94a73.jpg)

It's scary. If you are Unity devs, you know the feeling of checking Unity Hub every morning for update, and hope that it will randomly fix your years old bug, while introducing the less amount of new bugs as possible. It really make you sweats nervously, especially when you discovered new bug 1 month later that is more critical and it is too late now to revert version back.

While in Unreal, you still have the ultimate (though extremely difficult nonetheless) solution of fix it yourself because you can see all the engine's source. At best, if you manage to find the spot in engine source you can point to it for the dev to fix it.

In Unity, it's a game of blindly creating a black box on your side, that triggers error spot on their side, because you have no access to engine code.

Lately many things came in UPM package though, if the bug revolves around those code then you have higher chance to tell them which lines are wrong, and even temporarily fix it instantly. In UE, fixing engine code yourself would require a recompile of engine. Unity with C# package system is better here.

## Practicality of features

In multiple places, UI, and release note, I can see Unreal Engine is being very practical in each feature. This feature do this and that. Their features are high level and specific. And often looks like a result from their own games. Some feature like big map streaming is obviously from Fortnite, where in Unity the feature like this is called "DOTS ECS Scene Workflow" (which could be memory loaded and stream kinda the same way) but you see it is not as obvious as the "this could make this" style in Unreal.

I will give you one UE patch note to read : [https://docs.unrealengine.com/en-US/Support/Builds/ReleaseNotes/4_22/index.html](https://docs.unrealengine.com/en-US/Support/Builds/ReleaseNotes/4_22/index.html) versus Unity's [https://blogs.unity3d.com/2019/04/16/introducing-unity-2019-1/](https://blogs.unity3d.com/2019/04/16/introducing-unity-2019-1/). While I know Unity is releasing a very exciting tech like DOTS audio, most of them feels intangible to typical users.

## Animation solution

Someone I know said that he switched to UE because of Unity tools from 5.x to 2018.3 sucks for creating a large scale action game and he never came back to visit Unity ever since.

I asked him to elaborate what exactly is that "tools" and he said it's Mechanim and multiplayer. At that moment, I understand completely. He also said he heard about Playable Graph and didn't know if it helps or not. We will visit this later as well. I don't make multiplayer games so I cannot comment about that in Unity, but I know that Unity obliterate its own UNET without replacement and so I think there is no way UE could be worse than this.

He said he cannot make a precise notification system in Unity. This is true, as in Mechanim we are stuck with that little event pin that serialize (remember) your method to be called by name and is very prone to error and difficult to maintain, difficult to bring the script you want to be "around here". There are so many annoying parts that make you worry they could fall into pieces at any moment.

In Unreal, he used `AnimNotify`

([https://docs.unrealengine.com/en-US/Engine/Animation/Sequences/Notifies/index.html](https://docs.unrealengine.com/en-US/Engine/Animation/Sequences/Notifies/index.html)) For Unity users like me, you don't have to know about UE but just by follow that link looking at some example images, one could already see full of "UE style practicality" waiting for you! I am not even making an AAA-style 3d game and I am impressed, and this is just about the notification.

Here is one instance of practicality : there is a specific button that says play particle effect as a result of notification. In Unity's way of doing it, they would hand you a method connector and call it a day, because you could do whatever you want in the method by coding. Here, it is suggested that it could be used in something like dust coming out of character's foot. It would not be surprising if Blueprint's generated code take a different, more efficient path based on these pre-made choices.

There is even a small thing like setting color for notification marker, it would be a dealbreaker in bigger projects where you got code events, particles, and audio together in the notification system. Meanwhile in Unity, a bug report about the marker in its collapsed state or timeline extrapolation mark, could be almost invisible in their personal (free) skin [was rejected as a low priority defect](https://fogbugz.unity3d.com/default.asp?1155967_npdd3e7lu88sfvuk). It would be a serious issue in big project if you can't see these marks. Can you spot the folded default signal track marker and the infinity extrapolation mark?

![](../../assets/01424c5745702794.png)

![](../../assets/b4c23a5de07b03db.png)

![](../../assets/33c124484a8845fc.png)

![](../../assets/34e7c35dfc3249b5.png)

Unity has marker customization with editor scripting though, but the API is a bit weird to use and requires placing images in magic-named folders in 2019.1. More extensive timeline customization came in 2019.2, but I didn't try yet.

Look at that preview button in UE! Unity cannot preview the complete Mechanim graph in edit mode just because it contains state machine and Unity team thought edit mode must be stateless. Here apparently you can preview notification.

He said UE's state machine make more sense than Mechanim, but nothing more so I have no other comment to say. If someone used both, maybe could you leave a comment why UE's make more sense?

He said take a look at Animation Montage feature. ([https://docs.unrealengine.com/en-US/Engine/Animation/AnimMontage/Overview/index.html](https://docs.unrealengine.com/en-US/Engine/Animation/AnimMontage/Overview/index.html)) He said it's small difference like this that make or break productivity. I disagree about small difference though because this is a big difference. Just by reading that documentation I could imagine the use case immediately. And look at that left side bar of the documentation, so many **specific** features! He said there are many more glitches to fix in state transition in Unity too.

He said everything UE offer could be used to implement mechanics in a game like Gears of War. He did say of course the art asset and animation quality couldn't match AAA studios, but you have the same potential to get the same "mechanics" as they do. When in Unity, you would be at loss how the hell can you get to that point with given few tools. He said he had written many custom tools to achieve a workflow he wanted in Unity before the switch, only to be given for free in Unreal after he moved!

Previously was all his opinion. Next up will be my opinion from Unity's side.

I saw many voiced their opinion about Unity's mechanim that it's a joke for big scale AAA production. And I kind of agree even if all I made was 2D games with simple character animations.

The first thing is that I think the level of abstraction of Mechanim is wrong. It is too general. If you list out all the features and ask could you make **any **games with this? The answer would be yes. As the person I mentioned tried to bash his head around with custom toolings assembled from these features. However, I think the current level of abstraction would be just right if it were meant for something like UI animation. For character production, if I am making a game like Kingdom Hearts 3 or Monster Hunter World (Both used UE) I would be very worried about depending my life on top of Mechanim.

For example, I want to make a button that play one animation when lifted out, and one different animation if you drag the finger out of boundary to lift off. I could picture how I can script that up in Mechanim easily, which state requires a trigger, interruption allowed, transition time, etc. That's why I say it is just the right abstraction level **for UI design.**

For **characters **however Mechanim is **too general purpose.** Unreal's practicality gives you many specific purpose tools that invites you to make a game from a subset of those. It doesn't hurt if you ended up ignoring some of them. In Unity you would instead feel that you have to figure out how to use the given generic tools to work with your game, and leads to you adding up custom editors on top of it. In some aspect the Unity way do have some merits, such as making reserch application or non-games. (Which I think ECS will works wonder.) But definitely not in making AAA games.

I think Unity could rename Mechanim to something like "State Animator" (so not to invite everyone to use it for important animations, and indicate that it is an animation with states and cannot be previewed at edit time), and start making a new dependable and feature-rich system for characters. By feature-rich I mean just hand the features to programmers without worrying that it would be too specific, or it would not be usable in some kind of games. I think especially in animation system Unity need to adopt more of UE-style toolings.

About Playable Graph then, if you are Unity user then you know it doesn't help since it is just an API backend for "everything that plays through time" and currently used by Mechanim. User-facing features are still barebone. The latest developement is Playables Notification API in 2019.1, but that mostly related to Timeline feature and not Mechanim. I see no advanced toolings in Mechanim has been added to utilize this new API yet.

If you want to know about the latest movement of this aspect in Unity, following Timeline and Playable Notification API, it's Animation Rigging.

However I doubt this alone will reach the completeness in Unreal. I guess the rest got stuck in "wait for ECS" limbo and cannot advance, or could only advance in an incompatible way with old versions. DOTS animation better be really amazing.

Animation Rigging is coming to fix humanoid problem in Unity, and it is really good. See this :

And this :

Finally there are serious usability issues on keyframe editor in Unity, like how one [cannot preview the animation once](https://forum.unity.com/threads/how-to-make-animation-preview-plays-only-once.585847/) without it looping like crazy, or you can't adjust the bezier handle for multiple keyframes to go the same way (same tangent value). Seems like everyone lives with it since Unity 4 and it still stay that way. The greatest upgrade was the box-boundary handle that appears when you select multiple keyframes, which let you scale and flip in a very intuitive way. I hope Unity keep on adding usability upgrades like that.

UX and utilities difference of an animation system **is a deal breaker**. I have always belive a game is exciting because something always move. So you likely spend most of the time making things move whether you are coder or animator. I can easily recommend many to avoid Unity just because animation toolsets in Unreal are more "there for you" than Unity especially for 3D games. (For 2D games, luckily external tools like [Esoteric Software's Spine](http://esotericsoftware.com) is here to free us from bad UX in Unity.)

## Closed source, and the “extern”

In Unity, when you can’t quite figure out why something went this way, is it your fault or Unity’s fault? You would turn to Unity’s [CsReference](https://github.com/Unity-Technologies/UnityCsReference) which is the C# part open for view in the GitHub. But in the end I would always come to the dreaded `extern`

. That means from this point it is in C++, which is the closed source part that Unity didn’t open.

UE definitely feels more reassuring when you know you can dig as deep as you want and even edit something. Even if I didn't use UE at all, in an hour I could pull the source code from Epic's GitHub to explore and deduce if Unreal allocate memory in data-oriented or object-oriented style. ([Read about my deduction here.](https://forum.unity.com/threads/anyone-know-how-ues-generated-class-from-blueprint-allocate-and-use-data.688189))

For example of problems about this, I have been researching about audio latency in Unity and it results in this huge article.

**Android Native Audio Primer for Unity Developers***I will demystify the “black box” surrounding the Android audio system and analyze why Unity’s way of using it makes…*gametorrahod.com

But to write this article, it is a result of rage-inducing **probing **around what I cannot go in and see. (Trying various input into a black box, and reason on the output) A lot of mysteries that I must **assume **why it turned out that way. It would be much easier and informative if I can go in and see why Unity set sampling rate to 22,000Hz for some of my phone. That's a magic number.

The dang Animation panel that don’t let me play only once for like 7 years ago and it is still that way. I wonder how animators can work on a short UI animation while seeing it loops like crazy. See this thread I got no answer.

And the curve adjustment UX is stupid. You can't edit X Y Z tangents of a scale together. See this thread I got no answer.

If I have an access to the source like Unreal, I would have go in and add some small usability feature by now instead of waiting years because the priority is not high enough for the rest of the world for them to care.

They used a voting system on requesting a new feature, which everyone got 10 points to freely allocate in and out. Imagine I post a request to let the animation play once, now additionally I have to rally a campaign somehow to get points so that it is not only me that is requesting for this feature. (Others might encounter this pain, but did not come to check my request and vote)

## Do you really want to edit the source code?

To contrast with the previous section where I had trouble debugging into Unity's black box, this one I think Unity get it right. Unity has something even **better than source code.**

### Unity started to bring up things you actually want to edit

Basically, very deep features are coming from closed source C++ to C# package which are all readable and editable. It goes very well with Unity's closed source + license fee scheme, the engine code is still closed.

The first revolution is the SRP (Scriptable Rendering Pipeline) where we could edit rendering steps to the point that it breaks all existing materials. Unity didn't stop there, they used this ability themselves and give us URP (Universal Rendering Pipeline) and HDRP (High Definition Rendering Pipeline) as a starting point but likely you wouldn't want to edit much more or at all. But now the critical rendering sources are visible, in a sane way that cannot break the engine if modified, even if Unity itself is not open source. This is better than editing render pipeline in an open sourced engine.

Then we have DOTS (Data Oritented Tech Stack) where we decided to use hand-allocated space in C# instead to optimize cache usage, then DOTS Audio is coming where we could essentially make a new mixing pipeline on thread if we want to. The incoming New Input System let you access the input buffer memory that hardwares are sending in.

These are things I actually want to edit. In Unreal, because the source is included **theoretically** I could do the same to surgically change rendering steps or audio mixing. However, the way Unity did is "serving up" to the user without the engine code in the mix. The modular approach.

In a way I feel even better than Unity one day says "the engine is now open source and is hackable to the core", because I don't have to worry breaking the engine, I could edit things I care about with full Unity support. I feel like I could make the engine my own faster than UE, where the theoretical upper limit of what I could change is unlimited, but it is no use if I am not going to that limit. Also remember that by changing the "allowed" area, you still receive updates from other not allowed areas while keeping your changes. (Taken from [this talk](https://www.youtube.com/watch?v=91zUwJwkXNQ).)

![](../../assets/7e8f7760dea99e35.png)

It draws parallel to Android where it is advertised as fully open OS, most Android believer attack iOS with this argument, yet most user will only "mod" the phone on higher level like custom cute icons. We don't actually want to change the OS, how touch detection works, how audio HAL submit audio frame, etc.

The same in Unity, I don't want to change the UI to pink or move the play mode button to bottom bar (where if it is 100% open source like Unreal, I would be able to do). I want to optimize rendering and mix faster audio, and they are providing that without breaking thier own closed source business plan.

I think it take a lot more work to enable this in the most flexible and safe way, than just open up the source code and let user edit it freely like Unreal and claim everything is possible.

Could Unreal do this modularly too? I don't know. But my Google search yields no result about rearranging rendering pipeline. For example, switching the clear color step to the last step for some stupid reason, where in Unity SRP you are able to do easily by coding in C#. Still, Unreal's theoretically could do this by editting the source.

However, I heard big companies would go great length to make **the engine** "their own". This is the real strength of Unreal's C++ source included feature. And you could fix all bugs by yourself theoretically, because in Unity you are always at risk of waiting for Unity team to look or fix what's in the black box. If you talk about open source advantage in Unreal, this must be your intention or else the argument is not that strong because Unity's closed source turns out to be more extensible.

## Company owning a game vs not

In a nicer wording Unity don’t want to compete with their own user. Instead they made a demo project to test a use case on various things.

In Unreal undenieably when you see Fortnite, you would think you would have the same feature set and resources to make a complete game like Fortnite. If some feature would be sorely missing, then Fortnite can’t do that either. They must have some pressure to keep Fortnite a good game. So they must implement something new.

In Unity, user sometimes feel if the team had any **pressure **to implement something real quick at all, because they don’t own a game? Like the sunsetted UNET networking system with the new one only on preview. If Unity own a networked game, what will they do in this situation? Or the “new input system” that the team had been working on for 2–3 years. It is just a feeling, but can’t deny the “Wow, I am using the engine that made Fortnite!” feel.

For instance Unity can’t do localization built-in while in Unreal it is there. A game of Fortnite caliber should be able to accommodate multiple languages, and that feature should be there in the engine not from external bought packages. And yes it is really there. SDF text rendering is in UE for very long time too, while in Unity it is just integrated as a package not long ago.

## Project-breaking, reworking madness

This will likely be much better for new projects starting from 2020 onwards, but let me record them for historic reason.

Continuing from the previous point, In Unity, I would need something like I2Localization asset store package. And localizing is something that should be done while you make the game, if you decided to add it later then have fun updating everything and every text… it should be integrated and thoughtout in the engine to prevent this kind of “mass rework” which cost time.

And also imagine pre-2018.3 era, you cannot even reliably make the button the same instance. The button usually contains a text, and that problem connects with localization.

Start seeing this kind of "reworking" pattern? Imagine multiply that by more than 10. Let me tell you my own story.

*inhales* the first time I remembered the UI system was super bad with that IMGUI-in-your-scene, so I used NGUI asset store. Then uGUI caught up with still-bad tag-based sprite packing system, so I moved to uGUI with external sprite packer, while a part of my game is still NGUI. Then SpriteAtlas (asset) appears that makes the packing transparent and good, so I migrate again and have to relink all the damn picture I used in the project because all the GUID changed. (Thanks to VSCode I was able to surgery the GUID for the entire project but one-by-one per piece of sprite) Then, the font rendering system sucks. This is connecting with localization again of course. Then TextMeshPro came around which uses Valve’s distance field rendering, requiring a replacement of the entire game’s text, prompting an entire replacement of texts in the game. Then Timeline came, I ditched the yield return stupid sequencer I code up painstakingly and opt in to Timeline. But then (unluckily discovered later deep into the commitment) there’s no event in the Timeline! I then hack up a portal to activate the event from clips, then in 2019 where Timeline “Signal” came I would want to opt in to that instead. Also discovered Timeline could only “hold hands” with the Animator and non-legacy animation clips. There are some legacy clips I used for performace which became incompatible with the timeline, previously compatible with the manual code sequencer madness I was doing. To play animation simply I then need to create a TimelineAsset wrapper with one Animation track, or use [semi-official solution](https://github.com/Unity-Technologies/SimpleAnimation). Then Unity Package Manager came, I was using Git Subversion to share common code between projects. It was not good because script GUID cannot be shared and it unlinks the entire project with just a small mistake. When I moved to UPM basically all my shared code got unlinked for the last time, and I have to manually rewire everything. (and never again, thanks UPM) UPM also adds its own frustration, every time you do an upgrade you have a chance of strucking in the state where packages error, but because UPM is a package you cannot see and use the “Package Manager" menu to fix them, creating a deadlock of doom. This cause a reimport-all and various combination of pinpoint Reimport for it to work, typically costs around 3 hours. (I remembered because I did it enough time) Then the Resources folder system sucks because it is the only way to load things on demand at runtime, and it is a nightmare to maintain paths that it make sense. But we are all put up with it like it is so natural to load things from folder path, and carefully craft the path so equally ugly hardcoded string make sense. Then Addressable Asset System came, as I read the description I was drooling and wonder why I could put up with the Resources folder? Then I have to migrate Resources to AAS. I thought it would be easy, the API even said you can use Resources path as AAS key and it would still work. But no! Now everything are async-based. And your synchrounous code now have to be infected with callback hell. So it is not just “replace Resource.___ with Addressables.___” as advertised. Unity is not committed to C# async/await yet. Then I looked around for ways to minimize this pain and I found UniRx.Async package that would let me maintain linear code. I then go around and update Resources based code to awaiting the AAS. Oh, then the drawer for AssetReference broke that I had to write my own every version update. Updating AAS version also corrupts the previous entries I had built too, fair enough that it is in preview status so I can't really complain. Then there are some UPM packages that you must use the “staging” version, but some package like AAS if you use the staging version then it break your project and officially discouraged in the forum. Then, using AAS you need a better resource releasing scheme based on reference counting. Also this invalidates the asset bundle system, which is a good riddance (actually it is still hiding inside) but I have to learn how to host things the new way. Then adding UniRx.Async would break the PlayerLoop hackery that ECS package is doing. Causing more problems. ECS itself cause my entire game to be remade, for the better future. Nested prefabs again cause my multi-scene LoadSceneMode.Additive hackery to looks unbearable and I remade them into a single scene composed of prefabs properly. In remaking the UI to nested prefab I have to redo many animations because they are now linked differently. Next up is not Unity’s fault but the world had moved on to super long 2:1 screen and I was doing as long as 16:9 only, I had to remade many UI again to fit. Also in the process of this remade, Unity still doesn't have a proper support for the dang notched phone at edit time. I foresee a remake is coming so I made my own [Notch Solution](https://github.com/5argon/NotchSolution) so I could take care of the notch at the same time as this 2:1 rework. It is lucky that this change occurs at the same time that TextMeshPro became built-in, so I migrate them altogether in one go, and together with localization. (I was lucky with my timing, but imagine someone who decided to touch up the game a bit too soon as each feature came in...) ECS came with its own little apocalypse which I am happy to take the pain because I signed myself up for this preview, for the better API, but still it's an another rework. Almost forgot about Assembly Definition File, the idea is great, but a code that went too far is difficult to separate into asmdef without cyclic dependencies, so one another thing that should have been opted-in from the start but at that time it was not available. The asmdef feature also got increasingly better in each version, like now you can put in custom defines and dedicated test assembly. This again cause a problem in asmdef planning for my Asset Store item as I would have to wonder if the asmdef will be backward compatible or not. And crucial feature like ignoring invalid assembly instead of error will not be not backported from 2019.1 so in the end I can't even use it safely without dropping support for the "just 1 version away 2018.4 LTS" which will lasts for 1 whole year with tons of users, lol. In the latest 2019 alpha the asmdef just gain expression-based include, which I think should be there very early to prevent this kind of non-backward compatibility problem if I want to use the feature. In 2019.1, Timeline is becoming a package as a part of UPM movement, breaking many old code and plugins that assumes timeline is built-in and now needs using statement. 2019.3 the UGUI package is now needed to be linked everywhere. I could see an [official Localisation package](https://forum.unity.com/forums/localisation-tools-previews.205/) looming next year too, so a yet another round of "rework all texts in all scenes and prefabs" game by then. In 2019.3 the enter play mode is now lightning fast, except to use that it breaks the world again because domain no longer reloads, requiring all plugin owners that assumes the domain would be reloaded to [take action](https://docs.google.com/document/d/1QFMWHG05w7Rj8pe2nz5rbWUm1gj-Pd9M71Uz9dc-dg4).

Thankfully that I am not making a **networked** game. I have heard some more rants from people that makes networked game and “mistakenly” used Unity’s built-in networking solution and are regretting. Imagine how scary it is to wake up and see a big UNet text gradiented by nice “sunset”!

**Evolving multiplayer games beyond UNet - Unity Blog***Through our connected games initiatives, we're revamping how we can make networked games easier, more performant, and…*blogs.unity3d.com

In an ideal world it should be impossible for the user to make a mistake of committing into something heading towards its demise but unfortunately we all make mistakes. Think about this, what if I used the pen tool in Illustrator and one day they announce that the internal data structure of vector path is changed forever , and all paths made with "the old pen tool" will not be compatible with the new one and a conversion is not possible, you must remake it. That would be breaking the world. (But Unity do try to push a new motto "performance by default" where you can't just make a bad choice, let's see it happen.)

Or just read the comment of [this blog post](https://blogs.unity3d.com/2019/06/13/navigating-unitys-multiplayer-netcode-transition/) about the solution of what to do in this transition. Or [this new update post](https://support.unity3d.com/hc/en-us/articles/360001252086-UNet-Deprecation-FAQ) in April 2019. You can see the users are outraged and already fed up of this endless reworks.

Or the **Collaborate** function. The little dropdown around the menu bar. I think it had been advertised since around Unity 5 where there is a built-in source control that was said that it is better than Git or something else because you could merge scenes, assets, and you could do it all from inside Unity, concurrently while multiple team members are making games at the same time.

Sounds tempting, and I almost give in but I am still sticking with Git in the end as I worked alone and visible `.meta`

file plays nice with Git. I also remembered trying it as far as Unity let me do it for free, but I remembered the interface is very clunkly, sometimes doesn't update or requiring restart, where my Terminal + Git would already get the job done. Also I have worked with a game company which uses this feature and they said it brought more trouble.

And fast-forwarded to now, collaborate is now being rebuilt! I am grateful that Unity often comes out and says what went wrong, UNet and now Collaborate. But it must be frustrating for those who tried to live with the feature. New Collaborate is enabled by the recent UPM package movement which is currently breaking everything.

Enlighten the lightmap baker is [now being replaced](https://blogs.unity3d.com/2019/07/03/enlighten-will-be-replaced-with-a-robust-solution-for-baked-and-real-time-giobal-illumination/) too! What could go wrong from here? Read that blog's comments too while you are at it. And [reasons in the forum](https://forum.unity.com/threads/enlighten-deprecation-and-replacement-solution.697778/#post-4666784), before you start hating Unity for deprecating stuff. In there, you can learn a lot about pains from real users. Unfortunately I am mostly with 2D games, so I can't say more. (I used baked lightmap only once to make[ a music video](https://www.youtube.com/watch?v=VTj4O3cMJ9M) for hobby, but not in production.)

One relevant article about software rewrite here is an another good read : [https://medium.com/@herbcaudill/lessons-from-6-software-rewrite-stories-635e4c8f7c22](https://medium.com/@herbcaudill/lessons-from-6-software-rewrite-stories-635e4c8f7c22). I did chuckled a bit at the Basecamp part.

The comments are mostly in the same tone as this article : "I love Unity, but man, how painful it is when foundations after foundations collapsing randomly over time". I am not surprised at all why AAA devs do not want to risk their game with Unity's surprises like this.

Unity make this kind of move very often and is not afraid to try. The engine is going on a big transition and just starting to be usable, it is even more painful to not migrate to these new things when you know it’s there but you are still doing the stupider way. UE's release note feel more like a new extension rather than reworks of features.

The problem is that how could someone new choose the right one? There are too many traps in Unity. To name them currently :

`Text`

vs`TextMeshPro`

UI. You are doomed if you used the normal version.- Tag-based Asset Bundle vs Addressable Asset System. AAS ended up using Asset Bundle underneath but it save you from manual bundling madness and extremely unintuitive tagging way to determine which goes into which. Also using the bundle is the actual nightmare to code. When it works I am not even sure what I did.
- Default project vs LWRP/HDRP. If you switch to LWRP later on then all your textures may become incompatible. Also shader graph is only usable on LWRP which will make you switch later.
- If you don't make your game in packages early on, you are stuck with compilation and domain reload time of doom. It is because you could go to
**an another project**to work on a part of your game that gives UPM-based development an edge. But think about it, it is funny that I have to split my game into pieces just because the script piles up and add domain reload time on unrelated or even empty scene, that a workaround is go to a new project without scripts and use UPM to link back. UPM do make me a better coder however. The scripts are ready to be reused in projects in the future.

I wished these things are there from the start. Right now Unity looked much more reasonable, even though most packages are still in preview status I consider them **essential.**

My hunch is telling that Unity is far from done doing this big migration.

- UI Elements break your editor code next?
- UI Element runtime deprecates uGUI?
- New input system breaks uGUI event system?
- What will become a package next?
- DOTS-everything breaks everything?
- Nothing is compatible with Tiny Mode?

If you want to stick with Unity, you have to move forward with them constantly. (Or stick with LTS version, but new features are usually deal breaker since Unity was too incomplete to commit a version freeze throughout the project's life. I like that my project is becoming better overtime and my design has moved from monolithic to a more **ready for change** (agile) design. But as a result I have lose so much time too. All my subversions gone, my personal toolbox all became UPM.

This is yet another blog post which the comment section was lit on fire : [https://blogs.unity3d.com/2019/12/12/2019-3-is-now-in-the-final-stages-of-beta-testing](https://blogs.unity3d.com/2019/12/12/2019-3-is-now-in-the-final-stages-of-beta-testing). Look how everyone agree that 2019.3 is nowhere near release candidate that it cause this huge uproar! Unity has large userbase that are on the verge of switching away.

Each version has its own beta test forum. This 2019.3 in particular shows how deprecating without replacement and left the engine in uncertainty state comboed with Unity's own rule of "`xxxx.3`

version becoming LTS `.4`

version at the end of each year." This indirectly means they cannot left the engine in bad state for more than 1 year, or else they would have to long-term-support that mess. And it is happening now. Back when Unity started this risky journey around 2018, the 2018.3-4 survived because 2018.3 is just the right time that they landed improved prefab system and they haven't started breaking other things yet. ( `UIElements`

still stay in experimental, for example.) That make 2018.4 a reasonable version to stay on. Right now I cannot say the same with 2019.3, it is far from rock solid and too many things are half way done **all at once**. [Check out this beta test forum's post of 2019.3](https://forum.unity.com/threads/2019-3-entered-the-final-stages-of-beta-testing.792882/). I found the discussion quite civilized here and I agreed with many.

But Unreal is definitely more suitable for professional in this regard because it is relatively more stable, professionals may not want to always catch up and maintain the project to latest tech but rather just have to ship in time. You can freeze the engine and evolve it yourself by editing the source code if you really want a complete control, which is a very corporate-thing to do. Unity is for tinkerer and you take the risk.

## The looks

I have something I called "that Unreal look". I go to a certain indie game competition every year to see what the kids come up with. They are either made with Unity or Unreal, which every year I like to play a game of "guess the engine" before I ask them.

I get the game that was made with Unreal almost 100% correct. That Unreal look is unmistakable and it is the source of misunderstanding that Unity game looks like shit and Unreal is well, looks beautifully unreal. At an instant I saw a booth with FPS game, with (excessive) motion blur on turning head, and exposure adjusting when going out of the building, maybe excessive vignette, it's definitely Unreal.

Also the fact that big games put Unreal logo upfront solidifies that Unreal is darn beautiful.

It's just the default and lack of skills. The problem is just Unity has postprocessing as a package and all these kids don't even know they are there.

Unity show in its feature films that beautiful result is definitely possible in a hand of good artists. But bad artists with Unreal's default will always win over bad artists with Unity default previously.

Unity is changing this with pre-made scriptable rendering pipeline HDRP and URP so that it is harder to make ugly result. Now (2019.3) post processing (v3) is even built into URP without packages. I hope Unity gain better reputation from now on.

![](../../assets/c24e8725ddd3e2f9.png)

Watch this talk in full :

## Netcode

I am probably not an ideal person to ask about networked games because I have no interest in them. But apparently very high demand of this feature from other devs that the game engine must be able to do.

I don't know about Unreal, but in Unity the goto solution is to not just use anything Unity present and go for plugins and external solutions like Photon or game BaaS such as Playfab, etc.

### DOTS Netcode

You read about UNET deprecation already, because they are going all out with DOTS. In networked games its not like you are sending images frames over the wire, you are sending some kind of commands and communicate with server then server holding the game state communicate back along with data of other players. That's a kind of **data**, maybe you create a `moveTo`

packet so a client can express their intent to move to the server.

DOTS is data oriented. DOTS align itself with networked games perfectly, because now you program the game with the same thing as you send over the network (you can send a subset of them). It's all data!

However the problem is again, it's not now. Watch this talk how DOTS-based netcode will work. He shows client side prediction as well. Entities "world" seems to fit perfectly to debug network games, as you can make a server world or client world as much as desired inside one client. I am not a networked games developer yet I was intrigued how the DOTS puzzle piece suddenly fits together to use cases.

When this is ready, I think Unity will be very strong in this regards.

## Packages

**This is nuts.** If front-end web dev came and watch that clip they would react with a sigh of relief. How was we living without packages before? Apparently Unity was like that with just `.unitypackage`

to import (just kinda unzip and duplicates into the project) the same goes for Unreal with this [https://docs.unrealengine.com/en-us/Engine/Basics/AssetsAndPackages](https://docs.unrealengine.com/en-us/Engine/Basics/AssetsAndPackages) `.unitypackage`

equivalent system.

Before this point I was trying to utilize Git Submodules in a package-like style, but there are too many workarounds, no proper dependencies, no other ecosystem other than your own, no standards, and it dirties the project as it became a part of project nonetheless.

This now changes. Unity is now getting modern that they adopted NPM-like approach, called Unity Package Manager (UPM). (They like to attach U to everything, now there's also UXML and UCSS)

What's even better is that they transitioned their entire engine to this packaged approach and deliver the engine the same way we could write our little reusable package. That is no simple, it breaks the universe and everyone takes the transition pain. And it was, but bright future awaits.

I used to read Unity's version release note with excitement whether it will contain THAT bug I reported long ago or not. Now we could get updates from each of Unity's internal team delivered, with its own `CHANGELOG.md`

to read, out of release cycle, in parallel! I really like this. Also it plays nice with [Assembly Definition File](https://docs.unity3d.com/Manual/ScriptCompilationAssemblyDefinitionFiles.html) where it split your game into several dll.

The engine's modernized into packages, what about your game? Happy packaging!

- Packages can be reused on multiple of your own games and updates together.
- Even if you are not going to ever reuse it, single game specific package is still a valuable separation of concern.
- Packages can be tested in isolation thanks to ASMDEF per package that keep me from going outlaw. Stop circular dependency spaghetti hell in style plus other benefits.
- Local package reference (non cached) updates immediately. This open a new way of developing your game in pieces of multiple
**project**. Work on a feature in an entirely new project is now possible, then your main project just reference the UPM package. No copy, instantly synched. - Open source the package and bring the power of the world to help you? I have open sourced my
[Notch Solution](https://github.com/5argon/NotchSolution)as an experiment and I met many wonderful contributors. - Publishing can be versioned properly, receiving sides properly cache and reference a specific one NPM-style.
- All the way to Asset Store which will be transitioned to UPM shortly. Helps the package maintainer happy, and so easier time making money out of it.
- If I got a new outsource Unity job, the first thing I will ask them can your Unity version uses UPM and ASMDEF? Because I can now deliver my work in a form of packages completed with tests that do not have to see their multi-gigabyte game anymore. It will be easier to say something is not my fault. It will be easier to work in parallel.
- In the end this will be a good initiative to foster code reuse and code sharing community. No more having to post your source code in the forum to copy, for example.

### Example package

Basically `package.json`

because Unity utilized NPM in the back. The local import point to this file and the rest happen automatically, or you can even pull from GitHub URL. I could imagine a vibrant community made scripts being shared on GitHub which I could include in a project in seconds, and transparently because they will not occupy `Assets`

section of your project. This make your `Assets`

section truly **your game**. (Packages appear in a separated **Packages **tree, which you can mark your UPM as not displaying in that tree if you have nothing the user will want to see and maybe drag to the scene to use.)

![](../../assets/12a3923ca2ac63f1.png)

This is a example "shape" of compatible repository, containing `package.json`

at the root.

![](../../assets/8d01e698bce25a74.png)

### Packages and the forum

I had never been to Unreal forum, but Unity forum which was mainly for users, right now after this UPM movement, each package mostly gain its own forum and we could talk, suggest, and report to the devs directly.

This is huge, I could get personal with a particular feature's developer! Gone is the feeling that big company that made big program is out of reach and nothing we complain could reach them. (For example, I am sure don't want to suggest anything to Facebook or Adobe because I think it is a waste of time.)

I am impressed by the [ Addressables sub-forum](https://forum.unity.com/forums/addressables.156/) in particular.

`unity_bill`

who is a developer for this feature is very active and address (no pun intended..) ALL threads regularly. One thread I posted long ago I already forgot, he bumped the thread and say this problem is fixed in the next version. I mean, look at this. It's phenomenal!![](../../assets/4713eeccef072de0.png)

Or recently, the **Quicksearch** package which provides "Go To Anything" popular functionality often seen in IDE.

[This thread](https://forum.unity.com/threads/quick-search-preview.635863/page-4#post-4643404) is particularly spectacular, the turn around time of reporting bug is fantastic. As soon as he said a new fix is available it really is available on my Package Manager UI, press update, and it fixes the problem instantly! It's.. magical. Look at this, it's about an hour ago and it is already there.

![](../../assets/c25de26fc38ba6be.png)

It really highlight full strength of package-based approach. And currently I think even if I don't count just game engine competitors like Unreal Engine, but expands to other softwares, Unity is still among the earliest to adopt this modern design.

The [ Entity Component System sub-forum](https://forum.unity.com/forums/entity-component-system-and-c-job-system.147/) is also very active, and it is exciting that the CTO Joachim Ante himself is around to guide the early adopters since he is also one of the developer of this package. For ECS feature in particular, if someone says that ECS way is slower than mono then he has to debunk it immediately. Since if that ended up to be true, it would defeat almost the whole point of ECS. It's great to see he is not letting any thread that question performance passed by. Also threads about usability get answered, and the dev team could feel by themselves if these thread is difficult to answer, then the API needed more work to be friendlier.

[TextMeshPro forum](https://forum.unity.com/forums/unity-ui-ugui-textmesh-pro.60/), which Unity brought the developer of this previously-plugin to be an in-house dev quite some time ago, has a very dedicated staff that you could feel he is giving his all to provide us the solution.

Having devs that knows exactly what user is talking in a sub-forum that begs for outrages due to huge workflow change, like [Prefabs sub-forum](https://forum.unity.com/forums/prefabs.158/) or [Timeline sub-forum](https://forum.unity.com/forums/timeline.127/), is big.

Back then when the forum is just General Discussion or something like just "Audio" it wasn't this constructive. One to one mapping to packages is pretty nice. Google search hits them more. We can ask for features or discussions, not just reporting bugs. Unity people can just look in one forum instead of having to check the General Discussion constantly in the midst of "free the DARK theme".

If you watched many of Unite Copenhagen 2019 talks, a recurring theme noticable is "thanks to feedback in the forum...". Project Tiny collapsed multiple times in its experimental stage until it arrives at this DOTS runtime stage. The forum drives development. (Still some UE folks says any kind of trial and error iterating/restarting over with real users is unprofessional because it shows your failure side, etc.)

### Stemmed from packages : "Unity's default sucks"

Even with undeniable advantages explained, I still seeing some UE users keep saying something like why Unity has nothing by default (even more "nothing" after this package movement), why must I suffer a hassle of installing a package? Therefore, UE is better.

Think this way, it's actually good that the engine is not bloated by default (and it will pave way to something like Tiny Mode, where you only have a few packages in the build). Base installation is just 4~5GB with only Standalone build selected. I could imagine a feature like Cinemachine if on UE side, it would be strange for that to not be a built-in. (because realistic stuff, etc.) The wrong reasoning of UE people who are not used to packages is that, he feels like packages are "add-on" and unofficial. Therefore, a game engine that **requires **an add-on to perform decently, cannot work fully on its own, and therefore sucks and is unprofessional. Actually it's not embarassing at all to build your software from pieces. The world run on open sources, and they are mostly considered packages of sorts.

### Preview Packages : Preview by default

Right now (2019) you will notice that there is not much in Unity Package Manager, until you press Show Preview Packages, the ultimate button of wonders. When you do this, you entered **not production ready **area and it even labels the top of your title bar with a big **[PREVIEW PACKAGES IN USE]**

The thing is all the goodies that make Unity competent are in here! ECS, new input system, addressables asset (out of preview in 2019.3). Few got out of preview like Lightweight Rendering Pipeline. But even so, many rages when they hit a blocker that prevent them from publishing everywhere they go because they used a preview packages.

Even occured to myself. I think I could get away with it if I use it for "just a bit". No, you will probably not get away with preview packages. Someone [successfully used ECS in production](https://forum.unity.com/threads/unity-ecs-and-job-system-in-production.561229/page-2#post-4711196) doesn't mean you could. I used AAS "for a bit" by having just scenes in the bundle group and nothing else. [I found a bug](https://forum.unity.com/threads/is-it-possible-that-il2cpp-broke-null-but-not-referenceequals-x-null.705398/), that took me 3 days and I didn't think the culprit was AAS.

Why people wants to risk their project with preview packages? It's simple and goes with what I said before : It's because **rework** is immenent. They see if they use this package early they don't have to rework the game later. (Because packages are like Unity, like AAS or ECS, they completely changes how you design things and loves to break everything) But trust me, **resist the temptation** and just follow the development from a far is usually better for most devs.

There are few exceptions. I choose to remodel my to be commercial game for ECS because I want a reason to learn ECS seriously along the way and I know I would be lazy to learn if it is not tied to my important game, so I made this gamble. Even if that cost the game to never be released by an outside factor like having to wait until 2022 that ECS is publicly released.

Some safe to use preview packages are one that affect only editor like Quicksearch, or Immediate Window, or Device Simulator. These are safe toys for you to play with generally. I had fun with them with zero risk.

Also, production-ready packages like the built in Timeline **doesn't mean** you will not find any blockers, lol. In 2019.1, Timeline is a package and wasn't marked with Preview status. But over the course of 3 months I found too many bugs that are critical like Control Track that doesn't work properly, sometimes Animation Track do not sample its last frames when the play head goes too fast or lagging, frame of even number not evaluating, Audio Track do not play their first few samples, etc. AHHH!!

### Backports aren't as often as you might think

Imagine you are using a verified packages. You found a bug, you report it, and they replied this is fixed in version x.xxxx that is a beta and also 2 versions ahead of you.

Theoretically the packaged approach allows the fix to be backported more easily in only the area you wish could be fixed quickly. It should be heaven for the bug reporting feedback loop that make both Unity devs and the game developer happy since they could precisely inject the fix back to you without touching other things. But personal experience says this is not always the case.

You can no longer complain something since the bug is already fixed **in the future version **it is just that it wasn't backported to the package in your version yet. One example is Timeline package where all the bugs I reported were fixed and verified for 2019.3 and 2019.2. I am happy that Timeline is now a package and expect the fix to come back faster than ever. But I have waited for half a year but there is no sign that the package in 2019.1 would receive that fix. (It maybe wiser to just modify the code according to that fixed future version and verify the fix on your own.)

Since April 2019 to October, it's finally time to ship the game and I am still waiting for packages bug fix to backport. Finally I hit an another Android build bug that requires me to go up to 2019.2 and finally receiving the fix I have been waiting for. (while the one in 2019.1 I left behind is still not getting backport...)

### But still I love packages

I have listed all pros and cons of packages, where as far as I know Unreal has no equivalent thing. Some topic like "preview by default" just take time for the team to finish them. Overall I am very satisfied developing my game with packages. It encourages quality code and an engine that could enforce this to you (as opposed to let the language feature enforcing you) is a good engine.

## Prefabs vs Blueprints, a performance comparison

Blueprint is viewed as kinda prefab in Unity, **UX-wise**. But as I said before that's a common misconception for the actual thing they do underneath. Blueprints are more than Prefabs because it is a C++ codegen system. Where prefabs in Unity is only a data container of sorts, containing how to assemble assets together by their GUID in their `.meta`

files at runtime. (Same as "scene", actually 2018.3 prefabs are all on the scene backend.)

### Composing your game from pieces

Unity shipped improved prefab workflow as of 2018.3 where you could nest, make variants, and edit in isolated environment. **It is awesome.** After using it I think I cannot go back to the old, “no more than 1 layer !!”, stupid prefab anymore. [Megacity](https://unity.com/megacity) demo is impossible without this new prefabs, and here I am not surprised why previously there are so few large scale games made by Unity.

That's the actual hell for UI design where you must choose either make the button a prefab and nothing else, or make the panel a prefab but bake the buttons and make them cursed of not being to receive any more updates ever again.

You see how that sounds very stupid, and that’s true when I said Unity just been able to do this stuff to my brother that has no idea about Unity but is an architect, and he replied “lol that sounds like a feature that should be there in the first place”. (He used several CAD programs which could do layered object instancing, like it should be able to.)

But in UE, the “prefab isolated view” new in Unity 2018.3, is already there. I guess from very early version?

![](../../assets/48a3c78630ad0826.png)

In UE you do C++ first to make a functional Blueprints, then you can connect up visual scripting and spawn Blueprints to make a game. In Unity as of 2018.3 you would make each prefab the similar way and compose up a prefab in the scene and connect using exposed variable slots.

Graphs in the Blueprint became your code, plus your thing. In prefabs you script a code and attach to your thing. Unity did promoted Bolt asset in the store as a goodies for purchasing Unity, so maybe the official one is still very far off. And again, Bolt is no comparison for Blueprints as Bolt is a visual scripting to program logic, but Blueprints generates code. Unity is going all out with DOTS, and visual scripting in Unity will generate DOTS system/component code.

Why codegen is a big deal? Because you can't go wrong! The generated code **must** produce an efficient C++. There are many places that could go wrong when Unity user writes `MonoBehaviour`

to paste onto their prefab.

In 2020.1 prefabs will be upgraded further with prefab in context. So you don't go to a separated scene but just edit the thing there. I don't know if UE can do an equivalent of this right now or not?

![](../../assets/a1c9e49dd54f2f5d.png)

### You can compile each individual Blueprint

Just from seeing the compile button, I feel like this is one step ahead of Unity in both modularity, AND **assembly management. **If the “enter play mode” of UE is lightning fast thanks to this design, I wouldn’t be surprised.

It takes isolation to the next level. Event system for example, in Unity you could use `EventTrigger`

, `UnityEvent`

, or the new `SignalReceiver`

. But the interface presented that you can select the method to invoke is a result of compiling the **entire C# project.**

![](../../assets/ec8cac9f42e372f4.png)

But in Unreal, it can immediately show that a function does or does not exist. You can go script it and make it exist and then hit compile just that thing. I can imagine a lot of optimization that is possible in the engine with this design. In Unity, various things are gated by the big assembly it requires. (The UPM deadlock nightmare for example!)

![](../../assets/a177a28e0adb9b24.png)

### Code-gen visual scripting is coming for ECS

Unity is doing similar approach to Blueprints that an ECS visual scripting graph would produce C# system code. ("System" is the thing that work on entities in the new DOTS paradigm) You could read more in this post.

![](../../assets/408f7911d6cc03aa.jpg)

How does it compare to Blueprint? Both generates code, but ECS System code do not carry data but work on data coming from anywhere, inside its `World`

the system was placed in. UE's Blueprint code includes data fields because it is an object-oriented design. Let me remind you again that ECS code gen will not directly solve assembly reload time of doom.

However that's not an upgrade to the prefab, the current topic we are talking about. (But since Blueprints was compared to Prefabs and Blueprints has visual scripting so I had to...)

### Prefab as memory-ready prebuilt data

This is an exciting upgrade coming for prefabs itself. It actually goes one step ahead of UE's Blueprint codegen, because these Prefabs they skip the code and go straight to become memory data!! So the idea is, nothing could be faster than just putting a pre-made memory into the game hardware memory at runtime, where this data was made at game's building.

(For UE Blueprint codegen or regular Unity Prefab, the code would usually then allocate data and setup your things as designed in editor, **at runtime**. It is costly to resolve all the links to your assets.)

It's all beautiful linear memory access blasting through the data

What sorcery is this? So there is always a catch. Those prefabs must be ECS compatible. (Has "data" representation, not just any prefabs.) The stunt is possible because ECS is data oriented and now your "thing" is just a block of data, whenever that appears, the System is ready to work on them. You could just casually stream them to appear over time, as long as it appears in a unit of `Entity`

it's all good.

Currently, Unity use something called "Subscene" which all prefabs inside it could become memory, and this memory would ship with the game. Though it is strange wording-wise that "Subscene" has more high-tech feature than the actual Scene feature.

## UI Authoring

### IMGUI

![](../../assets/e79ed51ebd91c127.png)

It's really bad.

### uGUI

Unity's uGUI WYSIWYG `RectTransform`

designing is one of the thing I really like. I couldn't think of more appropriate way I would like to design my UI. (Until I see UIElements) So how it works is that we use a giant plane of GameObject floating in the scene that could be layered on top of your game, then you have got a UI! There are many components to achieve your desired design. You feel that this is a lil bit strange, but goes along with it since there is possibly no better way?

However we don't talk about performance. Explained in the next section.

### UIElements

This clip says it all why this is awesome. Look at that live reload. It is not even a reload since the renderer just render. There is nothing to diff to "reload"...

A revolution. Now we do front end in Unity! Because UI is now defined with HTML-like "UXML". Styled with CSS-like "USS". And then rendered with a proper UI layout engine [Yoga](https://yogalayout.com/).

What's wrong with uGUI?

**Design wise** it may got reasonable after 2018.4's new prefab system. (Of course I want the buttons to be the same one with different text)

**Performance wise : **

- uGUI is an attempt to bake UI into Unity's GameObject concept. It is a massive tree of GameObjects trying to make each other behave in a way that's not just a simple classical transform hierarchy (that could be efficient with matrix operation). Turns out to be fitting round peg in a square hole.
`RectTransform`

, an invention that trying to fake classical Transform to think they are all a rectangle cause ripple effect on API design and performance. As you read[Unity UI repository source code](https://bitbucket.org/Unity-Technologies/ui), you start to feel that "this is not it" that each component is trying to relay information to each other messily, yet they went this way too deep to back out.- Components sometimes wants the sibling and not the child to adapt to each other (i.e. the "flex box" behaviour) where
`GameObject`

transform tree wasn't designed to efficiently enables that. - Input handling is servicable enough since
`GraphicRaycaster`

did far more simpler check than even`2DPhysicsRaycaster`

which could be use for raycasting to a rectangle, but still could be improved if we didn't rely on GO tree in the first place. - Rendering is hard to optimize because it work together with shader that comes with
`Image`

component inside the tree. z-index when rendering is figured out by game object ordering, seems intuitive in some case this turns out to be painful. (Imaging a 3d card game where your hand usually be an overlapping cards horizontally, then you want the selected one to be on front but stay where it was horizontally. Now you can't because the game object ordering is already used for horizontal layout.) - Lastly every little thing you do randomly cause or not causing layout rebuild (visible in the Profiler) of an entire tree. This is because the system is too relaxed as a
`GameObject`

, there are many possibilities for outsider such as Animation/Playable Director/scripts to change any rect that affects multiple things. A built-in UI specific animation system (like CSS-authored animation) enables more performance because the UI "knows" they are coming and what to behave layout-wise. Not just "Oh no something changed? let's refresh the entire thing, haha!" (This is kinda equivalent to pre-React/Angular/Vue/Svelte/whatever era of web design.) For example, I once added a little visual animation of white rectangle running on the edge of UI, then fade out at the end. The fade out ended up causing massive performance hit! I changed the fade out to scaling Y from 1 to 0, equally gives disappearing impression, but this time no performance hit. The reason is probably draw call something something, but the main problem is that this kind of unpredictability should not happen, no matter how flexible I can mangle the UI at any point I am allowed to do. It's better to**not**allow me to do non-performant things. - In summary with uGUI you have to always be aware of performance yourself. What breaks batches? Any little text inbetween UI in the same atlas? Will that changes mid-animation? In this new "ecosystem" it is even possible for Unity to atlas everything you need at edit time. (Please make it take account of SDF text too! I hope!)

Edit : I wrote all that but just found out this talk which sums it up very nice where exactly is the problem in UI in games.

Overall I think UI is a unique problem and cannot be made generic and "Unity-native" by forcing them into GO. New one using Yoga open source layout engine that's designed for UI is already a good start.

An another plus is that this `UIElements`

system works for both editor extending and runtime UI for your game!

Editor UIElements is already usable. Runtime UIElements is stated to be ready [in 2020.3](https://forum.unity.com/threads/ui-roadmap.735338/) or something. Can't wait!

### Unreal's UMG

I didn't try it yet. But I know someone who is trying to program UMG (Unreal version of uGUI) and ended up with a huge zoomed-out graph and he think that visual scripting is not a natural design interface for this task. If it was just a code it would be much more easy to understand. (Visual is not always the best presentation for everything.)

One thing I know is that I liked the UI in Monster Hunter World and Kingdom Hearts 3. That says UMG's possibility is not shallow. (in the case that they used it.)

Performance comparison, I will need to dig deeper into both UMG and UIElements source code how will they compete in various situations. (like animating UI)

## Visual/graph scripting

Performance of codegen Blueprints asides, now onto subjectivity of visual scripting UX. Do you like creating game by connecting graphs? Or are you a coder?

The advantage of visual scripting is that it gives you directions. It can go “this way” or “that way”. Plus you can see connections.

But sometimes all the logic needs to communicate with you is not directions but **reasoning**. Top-to-bottom text based presentation (that is coding) may be better in many cases, but you cannot see connections. The connection the coding way got is “line” which flows from top to bottom. If you are a code-person it even feels “visual” when looking at lines, it does not have to be literally visual.

Unfortunately most who claims "not a code-person so I need visual scripting" are just fearing lines of codes without trying. They just want a rectangle to surround something.

But why for **shader** design visual graph is considered the “standard” presentation? I think it is because you often dissect and mix/merge things, that it benefit from the connections. It is not always the case in coding, where if it ended up “waterfall-y” then visual scripting is having disadvantage against pure coding. Coding is exactly waterfalling from top to bottom plus jumps from method calls. Visual graph is not always an appropriate representation of what you want to make.

## Shader authoring / Shader graphs

![](../../assets/4f8f49b46c5ab9df.png)

Unity is now even with Unreal in 2019.3. Previously their roadblock is probably that resulting shader from the tool will be usable or not is heavily tied to rendering pipeline which was monolithic and closed source. They change that with Scriptable Rendering Pipeline (SRP), which still could be varying from project to project depending on how the dev script it, and if they made a shader authoring tools whose project will the generated result fits to? Now that they got SRP done, they can make a "recommended" prepackaged and hard to go wrong SRP called URP and HDRP. Finally, by having that 2 pipelines, they can **finally **make an authoring tool that they ensure those 2 pipelines understand and ensure their intended purpose. (URP = should run on everything including mobile, HDRP = beautiful) See how far Unity has come... it's finally here in 2019.3 folks!

That's not all, they even made the URP itself ..scriptable. So instead of doing SRP from start, you use URP to ensure support with shader graph and guarantee good performance coverage first, then add your own thing from there without touching what URP linked with toolings. If that's not enough, you can even add just a new render pass in that scriptable bits.

![](../../assets/96759316e6310e09.png)

The damage has been done for a very long time however because UE could do it from very long time ago and therefore UE was more of a professional tool.

![](../../assets/685e362f85c20a66.png)

It’s right there! As I double click the shader a very promising UI pops up. Unreal has no aforementioned rendering-dependency problem because UE rendering pipeline is not scriptable, and if you go change UE's source code there are chance that this entire tool will generate an unusable shader. Shader always depending in a not so flexible way with rendering.

Here’s a basic example of a material with a few nodes. *viewport contains some post-processing effects. The gradient on the line looks nice, the interface is vectorized. Personally I like angled line more than UE's bezier line, but maybe that's just me. Nodes available to play with cannot be commented, since I didn't get very far on both Unity or Unreal.

![](../../assets/a2fa290813bee348.png)

## Visual Effects / Particles

The game looks AAA because of explosive visual effects of millions of little things always going on in the screen. That's particles! Authoring satisfying effects is a job by itself, and when it goes with the character and sound you made a good game.

Unity originally had [Shuriken](https://docs.unity3d.com/Manual/class-ParticleSystem.html), and UE had [Cascade](https://docs.unrealengine.com/en-US/Engine/Niagara/CascadeToNiagara/index.html). Both with curiously the same less-desired approach of authoring it. So they give you a stack of things you could and you tweak the parameters. Then the machine follows and do things according to it. I don't know about Cascade but Shuriken runs on CPU. Imagine you make a rock shattering effects, the CPU must move every little bit of purely-visual rock bits according to this curve while scaling down every frame. It sounds like a very wasteful thing for CPU.

A better solution is offloading the work to GPU. We trick GPU to do math work for us with compute shaders, then we render it really fast because we are already in a rendering unit! However we don't want to write compute shaders so most wanted a codegen from authoring tool where they could work more artistically. Some cons includes we cannot access game things ("readback") but as the name says mostly "visuals" is for show and not for interaction. An another cons is the need for GPU that can do compute shader itself, so low end mobiles couldn't do it. And so the tool to make this must generate a shader file for efficient runtime use, but also enables preview and instant change while designing. (We can't afford to compile every little bit of changes, that would be annoying..)

Unity provide this solution production ready in 2019.3 called [VFX Graph](https://docs.unity3d.com/Packages/com.unity.visualeffectgraph@latest) while Unreal has [Niagara](https://docs.unrealengine.com/en-US/Engine/Niagara/index.html) solution from quite a while ago.

I have used VFX Graph in a (fodder) project that I specifically start in order to evaluate VFX Graph quickly, which I did in 2 days. I would says I underestimated it. Unity normally (haha) not making a UX **this **good.

Both VFX Graph and Niagara provided a graph-based designing approach, which personally I think is the right representation for effects design. (As opposed to scripting, visual scripting by graph I think is more controversial if it wastes more time than coding and less flexible.) This is not the same topic as shader authoring as also commonly edited as a graph. (Unity can also connects VFX Graph to Shader Graph anyways.)

![](../../assets/23a1aea5682fc032.png)

VFX Graph interface is vector-based, can zoom in as much as you like, fonts are crisp, colors are automatically sprinkled in just the right amount (something I liked a bit more than Niagara aesthetically), and it's DARK even if you didn't pay for Unity subscription (lol). It is almost like a glimpse of future Unity somehow sandwiched into the current era. You can make a proper reusable "subgraph" component, nest things as much as you want. It is possible to add comment sticky notes. It is possible to expose values to the outside, or to the other graph that ended up using this graph as a subgraph.

If you wanna look at that fodder project here it is. There are a lot of little particles around that center things and a lot of floating dust all over the scenes. Those are compute shader evaluating on GPU generated from VFX Graph.

I didn't try Niagara yet so I cannot comment, but for the look of it (image search via Google) functionally it is the same as VFX Graph. But in the docs it says it supported codegen for CPU workload too. VFX Graph says this feature will come later, the current focus is on compute shader. For CPU particles for now Niagara wins since it could also generate one, in Unity you have to use Shuriken for the time being.

## Sequencer / Timeline

**Sequencer Editor***Sequencer is Unreal Engine 4's mult-track editor used for creating and previewing cinematic sequences in real time.*docs.unrealengine.com

Unreal got many practical sounding tracks like dialogue, subtitle, layered animation, and even could record animation takes like a real movie editing program.

In Unity we get barebone tracks like activation track where it just set active on the present of clip. It seems to invite you to create a custom track, however amount of learning required is crazy. Even the component that plays the timeline is called `PlayableDirector`

. I witnessed firsthand on showing this feature to someone and he exclaimed "playable what??".

Then when I explain you have to make playable asset which is not a playable yet, but a magic container containing more containers that are clips and also a tracks, they are not the real thing but will become real when the outer layer timeline which is also a playable asset ask them to and connect to graph ports, then also bindings and output shenanigans it is getting confusing which is which form of which. And which level you can safely extend.

For example I tried making my custom playable asset type, which could be materialized into a file successfully, but I was not able to edit it in the Timeline tab. And also many audio-related things are hard coded, so you could subclass them but have to hack your way to the underlying data so that the hardcoded Timeline source will read it. You can't make it from scratch while conforming to some interfaces and expect it to work.

The API has high potential, but the whole castle is difficult to understand. In fact I think digging the source is faster than trying to read the docs but unfortunately only `Timeline`

part is available to real but not `Playables`

. I will not forever know what the heck is inside `AudioMixerPlayable`

that does the magic with connected `AudioSource`

binding.

In Unity's fasion, when Timeline first arrived in 2017 everyone was excited and now Unity could potentially do cutscenes or make non-game movies. However for games, it lacks event which didn't arrive until 2019.1. For cinematics, it lacks proper child track and additive track. The "Control Track" is nice and looks like the key to end it all, but on closer inspection it is a band-aid at best since what it does is to ask the other `PlayableDirector`

to play or destroy a completely different `Playable`

**together **while playing the current timeline. It's not a real "inheritance". The grouping feature is there, but to just help you fold and organize your BIIIIIG (vertically) timeline.

And also, see this thread where Unity's mass-demolition of features affects every ETA in existence include the Timeline team. Luckily when packaged it should go more smoothly from now on. (Now = 2019.1 ~ .2)

Also despite Unity advocating it is animation ready and animation studios are using Timeline + Playables + Cinemachine to make awesome things, there are of course bugs in your way. Like [this one](https://issuetracker.unity3d.com/issues/audio-track-is-missing-some-samples-if-it-starts-at-the-first-frame-of-a-timeline-in-player) that make all audio track always missed first few samples. (I have been waiting for this to be fixed for years... no one can make playable-based audio code until this is fixed or all your short sound turns into complete silence. Crazy!)

## Multi Threading

Both Unreal and Unity will have a part of engine code that your game touch that ended up utilizing threads. Moore's law slow down and more threads are added instead even on mobile so it's great if we can use them. In Unity, UI layout, audio mixing, culling, transform system and so on would use threads (that was already spun up at start) for you. Your game definittely touches these threaded work more or less.

But this section will talk about multithreading your own game code. Multithreading explicitly, any work. How possible to do this from both engines?

I am sorry UE fans but I think Unity had delivered some serious usability threading upgrade with the HPC# subset design. It changed the perspective that now “now everyone can thread!” just like AirAsia said “now everyone can fly!”.

I have read how to do threading with UE and it looked like a typical threading nightmare you would expected.

**Multi-Threading: How to Create Threads in UE4 - Epic Wiki***Edit description*wiki.unrealengine.com

But C# job system, it might irk you that you have to use struct or you must copy things, but it strike the balance between performance and non-frustration coding experience quite well. No race condition. No memory aliasing. Automatic dependency warning. This is a fool-proof multithreading API that you can finally put your game logic in.

**Job System & ECS - Unity | Unity***Unity is the ultimate game development platform. Use Unity to build high-quality 3D and 2D games, deploy them across…*unity.com

In Unity, you don't even have to spin up a new thread and manage it. It uses Unity's "worker thread" that it already is using for engine stuff. When they are not busy, they could do your custom work. This is great not only for reducing headache, it manages work stealing/scheduling automatically for you. (Flashback to that algorithm class!) C# could spin up a thread, but C# Job System that use the already existing worker thread is just better imo.

And if you use ECS, you will thread more naturally with automatic lockstep that avoid write dependencies magically. (The `JobComponentSystem`

) The downsides is that all these tech are still in preview. New comers probably have no hope on avoiding all the gotchas.

Unreal CEO himself have some say about this too. UE's user code is strictly locked on a single thread much like what you wrote in `MonoBehaviour`

before, but that doesn't mean it's bad because it constraints complexity. And also some code could be from Blueprint meaning that the performance is in control and hard for user to go wrong. The generated code from Blueprint can even use threads for you safely. (Can't confirm, but it is very possible and Unity doesn't have code gen so everything you typed in `MonoBehaviour`

will be 100% main thread.)

He says more that concurrent language like Erlang is not suitable for game since game needs atomic sync point often.

## The language : C# vs C++

C++ has been synonymous with “performance” and most assume that Unreal must be faster. But previously, Unity was slow because it often travels back and forth between C++ and C#. (Mainly the call to `Update`

) Now with the UPM movement, it stays in the C# realm for longer.

I think people clouded their judgement too much on the performance aspect attaching to the language's name. We should instead consider the language's feature and how that allow us to express ourselves. C#? Strong type declaration and compile time checking, sometimes too strong. C++? Flexible pointer operations and memory manipulation, sometimes hard to understand or connecting imports. These are valid advantages and reasons for loving the lanugage. Far too many times I see UE diehards simply says "we use C++, the faster, pure, and original language, and you sucks". When I says something that leads the conversation to pointer advantage of C++ and therefore make it a superior language, I said C# has `unsafe`

and then you can do the same thing full of `*`

in your code as the finishing blow and they don't know what else to say other than "anyways, UE ended up faster". So it is not the language afterall! It's the tech and codegen that makes performance. Then this is now a valid point to criticize that C# is slower.

Also with ECS, you could make the majority stays in C# **WHILE **getting a good assembly with Burst that could beat C++’s assembly. You see, everything became an assembly so it does not matter if it is C# or C++. And Burst is trying to make C#’s assembly competitive. ([Read more here](https://gametorrahod.com/burst-and-the-generated-assembly-how-smart-is-it/) if you want to see that assembly, see if you could handcraft C++ in Unreal to beat it?)

[Unreal CEO said](https://www.reddit.com/r/unrealengine/comments/aezhdv/it_seems_people_at_epic_are_considering_adding/edxha25/) he liked simplicity of C#, but don't like that the data has to be linked to the actual C++ implementation. That's actually the trap Unity already falls into because `MonoBehaviour`

also got C++ database underneath. [Unity CTO also acknowledged](https://forum.unity.com/threads/why-can-the-subscene-of-the-ecs-improve-load-times.686893/#post-4595524) that the foundation of `MonoBehaviour`

was bad. And Unity is now eliminating that with ECS where the database is entirely on C#, for all objects (`Entity`

).

### Preference

If you love C++ then you probably love Unreal Engine. (?) But I don’t… my experience with C++ the entire life was not good. Naming convention irks me. And I made too many mistakes.

I don’t have any good memories with C++ throughout my master degree study (where I use it for OpenGL and Caffe stuff for neural nets.) so obviously I will be biased towards C# ! So from here I would like to mostly advertise C#.

However Unreal C++ is not as brutal as your previous experience, there are macros to help you. And most importantly Blueprints to help you get the best code.

### C# 7.3

If you are **open minded **and don’t mind any of the languages, then you will need to see what civilization in the latest C# that Unity just supported.

The most powerful and game-changing in my opinion is `async/await`

. If you are coming from JavaScript then you know how useful this is. The key point is that it returns the value to the left side after awaiting, making `async`

code linear.

Even if I like C++, I can imagine programming much faster with `async/await`

. Also I like how tuple syntax works. Firebase Unity comes with `async/await`

compatible API and that’s a huge boost in productivity. I don’t know what Firebase API looks like in Unreal/C++.

### Unsafe

One of the most popular claim about C++ is that you can use pointers rather than reference type variable. You don't want that pesky Garbage Collector. Yes, you can go `unsafe`

if you want to do pointers in C#, if that is the reason for C++ for you. The `*`

deref syntax is the same. `void*`

is there for you. They even give you an `IntPtr`

as an almost-`unsafe`

alternative.

The majority of Unity ECS code (C#) is in `unsafe`

scope and used pointers a lot. With Unity `asmdef`

, the `unsafe`

can be contained in a small scope. (C# `unsafe`

requires an assembly-level toggle, previously a problem since it makes your entire project unsafe. Not anymore with `asmdef`

.)

Also it is possible to do `unsafe`

on C# Jobs system mentioned earlier to do threaded pointer gymnastics. When checking the generated Burst assembly I could say it is no different from handcrafted C++ code, so the point about "C++ for performance" is not true.

Lastly Unity made some methods like `UnsafeUtility`

to help you do malloc from safe context. So this point is mostly moot.

### GC

If garbage collector is the reason of C++ for you, the latest 2019.1 Unity gives you more control of GC, you can temporarily stop it. And it became incremental, whic free garbage in smaller amount but more often than before, reducing spikes.

More, if you use ECS then your **data **is arranged in a way that GC cannot touch in the first place. Also, Unreal has garbage collector too.

Other reason for C++ might be the C# language restrictions, like multiple inheritance. And maybe C#’s verbosity. And maybe you hate C# `interface`

that it couldn't do what you want. (default implementation, inherited generic constraint, etc.) That’s a fair point if you would like to use C++ over C# because of those. But I had already jumped on the Data Oriented Design train so OOP concept like inheritance is not of my interest any more.

For other C++ advantages, if you are C++ expert then you may know more but I am not one. So I could not recommend you any more reasons for C++.

### Nuget

You also have NPM-like repository for C#. Unity supports .NET Standard, if you found something .NET Standard it would be usable in Unity. For example you may use popular library like [Newtonsoft.JSON](https://www.nuget.org/packages/Newtonsoft.Json/) or [LitJson](https://github.com/LitJSON/litjson) without a problem. Anyways, UPM sets to be an equivalent of Nuget with things that works 100% with Unity.

### Code documentation

If you are a documentation freak and like to tidy up your code the way you like to make your room orderly, I think C# is good for you. The XML code documentation is verbose, but the resulting integration with intellisense, etc. is great. I enjoyed seeing the code say something back to me as I type.

You can make link to jump to other code, you can use markdown that shows up properly in some IDE, and editor like VSCode can ease the verbosity pain for example typing just `///`

will expand to a big XML template depending on the thing under your cursor. Then mass-refactoring works throughout the documentation too if you get them linked right.

I don’t know if in C++ it is as civilized or not. But it is a blast creating UPM package fully documented for myself in the future to read on Intellisense.

![](../../assets/358f809db769cc1c.png)

## Data-Oriented Tech Stack (DOTS)

Unity is clearly trying to step ahead of Epic Games on this one. I can’t find something similar in UE that boldly tries to change up how you code the game! Here's a brief history how the team ended up embarking on this crazy path : [https://www.youtube.com/watch?v=7ons0eVjhDY&feature=youtu.be&t=1910](https://www.youtube.com/watch?v=7ons0eVjhDY&feature=youtu.be&t=1910)

For those new to these things, there is one thing very desirable for all games : **performance**.

Where is it? Of course you can upgrade the CPU by overclocking but it is not the game's task. You can write better code, which you should. Better code use less commands to achieve the result. Even if we write the most beautiful code maybe the resulting assembly still sucks and you don't want to go fix it at that level.

Then there are data to be read (which those assembly reads), your game can't came from nothing, or you are not gonna make any games that do not remember things. (so you use variables) At the deepest level, cache** **is the fastest memory available located near CPU. Therefore if we can abuse the cache then the game is fast. Cache miss came from the source data not being close to each other, usually a by-product of OOP where each allocation just go to where they want.

Supposed we got our cache abused beautifully somehow what's next? All that but multiplied. You hope that the cache-abusing database and the code, somehow works in parallel according to how many CPU cores you have. Do everything, at the same time.

These 3 things : cache, code, and multithreading, combines into what we ultimately want. For the game to be fast or if it is fast enough already, it is then able to run on lower-end device, or if you don't care about lower-end device, cost less energy consumption. (Don't say you don't care about energy consumption!)

Assuming all those are in place now, the final touch is that it should be reasonably easy to do all 3 things. Multithreaded programming, that correctly access beautifully lined up data, that generates efficient code, is not an easy thing to do without bugs.

But Unity sets out on a big jorney to enable all of them at the same time. Big enough to deprecates everything and annoy users over a past few years and Unity is not stopping. Three components : Burst, Entities, and C# Jobs System will enable this.

Burst is a transpiler that ensure good assembly from C# custom-fitted to each mobile device with awareness of Entities and C# Jobs System (so that other general purpose compiler couldn't match). Entities is basically a new API to create things instead of `new`

. If you always go through the entity manager, expect your things to be lined up neatly in memory **and **ready for magically-works multithreading. This cause a large scale change because everything must be reworked to pass through this API to utilize it and stay in line of performance. C# Jobs System lastly let you code multithreaded code without worries, because you stay under a constraint called High Performance C# (HPC#) that Unity coined which eliminates nasty cases. There are some consequences like it must be started from main thread (so jobs cannot spawn jobs) among other things but Unity decided this balance between usability and power. Theoretically there are faster paths, but you will eventually arrive at pure multithreaded programming full of headaches if you do so. Entities utilized C# Jobs System to the max by scheduling them beautifully. Imagine how hard it is to maintain a perfectly lined up cache-friendly database, that ensure this condition everytime something changed, and it could be changed from multiple threads or not, and if it is just read then you should not be conservative and let the reader go nuts. Entities package has APIs that let you perform this very difficult interlocking design automatically. (Specifically, `JobComponentSystem`

, but let's not go deep.) Then Burst optimized both Entities code, and your game's code. Three things working together.

Ultimately you can call those 3 things as just an ultimate database. But do not underestimate it because all the things use data. Therefore all the things can get faster by basing themselve on DOTS. Networked games can now sync DOTS compatible data. Animation and Physics now faster because data are all on DOTS. Unity can go as far as removing the engine to pieces because now everything just plugs itself to this Entities core. (Project Tiny) Every darn thing can now be faster. This is how important Burst-Entities-Jobs is and it must be absolutely free of bugs.

More business oriented people are not excited by this kind of thing as me. They want to finish stuff, thing that already worked must not be touched. I like evolving tech and I kind of bored with OOP already. I am excited to be able to go to where it wasn't impossible. I am excited to create a game that utilized thing as low level as cache.

Something experimental and engine-breaking is uncommon on Unreal side. But Unity has no fear of doing so. I have talked with someone switched to UE from Unity, he said it is stupid to always make the customer a lab rat for all the features.

You can agree or not. An obvious improvement is in front of you, but backward compatibility is holding you back. Unity chooses to go forward. And I think this kind of decision ultimately separate the engine choice of devs. I don’t mind being a lab rat personally. I won not once but twice in a beta test giveaway program where you are given Unity swags based on randomizing through unique bugs submitted. I tried so many shiny features and submit a lot of bug reports. But he finishes a game as soon as he switched to UE and now hates Unity from the heart, because he was frustrated with built-in animation solution in Unity.

Do you often select the hardest difficulty in a game, or remove armors just for self-imposed challenge without any kind of archievement or trophies to back up the reason? I think Unity feels that way. And it satisfies a certain kind of dev.

## Data-oriented design vs Object-oriented design

As you may know now Unity is building a new Data Oriented Tech Stack (DOTS) foundation, while UE is staying strong in OOP. (Read [my deduction](https://forum.unity.com/threads/anyone-know-how-ues-generated-class-from-blueprint-allocate-and-use-data.688189/) that UE has OOP-style allocation)

In short, the strength of DOD is that "The hardware will thank you" because you are playing to the hardware's strength by knowing exactly where the data is and how it flows, while OOP you are playing to your own brain's strength because it is easier to visualize and program, and abstract away those details.

### OOP's strength we all love : it's easy to understand

This is highlighted by Epic's CEO which [he commented](https://www.reddit.com/r/unrealengine/comments/aezhdv/it_seems_people_at_epic_are_considering_adding/edxslvy/) DOD has potential but how hard it is to map game design problems to?

Unity is exploring an interesting direction with their ECS (Entity-Component System), which aims to escape the overhead of C# by moving data away from high-level objects linked by pointers to much tighter data layout, as is commonly seen in graphics programming and particle systems, and is less explored in gameplay programming. What's unknown is the productivity cost of recasting gameplay programming problems within the more constrained data model, and whether it would scale to e.g. a triple-A multiplayer game developed by a large team.

It's true. This area is unexplored and how could we map (recast) common gameplay problem to ECS's strength? It's not like we always make a game full of identical cubes or particles. ECS is good at iteration through linear memory and take advantage of cache line, but how can we design a game to fit this? Unity is working on higher level component that automatically use ECS so "recasting" is not your job. But not now. (I wish UE fanboys could think neutrally while presenting your own advantages like this CEO...)

Also, OOP doesn't instantly equal slow the same way C++ doesn't instantly equal fast. Overusing OOP's hierarchical design leads to poor performance because you are not aware of it's data structure. Read more here : [OOP is dead, long live OOP.](https://www.gamedev.net/blogs/entry/2265481-oop-is-dead-long-live-oop/)

### DOD's exciting untapped potential

I will simply quote from [http://dataorienteddesign.com](http://dataorienteddesign.com), an online free DOD book also available on paperback :

As we now live in a world where multi-core machines include the ones in our pockets, learning how to develop software in a less serial manner is important. Moving away from objects messaging and getting responses immediately is part of the benefits available to the data-oriented programmer. Programming, with a firm reliance on awareness of the data flow, sets you up to take the next step to GPGPU and other compute approaches. This leads to handling the workloads that bring game titles to life. The need for data-oriented design will only grow. It will grow because abstractions and serial thinking will be the bottleneck of your competitors, and those that embrace the data-oriented approach will thrive.

It is simply exciting that you could be ahead of competitors where they couldn't follow you! (If they stayed with OOP) Also that currently DOD is far from norm of the industry, it is also thrilling that you could be one of the earliest adopter, should DOD rise to mainstream fame in the future.

Also there are problem domain that are naturally suited to DOD as well, not just "everything could be thought in OOP". You are expanding your thinking toolbox by knowing DOD, just like reading an algorithm book make you able to map various problems to classic problems solved with graphs, dynamic programming, or clever data structures.

### Data transparency

Unity is not afraid to show the innards and I like it. For example, in Game Object Conversion Workflow which lets you author in Game Object but became Entity in runtime, there is a debugger that says what data you get exactly. This reflects in many other area in DOTS. While not exactly data, you can even view [down to assembly code](https://gametorrahod.com/analyzing-burst-generated-assemblies/) in the Burst inspector.

With conversion, it maybe theoretically possible to not know that you are using a different insides at all. I can imagine some engine if they managed to rewrite the core of engine this large scale, may want to abstract all that out and just say "the engine is faster now, revolutionary!" and that may made them look better than presenting something uninviting and geeky like a bunch of `IComponentData`

. (As evident in many comments around the net that DOTS is overpowered mess, hard to understand, and scary.) But I appreaciated this approach more then a black box one.

### Keep on learning

Putting performance or usability asides. Do you love learning? I really do, but not everyone.

Frankly I have come a long way with OOP and it is getting stale and boring. Reading website like [http://dataorienteddesign.com](http://dataorienteddesign.com) is just like making a new character in MMORPGs as a different class from your old character, it level up crazy fast and fun. Unity may bring pain along the way, DOD maybe super unwieldly to use now, but if tagging along will get me a nice ride on learning track then I'm on it. I know by myself I would get lazy, so it's nice that the engine is forcing me to learn. In this viewpoint I want to stick with Unity because it challenges and keeps me on the edge.

## Everything are queued to be reworked for DOTS!!

You read that I have been reworking my game countless times in order to catch up with Unity. Ironically Unity need to rework itself to catch up with its new Data Oriented Tech Stack self, in order to utilize the unlocked performance. Of course our game and editor toolings are queued for a rework next once those came out. What a time to be making games.

Now to the frustrating part. The recent years you could feel it that many upcoming features are delayed or appears stagnant. It's almost as if everyone in the compary was summoned to a secret meeting at one point and told : "You all stop what you are working right now, listen to this... *presents how data-oriented design would save the world* OK, do you want what you are working on to be obsolete in 2022? Then rework what you are doing for DOTS no matter how far away the schedule have to be posponed. Also no one should disclose this to any user since it would be an uproar. It will pays off later guys. We are doing this gently and gradually but if possible we just wanna pull the rug lol.. just kidding. (Or maybe not...)".

Frustrating part #2, it means whatever problems you encountered in the current system (that 95% of users depends their life on), they might not be as incentivized to fix anymore that they have a new and shiny DOTS-based-something cooking internally.

For example, multiple bugs related to IMGUI that I reported was marked as Won't Fix, because UIElements rework of the entire interface in 2019.3 would fix it. Ok, understandable, except that the current TECH stable is 2019.1 and it's frustrating you have to live together with the bugs for potentially 1 more year. It's like you got a toad in the room somewhere and you have to be constantly aware of it.

You feel like the Animation tab's UX [was stuck in prehistoric era](https://forum.unity.com/threads/my-biggest-pain-points.553498), because of course, they have the new DOTS-animation system in the work that fix everything since [it is a complete rework](https://forum.unity.com/threads/roadmap-for-better-animation-tools.673996/#post-4543342). They even state that it wouldn't be compatible with whatever exists now!

[The new input system](https://forum.unity.com/forums/new-input-system.103/) project started many many years ago, you could imagine it got some pivot over the year that by now it is not done yet. Maybe they are trying to make it DOTS-compatible but this one no official statement yet. The current alpha (2019) as per source code it use low level native memory access via pointer for interop speed with OS-detected input, but with DOTS they could have that threaded and bursted. I have been waiting in [this page](https://github.com/Unity-Technologies/InputSystem/blob/stable/README.md) for soooo long for the version number to be 0.3, so I could try the new touch input.

Unity SourceTree UI reference seems to be [stuck at the end of 2018 for half a year](https://bitbucket.org/Unity-Technologies/ui), around the same time they start promoting DOTS that may make it obsolete. (EDIT: It lives again on June!!) They have stated that the new [runtime-UIElements](https://blogs.unity3d.com/2019/04/23/whats-new-with-uielements-in-2019-1/) would, yeah, again, not be compatible with uGUI.

And of course UNET sunsetting that I said before. The reason a new solution didn't appear promptly is likely because it have to be [depending on DOTS](https://support.unity3d.com/hc/en-us/articles/360001252086-UNet-Deprecation-FAQ). Networking seems like a thing that could benefit from DOTS greatly, if I know DOTS is coming I would also stop my networking team from making mono-based solution for the better future of the company.

DOTS itself get its own rework from time to time, like that big API apocalypse that deprecates `[Inject]`

junks, or a system version number needed to be passed to the job, or the magic entity command buffer `CreateEntity`

which talks to the next one spiritually but now fixed to return `Entity`

properly, or all your existing jobs now has to explicitly register itself to its barrier/ECBS to dequeue commands. All requiring manual fixes.

Something like this I genuinely think is good for Unity. However prepare for shitstorm and countless "ETA??" threads in the forum because people are mad when their stuff break, madder when given a **experimental preview** but they use it for real and break their game beyond repair, and maddest when they don't know when they could use it. I salute Unity for making changes this big and dealing with bad users.

### But it's fucking exciting

I think just use whatever engine you are the most happy with. One Unreal fanatics I know said it the engine that helps ship the game fast and most popular games trusted Epic and its gigantic financial success, so my game should equally survive well. He doesn't need to press the update button ever and complete the game, he enjoy the stability and many instant and specific toolings Unreal is good at.

For me, Unity maybe wonky sometimes, but it's fun working on things with it and it's unexpectedly hardcore (especially the recent ECS), so I like it. I find it adrenaline pumping that Unity is going hardcore to make you think down to memory layout level. Ableton Live the music making software made me feel the same, I feel I want to mess with it more than other brands. Use what excites you.

## Terrains

I have not made any game that uses the terrain system so I cannot say anything. However there are some that says there's a deal breaker in Unity's built-in terrain system where Unreal could do anything, so I think I should include a bit of this. For example [this](https://forum.unity.com/threads/the-issue-with-the-new-terrain-tools.702290). Use your own judgement. If you have bad experience with Unity terrain before, note that Unity updated the terrain tool recently.

As far as I looked to UE roughly, UE has [an explicit support for making a streaming open world](https://docs.unrealengine.com/en-US/Engine/OpenWorldTools/index.html) thanks to owning the game Fortnite. I think this connects tightly with practicality of UE's terrain feature, since terrain is a big mesh and streaming that means the mesh has load only partially, or something? (I actually has no idea)

Unity 2019.2 came with a rewrite of Terrain system, but I have no information until I have got to use it. (Probably never)

## Please read the comments below

This article is still in-progress, as stated at the beginning. Likely will be for years. Here, I will summarize what it feels like in a given year.

**2018 :**DOTS announced and at full speed. Deprecations looming. 2018.3 is an important breakpoint to use the new prefabs and package-based development.**2019 :**DOTS transformation still in progress but still zero usable high-level DOTS stuff. Premitive DOTS that is ECS still in-dev. Some DOTS backend creeped in silently like audio in 2019.1. 2019.3 is an important breakpoint that the editor changed completely. Massive packagization of Unity, Timeline, uGUI becoming a package.

In the mean time many from both Unity and UE had come to fill in some voids where I couldn't make my judgement because I am not that far into UE yet, in the comments below. Like, I didn't think UE would be that difficult to program a custom shader without hacking engine code. Also it is nice to see almost every one stating opinion objectively, from personal experience, complete with "why".