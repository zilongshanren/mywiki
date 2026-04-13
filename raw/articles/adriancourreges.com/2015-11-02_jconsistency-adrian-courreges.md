---
title: JConsistency - Adrian Courrèges
url: http://www.adriancourreges.com/projects/jconsistency/
author: Adrian Courrèges
published: '2015-11-02'
source_blog: Adrian Courrèges
source_site: http://www.adriancourreges.com/
category: graphics
fetched: '2026-04-13'
---

![JConsistency logo](../../assets/6293be6f8ae0f41b.png)

**JConsistency is a middleware which allows concurrent access in read-mode or write-mode to Java objects shared by multiple JVMs over the network. **

It provides a layer of synchronization so many virtual machines can safely access concurrently different objects shared among them.
The system authorizes accesses in read-mode from multiple JVMs, however in write-mode only a single JVM is able to interact with the object.

### Download ![Download](../../assets/c044d82d1b7f4ef5.png)


### Description

JConsistency allows many JVMs to share objects in a distributed way. Before interacting with a shared object, a virtual machine will request a lock on it.

There are two types of lock possible:

**“read lock”**is used when the virtual machine only needs to access the object without modifying it.**“write lock”**is used when the virtual machine needs to perform operations that will alter some attribute values of the object.

The system uses a central server to handle the synchronization. All the JVMs connect to this server by RMI, they can then register a new shared object,
retrieve an existing one or request some lock.


*The part of the central server is only to guarantee the synchronization between the different JVMs and the gestion of the states of shared objects.
It never performs any operation on the object: the object (or its copy) is always transfered to the JVM so the virtual machine can interact with
it as a local object. *

Therefore the load on the server stays low, and the interaction with the objects is done locally without all the overhead of network communication.


The interface provides a generic class (SharedObject) which acts as a wrapper for any objects that need to be shared.

To avoid the hassle to extract the real object from its SharedObject at each serialization, a stub generator is also included so original methods can be directly called on the instance of the wrapper.

The system even allows you to define a shared object whose attributes are also shared objects.

### Example

Here is a simple example where we create an object, share it and request a write lock on it.

1 2 3 4 5 6 7 8 9 10 11 12 13 14 |
|

### Screenshots

Well, you should not expect anything eye-candy from a middleware. ;)

Here is the debug mode of a test session: 3 JVMs reading and modifying a SharedObject in parallel.

The bottom part represents the server log.

![LOGO Screenshot](../../assets/2af8cf6c22c5d7ae.png)