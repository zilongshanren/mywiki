---
title: Open Source Maintenance
url: https://anteru.net/blog/2024/open-source-maintenance
published: '2024-04-02'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

This has been a topic I wanted to cover for a long time now, but with the recent stories about [ log4j](https://www.cve.org/CVERecord?id=CVE-2021-44228) and the

[vulnerability, I figured it’s high time to get this finally out of the door. Open source software the way we know simply doesn’t work any more, and we’ve probably crossed the point where it can be fixed without a lot of pain for everyone involved.](https://www.cve.org/CVERecord?id=CVE-2024-3094)

`xz`

⚠ Warning: I’ll be obviously generalizing here. There’s always that one unicorn library somewhere which is well funded, has no security issues, no dependencies, and what not. Please don’t get hung up because there’s one counter example.

### Maintainer fatigue

As an open source project maintainer myself, I do want to talk about “maintainer fatigue”. Many open source projects out there are hobby projects which make no money (more on this later though.) This means they’re a “labor of love”, but most of the time, they’re scratching some particular itch of the maintainer. That also means that open source maintenance comes without guarantees or commitments – I can always step away for a while, a long time, or forever, and it’s my problem first and foremost. If it becomes your problem that some open source library becomes dormant, that usually implies you’ve been building a business on top of someone’s free labor (even if they’re paid for writing it, you got it for free in the end by virtue of being open source), and this “no cost” mentality is now causing you trouble.

Everyone needs to be aware that an open source maintainer is probably a person who has a day job (which means money is probably not the main motivation anyways!), has a life outside of work as well (and that life consists of more things than maintaining their open source library), and that a lot of time in an open source project already sinks into just dealing with feedback and making a release to start with. I’ve seen it many times where someone feels entitled that their favorite PR or issue should get addressed by the maintainers, who are already struggling to even keep the number of PRs not growing exponentially, and are still expected to make regular releases on top of everything. Burning out maintainers is a sure way to make things worse very quickly for everyone involved, and I see very few open source projects run by volunteers who aren’t struggling with this. Even those with commercial backing usually have their share of “grumpy customers” who don’t pay and yet demand, and still struggle to handle external contributions.

There’s also something about open source software which I’d call “doing it right”. Given it’s a hobby project for most developers, and also something they care about, that care usually translates into not taking shortcuts and adhering to higher quality standards than you’d have let’s say in a company where there’s pressure to hit some deadline. This results in some “guilt driven development”: As an open source maintainer, you really want to do things properly, which means most PRs won’t meet the bar to start with (especially from people with said deadlines), and you get into a self-reinforcing cycle.

What makes this a real problem is that there’s really no simple way out. You can try to pay maintainers (if they have set up means for that), but that doesn’t necessarily translate into more time devoted to the project. You can fork the project which most of the time results in a disaster if you take it public. You can try to contribute to the project in helpful ways to reduce/offload the maintainers, but that may only get you so far. Finally, you can also try to become actively involved, but realistically that’s probably not what you want (especially if you only care about this one feature) and it brings us to the next problem, which is: Trust.

### Maintainer trust

There’s no guarantee to start with that your friendly maintainer is even the person you think they are. Some random contributor may be a malicious actor, only waiting to have enough power to use the project for bad. This will become worse over time as maintainers simply retire or die, and we’ll have to figure out how to hand over maintenance from a well-known public figure to someone who may not have built up any reputation or trust with the community. There’s no help for maintainers to make this transition, and the security implications are mind-blowing and worrying. Just think about it: At any given time, the “load bearing” libraries with 1-2 maintainers may have one maintainer hit by a bus and then some enthusiastic person in the community shows up to take over or forks it and puts some work to make the fork look attractive. How quickly would you switch to a new `zlib`

if you heard the original one got abandoned and `super-zlib-turbo2`

is merging all new features and making rapid progress? Would you audit this new library if you see a reputable project use it? Would you *pay* for an audit?

The reality is that the software ecosystem is a house of cards held together by duct tape and hope, and the fact that it hasn’t completely imploded yet is because there’s still just enough people paying attention. But we can clearly see that hope is not enough, and with software becoming increasingly more complex, the number of attack vectors is increasing. Every dependency we introduce into our software is a potential security issue, and every maintainer we don’t know is another random person we hand the key to our system. You wouldn’t plug in a random USB thumb drive you’d find in the streets, but we’re more than happy to pull in 10.000 different pieces of code and execute them during a build. Trust is hard to build in the real world, and historically we’ve trusted our fellow software developers to do the right thing. It’s clear by now that we need to change the default assumption from “trust everyone” to “trust no-one” if we don’t want history to repeat itself.

### AI will save us

I’m a bit puzzled that nobody has brought up the “AI will save us” card yet. You could imagine that someone could train an AI to audit code for “suspicious changes” and help maintain it in the same way as the original maintainer (“what would Linus do?”) It’s an interesting avenue to explore, but ultimately, it doesn’t solve the underlying problems of maintainer fatigue, and from a security perspective this may be even worse (“the AI thinks this blob of data is safe”.) Not to mention that training an AI on security backdoors may backfire in the sense we’ll get AI assisted backdoor injection, which will only end up in an arms race where understaffed projects will have no chance to survive under a barrage of AI generated, hard-to-spot backdoors. I’m mostly adding it for the sake of completeness here, not because I see it as a general solution.

### Closed source is better

Just to get this out as well: There’s no reason to assume that closed source helps here; there’s little closed source code in existence these days which doesn’t heavily rely on open source to start with; and we simply don’t see what’s going on in a closed source codebase. Given the widespread fallout we see from open source library security issues, and how most closed source handles dependencies (and updates), it’s fair to assume that “closed source” doesn’t actually solve any of the problems.

### And now what?

That’s the question I’ve been asking myself for a while. What do we do about all of this? For me for example, more money wouldn’t actually make me more motivated to spend time on my open source projects, and it’s hard to imagine that I could actually make a living off my open source projects. Doesn’t look like a promising avenue to me. Mandatory payment however to fund audits of open source software could be interesting, together with “tagged and certified” releases. Something which allows you to get at least one working version of every dependency which has been at least audited to some extent. That’s only a partial solution though as dependency management these days is so complex, that there’s no way to fully solve this until you can basically audit close to every version of every dependency.

What else could we do? Mandatory identity management for contributors, at least that way you could figure out if a person is real, but that poses a lot of problems if your project gets considered problematic (think: `DeCSS`

), and it’s unclear how well this would work if state actors are involved anyways: What’s the point if having a verified identity if the government issuing it is involved? What could be done though is at least mandate all verified commits, 2FA, the little things that give at least some confidence that an account hasn’t been compromised.

This is really a complex problem, and the solution to this will be equally complex. Just helping maintainers for example is not going to resolve ownership issues, security problems, and certainly doesn’t fix the fact that a lot of “the industry” relies on essentially free labor. Similarly, introducing more process will not help when your maintainer is already burned out and struggling to even make one release happen. I wish I had some answers to the problems, but for now, I think the most important steps everyone can take is to review their own situation. If you’re a maintainer or consumer of an open source project, start asking yourself “what if?” and try to come up with ideas. Eventually I’m sure we’ll figure something out that works better than what we have now, because I hope it’s clear by now that the “status quo” will eventually lead to a “system wide” disaster (i.e. vulnerabilities affecting the majority of all users.)