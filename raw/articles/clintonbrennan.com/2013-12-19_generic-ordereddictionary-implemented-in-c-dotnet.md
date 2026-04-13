---
title: Generic OrderedDictionary implemented in C# DotNet
url: http://clintonbrennan.com/2013/12/generic-ordereddictionary-implemented-in-c-dotnet/
author: Clinton
published: '2013-12-19'
source_blog: Clinton Brennan
source_site: http://clintonbrennan.com
category: game programming
fetched: '2026-04-13'
---

The Dictionary class in .NET does not have a defined ordering when iterating through it. It can seem to maintain order until you start to remove objects from the collection. In order to maintain determinism, when ever we loop through a collection it needs to be in a deterministic order. There does already exist a [OrderedDictionary](http://msdn.microsoft.com/en-us/library/system.collections.specialized.ordereddictionary(v=vs.110).aspx), however there is not a Generic version.

This implementation uses two underlying collections. A Dictionary and a LinkedList. The Dictionary maintains a mapping from the Key to a LinkedListNode in the LinkedList. The LinkedList maintains a list of KeyValuePairs and keeps them in insertion order. A LinkedList is used instead of a List as it provides constant time removal (assuming you have a reference to a node).

private Dictionary<TKey, LinkedListNode<KeyValuePair<TKey, TValue>>> mDictionary; private LinkedList<KeyValuePair<TKey, TValue>> mLinkedList;

This implementation was inspired by the OrderedHashSet found at:

The source code can be found at: