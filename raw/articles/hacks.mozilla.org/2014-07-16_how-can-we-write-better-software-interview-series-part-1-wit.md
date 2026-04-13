---
title: How can we write better software? – Interview series, part 1 with Fernando
  Jimenez Moreno – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2014/07/how-can-we-write-better-software-interview-series-part-1/
author: Shane Tomlinson
published: '2014-07-16'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Do you ever look code and [murmur a string of “WTFs?”](http://www.osnews.com/story/19266/WTFs_m) Yeah, me too. As often as not, the code is my own.

I have spent my entire professional career trying to write software that I can be proud of. Writing software that “works” is difficult. Writing software that works while also being bug-free, readable, extensible, maintainable and secure is a Herculean task.

Luckily, I am part of a community that is made up of some of the best development, QA and security folks in the industry. Mozillians have proven themselves time and time again with projects like [Webmaker](https://webmaker.org/), MDN, Firefox and Firefox OS. These projects are complex, huge in scope, developed over many years, and require the effort of hundreds.

Our community is amazing, flush with skill, and has a lot to teach.

## Interviews and feedback

This is the first of a series of interviews where I take on the role of an apprentice and ask some of Mozilla’s finest

“How can we, as developers, write more superb software?”


Since shipping software to millions of people involves more than writing code, I approach the question from many viewpoints: QA, Security and development have all taken part.

The target audience is anybody who writes software, regardless of the preferred language or level of experience. If you are reading this, you are part of the part of the target audience! Most questions are high level and can be applied to any language. A minority are about tooling or language specific features.

## Questions

Each interview has a distinct set of questions based around finding answers to:

- How do other developers approach writing high quality, maintainable software?
- What does “high quality, maintainable software” even mean?
- What processes/standards/tools are being used?
- How do others approach code review?
- How can development/Security/QA work together to support each-other’s efforts?
- What matters to Security? What do they look for when doing a security review/audit?
- What matters to QA? What do they look for before signing off on a release?
- What can
*I*do, as a developer, to write great software and facilitate the entire process?

I present the highlights of one or two interviews per article. Each interview contains a short introduction to the person being interviewed followed by a series of questions and answers.

Where an interview’s audio was recorded, I will provide a link to the full transcript. If the interview was done over email, I will link to the contents of the original email.

Now, on to the first interview!

## Introducing Fernando Jimenez Moreno

![Fernando Jimenez Moreno](../../assets/af701acdc0bbd203.jpg)


Fernando talks about how Telefonica became involved in Firefox OS, how to bring a disparate group together, common standards, code reviews, and above all, being pragmatic.

### What do you and your team at Telefonica do?

I’m part of what we call the platform team. We have different teams at Telefonica, one is focused on front end development in Gaia, and the other one is focused on the platform itself, like Gecko, Gonk and external services. We work in several parts of Firefox OS, from Gecko to Gaia, to services like the SimplePush server. I’ve personally worked on things like the [Radio Interface Layer (RIL)](https://developer.mozilla.org/Firefox_OS/Platform/Architecture), payments, applications API and other Web APIs, and almost always jump from Gecko to Gaia and back. Most recently, I started working on a WebRTC service for Firefox OS.

### How did Telefonica get involved working with Mozilla?

Well, that’s a longer story. We started working on a similar project to Firefox OS, but instead of being based on Gecko, we were working with WebKit. So we were creating this open web device platform based on WebKit. When we heard about Mozilla doing the same with Gecko, we decided to contact you and started working on the same thing. Our previous implementation was based on a closed source port of WebKit and it was really hard to work that way. Since then, my day to day work is just like any other member of Telefonica’s Firefox OS team, which I believe is pretty much the same as any other Mozilla engineer working on B2G.

### You are known as a great architect, developer, and inter-company coordinator. For Firefox Accounts on Firefox OS, you brought together people from Telefonica, Telenor, and Mozilla. What challenges are present when you have to work across three different companies?

It was quite a challenge, especially during the first days of Firefox OS. We started working with Mozilla back in 2011, and it took some time for both companies to find a common work flow that fit well for both parts. I mean, we were coming from a telco culture where many things were closed and confidential by default, as opposed to the openness and transparency of Mozilla. For some of us coming from other open source projects, it wasn’t that hard to start working in the open and to be ready to discuss and defend our work on public forums. But, for other members of the team it took some time to get used to that new way of working, and new way of presenting our work.

Also, because we were following agile methodologies in Telefonica while Mozilla wasn’t still doing it, we had to find this common workflow that suits both parts. It took some time to do it, a lot of management meetings, a lot of discussions about it. Regarding working with other telco companies, the experience has also been quite good so far, especially with Telenor. We still have to be careful about the information that we share with them, because at the end of the day, we are still competitors. But that doesn’t mean we cannot work with them in a common target like what happened with Firefox Accounts.

### When Mozilla and Telefonica started out on this process, both sides had to change. How did you decide what common practices to use and how did you establish a common culture?

I think for this agile methodology, we focused more on the front end parts because Gecko already had a very known process and a very known way of developing. It has it’s own train mechanism of 6 weeks. The ones doing the most, the biggest effort of finding that common workflow were the front end team because we started working on Gaia and Gaia was a new project with no fixed methodologies.

I don’t know if we really found the workflow, the perfect workflow, but I think we are doing good. I mean we participate in agile methodologies, but when it turns out that we need to do Gecko development and we need to focus on that, we just do it their way.

### In a multi-disciplinary, multi-company project, how important are common standards like style guides, tools, and processes?

Well, I believe when talking about software engineering, standards are very important in general. But, I don’t care if you call it SCRUM or KANBAN or SCRUMBAN or whatever, or if you use Git workflow or Mercurial workflow, or if you use Google or Mozilla’s Javascript style guide. But you totally need some common processes and standards, especially in large engineering groups like open source, or Mozilla development in general. When talking about this, the lines are very thin. It’s quite easy to fail spending too much time defining and defending the usage of these standards and common processes and losing the focus on the real target. So, I think we shouldn’t forget these are only tools, they are important, but they are only tools to help us, and help our managers. We should be smart enough to be flexible about them when needed.

We do a lot of code reviews about code style, but in the end what you want is to land the patch and to fix the issue. If you have code style issues, I want you to fix them, but if you need to land the patch to make a train, land it and file a follow on bug to fix the issues, or maybe the reviewer can do it if they have the chance.

### Firefox OS is made up of Gonk, Gecko and Gaia. Each system is large, complex, and intimidating to a newcomer. You regularly submit patches to Gecko and Gaia. Whenever you dive into an existing project, how do you learn about the system?

I’m afraid there is no magic technique. What works for me might not work for others for sure. What I try to do is to read as much documentation as possible inside and outside of the code, if it’s possible. I try to ask the owners of that code when needed, and also if that’s possible, because sometimes they just don’t work in the same code or they are not available. I try to avoid reading the code line by line at first and I always try to understand the big picture before digging into the specifics of the code. I think that along the years, you somehow develop this ability to identify patterns in the code and to identify common architectures that help you understand the software problems that you are facing.

### When you start coding in unfamiliar territory, how do you ensure your changes don’t cause unintended side effects? Is testing a large part of this?

Yeah, basically tests, tests and more tests. You need tests, smoke tests, black box tests, tests in general. Also at first, you depend a lot on what the reviewer said, and you trust the reviewer, or you can ask QA or the reviewer to add tests to the patch.

### Let’s flip this on its head and you are the reviewer and you are reviewing somebody’s code. Again, do you rely on the tests whenever you say “OK, this code adds this functionality. How do we make sure it doesn’t break something over there?”

I usually test the patches that I have review if I think the patch can cause any regression. I also try and run the tests on the “try” server, or ask the developer to trigger a “try” run.

### OK, so tests.. A lot of tests.

Yeah, now that we are starting to have good tests in Firefox OS, we have to make use of them.

### What do you look for when you are doing a review?

In general where I look first is correctness. I mean, the patch should actually fix the issue it was written for. And of course it shouldn’t have collateral effects. It shouldn’t introduce any regressions. And as I said, I try to test the patches myself if I have the time or if the patch is critical enough, to see how it works and to see if it introduces a regression. And also I look that the code is performant and is secure, and also if, I always try to ask for tests if I think they are possible to write for the patch. And I finally look for things like quality of the code in general, and documentation, coding style, contribution, process correctness.

### You reviewed one of my large patches to integrate Firefox Accounts into Firefox OS. You placed much more of an emphasis on consistency than any review I have had. By far.

Well it certainly helps with overall code quality. When I do reviews, I mark these kinds of comments as “nit:” which is quite common in Mozilla, meaning that “I would like to see that changed, but you still get my positive review if you don’t change it, but I would really like to see them changed.”

### Two part question. As a reviewer, how can you ensure that your comments are not taken too personally by the developer? The second part is, as a developer, how can you be sure that you don’t take it too personally?

For the record, I have received quite a few hard revisions myself. I never take them personally. I mean, I always try to take it, the reviews, as a positive learning experience. I know reviewers usually don’t have a lot of time to, in their life, to do reviews. They also have to write code. So, they just quickly write “needs to be fixed” without spending too much time thinking about the nicest ways to say it. Reviewers only say things about negative things in your code, not negative, but things that they consider are not correct. But they don’t usually say that the things that are correct in your code and I know that can be hard at first.

But once you start doing it, you understand why they don’t do that. I mean, you have your work to do. This is actually especially hard for me, being a non-native English speaker, because sometimes I try to express things in the nicest way possible but the lack of words make the review comments sound stronger than it was supposed to be. And, what I try to do is use a lot of smileys if possible. And always, I try to avoid the “r-” flag if I mean, the “r-” is really bad. I just clear it, use use the “feedback +” or whatever.

### You already mentioned that you try to take it as a learning experience whenever you are developer. Do you use review as a potential teaching moment if you are the reviewer?

Yeah, for sure. I mean just the simple fact of reviewing a patch is a teaching experience. You are telling the coder what you think is more correct. Sometimes there is a lack of theory and reasons behind the comments, but we should all do that, we should explain the reasons and try to make the process as good as possible.

### Do you have a snippet of code, from you or anybody else, that you think is particularly elegant that others could learn from?

I am pretty critical with my own code so I can’t really think about a snippet of code of my own that I am particularly proud enough to show :). But if I have to choose a quick example I was quite happy with the result of the last big refactor of the call log database for the [Gaia Dialer app](https://github.com/mozilla-b2g/gaia/blob/master/apps/communications/dialer/js/call_log_db.js) or the recent [Mobile Identity API implementation](https://mxr.mozilla.org/mozilla-central/source/services/mobileid/).

### What open source projects would you like to encourage people to participate in, and where can they go to get involved?

Firefox OS of course! No, seriously, I believe Firefox OS gives to software engineers the chance to get involved in an amazing open source community with tons of technical challenges from low level to front end code. Having the chance to dig into the guts of a web browser and a mobile operative system in such an open environment is quite a privilege. It may seem hard at first to get involved and jump into the process and the code, but there are already some very [nice Firefox OS docs on the MDN](https://developer.mozilla.org/en-US/Firefox_OS) and a lot of nice people willing to help on [IRC](https://wiki.mozilla.org/IRC) (#b2g and #gaia), [the mailing lists](https://lists.mozilla.org/listinfo) (dev-b2g and dev-gaia) or [ask.mozilla.org](https://ask.mozilla.org/questions/).

### How can people keep up to date about what you are working on?

I don’t have a blog, but I have my public [GitHub account](https://github.com/ferjm) and my [Twitter account](https://twitter.com/f_jimenez).

## Transcript

A huge thanks to Fernando for doing this interview.

The [full transcript](https://github.com/shane-tomlinson/devs-at-work-software-quality/blob/master/interviews/fernando-jimenez-moreno.txt) is available on GitHub.

## Next article

In the next article, I interview Brian Warner from the Cloud Services team. Brian is a security expert who shares his thoughts on architecting for security, analyzing threats, “belts and suspenders”, and writing code that can be audited.

As a parting note, I have had a lot of fun doing these interviews and I would like your input on how to make this series useful. I am also looking for Mozillians to interview. If you would like to nominate someone, even yourself, please let me know! Email me at [stomlinson@mozilla.com](mailto:stomlinson@mozilla.com).

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 7 comments

maitreyaJuly 16th, 2014 at 10:11Shane TomlinsonJuly 17th, 2014 at 01:03Ivan DejanovicJuly 17th, 2014 at 07:09Shane TomlinsonJuly 18th, 2014 at 06:32Robert Nyman [Editor]July 21st, 2014 at 02:14André JaenischJuly 21st, 2014 at 13:25Robert Nyman [Editor]July 21st, 2014 at 14:00