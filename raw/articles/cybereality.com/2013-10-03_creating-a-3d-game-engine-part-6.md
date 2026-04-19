---
title: Creating a 3D Game Engine (Part 6)
url: https://cybereality.com/creating-a-3d-game-engine-part-6/
author: Cybereality
published: '2013-10-03'
source_blog: cybereality » the matrix was a documentary
source_site: https://cybereality.com/
category: graphics
fetched: '2026-04-19'
---

It’s been quite a while since my last 3D game engine post, but I haven’t forgot about it. In fact, I’ve been so heads-down in research I haven’t really done any development at all. I still feel like there are a few more books I will need to read to be better prepared, but I guess that will always be the case. So I’ve decided to at least start some preliminary work on the engine itself. Honestly, I’ve barely even started but I thought this series would be more interesting if you saw the genesis of the engine. From absolutely nothing to, well, I hope something respectable.

Since I’m considering this the precursor to my first 3D engine, I am code-naming the project “Engine Zero”. Partly because this is sort of the “day zero” and partly because I’m a programmer and zero comes before one. Though it does look like there is a “Zero Engine” already, so I will have to come up with a better name once I am further along. So behold, the first screenshot of the engine below. Yes, it’s just a message box. You have to start somewhere, right?

![Engine Zero 01](../../assets/0b82ed78deac2842.jpg)


OK, so that took all of 5 minutes to whip together. But I have done some planning in terms of file management and source control. First off, the way Visual Studio organizes files by default is non-optimal. Having the source files mixed in with project/solution/temp files is not what I want. So I have made a folder just for source code, another for the build binaries, and a project folder for everything else. This feels a lot cleaner and will help keep the project more organized. You can see the structure below.

![Engine Zero 02](../../assets/3d47705e229e9e79.jpg)


Next up, I created a source control repository for the project. I ended up going with Subversion, as this will be fine for just coding by myself. I know everyone loves Git, but honestly I find the tools and front-ends for Subversion to be a lot more mature than with Git. If I can use a user-friendly GUI and save myself time, I’d rather do that over command-line hacking. However, I am not using source control as my sole backup method. I have the project folder backing up to an external hard-drive and to the cloud. Plus, it saves each file revision, so I could rollback changes even if I forgot to commit to SVN. It would literately take Armageddon to destroy this code. And, frankly, if it’s the end of the world I’ll probably have more important things to worry about than the integrity of my backups.

Anyway, I am still very excited about this project and think the potential is enormous. While there is not much room for yet another 3D engine, I think I have some innovative ideas to bring to the table that the community would be genuinely excited about. I don’t want to over hype things this early into development, or give away all my ideas, but if you stick around with me through this series, I think it’s going to be a fun ride.