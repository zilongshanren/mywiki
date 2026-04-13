---
title: Why Package Managers are not my Ideal Software Distribution Mechanism
url: https://blog.mecheye.net/2014/11/why-package-managers-are-not-my-ideal-software-distribution-mechanism/
author: Jasper St Pierre
published: '2014-11-30'
source_blog: Clean Rinse
source_site: https://blog.mecheye.net
category: graphics
fetched: '2026-04-13'
---

Those who have spoken to me know that I’m not a big fan of packages for shipping software. Once upon a time, I was wowed that I could simply `emerge blender`

and have a full 3D modelling suite running in a few minutes, without the fuss of wizards or unchecking boxes seeing the README. But today, iOS and Android have redefined the app installation experience, and packages seem like a step backwards.

I’m not alone in this. If you’ve seen recent conversations about the systemd team’s proposal for [ shipping Linux software differently](http://0pointer.net/blog/revisiting-how-we-put-together-linux-systems.html), they’re effects of the same lunchtime conversations and gripes on IRC.

My goal here is to explain the problems we’ve seen, map out some goals for a new solution to supercede packages, and open up an avenue for discussion about this.

## As a user

Dealing with packages as a normal user can be really frustrating. Just last week I had the frustrating experience of trying to upgrade my system when Debian decided to stop in the middle, ask me a question about which sshd configuration file I wanted to keep out of the two. I left it like that and went to lunch, and when I got back I accidentally hit the power strip with my feet. After much cursing, I eventually had to reinstall the OS from scratch.

It should **never** be possible to completely hose your OS by turning it off during normal operation, and I should be able to upgrade my OS without having the computer [ask me incomprehensible questions I don’t understand](http://blogs.msdn.com/b/oldnewthing/archive/2004/04/26/120193.aspx).

And on my Fedora laptop, I can’t upgrade my system because Blender used an older libjpeg than my system. It gave me some error about packages conflicting and then aborted. And today, as I’m writing this, I’m on an old, insecure Fedora installation because upgrading it takes too much manual effort.

Today’s package managers do not see the OS independently from the applications that make it up: all packages are just combined to create one giant filesystem tree. This scheme works great when you have a bunch of open-source apps you can rebuild at every ABI break, but it’s not great when trying to build a world-class OS.

It’s also partially because package installations aren’t reproducible. Installing package A and then package B does not guarantee the same filesystem tree as installing package B, then A.

Packages are effectively composed of three parts: metadata about the package (its name, version, dependencies, and plenty of other information), a bunch of files to place in the filesystem tree (known as the “payload”), and a set of scripts to run when installing, uninstalling and upgrading the package (known as the “triggers”). It’s because of these scripts that packages are dangerous.

It would be great if developers could ship their apps directly to users. But, unfortunately, packaging gets in the way. The typical way to do things is to package up the source code, and then let community members who are interested make their own package for their favorite “distribution”. Each distribution usually has its own package format, build system, different payloads and triggers, leading to a frustrating fragmentation problem for both users and developers.

The developers of Chromium, for instance, doesn’t allow any bugs to be reported for any builds but their official version, since they can’t be sure what patches the community has made. And in some ases, [the community has patched a lot](http://spot.livejournal.com/312320.html). (Side note: I find it personally disappointing that a great app, Chromium, isn’t shipped in Fedora because of disagreements in how their app is developed. Fedora should stand for freedom and choice for the user to use whatever apps they want, and not try to force their engineering practices on the world.)

## As a developer

That said, packages are amazing when doing development. Want to read PNGs? `apt-get install libpng-devel`

. Want a database? Instead of hunting around for SQLite binaries, just `yum install 'pkg-config(sqlite3)'`

.

Paired with pkg-config, I think the usability and ease of use have made it quite possibly the most attractive development environment out there today. In fact, other projects like node’s [npm](https://www.npmjs.org/), Ruby’s [gems](http://rubygems.org/), and Python’s [pip](https://pip.pypa.io/en/latest/) have stolen the idea of packages and made it their own. Even Microsoft has endorsed [NuGet](https://www.nuget.org/) as the easiest way of developing great apps on top of

their .NET platform.

Development packages solve a lot of the typical problems. These libraries are directly uploaded by developers, and typically are installed per-project, not globally across the entire system, meaning I can have one app built against an older SQLite, and another building something more modern. Upgrading these packages don’t run arbitrary scripts as root, they just unpack new files in a certain location.

I’ve also doing a lot of recent development on my ThinkPad and my home computer, both being equipped with SSDs without a lot of disk space. While I happily welcome [HP’s memristors](http://arstechnica.com/information-technology/2014/06/hp-plans-to-launch-memristor-silicon-photonic-computer-within-the-decade/) to hit shelves and provide data storage in sizes and speeds better than today’s SSDs, I think it’s worth thinking about how to provide a great experience for those not as fortunate to waste another gig on duplicated libraries.

## Working towards a solution

With all of this in mind, we can start working on a solution that solves all these problems and meets these goals. As such, you might have seen different things trickle out of the community here. The amazing [Colin Walters](http://blog.verbum.org/) was the first to actually do [my former employer](http://www.redhat.com/)anything when he built [OSTree](https://wiki.gnome.org/action/show/Projects/OSTree), which allows *fully atomic* system upgrades. You can never get your system into a hosed state with it.

At [Endless Mobile](https://endlessm.com/), we want to ship a great OS that upgrades automatically, without ever breaking if the power gets cut or if the user unplugs it from the wall. We’ve been using OSTree successfully in production, and we’ve never seen a failed upgrade in the wild. It would be great to see the same applied to applications.

As mentioned, we’ve also seen some work starting on the app experienced. [Lennart Poettering](http://0pointer.net/blog/) started working on [Sandboxed Applications for GNOME](http://www.superlectures.com/guadec2013/sandboxed-applications-for-gnome) back in 2013, and work has steadily been progressing, both on [building KDBus for sandboxed IPC](https://lkml.org/lkml/2014/11/21/3), and [a more concrete proposal](http://0pointer.net/blog/revisiting-how-we-put-together-linux-systems.html) for how this experience will look and fit together.

Reading closely, you might pick up that I, personally, am not entirely happy with this approach, since there’s no development packages, and a number of other minor technical criticisms, but I haven’t really talked about to Lennart or the rest of the team building that yet.

## Disclaimer

I also know that this is controversial. Wars have been fought over package management systems and distributions, and it’s very offputting for someone who just wants to develop software for our platform and our OS.

Package managers aren’t magic, they’re a set of well-understood technical tools, with tradeoffs and limitations like every other system out there. I hope we can move past our differences, recognize issues in existing technology, and build something great together.

As always, these opinions are my own. I do not speak for anybody mentioned in this article, anybody else in the GNOME community, the opinion of GNOME in general, and I certainly don’t speak for either [my current employer](https://endlessm.com/) or [my former employer](http://redhat.com/).

Please feel free to express opinions in the comments, for or against, however strong, as I’m honestly trying to open an avenue of discussion. However, I will not tolerate comments that make personal attacks on anybody. My blog is not the place for that.

I think it makes sense to see packages and package managers as first-party distribution methods: they’re primarily designed for distributions to distribute the parts of the OS they distribute. I think it’s reasonable to say that the distribution-maintained package managers are not the ideal way for third parties to distribute software. Ironically it’s at its worst when third parties try to do sort-of the ‘right thing’ and build their packages dynamically, because they have a *terrible* track record of being prompt with rebuilds; that sounds like the situation you have with Blender. Even though in many ways it’s the ‘wrong thing’, third party packages that are very statically compiled usually produce fewer immediately visible problems.

I’ve been saying for a while that it’d be nice for a more third-party, “app focused” distribution layer to be written in a fairly distribution-independent way, for third-party app distribution cases, but I’m not really that interested in writing it because my favoured solution is usually ‘just don’t use third-party distributed software’ ;) but for people who want that, it seems like the sensible way to go. The thing that worries me a bit is that if no-one writes a nice open source, community-focused one, Steam will wind up becoming the de facto standard distro-independent third party software distribution mechanism, like it is on Windows to some extent.

I must say, that I’m seeing “apps” as a huge step backwards compared to Linux package management. Installing apps directly from developers does not sound so great. I’m a Debian developer myself and how often do we need to clean things up and fix license issues, before we can upload something to Debian? If a user does not care about licenses, this might not be an issue, but I do care.

Also, I like that Debian, Ubuntu, Redhat etc. have central bug tracking. As a user I don’t like to deal with many different bug trackers.

What I do not like in the package manager world is the idea of maintainer scripts (pre/post-inst/rm). It would be much better to have a declarative syntax, that can be parsed and checked before execution and even allows the administrator to allow or not every single rule. E.g. “add system user ‘postgres'” or “update font cache” or “add alternative for editor ‘vi'”. Shell scripts are so 1970s – and dangerous. They give a lot of flexibility to the package maintainer, but the user/admin has to take all or nothing.

I think the issue here is a social one not a technical one,

There are several ways desktop/user apps could be distributed across distros but they all have one thing in common, they would weaken the distro package management.

So distro’s will never solve this issue but we need the distros to implement the infrastructure to make this work, good luck getting debian,ubuntu,redhat and others to agree on that

Really distro packaging should be reduced to server packages and core libs. At the very least this would allow distros to concentrate on keeping server packages upto date and better security.

I’d say this is one of the reasons the linux desktop will never go main stream (at least without a big corp *fixing* the user issues ala android)… well this and the fact my desktop still flashes text and blinks like its the 90’s (its 2014 people) when booting

It’s both a social and technical problem. There are very real technical limitations to packages, and then there’s also the social problems of fragmentation. When building a new system, attempt to meet goals to solve both of those.

Look at the mess that you have with .jar files and maven. Nothing ever gets cleaned up, and you have next to no way to ensure everything is up to date and all security issues are resolved. Because it’s not at all meant to be upgraded. Yet, .jar management is “atomic” so to speak. Maven will keep all the old versions around, and never replace any .jar file…

The same thing will happen with the proposed sandbox approach.

It may be attractive to a developer wishing to deploy his latest version to the users: make a sandbox, have them download it, and run it 1:1 as it was built.

At first, it may also appear as nice for the user: keep the old sandbox around, get the new one, and if it works, drop the old one. Live happily thereafter.

But sooner or later, you will be stuck and trapped inbetween. For example, there is a bug in your favorite sandbox, but there is no upgrade available at all. This particular branch has been abandoned. It’s like going with all those 100 distributions out there that believe they can do it better than the big ones. It works for some time, but it doesn’t scale over time.

In the end, the snapshot-deployment approach is not half as nice as it appears to be. You’ll have plenty of users reluctant to upgrade, running really old versions, and buggering you about bug in there, asking for a new snapshot with nothing else changed except their favorite bug.

Maybe the better way is to use e.g. btrfs to upgrade on a “branch” of your filesystem, then switch (atomically) to this branch, test it, and either go back or keep it permanently. But for the actual continuous management of the upgrades, the package managers have been doing an excellent job IMHO.

One very important point that you fail to address is the security updates. The distribution packages allow for very efficient security updates.

In your example, by using a blender binary that depends on an old version of the jpeg library, your application is vulnerable to all the attacks already patched in newer versions.

But by using distribution packages, you know that the application depends on the system library, maintained by the distribution.

Citing as example the android or iOS applications ignores all those problems, as security is ignored in those platforms, is the responsibility of the application developers. Also, the level of integration between different applications is very low, making the distribution problem a lot simpler.

On another point, you said that “…partially because package installations aren’t reproducible. Installing package A and then package B does not guarantee the same filesystem tree as installing package B, then A”. At least in Debian (and Ubuntu) this is considered a bug, and any occurrence should be reported as such. Package installation and removals should be idempotent, and that is tested in Debian.

I think it should certainly be the responsibility of the application vendor to ship a working and up-to-date application, but also the choice of the system administrator to choose to override what gets run on their system.

With what I’ve imagined, the sysadmin would install overrides for ABI-compliant security updates at his own discretion.

have a look at this interesting paper.

http://0pointer.net/blog/revisiting-how-we-put-together-linux-systems.html

I truly don’t understand all the recent whining about packaging managers. They do their job, and do it well. Yes, distro is a OS+software, tightly integrated, this has it’s perks (no DLL hell or 100 copies of same library in different versions). If you, as a developer don’t want to package your software for specific distribution, or, if you provide proprietary product – then compile it statically and dump all your payload into /opt/app_name and be done with it. Yes, it’s usually frowned upon, but it will work nonetheless.

Is this how we convince people to develop for our platform? “Let somebody else ship it for you, or build your own app update system completely different than anybody else’s”?

The problem with Linux is NOT package management. Package management is the result of the cause, not the cause itself. The problem is that Linux doesn’t have a functioning system of side by side assembly. Ironically, Linux users have made “DLL hell” a slogan, when Linux is in the deepest state of DLL hell.

nix package manager has already addressed this problem. Obviously, Canonical or Red Hat have to much pride in their own system that they would never switch to nix.

Actually, mobile phone stores are all basically package managers/repositories.

Heck, Sailfish’s even actually uses rpm as a backend.

The big difference with mobile phones is how the package are built, not the idea of package managment itself. For example, upgrading sshd on Debian will ask some question. Upgrading sshd on my phone won’t. Ever. But that’s just the packager’s philosophy.

The same applies to all the other packages. Fedora will ask a bunch of questions, and Sailfish *never* asks anything, but they both use rpm!

And then there’s arch: where the package manager won’t prompt for more than a confirmation (or warn if you’re trying to install two conflicting things), but no more than that.

Mobile phone package managers are KISS to the extreme, and comparable to things like Arch’s pacman. Debian’s apt is on the other end of this spectrum, and lots of user intervention (and knowledge) is expected.

Onto a more specific point:

> It’s also partially because package installations aren’t reproducible. Installing package A and then package B does not guarantee the same filesystem tree as installing package B, then A.

That depends strongly on the package manager you use (and to a certain amount, to how the packages created the package).

Finally, duped libraries isn’t just about disk usage, it adds up in RAM as well, since you’ll probably be loading multiple copies of the same lib into memory. And these can add up quite a bit, quite fast.