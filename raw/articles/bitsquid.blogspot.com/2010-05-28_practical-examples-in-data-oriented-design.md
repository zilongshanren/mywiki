---
title: Practical Examples in Data Oriented Design
url: https://bitsquid.blogspot.com/2010/05/practical-examples-in-data-oriented.html
author: Niklas
published: '2010-05-28'
source_blog: 'bitsquid: development blog'
source_site: https://bitsquid.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

Interesting read, I hope it's ok to ask some questions for such an old post.. I'm designing a scene graph now and decided to try the data oriented approach, but I can't figure out how to do certain things cleanly.. Regarding the scene graph, how would one remove or add a node? If deleting a node involves moving all nodes below it to the left in the array, isn't that slow? Also, the index for the mesh would have to be updated, which means that adding new objects that attach to the scene graph would involve changing the "remove node" function, correct? Do I have to search through all meshes to see if the node index for each mesh needs to be updated? Thanks for a great blog.

Note that our "scene graphs" do not cover the entire scene, only the objects within a particular entity. So adding or removing nodes is actually not a very common operations. (You would seldom add a new mesh to an entity.) So the system is not super optimized for that case. It is optimized for the common case of updating the scene graph.

That said, to add a node as a leaf (which you would normally do), you would just add it to the end of the scene graph array.

Removing a node isn't really necessary. You can just leave it in the scene graph. Unless you have some use case where you constantly add and remove nodes, but we don't have that.

Relinking within the entity's scene graph is thus the only thing that actually would require things to move around in the array. But that is an even more rare thing to want to do. You would seldom want to relink so that the hand is before the shoulder in the scene graph, for instance. So you can afford to have special, expensive code for those rare cases.

Thank you for giving us this interesting information. It is really helpful. Quickbooks , which is an accounting software used in many organization. Sometimes users face some errors like Quickbooks won't open . Due to this error Quickbooks shows page not loading or doesn't start. It stops ongoing procedure and windows crashes.

The QuickBooks Error 15227 is experienced when you are doing any Update of the product. This Error is known as the Update Error .We have some easy steps to fix this error code problem.

Very good read, thanks!(is there audio btw?) I wonder if there is a good book on data oriented approach...

ReplyDeleteThank you very much! The ideas reflect my practice as well, but here they are compiled in one presentation!

ReplyDeleteInteresting read, I hope it's ok to ask some questions for such an old post..

ReplyDeleteI'm designing a scene graph now and decided to try the data oriented approach, but I can't figure out how to do certain things cleanly..

Regarding the scene graph, how would one remove or add a node? If deleting a node involves moving all nodes below it to the left in the array, isn't that slow?

Also, the index for the mesh would have to be updated, which means that adding new objects that attach to the scene graph would involve changing the "remove node" function, correct? Do I have to search through all meshes to see if the node index for each mesh needs to be updated?

Thanks for a great blog.

Note that our "scene graphs" do not cover the entire scene, only the objects within a particular entity. So adding or removing nodes is actually not a very common operations. (You would seldom add a new mesh to an entity.) So the system is not super optimized for that case. It is optimized for the common case of updating the scene graph.






ReplyDeleteThat said, to add a node as a leaf (which you would normally do), you would just add it to the end of the scene graph array.

Removing a node isn't really necessary. You can just leave it in the scene graph. Unless you have some use case where you constantly add and remove nodes, but we don't have that.

Relinking within the entity's scene graph is thus the only thing that actually would require things to move around in the array. But that is an even more rare thing to want to do. You would seldom want to relink so that the hand is before the shoulder in the scene graph, for instance. So you can afford to have special, expensive code for those rare cases.

This comment has been removed by the author.

ReplyDeleteThank you for giving us this interesting information. It is really helpful. Quickbooks , which is an accounting software used in many organization. Sometimes users face some errors like Quickbooks won't open . Due to this error Quickbooks shows page not loading or doesn't start. It stops ongoing procedure and windows crashes.

ReplyDeleteThe QuickBooks Error 15227 is experienced when you are doing any Update of the product. This Error is known as the Update Error .We have some easy steps to fix this error code problem.

ReplyDeleteThanks for this.. This is great.


ReplyDeletecheckout Quickbooks database server manager

대구출장샵


ReplyDelete대전출장샵

부산출장샵

울산출장샵

정선출장샵

울산출장샵

대구출장샵

부산출장샵

This post was packed with great ideas. Thanks for sharing!

ReplyDelete