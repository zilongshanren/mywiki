---
title: My Biggest Fear for the Future of Human-Computer Interfaces
url: https://etodd.io/2013/03/18/my-biggest-fear-for-the-future-of-human-computer-interfaces/
published: '2013-03-18'
source_blog: Evan Todd
source_site: https://etodd.io/
category: game programming
fetched: '2026-04-13'
---

# My Biggest Fear for the Future of Human-Computer Interfaces

I recently had to install and configure an 18-node [OpenStack](http://www.openstack.org/) cluster, a process which involved a lot of SSHing and text-editing in terminals. I thought about learning Vim, but I was afraid of the incredibly steep learning curve, so I made do with GNU nano. It's not at all powerful, but it's easy.

Eventually I realized, "This is my job. This is what I do every day. Why am I holding off on learning something *now*, thinking it will slow me down, and that I'll have time to learn it later? It's not like I'm anticipating a major career shift any time soon."

With that in mind, I quit nano cold-turkey and moved to Vim. I won't waste time explaining why it's so great. There are already plenty of [fantastic articles](http://www.viemu.com/a-why-vi-vim.html) on that subject.

I'll just say this: Vim is powerful because it opens up a new interface to interact with your entire computer. Especially on Unixes, there's hardly anything you can't do with a shell and a good text editor. Which means you have **one consistent interface** that exposes everything on your computer.

Think of that. How many poorly designed, mismatched UIs do you use on a daily basis? Right now I have Chrome, Steam, Spotify, Windows Explorer, and Visual Studio open. I see about fourteen different UI paradigms cobbled together here. *And,* if I click in the lower-left corner, I get a completely disorienting context switch into an entirely different paradigm (that of the dreaded *Metro tiles**)*. I'm at the mercy of all these hapless UI designers.

Each one of those programs has a UI that I had to learn, each with their own quirks and bugs. Granted, Spotify and Chrome are both shining examples of UI design. I think they're about as good as it gets. Incidentally, web browsing and music organization are two things I will probably never do in a terminal.

Exceptions aside, it's incredibly empowering to be able to operate your computer on your own terms. And that brings me to my biggest fear for the future of human-computer interfaces:

**There is no terminal in the cloud, or on mobile.**

"That's good, right? CLIs are old and not at all user-friendly."

No argument there. But imagine for a second what a UI would look like if it had all the capabilities of a CLI with none of the cruft.

- Again, it would provide one consistent interface between you and all your apps.
- On the other hand, it would allow you to operate your apps on your own terms. Going with the analogy, right now you can choose one of 17 different shells and 5 text editors. Apache doesn't care what editor you used to configure it.
- It would glue together all your applications, connecting them together however you want. In a CLI, that's accomplished with a single keystroke.

Compare that with current trends:

- Cloud applications are the future of computing. Yet, to copy a picture from Facebook to Gmail, I still have to download the image, save it to disk, and upload it to another server. Most people don't have time to figure out how to do that.
- Mobile applications, the uh, other future of computing, are notorious for not working with each other. Particularly on iOS, where the filesystem is almost completely opaque. On Android, it might as well be.
- In both cases, each app has its own set of paradigms which do not relate to other apps at all.

The *whole point* of the internet is to connect things together through a common interface: HTTP and hyperlinks. These days, web apps have a single URL with a giant hashtag fragment appended. That breaks the interface. I can't write a script against that; I'd have to simulate user clicks.

"No you wouldn't, it's probably calling a RESTful API!"

Yes, the one shining light of hope is that every web app now has a nice, friendly, documented, open API. No, there are still major problems:

- The main use of these APIs is still just identity. Great, I can connect my Facebook to my account on the pygmy llama forums I visit! Oh wait, all it does is save me the hassle of logging in all the time. I still can't have these two "apps" communicate with each other in any meaningful way.
- Third-party clients are the other use-case. Great, I can choose between 3,000 different Twitter client apps! Oh wait, each one still only talks to Twitter and nothing else.
- In the few instances where apps
*do*talk to each other, it's only because the users bugged the developers enough for them to coordinate a common interface. The users can't operate their computer on their own terms. They're dependent on the developers to add this functionality.

Contrast this to command-line tools, where every program is designed from the ground up to work with other programs through common abstractions, most notably files and pipes, and where having a UI automatically entitles you to a scriptable API.

In short, open web APIs are good but not good enough. The question is, can we design an interface that has the power of a CLI with the user-friendliness of a GUI, and that is designed from the start for cloud and mobile environments?

If we don't, we will eventually lose control of our own computers; we'll be at the mercy of app developers.