---
title: 2D game art work feedbacking and management tool
url: https://www.gamedeveloper.com/art/2d-game-art-work-feedbacking-and-management-tool
author: Junxue Li
published: '2013-07-03'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

# 2D game art work feedbacking and management tool

This article is about in the process of game art work creation, how to handle version control and tracing feedbacks. And a neat feedback management tool is introduced.

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

Usually the 2D art work creation and feedbacking process involves 3 people:

1. The artist: who creates the art; Either in-house artist or contractor.

2. The art director: who reviews and approves the art;

3. The Producer(or director, project manager): who is the head of the project.


And the process goes like this:

1. The artist creates the art;

2. The artist submit the art to the art director for review. The art director would either approve the art, or give feedbacks;

3. In later case, the artist would apply the feedbacks, make a new version, then submit to the art director again.

4. The step #2 and #3 may go many rounds, until the art is approved.


In this process, we need to solve some issues, as follow:

1. Keep the versions of the art work well organized. There must be an indicator, to show all the team members its current status: under working, delivered, feedback given, approved? And to show what is the newest version. And a good access of the newest version to all the team members. Sounds simple. But I have seen far too many teams have messed up the versions, and all versions of files scatter in many computers.


2. For each version of update, there would be feedbacks given by the art director; Those feedbacks need to be well documented, organized, and tracked. That the art director may know whether in a new version of art work, the feedbacks for the last version are all applied. In fact the tracking of the feedbacks needs some attention. If the art director has good memory, she/he may remember all the feedbacks given last time, and check out if all are fixed in the new version. But if her/his memory is bad, or she/he manages a big volume of art works, perhaps for multiple projects, then to find out if all the problems are fixed, theoretically, she/he must open the feedback documents, and compare the old & new versions, to see line after line if everything is fixed.


To solve these issues, in the projects I have participated, people have used many feedback management tool. Like Red Mine, you can upload versions of files, and post feedbacks to each version. It works, but this tool is designed for soft ware development, not well tailored for art production. And you need to deploy it on a host server. And there are many similar tools and some custom programmed tools.


So far, the best management tool I have used, is proofHQ. It solves the above issues nicely. And it is an online service, you need only to register to use it, no need of custom programming and deploy.

You can access it from here:

![](../../assets/645cd56dc6a44801.jpg)



I’m not writing a step by step tutorial for it, but only give a few basic ideas of how it works.

First, the artist may upload a picture by a single click. Then a “proof” is automatically created (the unit of all versions of an art works uploaded is called a “proof”). Then you add 3 people to view the proof: the artist, the art director and the producer.

The art work browser window is like this, in this case it is run on Google chrome.![](../../assets/2654a5bdcf9c8151.jpg)


Let me explain the browser, in this case Lucy is the artist and Tom the art director. And usually the ultimate decision maker is the producer, let’s call him Jim.![](../../assets/439a0337ceeaf517.jpg)



Area A: here shows the history of versions uploaded. You can see currently there are 4 versions uploaded, and the most recent is V.4. You can click each version to jump to it.


Area B: Here is all the points of feedbacks for this V.4, made by Tom. Click each bar, the detail of the feedbacks would appear at Area D.


Area C: Here is a list of all the person who see the proof, and the upper case letter box shows the status given by each person. S stands for Sent; O Opened; C Commented; D Decision made(need fix or approved). It is important to see the decision maker’s status, Jim’s.


Area D: Here is the feedback detail displayed, upon click corresponding bar at Area B. All the viewers can reply the feedback, and attach files here.


Area E: Here is the art work displayed. You have all the zoom-in and pan tools here, very convenient. ProofHQ has a very robust server, you can upload a picture up to 1.5G size, and still be able to browse it in real time. And upon giving feedbacks, you can draw marks on the picture by the imbedded drawing tool. Pretty useful, huh?


The drawback of proofHQ is that for each version, you can only upload a picture. This is bit inconvenient. Sometimes you need to upload multiple pictures for a version, for example, a picture with&without GUI frame, a picture with door close&open. Under this situation you need to send other pictures in attachment, which is unable to be viewed in the main window. Or you would have to upload extra pictures as new versions.


And there’s a function to compare pictures of different versions.

![](../../assets/82c871adb2762dff.jpg)


You can lock two pictures to synchronize the zoom-in and pan. And you can display all the feedbacks given to a certain version here, by clicking the bin. And the art director may strike out individual feedback upon checking.![](../../assets/9ac44d8fab48f3f1.jpg)


Upon an action is taken, for example, a new version is submitted, a new feedback made, a picture approved, the system would send email notification to all viewers. So nothing will be missed out.

Of course proofHQ provides folder structure, when you manage art works for multiple projects, you can organize them in folders.