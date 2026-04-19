---
title: A new data storage model
url: https://bitsquid.blogspot.com/2010/08/new-data-storage-model.html
author: Niklas
published: '2010-08-18'
source_blog: 'bitsquid: development blog'
source_site: https://bitsquid.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

The basic idea is as follows:








- A database is a collection of objects.
- Each object is identified by a GUID.
- An object consists of a set of key-value pairs.
- The keys are always strings.
- A value can be one of:
- null (this is the same as the key not existing)
- true/false
- a number
- a string
- a generic data blob (texture, vertex data, etc)
- a reference to another object (GUID)
- a set of references to other objects (GUIDs)
- A special object with GUID 0000-00000000-0000 acts as the root object of the database.

This simple setup has many nice properties.

It is easy to map objects back and forth between this storage representation and an in-memory representation in C++, C#, Lua, etc.

We can perform referential integrity checks on the GUIDs to easily locate "dangling pointers" or "garbage objects".

We can add new fields to objects and still be "backwards compatible" with old code.

It is easy to write batch scripts that operate on the database. For example, we can lookup the key "textures" in the root object to find all texture objects and then loop over them and examine their "height" and "width" to find any non-power-of-two textures.

All modifications to the data can be represented by a small set of operations:

create(guid)

destroy(guid)

change_key(guid, key, value)

add_to_set(guid, key, object_guid)

remove_from_set(guid, key, object_guid)

These operations can also be used to represent a

*diff*between two different versions of the database.A user of the database can have a list of such operations that represents her local changes to the data (for testing purposes, etc). She can then commit all or some of these local changes to the central database. The database can thus be used in both online and offline mode. Versioning and branching systems can be built on this without too much effort.

Merge conflicts are eliminated in this system. The only possible conflict is when two users have changed the same key of the same object to two different values. In that case we resolve the conflict by letting the later change overwrite the value of the earlier one.

Note that this model only supports sets, not arrays. The reason is that array reordering operations are tricky to merge and in most cases the order of objects does not matter. In the few cases where order really does matter, you can use a key in the objects to specify the sort order.

It seems that are talking about NoSQL here. Take a look here http://nosql-database.org/ and you will find your concept has already been implemented. Well yours is a simplification of a nosql database. But it is basically the same. Maybe you will find some valuable ideas there as well.

ReplyDeleteHow do you handle the data in the engine? Presumably you want type safefy and efficient storage, so I'm guessing you'll generate classes/structs?




ReplyDeleteI'm presuming that a set of objects must be of the same type?

Have you considered how you'll be editing the data? Just a single tool with automatically generated tables, like a database tool, or custom tools for each type of data?

I'm assuming that just because you manage the keys as strings in the tools chain, in the actual engine you'll either use hashed strings to access some sort of hashtable, or preferably typed pointers.

amecky: Yes this is a NoSQL database, but that doesn't really say much, since NoSQL is such a vague term (encompassing anything that isn't a traditional relational database).



ReplyDeleteTo me, the simplifications and restrictions are what makes this scheme interesting. First, because a simple system is easy to understand, explain and reason about, which is very valuable in itself. Second, because these restrictions makes it possible to do conflict-free diffs and merges of database versions which means it can be used by multiple users in "offline" mode or as a revision control system.

You could use a NoSQL database as a backend for implementing this scheme though. Tokyo Cabinet could be a good fit.

Srekel: I'm still toying with this idea and it hasn't been implemented in the engine. There we still use JSON files in the file system.









ReplyDeleteAlso, this is intended for production data, not for runtime data. The runtime data would be effecient binary blobs "compiled" from this data. This data would only be touched by editors and the data compiler.

I would not generate classes/structs from this data. Classes would be defined in the editors and these classes would then save/load their data from the database.

In pseudo code something like (sorry for the bad formatting):

function GuiText:Load(db, id)

____self.id = id

____self.x = db.get(id, "x")

____self.y = db.get(id, "y")

____self.text = db.get(id, "text")

end

The editors would be written in a language with decent reflection support (e.g. C#), which means that this could be completely automated.

Objects in a set do not need to be of the same type. The database has no concept of "type".

There would be both a generic tool and custom tools for examining/modifying the data. Using the generic tool would be similar to looking at XML-files or JSON-files in a text editor -- useful for debugging but not a very good way of manipulating the data. The custom tools would be your game editors and exporters -- level editor, animation editor, particle editor, gui editor, etc.

As said above, the runtime engine will not touch this data, by the time it reaches the engine it will have been compiled to efficient binary blobs. There won't be any keys at all, just binary data matching the engine's structs that can be read directly into memory.

We something like this ...the editor would export the data in binary format and it would also export c structs so our game could load the data.

ReplyDeletethe problem was that designers would often update only the exe or only the data and then everything would be out of sync ....and it would crash :(

@Mihai Our solution to that is to always export to an intermediate format, not the final binary format.




ReplyDeleteThe intermediate format (JSON) is human readable and stable to version changes (since it is property-based it is quite easy to make it backwards _and_ forward compatible). The intermediate format is what is checked in to source control, so it can't be out-of-date.

The JSON->binary conversion is done by our data compiler. The data compiler is built and distributed together with our game executable. (In fact it is a special version of that executable.) This means that when designers update they will always get a data compiler and a matching executable that agree on the binary format, so the binary format can never get out-of-sync.

A change of the binary format triggers a recompile of the intermediate files (JSON->binary).