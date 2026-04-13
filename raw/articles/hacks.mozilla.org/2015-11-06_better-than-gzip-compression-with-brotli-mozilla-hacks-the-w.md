---
title: Better than Gzip Compression with Brotli – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2015/11/better-than-gzip-compression-with-brotli/
author: Mozilla
published: '2015-11-06'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

## HTTP Compression

Brotli is an open source data compression library [formally specified by IETF draft](https://tools.ietf.org/html/draft-alakuijala-brotli-07). It can be used to compress HTTPS responses sent to a browser, in place of gzip or deflate.

Support for Brotli content encoding has [recently landed](https://bugzilla.mozilla.org/show_bug.cgi?id=366559) and is now testable in Firefox Developer Edition (Firefox 44). In this post, we’ll show you an example of how to set up a simple HTTPS server that takes advantage of Brotli when supported by the client.

When serving content over the web, an easy win or low hanging fruit is turning on server side compression. Somewhat unintuitive, doing extra work to compress an HTTP response server side, and decompress the result client side is faster than not doing the additional work. This is due to bandwidth constraints over the wire. Adding compression improves transfer times when the content is large, isn’t already compressed (reapplying compression doesn’t buy you anything, unless you’re [Pied Piper](http://www.piedpiper.com/)), and the cost to communicate is relatively large.

The way the User Agent, client, or Web browser signals to the server what kinds of compressed content it can decompress is with the `Accept-Encoding` header. Let’s see what such a header might look like in Firefox 43 (prior to Brotli support) [dev tools](https://developer.mozilla.org/en-US/docs/Tools/Network_Monitor#Headers).

And in Firefox 44 (with Brotli support)![Accept-Encoding FF 41](../../assets/1717da9c1c8f2dee.png)


Just because the client supports these encodings doesn’t mean that’s what they’ll get. It’s up to the server to decide which encoding to choose. The server might not even support any form of compression.

The server then responds with the `Content-Encoding` header specifying what form of compression was used, if any at all.

While the client sends a list of encodings it supports, the server picks one to respond with. Responding with an unsupported content encoding, or with a header that doesn’t match the actual encoding of the content can lead to decompression errors and the summoning of Z͈͈̩͔̹͙͂͆ͨ̂͒́̌͋ͩ͑̄̔̏́̕ͅĄ̸̢̤͚̜̰̺̉͗̂͋̈͋̏̎̌ͬ͊̾͟L̵͈̠̯͙̠̩͚̰̖̬̩̂̐͐̐̇͑ͥͩ̇͐̄̇̀̕͡G̵̡͋̄͛̈́̓҉̶͉̳̮̣́Ő̐̈̀͐̅ͦ̔͊̽́̅̏͏̦̫̹̖̯͕̙̝̹̳͕͢͜.

Most browsers support gzip and deflate (as well as uncompressed content, of course). Gecko based browsers such as Firefox 44+ now support “br” for brotli. Opera beta 33 has support for lzma (note: lzma1 not lzma2) and sdch. [Here](https://code.google.com/p/chromium/issues/detail?id=472009)‘s the relevant Chromium bug for brotli support.

## Creating Our Server

Here’s a simple Node.js server that responds with [5 paragraphs of generated Lorem Ipsum text](http://lipsum.com/feed/html). Note: you’ll need Node.js installed, I’m using Node v0.12.7. You’ll need a C++ compiler installed for installing the native addons I’m using:

npm install accepts iltorb lzma-native

Finally, you’ll need to generate some TLS certificates to hack on this since Firefox 44+ supports Brotli compression over HTTPS, but not HTTP. If you’re following along at home, and aren’t seeing Accept-Encoding: “br”, make sure you’re connecting over HTTPS.

You can follow the tutorial [here](https://nodejs.org/api/tls.html#tls_tls_ssl) for generating self-signed certs. Note that you’ll need openssl installed, and that browsers will throw up warnings since you’re newly generated certificate is not recognized by [them or their trusted Certificate Authorities](https://wiki.mozilla.org/CA:IncludedCAs). These warnings can be safely ignored when developing locally with certificates you generated yourself that you trust, but don’t go around ignoring certificate errors when browsing the web.

Here’s the code for our simple server.

```
#!/usr/bin/env node
var accepts = require('accepts');
var fs = require('fs');
var https = require('https');
var brotli = require('iltorb').compressStream;
var lzma = require('lzma-native').createStream.bind(null, 'aloneEncoder');
var gzip = require('zlib').createGzip;
var filename = 'lorem_ipsum.txt';
function onRequest (req, res) {
res.setHeader('Content-Type', 'text/html');
var encodings = new Set(accepts(req).encodings());
if (encodings.has('br')) {
res.setHeader('Content-Encoding', 'br');
fs.createReadStream(filename).pipe(brotli()).pipe(res);
} else if (encodings.has('lzma')) {
res.setHeader('Content-Encoding', 'lzma');
fs.createReadStream(filename).pipe(lzma()).pipe(res);
} else if (encodings.has('gzip')) {
res.setHeader('Content-Encoding', 'gzip');
fs.createReadStream(filename).pipe(gzip()).pipe(res);
} else {
fs.createReadStream(filename).pipe(res);
}
};
var certs = {
key: fs.readFileSync('./https-key.pem'),
cert: fs.readFileSync('./https-cert.pem'),
};
https.createServer(certs, onRequest).listen(3000);
```


Then we can navigate to https://localhost:3000 in our browser. Let’s see what happens when I visit the server in various browsers.

Firefox 45 uses Brotli:

Safari 9 and Firefox 41 use gzip:![Opera 33 lzma](../../assets/305e081e94f9ee89.png)


We can compare the size of the asset before and after compression using Firefox Developer Tools, under the network tab, by comparing the Transferred vs Size columns. The transferred column shows the bytes of the compressed content transferred over the wire, and the size column shows the asset’s decompressed size. For content sent without any form of compression, these two should be the same.

We can also verify using the curl command line utility:

```
$ curl https://localhost:3000 --insecure -H 'Accept-Encoding: br' -w '%{size_download}' -so /dev/null
1333
$ curl https://localhost:3000 --insecure -H 'Accept-Encoding: lzma' -w '%{size_download}' -so /dev/null
1502
$ curl https://localhost:3000 --insecure -H 'Accept-Encoding: gzip' -w '%{size_download}' -so /dev/null
1408
$ curl https://localhost:3000 --insecure -w '%{size_download}' -so /dev/null
3484
```


## Notes about compression vs performance

The choice of which compression scheme to use does have implications. Node.js ships with zlib, but including native node add-ons for lzma and brotli will slightly increase distribution size. The time it takes the various compression engines to run can vary wildly, and the memory usage while compressing content can hit physical limits when servering numerous requests.

In the previous example, you might have noticed that lzma did not beat gzip in compression out of the box, and brotli did only maginally. You should note that all compression engines have numerous configuration options that can be tweaked to trade off things like performance for memory usage, amongst other things. Measuring the change in response time, memory usage, and Weissman score is something we’ll take a look at next.

The following numbers were gathered from running

```
$ /usr/bin/time -l node server.js &
$ wrk -c 100 -t 6 -d 30s -H 'Accept-Encoding: <either br lzma gzip or none>' https://localhost:3000
$ fg
ctrl-c
```


The following measurements were taken on the following machine: Early 2013 Apple MacBook Pro OSX 10.10.5 16GB 1600 MHz DDR3 2.7 GHz Core i7 4-Core with HyperThreading.

| Compression Method | Requests/Second | Bytes Transferred (MB/s) | Max RSS (MB) | Avg. Latency (ms) |
|---|---|---|---|---|
| br-stream | 203 | 0.25 | 3485.54 | 462.57 |
| lzma | 233 | 0.37 | 330.29 | 407.71 |
| gzip | 2276 | 3.44 | 204.29 | 41.86 |
| none | 4061 | 14.06 | 125.1 | 23.45 |
| br-static | 4087 | 5.85 | 105.58 | 23.3 |

Some things to note looking at the numbers:

- There’s a performance cliff for requests/second for compression other than gzip.
- There’s significantly more memory usage for compression streams. The
~~9.8 GB~~3.4 GB peak RSS for brotli looks like a memory leak that’s[been reported upstream](https://github.com/MayhemYDG/iltorb/issues/3)(my monocle popped out when I saw that). - The latency measured is only from localhost which would be at least this high across the Internet, probably much more. This is the
[waiting timing under Dev Tools > Network > Timings](https://developer.mozilla.org/en-US/docs/Tools/Network_Monitor#Timings). - If we compress static assets ahead of time using brotli built from source, we get fantastic results. Note: we can only do this trick for static responses.
- Serving statically-brotli-compressed responses performs as well as serving static uncompressed assets, while using slightly less memory. This makes sense, since there are fewer bytes to transfer! The lower number of bytes transferred per second makes that variable seem independent of the number of bytes in the file to transfer.

For compressing static assets ahead of time, we can build brotli [from source](https://github.com/google/brotli/blob/master/tools/Makefile), then run:

```
$ ./bro --input lorem_ipsum.txt --output lorem_ipsum.txt.br
```


and modify our server:

```
4d3
< var brotli = require('iltorb').compressStream;
8c7
< var filename = 'lorem_ipsum.txt'; --- > var filename = 'lorem_ipsum.txt.br';
17c16
< fs.createReadStream(filename).pipe(brotli()).pipe(res); --- > fs.createReadStream(filename).pipe(res);
```


## BREACH

Like other HTTP compression mechanisms, using Brotli with HTTPS can make you vulnerable to [BREACH attacks](http://breachattack.com/). If you want to use it, you should apply [other BREACH mitigations](http://breachattack.com/#mitigations).

## Conclusion

For 5 paragraphs of lorem ipsum, Brotli beats gzip by 5%. If I run the same experiment with the front page of reddit.com from 10/01/2015, Brotli beats gzip by 22%! Note that both measurements were using the compressors out of the box without any tweaking of configuration values.

Whether or not a significant portion of your userbase is using a browser that supports Brotli as a content encoding, whether the added latency and memory costs are worth it, and whether your HTTPS server or CDN support Brotli is another story. But if you’re looking for better than gzip performance, Brotli looks like a possible contender.

## 6 comments

Dan CallahanNovember 6th, 2015 at 10:48Nick DesaulniersNovember 6th, 2015 at 10:54MindaugasNovember 6th, 2015 at 13:02Nick DesaulniersNovember 6th, 2015 at 14:48Eric LawrenceNovember 6th, 2015 at 15:03Nick DesaulniersNovember 6th, 2015 at 15:23