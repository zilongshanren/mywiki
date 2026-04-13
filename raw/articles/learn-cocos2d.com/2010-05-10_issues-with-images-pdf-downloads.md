---
title: Issues with Images & PDF downloads
url: http://www.learn-cocos2d.com/2010/05/issues-images-pdf-downloads/
published: '2010-05-10'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

On May 10, 2010,
in Announcements,
by Steffen Itterheim

I keep getting reports from users who either don’t see images on some lessons of the Tutorial and FAQs or who can’t download the Manual/Lesson PDF files.

The broken images usually fix themselves if you hit the reload button in your browser. You may have to wait a few minutes though. I’m still looking into what’s causing this. For the time being i have disabled the WordPress QuickCache plugin as i suspect it may have something to do with it.

If you can not download the PDF files and instead you get an error message which is formatted in XML like this:

Objective-C

1

2

3

4

<?xml version="1.0"encoding="UTF-8"?>

-<Error>

<Code>AccessDenied</Code>

<Message>Requesthas expired</Message>

This is because the links to the PDF files expire some time after you have loaded the webpage. A PDF link normally looks something like this:

Amazon’s S3 service will expire such a link after some time. Please do not share direct download links to the manual/lesson PDF files since they will expire, instead link to the lesson itself. If you have problems downloading the PDF, please reload the page and try downloading the PDF again.

I’m sorry about the inconveniences this is causing some of you.

I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. Help me help you by browsing the products in the Learn Cocos2D Store.

TilemapKit is the complete solution for tilemap game developers. Click an image to learn more!

Iso Map rendered by TilemapKit

Ortho Map rendered by TilemapKit

Hex Map rendered by TilemapKit

Steffen's Books

The iOS Action RPG Engine

Rapidly create your own RPG or action-adventure game with this complete starter kit. Includes an ebook, game source code and a royalty-free art package. More Affiliate Products …