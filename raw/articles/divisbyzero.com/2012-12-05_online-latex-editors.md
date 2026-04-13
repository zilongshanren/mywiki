---
title: Online LaTeX editors
url: https://divisbyzero.com/2012/12/05/online-latex-editors/
author: Dave Richeson
published: '2012-12-05'
source_blog: 'David Richeson: Division by Zero'
source_site: https://divisbyzero.com
category: game programming
fetched: '2026-04-13'
---

For the last 10+ years I’ve taught topology using a modified [Moore method](http://en.wikipedia.org/wiki/Moore_method), also known as [inquiry-based learning](http://en.wikipedia.org/wiki/Inquiry-based_learning) (IBL). The students are given the skeleton of a textbook; then they must prove all the theorems and solve all of the problems. They are forbidden from looking at outside sources. The class types up their work as they go. At the end of the semester they have a textbook **that they wrote**. It is a great way to learn, and at the end of the semester the student are thrilled to hold a bound copy of the textbook that they created.

When I did this first (as a student) it was a Word file shared on a floppy disk. When I started teaching the class this way it was a Word file emailed between participants. Later I rewrote the textbook as a LaTeX file. I’ve experimented with various means of collaboration. Most recently I used a shared [DropBox](http://db.tt/c8nOEkH) folder to house the file. This way all of the students could collaborate on the ever-growing document.

This approach worked pretty well, but there are a few downsides. The document occasionally got forked. This happened when two or more students edited the document at the same time. It would take a while to merge the content back together. Also, a student must have LaTeX installed on his or her computer or must be willing to work on one of the computers in our building.

This spring I’m considering trying an online LaTeX environment. (And, in fact, I’m also going to try using this IBL approach in my Discrete Math class—our “intro to proof” course). I wanted a robust, easy-to-use online solution that would house the LaTeX files and any extra files (images, etc.), would allow the students to compile the document online, would allow us (me) to download the files at any time, would allow collaboration by up to 16 people (with 0-3 people editing at any one time), and would allow access to previous versions (in case someone deletes the entire document, for example).

After a little investigating I found these great sites. So I thought I’d share them with you.

[ShareLaTeX](https://www.sharelatex.com/)(which, from what I can tell, has merged with the popular[ScribTeX](https://www.scribtex.com/))[SpanDeX](http://spandex.io)[WriteLaTeX](https://www.writelatex.com/)[MonkeyTeX](http://monkeytex.bradcater.webfactional.com)

Most of them have free and pay versions. It is likely I’ll have to pay for an account so that I can be the “owner” of the file (the textbook), then the students can get free accounts and I can add them as collaborators.

Not all of these sites fulfill my complete wish list—especially the version history requirement—but it looks like they’re all being actively developed and that new features (version history, DropBox integration, etc.) are right around the corner. I’m thrilled that the technology has come so far. I haven’t decided which one I’m going to use. If you have any thoughts/preferences, post them in the comments. Likewise, if I’m missing any sites, suggest them in the comments too.

If I could add some items to my wish list it would be:

- Point-and-click menus containing the common LaTeX symbols. This isn’t a key feature for me, but the students would love it. (In the meantime I’ll have to point my students to my
[quick guide for LaTeX](https://divisbyzero.com/2011/08/17/a-quick-guide-to-latex/)and[Detexify](http://detexify.kirelabs.org/classify.html).) - Table and array editors in which you enter the contents of a table in a grid (like
[this](http://truben.no/latex/table/)), then the editor would insert the code into the document - A BibTeX interface to help create a .bib file. At a minimum something like
[this](http://truben.no/latex/bibtex/), but even better, something that would tie in to databases such as Google Scholar, MathSciNet, Zentralblatt, and JSTOR and scrape the bibliographic content for you.

I like the basic idea. Topology students tend to be a bit more advanced, and maybe easier to sell on LaTeX. Do you anticipate the format for writing to be a barrier for discrete math students?

I would guess that they are not all thinking of math grad school.

I’ve had my students use LaTeX in quite a few courses. I’ve found that they love it. One semester I had my Discrete Math students create wikis—all of the math was in LaTeX. They did fine with it.

But ease-of-use is one of the key features I’m looking for. I want the interface to be simple to use and robust. The difficult LaTeX in the textbook is created by me in advance. They just have to type the proofs into the appropriate spaces in the book. It is an experiment. We’ll see how it goes…

I’ve been having my students type up their homework using LaTeX in my intro to proof classes and it has been working great. I believe this class is at the same level as Dave’s discrete class. Having the students use an online LaTeX editor removes one of the major obstacles to getting started with LaTeX (i.e., installing a front end and back end on your computer). Another advantage to the online editors is that the students can share their documents/projects with you. In this case, you can access the file a student is having trouble with. In my experience, I have to help quite a bit during the first couple weeks and then they are pretty self-sufficient after that.

I’ve had a lot of success using ScribTeX with my students in the past. Because of this I had been leaning towards using ShareLaTeX (ScribTeX and ShareLaTeX have now merged). However, after some fiddling around with SpanDeX, I’m impressed. In particular, the built-in help for SpanDeX is excellent.

Those are the two I’ve been playing with most. I’m leaning toward ShareLaTeX, but only barely. (I found SpanDeX a little buggy while playing with it (I think it is a newer site). But the people running it responded to my emails extremely quickly. I predict it will be a solid platform very soon.) I’m still undecided.

Hi Dave, Josh from SpanDeX here :) we are a bit newer, and the first to push features like version history, Dropbox, and some other coming-soon features, so there are some bumps along the way. If you’ve run into any issues you haven’t emailed me about yet, I’d love to look into them.

Thanks for the writeup. Your wish list confirms a few things we’ve been wanting to work on. Particularly, my favorite would be Detexify integration.

Hi Josh,

I was thrilled to see your announcement this morning about Dropbox integration. I’ve been very impressed by your responsiveness to my emails. My only hesitation is entrusting a major portion of my class to a website that is still sorting out bugs like this. Even if they get fixed in a timely fashion I need a product that has nearly 100% up-time. That’s why I’m on the fence. Otherwise SpanDex is my favorite option for what’s out there right now.

Dave

Hi, Dave, as I mentioned in my email I have a lot of experience with scaling and site stability projects, and in the next month that’s one of our top priorities. We haven’t had any major problems with down-time but we’re engineering fail-safety to make it nearly impossible :) Hope that eases some of your fears.

Have been squashing lots of bugs and making small usability improvements here and there the past few days; some more announcements will be coming tomorrow or Monday.

Thanks again for your support, patience and feedback so far!

I vaguely recall some online TeX programs working with google docs, which I’ve found to be the absolute best thing for big-group editing. It wouldn’t have anything nice for clicking to get symbols, but you’d never have to worry about forking, and you can just tex a google doc file whenever you need it.

There is a site called “Latex Lab” that supposedly ties in to your Google Docs account http://docs.latexlab.org/. But I was too squeamish to click the “allow” button to allow a third party access to my Docs. I’m probably being paranoid.

Do you have a sample page (or few pages) from these Course Notes? I’d love to see them. I’m in the process of trying to convert my own Course Notes into LaTeX and so I’m trying to see what aesthetic look I prefer (e.g., where to put page numbers? Section headings? Number theorems by section, or something else?). Are the notes based of the article class? (I’ve been using exam.cls because I like the \question command and its options.)

Kate—you’ve inspired me to write a blog post about this. (I’m surprised I haven’t yet.) In the meantime I’ll send you some things offline.

Kate, you can see what my intro to proof notes look like by going here:

http://danaernst.com/archive/spring2012/ma3110/notes.html

I’ll be bundling each of the separate files together and adding more soon. I’m curious what your notes end up looking like using the exam class.

Would love a sample copy of your Course notes too. Intrigued by the book u get your students to create. I presume u provide the skeleton text, in LaTex? How complete is this skeleton book u provide for your students? Have u written a blog on that book the students create?

regarding forking/merging documents, there is well-established in computer programming technology to deal with this, namely version control systems. Unlike dropbox, one is in control of what gets forked and merged, and there are free online facilities to deal with this, such as http://bitbucket.org and http://github.com

E.g. I completely switched over to using bitbucket.org for writing joint papers, for it is very easy to track changes…

Yes, that would be a great option for collaborating with other professors, but I’m hesitant to go that route with 30 students (next semester they’d be first-years or sophomores). Too many headaches. I’m looking for the simplest, most robust solution possible.

If you have 30 people editing a collection of documents simultaneously, a version control system like the ones behind bitbucket (mercurial) and github (git) is the way to go. It’s way more robust than dropbox or any other “cloud” setup, as everyone works on his/her own fork that gets merged into master. There is certainly a learning curve involved, but chances are that among 30 people there would be someone knowledgeable about it already (and, after all, learning a bit of software engineering along the way would not hurt the students…).

Thanks, Dima. I’ll look again at what that approach would entail.

You could even just collaborate directly on github (though you’d be missing the nice point-and-click features). You can create files there, when a person edits the file, it automatically sends a pull request to you (or you can just add them as a collaborator).

I’ve decided to try these out while writing exams.

I just wrote my euclidean geometry (math 3600) exam with writelatex. I’ll do two other services for my other two exams over the weekend. Then I’ll post a little comparative review.

It would be fantastic if you reported back about your experiences. Thanks!

Reblogged this on Astronovae.

Hi Dave,

One of the founders of writeLaTeX here – thanks for the review and comments, there are lots of great things happening with online LaTeX editors at the moment!

I wanted to let you know that we rolled out a number of updates to writelatex.com in December (just after you wrote this!), including:

* Support for user signups (to help you manage your documents);

* Additional help and examples, to make it easier to get started;

* Faster previewing of the output – some work behind the scenes to improve the speed of our auto-preview feature – making it easier to keep on top of errors.

Hope you give the updated site a try, and look out for more developments in 2013 :-)

Best,

John Hammersley

That’s great. I really like the writelatex editor. Is version control and Dropbox integration in the future?

Thanks, glad you like it – we focused on ease of use to help lower the entry barriers to getting started with LaTeX.

Version control and dropbox integration are both on the way, plus a few other things – I’ll let you know as we roll them out.

Hope you’ve had a good start to 2013 :-)

John

Great. The other thing I really like is that you can edit documents on the iPad. That isn’t possible with the other two I mentioned.