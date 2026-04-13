---
title: Archive for January, 2013
url: http://greyaliengames.com/blog/2013/01/
published: '2013-01-15'
source_blog: Grey Alien Games
source_site: http://greyaliengames.com/blog
category: game programming
fetched: '2026-04-13'
---

*(click to enlarge)*

It’s been a while since my last [Titan Attacks developer diary](http://greyaliengames.com/blog/titan-attacks-mobile-developer-diary-2/) and that’s due to two things:

1) I spent a couple of weeks banging out a new version of one of my games called [Holiday Bonus GOLD](http://www.greyaliengames.com/holidaybonusgold/index.php) and it launched on iPad/Android/PC/Mac in December. It was a spur of the moment thing to make that game but it should generate some good money (it got to no.2 on iWin.com!) and give me more indie “runway”, which is always a good thing.

2) I had a couple of weeks of lounging around, playing games and doing family stuff over Christmas

**Anyway, here’s what’s new since the last update:**

– I finished ripping out all old code and media from the project which I’d copied from another of my games. It always feels good to have this step done so that your new game is 100% “clean”.

– Added a tank that can fire multiple bullets and a basic background.

– Added a control method where you can move your finger anywhere to position the tank instantly and it autofires on finger down. However, it turns out this method won’t work because you sometimes need to be able to position the tank under a parachuting alien and catch it without shooting it. So I’m tweaking this control method to require a second finger to fire.

– I’ve been doing a ton of GUI code and that started with a new TVisualComponent class that I then extended other classes from. For some reason I never did this in previous frameworks (this one is technically my 5th framework and it’s shaping up to be the best one yet).

– Created a TSliderControl class and hooked it up to the player as another control method along with a fire button. See the image below (click to enlarge). As you slide your finger around in the rectangle the tank moves the full distance across the screen. This will be really useful on iPad. It feels smooth and good to use.

– Made an options screen so I could change control method on the device and then test it and get other people to test it. The final game will also allow you to change control method.

– Made the controls and buttons work with multi-touch on phone. This took quite a lot of fiddling to get right, but I properly understand the “problem space’ now.

– Got basic settings data saving/loading so that the game can remember the last control method you used.

– Improved my Screen Manager system to handle modal screens and multiple screens active and/or visible at once (e.g. show in-game menu over game-screen and call another dialog from that). I already had something basic that worked but this is a lot more flexible for the future and will require less code to add pop-up dialogs.

– Added a button down state and a bunch of other mini GUI tweaks/fixes that seemed to take forever as every time I changed something I spotted something else.

– Made mouse/finger up operate buttons instead of mouse/finger down. This turned out to be pretty complicated, especially on iOS as I’ve made it keep track of which finger first presses down on the button so that it can still activate it even when it moves away (but is not lifted up) and comes back to the button. In all my previous games the buttons activate on mouse/finger down which feels snappy but it’s not how OSes do it and nor how most decent games on iOS do it, so I changed my framework finally to handle this.

**Next up**

– Changing layout based on device orientation. Already components spread out and centre based on different aspect ratios but I want it to be dynamic.

– Tilt control method

– Finish tweaking/testing “easy” control method of placing finger where you want the tank to be.

– Add in first enemy.

OK that’s it for now. I’m going to meet Cas (from Puppy Games) and Cliffski (Positech games) on Wednesday, so I’m aiming to get more stuff to show them such as the game changing layout based on device orientation. All this GUI/framework stuff doesn’t move the game forward gameplay-wise but it’s a solid base for me to build this game, and future games, on.