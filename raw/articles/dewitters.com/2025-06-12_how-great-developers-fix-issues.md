---
title: How great developers fix issues
url: https://dewitters.com/how-great-developers-fix-issues/
published: '2025-06-12'
source_blog: deWiTTERS
source_site: https://dewitters.com
category: game programming
fetched: '2026-04-13'
---

You’re staring at a bug.

Something is broken. It’s not working, and you have no clue why. So you do what any sane person would do:

You poke it.

You change a line. Doesn’t work. You remove some line. Still broken. You randomly reorder 2 things, and suddenly, it works!?

It works! Don’t touch it! `commit`

and claim victory!

But that’s not victory, that’s a fluke.

You have no clue why it works, and you certainly have no idea what was the problem was in the first place.

This is the bad way of solving a problem.

And back in the day, throwing random fixes at code took effort. Now? You can do it faster than ever with ChatGPT. It’s like playing slot machines with your code.

Don’t get me wrong, ChatGPT is powerful. But if you use it to bypass thinking, you’re just turbo-charging your ignorance.

Use it *to learn*, not to skip the learning.

## Why trial and error is bad

There are plenty of issues with this way of solving a development problem:

- You cannot be sure you solved every aspect of the problem
- Your code is very fragile, because a change could reintroduce that issue again
- And worst of all,
**you didn’t learn anything!**

## Trial and error isn’t always wrong

Let’s be fair, trial and error *can* help.

But it only works when it’s used as a *tool for understanding*, not as a replacement for thinking.

If you’re poking something to see what changes, that’s observation, that’s *science!*

If you are poking just to silence the error message and ship the feature, that’s duct tape on a cracked reactor core.

## The good way: understand first

When you hit a bug, stop! Don’t fix it yet. First, **understand the problem.**

#### How to understand?

The issue is hiding in your code, and you are the detective that will uncover it. Here are the tactics that you can use:

- Isolate the bug, so you can pinpoint where it goes wrong. Remove a few lines and see what happens
- Add logs, to know what’s going on
- Properly read the error message, don’t skim over it
- Use the debugger, and see where it behaves differently than what you expect
- The scientific method: make an assumption (you probably already made plenty of assumptions in the first place), test your assumption, see if the computer confirms it or not

When the chase above didn’t help you corner the issue, there’s always other people:

- Google it
- ChatGPT it
- Go ask on reddit or some forum
- Go ask your colleague

The goal isn’t to find a fix, it’s to *understand what’s actually going wrong.*

Once you understand the core of the issue, the fix is usually obvious.

#### Bonus tip on the worst problems

When you come across a problem that you just can’t pinpoint. It’s so complex that you start questioning the basic laws of physics. You tried everything already, but the bug still escaped. According to my experience (and I have plenty), it’s the most stupid thing you can imagine. Like a copy-paste and you forgot to change an `x`

into a `y`

, or something like that.

## The payoff

So what are the benefits of first understanding the core of the problem before you make the fix?

- You fix the
*real*problem - You learn how the system works
- You prevent future bugs
- And best of all: Next time you see a similar issue, you’ll recognize it instantly! Extra bonus points when you fix someone else’s problem.
- Congrats, you just leveled up as a software engineer!

Maybe you were sad because ChatGPT couldn’t find and fix your issue? Don’t be! Because you just proved that your squishy, moist brain can still outperform an AI that burns through 3.8×10²⁵ FLOPs and several megawatts of power.

## Summary for the Lazy

**Step 1**: Understand the problem**Step 2**: Fix the problem**Rule 1**: Don’t skip step 1!**Rule 2**: Use ChatGPT to help you understand the problem, not to bypass your thinking!

That’s how great coders are made!

Write code like you mean it! Not like you’re hoping to get lucky.


## 0 Comments