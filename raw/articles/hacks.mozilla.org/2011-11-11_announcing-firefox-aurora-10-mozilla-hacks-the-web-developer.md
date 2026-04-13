---
title: Announcing Firefox Aurora 10 – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2011/11/announcing-firefox-aurora-10/
author: Joe Stagner
published: '2011-11-11'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

We’re happy to announce the availability of Aurora 10.

([Download and Test Aurora 10](http://www.mozilla.org/en-US/firefox/channel/))

In additional to the normal improvements that you’ve come to expect like performance, security and bug fixes, Aurora 10 focuses in HTML5 enhancements.

## New additions

[HTML5 Visibility API](https://developer.mozilla.org/en/DOM/Using_the_Page_Visibility_API)[createProcessingInstruction](https://developer.mozilla.org/en/DOM/document.createProcessingInstruction)- WebGL antialiasing
- 3D Transforms
- Visibility API
- Document.mozFullScreenEnabled

## Developer Tools

Aurora 10 also implements incremental enhancements like IndexedDB setVersion API changes. Ongoing detailed attention to evolving specifications help to keep Firefox at the front of the Web revolution. (Read more about [IndexedDB on MDN](https://developer.mozilla.org/en/IndexedDB/IndexedDB_primer).)

## DOM

- We now fire a “load” event on stylesheet linking when the sheet load finishes or “error” if the load fails.
- We turn the POSTDATA prompt into an information page (when navigating in session history).
- We only forward event attributes on body/frameset to the window if we also forward the corresponding on* property.
- We no longer allow more than one call to window.open() when we allow popups.
- We fixed a bug where a success callback never fired when a position update is triggered after getCurrentPosition().
- We removed replaceWholeText().
- We fixed an error with createPattern(zero-size canvas).
- We now handle putImageData(nonfinite) correctly.
- We now throw INVALID_STATE_ERR when dispatching uninitialized events.
- We’ve made Document.documentURI readonly.
- We fixed document.importNode to comply with optional argument omitted.

## Web workers

- We now allow data URLs.
- We implemented event.stopImmediatePropagation in workers.
- We made XHR2 response/responseType work in Web Workers.

## Graphics

- We implement the WebGL OES_standard_derivatives extension.
- We implement minimal-capabilities WebGL mode.

## JavaScript

- The function caller property no longer skips over eval frames.
- We fixed E4X syntax so that it is not accepted in ES5 strict mode.
- weakmap.set no longer returns itself instead of undefined.
- We implemented the battery API.

## Offline: IndexedDB enhancements

- IndexedDB setVersion API changes
- Added support for IDBObjectStore/IDBIndex.count
- Various methods accept both keys and KeyRanges.
- Added support for IDBCursor.advance.
- Implemented deleteDatabase.
- objectStoreNames are no longer updated on closed databases when another connection adds or removes object stores
- IDBObjectStore.delete and IDBCursor.delete now return undefined.
- No longer throws an error if there are unknown properties in the options objects to createObjectStore/createIndex.
- We now the errorCode to “ABORT_ERR” for all pending requests when IDBTransaction.abort() is called.
- Fixed the sort order for indexes.

## Layout

- We have updated the current rule for handling malformed media queries.
- We now support the HTML5 <bdi> element and CSS property unicode-bidi: isolate.
- The CSS3 implementation now supports unicode-bidi: plaintext.

## Media

- Implemented Document.mozFullScreenEnabled.
- Enabled the DOM full-screen API on desktop Firefox by default.

## 19 comments

Caspy7November 11th, 2011 at 23:48redpandaNovember 12th, 2011 at 00:06A.I.November 12th, 2011 at 03:43Benoit JacobNovember 12th, 2011 at 09:24pdNovember 12th, 2011 at 22:20thinsoldierNovember 12th, 2011 at 11:24Benoit JacobNovember 12th, 2011 at 11:29Ken SaundersNovember 12th, 2011 at 18:26pdNovember 12th, 2011 at 22:21Kevin DangoorNovember 12th, 2011 at 21:52JerryNovember 13th, 2011 at 09:05Ken SaundersNovember 13th, 2011 at 12:17JasonNovember 14th, 2011 at 10:34Kevin DangoorNovember 14th, 2011 at 11:03JasonNovember 14th, 2011 at 11:43ReneNovember 16th, 2011 at 05:24JasonNovember 16th, 2011 at 10:18ReneNovember 16th, 2011 at 10:36ReneNovember 16th, 2011 at 10:37