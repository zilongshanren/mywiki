---
title: Learn & Master Cocos2D Game Development
url: http://www.learn-cocos2d.com/knowledge-base/free-source-code/
author: Matthew says
published: '2010-12-23'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

# Free Source Code

Download the free source code for cocos2d from my Codaset git repository: ![](../../images/logo.png)


[free cocos2d-iphone Source Code Collection](http://codaset.com/gaminghorror/free-cocos2d-iphone-source-code-collection)or click on the Codaset image.

I maintain a repository of commonly useful cocos2d free source code, most of which i

**obtained from other developer’s blog posts**(see backlinks in the code). As you may be well aware, most blogger’s code doesn’t even work out of the box. Often it is untested and still contains terrible bugs like memory leaks or crashes that only happen when you really put the code to the test. In other cases the code was simply never updated to work with the latest version of the cocos2d game engine or the iPhone SDK, leaving it in a broken state.

While i can not guarantee bug-free code that always works i did use all of this code in published Apps and continue to maintain the codebase. You may find some work-in-progress but i try to clearly mark it as such. I then decided to host my [collection of free source code for cocos2d-iphone](http://codaset.com/gaminghorror/free-cocos2d-iphone-source-code-collection) on Codaset so anyone can grab it from there. You can join Codaset for free and you are welcome to make changes, additions and bugfixes to this codebase as you see fit! If you add other developer’s code please add a comment crediting the original author and add a link to the blog post or article where you obtained the code from.

**Please report bugs as Tickets on Codaset, do not post bug reports in comments, thank you.**

Thanks you so much for sharing!

great,thanks u very much.

This is awesome, thanks Steffen

soo very generous of you, thank you for sharing!

Hi

these are great. Can you please explain how to use email in cocos2D in landscape mode.

Hi Narindar, good questions (also got your email). I’ll add how to do landscape in-app mail to the FAQ as soon as i can.

Hi steffen

I figured it out using the following code:

SendMail *sendMail = [[SendMail alloc] init];

sendMail.isHTMLBody = YES;

[sendMail displayMailComposer];

[[[CCDirector sharedDirector] openGLView] addSubview:sendMail.view];

[sendMail presentModalViewController:sendMail animated:YES];

[sendMail release];

Thanks so much for your sendMail


Cool, i’m glad you got it working! I know i had some issues going from Portrait to Landscape as well and they seemed inexplicable at first. Too bad i didn’t make a note what i did change to fix it.

Hey, Narider & Steffen…

Is Narider’s code for calling “SendMail” correct?

I can’t make it work; I keep getting a EXC_BAD_ACCESS error.

Does anyone else have an example of how to properly call SendMail from within a cocos2d layer?

The error means that for example a message was sent to a released instance of a class. It could be anything, ideally you should try running the app with NSZombieEnabled (needs to be added to executable setting, google it for details, it’s pretty well explained on other blogs). This will tell you the root cause (class) of the crash.

Steffen,

I was trying out some of your code-specifically simpleButton. Do you realize you are using the drawScene method you suggested but was not implemented? Did you subclass it?

Here’s where functional examples would come in real handy-That had me going for a while!

Yes, i hacked the drawScene method. Actually the call isn’t even needed anymore i probably just forgot to remove it.

Hi Steffen,

First of all, thanks for your codes and site. They’re of immense help.

I was looking at MenuGrid, and was wondering if it could actually accept SimpleButton? Since MenuGrid lays out menuitems, and well, SimpleButton is sort of a menuitem.

MenuGrid doesn’t support SimpleButton. I’m not sure of the reason, i think it’s because a SimpleButton is already a menu in itself and if i’m not mistaken you can’t have a menu of menues.

I’m after a big money format snippet, ie: turn really big numbers into a shorthand, such as:

1) 10,000,000 => 10m

2) 750,000 => $750k

3) 10,250 => $10.25k

Etc… Please could you post a snippet to deal with this?

quite useful, I like it.

Hi Itterheim. My english isn’t good enough Sorry for that. Congratulation finish your book “Learning Cocos2d iPhone iPad”. Did you made “Tetris”, “arkonaid”, “Pac Man”, “Mario” any platform?

Haha, no I didn’t do any of these.

I searched from google about “Game Programming”. Then wiki said me “make required game” little simple game (tetris,…).

Merry Xmas and a Happy new year Steffen.

Just wanted to thank you because your website has been a great help for me this year.

Thank you.

Ismael.