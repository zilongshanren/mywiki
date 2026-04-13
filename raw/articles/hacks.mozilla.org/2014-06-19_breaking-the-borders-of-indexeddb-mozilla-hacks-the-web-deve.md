---
title: Breaking the Borders of IndexedDB – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2014/06/breaking-the-borders-of-indexeddb/
author: David Fahlander
published: '2014-06-19'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

In this article I want to share with you how to do some cool IndexedDB queries that aren’t ‘possible’ out of the box unless you add some ‘tricks’.

The algorithms I’m going to show, except the ‘full-text-search’ one, were invented by me while I was writing on the open source javascript library [Dexie.js](https://github.com/dfahlander/Dexie.js/wiki/Dexie.js). Some of them are not unique inventions since other people have discovered them too, but I believe that the *case insensitive search* algorithm, at least, is unique for my [Dexie.js](https://github.com/dfahlander/Dexie.js/wiki/Dexie.js) library.

All code snippets in this article are conceptual. In case you need to look at bullet proof code, I encourage you to dive into the source of [Dexie.js](https://github.com/dfahlander/Dexie.js/wiki/Dexie.js) where all of these algorithms are implemented and thoroughly unit tested.

## The Four IndexedDB Queries

IndexedDB API is only capable of doing four type of queries:

- IDBKeyRange.only (Exact match)
- IDBKeyRange.upperBound () – Find objects where property X is below certain value
- IDBKeyRange.lowerBound () – Find objects where property X is above certain value
- IDBKeyRange.bound() – Find objects where property X is between certain values.

## What I Will Show

I am going to show you how to extend IndexedDB to support the following:

- anyOf()
- Find objects where property X equals any of a given set of possible values
- equalsIgnoreCase()
- Case insensitive search
- startsWith()
- Find strings starting with a certain prefix
- startsWithIgnoreCase()
- Find strings starting with case insensitive prefix
- or()
- Combine two queries and get the union of these two.
- full-text-search
- Find objects by searching for words contained in a large text

The list could be much longer than that, but let’s start with these for now.

None of these extended types of queries, except *full-text-search* require you to store any meta-data. They will work with any IndexedDB database already being used. For example, you do not have to store lowercase versions of strings that you need to do case insensitive matching on.

So lets start showing the ‘tricks’ that breaks the borders of IndexedDB.

## anyOf()

In SQL, this is equal to the IN keyword:

`SELECT * FROM table WHERE X IN (a,b,c)`

The reason I begin with this one, is that it pretty straight forward and simple to understand. Understanding this one will make it easier to understand the algorithms for doing case insensitive search.

### Some Background Knowledge

Let’s start by diving into some IndexedDB basics:

To iterate ALL records in a table with IndexedDB, you call indexOrStore.openCursor() on the IDBObjectStore or IDBIndex instance. For each record, you’ll get called back on your `onsuccess`

callback:

```
// Start a transaction to operate on your 'friends' table
var trans = db.transaction(["friends"], "readonly");
// Get the 'name' index from your 'friends' table.
var index = trans.objectStore("friends").index("name");
// Start iteration by opening a cursor
var cursorReq = index.openCursor();
// When any record is found, you get notified in onsuccess
cursorReq.onsuccess = function (e) {
var cursor = e.target.result;
if (cursor) {
// We have a record in cursor.value
console.log(JSON.stringify(cursor.value));
cursor.continue();
} else {
// Iteration complete
}
};
```

### Overloaded Version of IDBCursor.continue()

In the sample above, we call cursor.continue() without any argument. This will make the cursor advance to next key. But if we provide an argument to cursor.continue(nextKey), we tell the cursor to fast-forward to given key. If we were iterating the “name” index and wrote:

`cursor.continue("David");`

…the next `onsuccess`

would have a cursor positioned at the first record where name equals “David” if that key exists. **The specification requires that the cursor must be positioned at the first record that is equal to or greater than the specified key in the same sort order as the index.**

### The Algorithm

So lets say we have a huge database of friends and *friends of friends* with various names. Now we want to find all friends that have any of the following names: “David”, “Daniel” or “Zlatan”.

We are going to do a cursor based iteration on the ‘name’ index as shown above, and use cursor.continue(nextName) to fast forward to the names we are looking for. When opening a cursor on an index, the order of found items will be in the sort order of that index. So if we do it on the ‘name’ index, we will get all friends in the sort order of their ‘name’.

What we want to do first, is to sort() the array of names we are looking for, so we get the following JavaScript array:

`["Daniel", "David", "Zlatan"]`

(since n comes before v). Then we do the following:

- call
`cursor.continue("Daniel")`

(first item in sorted set) `onsuccess`

: Check if`cursor.key == "Daniel"`

. If so, include`cursor.value`

in result and call`cursor.continue()`

without arguments to check for more Daniels.- When no more Daniels found, call
`cursor.continue("David")`

(next item…) `onsuccess`

: Check if`cursor.key == "David"`

. If so, include cursor.value in result and call`cursor.continue()`

without arguments to check for more Davids.- When no more Davids found, call
`cursor.continue("Zlatan")`

`onsuccess`

: Check if`cursor.key == "Zlatan"`

. If so, include`cursor.value`

in result and call`cursor.continue()`

without arguments to check for more Zlatans. Else, we could stop iterating by just don’t call`cursor.continue()`

anymore because we know we wont find any more results (The set was sorted!)

### Sample Implementation of the Algorithm

```
function comparer (a,b) {
return a < b ? -1 : a > b ? 1 : 0;
}
function equalsAnyOf(index, keysToFind, onfound, onfinish) {
var set = keysToFind.sort(comparer);
var i = 0;
var cursorReq = index.openCursor();
cursorReq.onsuccess = function (event) {
var cursor = event.target.result;
if (!cursor) { onfinish(); return; }
var key = cursor.key;
while (key > set[i]) {
// The cursor has passed beyond this key. Check next.
++i;
if (i === set.length) {
// There is no next. Stop searching.
onfinish();
return;
}
}
if (key === set[i]) {
// The current cursor value should be included and we should continue
// a single step in case next item has the same key or possibly our
// next key in set.
onfound(cursor.value);
cursor.continue();
} else {
// cursor.key not yet at set[i]. Forward cursor to the next key to hunt for.
cursor.continue(set[i]);
}
};
}
```

## Case Insensitive Search

Dexie.js implements case insensitive searching using a similar IDBCursor.continue(key) method as with the *anyOf()* algorithm above, however a little more complexity in the algorithm is needed.

Let’s say we need to find “david” in table “friends” no matter its casing. “David” or “david” should both be found. Obviously, we could create an array containing all possible case combinations of “david” and then use the *anyOf()* algorithm above. However, the number of combinations would increase exponentially with the length of the key we’re looking for. But there is a trick we can use; since cursor.continue() will land on the next record in sort order, that will reveal what combinations we can skip when landing on the key that is not a match.

What we do is to start searching for the lowest possible value of “David”, which would be “DAVID” since uppercase unicode characters have a lesser value than their corresponding lowercase version. If there is no “DAVID” in the DB, we will land on the least possible key yet greater than “DAVID”. Now, instead of testing the next combination of davids (which would be “DAVId”), we first inspect the key we landed on and from that key, we derive what would be the next “david” variant to search for. Look at the function *nextCasing()* in the code snippet below to see how we derive next possible version of a key based on the key that the IDBCursor landed on. I will not go through it line-by line here, but instead, I refer to the code comments in **function nextCasing(key, lowerKey) {…}** below.

```
function findIgnoreCaseAlgorithm(index, needle, onfound, onfinish) {
// index: An instance of IDBIndex
// needle: The string to search for
// onfound: A function to call for each found item
// onfinish: A function to call when we're finshed searching.
var upperNeedle = needle.toUpperCase();
var lowerNeedle = needle.toLowerCase();
var cursorReq = index.openCursor();
cursorReq.onsuccess = function (event) {
var cursor = event.target.result;
if (!cursor) {
// No more data to iterate over - call onfinish()
onfinish();
return;
}
var key = cursor.key;
if (typeof key !== 'string') {
// Just in case we stumble on data that isnt what we expect -
// toLowerCase() wont work on this object. Check next.
cursor.continue();
return;
}
var lowerKey = key.toLowerCase();
if (lowerKey === lowerNeedle) {
onfound(cursor.value); // Notify caller we found somethin
cursor.continue(); // Check next record, it might match too!
} else {
// Derive least possible casing to appear after key in sort order
var nextNeedle = nextCasing(key, lowerKey, upperNeedle, lowerNeedle);
if (nextNeedle) {
cursor.continue(nextNeedle);
} else {
// No more possible case combinations to look for.
// Call onfinish() and dont call cursor.continue() anymore.
onfinish();
}
}
};
function nextCasing(key, lowerKey) {
var length = Math.min(key.length, lowerNeedle.length); // lowerNeedle is from outer scope
var llp = -1; // "llp = least lowerable position"
// Iterate through the most common first chars for cursor.key and needle.
for (var i = 0; i < length; ++i) {
var lwrKeyChar = lowerKey[i];
if (lwrKeyChar !== lowerNeedle[i]) {
// The char at position i differs between the found key and needle being
// looked for when just doing case insensitive match.
// Now check how they differ and how to trace next casing from this:
if (key[i] < upperNeedle[i]) {
// We could just append the UPPER version of the key we're looking for
// since found key is less than that.
return key.substr(0, i) + upperNeedle[i] + upperNeedle.substr(i + 1);
}
if (key[i] < lowerNeedle[i]) {
// Found key is between lower and upper version. Lets first append a
// lowercase char and the rest as uppercase.
return key.substr(0, i) + lowerNeedle[i] + upperNeedle.substr(i + 1);
}
if (llp >= 0) {
// Found key is beyond this key. Need to rewind to last lowerable
// position and return key + 1 lowercase char + uppercase rest.
return key.substr(0, llp) + lowerKey[llp] + upperNeedle.substr(llp + 1)
}
// There are no lowerable positions - all chars are already lowercase
// (or non-lowerable chars such as space, periods etc)
return null;
}
if (key[i] < lwrKeyChar) {
// Making lowercase of this char would make it appear after key.
// Therefore set llp = i.
llp = i;
}
// All first common chars of found key and the key we're looking for are equal
// when ignoring case.
if (length < lowerNeedle.length) {
// key was shorter than needle, meaning that we may look for key + UPPERCASE
// version of the rest of needle.
return key + upperNeedle.substr(key.length);
}
// Found key was longer than the key we're looking for
if (llp < 0) {
// ...and there is no way to make key we're looking for appear after found key.
return null;
} else {
// There is a position of a char, that if we make that char lowercase,
// needle will become greater than found key.
return key.substr(0, llp) + lowerNeedle[llp] + upperNeedle.substr(llp + 1);
}
}
}
```

### Performance

In a performance test I created 10,000 objects with random strings and let the equalsIgnoreCase() algorithm try to find items in it. For Opera, it took between 4 and 5 milliseconds to find 6 matching items among 10,000. For Mozilla latest version, it took 7 ms. If instead iterating through all 10,000 items and comparing manually, it took 1514 ms for Mozilla and 346 ms for Opera.

## startsWith(str)

Matching prefix of string keys is the most straight-forward trick you can do with IndexedDB. It's not unique for Dexie.js as other libraries support it as well. However, for the sake of completeness, here is how it is done: Just do an IDBKeyRange.bound() where lowerBound is the prefix and upperBound is a string that would include all possible continuations of the prefix. The simplest way to do this is just to append a character with highest possible value; '\uffff'.

`IDBKeyRange.bound(prefix, prefix + 'uffff', false, false)`

## startsWithIgnoreCase(str)

When the matched string should be compared without case sensitivity, we need to do a cursor search, as for equalsIgnoreCase(). We can actually take the same algorithm but change how we compare each entry. Instead of comparing using the '==' operator, we use String.indexOf(). This will give us the value 0 if the string starts with given value. So, just copy the code samples from equalsIgnoreCase() above and change the `onsuccess`

part to the following:

```
cursorReq.onsuccess = function (event) {
var cursor = event.target.result;
if (!cursor) {
// No more data to iterate over - call onfinish()
onfinish();
return;
}
var key = cursor.key;
if (typeof key !== 'string') {
// Just in case we stumble on data that isnt what we expect -
// toLowerCase() wont work on this object. Check next.
cursor.continue();
return;
}
var lowerKey = key.toLowerCase();
if (lowerKey.indexOf(lowerNeedle) === 0) {
onfound(cursor.value); // Notify caller we found somethin
cursor.continue(); // Check next record, it might match too!
} else {
// Derive least possible casing to appear after key in sort order
var nextNeedle = nextCasing(key, lowerKey, upperNeedle, lowerNeedle);
if (nextNeedle) {
cursor.continue(nextNeedle);
} else {
// No more possible case combinations to look for.
// Call onfinish() and dont call cursor.continue() anymore.
onfinish();
}
}
};
```

## Logical OR

IndexedDB has no support for logical or. You can only specify one keyrange at a time. However, what it does have support for, is to run several queries in parallel - even when using same transaction (as long as the queries are readonly queries). Even if the queries wouldn't run in parallel, it would still work but a little less performant. The OR operation in [Dexie.js](https://github.com/dfahlander/Dexie.js/wiki/Dexie.js) has been unit tested with Chrome, IE, Firefox and Opera.

The only thing we need to do except executing both queries in parallel, is to remove any duplicates. To do that, we can use a set of found primary keys. Whenever a new record match is found on any of the parallel queries, it first checks the set if it's already included. If not, it calls onfound for the entry and sets set[primKey] = true so that if the same entry would be found on the other query, it would silently ignore to call onfound().

Here's how it's done. The code snipped below is a simplified version only supporting the logical OR of two standard IDBKeyRange queries. With Dexie, you can do arbritary number of OR with any standard or extended operation such as equalsIgnoreCase().

```
function logical_or(index1, keyRange1, index2, keyRange2, onfound, onfinish) {
var openCursorRequest1 = index1.openCursor(keyRange1);
var openCursorRequest2 = index2.openCursor(keyRange2);
assert(index1.objectStore === index2.objectStore); // OR can only be done on same store
var primKey = index1.objectStore.keyPath;
var set = {};
var resolved = 0;
function complete() {
if (++resolved === 2) onfinish();
}
function union(item) {
var key = JSON.stringify(item[primKey]);
if (!set.hasOwnProperty(key)) {
set[key] = true;
onfound(item);
}
}
openCursorRequest1.onsuccess = function (event) {
var cursor = event.target.result;
if (cursor) {
union(cursor.value);
} else {
complete();
}
}
openCursorRequest2.onsuccess = function (event) {
var cursor = event.target.result;
if (cursor) {
union(cursor.value);
} else {
complete();
}
}
}
```

To access this algorithm with [Dexie.js](https://github.com/dfahlander/Dexie.js/wiki/Dexie.js), you type something like the following:

`db.friends.where('name').equalsIgnoreCase('david').or('shoeSize').above(40).toArray(fn)`

... which would make given callback function (fn) be called with an array of the results.

When using parallel OR execution, the sort order will not be valid. Partly because the two different queries execute on different indexes with different sort order, but mainly because the two queries run in parallel by the browser background threads and we cannot know which `onsuccess`

is called before the other. However, this can be resolved by implementing `onfound`

to push the items to an array, and `onfinish`

to sort it using any requested sort order:

```
var index1 = transaction.objectStore("friends").index("name");
var index2 = transaction.objectStire("friends").index("shoeSize");
var keyRange1 = IDBKeyRange.bound ("Da", "Dauffff");
var keyRange2 = IDBKeyRange.lowerBound (40, true);
//
// SELECT * FROM friends WHERE name LIKE 'Da%' OR shoeSize > 40 ORDERBY shoeSize;
//
var result = [];
logical_or (index1, keyRange1, index2, keyRange2, function (friend) {
result.push(friend);
}, function () {
result.sort (function (a,b) { return a.shoeSize - b.shoeSize; });
});
```

## Full Text Search

Searching for certain words in a large string (text field) is another common use case that is not supported out-of-the-box by IndexedDB. However, it can be easily implemented by splitting the text into words and store the resulting set in a 'multiEntry' index. With all my other algorithms in this article, no meta-data is required to make them work, but with Full Text Search, it must be prepared by adding a specific multiEntry index and each time a text is changed, the multiEntry index must be updated accordingly with the resulting set of words in the text.

- When defining your schema, create an index "words" with multiEntry set to true.
- In bare-bone IndexedDB:
`store.createIndex("words", "words", { multiEntry: true });`

- In Dexie.js: Prefix with asterisk (*):
`db.version(1).stores({blogs: '++id,title,text,*words'});`


- In bare-bone IndexedDB:
- Whenever you update your text, split the text into words and store all unique words in the "words" property of the object.
var blogEntry = new BlogEntry( "Blogging about IndexedDB", "Much to say about IndexedDB there is... bla bla bla - hope I'm not boring you..."); db.put(blogEntry); blogEntry.setText("...changing my blog post to another IndexedDB text..."); db.put(blogEntry); function BlogEntry(title, words) { ... this.setText = function (value) { this.text = value; this.words = getAllWords(value); } function getAllWords(text) { var allWordsIncludingDups = text.split(' '); var wordSet = allWordsIncludingDups.reduce(function (prev, current) { prev[current] = true; return prev; }, {}); return Object.keys(wordSet); } }

- To find an item by searching for a word, use the "words" index to launch the query on.
- bare-bone IndexedDB:
`index.openCursor(IDBKeyRange.only('IndexedDB'));`

- Dexie.js:
`db.blogs.where('words').equalsIgnoreCase('indexeddb')`


- bare-bone IndexedDB:

An example of how to do this with Dexie follows in the [FullTextSearch.js file in Dexie](https://github.com/dfahlander/Dexie.js/blob/master/samples/full-text-search/FullTextSearch.js)

## Live Samples

If you want to play with the samples in your browser or phone, go to [Samples on the Dexie.js wiki](https://github.com/dfahlander/Dexie.js/wiki/Samples) where you have these samples and some more to experiment with.

## A Last Word

Whether you are just curious about the IndexedDB API, or you're implementing your own IndexedDB library, I hope the techniques shown in this article could be useful for you when you need to maximize the posibilities with IndexedDB.

I would also like to encourage you to have a look at [Dexie.js](https://github.com/dfahlander/Dexie.js/wiki/Dexie.js) to discover how it may help you achieve your goals. A lot of effort has been put to make this library well documented and tested. The library is still young but the few users that has discovered it so far, have expressed a great deal of enthusiasm in the [Dexie.js forum](https://groups.google.com/forum/#!forum/dexiejs).

## About
[
David Fahlander ](https://dfahlander.medium.com)

Ex Commodore 64 hacker ([triad](http://www.triad.se/members/daw)) and nowadays Javascript fan. Developer at [Awarica AB](http://www.awarica.com). Author of [Dexie.js](https://github.com/dfahlander/Dexie.js/wiki/Dexie.js) - an open source wrapper library for IndexedDB.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 3 comments

Doug ReederJune 19th, 2014 at 10:55JoeJune 22nd, 2014 at 13:00chrisJune 24th, 2014 at 11:52