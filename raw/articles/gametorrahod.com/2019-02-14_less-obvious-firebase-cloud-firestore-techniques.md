---
title: Less obvious Firebase Cloud Firestore techniques
url: https://gametorrahod.com/less-obvious-firebase-cloud-firestore-techniques/
author: Sirawat Pitaksarit
published: '2019-02-14'
source_blog: Game Torrahod
source_site: https://gametorrahod.com/
category: game programming
fetched: '2026-04-13'
---

I have been using the recently GA (generally available) Cloud Firestore via REST API from Unity. I want to collect something that is not at the forefront or in documentation, that I think **if I had known this **it would change my database design and planning early.

## Field Transforms

Things like “request server timestamp”, “array append”, and “array remove” are field transforms. So you do not either creating a new document or writing something new to the document. You **ask them to change.**

You don’t need to know the content in them but it will change according to their own content, that’s what make it called “transform”.

**Write | Firebase***DynamicLinkItunesConnectAnalyticsParameters*firebase.google.com

- On any of your timestamp field if you set “request server timestamp” sentinel value, it will be replaced with server time on write. Easily understandable.
- Array append ask any array field to be added some elements. The catch is that duplicate element will not be added (but Firestore array could contains duplicate elements). This is great for function like add friends. You don’t need to do something like get all your friends -> add one new friends -> overwrite all of them back. Just use this field transform.
- Array remove is the same but remove what’s there. If you remove something that is not in the array, nothing happen!
- You notice increment maximum and minimum too. It could come in handy to your design. maximum ‘s use is for example to update highscore. You can write the score regardless if it is lower or higher than server value and field transform should take care of that.

## What else can I do in Firestore rules?

You have probably went through this already. You know about future value, existing data value, creating functions, and validating auth.

**Writing conditions for Cloud Firestore Security Rules | Firebase***The primary building block of Cloud Firestore Security Rules is the condition. A condition is a boolean expression that…*firebase.google.com

But wait, from this page data you use in the rule is a Map

**Interface: Resource | Firebase***DynamicLinkItunesConnectAnalyticsParameters*firebase.google.com

What is a Map ? Other than the dot notation you used to access your fields there are more things to play with.

**Interface: Map | Firebase***DynamicLinkItunesConnectAnalyticsParameters*firebase.google.com

### Map

- keys is a List of keys.
- size . You could then check if size is something you are expecting.
- values would be a List of data you used the dot notation to access, but they are in List instead.
- x in y this operator can check existence of a
**key**in your map. (cool!)

What can you do with a List ?

**Interface: List | Firebase***DynamicLinkItunesConnectAnalyticsParameters*firebase.google.com

### List

- hasAll hasAny hasOnly you can give it an another List to compare and returns a boolean. I think this could be very good in designing rules.
- join returns new List , then maybe you could use has__ again.
- size
- x in y also available in list, but checks for
**value’s existence**instead of key.

### hasAll fails when there is no list

On the data I am going to write I am writing [1,2,3] to the field named nums . I asked if the future value of nums should contains the old nums array at least (So if the old nums is currently [1,3] that write is valid), so I used hasAll .

However hasAll does not work when I don’ have anums field yet and intended to create new from this update operation.

## To check for field’s existence

### Incorrect

```
allow update : if addedAsRival in resource.data == false;
allow update : if "addedAsRival" in resource.data == false;
```


== false need a parentheses because otherwise it would apply to resource.data .

The Map in check is checking for string key, so the thing in front of in need a string quotation.

### Correct

```
allow update : if ("addedAsRival" in resource.data) == false;
allow update : if !("addedAsRival" in resource.data);
```


This rule would allow you to add rival only once where there are no rivals before. This is the complete rule for example :

![](../../assets/8faf866374b3f928.png)

I am using a scheme where you add yourself to other player’s “added as rival” list. This rule ensure that you can only add yourself whether the target has this field before or not. (It looks hideous but I don’t know how I could make it better while retaining the same intent)

## Getting a subset of document

Multiple times throughout learning material it said that the smallest unit you can request is a document. But in REST API it is possible for server to returns only fields you want from one document via DocumentMask .

**Method: projects.databases.documents.get | Firebase***DynamicLinkItunesConnectAnalyticsParameters*firebase.google.com

I don’t know if this exists in other API or not. But it could suggest that eventually you will be able to do it. So, no need to fear “private fields leaking” if you keep them in the same document, just use mask in your request and the returned document will be as if those fields does not exist.

(I saw the official Firestore video suggesting doing sub-document containing private data, so that getting public data document will not returns private data as the query is shallow.)

## Avoiding PATCH header in Android

One thing about Android is that they could not do PATCH header.

**Patch Request Android Volley***Thanks for contributing an answer to Stack Overflow! Please be sure to answer the question. Provide details and share…*stackoverflow.com

But all PATCH-based Rest API could be replaced with write , which uses POST header. Also with write you have a choice to do field transforms.

**Method: projects.databases.documents.write | Firebase***DynamicLinkItunesConnectAnalyticsParameters*firebase.google.com

## Map field is auto-indexed for only 1 level

Just in case you missed it, in here

**Index types in Cloud Firestore | Firebase***A single-field index stores a sorted mapping of all the documents in a collection that contain a specific field. Each…*firebase.google.com

For each map field, Cloud Firestore creates one ascending index and one descending index for each non-array and non-map subfield in the map.