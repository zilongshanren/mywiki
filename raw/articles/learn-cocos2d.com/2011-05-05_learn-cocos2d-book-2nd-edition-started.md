---
title: Learn Cocos2D Book 2nd Edition Started
url: http://www.learn-cocos2d.com/2011/05/learn-cocos2d-book-2nd-edition-started/
author: James says
published: '2011-05-05'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Today, after several delays I finally got around to start updating the Learn Cocos2D book to its second edition. The second edition is due to be published in summer, likely in July/August.

I decided I’ll easy myself into it and start by updating the first chapter. There’s no code and relatively little to change. The biggest addition here is the list of popular Cocos2D game engines I wanted to add. Here’s a screenshot of the comparison table I added:

![Screen shot 2011-05-05 at 19.12.27](../../../wordpress/wp-content/uploads/Screen-shot-2011-05-05-at-19.12.271.png)


**Note:** the link to cocos2d should have been [http://www.cocos2d.org](http://www.cocos2d.org/)

The list doesn’t include all of the cocos2d ports, just those that are mature, stable and relatively up-to-date. I also completely removed the paragraph about Section 3.3.1 because that topic fortunately is no longer an issue.

### Errata Corrigata

Next I started to go through all of the 108 erratas that were posted on the Apress site. If you’re interested, here’s the errata list as [xlsx](http://www.learn-cocos2d.com/wordpress/wp-content/uploads/Learn_Cocos2D_Errata.xls) or as [csv](http://www.learn-cocos2d.com/) file with emails and names of reporters removed.

I knew that there were duplicates but I didn’t expect over 50% of the errata to focus on only two things: the mixed up images 3-1 and 3-2 was by far the most often reported errata. Following that were two packs of spider variables either not being declared or not being initialized in chapter 4. Those led to compile errors in one case and non-dropping spiders in the other - if you were typing in the code straight from the book.

After I had removed all duplicates I was left with 28 unique and usable errata items that I’m going to look into, and 14 of those I was able to fix today.

Once I’m done with those I’ll be going through the painstaking process of updating no less than 72 Xcode projects from cocos2d v0.99.3 to v0.99.5 to cocos2d v1.0. Or maybe I’ll just wait a couple more days for the final v1.0.

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

Where can we find the list of errata? They’re not showing up on the Apress’ Errata tab for the book.

They were not migrated when the Apress website was recently re-done. I got them as an excel file from Apress.

Can you post the excel file somewhere on this site?

I updated the post and added the errata as xlsx and csv files. These are just the reports though, not the corrections.

Waiting for your 2nd version. Your book the 1st version is simply awesome. The most helpful book I read among other books. The Game Center helper class helps me to easily integrate game center in my game. And I like your simple example to understand the features.

All the best wishes!

Thank you, much appreciated!![:)](../../../wordpress/wp-includes/images/smilies/simple-smile.png)


[…] I’m going through the process of updating over 70 (!) Xcode projects for the second revision of my Learn Cocos2D book, I thought I should outline the steps to upgrade an existing Xcode 3 project which uses […]

[…] these changes will be reflected in the second edition of the Learn Cocos2D book. The second edition will be released summer 2011, likely around July to August. This is my estimate […]