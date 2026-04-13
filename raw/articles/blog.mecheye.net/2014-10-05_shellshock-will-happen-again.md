---
title: Shellshock will happen again
url: https://blog.mecheye.net/2014/10/shellshock-will-happen-again/
author: Jasper St Pierre
published: '2014-10-05'
source_blog: Clean Rinse
source_site: https://blog.mecheye.net
category: graphics
fetched: '2026-04-13'
---

As usual, I’m a month late, the [big Bash bug known as Shellshock](http://en.wikipedia.org/wiki/Shellshock_%28software_bug%29) has come and gone, and the world was confused as to why this ever happened in the first place. It’s been fixed for a few weeks now. The questions have started: Why has nobody spotted this earlier? Can we can prevent it? Are the maintainers overworked and underfunded? Should we donate to the FSF? Should we switch to another shell by default? Can we ever trust bash again?

During the whole thing, there’s a big piece of evidence that I didn’t see anybody point out. And I think it helps answer all of these questions. So here it is.

I present to you the upstream git log for bash: [http://git.savannah.gnu.org/cgit/bash.git/log/](http://git.savannah.gnu.org/cgit/bash.git/log/)

Every programmer who has just clicked that link is now filled with disgust and disappointment.

It’s all crystal clear now: Nobody would have spotted this earlier. No, we can’t really prevent it. No, the maintainers aren’t overworked and underfunded. No, we shouldn’t donate to the FSF. Perhaps we should switch to another shell. No, we cannot trust bash. Not until a serious change in its management comes along.

For those of you who aren’t programmers, you might be staring at that page, not quite understanding what it all means. And that’s OK. Let me help explain it to you.

There’s a saying in the open-source development community: “With enough eyeballs, all bugs are shallow”. I don’t believe in it as strongly as I used to, but I think there’s some truth to it. It can be found in other disciplines as well: in science, it’s known as “peer-review”, where all papers and discoveries should be rigorously double-checked by peers to make sure you didn’t make any mistakes. In other sorts of writing, the person reviewing it is the editor. Basically, “have somebody else double-check your work”.

The issue with this, though, is that you need enough eyeballs to double-check your work. And while it was assumed before that all open-source software had enough eyeballs, that doesn’t seem to be the case. That said, you can certainly design and maintain a software project in certain ways to attract enough eyeballs. And unfortunately, bash isn’t doing these things.

First of all, you can see that there’s zero eyeballs on the code: one person, Chet Ramey, is writing the code, and nobody double-checks it. Because there’s only one developer, we might assume that there’s no big motivation to do code cleanups or try to make it accessible to anybody other than Chet, since nobody is working on it. And that’s true. This makes the eyeballs wander elsewhere.

But, in fact, that isn’t even true: Florian Weimer of the Red Hat Security Team has developed multiple fixes for the Shellshock bug, but his work was included in bash uncredited. Developers really need to be credited for their work. This makes the eyeballs wander elsewhere.

The code isn’t really that actively developed. Down the bottom of that page, we see dates and times that are from 2012. It seems like nobody actually cares about this code anymore, and nobody is really trying to fix bugs and make it modern. This makes the eyeballs wander elsewhere.

There are no detailed descriptions of what changed between versions, and Which commits in that log are ones that are serious and fixed CVEs, and which might just fix minor documentation bugs? It’s impossible to tell. This makes the eyeballs wander elsewhere.

And even with the corresponding code change, it can be difficult to tell whether a specific commit is an important security fix, a new feature, or a minor bug fix. There’s no explanation in the commit message for *why* this change was mode. or any sort of changelog, which makes it hard for people redistributing and patching bash to know what fixes are important, and which aren’t. The eyeballs will wander elsewhere.

In comparison, look at the commit log for [the Linux kernel](http://git.kernel.org/cgit/linux/kernel/git/torvalds/linux.git/log/). There’s a large number of different people contributing, and all of them explain what changes they make and why they’re making them. To use a recent example (at the time of this writing), [this NFS change](http://git.kernel.org/cgit/linux/kernel/git/torvalds/linux.git/commit/?id=f87d928f6d98644d39809a013a22f981d39017cf) describes in perfect detail why the change was made (for compatibility with Solaris hosts), and includes a link to a bug report with further information from debugging. As a result, even though bash is more commonly used and included in more things than the Linux kernel itself, the Linux kernel has more eyeballs *and* more developers.

So, what should we do? How should we fix this situation? I don’t really know. Moving to a new shell isn’t really a solution, and neither is a fork of bash. The best case scenario would be for bash to indeed change its development practices to be more like the Linux kernel, and adopt a thriving community of its own. I don’t have enough power or motivation to enact such a change. I can only hope that I can convince enough people of the right way to maintain a project.

Perhaps, Chet, if you’re out there, do you want to talk about it? This is a discussion we really should be having about the future of your project, and your responsibilities.

Bash development isn’t even under source control. That git repository is just someone manually checking in the patches that are issued on the GNU ftp site: http://ftp.gnu.org/gnu/bash/bash-4.3-patches/

Yes, that’s how bash development happens. Someone uploads patch files to a ftp server. The whole git thing is just an afterthought.

Well, that at least has something like commit messages and some author attribution. Thanks for pointing it out. I wasn’t able to find it in my research.

Diego Elio Pettenò posted similar observations at https://blog.flameeyes.eu/2014/09/project-health-and-why-it-s-important-part-of-the-shellshock-afterwords and also concluded bash is not a healthy project and needs to adapt to move forward.

As for the “enough eyeballs” canard, issues like this, heartbleed, patches I’ve pushed for 20+ year old X11 security bugs, and more prove that it’s constantly beaten by the tragedy of the commons – everyone assumes someone else will go review the code and few bits of open source actually achieve the necessary critical mass of eyeballs who know what to look for to find issues like this.

Well aside from Bash’s development process, one thing that Shellshock made abundantly clear is that some people are deploying things in horrible ways.

Why are there CGI scripts subshelling out to Bash?! Why are people using setups where /bin/sh is mapped to Bash (instead of Dash et al)? Why aren’t CGI implementations sanitising environment variables? Come to mention it, why is CGI still a thing when we have FastCGI, WSGI, etc..?

Bash certainly needs to pull its socks up but given there likely will be ingress through part of this stack at some point, we really need to inspect how the rest of it fits together. We can mitigate for the next shellshock.

It’s the UNIX philosophy.

I think the UNIX philosophy you are referring to is that “everything is a file”, which does work well for a unix computing system, and again, works well for the www.

However, if we follow this UNIX philosophy from the operating system and apply it to www, i.e. if a URL path “is a file”, then an HTTP service “is a filesystem”. Any filesystem which accepts random input in it’s fopen/fread/fwrite semantics and then delegates treatment of this uncensored input to some third party interpretor is really, really sadly insecure.

No. The UNIX philosophy I was referring to was “do one thing and do it well”. As in, “the shell is the core of the system that plugs different utilities and tools together”.

“Why are there CGI scripts subshelling out to Bash?! Why are people using setups where /bin/sh is mapped to Bash (instead of Dash et al)? Why aren’t CGI implementations sanitising environment variables? Come to mention it, why is CGI still a thing when we have FastCGI, WSGI, etc..?”

Because most people who use Linux are ABM-ers (anything but Microsoft) who pose as security conscious, but don’t really know about security. There are automatic tools to sanitize and harden your server and very few people even use that.

I wonder if even 20% of Linux sysadmins even heard of grsecurity.

I still don’t buy it, this is not a bug in bash, never was.

Running a privileged process that accepts requests over the wire, allowing any input whatsoever (presumably setting env vars directly from HTTP header fields) and just delegating this to any third party interpretor (i.e. bash is third party where your software is an HTTP server)… is just extremely, ridiculously, naive and dangerous.

This is just as true of any other interpretor (python, perl, php, etc…) as it is true of bash, if you are not in complete control over what is happening with HTTP requests in your daemon then you have no right to complain about any security issues which occur. The only way that this could conceivably be secure is if a said third party interpretor promised that they would never, ever extend their formalism, i.e. a permanent feature freeze would conceivably allow that.

This whole story of there being a bug in bash is just some noise coming from som Apache/CGI developers who are but hurt that the way they have been doing things for 10 years is just completely and utterly insecure and wrong. They are just trying to pass the buck on this one and blame the third party interpreter they have been naively offloading work to, work that they should have been doing themselves all along.

There is an argument that we will solve more widespread issues in one fell swoop if we modify the behavior of bash to cater to the needs of ignorant web developers, it’s a valid and reasonable approach, but just a bandaid. This kind of thing will keep happening so long as naive/lazy developers place their faith in this messed up CGI contract.

Anyway, my 2 cents, rather long, cause well, it really irks me ;-)

Executing a shell string simply because an environment variable is set is very much so a bug. And it’s a bash one, too. No other shell does this.

I’m not a strong believer in plumbing together large systems with the shell, but I understand the value and utility in it. The shell is quite core to the system, and when that can’t be trusted, there’s not much left.

Don’t point fingers at only the developers of the core or the developers of the large systems. Both are at fault. But we should be curteous and kind to both, and help them fix their systems. Pointing blame just makes the user unsafe, and keeping the user safe should be the first priority.

Yes Jasper I can definitely agree with this.

I think the media coverage of this has been doing a lot of blame shifting towards bash when I think people are using it in a way that is inherently insecure.

Honestly, I’m not sure that executing a statement as a part of a variable assignment is unintentional / a bug, there are plausible use cases for such semantics.

For instance, classic valid C statement which does this:

varname = (free (varname), NULL);

It could be that the feature of executing a statement in a variable assignment in bash is unintended / a bug and perhaps has no usefulness like the above C statement does, I don’t have the history of that on hand.

But yes, I am sort of lashing out at all the bash hating of late, and as I said, modifying bash to cater to the greater needs will fix more problems in one place, but I think the media coverage of saying this is a security flaw in bash is off the mark of this point of view.

The specific bug was that environment variable values that started with the four characters “() {” are parsed as a function. This is how the bash-specific “export -f” functionality is implemented, which allows you to export functions to subshells.

The intention was to see functions like “() { echo foo }” as environment variables. The intention was never to see “() { echo foo }; /bin/do_insecure_thing”. The fact that /bin/do_insecure_thing was actually ran was the bug. It ran before bash was properly boostrapped, causing bash to segfault after it had run the command. It is certainly a bug, not a feature.

The command isn’t ran on variable assignment. You can do foo=”() { echo foo }; /bin/do_insecure_thing” and nothing bad will happen. It’s only when the environment is then parsed at bash startup that the bug occurs.

Since environment variables are inherited from their parent processes, quite intentionally in UNIX, this means that simply starting bash in an unsafe environment.

Since CGI relies on environment variables to be set by incoming user data, and programs do intend for these environment variables to be passed to spawned bash shells underneath (several open-source statistics packages spawned shell scripts which read HTTP_USER_AGENT), it is not a bug that they did not strip the environment from their subshells.

Interesting and enlightening discourse, since I’ve been wondering these things these last weeks as well.

I’ll buy that executing statements in an environment variable assignment was unintentional, but I still think the point still stands that a semantic such as:

env x='() { :;}; /bin/do_useful_thing’

could in some context actually be useful, and that relying on bash (or any interpretor) not implement something similar in the future, at the moment of developing the CGI contract, was folly.

Anyway, pointing the finger at one group or another doesn’t help, it is at least amusing that apache passes unscreened data down to some scripts, and then bash receives all of the blame.

Given that bash segfaults after running the program since it wasn’t bootstrapped properly, I’m going to assume it was unintentional.

Folk wisdom: free cheese is only found in mousetraps. Use proprietary software from reputable companies eg. Microsoft.

Bugs like this will appear once again, maybe GNOME Shell is the next one. To me the question is, how we can improve the environment to cope with such bugs. Basically a concept to address bugs of this grade. Maybe there are conceptual solutions which can be used to compensate such a bug .. SELinux goes into that direction. But maybe there are conceptual different solutions which can be used to address/mitigate such bugs.

From a humble user point of view, I wonder if there isn’t a little bit of responsability towards the “major” distributions (ie: Debian, Fedora, OpenSuse, Ubuntu, etc) in this ShellShock issue. Shouldn’t at least the Bash package maintainer(s) of any of those distros have raised a concern about the status of the upstream Bash development team?. I mean, something like saying “Hey!, the upstream Bash development situation isn’t healthy right now. There is only one active developer doing the whole stuff. Lots of things need to get done and/or reviewed!. Let’s see how we can help there.”. IMHO, given the important level of adoption and relevance that Bash has among several distros out there, this shouldn’t be something crazy to expect to happen!.

On the other hand, I perfectly understand that comunication between upstreams and downstreams aren’t always easy.

Just to clarify, I am perfectly aware that I’m in no position to blame anyone in particular, nor it’s my intention to do that. I’m just giving my 0.0005cents!.

Cheers!.

> I wonder if there isn’t a little bit of responsability

> towards the “major” distributions (ie: Debian, Fedora,

> OpenSuse, Ubuntu, etc) in this ShellShock issue.

> Shouldn’t at least the Bash package maintainer(s) of

> any of those distros have raised a concern about the

> status of the upstream Bash development team?

You bet.

As someone working on gnome-terminal, the Bash maintainer of one of those distributions basically told me to fuck off. One of the things that I had hoped to discuss with him was their interesting use of Git.

That was more than six months ago. Long before Shellshock, when most people were unaware of the state of their version control. ;-)

I like this one: http://git.savannah.gnu.org/cgit/bash.git/commit/?id=b7ec1810367e42788ded6c2fb99db698bd26ccf1

Might as well have said “well don’t ever change this bit of code, you’ll break something and I’m not going to tell you what.”

Well, this bug was discovered not by coincidence but by reviewing the source code. So there are at least a few eyeballs performing these kinds of security audits.

Advocating closed source software is idiotic. Also, you have, generally speaking, and I cannot stress this enough, far, waaaay far worse code quality in closed source software, and god knows how many black holes and security problems hidden in them. If bash were closed source software, we’d still be vulnerable and the public would stil not know by now.

Bash is fixable, but most closed source software is not. This is not the first time this happens, but it’s also not the first time it gets fixed. You bet this seldom happens with closed source software.

> Moving to a new shell isn’t really a solution […]

Why not? Lots of users out there use zsh as an interactive console, and symlink sh to dash. What’s wrong with that?

Both have a pretty big userbase, are optimized for their own thing, and don’t have lots of these issues that bash has.

dash is also fairly unmaintained as well, and doesn’t support lots of things that modern users expect from shells. As a quick example, dash doesn’t understand “source foo”, only “. foo”. “source” is a bash feature.