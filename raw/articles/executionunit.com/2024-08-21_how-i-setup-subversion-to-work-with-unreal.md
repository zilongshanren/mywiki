---
title: How I setup Subversion to work with Unreal.
url: https://www.executionunit.com/blog/2024/08/21/how-i-setup-subversion-to-work-with-unreal/
published: '2024-08-21'
source_blog: Blog | Execution Unit
source_site: http://www.executionunit.com/blog/
category: game programming
fetched: '2026-04-13'
---

## Overview

I have used Perforce, Subversion (SVN) and Git with Unreal on AA Game and Indie Games. I feel that Subversion is often overlooked as a source control solution for small to medium teams. Subversion has fallen out of favor and is no longer cool. It definitely earned a reputation for “screwing up branching” but this isn’t an issue for Unreal projects. Subversion is fast, stable and reliable.

This is a blog to help you IF you are interested in an alternative to Git+LFS and Perforce+$$$. If you’re not interested that is fine.

It’s not just me who thinks Git+LFS is bad. Ari Arnbjörnsson also thinks it kinda sucks for Unreal development.

### Summary

For small hobby projects Git/GitHub are fine. Ignore this, carry on using Git.

For AAA just use Perforce, you’ve got the money.

For film or architecture/visualization, just use perforce as your files are likely way to big and your staff less open to change.

For medium to AA games I’d argue Subversion is fine. Not perfect, but fine. For teams between 5 and 50 members it fine. For 100+ you’re definitely in the Perforce territory and outside my experience. You might be fine. I’d hazard a guess that you would be fine but this is outside of my experience.

## Why

Opinions, you don’t have to agree with me.

### Git+LFS is slow

It’s not terrible but it’s slower than Perforce and Subversion. Locking is also not perfect and I found it failed frequently. I do not consider Git+LFS to be mature for the thousands of opaque binary files that Unreal uses. I do not consider Git+LFS locking to be mature for medium sized teams.

### Git+LFS doesn’t scale as well as Perforce and Subversion.

Git stores the whole repository over time locally. This is great because you can switch branches trivially, experiment more easily and develop powerful workflows. Alas it means every binary file exists in all it’s forms over the life of the project locally. Even a medium sized Unreal game will be 100GB of live assets and nanite is making this look small. After a few years for a small team of 10 this can result in a dataset nearing 1TB of data. Disk space is cheap but it’s all just noise and slows Windows and git down.

Git’s primary innovation of it’s branching strategy and branching is not used by most Unreal devs because locking files is integral to the workflow of Unreal Editor.

A AAA game will easily have 1TB of live assets and a total dataset can easily be 50TB in size. For this scale Perforce really is the only product in town… but most people will not be working on a game that large.

### Perforce

This is industry standard. This is a pointless phrase and tells you nothing of whether it meets your needs. The games industry is conservative and like all mature industries, full of group think.

Perforce is stable, secure and scales well. If you want to use it, it’s great. It’s expensive though. It broadly uses the same algorithms as Subversion to store data but it’s primary advantage is Streams, tight integration in to Unreal Editor and it scales to HUGE depot sizes.

Unlike GitHub, GitLab or Gitea, Perforce is a stable product over time. You won’t be upgrading every week with security patches you won’t have fancy websites to worry about being hacked, you will basically, every so often, load the admin interface to check why it’s starting to crawl and delete users because you’re running out of seat licenses and the CFO wonders why your sending $$$ to a company in SW England.

## Good and bad of Subversion

I’m just gonna add a summary here because you’ve already read a lot.

- + server is simple to setup on Windows, Linux, *BSD or macOS
- + easy to maintain
- + works just as well if not better than Perforce with Unreal Editor
- + is substantially faster than Git.
- + Is supported by UnrealEd out of the box
- + Repo size scales better than Git (but not as well as perforce).
- + Team size scales better than Git (but not as well as perforce).
- + Simple to backup… remember to do this!
- + Free to use.
- + Highly scriptable, much better than Perforce, same as git
- + Integrates with Jenkins out of the box
- + Supports locking by default… and it works and you can cancel/override locks.
- + Subversion is extremely mature. It changes slowly letting you get on with you actual job of making a game.
- + BP “diffing against last depot” is fast because the “depot” reversion is stored locally (see negative [1])
- -
[Tortoise Subversion](https://tortoisesvn.net/)is the best “desktop UI” for Subversion. It’s worse then P4Win, GitFork, GitExtension, GitHub Desktop. But you’ll mostly be in Unreal or Rider both of which support Subversion very well. - - When you checkout an Subversion repository you get two copies of nearly everything (by design this is to make reverts/diffs fast) and this is why for AAA it’s not good enough. Still better than a version of everything through all time like git-lfs though. [1]
- - You don’t get all the bells and whistles of bug tracking, CI, Pull requests that you get with GitHub/Lab and for $$$ with Perforce.
- - Perforce streams are a good way to lower bandwidth for remote teams. With Subversion you can (ab)use it’s
`externals`

property to create something similar but it’s not as powerful. It does work though. I’ve used externals to create “views” of the repo for design, art and code. - - Perforce support exists. It’s not that good but it is there. Subversion support is the internet.
- - Perforce is industry standard and by that I mean people who know nothing about source control will complain you are not using Perforce only to complain just as much if you do use Perforce. Go figure.

## Setting up Subversion

**This isn’t a tutorial, there are already lots of those out there for your OS of choice**

A fresh install of any operating systems will do. Install Subversion, Apache and Python 3 on these machines which are all mature well used packages on most operating systems. There are detailed docs for all platforms on installing Subversion. I’ll just give my set up here. If you must use docker… then there are docker files out there.

You’ll need at least two (metal or virtual) machines if you want a live backup (which I recommend). The backup can be a small PC in your home. You don’t need to give AWS/MS more money. Just make sure you do back shit up!

Here is my (FreeBSD) apache conf file for svn

`/usr/local/etc/apache24/Include/svn.conf`

.

1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 |
|

There are some tweakables in here but this is what works well for me. Again, there are lots of tutorials about setting up apache+svn.

## Setting user password

Apache will be doing user authentication. The above file tells apache where the user password database is. This command adds a user and sets their password.

`1` |
|

To delete a user, edit the svn-auth-htdigest file and delete the line with the username in it.

If you want groups for finer access control look up svn conf/authz files, you can set groups of users, set access controls to specific paths, set who can read and who can write etc.

## Security

I always run access over VPN software. I use wireguard but use whatever you want. This gives me peace of mind. While apache and subversion are very mature and secure it pays to be careful.

If your team is on a LAN then you don’t need a VPN as you can probably trust your team members (ymmv).

## Maintenance script

Server shell script to repack/clean repositories overnight. I’m not actually sure if this is needed but it’s mentioned in the docs so I do it. I went years without doing this and never had a problem.

Again this is a FreeBSD csh script.

1 2 3 4 5 6 7 8 9 10 11 12 13 |
|

## Backing up

Subversion has a concept of syncing two repositories. The easiest way to backup your live repo is to have another machine, somewhere in the universe, that syncs all commit from the primary repo to the backup repo. I run this script nightly but you can do it every hour if you want.

Note in 15 years of using Subversion I’ve had one corruption (due to a disk failure) and I had the repo back online in an a few hours. This was basically the time it took to move the data across the internet.

There are many good tutorials on setting this up.

## Integration with other tools.

Subversion has various hooks that get called when things happen. The most useful is the post-commit hook to trigger Jenkins and to push a message to discord of a change.

In the trunk of each repository I have a folder called `.hooks`

. When subversion has committed
a file to the repo successfully this hooks/post-commit script is called

1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 |
|

The script never really changes and stores the secrets I don’t want in the repository (password, tokens etc).

The script copies a python file from the repo called post-commit.py and runs that. This allows each repo to have scriptable actions that are easily changed and the changes are recorded in the repo.

### post-commit.py

This file does all the work. It copies a json file from the repository in `/trunk/.hooks/post-commit.json`

and uses data in that to decide what actions to do depending on what files/paths changed.

*If you’re going to use this you’ll need to install some python packages*

### post-commit.json

This is the file contains configuration info for jobs that will be run if certain conditions are met.

Hope this helps someone.

### Changes:

- 240827 - added video on git+lfs not being great.

EOL

## Comments