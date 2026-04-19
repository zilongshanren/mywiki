---
title: Avoiding Content Locks and Conflicts -- 3-way Json Merge
url: https://bitsquid.blogspot.com/2010/06/avoiding-content-locks-and-conflicts-3.html
author: Niklas
published: '2010-06-03'
source_blog: 'bitsquid: development blog'
source_site: https://bitsquid.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

But having content conflicts is no fun either. A level designer wants to work in the level editor, not manage strange content conflicts in barely understandable XML-files. The level designer should never have to mess with WinMerging the engine's file formats.

And conflicts shouldn't be necessary. Most content conflicts are not

*actual conflicts*. It is not that often that two people have moved the exact same object or changed the exact same settings parameter. Rather, the conflicts occur because a line-based merge tool tries to merge hierarchical data (XML or JSON) and messes up the structure.

In those rare cases when there is an actual conflict, the content people don't want to resolve it in WinMerge. If two level designers have moved the same object, we don't really help them address the issue by bringing up a dialog box with a ton of XML mumbo-jumbo. Instead, it is much better to just pick one of the two locations and go ahead with merging the file. Then, the level designers can fix any problems that might have occurred in the level editor -- the right tool for the job.

At BitSquid we use JSON for all our content files (actually, a slightly simplified version of JSON that we call SJSON). So to get rid of our conflict issues, I have written a 3-way merger that understands the structure of JSON files and resolves any remaining

*actual*conflicts by always picking the right-hand branch.

If we disregard arrays for the moment, merging JSON files is quite simple. A diff between two JSON files can be expressed as a list of

*object[key] = value*operations. Deleting a key is represented by changing its value to

*null*. Adding a key is represented by changing a

*null*value to something else. Merging these operations is simple. We only have trouble when the same key in the same object is changed to two different values, but then we just pick one of the values, as explained above.

Arrays are trickier because without context, it is impossible to tell what a change to an array means semantically. If the array [1, 2, 3] is changed to [1, 2, 4] is that a single operation that changed the last value from 3 to 4. Or is it two operations, deleting the 3 from the array and inserting 4. How we interpret it will affect the result of our 3-way merges. For example, the 3-way merge of [1, 2, 3], [1, 2, 4] and [1, 2, 5] can give either the result [1, 2, 5] or [1, 2, 4, 5].

I have resolved this by adding extra information to the arrays in our source files. Most of our arrays are arrays of objects. For such arrays, I require that the objects have an "id"-field with a GUID that uniquely identifies the object. With such an id in our array [ {x = 1, id = a}, {x = 2, id = b}, {x = 3, id = c} ] it becomes possible to distinguish between updating an existing value [ {x = 1, id = a}, {x = 2, id = b}, {x = 4, id = c} ] and removing + adding a value [ {x = 1, id = a}, {x = 2, id = b}, {x = 4, id = d} ].

The 3-way merge algorithm I'm using applies some heuristics to guess array transformations even when no id-field is present, but the recommendation is to always add id-fields to array elements to get perfect merges.

You can download my 3-way Json merger

[here](http://www.bitsquid.se/files/json_merge.7z). I just wrote it today, so it haven't received much testing yet. But it is public domain software, so free free to fix the bugs and do whatever else you like with it.

A friend of mine wrote this http://github.com/rsms/js-object-merge which is a 3 way javascript object merger. Could be of interest maybe.

ReplyDeleteThats a very interesting way of making it possible to work together on things. Good post. :)

ReplyDeleteI like it. This is similar to my vertex.js project except vertex's objects have lexically ordered slots so they can be used as indexes.

ReplyDeleteAnd I've written the XML equivilent. More information can be found at: http://www.projectmerge.com

ReplyDeleteJames: That's nice. I would like to have a UI like that for my merger as well (as default you want it to merge without user interference, but the UI would be nice for diffs, etc). I'll see if I have time to write it.

ReplyDeleteDo you have an executable for JSON-Merge? I need to combine several Firefox bookmark backups together to restore missing bookmarks. Thanks.

ReplyDelete@Craig: You can find the sources here https://bitbucket.org/bitsquid/json_merger. If you can't build the exe yourself, give me your email address and I'll send it to you.

ReplyDeleteWe are a reliable third party Quickbooks services provider offering technical support for various any types of technical errors. If you are facing any problems you can call Quickbooks customer service. We provide you cost-effective support services suiting your budget.


ReplyDeleteIf you have a Quickbooks Desktop and you are thinking about shifting to QBO then you should take assistance from Quickbook Customer Service for better migration. They will assist you to import your files completely without losing data.

Thanks for sharing such an amazing article. Your article has such an strong features that are very helpful for us.

ReplyDeletehttps://premiumcrack.com/adobe-acrobat-pro-dc-crack/

google 4004

ReplyDeletegoogle 4005

google 4006

google 4007

google 4008

대구출장샵


ReplyDelete대전출장샵

부산출장샵

울산출장샵

정선출장샵

울산출장샵

대구출장샵

부산출장샵

I can recommend you a printing house. Many people just need printing. I found a good option https://bannerprintingsanfrancisco.com/. There are good prices, many services and everything can be useful for various types of business or even just business cards for different salons to make your own.

ReplyDelete