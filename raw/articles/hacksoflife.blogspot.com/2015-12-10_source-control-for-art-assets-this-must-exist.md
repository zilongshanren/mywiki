---
title: Source Control for Art Assets - This Must Exist
url: http://hacksoflife.blogspot.com/2015/12/source-control-for-art-assets-this-must.html
author: Benjamin Supnik
published: '2015-12-10'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

I've been thinking a lot lately about revision control for art assets. As X-Plane has grown, our art team has grown, and as the art team has grown, our strategy for dealing with art assets is coming under strain.


Currently we use GIT for source code and SVN for art assets in a single shared repo. No one likes SVN - it was selected as the least bad alternative:







For the task of getting art without revision control, rsync would be just great.









But we can imagine if it was. If it was, we wouldn't keep a fresh mirror of every version of X-Plane on the server - we'd just have a big pool of content-addressed files (a la GIT) and fetch the subset we need.



Currently we use GIT for source code and SVN for art assets in a single shared repo. No one likes SVN - it was selected as the least bad alternative:

- Since it's centralized, it's much more in line with what artists expect for revision control - no explaining distributed source control to non-programmers.
- It doesn't replicate the entire history of an art asset, which is too much data.
- Parts of a tree can be checked out without paying for the entire tree.
- There are decent GUIs for every platform.
- It's scriptable for integration flexibility.

~~It is just so slow. You can look at your wire speed and SVN's speed and you're just not getting a fast transfer.~~**Update**: this finding is wrong! SVN's speed at transferring binary files is about the same as your wire speed to the server. I'll write up a separate post on speed tests. Many of us are using GUI clients and it is possible that some of them are adding a tax, but the command line SVN client is similar in up/down transfer speed to GIT and rsync for basic data transfer.- SVN can't do an incremental update without a working repo, which means having a .svn directory even for the art assets you're not working on. That means at least 2x the disk space on the entire art asset pile, just to be able to get latest.

#### GIT's Not It

Since I am a programmer, my first thought was: well, clearly GIT can be made to do this, because GIT is the answer to all problems involving files. I spent some time trying to figure out how to shoe-horn GIT into this roll and have concluded that it's not a good idea. GIT simply makes too many fundamental assumptions that are right for source trees and wrong for art asset piles. We'd be fighting GIT's behavior all of the time.#### We Kind of Want Rsync

There are two parts of art asset version control: letting the guys who are doing the work make revisions, and letting the people not doing the work get those revisions. It's easy to overlook that second task, but for any given person working on X-Plane, that artist is*not*working on*most*of the airplanes, scenery packs, etc. And the programming team is working on*none*of them.For the task of getting art without revision control, rsync would be just great.

- It can work incrementally.
- It only gets what you need.
- It's reasonably fast.
- It doesn't waste any disk space.

- Files live on the server.
- We fetch only the files we want.
- We basically do a straight network transfer and we don't try anything to clever.

#### We Kind of Want The X-Plane Installer/Updater

We solved the problem of getting the latest art assets for all of our users - it's called the X-Plane updater. In case you haven't spent your copious free time wire-sharking our updater, it's really, really simple:- All files live on an HTTP server, pre-compressed.
- A manifest lives on the HTTP server.
- The client downloads the manifests, compares what it has to what's on the server, then fetches the missing or newer files and decompresses them.

But we can imagine if it was. If it was, we wouldn't keep a fresh mirror of every version of X-Plane on the server - we'd just have a big pool of content-addressed files (a la GIT) and fetch the subset we need.

#### Let's Version Control the Manifest

So naively my thinking is that all we need to do is version control our file manifest and we have our art asset management solution.

- Each atomic revision of a version-controlled art asset pack (at whatever granularity that is) creates a new manifest describing exactly what art assets we have.
- Art assets are transferred from a loose file dump by syncing the manifest with the local machine.

*any*source control system and get away with it, because the manifest files are going to be relatively small.

#### Does This Really Not Exist

I feel like I must be missing something...does a tool like this not already exist? Please point me in the right direction and call me an idiot in the comments section if someone has already done this!

Sounds like you're talking about git large file storage honestly. https://git-lfs.github.com/


ReplyDeleteThough before this was a thing everyone I know who works in game dev used perforce for version controlling all game assets.

I saw several "big file" extensions to GIT...is there an open source production quality LFS server yet? Or traction for LFS? My concern was to not base our work-flow on what might be an evolutionary dead-end in the several big file extensions.


ReplyDeleteAnd yes, perforce seems to be pretty ubiquitous. I think my brother might be using it at his company, I'll have to ping him. The overall tone sounded like "solid, not amazing, and sometimes crufty"...not the strongest recommendation, but maybe not the worst?

I've been pondering over this same problem for a long time now and haven't found a satisfactory answer yet. git-lfs seems to be gaining a lot of traction in the last couple of months, so that might be worth another look.



ReplyDeletePerforce is used a lot in game development, but from what I hear it seems to be geared more towards artists than programmers. It's largely centralized and requires you to explicitly claim files before you're allowed to edit them, which sounds a bit archaic to me. Being spoiled with Git's shiny branching models, I think moving to Perforce would feel too much like a step backward.

I also remember reading an article some time ago from a game developer (I think it was DICE, correct me if I'm wrong) using Bittorrent Sync as a means to collaborate on art assets, in addition to traditional source control. This falls in line with your "we kind of want rsync" argument and sounds like it would scale nicely for larger organizations. I think the biggest challenge is finding a good workflow that is easy enough to learn and that makes everyone on the team happy.

Geared toward artist, centralized, and locking are actually -not- bugs in this particular case!


Delete- Our art team varies in sophistication; some of them could clearly use GIT, and some are just barely okay with source control.

- We have file formats that are often impossible to merge, and most of the time it's one artist, one pack, so locks are a feature, not a bug...it will force a small amount of communication that is needed anyway before we have an epic merge fail.

In terms of "share stuff", we've found that drop box is great at our scale for "throw it over the wall" - it's fast and couldn't be easier.

Well, you can integrate Perforce and Git (Git-Fusion). Basically the git repositories will be part of the the Perforce repository tree as sort of leaves (from Perforce's point of view) and will be regular Git repos for Git. This way developers can work in Git and others in Perforce and still share things.


DeleteWhile I can work with both I found it often quite helpful to be able to restructure/remap the whole project in Perforce using a client spec. This seems to be missing in Git. In Perforce I miss the distributed nature of Git. Can't have everything.

Perforce does all of this. Maybe you want to evaluate this. Costs money though.




ReplyDeleteIn particular is supports:

- Working with large files

- Getting only the needed files form the sever, not all

- Not wasting space with .svn/.git copies of the files

- Reasonably fast.

They have quite some customers in the video game industry because of their support for huge projects and large files. We are using it for a different kind of application with similar requirements (100000s files, size up to GBs range). Perforce is well suited for the job and has good 24/7 support.

in addition to git-lfs, there is also git-annex from a few years ago. It's still around, here: http://git-annex.branchable.com. Your description of tracking the manifests reminded me of git-annex.

ReplyDeleteHere's a page from the git-annex team/guy describing the differences: http://git-annex.branchable.com/not/.

I can't say much about either of these but they seem to target your issue. Good luck.

That's a great link - and sort of shows our bewilderment re: GIT and large files...there's at least git-bigfiles, git-lfs, git-annex, and I didn't even know about git-fat and git-media.

DeleteI used Perforce at Google and hated it. Now at my company we use git for source version control and git-fat for anything version-y involving large files. Works fairly ok.

ReplyDeleteGithub and Gitlab (the git servers I use) both support LFS now so I don't think it's going to be a dead end any time soon

ReplyDeleteThere is also Alienbrain. I haven't used it though. http://www.alienbrain.com

ReplyDelete>One of the main problems with SVN is performance - if I have to change a branch, having SVN take half an hour to get the new art asset pack I need is pretty painful. So it's at least interesting to look at the architecture rsync implies:



ReplyDelete`svn switch` to a branch should never take ~30 minutes to complete. Switching in Subversion should be very fast so what you describe is unexpected.

What process do you follow to switch a working copy to another branch? Do you run `svn switch`?

Would Plastic SCM meets your bill? A bit gitty but cost money.


ReplyDelete1TB file is fine, according to them.

You may want to check www.multiverse.io. It's an actively developed Git-based backend for the Alembic 3D format.

ReplyDeleteI want to clarify the previous comment. Subversion is a universal version-control system and it natively supports storing large binaries (art assets in your case). For example, checking out ~500MB of assets from Subversion repository (transatlantic) should take about 12 miniutes. It should take much less time if Subversion repository is located on your LAN. Therefore, changing to another branch should not be as painful as you describe.



ReplyDeleteHowever, some details about your use case are not clear. Could you please provide a bit more information on the use case?

* What is the size of the working copy that you switch to another branch?

* How exactly do you perform this operation? I.e. what commands do you run?

* Do you access the repository over WAN or LAN?

* What version of Subversion do you have on the server and the client?

I concur with your comment re: speed, and my comments about SVN's speed in the post are -incorrect- (I need to edit the post, and I'm going to write a new post with my test results).


DeleteWhile I haven't tested switch specifically, I did a bunch of pure upload/download tests in SVN, GIT, and rsync (loose files and a tarball) and found them all to be pretty well clustered around the wire speed.

I've recently gone through the same problem at getting two different mindsets to suit teams.











ReplyDeleteThe simple answer is that no such solution does exist and there's a wide open gap in the market for someone to fulfill (which doesn't cost the earth).

Git's LFS is very promising but it currently struggles with end users installing, support from Git clients and it's still young with server support.

But the core issue is that some members of teams are illerate in revision control and often refuse realisng they're missing a core social skill.

DVCS aren't simple things and require training, but the likes of Automatic Merges in my experience just cause confusion. During which time the same users will be too confused on even resolving a merge conflict correctly.

Two things need to change:

We need a DVCS with the power of Git (for the love of the programmers) but with an idoit mode. Tools need to welcome novice users and let them use advanced features like branches if they choose to learn.

More needs to be done within teams to make everyone social users with version control. It's bad when users decide to stop learning about something they require every day.

The best solution so far (Unity3D project, mixed art/code in the same repo) that I've found is to use Perforce + Git Fusion. Perforce have done a really good job at giving perforce to the novice users and allowing programmers to use Git on the same repository.

(Don't even bother using git-p4, it just doesn't work too well)

Why do you think that DVCS is important for the art team? What's the win compared to centralized version control and (dare I say it) locking?



DeleteNaively, it seems to me that the really big difference between our programming team and art team isn't just technical sophistication with command line tools and VCS experience, it's that the code is very merge-able and the art assets are almost entirely un-merge-able.

Until we change that about the art assets (and that's somewhere between an expensive long term goal and impossible) the work-flows are going to have to be very different.

I've seen some work on true revisions for graphics assets. With compositions like the layer trees in GIMP or Photoshop, this works. It also works somewhat well with scene graphs.



DeleteThe interesting thing with scene graphs is that you actually can merge changesets. One of the big blockers here is that graph diffing is nowhere near as mature a field as line diffing.

You might want to take another look at Perforce. The new Helix platform has native DVCS features that make it possible for devs to narrow clone just the stuff they need and artists can narrow and shallow clone only the head revisions of just the art assets they need. It saves a lot of transfer time and disk space.


ReplyDeleteHonesty disclaimer: I work for Perforce now, but I say this because I'm using the tech myself not because I work there.

I also recommend Perforce. Checkout their newest, GitSwarm, while you're at it. It uses GitLab as the front-end, git-fusion in the middle and perforce on the backend. It would allow your artists to user Perforce, and devs to use git without having to support two VCS's.

ReplyDeleteI've worked as an artist/technical artist in the game industry for a while now and I've (had to) use various versioning software. Perforce is definitely the one I am most familiar and comfortable with.





ReplyDeleteI can't really testify to relative speed etc., but I can say it works well for large teams, large and numerous files, complex code/asset structures, and working on multiple projects / branches.

If you have P4 savy tech staff you can do some fairly fancy setups with streams, automation, etc. I recently used the perforce python API to set up and auto-build machine that understood dependencies and on asset check-in would rebuild an asset as well and any cross dependent assets, reverting all if any failure occurred. Then it would notify the police with names and dates of bad artist check-ins ;)

Not sure if that helps at all, but I can say a couple things. Artist are not engineers; if you want them to follow versioning best practices without a mental breakdown you need to provide them with something they can reasonably figure out. The other thing is, the larger your team the more sophisticated things get. Three artist creating content is a lot different than thirty artist working in tandem with outsource teams in other countries.

Hope that helps.

Is reverting back to old version really that important for art work?



ReplyDeleteFor code, being able to revert is pretty essential.

But for artwork, I'm not so sure.

Hence, I store art on Dropbox, and be done with it.

I make an exception for SVG vector art, because it is text, and is well suited for storing in git.

Versioning is a mandatory feature, and so is branching. Here's why:




Delete- Versioning - at any given time, the latest version of an aircraft (which is an art asset pack in X-Plane) may not be what we are shipping now. For example, we have an artist reworking our king-air. He's not done yet, but he has a check-point that is pretty good on the tip of SVN.

When I go to cut a bug fix patch to our current release, I need to go pull the last "stable released" version of the Kingair, not his latest.

If we always have to get latest then artists are stuck in an "always be shipping" mode. So old versions must be accessible.

- Branching - we fixed a problem in the FM that will require a small change to all flight models - it's really quick to apply (it's just a resave in the airplane editor). For that in-progress Kingair, I need to take the last shipped one, resave, and make that a branch. Otherwise I can't apply the re-save until the artist finishes his next-gen work.

You could try putting each plane (or similar asset) in its own repository. That way you get full history, although only that needed for the craft.


ReplyDeleteYou can also do shallow clones. Which allow you to only fetch the current revision (i.e. just like rsync). After that you can fetch revisions incrementally since then.

I've heard reports that one-pack-per-repo in GIT works decently from other flight simulation developers. We have "all planes in one pack" in GIT on the mobile product and GIT is definitely getting dragged down.

Delete