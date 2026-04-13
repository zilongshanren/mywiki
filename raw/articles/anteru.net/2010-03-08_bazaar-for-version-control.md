---
title: Bazaar for version control
url: https://anteru.net/blog/2010/bazaar-for-version-control
published: '2010-03-08'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

I’ve been a long-time user of Subversion – and I really like the project. However, I recently switched to Bazaar for nearly all of my work, and I’d like to explain some of the reasons behind this. First of all, for those who are not familiar with Bazaar: Bazaar is a distributed versioning system built by Canonical, the same guys that created Ubuntu. It’s written in Python, and runs on Windows, Linux and Mac OS X. The UI is very consistent, as it is written with Qt, so you can easily switch between systems. As I said, it’s distributed, which is a major differences to centralised versioning systems like Subversion or Perforce. Centralised systems store the history – like the name implies – at a central location. If you run log or diff, this central location has to be reachable. The clients store only the current revision and have to query the server for many operations.

Distributed systems on the other hand don’t require a central server at all. Instead, they store all history at each client. That is, you can work locally all the time and you never have to connect somewhere. It’s likely that you will have some location to which you push your changes so they can be easily discovered by your co-developers, but this is by no means required. Many modern versioning systems are distributed, like git, Mercurial and Bazaar.

## Why you should prefer a distributed system

Distributed systems have some advantages over central systems, specifically:

- Working offline is easy: You can do all your work locally, revert, query the logs, diff, without network access. That’s really cool if you are not online or your server is unreachable.
- Simple branching: Branching is typically very efficient and well supported in distributed systems, as it’s a core part of them. Merging is usually much more flexible as well.
- Easy backup: Every developer has a full backup available all the time, so if your server explodes, nothing is lost at all.

Of course, there are some disadvantages as well:

- It may be more difficult to know which copy is the “latest”. Usually, a server is still running somewhere to which all developers push or which gets the latest changes merged to, but you have to agree on this. That’s simply an organisational issue.
- Local history can become huge, especially when you store binary files. If you’re about to store binary data, a central system is usually superior.

## Bazaar

I’ve tried git, Mercurial and Bazaar, and I stuck with the latter. Feature-wise, they are all very similar. Git is more low-level than the others, so it might be easier to hack something together with git, but for day-to-day use, I didn’t find a killer feature in any of them. Performance-wise, git is the fastest, but that’s only relevant if you do benchmarking. For the projects I work on, Bazaar and Mercurial are fast enough, as the response time for most commands is less than a second. Most of the time, you’re going to be limited by network speed during pushing/pulling anyway, and typical commits (changing a dozen files or so) are instantaneous with all of them. One nice feature of Bazaar is the excellent interoperation with other VCS. I’ve been using Bazaar heavily against a Subversion server, and this really worked fine – much better than with git, which was very slow when importing from SVN, and each operation against the SVN server took some time as well. The nice thing when using Bazaar against SVN is that renaming/changing content is much more robust than with SVN alone – I did some large-scale refactorings with both SVN only and Bazaar against a SVN server, and using Bazaar is much more comfortable. For instance, you can rename, change content, rename again, commit, and then push to SVN without any problems, even if one of your renames only changes the case.

Right now, I’ve switched here to Bazaar for a rather big project (5 years of history and 3000 revisions), without any trouble. I’m developing from three different machines, and keeping them up-to-date was very easy. One didn’t have internet access for instance (let’s call it B), so I would pull the trunk on machine A, and pull updates to B from A – now B has internet, and I pull from trunk again, without any problems.

Another reason I like to use Bazaar is that the UI is nice, useful and consistent across all platforms. Most of the time, I actually use the UI, as it makes many operations rather easy (like selecting which file to commit, see added files, edit ignore lists …) Finally, Bazaar has corporate backing, which provides two main benefits: Someone is getting paid to write docs, so Bazaar is really well documented. The other benefit is that some developers are working full-time on Bazaar, which means that bugs, suggestions, and other issues get eventually looked at even if they’re rather boring. With git, you don’t even have a proper way to report a bug, while you can be pretty sure that any bug you report against Bazaar gets processed some day. All in all, I would recommend to take a look at Bazaar when you are choosing a DVCS, as it might be actually all you need in an easy-to-use package with a nice, helpful community.

One side note: If you try Bazaar 2.1.0, you should get the Bazaar Explorer 1.0.0rc2, as there is a known issue with the one bundled with 2.1.0 – the toolbar is simply empty in the explorer bundled with 2.1.0.