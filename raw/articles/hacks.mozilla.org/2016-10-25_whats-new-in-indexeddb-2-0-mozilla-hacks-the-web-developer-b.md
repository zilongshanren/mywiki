---
title: What’s new in IndexedDB 2.0? – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2016/10/whats-new-in-indexeddb-2-0/
author: Bevis Tseng
published: '2016-10-25'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

The draft of [Indexed Database API 2.0](http://w3c.github.io/IndexedDB/) is almost complete, providing several new APIs for fine-grained access to IndexedDB.

The good news is that all these new APIs are implemented in Firefox and will be available in the release of Firefox 51 (currently available in [Developer Edition](https://www.mozilla.org/en-US/firefox/developer/), scheduled for general release in January 2017). In this article, we will share some examples of how to use these APIs to access IndexedDB in a better way.

## Setters to `IDBObjectStore.name`

and `IDBIndex.name`


In the [previous version of the Indexed Database API](https://www.w3.org/TR/IndexedDB/), IndexedDB allowed developers to upgrade the schema of the indexedDB by adding/deleting object stores and indexes; but renaming existing object stores and indexes was not possible.

This made it impossible to properly name the index and object store, when the original name no longer accurately represented the new schema of the objects to be stored. In addition, it was a waste of time to move objects into a new object store just for renaming.

For example, let’s say there is an object store called “text messages,” to store plain text messages sent or received on a mobile network. Later, suppose the developer would like to provide richer content messages, that include attachments such as images, audio, and video —it would be better to give this object store a more generic name such as “mobile messages.” Additionally, imagine that there is an index in this object store named “recipient,” which represents the recipient address of a message, and now, the developer would like to support multiple recipients for messaging. Then, it would be nice to have this index renamed as “recipient**s**” (plural).

```
let request = indexedDB.open("messageDB", 2);
request.<strong>onupgradeneeded</strong> = (event) => {
let txn = event.target.transaction;
let store = txn.objectStore("text messages");
store.<strong>name</strong> = "mobile messages";
let index = store.index("recipient");
index.<strong>name</strong> = "recipient<strong>s</strong>";
};
```


`IDBDatabase.onclose()`


A new `onclose`

event handler is defined in the `IDBDatabase`

interface to allow the developer to listen to the storage change of the indexedDB outside the scripts. Taking the Firefox browser as an example, the browser allows the user to [clean up the storage used by a single site](https://support.mozilla.org/en-US/kb/delete-browsing-search-download-history-firefox#w_how-do-i-remove-a-single-website-from-my-history). With this handler, scripts can be notified that the database was closed forcibly outside the scripts to provide more responsive information or as a warning to the user.

```
let request = indexedDB.open("bookstore");
request.onsuccess = (event) => {
let db = event.target.result;
db.<strong>onclose</strong> = (event) => {
alert("the database: " + db.name + "was closed outside the script!");
};
};
```


## Binary Key Indexing

Binary data types can be treated as indexed keys in the 2.0 implementation. More precisely, any properties of the stored object presented by [Arraybuffer](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/ArrayBuffer), [typed array objects](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/TypedArray), and [DataView](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/DataView) can now be indexed. This benefits developers: now you can have binary signatures as keys directly, without serializing them into strings or array objects as required by the previous API version.

`IDBTransaction.objectStoreNames[]`


This handy new property gives developers an easier way to determine which object stores are involved in the current transaction:

```
let request = indexedDB.open("bookstore", 2);
request.<strong>onupgradeneeded</strong> = (event) => {
let txn = event.target.transaction; // txn.mode == "versionchange"
txn.<strong>objectStoreNames</strong>; // a list of objectstore names can be accessed in this txn.
};
```


`IDBObjectStore.getKey(query)`


`getKey(query)`

is now provided in `IDBObjectStore`

for performance reasons and the symmetry with `IDBIndex`

. With this new API, you don’t have to adopt heuristics to check if an object key in a specific range is available in the store. For example, `openCursor(query)`

might be an alternative approach, but you’ll still have the overhead cost of cursor creation and the serialization/deserialization of the object.

Let’s assume that there is an object store for the logging of the network activities and the timestamps are chosen as the object keys. Now, we’d like to know when the first activity occurred in the last 24 hours:

```
let openRequest = indexedDB.open("telemetry");
openRequest.onsuccess = (event) => {
let db = event.target.result;
let store = db.transaction("netlogs").objectStore("netlogs");
let today = new Date();
let yesterday = new Date(today);
yesterday.setDate(today.getDate() - 1);
let request = store.<strong>getKey</strong>(IDBKeyRange(yesterday, today));
request.onsuccess = (event) => {
let when = event.target.result;
alert("The 1st activity in last 24 hours was occurred at " + when);
};
};
```


`IDBObjectStore.openKeyCursor(range, direction)`


As a lightweight version of `openCursor()`

in `IDBObjectStore`

, `openKeyCursor()`

allows you to iterate object keys in a specified range without retrieving the entire object from the database. This reduces the overhead of serialization.

Let’s continue the previous example to retrieve the timestamps of the network activities that occurred in the last 24 hours:

```
let openRequest = indexedDB.open("telemetry");
openRequest.onsuccess = (event) => {
let db = event.target.result;
let store = db.transaction("netlogs").objectStore("netlogs");
let today = new Date();
let yesterday = new Date(today);
yesterday.setDate(today.getDate() - 1);
let request = store.<strong>openKeyCursor</strong>(IDBKeyRange(yesterday, today));
let timestamps = [];
request.onsuccess = (event) => {
let cursor = event.target.result;
if (!cursor) { return; }
timestamps.push(cursor.<strong>key</strong>);
cursor.continue();
};
};
```


`getAll`

/`getAllKeys(range, count)`

from `IDBObjectStore`

and `IDBIndex`


Instead of retrieving data one by one by iterating the cursor, `getAll()`

and `getAllKeys()`

allow us to retrieve all the data at once in ascending order from an `IDBObjectStore`

or an `IDBIndex`

. You can specify optional `range`

and `count`

to limit the number of results in the response. It’s very useful when the total size of data to be retrieved is not huge.

For example, if you would like to retrieve the first ten activities in the last 24 hours at once:

```
let openRequest = indexedDB.open("telemetry");
openRequest.onsuccess = (event) => {
let db = event.target.result;
let store = db.transaction("netlogs").objectStore("netlogs");
let today = new Date();
let yesterday = new Date(today);
yesterday.setDate(today.getDate() - 1);
let activities = null;
let request = store.<strong>getAll</strong>(IDBKeyRange(yesterday, today), <strong>10</strong>);
request.onsuccess = (event) => {
activities = event.target.result;
};
};
```


Note: This is less useful if you want to retrieve data at once in *descending order* when *count* is specified.

`IDBCursor.continuePrimaryKey(key, primaryKey)`


In the design of IndexedDB, records in an IDBIndex tree are stored in ascending order of the index key followed by ascending order of the object key. With the help of `continuePrimaryKey()`

to an opened `IDBCursor`

of an `IDBIndex`

, developers can immediately resume the iteration of a cursor that was closed in a previous iteration. You simply specify the index key and primary key recorded previously, instead of starting the iteration from the beginning and comparing the primary keys one by one.

For example, here’s how you can resume an iteration of all articles tagged with “**javascript**” since your last visit:

`let request = articleStore.index("tag").openCursor(); let count = 0; let unreadList = []; request.onsuccess = (event) => { let cursor = event.target.result; if (!cursor) { return; } let lastPrimaryKey = <code>getLastIteratedArticleId()`

; if (lastPrimaryKey > cursor.primaryKey) { cursor.continuePrimaryKey("javascript",lastPrimaryKey); return; } // update lastIteratedArticleId`setLastIteratedArticleId`

(cursor.primaryKey); // preload 5 articles into the unread list; unreadList.push(cursor.value); if (++count < 5) { cursor.continue(); } };

`IDBKeyRange.includes(key)`


This is a new helper function to check if a key is in the scope of an `IDBKeyRange`

:

```
let openRange = IDBKeyRange.bound(5, 10, true, true);
openRange.<strong>includes</strong>(5); // false;
openRange.<strong>includes</strong>(10); // false;
openRange.<strong>includes</strong>(7); // true;
```


With the 2.0 changes and updates, it’s possible to accomplish entirely new things with [IndexedDB](https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API). See where these new capabilities take you and let us know how it goes.

## About Bevis Tseng

Bevis Tseng is a platform engineer at Mozilla who used to work on telephony-related features in Firefox OS (B2G). He has completed the enhancement of IndexedDB in Gecko for Spec v2 recently and now is involving in the task labeling for Quantum-DOM scheduler.