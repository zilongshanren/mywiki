---
title: Master the Art of Perfection
url: http://www.learn-cocos2d.com/2011/04/master-art-perfection/
author: Steve Oldmeadow says
published: '2011-04-14'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Today I tweeted:

“How to be efficient? Don’t try to master the art of perfection.”


That seems to have caught some attention. I must admit it wasn’t entirely devoid of any meaning to my work. For all the time when I was an actual employee and someone else was paying me to do a certain job within a specified time frame as good as possible, it remained an elusive notion that one day, you want to do a job “right” for once. Because there’s always either time or budget cutting into what’s possible or worse what’s reasonable.

I always considered myself to be a pragmatic, and while I liked the notion of one day doing one’s work as good as one possibly can - a mantra some of my colleagues were more keen than others to repeat - I accepted that it would never happen. That was until I became responsible for my own work and financials. I recently started [digging into the Xcode 4 Template system](http://www.learn-cocos2d.com/2011/04/cocos2d-podcast-coming-2/), at first out of interest and requirements for the [Kobold2D](http://www.kobold2d.org/) project, and then to make quality documentation for the new Xcode 4 template system. I think that was about 3 weeks ago now, and recently I noticed I’m not going very far, I keep finding the roadblocks and dead ends and generally quirks and issues which end up in countless of hours doing nothing but trial & error with little results to show for.

And there I was, fighting with myself trying to figure it all out - I mean literally everything. And it was getting harder to finish the job because it became more and more demotivating not being able to find a good (or even a working) solution to my problem.

#### How not to get the job done, after it’s done

I fell to the elusive thought of documenting the Xcode 4 template system perfectly. I couldn’t succeed because almost by definition you can’t perfectly document a system that is in itself imperfect, flawed, incomplete and merely designed to be used for the things it is used for, no more no less. It’s not even designed to be used by others, or it would have been documented by Apple. I now have a very good understanding of why it was never documented, it just makes sense. My suspicion is that they don’t even edit the templates manually but instead rely on tools to do most of this job. And there seem to be a couple bad hacks in there too.

I had to accept that I’ll have to look for other ways for [Kobold2D](http://www.kobold2d.org/) users to start new projects because of several technical limitations of the Xcode 4 template system: it can’t deal with cross-referenced projects and it’s unbearable for projects with hundreds of files. One of the important goals for Kobold2D was to provide a variety of meaningful, working project templates. Very simple demo games. They’ll have to be created somehow, and sadly I had to come to terms that this won’t be possible within Xcode (4) and has to be done through some other means (and ideally not manually).

Trying to find a solution for Kobold2D project templates kept me working on the documentation even though I should have realized that I have already documented way more than what most people would need for their file and project templates. I couldn’t stop looking for a Project Template solution for Kobold2D, it seemed so close and other solutions so far - so I didn’t even spend time considering those other solutions. Awww, the horror of working alone. No one to kick your butt in the right direction, away from perfection and towards getting the job done. ![:)](../../../wordpress/wp-includes/images/smilies/simple-smile.png)


#### Decision

So today I decided that I’ll wrap up the Xcode 4 Template documentation I have so far, which is quite a lot nevertheless (currently 57 pages as PDF), and then start selling the document for $10 instead of $15 because it’s not as complete as I intended it to be. Watch for it in the next few days. I’ll let you know.

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

Le mieux est l’ennemi du bien. To quote Voltaire.

Have you considered using scripting for Kobold2D? The XCode IDE can be controlled by scripting, you can even run shell scripts from within scripts. Applescript is a bit weird but pretty cool once you get used to it. I could imagine a nice wizard type UI that sets up a project for you using scripting.

Good idea! I’ll look into Xcode scripting and see what’s possible, I was always looking for a reason to get into Applescript scripting actually.

I downloaded and installed Kobold2D. I chose the Hello template (and the physics effects template on the next try.) When I run, the build succeeds but the simulator does not load. If I load the simulator myself, and run the program, nothing happens. Should I have expected to see a xib file or a storyboard?

Change the build scheme, you’re probably just building one of the libraries like cocos2d or box2d instead of the app. Normally Kobold2D hides those schemes but only if you installed it for the current user by using the installer.

In Xcode, build scheme selection is just to the right of the Run/Stop buttons.