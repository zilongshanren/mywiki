---
title: 'Interview: Marco Castelluccio & Mozilla Apps in Ubuntu – Mozilla Hacks - the
  Web developer blog'
url: https://hacks.mozilla.org/2012/06/interview-marco-castelluccio-mozilla-apps-in-ubuntu/
author: Eduardo Bouças
published: '2012-06-13'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

![Marco Castelluccio Marco Castelluccio](../../assets/967add70eff5aca2.jpg)


*Hacks blog readers might remember Marco Castelluccio. Back in March we published an interview with Marco after he took first and second place in the IndexedDB Dev Derby with eLibri and FileSystemDB.*

*Since then Marco has ramped up his contributions to Mozilla and the Open Web through a Google Summer of Code project building web runtime support for Firefox on Ubuntu. Mozilla’s Open Web Apps stack is available now for Linux users. Visit the Firefox Nightly channel to download Firefox 16, then you can run, install and separately manage web apps in the browser on Ubuntu.*

*We were thrilled to learn about his project, and decided it was time to check back in. Here’s Marco in his own words:*

**Marco, it’s great to get back in touch. Please share a bit about yourself: where you live, what you’re working on, and what you’re passionate about: **

I live in Napoli (Naples) and study Computer Science Engineering at the University Federico II. My passion is computer science—I like experimenting with new solutions and technologies and I like working to develop something useful to people. These are the reasons why I decided to start contributing to Mozilla projects.

My other passions are reading and cinema. I like classics (*“A classic is a book that has never finished saying what it has to say”*) and science fiction books.

You can see another of my passions in the photo above.

**How did you get involved in contributing to Mozilla? How did you get started with Dev Derby?**

I started contributing especially because I believe Mozilla is one of the few foundations that can struggle for users’ freedom on the Web. And, obviously, also to satisfy my hacking hunger. I started contributing in the last year, but with simple fixes and so on. In recent months I’ve started to contribute more seriously.

I think Dev Derbies are a great opportunity to learn the new WebAPIs, so I started just for learning purposes. Sadly I didn’t participate in the last three or four, but I’ll begin participating again in the future.

**What inspired you to work on bringing the Mozilla Web Apps stack to Ubuntu?**

The Open Web Apps project is really important for a lot of reasons (both for developers and users). In particular, it has a surplus value for Linux, a platform sometimes snubbed by developers. With Open Web Apps, applications are cross-platform by definition.

In future, in my opinion, the operating system will slowly become less important. The framework where the applications will run won’t be the operating system anymore, but the browser. This is why a project like this is really important for the Mozilla mission.

**Tell us a little about your developer tools and work environment for development?**

I use Linux, because it provides really useful, simply installable and, above all, really powerful development tools. I use the [GCC compiler](http://gcc.gnu.org/), [GDB](http://sources.redhat.com/gdb/) for debugging (it’s marvellous what you can do with GDB), and I have a virtual machine to test the work with several distributions and several desktop environments. As a side note, the compilation performance is really awesome with Linux, and saving time during compilation gives you more time to effectively develop.

**I heard that you are working on this as a Google Summer of Code project, is that correct? Can you tell us more about how that happened?**

Yes, initially I proposed two projects: this and the development of an eBook reader application. In my opinion, the [GSoC](http://code.google.com/soc/) is a great opportunity for open source projects to attract new contributors. (Though some people only want the money, many people work with passion. For example, I haven’t even activated the Google credit card yet…)

**How long have you been working on this? What are the next steps for this project?**

Development for the GSoC officially started May 21. But I already started the work a bit before, even if I didn’t think I could finish a part of the work in time for Firefox 15. The project obviously is not yet completed, however. We need to do a lot of testing on several distributions and desktop environments, as Linux’s greatest quality is also its greatest flaw: the infinite possibilities of personalization. There are only a few standards, and they aren’t always followed to the letter. So you can run into a lot of problems.

The next step, aside from testing, is the implementation for uninstalling applications (it’s manual so far). Uninstall will be possible through a desktop action and through a Firefox specific page.

I think we’ll also try to improve system integration with apps. Maybe we’ll solve this by developing addons for the most used distributions (where the code is too distribution-specific to be included in Firefox). For example we could integrate the webapps uninstallation in the Ubuntu Software Center. Actually, my idea was to develop a skeleton addon that distributions could simply modify.

Another bright spot is that the implementation that I developed, unintentionally, works even on other Unix platforms.

**How do you work with the Open Web Apps development team to land your code? Anything about the experience you’d like to share?**

I’m in harness with my mentor, [Felipe Gomes](https://twitter.com/#!/felipc/). I often contact him when I have problems or when I need to know who’s the right person to contact for a specific problem. Frequently he is contacts me to make sure that I don’t have any problems (in short, he’s very kind). Once you know the other developers on the team, however, you can work more quickly. So, if you start to contribute, don’t be afraid to ask questions.

**What are your plans for when you finish your studies?**

I haven’t precise plans, but I’d really like to work for Mozilla or in the research field. I think the next year (that’s my third year at the University) I’ll apply for an internship at Mozilla. Anyway, I’ll for sure continue to volunteer for Mozilla. I’d really like also to develop some mobile applications (obviously using web technologies) to see if they can make a success or not.

**Have you thought about developing an HTML 5 app? (Are you already working on an app?)**

I have many ideas. Mozilla’s new WebAPIs make it possible to develop web applications with the same capabilities as native ones.

I haven’t started yet, but I’d like to work on an instant messaging P2P application (I’m waiting for [WebRTC](http://webrtc.org/), as I want to experiment with it). I have an idea for an eBook reader application (that was the other opportunity for the GSoC) that I hope could be integrated in B2G. (If I recall correctly, the B2G phone needs something like that). I have several other simple app ideas.

As I’m also attracted by the idea of web games, I think I’ll develop a framework to simplify and speed up the development of 2D games.

**What are some of your favorite apps or games?**

I’m an admirer of videogames, I’m really excited by the idea of BananaBread or the other games that could be ported to JavaScript through Emscripten. I really also like the [Gladius engine](http://blog.mozilla.org/labs/2012/04/gladius-a-modular-3d-game-engine-for-the-web/). It’s something like the 2D games framework that I’ve got in mind.

About applications, I’m fascinated by [pdf.js](https://addons.mozilla.org/en-US/firefox/addon/pdfjs/). In my opinion it’s one of the best examples of JavaScript application. And, as I explained, I’m going to use it (along with other libraries that I’ll develop for other formats) to develop an eBook reader application.