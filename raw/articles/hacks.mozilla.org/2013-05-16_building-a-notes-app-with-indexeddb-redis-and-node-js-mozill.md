---
title: Building a Notes App with IndexedDB, Redis and Node.js – Mozilla Hacks - the
  Web developer blog
url: https://hacks.mozilla.org/2013/05/building-a-notes-app-with-indexeddb-redis-and-node-js/
author: Mozilla
published: '2013-05-16'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

In this post, I’ll be talking about how to create a basic note-taking app that syncs local and remote content if you are online and defaults to saving locally if offline.

![notes app sample](../../assets/ad75f8202d68144f.png)


### Using Redis on the server-side

When adding records in Redis, we aren’t working with a relational database like in MySQL or PostgreSQL. We are working with a structure like IndexedDB where there are keys and values. So what do we need when we only have keys and values to work with for a notes app? We need unique ids to reference each note and a hash of the note metadata. The metadata in this example, consists of the new unique id, a creation timestamp and the text.

Below is a way of creating an id with Redis in Node and then saving the note’s metadata.

```
// Let's create a unique id for the new note.
client.incr('notes:counter', function (err, id) {
...
// All note ids are referenced by the user's email and id.
var keyName = 'notes:' + req.session.email + ':' + id;
var timestamp = req.body.timestamp || Math.round(Date.now() / 1000);
// Add the new id to the user's list of note ids.
client.lpush('notes:' + req.session.email, keyName);
// Add the new note to a hash.
client.hmset(keyName, {
id: id,
timestamp: timestamp,
text: finalText
});
...
});
```

This gives us the following key pattern for all notes on the server-side:

`notes:counter`

contains all unique ids starting at 1.`notes:<email>`

contains all the note ids that are owned by the user. This is a list that we reference when we want to loop through all the user’s notes to retrieve the metadata.`notes:<email>:<note id>`

contains the note metadata. The user’s email address is used as a way to reference this note to the correct owner. When a user deletes a note, we want to verify that it matches the same email that they are logged in with, so you don’t have someone deleting a note that they don’t own.

## Adding IndexedDB on the client-side

Working with IndexedDB requires more code than localStorage. But because it is asynchronous, it makes it a better option for this app. The main reason for why it is a better option is two-fold:

- You don’t want to wait around for all your notes to process before the page renders all elements. Imagine having thousands of notes and having to wait for all of them to loop through before anything on the page appears.
- You can’t save note objects as objects – you have to convert them to strings first, which means you will have to convert them back to objects before they are rendered. So something like
`{ id: 1, text: 'my note text', timestamp: 1367847727 }`

would have to be stringified in localStorage and then parsed back after the fact. Now imagine doing this for a lot of notes.

Both do not equate to an ideal experience for the user – but what if we want to have the ease of localStorage’s API with the asynchronous features of IndexedDB? We can use [Gaia’s async_storage.js](https://github.com/mozilla-b2g/gaia/blob/master/shared/js/async_storage.js) file to help merge the two worlds.

If we’re offline, we need to do two things similar to the server-side:

- Save a unique id for the note and apply it in an array of ids. Since we can’t reference a server-side id created by Redis, we’ll use a timestamp.
- Save a local version of the note metadata.

```
var data = {
content: rendered,
timestamp: id,
text: content
};
asyncStorage.setItem(LOCAL_IDS, this.localIds, function () {
asyncStorage.setItem(LOCAL_NOTE + id, data, function () {
...
});
});
```

The structure of the IndexedDB keys are very similar to the Redis ones. The pattern is as follows:

- All local ids are saved in a
`localNoteIds`

array - All local note objects are saved in
`note:local:<id>`

- All remote/synced ids are saved in a
`noteIds`

array - All remote/synced note objects are saved in
`note:<id>`

- Local notes use a timestamp for their unique id and this is converted to a valid server id once Redis saves the data

Once we’re online, we can upload the local notes, save the remote ones on the client-side and then delete the local ones.

## Triggering note.js on the client-side

Whenever we refresh the page, we need to attempt a sync with the server. If we are offline, let’s flag that and only grab what we have locally.

```
/**
* Get all local and remote notes.
* If online, sync local and server notes; otherwise load whatever
* IndexedDB has.
*/
asyncStorage.getItem('noteIds', function (rNoteIds) {
note.remoteIds = rNoteIds || [];
asyncStorage.getItem('localNoteIds', function (noteIds) {
note.localIds = noteIds || [];
$.get('/notes', function (data) {
note.syncLocal();
note.syncServer(data);
}).fail(function (data) {
note.offline = true;
note.load('localNoteIds', 'note:local:');
note.load('noteIds', 'note:');
});
});
});
```

## Almost done!

The code above provides the basics for a CRD notes app with support for local and remote syncing. But we’re not done yet.

On Safari, IndexedDB is not supported as they still use WebSQL. This means none of our IndexedDB code will work. To make this cross-browser compatible, we need to include a [polyfill for browsers that only support WebSQL](http://nparashuram.com/IndexedDBShim/). Include this before the rest of the code and IndexedDB support should work.

## The Final Product

You can try out the app at [http://notes.generalgoods.net](http://notes.generalgoods.net)

## The Source Code

To view the code for this app feel free to browse the [repository on Github](https://github.com/ednapiranha/generalnotes).

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 4 comments

MatrixMay 17th, 2013 at 01:54Scott TurnerMay 17th, 2013 at 11:50Aaron ShafovaloffMay 20th, 2013 at 20:41Robert Nyman [Editor]May 21st, 2013 at 01:41