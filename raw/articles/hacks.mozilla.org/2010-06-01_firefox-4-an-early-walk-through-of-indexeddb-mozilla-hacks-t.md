---
title: 'Firefox 4: An early walk-through of IndexedDB – Mozilla Hacks - the Web developer
  blog'
url: https://hacks.mozilla.org/2010/06/comparing-indexeddb-and-webdatabase/
author: Arun Ranganathan
published: '2010-06-01'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Web developers already have [localStorage](https://developer.mozilla.org/en/DOM/Storage), which is used for client side storage of simple key-value pairs. This alone doesn’t address the needs of many web applications for structured storage and indexed data. Mozilla is working on a structured storage API with indexing support called [IndexedDB](http://dev.w3.org/2006/webapi/IndexedDB/), and we will have some test builds in the next few weeks. This can be compared to the [WebDatabase API](http://dev.w3.org/html5/webdatabase/) implemented by several browsers that uses a subset of the allowable language of [SQLite](http://www.sqlite.org/). Mozilla has chosen to not implement WebDatabase for [various reasons discussed in this post](http://hacks.mozilla.org/2010/06/beyond-html5-database-apis-and-the-road-to-indexeddb).

In order to compare IndexedDB and WebDatabase, we are going to show four examples that use most parts of the asynchronous APIs of each specification. The differences between SQL storage with tables (WebDatabase) and JavaScript object storage with indexes (IndexedDB) becomes pretty clear after reading the examples. The synchronous versions of these APIs are only available on worker threads. Since not all browsers currently implement worker threads, the synchronous APIs will not be discussed at this time. The IndexedDB code is based off a [proposal that Mozilla has submitted to the W3C WebApps working group](http://lists.w3.org/Archives/Public/public-webapps/2010AprJun/0717.html) that has gotten positive feedback so far. The code for both APIs does not include any error handling (for brevity), but production code should always have it!

These examples are for the storage of a candy store’s sale of candy to customers, which we’ll refer to as kids. Each entry in `candySales`

represents a sale of a specified amount of candy to a kid, specified by an entry in `candy`

and `kids`

respectively.

### Example 1 – Opening and Setting Up a Database

This first example demonstrates how to open a database connection and create the tables or object stores if the version number is not correct. Upon opening the database, both examples check the version and create the necessary tables or object stores and then set the correct version number. WebDatabase is a bit stricter in how it handles versions by giving an error if the database version is not what the caller expects (this is specified by the second argument to openDatabase). IndexedDB simply lets the caller handle versioning as they see fit. Note that there is [active discussion about how IndexedDB should handle version changes](http://lists.w3.org/Archives/Public/public-webapps/2010AprJun/thread.html#msg611) in the working group.

**WebDatabase**

```
var db = window.openDatabase("CandyDB", "",
"My candy store database",
1024);
if (db.version != "1") {
db.changeVersion(db.version, "1", function(tx) {
// User's first visit. Initialize database.
var tables = [
{ name: "kids", columns: ["id INTEGER PRIMARY KEY",
"name TEXT"]},
{ name: "candy", columns: ["id INTEGER PRIMARY KEY",
"name TEXT"]},
{ name: "candySales", columns: ["kidId INTEGER",
"candyId INTEGER",
"date TEXT"]}
];
for (var index = 0; index < tables.length; index++) {
var table = tables[index];
tx.executeSql("CREATE TABLE " + table.name + "(" +
table.columns.join(", ") + ");");
}
}, null, function() { loadData(db); });
}
else {
// User has been here before, no initialization required.
loadData(db);
}
```

**IndexedDB**

```
var request = window.indexedDB.open("CandyDB",
"My candy store database");
request.onsuccess = function(event) {
var db = event.result;
if (db.version != "1") {
// User's first visit, initialize database.
var createdObjectStoreCount = 0;
var objectStores = [
{ name: "kids", keyPath: "id", autoIncrement: true },
{ name: "candy", keyPath: "id", autoIncrement: true },
{ name: "candySales", keyPath: "", autoIncrement: true }
];
function objectStoreCreated(event) {
if (++createdObjectStoreCount == objectStores.length) {
db.setVersion("1").onsuccess = function(event) {
loadData(db);
};
}
}
for (var index = 0; index < objectStores.length; index++) {
var params = objectStores[index];
request = db.createObjectStore(params.name, params.keyPath,
params.autoIncrement);
request.onsuccess = objectStoreCreated;
}
}
else {
// User has been here before, no initialization required.
loadData(db);
}
};
```

### Example 2 – Storing Kids in the Database

This example stores several kids into the appropriate table or object store. This example demonstrates one of the risks that have to be dealt with when using WebDatabase: SQL injection attacks. In WebDatabase explicit transactions must be used, but in IndexedDB a transaction is provided automatically if only one object store is accessed. Transaction locking is per-object store in IndexedDB. Additionally, IndexedDB takes a JavaScript object to insert, whereas with WebDatabase callers must bind specific columns. In both cases you get the insertion id in the callback.

**WebDatabase**

```
var kids = [
{ name: "Anna" },
{ name: "Betty" },
{ name: "Christine" }
];
var db = window.openDatabase("CandyDB", "1",
"My candy store database",
1024);
db.transaction(function(tx) {
for (var index = 0; index < kids.length; index++) {
var kid = kids[index];
tx.executeSql("INSERT INTO kids (name) VALUES (:name);", [kid],
function(tx, results) {
document.getElementById("display").textContent =
"Saved record for " + kid.name +
" with id " + results.insertId;
});
}
});
```

**IndexedDB**

```
var kids = [
{ name: "Anna" },
{ name: "Betty" },
{ name: "Christine" }
];
var request = window.indexedDB.open("CandyDB",
"My candy store database");
request.onsuccess = function(event) {
var objectStore = event.result.objectStore("kids");
for (var index = 0; index < kids.length; index++) {
var kid = kids[index];
objectStore.add(kid).onsuccess = function(event) {
document.getElementById("display").textContent =
"Saved record for " + kid.name + " with id " + event.result;
};
}
};
```

### Example 3 – List All Kids

This example lists all of the kids stored in the `kids`

table or the `kids`

object store. WebDatabase uses a result set object which will be passed to the callback method provided after all rows have been retrieved. IndexedDB, on the other hand, passes a cursor to the event handler as results are retrieved. Results should come back faster, as a result. While not shown in this example, you can also stop iterating data with IndexedDB by simply not calling `cursor.continue()`

.

**WebDatabase**

```
var db = window.openDatabase("CandyDB", "1",
"My candy store database",
1024);
db.readTransaction(function(tx) {
// Enumerate the entire table.
tx.executeSql("SELECT * FROM kids", function(tx, results) {
var rows = results.rows;
for (var index = 0; index < rows.length; index++) {
var item = rows.item(index);
var element = document.createElement("div");
element.textContent = item.name;
document.getElementById("kidList").appendChild(element);
}
});
});
```

**IndexedDB**

```
var request = window.indexedDB.open("CandyDB",
"My candy store database");
request.onsuccess = function(event) {
// Enumerate the entire object store.
request = event.result.objectStore("kids").openCursor();
request.onsuccess = function(event) {
var cursor = event.result;
// If cursor is null then we've completed the enumeration.
if (!cursor) {
return;
}
var element = document.createElement("div");
element.textContent = cursor.value.name;
document.getElementById("kidList").appendChild(element);
cursor.continue();
};
};
```

### Example 4 – List Kids Who Bought Candy

This example lists all the kids, and how much candy each kid purchased. WebDatabase simply uses a LEFT JOIN query which makes this example very simple. IndexedDB does not currently have an API specified for doing a join between different object stores. As a result, the example opens a cursor to the `kids`

object store and an object cursor on the `kidId`

index on the `candySales`

object store and performs the join manually.

**WebDatabase**

```
var db = window.openDatabase("CandyDB", "1",
"My candy store database",
1024);
db.readTransaction(function(tx) {
tx.executeSql("SELECT name, COUNT(candySales.kidId) " +
"FROM kids " +
"LEFT JOIN candySales " +
"ON kids.id = candySales.kidId " +
"GROUP BY kids.id;",
function(tx, results) {
var display = document.getElementById("purchaseList");
var rows = results.rows;
for (var index = 0; index < rows.length; index++) {
var item = rows.item(index);
display.textContent += ", " + item.name + "bought " +
item.count + "pieces";
}
});
});
```

**IndexedDB**

```
candyEaters = [];
function displayCandyEaters(event) {
var display = document.getElementById("purchaseList");
for (var i in candyEaters) {
display.textContent += ", " + candyEaters[i].name + "bought " +
candyEaters[i].count + "pieces";
}
};
var request = window.indexedDB.open("CandyDB",
"My candy store database");
request.onsuccess = function(event) {
var db = event.result;
var transaction = db.transaction(["kids", "candySales"]);
transaction.oncomplete = displayCandyEaters;
var kidCursor;
var saleCursor;
var salesLoaded = false;
var count;
var kidsStore = transaction.objectStore("kids");
kidsStore.openCursor().onsuccess = function(event) {
kidCursor = event.result;
count = 0;
attemptWalk();
}
var salesStore = transaction.objectStore("candySales");
var kidIndex = salesStore.index("kidId");
kidIndex.openObjectCursor().onsuccess = function(event) {
saleCursor = event.result;
salesLoaded = true;
attemptWalk();
}
function attemptWalk() {
if (!kidCursor || !salesLoaded)
return;
if (saleCursor && kidCursor.value.id == saleCursor.kidId) {
count++;
saleCursor.continue();
}
else {
candyEaters.push({ name: kidCursor.value.name, count: count });
kidCursor.continue();
}
}
}
```

IndexedDB generally simplifies the programming model for interacting with databases, and allows for a wide number of use cases. The working group is designing this API so it could be wrapped by JavaScript libraries; for instance, there's plenty of room for a CouchDB-style API on top of our IndexedDB implementation. It would also be very possible to build a SQL-based API on top of IndexedDB (such as WebDatabase). Mozilla is eager to get developer feedback about IndexedDB, particularly since the specification has not been finalized yet. Feel free to leave a comment here expressing your thoughts or [leave anonymous feedback through Rypple](https://rypple.com/sdwilsh/IndexedDB-feedback).

## 182 comments

HurfDurfJune 1st, 2010 at 12:30Shawn WilsherJune 1st, 2010 at 13:25AndyJune 1st, 2010 at 14:35Shawn WilsherJune 1st, 2010 at 20:13EgeAugust 26th, 2010 at 07:18Jesper KristensenJune 1st, 2010 at 13:44Preston L. BannisterJune 2nd, 2010 at 13:51Wes BrownJune 1st, 2010 at 14:00Shawn WilsherJune 1st, 2010 at 14:19voracityJune 2nd, 2010 at 07:29Tom HarrisonAugust 19th, 2010 at 12:24ArtifexDecember 1st, 2010 at 14:34George MoschovitisJune 1st, 2010 at 14:40Shawn WilsherJune 1st, 2010 at 14:53JohnJune 1st, 2010 at 15:26Shawn WilsherJune 1st, 2010 at 16:26Laurens HolstJune 1st, 2010 at 15:27goldfrapperJune 2nd, 2010 at 01:19Shawn WilsherJune 2nd, 2010 at 09:55ScrewtapeJune 1st, 2010 at 16:55Shawn WilsherJune 1st, 2010 at 17:01ScrewtapeJune 1st, 2010 at 19:54Shawn WilsherJune 1st, 2010 at 20:18ScrewtapeJune 1st, 2010 at 22:41gedOctober 21st, 2010 at 12:32Music TeacherJune 1st, 2010 at 16:59Jonas SickingJune 1st, 2010 at 18:48DavidJune 1st, 2010 at 18:53Shawn WilsherJune 1st, 2010 at 20:26Tom HarrisonAugust 19th, 2010 at 12:36Mark RendleJune 2nd, 2010 at 01:44alexJune 2nd, 2010 at 22:0529aJune 3rd, 2010 at 08:37DarrenJune 4th, 2010 at 11:00Shawn WilsherJune 7th, 2010 at 10:16Darren GovoniJune 7th, 2010 at 10:33Shawn WilsherJune 7th, 2010 at 10:42MewpJune 4th, 2010 at 13:46Shawn WilsherJune 7th, 2010 at 10:27MartinJune 7th, 2010 at 03:52Shawn WilsherJune 7th, 2010 at 10:32Darren GovoniJune 7th, 2010 at 11:26Rob ArnoldJune 7th, 2010 at 12:03austinJune 10th, 2010 at 09:24Darren GovoniJune 11th, 2010 at 04:53Rob ArnoldJune 11th, 2010 at 10:33Brett ZamirJune 17th, 2010 at 19:55Steve AntalJune 17th, 2010 at 20:42Brett ZamirJune 17th, 2010 at 19:58Brett ZamirJune 17th, 2010 at 21:03Andrzej LisJune 21st, 2010 at 11:34Andrzej LisJune 22nd, 2010 at 09:51Brett ZamirJune 23rd, 2010 at 03:30Brett ZamirJune 23rd, 2010 at 03:41Evan IrelandJune 27th, 2010 at 14:24Evan IrelandJune 27th, 2010 at 14:50Shawn WilsherJune 30th, 2010 at 09:21Shawn WilsherJune 30th, 2010 at 09:22Brazilian JoeJuly 5th, 2010 at 14:45Jeffry EngertJuly 9th, 2010 at 23:16Shawn WilsherJuly 10th, 2010 at 23:29Michal GieldaJuly 14th, 2010 at 04:25Michal GieldaJuly 14th, 2010 at 04:27Shawn WilsherJuly 19th, 2010 at 12:05AnentropicJuly 17th, 2010 at 05:45Shawn WilsherJuly 19th, 2010 at 12:10DanielJuly 20th, 2010 at 07:30AnentropicJuly 21st, 2010 at 16:24Shawn WilsherJuly 21st, 2010 at 16:43AnentropicJuly 22nd, 2010 at 02:15AnentropicJuly 22nd, 2010 at 02:23Shawn WilsherJuly 22nd, 2010 at 11:01Shawn WilsherJuly 22nd, 2010 at 11:05AnentropicJuly 26th, 2010 at 10:54TKJuly 21st, 2010 at 23:48Shawn WilsherJuly 22nd, 2010 at 10:58TKJuly 22nd, 2010 at 12:15Shawn WilsherJuly 22nd, 2010 at 12:34TKJuly 22nd, 2010 at 23:50TKSeptember 9th, 2010 at 06:39Shawn WilsherSeptember 9th, 2010 at 10:50TKSeptember 16th, 2010 at 01:12TKSeptember 19th, 2010 at 19:53TKJuly 28th, 2010 at 12:32Shawn WilsherJuly 28th, 2010 at 13:05Guido TapiaJuly 29th, 2010 at 16:58TKJuly 30th, 2010 at 03:31FrankJuly 30th, 2010 at 08:42TKJuly 30th, 2010 at 12:01TKAugust 12th, 2010 at 05:41Shawn WilsherAugust 12th, 2010 at 10:23TKAugust 12th, 2010 at 11:24Shawn WilsherAugust 12th, 2010 at 11:40TKAugust 13th, 2010 at 10:08TKAugust 13th, 2010 at 10:13TKAugust 24th, 2010 at 17:54SriAugust 4th, 2010 at 00:57Michal GieldaAugust 4th, 2010 at 01:43Dwight VietzkeAugust 8th, 2010 at 20:53Shawn WilsherAugust 10th, 2010 at 07:09gregSeptember 2nd, 2010 at 13:41Christopher BlizzardSeptember 9th, 2010 at 10:09Morn JaonAugust 11th, 2010 at 18:00Shawn WilsherAugust 12th, 2010 at 10:21Morn JaonAugust 12th, 2010 at 22:13Shawn WilsherAugust 13th, 2010 at 14:13Morn JaonAugust 15th, 2010 at 05:35TKAugust 13th, 2010 at 13:24Shawn WilsherAugust 13th, 2010 at 14:14PeteAugust 24th, 2010 at 09:17MeniSeptember 19th, 2010 at 00:53Greg QuinnSeptember 19th, 2010 at 19:58EmmanuelSeptember 20th, 2010 at 14:01JoshuaBlnSeptember 23rd, 2010 at 01:37MattNovember 1st, 2010 at 20:01Joe ShawfieldNovember 4th, 2010 at 03:13MornDecember 6th, 2010 at 01:48ChadDecember 11th, 2010 at 17:04Jesse MorganDecember 12th, 2010 at 04:02PaulDecember 27th, 2010 at 22:29ChrisJune 2nd, 2011 at 14:52ChrisAugust 29th, 2011 at 02:28Clay LenhartJanuary 4th, 2011 at 15:32JohnJanuary 14th, 2011 at 08:20PaulJanuary 15th, 2011 at 09:32Shawn WilsherJanuary 18th, 2011 at 15:10satishJanuary 29th, 2013 at 07:06codeguru413February 1st, 2011 at 10:06RafalFebruary 14th, 2011 at 00:57RafalFebruary 14th, 2011 at 14:18Ben DiltsMarch 2nd, 2011 at 00:09rayMarch 7th, 2011 at 21:46PaulMarch 7th, 2011 at 22:46Mike WilsonMarch 21st, 2011 at 21:56Christopher BlizzardMarch 22nd, 2011 at 09:58GregMarch 22nd, 2011 at 10:13Shawn WilsherMarch 22nd, 2011 at 10:19Marcelo CantosMarch 23rd, 2011 at 04:15John SmithApril 4th, 2011 at 22:03DanJune 13th, 2011 at 08:16Jesse MorganApril 7th, 2011 at 17:41PaulApril 8th, 2011 at 17:31Jesse MorganApril 11th, 2011 at 18:36Jesse MorganApril 11th, 2011 at 18:42PaulApril 23rd, 2011 at 09:09Jesse MorganApril 23rd, 2011 at 17:03Jesse MorganApril 11th, 2011 at 18:59ShibyMay 24th, 2011 at 02:08louisremiMay 24th, 2011 at 05:45ShibyMay 24th, 2011 at 22:30Bill HartenJune 27th, 2011 at 13:15PaulJune 30th, 2011 at 04:09Bill HartenSeptember 8th, 2011 at 08:31Robert BrownSeptember 15th, 2011 at 14:07devlimJuly 20th, 2011 at 10:18MichaelSeptember 1st, 2011 at 06:43Robert BrownSeptember 15th, 2011 at 14:08Ken CoreySeptember 6th, 2011 at 13:23Leigh HarrisonSeptember 20th, 2011 at 01:49PaulSeptember 21st, 2011 at 12:45DanielSeptember 21st, 2011 at 13:10Marcelo CantosOctober 22nd, 2011 at 08:11DanielOctober 24th, 2011 at 09:15Marcelo CantosOctober 24th, 2011 at 14:46MikeOctober 22nd, 2011 at 12:23ShibyOctober 25th, 2011 at 04:51FikreApril 14th, 2012 at 20:53StanOctober 16th, 2012 at 06:07KurtDecember 11th, 2012 at 10:28Robert NymanDecember 11th, 2012 at 12:33KurtDecember 12th, 2012 at 12:56JimPMarch 6th, 2013 at 19:32Anthony CaudillMarch 9th, 2013 at 15:08Daniel BuchnerMarch 9th, 2013 at 15:52Anthony CaudillMarch 9th, 2013 at 20:50Anthony CaudillMarch 9th, 2013 at 21:36DGMarch 10th, 2013 at 17:06GregMarch 11th, 2013 at 06:20