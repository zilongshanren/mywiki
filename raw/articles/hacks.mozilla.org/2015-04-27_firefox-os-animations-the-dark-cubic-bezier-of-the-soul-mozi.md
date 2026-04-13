---
title: Firefox OS, Animations & the Dark Cubic-Bezier of the Soul – Mozilla Hacks
  - the Web developer blog
url: https://hacks.mozilla.org/2015/04/firefox-os-animations-the-dark-cubic-bezier-of-the-soul/
published: '2015-04-27'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

I’ve been using Firefox OS daily for a couple of years now (wow, time flies!). While performance has steadily improved with efforts like [Project Silk](https://hacks.mozilla.org/2015/01/project-silk/), I’ve often noticed delays in the user interface. I assumed the delays were because the hardware was well below the “flagship” hardware I’ve become accustomed to with Android and iOS devices.

Last year, I built Firefox OS for a Nexus 4 and started using that as my daily phone. Quickly I realized that even with better hardware, I sometimes had to wait on Firefox OS for basic interactions, even when the task wasn’t computationally intensive. I moved on to a Nexus 5 and then a Sony Z3 Compact, both with better specs than the Nexus 4, and experienced the same thing.

Time passed. Frustration grew. *Whispers of a nameless fear…*

### Running the numbers

While reading [Ralph Thomas’s](https://twitter.com/i_am_ralpht) post about [creating animations based on physical models](http://iamralpht.github.io/physics/), I wondered about the implementation of animations in Firefox OS, and how that might be involved in this problem. I performed an audit of the number of instances of different animations, grouped by their duration. I removed progress indicators and things like the boot shutdown animation. Here are the animation and transition durations in Firefox OS, grouped by duration, for transitional interactions like scaling, opening, closing and sliding:

- 0.1s: 15
- 0.2s: 57
- 0.3s: 79
- 0.4s: 40
- 0.5s: 78
- 0.6s: 8

A couple of things stand out. First, we have a pretty wide distribution of animation durations. Second, the vast majority of the animations are more than 300ms long!

In fact, in more than 80 animations we are making the user wait *more than half a second*. These slow animations are [dragging us down](https://www.youtube.com/watch?v=dK_OKGELcn0&t=140), resulting in a poorer overall experience of Firefox OS.

### How did we get here?

The Firefox OS UX and interaction designers didn’t huddle in a room and design each interaction to be intentionally slow. The engineers who implemented these animations didn’t ever think to themselves *“this feels really responsive… let’s make it slower!”*

My theory is that interactions like these don’t feel slow while you’re designing and implementing them, because you’re working with a single interaction at a time. When designing and developing an animation, I look for fluidity of motion, the aesthetics of that single action and how the visual impact enhances the task at hand, and then I iterate on duration and effects until it feels right.

We do have [guidelines for responsiveness and user-perceived performance in Firefox OS](https://mozilla.app.box.com/s/aww17rx74k7fjds5vada), written up by [Gordon Brander](https://twitter.com/gordonbrander), which you can see in the screenshot below. (Click the image for a larger, more readable version.) However, those guidelines don’t cover the sub-second period between the initial perception of cause and effect and the next actionable state of the user interface.

Users have an entirely different experience than we do as developers and designers. Users make their way through our animations while hurriedly sending a text message, trying to capture that perfect moment on camera, entering their username and password, or arduously uploading a bunch of images one at a time. People are trying to get from point A to point B. They want to complete a task… well, actually not just one: Smartphone users are trying to complete * 221 tasks every day*, according to a study in the UK last October by Tecmark. All those animations add up! I assert that the aggregate of those 203 animations in

[Gaia](https://developer.mozilla.org/en-US/Firefox_OS/Developing_Gaia)that are 300ms and longer contributes to the frustrating feeling of slowness I was experiencing before digging into this.

### Making it feel fast

So I tested this theory, by changing all animation durations in Gaia to 200ms, as a starting point. The result? **Firefox OS feels far more responsive.** Moving through tasks and navigating around the OS felt quick but not abrupt. The camera snaps to readiness. Texting feels so much more fluid and snappy. Apps pop up, instead of slowly hauling their creaky bones out of bed. The Rocketbar gets closer to living up to its name ([though I still think the keyboard should animate up while the bar becomes active](https://bugzilla.mozilla.org/show_bug.cgi?id=1050411)).

Here’s a demo of some of our animations side by side, before and after this patch:

There are a couple of things we can do about this in Gaia:

[I filed a bug to get this change landed in Gaia](https://bugzilla.mozilla.org/show_bug.cgi?id=1143226). The 200ms duration is a first stab at this until we can do further testing. Better to err on the snappy side instead of the sluggish side. We’ve got the thumbs-up from most of the 16 developers who had to review the changes, and are now working with the UX team to sign off before it can land.[Kevin Grandon](https://twitter.com/kevining)helped by[adding a CSS variable that we can use across all of Gaia](https://bugzilla.mozilla.org/show_bug.cgi?id=1152591), which will make it easier to implement these types of changes OS-wide in the future as we learn more.- I’m working with the Firefox OS UX team to define global and consistent best-practices for animations. These guidelines will not be correct 100% of the time, but can be a starting point when implementing new animations, ensuring that the defaults are based on research and experience.

[report bugs](https://bugzilla.mozilla.org/enter_bug.cgi?product=Firefox%20OS)if you experience anything that feels slow. By reporting a bug, you can make change happen and help improve the user experience for everyone on Firefox OS.

## 12 comments

jorreteApril 27th, 2015 at 08:00AndréApril 27th, 2015 at 22:22Dietrich AyalaApril 27th, 2015 at 22:23AndréApril 29th, 2015 at 09:36dietrich@mozilla.comApril 29th, 2015 at 11:36macApril 28th, 2015 at 00:54dietrich@mozilla.comApril 28th, 2015 at 12:37alex_mayorgaApril 29th, 2015 at 06:14dietrich@mozilla.comApril 29th, 2015 at 08:09AndréApril 29th, 2015 at 09:25Aleksandar BlagotićApril 29th, 2015 at 13:53dietrich@mozilla.comApril 29th, 2015 at 13:54