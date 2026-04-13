---
title: Designing C APIs in 2016
url: https://anteru.net/blog/2016/designing-c-apis-in-2016
published: '2016-05-01'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

It’s 2016, and C APIs are as popular as always. Many libraries are written in C, or provide C APIs, and there are tons of bindings for any language making C the de-facto standard for portable APIs. Yet, a lot of C APIs fail basic design guidelines, and there doesn’t seem to have been much progress in recent years in the way we design those APIs. I’ve been working on a modern C API recently, and then there’s also Vulkan with a few fresh design ideas. High time we take a look at what options we have when designing a C based API in 2016!

## Design matters

API design matters a lot. I’ve written [about](https://anteru.net/blog/2008/09/08/264/) it before, and I still get to use a lot of APIs where I’d like to get onto a plane and have a serious chat with the author. Today we’re not going to talk about the basic issues, which are ABI compatibility, sane versioning, error handling and the like - instead we’ll look at ways you can expose the API to the client.

My assumption here is you’re designing an API which will live in a shared object/DLL. The basic approach to do this in C is to expose your API entry points directly. You just mark them as visible, decide on some naming scheme, and off you go. The client either links directly against your library, or loads the entry points manually, and calls them. This is practically how all C APIs have been designed so far. Look at sqlite, libpng, Win32, the Linux kernel - this is exactly the pattern.

## Current problems

So what are the problems with this approach? Well, there’s a couple:

- API versioning
- API loading
- Extensibility

Let’s tackle those one-by-one.

### API versioning

For any API, you’ll inevitably run into the issue that you’re going to update a function signature. If you care about API and ABI compatibility, that means you need to add a new entry point into your API - the classic reason we see so many `myFunctionEx`

or `myFunctionV2`

. There’s no way around this if you expose the entry points directly.

It also means you can’t remove an entry point. Client applications can solve that issue if you provide a way to query the API version, but then we’re going to run into the next problem - API loading.

In general, a direct C API has no really good way to solve this problem, as every version bump means either new entry points or more complicated loading. Adding a couple new entry points doesn’t sound like a big issue, but over time, you’ll accumulate lots of new versions and it’ll become unclear for developers which one to use.

### API loading

API loading covers the question how a user gets started with your API. Often enough, you just link directly against an import library, and then you expect a shared object or DLL exporting the same symbols. This makes it hard to dynamically use the library (i.e. if you want to use it only if needed.) Sure, you can do lazy loading tricks using the linker, but what if you don’t have the import library to start with? In this case, you’ll end up loading some kind of dispatch library which loads all entry points of your API. This is for instance what the OpenCL loader does, or GLEW. This way, your client is 100% isolated from the library, but it’s quite some boilerplate to write.

The solutions for this aim at reducing that boilerplate. GLEW generates all load functions from an XML description, OpenCL just mandates the clients expose a single entry point which fills out a dispatch table. Which brings us to the last topic, extensibility.

### Extensibility

How do you extend your API? That is, how can someone add something like a validation layer on top of it? For most C APIs, extensions mean just more entry point loading, but layering is completely ignored.

Vulkan explicitly attacks the layering problem. The solution they came up with allows layers to be chained, which is, layers call into underlying layers. To make this efficient, the chaining can skip several layers, so you don’t pay per layer loaded, just per layer that is actually handling an API call. Extensions are still handled using the normal way of querying more API entry points.

Vulkan also has a declarative API version stored in the vk.xml file, which contains all extensions, so they can generate the required function pointer definitions. This reduces the boilerplate a lot, but still requires users to query entry points - though it would be possible to autogenerate a full loader like GLEW does.

## Dispatch & generation focused APIs

Thinking about the issues above, I figured that ideally, what we want is:

- As few entry points as possible, ideally one. This solves the dynamic loading issue, and makes it easy to have one entry point per version.
- A way to group all functions for one version together. Switching a version would then result in compile-time errors.
- A way to layer a new set of functions on top of the original API - i.e. the possibility to replace individual entry points.

If you think C++ classes and COM, you’re not far off. Let’s take a look at the following approach to design an API:

- You expose a single entry point, which returns the dispatch table for your API directly.
- The dispatch table contains all entry points for your API.
- You require clients to pass in the dispatch table or some object pointing to the dispatch table to all entry points.

So how would such an API look like? Here’s an example:

```
struct ImgApi
{
int (*LoadPng) (ImgApi* api, const char* filename,
Image* handle);
int (*ReadPixels) (ImgApi* api, Image* handle,
void* target);
// or
int (*ReadPixels) (Image* handle, void* target);
// Various other entry points
};
// public entry points for V1_0
int CreateMyImgIOApiV1_0 (ImgApi** api);
int DestroyMyImgIOApiV1_0 (ImgApi* api);
```


Does this thing solve our issues? Let’s check:

- Few entry points - two. Yes, that works, for dynamic and static loading.
- All functions grouped - check! We can add a
`ImgApiV2`

without breaking older clients, and all changes become compile-time errors. - Layering - what do you know, also possible! We just instantiate a new
`ImgApi`

, and link it to the original one. In this case, the only difficulty arises from chaining through objects like`Image`

, for which we’ll need a way to query the dispatch table pointer from them.

Looks like we got a clear winner here - and indeed, I recently implemented a library using such an API design and the actual implementation is really simple. In particular if you use C++ lambdas, you can fill out a lot of the redirection functions in-line, which is very neat. So what are the downsides? Basically, the fact that you need to call through the dispatch table is the only one I see. This will yield one more indirection, and it’s a bit more typing.

Right now my thinking is that if you really need the utmost performance per-call, your API is probably too low-level to start with. Even then, you could still force clients to directly load that one entry point, or provide it from the dispatch table. The more typing issue is generally a non-issue: First of all, any kind of autocompletion will immediately identify what you’re doing, and if you really need to, you can auto-generate a C++ class very easily which inlines all forwarding and is simply derived from the dispatch table.

This is also where the generation part comes into play: I think for any API going forward, a declarative description, be it XML, JSON or something else, is a necessity. There’s so much you want to auto-generate for the sake of usability that you should be thinking about this from day one.

Right now, this design, combined with a way to generate the dispatch tables, looks to me like the way to go in 2016 and beyond. You get an easy to use API for clients, a lot of freedom to build things on top, while keeping all of the advantages of plain C APIs like portability.