---
title: shorty.js - Short string compression for the web.
url: https://enkimute.github.io/shorty.js/
author: Enki's blog
published: '2017-04-04'
source_blog: Enki's blog – Math, Graphics, Programming.
source_site: https://enkimute.github.io/
category: graphics
fetched: '2026-04-19'
---

GIT

![view on github](../../assets/cb9f317b98c6b74a.png)

# shorty.js - Short string compression for the web.

Compress your JSON data streams without buffering. Achieve zlib compression levels while retaining the ability to send frequent short messages.

## Get Shorty !

![](../../assets/a2be49be15e5bf24.jpg)


3919 bytes - [https://enkimute.github.io/res/shorty.min.js](https://enkimute.github.io/res/shorty.min.js)

## What is Shorty ?

You are sending a lot of JSON packages between your users, and many of them are similar, say your ship’s position, or chat messages, etc ..

They’re plain text and you feel they should therefor compress easily. However, they’re also very short and standard zlib inflate/deflate doesn’t perform to well on short input sequences. You could start buffering, but in many cases that would defeat the purpose of still sending the data.

That’s where shorty.js comes in. It implements the adaptive huffman algorithm with a tokenizer that’s been tweaked to perform well on JSON strings. As a result, you can get (almost) zlib compression rate’s without any buffering.

## How good is Shorty ?

On a stream of 100 random state update messages of the following form :

```
{"position":[0.6730729561370266,0.673753677417668],"playerName":"player0"}
{"position":[0.7435747657098075,0.8756806480717665],"playerName":"player0"}
{"position":[0.7180175092507983,0.4312792536217358],"playerName":"player0"}
...
```


We measured the output size of shorty, zlib per packet, and zlib but with all the data buffered. Here are the results :

| compression | size | ratio |
|---|---|---|
| uncompressed | 7552 | 100% |
| zlib deflate per packet | 7095 | 94% |
| shorty per packet | 2508 | 33% |
| zlib delayed entire stream | 2136 | 28% |

## Using Shorty

Using Shorty is extremely easy, there’s just two function calls (inflate and deflate) - and no configuration options.

Everytime you ask Shorty to deflate or inflate data it will update its internal tree, making tokens that occur more often occupy less bits. These updates happen continuously making Shorty adapt to the data you are sending.

Keep in mind that you’ll need two shorty’s for a bidirectional connection!

### compress

```
var shorty_out = new Shorty();
...
function send_compressed(data) {
send(shorty_out.deflate(data));
}
```


### decompress

```
var shorty_in = new Shorty();
...
function receive_data(data) {
data = shorty_in.inflate(data);
}
```


## Try it !

| input | compressed | output |
|---|---|---|
| total: | total: | total: |


Leave a comment if you use it !