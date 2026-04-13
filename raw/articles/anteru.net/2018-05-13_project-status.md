---
title: Project status
url: https://anteru.net/blog/2018/project-status
published: '2018-05-13'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

As many other developers, I wrote [many projects](https://sh13.net/projects/) over the years, and because I do believe in open source, I released most of them in public. As I focused on [scratching my own itch](https://anteru.net/blog/2015/04/19/2819/), nearly all of my projects are not very popular, and some of them are mostly dead these days. However, if you went to my project overview, you wouldn’t be able to tell what state each project is in.

This weekend, I sat down to solve this once and for all, by creating an inventory of my projects, categorizing the status, and getting this all on my website in an easy-to-digest fashion. Sounds straightforward, but there are a few details which are hopefully of interest: Maintenance work, inventory management, and figuring out what states I want to actually report. Let’s dive in!

## Maintenance

Going through my various projects I noticed that my most successful projects in terms of users and community contribution were in a rather sad state. No easy-to-find readme, no continuous integration, and even worse, no changelog. Those are the three main things I look for in other projects, and I failed my own minimum bar here.

Solving the changelog is rather simple, but the continuous integration and the readme required a bit more work. You might think how can a readme require extra work? Before we get to that, a bit of context first: The most popular projects of mine are pure [Python](https://www.python.org/) projects. This means there’s exactly one way to publish them, which is [PyPI](https://pypi.org/). PyPI uses `setuptools`

for distribution, and there have been quite a few changes since I originally uploaded my projects.

These days, uploading to PyPI requires [ twine](https://github.com/pypa/twine). Additionally, as PyPI moved to

[, update paths and more need to get adjusted. Fortunately, the](https://github.com/pypa/warehouse)

`warehouse`

[documentation for package deployment](https://packaging.python.org/tutorials/distributing-packages/)was also significantly improved. Some of this may sound like busywork, but it’s actually worth spending the time. For me, it meant I could include some nicely formatted readme as the long project description, for instance – which required some extra markup in

`setup.py`

.I also used the opportunity to get some continuous integration in place. I’m not a big fan of the git monoculture, so I use Mercurial as my primary version control management, and hence [Bitbucket](https://bitbucket.org/Anteru/). Unfortunately, popular services like [Travis CI](https://travis-ci.org/) don’t support Bitbucket, so continuous integration was usually a pain point. Turns out, Bitbucket solved the problem themselves by introducing [BitBucket pipelines](https://bitbucket.org/product/features/pipelines), which is a very simple way to run a project inside a [Docker](https://www.docker.com/) container. With some updates to my [tox](https://tox.readthedocs.io/en/latest/) scripts, I got this running for my projects in no time.

With this out of the way, it was time to figure out what projects I had floating around besides the few projects I updated: Time for some archeology!

## Inventory

The first step is getting a proper inventory of all projects. As usual, I have a lot of choice as to what is my “source of truth”. Is it Bitbucket, where nearly all of my projects live? Is it PyPI? Do I store it inside each project or do I use some other place?

I was tinkering around with just using Bitbucket. Turns out, nearly all my projects are in fact on Bitbucket, so stuffing a `meta.json`

in there seemed like a good choice. I even have a mirror script for Bitbucket which I use to back up my repositories locally, so that seemed like the natural choice … except for my closed source projects. To get that to work, I would have to index my local repository store which contains both my public and private repositories. Given I have roughly a dozen projects I care about, this started to smell like some serious overkill, but I’d probably go for this if I had more projects floating around (or if I had more time to automate some things.)

Turns out, I do have a decent index already – the project descriptions I’m using to generate my website in the first place. [Liara](https://sh13.net/projects/Liara/) – the backend for the website – uses a YAML block at the beginning of each page to store arbitrary metadata, and that’s now the new canonical index. Problem solved, but now comes the next problem: What do we want to store there?

## Status?

The key bit of information is what status a project can be in. There are some obvious candidates like “active” and “abandoned”, but there are a few more states which I think are worth discerning. Looking through all my projects, these are the states I settled with:

**Active**: I’m working on this project, which means I’m doing some work at least once a quarter. Plus if someone reports an issue or requests a feature, there’s a decent changes it will actually happen.**Maintenance**: The project is good enough, all features I wanted to write are in there, and there’s really no reason to keep working on it. However, if someone would ask for a new feature or a bug fix, I’ll most likely get to it in a timely manner.**Archived**: Similar to*maintenance*, but I’m not going to fix bugs or add new features even if requested. Those are projects which are online for reference purposes, hopefully useful but not popular enough to warrant spending time on them.**Stalled**: That’s a tricky one, as it’s kind of similar to the next state –*abandoned*. The main difference here is that a*stalled*project solves some problem, but it’s probably not generally useful. An archived project is completely done, I achieved everything I wanted there. For a*stalled*project, I have some things in mind for how to continue, but no good use case to make it happen or justify additional effort.**Abandoned**: That’s the case everyone is familiar with. I started hacking but due to lack of motivation or users, I stopped before it was useful. That’s the main difference to*stalled*– stalled does work for some limited use cases,*abandoned*probably never got beyond proof-of-concept.**Deprecated**: This is a special state for projects which are no longer relevant. I only have few projects in this state, where the upstream project moved along and hence there’s no reason any more to use my library. It’s similar to*archived*, but due to factors outside of my control, it’s no longer useful.

On top of that, I also added a quality tag for production-ready projects. Some libraries like SJSON are extensively tested (more than 90% code coverage), have been used by other developers, and are also well-documented. Sticking the *maintenance* tag onto those doesn’t seem to do them justice, so if you happen to look at the details of one of those projects, the status will mention it’s production ready.

## Conclusion

Besides a much friendlier overview page, I also got something I was missing a lot – peace of mind. Previously, any project which was in “limbo” was a constant mental weight, as I couldn’t put it to rest properly. Now I have a simple way to clearly mark it as done and I can finally stop thinking about it without having a bad conscience about it. Time to move on to new projects 😊!