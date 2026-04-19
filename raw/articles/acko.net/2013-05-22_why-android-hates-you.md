---
title: Why Android Hates You
url: https://acko.net/blog/why-android-hates-you/
author: Steven Wittens
published: '2013-05-22'
source_blog: Hackery, Math & Design — Acko.net
source_site: https://acko.net/
category: graphics
fetched: '2026-04-19'
---

![Why Android Hates You](../../assets/397b7f9eddb3c414.jpg)

# Why Android Hates You

## Usability, Affordance and Grannies in Vegas

For quite a while, I've been an Android user. After upgrading to a Nexus 4 several months ago, I'm living the Ice Cream Sandwich and Jelly Bean dream, enjoying a beautifully designed user experience, [just like Matias intended](http://en.wikipedia.org/wiki/Matias_Duarte), right?

Nope.

Android has a problem and no, this is not about fragmentation. I'd like to talk about Android's contempt for its users instead. See, no matter how many pages of tastefully designed [User Interface Guidelines](http://developer.android.com/guide/practices/ui_guidelines/index.html) the team puts together, Google just can't seem to shake its deep seated belief: that users are the most inconvenient and unreliable part of the cloud, and that getting adequate mediocrity across the board is the best you can do, rather than taking a holistic approach and excelling.

Strong words, for sure. Ever tried to get support from Google? If you've studied [how objects are supposed to be designed](http://www.amazon.com/gp/product/0465067107/ref=as_li_qf_sp_asin_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=0465067107&linkCode=as2&tag=ackonet-20), owning an Android phone is an exercise in frustration. It's a daily reminder of bad decisions, performed with a stubborn flourish, by someone who maybe doesn't have the skill or desire, but more likely, just isn't given room to do better.

None of what follows are mortal sins, let's be clear on that. But they're missed opportunities in making Android actually pleasant, and they're a last-mile of frustration some of which Steve Jobs would've probably fired people over.

## Don't Get Comfortable

Since the dawn of time, my Android phones have claimed that app data and settings will be backed up to the cloud, courtesy of Google. By "data and settings" they mean "except the stuff you actually care about".

It comes as absolutely no surprise that none of them have ever restored the layout and arrangement of icons and widgets on the home screens from the cloud. The only thing that seems to happen is that a bunch of apps get downloaded one after the other, spazzing out your notification bar for up to an hour if the connection is slow, filling up your app drawer while you're trying to put things back. Actually showing a progress of the entire restoration, perhaps estimating when you can expect it to be back to the way it was, is a pipe dream. Backing up to the cloud is done manually through apps, like G+ photo upload, or other third party mechanisms.

After restoring your phone, you can also look forward to repeating all the patronizing tutorials and "Don't stick your fingers in the sockets" warnings of Google Now, Maps, Navigation, Goggles, etc. and certainly not removing "U.S." and "Sports" from your default news subscriptions, because that's what everybody likes.

The fact that nobody at Google seems to consider this a problem is quite telling. But then, so is the default layout you get out of the box, or in this case, after "restoring my settings". Only the wallpaper was saved:

![Backup settings](../../assets/042a934c9a8a6c9e.png)


![Downloading Twitter](../../assets/0672277f2ee5e786.png)


**Never lose my stuff**

“Save what people took time to create and let them access it from anywhere. Remember settings, personal touches, and creations across phones, tablets, and computers. It makes upgrading the easiest thing in the world.”

![Android of of the box](../../assets/1244e18c413d9f94.jpg)

All the Google things are lumped into one folder, which includes the amazing labels "Play Music" alongside "Play Movie…", "Play Maga…", "Play Books" and "Play Store". The hesistant newbie has to make the cognitive leap that "Play" is not a verb here—despite the tacky golden rapper headphones—rather than conclude that Google has weird taste in words, or that this is a phone for children.

The action verb they were looking for instead was "Buy Music" and "Buy Movies". It seems they replaced the media player with a shop you can keep your own tunes in. My advice: get rid of the advertisements posing as widgets and use [DoubleTwist](http://www.doubletwist.com) instead.

Actually presenting functionality is a job left for the App Drawer, paralyzing you with choice by Pokémon. There's two Mails, three Googles, three Messengers, a whole Play-set as well as assorted circles, pins and triangles. You'll find yourself dragging every app you'll use regularly somewhere more convenient. Open App Drawer. Pan. Draaag. Repeat.

![Google folder](../../assets/3e8996955b19735e.png)


![App Drawer](../../assets/1c0734a472f08fd9.png)


As an aside, out of the box, don't expect that people can just send you geo coordinates, video messages, meeting invites or office documents. Whenever it's really mattered that I read something on my phone right now, Android's given me more "I don't know what to do with this" errors than even my Windows 98 box back in the day. Clearly this is just a matter of hooking up the right pre-existing bits, and the newer releases are better. But still, it feels like a lot of real world use cases weren't tested, in particular without an internet connection.

Just recently, I couldn't turn off the Satellite layer in Maps because I didn't have data, even though I'd cached the whole city I was in. Bug or fluke? Who knows. And when Google Now showed me flight info for the wrong day, there didn't seem to be a way to correct it. The algorithm knows better than you do, human.

**Decide for me but let me have the final say**

“Take your best guess and act rather than asking first. Too many choices and decisions make people unhappy. Just in case you get it wrong, allow for 'undo'.”

## Don't Touch Me

As late as the Nexus One, most Android phones weren't really multi-touch. They had separate X/Y sensors, capable of distinguishing two touches from one, but unable to tell whether they were rotating clockwise or counter-clockwise. As a result, multi-touch has always been tacked on as an extra: despite now being capable of tracking 5 or even 10 touches, most surfaces still only respond to one.

This all comes down to the concept of affordance: what do our devices suggest we can do with them, and what do they actually allow us to do? For example, based on the design of the handle, doors generally *afford* either pulling or pushing, giving strong hints as to how to open them. Instead of arguing over whether things should look skeuomorphic, how about making them act skeuomorphic?

Take for example the notification drawer. One way people often interact with real drawers is to pull them out with one hand, and reach in with the other. You could try doing this with the notification drawer: pull down with one finger, touch or swipe a notification while holding the drawer half open. It doesn't work: you can only interact with one thing at a time. It's not a drawer, it's a hand-operated modal dialog in disguise. This is obviously just a detail, but notable none the less.

More importantly, some notifications can't be dismissed despite looking identical. While responding to swipe gestures, they slide back with pixel-perfect inertia, glued in place with invisible chewing gum. If you're out of cell range, or e.g. simply do not wish to incur roaming costs, the "New Voicemail" message will not go away until you call in, even if it was probably VoIP spam.

The drawer is multi-functional: dragging down with two fingers brings up a dashboard of tiles. Unfortunately, this is a hard gesture to get right 100% of the time. Hence, it appears a clever Android programmer made it so you can add the second finger in the middle of the gesture. Convenient, but they messed it up, suggesting it's an accident: you have to land exactly on the gripper, instead of anywhere in the vicinity. This gesture is even harder than placing both fingers correctly in the first place.

These tiles are another boondoggle: can you tell which ones you can long-press to toggle and which ones you can't? By the way, that long-press has its own non-standard delayed acknowledgement, ensuring you'll accidentally toggle things back and forth a couple of times before you get used to it. Just how much less functional is this than a real slider, some big switches and a few separate icons?

This Flat UI theme has brought with it tons of unlabeled icon buttons. In some places you can long-press on an icon to get a tooltip describing it. Here too the interaction is cumbersome, requiring a long-press for every individual button rather than being able to slide your finger from icon to icon. The natural gesture of discovering a surface by feeling it has been reduced to a mechnical process of tap-hold-repeat. Heck, why not make use of the giant screen, blow up the icons, show tooltips with arrows to everything around your finger, do *something* more sophisticated than what Microsoft Office did.

![Notification Shade](../../assets/aa5622ff10a353e3.png)


![Notification Shade](../../assets/9e0c33abce3b36d1.png)


![Tooltip](../../assets/7a9d30242bb677c5.png)


**If it looks the same, it should act the same**

“Help people discern functional differences by making them visually distinct rather than subtle. Avoid modes, which are places that look similar but act differently on the same input.”

**Give me tricks that work everywhere**

“People feel great when they figure things out for themselves. Make your app easier to learn by leveraging visual patterns and muscle memory from other Android apps. For example, the swipe gesture may be a good navigational shortcut.”

Then there's the new Gesture-typing keyboard. If your nails are a bit long, or your hands a bit sweaty, or you're wearing thin gloves, you may find it difficult to form basic words. As soon as your finger leaves the pad for a fraction of a second, your gesture is interrupted, spawning a bunch of syllables. Even if you continue swiping and the line continues cleanly. It seems the physics of how fast humans can move their fingers are ignored here in favor of blind sensor obedience. If a gripped finger strays into the pad from the side, it'll stop working altogether. Oh and don't try to type the word "jerking", it's not allowed. What do you think this is, a real keyboard?

Finally if you use Google Talk, you get to enjoy a strange bug where it randomly gets stuck in a loop and forcibly scrolls to the bottom every couple of seconds, at random intervals, resulting in the most frustrating user-computer tug of war I've encountered. Fun times.

![Gesture Typing](../../assets/f9a4199ad2e66641.png)


## It's For Your Own Good

Now, everyone knows headphones can damage your hearing. This is why the EU passed laws to help ensure consumers would be protected from themselves: devices like iPods are limited in the sound level they can emit. If you've ever sat next to someone and listened to the kacrunch-kacrunch that their hip-hop or dubstep sounded like to everyone on the outside, you may think this is a very good idea.

Unfortunately, it takes a politician to think you could legislate against people being stupid, and a lawyer to come up with the convoluted verbiage that makes it seem sane to the rest of us. Then you need a developer to do a really hare-brained job in implementing it. Hence, in line with EU legislation, Android 4.2 introduces a new feature, for all users everywhere:

![My spoon is too big](../../assets/9a59d2dc1a426cfb.png)


**Only interrupt me if it's important**

“Like a good personal assistant, shield people from unimportant minutiae. People want to stay focused, and unless it's critical and time-sensitive, an interruption can be taxing and frustrating.”

**Get to know me**

“Learn peoples' preferences over time. Rather than asking them to make the same choices over and over, place previous choices within easy reach.”

This pops up whenever the device *thinks* you're raising the volume above a safe level. I say 'thinks', because reports suggest the behavior differs based on what the phone is plugged into, with some users never seeing it, and others complaining about it endlessly. In any case, it's clearly broken for two reasons.

One, it is ridiculous to think a phone could know whether the volume is unsafe: it could be plugged into a speaker dock, an amp or a recording device. Some headphones also have an additional volume control on the cord, and regardless, the amount of sonic power transferred depends on the design of the headphones and whether they fit the person's ears well.

Two, the feature is designed in the most user-hostile manner. If the screen happens to be off or out of sight when you push the volume above 50%, you won't notice anything except that your button stops working until you wake up the screen and press "Ok". Worse, after a certain amount of play time has passed, the volume will automatically be kicked back to 50% and the pop-up will return, for that's what the law apparently requires. There's no way to disable this 'feature' permanently. Volume regulation on Android is broken from a user's point of view.

Ridiculousness of law aside, there are any number of ways this could've been done more elegantly. An audible signal could be played along with the message, to provide feedback rather than failing quietly. Pressing volume up again (or twice more) should be interpreted as consent and dismiss the message. Users should be able to permanently disable the warning, for any situation where their hearing is not at risk, or for anyone who understands that banning smoking in parks doesn't make car exhaust any less toxic. And if the lawyers tell you to annoy the hell out of your users, only do it when you are absolutely sure it's required, not across the board, to everyone, with one of the most unimaginative implementations ever.

Oh and notice how it charmingly blacked out the copy of Transformers that Play Movies was playing in the background when taking a screenshot. Google *Play* clearly excludes sharing, do keep that in mind.

## The Wobbly Camera

Moving on, Android 4.2 includes a completely redesigned camera app, with fun features like Photo Sphere and a more minimal UI. It seems pretty slick and follows the crisp white-on-black style of Jelly Bean. However within 10 seconds of using it, it will eagerly show you how stupid it is:

**Make important things fast**

“Not all actions are equal. Decide what's most important in your app and make it easy to find and fast to use, like the shutter button in a camera, or the pause button in a music player.”

**Delight me in surprising ways**

“A beautiful surface, a carefully-placed animation, or a well-timed sound effect is a joy to experience. Subtle effects contribute to a feeling of effortlessness and a sense that a powerful force is at hand.”

When you rotate the device from portrait to landscape, it freezes the screen so it can do a completely useless transition. The image doesn't change, the widgets don't actually move anywhere, the controls just rotate out and back in again, and the focus ring trips out for a bit.

Somewhere, a Google developer probably realized this, thought about it, and said "Fuck it, I'll use `com.google.android.paint.by.numbers`

" instead of handling the odd upside down case elegantly.

Switching a camera from portrait to landscape is one of its main affordances. Android manages to jank even this up. To make matters worse, this minimal UI misses the mark: there is only one thing you can do with just one tap, and that's taking a picture. You can argue this makes the camera easier to handle, but I bet there's more than one Nexus 4 user who's never used the front camera, something more important than adjusting the white balance.

![Android camera](../../assets/916bc3681c536834.jpg)

There's a button for toggling recording mode and a radial menu for everything else, but no labels or hints in sight, not even on confirmation. Meanwhile switching between the pre-set "scene modes" requires 4 taps and a buried menu, which either says "we forgot to include this in our wireframes" or "nobody really knows what this is for anyway".

In the age of HDR imaging and live color filters, is there much reason to model a virtual camera after the confusing set-and-pray buttons of their physical counterparts, many of which only mimic film cameras to humor you?

The Instagram-like filters that you can apply afterwards are functional, but the UI for applying effects and transforms is its own kind of weird, lacking useful feedback in several places. It also requires you to flick an invisible mirror to apply a mirroring effect, after pressing the Mirror button, I shit you not.

The only thing that's genuinely clever about it though is how the camera acts like the newest picture frame in your gallery view, here on the left:

![](../../assets/4d56252356b80a8f.jpg)


However even this view is hard to use, because it uses the most uncomfortable form of inertial scrolling and snap-to-item seen on the platform yet. It moves like a slot machine wheel, flipping over at the very end. Dear UI programmers: please go learn about easing and the equations of motion, you really can't arse your way around these things anymore, unless the demographic you were aiming for was grannies in Vegas.

**Real objects are more fun than buttons and menus**

“Allow people to directly touch and manipulate objects in your app. It reduces the cognitive effort needed to perform a task while making it more emotionally satisfying..”

![network selection](../../assets/901f4dfadd457493.png)


## The Network Cocktease

But the most amazing example has to be the Network Operator screen. This dialog, normally buried, is presented when you lose connectivity. It's not just completely dysfunctional, but has remained unchanged for years. We're talking about the feature that turns your phone from a mostly useless brick into a node on the global voice and data network. It's kind of crucial when you need it.

If you're here, it means something has changed. Either you've travelled to a foreign country, you've just spent a noticeable time out of cell range, something's wrong on your operator's end, or the [software messed up](https://code.google.com/p/android/issues/detail?id=2845). Your goal is simple: to confirm to the phone which network you'd like to use and *start to reconnect* right now, so you can get back to business.

Unlike Wi-Fi, scanning for mobile networks can take a while. I've tried to dig into the relevant specs to see exactly why this is, and there doesn't seem to be a clear reason for it: networks advertise themselves, cell phones simply listen in, tuning to various channels to do so. But I may have missed something, given that 3GPP specs make W3C specs look like florid prose.

Most users just want the phone to choose the right network automatically, selecting their home network if it's available, or roaming on a preferred partner. This is done using a list stored in the SIM card, and hence all known ahead of time. So what went wrong?

![Android Network Selection 2](../../assets/6ae15be78738b1ba.png)

First, the obvious one: despite Android's emphasis on letting background processes and services run freely, scanning for network operators is a modal process. Scanning starts as soon as this screen is opened, and the only way to keep it open is to not touch anything. You have to wait until the phone finds all results to select one. Which means the 99% of users who wish to "Choose Automatically" have to wait for no reason.

But suppose you're travelling and you've set your display timer to a modest 15 seconds to conserve battery. Now the screen will shut off before scanning has completed. You'll want to just let the phone sit for a bit and then pick it up again, right?

Wrong. See, scanning completed ages ago. But because you weren't here to watch the phone do it, you can't actually select any of these options, because the modal popup will now never go away. Tapping it does nothing. Tapping in the dimmed area around it instantly closes the whole screen. If you try to return, the whole scanning process starts over again, because the results weren't even cached for 5 seconds.

This is Utterly Broken. Users go here because they want to pick an option, so it should maximize their opportunity for doing so, not do the opposite and fail completely. If there is a preferred provider available, it should indicate that it knows this, not just suggestively put it at the top of the list while being coy about it.

It's also a classic example of Google-Don't-Care: the Nexus One had this screen, the Nexus 4 still has it. Because most people only use this in unusual circumstances, it hasn't been on anyone's radar to merit fixing, despite several major OS revisions. But when you're walking around a foreign city, running late and needing to call someone, few things will make you want to toss your phone against a wall more than this.

**It's not my fault**

“Be gentle in how you prompt people to make corrections. They want to feel smart when they use your app. If something goes wrong, give clear recovery instructions but spare them the technical details. If you can fix it behind the scenes, even better.”

**I should always know where I am**

“Give people confidence that they know their way around. Make places in your app look distinct and use transitions to show relationships among screens. Provide feedback on tasks in progress.”

![android clock: good](../../assets/80a5d391e75bd69c.png)


![android clock: bad](../../assets/c45ff4d5017858e5.png)


![my phone](../../assets/ab3218a4a99f9b31.jpg)


## The Times They Are A-Changing

Level such criticisms at any good Android fanboy though, and you'll hear back a common refrain: "Yes, but, things are changing! It takes time to change a developer culture."

That would be valid, if some of the worst offenders weren't completely new in the latest upgrade. You can't set a good example with one mediocre experiment after another.

The other rebuttal is, "There's a replacement app for that, that's the beauty of Android." And indeed, I do use a custom launcher and root my phone. But the result is still a series of apps, not a mobile desktop.

The way I see it, there are basically four tiers of Android apps right now.

First, there's all the iOS apps that were ported over with no regard for the platform, which just feel like second-rate versions of better things. Luckily these are being replaced with native look-and-feel, with Twitter being a recent example.

Second, there's the legacy of Android 2.x, whose widgets and pop ups still show up with alarming regularity, serving as a constant reminder to stay away from the Play Store as much as possible.

Third, there's the mismatched Google apps from the No-Man's Land of Inbetween, like Play, Plus, Maps, Goggles, Reader and YouTube, which each have their own spin on the flatter UI with varying levels of blandness vs sophistication.

Finally there's the modern Roboto Thin style of Jelly Bean, which oscillates strangely between a Braun-esque brilliance and a confusing form-over-function Sci-Fi UI not meant to be seen or used up close.

There's nothing to tie it together but a bunch of disjoint cloud services. Are we all going to stay in our isolated messaging silos? Keep on emailing each other DropBox URLs? Substite mediocre AI for fine-grained control and precision?

As an end-user, Android feels like it's a glimpse of something great now, but there are too many forces pulling it in different directions. If there's someone whose job it is to curate the Android experience and make it excel, their vision is not being realized effectively. Too much manual assembly is still required.

The past decade, we've seen what was once just Apple's domain become mainstream, that is, bringing high-end UX design to software. But I can't help but feel some of the finesse has been lost. Gripes about iOS and OS X suggest the same is true for Apple as well.

You hear a lot about "first time user experience" for example. But it's not about wrapping up your product like a present. It's about creating a connection of trust through empowerment and a little bit of emotional appeal: "This is for you, you can do amazing things with this." And that means "first-time" shouldn't refer to the first time you turn on the device, but the first time you use a device *for a particular purpose and context*. Travelling to Another Country should definitely be treated as a "first time" experience, same with How Do I Work This Camera, I Don't Have an App For This, I Don't Have Data Right Now, I Dropped It Down The Stairs, I Should've Cached This Map But I Didn't, My Friend Has a Windows Phone, etc. Throwing in more obnoxious tutorials is not the answer, creating affordance is.

One of the most brilliant things Apple did for the iPhone was to make screenshots easy. People could show what they were doing with it, it empowered them to do so, popping up in articles and feeds. It took until Android 4 before you could do that without a USB debugger, so the only screenshots we got were taken by developers. Which platform has which image today? The iPhone isn't actually *that* intuitive, but most people already knew all about swiping and pinching by the time they picked one up for the first time. But the Android experience cannot come into its own when it's only chasing the walled gardens that already exist. It lacks agency for the user and pretends the cloud can pick up the slack.

The most annoying part is, the worst bugs are well known, and the war over services is obvious. The issue tracker has long been full of reports and me-too-s and [dear-god-when-will-this-be-fixed](http://code.google.com/p/android/issues/detail?id=40365). Owning an Android means you accept having something that's always a bit broken, which doesn't integrate as well with anything you do as an iPhone does with its family, and just substitutes Google for Apple more and more. I'll stay on this side, I like my phone to be hackable, but that means being able to shut off the stupid warnings too, and having an OS actually worth hacking for.

If the insides of this phone were as thoughtfully put together as the outside, Android could be to mobile what OS X was to the desktop in the 2000s. But so far, no dice.

Above all, it's true what Steve Jobs said: Android is a stolen product. After so many years, there is little about the platform that can be said to set it apart from direct competitors. It's now just a mostly well done version of the same thing. I'm one of those old fogeys who has resisted getting a tablet, simply because I don't want a gianter phone. I want a *touch computer*, with everything that implies, not just something to do email and watch movies on.

*Quotes from: Android – Design Principles, Google Inc. (cc)*