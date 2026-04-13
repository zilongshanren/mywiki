---
title: Coroutines Look Like Factories
url: http://hacksoflife.blogspot.com/2021/06/coroutines-look-like-factories.html
author: Benjamin Supnik
published: '2021-06-18'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

This is part two of a five part series on

[coroutines]in C++.

In my previous post I complained about the naming of the various parts of coroutines - the language design is great, but I find myself having to squint at the parts sometimes.

Before proceeding, a basic insight about how coroutines work in C++.

You write a coroutine like a function (or method or lambda), but the world uses it like a factory that returns a handle to your newly created coroutine.

One of the simplest coroutine types I was able to write was an immediately-running, immediately-returning coroutine that returns nothing to the caller - something like this:

class async {

public:

struct control_block {

auto initial_suspend() { return suspend_never(); }

auto final_suspend() { return suspend_never(); }

void return_void() {}

void unhandled_exception() { }

};

using promise_type = control_block;

};


The return type "async" returns a really useless handle to the client. It's useless because the coroutine starts on its own and ends on its own - it's "fire and forget". The idea is to let you do stuff like this:

async fetch_file(string url, string path)

{

string raw_data = co_await http::download_url(url);

co_await disk::write_file_to_path(path, raw_data);

}


In this example, our coroutine suspends on IO twice, first to get data from the internet, then to write it to a disk, and then it's done. Client code can do this:

void get_files(vector<pair<string,string>> stuff)

{

for(auto spec : stuff)

{

fetch_file(spec.first,spec.second);

}

}

To the client code, fetch_file is a "factory" that will create one coroutine for each file we want to get; that coroutine will start executing using the caller for get_files, do enough work to start downloading, and then return. We'll queue a bunch of network ops in a row.

How does the coroutine finish? The IO systems will resume our coroutine once data is provided. What thread is executing this code? I have no idea - that's up to the IO system's design. But it will happen after "fetch_file" is done.

Is this code terrible? So first, yes - I would say an API to do an operation with no way to see what happened is bad.

But if legacy code is callback based, this pattern can be quite useful - code that launches callbacks typically put the finalization of their operation *in the callback* and do nothing once launching the callback - the function is fire and forget because the end of the coroutine or callback handles the results of the operation.

## No comments:

## Post a Comment