---
title: Simonschreibt.
url: https://simonschreibt.de/gdt/sacred-2-floating-point-numbers/
author: Simon
published: '2013-11-22'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

Numbers are useful but when they are over-used in an UI you may end up with some Excel-game. It doesn’t get better when you’ve to deal with floating point numbers.

1.0

In [Sacred 2](http://www.sacred2.com/) you can increase the level of your spells with special runes which are dropped by enemies. But it would have been too easy if you just jump from level 1 to 2 to 3 to 4 … instead you need one rune to get from level 1 to 2. But you need **two** runes to get from level 2 to 3. Three runes for the next level and so on. This means after using your 2nd rune the spell level is for example:

2.5

So what to do? The lazy (and ugly) way would be: just write out this floating point number. Our UI designer proposed a different solution and i have to admit that i thought it was a very stupid solution.

We’ll write the first digit and render the rest as “pie chart”-circle around it.


In general i have often the case that i hear some game design mechanic and think “That’s stupid!” but then i see/play/feel it and i think “Wow…that works great! I’m so stupid!”. And so it happened here:

Here you can see how the circle is divided into pieces and instead of writing 3.0 > 3.3 > 3.6 > 4 you just see the outline filling up.

I was really impressed by the simplicity and beauty of this solution which is why i made this article. Maybe this helps some people. If yes, don’t hesitate spend me a comment! If not, tell me what you think!

Thanks for reading!

nice design element – i like it

also it reminds me good widgets for mobile – showing battery charge

for example – https://play.google.com/store/apps/details?id=com.pjw.batterywidget&hl=en

(i think sometime appropriate change color or circle too – “color design”)

.

also can remember how games like “Diablo kind” and MMO

use set of strips instead of numbers – to display any information of interest

like – XP \ level \ HP \ shield level \ weapon magazine filling \ distance \ charge level

time \ capture point level-time \ there are many examples

i think basically this is one of the core of UI design

(how fast and easy transfer to the user only the information he wants)

.

also i accidentally thought presentation of

“Dino Ignacio” about “UI of Dead Space” on a similar theme

http://www.gdcvault.com/play/1017723/Crafting-Destruction-The-Evolution-of

Thank you very much for these links. Very good examples! Yes it should be the core of UI/UX design to not overwhelm the user but sometimes times this doesn’t work out well :D

good article ,will keep in mind if i ever make a rpg-ish game

THanks! Let me know if you implement it somewhere :)