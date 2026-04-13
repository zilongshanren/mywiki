---
title: Dinner-driven Development (DDD)
url: https://gametorrahod.com/dinner-driven-development/
author: Sirawat Pitaksarit
published: '2019-06-27'
source_blog: Game Torrahod
source_site: https://gametorrahod.com/
category: game programming
fetched: '2026-04-13'
---

I have been developing a new **game** **software** development practice, and it's about time to publish this research : **Dinner-driven Development (DDD)**. May I remind you that this is a completely serious article, as you may have thought otherwise from the title.

## Game-specific testing problems

You may have unit tests for important logic in the game, such as score calculations which leads to it living permanently on the scoreboard. It would ruin competitive integrity if you can't ever get that max score due to rounding errors.

Then you should have some integration tests to increase confidence in your game how everything assembled together. You let that roll on your device farm before every release. Everything green. Good! All tests are awesome.

However let's face it. Problems like these are **not **going to be caught or goes red by either kind of tests :

- A fade-to-transparent transition animation is somehow still barely visible. Damn, that value slider. I should have type the number in. Even worse, that ghost UI remains for the rest of gameplay scene!
- The first frame on entering a new scene which should be pitch black and transition to visible, has a flash of visible scene for 1 frame before it goes black. Hmm, maybe some of my methods I thought it's async ended up blocking the black out code?
- The click sound of one particular button in the game didn't play. Ah, that one wasn't the same instance as the others. Forgot to replace it when we did
*that*rework. - Missing text characters. Ah, we forgot to bake a new set of signed distance field texture when we add that new tutorial text. (after baking them) Huh, why this completely unrelated dialog now looks garbled? Ah, the new baked characters ended up pushing the texture over 2048x2048 and somehow the new sheet isn't loading.
- Wait, I remembered making a new UI animation here and now where is it? Oh, the new outer parent animation cancels that out.
- The timing isn't quite right. This one too short, that one too long.
- The was-fine-before something that is an instanced object is now wrong, because you went in the ancestor and the edit you made propagates out in an unexpected way. For example the cursor that you used everywhere in the game, you went in and make the cursor flash with shiny blink every time you click, except that you used scaling and on one scene you made a mistake of scaling the parent of cursor and it ended up magnifying the scale even more.
- Why is that screen flash black instead of white? Damn, the colorizer logic for letterbox effect that runs before make it black and we reuse that texture.
- I remembered corner anchoring the UI, but why it's not sticking to the edge? Oh, I see, I was testing on iPhone res all along and and now we are on iPad res. Turns out this one is center-anchored.
- When switching to iPad, that UI moved down and slightly obscure the other UI at only some specific animation moment not previewable at edit time. You couldn't foresee this even though you really made sure your UI are responsive. And by obscuring, sometimes its just the edge is touching each other where your intended design was to have a bit of padding. Your OCD couldn't let this slip and you want to get that right.

Games are full of intricacies. It's a blend of art and technology. The test should not attempt to catch these errors by the way, it may hamper your artistic decision. But error is an error. You want to get your baby looking the best from your viewpoint. That [last 10%](https://en.wikipedia.org/wiki/Ninety-ninety_rule) you want to polish it to death.

### QA? Beta tests?

Something like garbled text, margins between list item not equal, or a button doesn't make sound like they are **supposed to, **could be caught by the QA rounds or beta tests. However that's because they have **the context.** The context of what it should be.

Some problems like margins **too small **or some sound effects that's too loud must be caught by you, the creator of it, who has the context of what it should be like. And therefore it is troublesome that no kind of automation tests could efficiently catch these other than you manually take a look at the whole game carefully. (And of course, again over and over, because regression happens.)

The solution is we will adopt the concept of [production line](https://en.wikipedia.org/wiki/Production_line) in factories. Some manual inspections are required but contraptions such as conveyor belts help minimize what human should not be doing. What did we do to the game when we wish to catch those kind of errors? 2 things.

## Navigational Tests

The first one is **navigating**. You try to navigate around all scenes and clickable things in your game and observe carefully. You may have to do it again if you was busy looking at one corner of the screen too much.

Because the integration test's assertion logic is unlikely to catch these delicate and even subjective errors, **the most optimal **test (fast to write, easy to understand, self-documenting, maintainable) for this is what I call **Navigational Tests. **They are tests that just navigates. No assertion, or very few like "which scene am I now?", or some timeout/sanity check. This kind of clicking around task should be for the machine to do it, not you. This is the conveyor belt.

This kind of test almost always turns green, but you should consider it red by your judgement from your eyes. For this purpose, it maybe helpful to mark the test as unconclusive, ignored, or skipped (some testing framework will then neither place green check or red cross on these) so you know these tests are never 100% correct. Only you could judge them, and yourself in the far future may judge them differently. If you would like them green just to mark that you have already run it then that's fine too.

## Look ma, no hands!

The 2nd one, we **look**. One thing I realized for navigational tests is that, those bugs are caught by human observation and not by code. By observation I mean, looking. As I believe everyone use the screen as an output device of choice and it is flat, so it is very convenient that we don't have to walk around the computer. If we were potters, we would have to use the hand somehow to judge the finished work with some help from rotatable dish base.

After writing navigational tests you eliminated the manual clicking around task, what's left is just that you must look and spot errors. This is already a big improvement!

However that's just the beginning of DDD. What more could be improved in this 2nd aspect of this kind of tests? To recap, even with navigational tests, it must be **you** looking to catch all possible bugs that QAs will never spot. How could you make this process faster?

Of course you should write a good test, so that it is not over-waiting and waste time. But I am going one step further. One alternative of increasing speed is increasing available time, since speed aims to cost you less of your available time. **What if we could magically get more time to test, for free?**

## Dinner

![](../../assets/84ca787d44ba11f1.png)

All comes together to the dinner. You may think this article is a joke but I'm (very) serious here. You have this extra time with you all along but you may not be realizing it.

But turns out, dinner is perfect for watching navigational tests!

### Preconditions

First I would like to make some assumptions, these are some conditions that helps you become a successful DDD practitioner :

- Work on your game solo and refuse to get a day job and get a normal life until your game is done.
- 50% of dinners are just you at the street food stall.
- The other 45% are still just you at your own room, with boxed version of the same thing from street food stall. (The remaining 5% are your office friend inviting you for a dinner, which you should treasure that moment for life)
- You tear up with envy at the sight of office workers finishing their day and joyfully group up for a buffet. You barely remember that feeling from university days long ago. You have absolutely no one to talk to other than the barista which you got to say to her only "Americano please".
- You can't get girlfriend/boyfriend because you are locked alone in a coffee shop with no interesting random fated events for the past year. All your past confession you mustered up failed. It's unlikely that you will bump into a new girl with a bread on the way to coffee shop either. You are very tired of your parent begging when will you get a life "like others". They ask you as if you should just propose to a random person walked past the coffee shop, or grow a girlfriend as if she's a plant.
- You have absolutely no one to call to at dinner. Also, no one ever called you on the phone except credit loans offering from the bank, who just searched registered company database and thought you are multi-million entrepreneur. In reality you want to start a Patreon to cover Americano and Houjicha costs.
- You have no fear of bringing out the laptop outside of workplace. Honestly it's really awkward, even for a person like me. (Yeah I am self aware) The screen is big and bright, and you have a keyboard that produce out-of-place sound in a place like cafeteria. But it will get better overtime like nowadays using smartphones on dinner is no longer awkward. Also you have no one around to care anyways.
- So eventually you will get some attention for bringing out the laptop. When you point out that everyone are also glued to the phone nowadays too, the response you get is that it is just not the same with laptops. You then reminiscence that 10 years ago when your mom don't know what is a social network and smartphones, you got scolded for playing PSP on dinner and when you tell her what about the TV she replied it is just not the same with handhelds.
- Also when you are invited to dinner by office friend, you spent time looking at their face while waiting for food because it was so long we haven't seen each other. But all of them are social networking like normal because for them they always eating together and it is nothing special. Now
*you*are the weird one for not fumbling with the phone. And the friend make a face that says "it's creepy, why are you staring at me?". - You dried up all your social media notifications before dinner because your game engine is so slow you could eliminate noti badge on one social network and back, and it even not starting the play mode yet. (e.g. Unity)
- Sometimes you feel like you had enough of all street food and all convenient store freeze product, like you just ate all of them together yesterday. So you tried cooking at the room from time to time. The food you cook is then consist of a period of waiting, but not long enough that you could left it alone. Also you now have to deal with washing dishes.

### Execution

Ok, so my point is that you have absolutely nothing better to do at dinner. No one to talk. No face to save. No social to check. No one you know around that you have to care. Twitch stream not happening. **It's time to whip out that laptop and let the navigational tests run.** And not the other kind of tests where greens give you full confidence. That's for your CI to run while you are sleeping.

And I would like to tell you I have been attempting to use this dinner time for anything else related to productivity but it just not working well enough that I would rather just enjoy the food. The best one was reading `CHANGELOG.md`

of updated packages I am using instead of mindlessly scrolling Facebook, I still lose one hand to scroll the page that could be used to enjoy my food, however.

Now you realize how everything comes together so perfectly :

- You need 2 hands for most food to enjoy it fully. If you try to one-hand the food, the other hand is likely a smartphone on Facebook. It's a bad habit. And now you start using only a spoon to cut things unoptimally without a fork, wasting even more life in addition to Facebook.
- While you enjoy your food with both hands to the fullest, your eyes could also look for that defects.
**You are not losing anything at all**, since these kind of tests just navigates and only require an observation from you. Food delicious. Nutrition improve brain axioms and you found more bugs. Eyes work on the game. Ship faster. Reach your dream. Retire game dev and get a real life sooner. - If you are going to take the next bite of your food and is now FOMO of what's happening on the screen, don't be! There are millions more dinners waiting for you. And remember these tests
**never pass.**You just keep doing it passively and find something new each round. - A new repeated round ideally, should be run with different configuration like iPhone/iPad aspect ratio switch.
- If you already have a life and got someone to eat with, you would feel reluctant to bring out the laptop because that would make you a weird geek and you will feel socially awkward. Also you should live in the moment and talk to him/her instead of running automation test. This won't work. That's why the preconditions I listed are important.
- If you are eating boxed food at home, you can even watch the navigational tests while you are washing dishes! Don't let that sink tub pile up. Wash dish concurrently to game development.
- If you cook, previously without navigational tests you are incentivized to cook lengthy-but-"running on its own" food like stew, soup, or steamed food because you want to go programming while leaving it cooks. Not anymore, now more dishes that requires more frequent intervention like deep frying are open for you! You could watch the test running while stirring or flipping them on the pan. Just don't try to DDD while using a knife, obviously.

When I realize this is probably an optimal thing to do for me at dinner, given the condition of my life, I wondered how many dinners I missed out doing nothing. I may have shipped the game by now if I realized this sooner.

And sure enough the defects was found instead at my night time devs, where I should be playing Overwatch with my get-laid-already friends before they have to sleep for their office job tomorrow.

### Weaknesses

This also highlights a big weakness of DDD, it make you socially awkward if someone found out you are doing it. I did by publishing this research, but since all of you cannot possibly know who I am or where to find me, I am still a completely normal person if someday we cross path with each other.

You are giving them more reasons. You will be accused that because you are *like this, *you never get laid and no one will like you as you are. While in reality, you are really trying your best to reach your dream faster in order to quit and get a life as socially requested (yep, deep down you secretly think you are perfectly happy as you are and could die keep creating things, if not for social effect that make you think you must get a life), but no one understands and keep bully you especially your relatives. Your friends occassionally cheer you for being brave and hope for your success, but at the same time you don't want to talk to them for too long because you feel really left behind given their continuously growing job position. What if nothing happen after releasing the game?

You then think making any human contact presents a risk of them saying something you couldn't un-hear. You started befriending, waving, and talking to your alley cats and dogs more than your parent because there is no risk that they will say something that ruin your day. You start thinking if this is the same bird as yesterday and if it really cares about your game's success more than your mom who only think that you have 0 salary and therefore you are "behind" everyone, so you always brought bread crumbs with you back from the cafe for it. That's why those preconditions will help a lot. Otherwise I think you have a better thing to do at dinner.

### Team up and double the fun

You don't have to be alone. If you happen to have a team that is ready to be awkward together, how about a dinner or pizza together in a projector room while everyone looking at the running tests? I heard those who practice agile have that stand-up meetings and scrums, why couldn't we have some kind of our own ritual too? Trust me you will be catching million bugs in one dinner while you have fun yelling at each other whose fault is it.

### How to make the best of DDD

The best thing of DDD is that you are now able to **develop games while having a dinner **every day! After you learned to stop caring how the social views you because of it, now it depends on your DDD mastery what will you get for each round of dinner.

- The goal is that you must have some navigational tests runnable
**before**each day's dinner. Plan that out through the day. By plannig, I mean some tests could fail because it's related to what you were working on today. If you know what are those tests, then skip them for this dinner. - If the coffee shop is closing, get those tests highlighted while your brain still have context of your work. At food place you then don't have to think about where you left off. Just run.
- At daytime before dinner,
**try not to find the problem**. There are some game dev routines that you are just "mindlessly checking around, polishing things" because you want to postpone that next chunk of work which looks tiring. It's time to stop that habit! I get this everytime I need to begin making a new scene, and it's already evening. - You should fix on the noted problem from yesterday's dinner at daytime, in addition to working on new features. Day time is not the time for looking for new stresses but rather eliminates them. Then you could get creative on new contents.
- All new features should be furnished with a quick and dirty navigational tests as you finish them, before you get lazy. For example, every dialog boxes should have a test that is able to open them and close them.

That last point is important. Therefore because my game engine of choice is Unity, I have go great length and developed a new UPM package called **Minefield **which works great with everything presented here. (told ya I'm serious)

It is optimized to write navigational test. I don't care about mocks, stubs, CI integration, report generation. The speed of coding a quick and dirty navigational test is the key. It just clicks and waits, but I really made sure it is top-notch at clicking and waiting!

I caught some difficult bugs like something being clickable briefly at certain unintended frame because of it, which could be reproduced by real user if they are unlucky enough, and it is game breaking since it would make the next transition runs in parallel with the current one causing havok. I am sure you may have face this kind of bugs before when asked someone to do [monkey testing](https://en.wikipedia.org/wiki/Monkey_testing) on the game.

It even has some assertion helpers so you could really focus on only observing. For example if something is clickable or not when you expect them.