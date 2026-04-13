---
title: Why aren’t YOU contributing to open source projects?
url: http://www.learn-cocos2d.com/2013/08/contributing-open-source-projects/
published: '2013-08-22'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

I got a lot of questions in the past why I’m not contributing my work to the cocos2d-iphone project.

One of the obvious reasons being that what I did is simply too radical technically and I don’t want to compromise. Another reason being a fundamental difference in attitude towards developing and managing open and closed source projects.

These questions made me wonder - in particular because there was often a notion associated with these questions: because I do so much with cocos2d-iphone I should somehow be obliged to contribute back to it. Weird, right? I am contributing a lot already, just not code to the repository.

So if I don’t contribute (code), why don’t you? Or generally speaking, why aren’t we all contributing more (code) to open source projects?

I have been using open source software for as long as I can remember doing programming work. Yet I’ve probably contributed no more than a few dozen lines to all projects together. And realizing this it’s easy to see that this is the case for 99.9% of the developers out there.

So why aren’t we contributing more to open source projects? What is stopping us? I’ll give you some probable causes and ideas how to improve it for your own open source project.


### The open dead projects

First off, let’s start by ignoring any open source project that was open-sourced just because someone could and thought it would be cool to do so (it’s not).

I’d say 80% of all the so-called open source software out there is just a bunch of code someone once wrote and then published on the Internet, hardly ever to be updated again, hardly ever to be used by anyone. [Most projects on github don’t even use an open source license](http://www.theregister.co.uk/2013/04/18/github_licensing_study/)!

Those are open dead projects. You’ll quickly identify them because authors typically include a line that reads “perhaps it’s of use to someone”. It never is. Especially without a license. You’re cluttering the Internet with garbage. Stop it!

### Not telling users what you wish them to contribute

The dumbest thing an open source project that seeks contributions could do is not to provide any information as to what kinds of contributions are wanted. And not providing guidance as to what users can do for the project. Write down some ideas for those considering contributions.

It doesn’t have to be all about the code!

Developers can contribute to open source projects in many ways besides code. Reporting bugs and giving feedback is helpful, too. Writing documentation is rather important as well. Or maybe the project could really use a better website, forum and logos?

If you don’t tell your users what you wish them to do, what kind of work will be happily accepted, then the chances that anyone will volunteer to do anything will be slim.

### Telling users exactly how they have to contribute

This is almost as bad, though necessary for some really large and complex projects (think: Linux kernel, Qt, Mono, Python).

If you have your users go through excrutiatingly detailed documents that describe every miniscule aspect of your coding style, the submission guidelines, the review process, etc. etc. with plenty of rules like always providing a test case then you just shushed away most of the users willing enough to contribute by having them read those rules and regulations.

Worse, any new user is guaranteed not to consider contributing because they come across that document, understand it’s way above their league, and even when they have learned a lot over the years they’ll still consider the process to be far above their skill set - or simply too much to bother.

Speaking of which: **requiring a test case** means you should at least have guidelines and templates for creating such test cases. Even then a test case requirement pretty much end most contribution efforts because they seem like a lot of work.

If you say “test case” what most developers hear isn’t “the crappy project I put together to try out my feature” - though that usually suffices. I think many expect a “test case” to be some elaborately set up project that goes through testing every nook and cranny of the feature, ie perhaps more so than unit tests.

Too many, too stringent, too detailed rules and unconditionally requiring test cases/unit tests are a sure way to put off most of your project’s potential contributors. Make it easy to contribute! Because …

### Dammit, source control is HARD!

For the uninitiated, git and github are a sure way to kill off their motivation. Even though there are good git guides everywhere, it’s definitely best if you write your own that explains exactly how to work with YOUR project, with the tools you use and recommend.

For example introduce project contributors to the more beginner-friendly [Github Mac client](https://mac.github.com/) rather than the command line git. And then explain exactly the subtleties of your project’s setup using the exact commands one has to type in to pull exactly your project instead of the general process. And how to incorporate the git version of the project into the user’s custom project.

It helps first-timers to have a positive first experience with git & github! Because git will be a b..ch when it comes to contributing.

A typical contributor will fork the project and use it in its own project either as subtree, submodule or by directly modifying it. Regardless, the usual contributor’s pain cycle goes as follows:

- User fixes a bug or adds a feature to project while working on his own code.
- User wants to contribute just the bugfix/feature back.
- User sends pull request.
- User realizes that the pull request includes ALL OF HIS CHANGES including the various hacks he made in the codebase. Or things are otherwise complicated by first having to fetch and merge upstream changes incompatible with user’s project.
- User thinks “Screw that!” and gives up.

It requires a certain amount of discipline to keep individual commits separate from one’s own project. Depending on the exact setup of the project (merged, subtree, submodule, some other way) the user’s working discipline with source control is probably the most decisive factor whether that user will contribute back or not. Some guidelines on how to cherry-pick commits or individual files to contribute back to can go a long way.

Here’s an idea:

Github allows you to setup an [organization](https://github.com/blog/674-introducing-organizations). You can have multiple teams with different permissions to individual repositories in the organization. Invite your contributors to join the project’s organization, and give them a “community” repository in which they can directly contribute to. Project owners can then take on the effort of cherry-picking individual contributions from the community project.

Allowing users into the organization is a simple matter of getting their github account names (ie by forum or email) and then adding them in manually. Since for most projects we’re talking no more than a couple dozen users per month, adding them manually doesn’t require much of an effort and can probably be automated if you want it hard enough.

What’s more important is that you can recruit the more active and reliable contributors to the “management” team which can work directly in the main repository. If you want to foster collaboration, there’s no better way than to give users more responsibility and the [ability to make a direct, immediate impact on the project](https://en.wikipedia.org/wiki/Homesteading_the_Noosphere).

### Allow sending patch files by email

With git it’s possibly even easier to create patch files than to fork and send pull requests. Especially compared with a good guide on how to create patch files.

Any open source project that asks for code contributions should provide more than one way of contributing code. Fork and pull requests will always work. Organizations with collaborators as the direct approach. Patch files via email are ideal for small changes without having to sign in to github and avoiding the other, more formal processes.

It’s more work for the maintainer(s) but certainly worth it! Those who contribute perhaps too much too often by email can be mentored to use github instead, rather than disallowing the process altogether.

### Government Model

I think it’s important to make sure everyone understands [how the project is governed](http://www.oss-watch.ac.uk/resources/governanceModels). Here’s a [relatively straightforward example](https://github.com/yui/yui3/wiki/Contributor-Model).

Especially where the actual government model deviates from the perceived one. For example, there are projects with the benelovent dictatorship model where the dictactor isn’t perceived as benevolent. There are community-driven projects that have forked into several variants because some individuals can not compromise and the community itself is heavily divided on even simple matters.

Who decides what? What decisions can individual contributors make on their own? Define at least roughly where the gray areas are so individuals know where to take the initiative and where to ask for collaboration or permission. In general this applies to the entire community moderation (code, documentation, forum, etc): what is allowed and what isn’t?

Not providing such “laws” means that a) you’ll get more conflicts with developers because certain ground rules have not been established, especially where there are conflicting interests. And b) there’s a potentially damaging aspect if such rules are made up as needed - usually a good idea - but then the new rule is applied [ex post facto](https://en.wikipedia.org/wiki/Ex_post_facto_law).

Don’t blame or punish users who have stepped over an as-of-yet imaginary, unwritten boundary.

### Accept or reject swiftly and indiscriminately

If contributions aren’t accepted or rejected quickly, say within 1-2 weeks at most, most contributors lose interest to ever do it again. It is frustrating and demotivating to see your contribution being included in the release following 6 to 12 months after you sent the pull request.

It is even more so frustrating if it takes that long to reject a contribution.

Most commonly this is because the project isn’t very active and there’s only one or two maintainers who tend to be busy with other work. The negative side effect is that contributors may regard the maintainers as arrogant, as simply not interested in community contributions. If at the same time some other contributors are treated with greater priority you risk alienating all other actual and potential contributors.

If a project doesn’t have a government model and it’s unclear who has which responsibilities, you are more likely to be(come) a clique with fanboys than a team of collaborators with an engaged community.

### Foster the community

If you want more contributions to your project, teach and mentor contributors. So many open source projects don’t do any of that. They just say “any contributions are welcome!” and consider their job done.

### Remove code fragments from the forum

This is one of my pet peeves. Some user posts a relatively useful class in the forum. Other users chime in to say thanks. All is good.

Then someone fixes a bug, reposts the changed code fragment. Someone else adds a new feature, posts the changed code fragments. A third user posts his reworked version of the class on page 4 of the thread to make it work with the current version of the project. Again users chime in to fix more bugs and add more features, but no one reposts the class in its entirety. Worse, some code changes are in conflict with each other.

When you find that thread via google the class seems to be **exactly** what you need, but you’ll quickly bash your head against the keyboard!

The code is hopelessly outdated and doesn’t work with the current version of the project. Worse, you don’t even know which version the code once worked with. Plus several important bugfixes and features are fragmented over various posts and you have to manually re-integrate them.

This is frustrating for users. But what can be done about it?

For one, you should have a forum dedicated to discussing addon code. If the code does end up in the repository - and that should almost always be the goal - the code should be removed from the forum thread and a link to the repository added in its place.

If you get a lot of code posts that don’t end up in the repository, your community takes no responsibility to take care of that. Mainly because it’s so much easier to post code on the forum than it is to work on it collaboratively via source control. If no one checks in that code even in a fork of the project to allow others to work on it on their own accord, you may have a mentoring problem.

Don’t just tell users to put the code in source control, show them how they can do it!

You may even have to consider radical approaches here, for example disallowing code fragments on your forum that are more than 50 consecutive lines of code with a notice that larger code fragments should be added to and edited in the repository.

### Related Articles

Brandon’s post [Why I still don’t contribute to Open Source](http://brandonhays.com/blog/2011/05/03/why-i-still-dont-contribute-to-open-source/) sums up some key points.

This talk provides key insights on [how to make an open source project’s community a central player](http://smarterware.org/7819/my-codeconf-talk-your-community-is-your-best-feature) in all processes.

Here’s an excellent article that explain [why the so-called “freeloaders” are desirable](http://opensource.com/business/13/6/foss-freeloaders). This includes businesses making money off of your free and open source (FOSS) project without contributing and users of FOSS projects who don’t purchase the businesses’ commercial versions or services, and definitely not all the other regular, non-commercial, non-contributing, freeloading users.

[Producing Open Source Software](http://producingoss.com/) is a free eBook about the human side of open source development. It describes how successful projects operate, the expectations of users and developers, and the culture of free software. Recommended read for all FOSS project maintainers/owners.

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |