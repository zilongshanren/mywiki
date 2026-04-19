---
title: Content Repositories and Databases
url: https://bitsquid.blogspot.com/2010/01/content-repositories-and-databases.html
author: Niklas
published: '2010-01-19'
source_blog: 'bitsquid: development blog'
source_site: https://bitsquid.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

- Simpler -- no need to update or check-in.
- Changes are immediately visible to everyone.
- No merge issues.
- Collaborative editing (several designers working on the same level) is possible.

But we would loose all the nice features of version control:

- Accountability, history tracking and reversion.
- Branching and tagging.
- Having local, uncommitted changes in a working copy.

How necessary are those features? I would say that they are essential. But I also have a small nagging doubt that maybe this opinion is just the result of my own prejudices as a programmer. After all, people in many industries do lots of serious collaborative work using databases without branching, reversion or working copies. Still, I'm not ready to take the plunge and give up on version control features. (Though if anyone has tried it, I would certainly like to hear about it.)

Having those features by necessity implies some of the complexities associated with version control. For example, if we want a local working copy we need some explicit check-in/update mechanism. If we don't need a local copy we can just make the editor do

*svn update, svn commit*on each change and the repository will be as "immediate" as a database.Collaborative editing depends more on how the editor is implemented than on the storage backend. Regardless of whether we are using a database or a repository the editor will at some point have to fetch and display the changes made by other users as well as submit the changes made by the local user. With a repository backend,

*svn update*and*svn commit*could be used for that purpose.The only issue then is to avoid merge conflicts as much as possible, since they force the user to interact with the

*svn update*command and ruin the collaborative editing experience. Fortunately, that should be relatively easy. At BitSquid, we store most of our data in JSON-like structures. With a JSON-aware 3-way-merger, conflicts will only arise if the same field in the same JSON-object is changed, which should happen rarely.So, no great new way of storing content. Instead I just have to write a 3-way JSON-merger to protect the content people from merge conflicts. And then start working on the collaborative level editor...

We stored parts of our game data - cutscenes, missions, some game entity parameters - in a central FileMaker database, edited directly via FileMaker UI (think the cousin of Microsoft Access, coming from a Mac background). The lack of accountability, history/reverting, and any kind of merging sucked big time; we're going back to Lua files under Subversion.

ReplyDeleteThough AFAIK it doesn't provide any version control, did you investigate using (or extending) the Verse protocol for collaborative and real-time content editing/data storage?


ReplyDeletehttp://verse.blender.org/

For some time I have been interested in the possibility of storing game data in a database, but I haven’t tested it in any production yet. I agree on most of the pros and cons that Niklas mentions above, but I have some comments. I think one important (maybe the most important) advantage with using a database is that you can ensure referential integrity of data. Keeping referential integrity in a big project can be demanding, especially if you need to make major changes in a late stage. Of course you can have the tools doing the checks for you even if you use a standard approach with a repository – but in the end, depending on how far you go – you might end up with reinventing some kind database management system.

ReplyDeleteOn the con side I do not really agree on that you would lose accountability, history tracking and reversion. Most databases I have been working with have been built to track changes. My experience on databases are mainly from within the financial sector were accountability and tracking are fundamental . In most bookkeeping system it is essential to be able to check old balances or to undo faulty transactions. This is usually implemented by some kind of history tables. Having history you also get tagging.

I agree on that branching will be difficult but I am not sure how often you really must have that for game-data.

It is also possible to keep local mirrors of the database to use for testing “uncommitted” changes, but this would increase complexity and you would either need to invent some kind merge scheme for exporting local transactions to the main database or you need lock parts of the main database to allow for local editing.

Yes, if you just need accountability and reversion you can do it with history tables. If you start to need more features like working copies, merging and branching you might end up reimplementing version control on top of the database, which is about as bad as implementing a database on top of version control.






ReplyDeleteMaintaining referential integrity is interesting, but I wonder how much time it would really save, in the grand scope of things. Especially considering as you note, that you could make tools that did the same thing in a VCS.

Are you thinking about an object database or a relational database? Mapping the game concepts on a relational database can be tricky, since they tend to have a nested/hierarchical structure, better fitted to a JSON or XML format. And all the schema changes needed when you add stuff will be painful.

Here's an idea that is sort of a VCS/Database mix:

* The game data consists of a collection of Objects.

* Each Object is identified by a GUID.

* An Object consists of a set of Properties.

* Each Property is a (Name, Data) pair.

* The Name is a string. The Data can be a bool, a float, a string (also used for raw data, such as textures), a GUID (object reference) or a list of GUIDs.

It is kind-of/sort-of an object database... but one that would be easy to store in a VCS (each object is in a separate file) and easy to merge (you only have three possible operations: create object, destroy object, change property). Referential integrity is also easy. Just check that no other object refers to the GUID that you are about to destroy. You can also do mark-and-sweep garbage collection on the data to find (and strip) unused objects.

I don't agree that it's a good thing that changes are immediately available for everyone. Often I do not want to update content because of the likely chance that someone have introduced a bug that prevent me from working.

ReplyDeleteI don't know if it is a good fit for your needs but if you want a JSON centric database with multi version concurrency control you should take a look at CouchDb http://couchdb.apache.org/

ReplyDeleteThanks chenrik... I had a look at it and it is definitely interesting. I think loose-format, link-based databases have a great future.


ReplyDeleteHowever it doesn't seem to be a perfect match for what I'm talking about here. They explicitly say that their versioning sysem is not suitable for revision control (history is not replicated, etc).

It's definitely possible to implement a game asset repository using a database, we used one for Burnout Paradise.





ReplyDeleteThis particular one reimplemented a perforce-style revision control on top of SQL and still stored binary files in Perforce. (it copied perforce to the level that each user had their own database locally and then there was a big server database). So there were some non-ideal things in there!

However on the whole it worked quite well and provided excellent referential integrity - you couldn't delete a file someone was using and vice-versa.

You can certainly build a database that gives each user (or workspace) a different 'view' of the data, and you can use this to provide private branches/versions and other SCM features. I would highly recommend looking at how Accurev works for an idea of how to do this. Quite a few SCM systems essentially are databases already.

As for merging/branching, the view was that we didn't allow branching (there was very little branching in the code development as well) and then only allowed exclusive 'check out' of each part of data. So there was never any need to merge. Whilst this seems initially like a big restriction, with a database you can chop your data into much smaller pieces and so the exclusive check-out is on very little of the data at any point. e.g. each single object in the open world of Paradise City could be checked out individually.

How about Alienbrain?

ReplyDeletegoogle 2792

ReplyDeletegoogle 2793

google 2794

google 2795

google 2796

계룡출장샵


ReplyDelete춘천출장샵

청양출장샵

충북출장샵

강릉출장샵

충북출장샵

강릉출장샵

홍성출장샵