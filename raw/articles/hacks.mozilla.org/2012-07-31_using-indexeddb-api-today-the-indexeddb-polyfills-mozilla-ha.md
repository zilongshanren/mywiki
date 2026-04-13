---
title: Using IndexedDB API today – the IndexedDB polyfills – Mozilla Hacks - the Web
  developer blog
url: https://hacks.mozilla.org/2012/07/using-indexeddb-api-today-the-indexeddb-polyfills/
author: Parashuram Narasimhan
published: '2012-07-31'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*This is a guest post from Parashuram Narasimhan on how to use IndexedDB today.*

Using the polyfills mentioned in this article, web developers can start using IndexedDB APIs in their applications and support a wider range of browsers.

The [IndexedDB API](http://www.w3.org/TR/IndexedDB/) has matured into a stable specification with support by major browser vendors. However, the specification is still [not supported in all browsers](http://caniuse.com/#search=IndexedDB), making it harder to use in production. There are also some interesting differences in the implementations among browsers that support the specification. This article explores a couple of polyfills that could be leveraged to enable developers to use IndexedDB across different browsers.

## Polyfill using WebSql

[WebSql](http://www.w3.org/TR/webdatabase/) was one of the first specifications for data storage in the browsers and is supported in some browsers that do not have an implementation of IndexeddB yet. However, the specification is no longer in active maintenance. As mentioned in the document: “it was on the W3C Recommendation track but specification work has stopped. The specification reached an impasse: all interested implementors have used the same SQL backend (Sqlite), but we need multiple independent implementations to proceed along a standardisation path”.

This [polyfill using WebSql](http://axemclion.github.com/IndexedDBShim) utilizes the WebSQL implementations to expose the IndexedDB APIs. To use the polyfill, simply link or include the [indexeddb.shim.js](http://axemclion.github.com/IndexedDBShim/dist/IndexedDBShim.min.js) file.

The polyfill assigns window.indexedDB to be window.mozIndexedDB, window.webkitIndexedDB or window.msIndexedDB; if any of those implementations are available. If no implementation is available, the polyfill assigns a ‘window.shimIndexedDB’ to window.indexedDB. Web applications can thus start using window.indexedDB as the starting point for all database operations. Internally, the polyfill uses the WebSql tables to store object store data and borrows heavily from the IndexedDB implementation in Firefox. For example, it has separate tables and databases to maintain a record of the database versions, or the values for object store definitions (IDBObjectStoreParameters). More implementation details about the internals can be found in [the blog post on it](http://blog.nparashuram.com/2012/06/indexeddb-polyfill-under-covers.html).

The polyfill has been tested to work with various IndexedDB libraries like [PouchDB](http://pouchdb.com/), [LINQ2IndexedDB](http://linq2indexeddb.codeplex.com/), [JQuery-IndexedDB](http://nparashuram.com/jquery-indexeddb) and [DB.JS](http://aaronpowell.github.com/db.js/). Since it leverages WebSql, applications can write code according to the IndexedDB API on web browsers like Opera and Safari, and additionally on mobile browsers like Safari on iPad/iPhone, or mobile development platforms like [Cordova](http://incubator.apache.org/cordova/) that have WebSql enabled browsers embedded in them.

It is implemented in Javascript and is a work in progress. Note that it may not fully confirm to the specification and you discover issues, you could [file a bug](https://github.com/axemclion/IndexedDBShim/issues) or send a pull request to the [source repository](https://github.com/axemclion/IndexedDBShim).

## Polyfill for setVersion

An earlier version of the IndexedDB Specification used the “setVersion” call to change the version of the IndexedDB Database. This was later revised to an easier to use “onupgradeneeded” callback. Though Internet Explorer and Firefox support the newer “onupgradeneeded” to initiate database version changes for creating or deleting objectStores and Indexes, Google Chrome (22.0.1194.0 canary) still uses the older setVersion.

All browsers will soon use the newer “onupgradeneded” method soon; till then, this simple [polyfill for setVersion](https://gist.github.com/2656808) lets you use the IndexedDB API with the onupgradeneeded method.

The polyfill substitutes the indexeddb.open() call with an openReqShim() call. The openReqShim() call invokes setVersion() and then converts it to the “onupgradeneeded” callback if only “setVersion()” is supported. If the implementation supports the “onupgradeneeded”, openReqShim() is simply a transparent call to the indexedb.open method. Hence, indexeddb.open() calls should be replaced with the openReqShim() call to use this polyfill.

## About Parashuram Narasimhan

Parashuram Narasimhan is a Programmer at Sneekpeeq. Before Sneakpeeq, he was a senior program manager for SQLCE at Microsoft, working on the IndexedDB implementation and specifications. He has written the Jquery IndexedDB plugin, a query layer for IndexedDB and is working on a WebSql shim for IndexedDB. He also like playing with latest HTML features in the web and their security implications. During his free time, he hacks at http://nparashuram.com/projects and posts the results at http://blog.nparashuram. He is also a "huge" fan of Mozilla Firefox and has been using it as his primary browser from version 1.

## 8 comments

Josh MatthewsJuly 31st, 2012 at 13:59Robert NymanJuly 31st, 2012 at 14:13kristof degraveJuly 31st, 2012 at 23:23Robert NymanAugust 1st, 2012 at 00:52Ido GreenAugust 1st, 2012 at 12:13ParashuramAugust 2nd, 2012 at 15:00C. Scott AnanianOctober 16th, 2012 at 15:53Robert NymanOctober 16th, 2012 at 22:37