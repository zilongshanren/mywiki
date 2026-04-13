---
title: Buffer-centric IO
url: https://fgiesen.wordpress.com/2011/11/21/buffer-centric-io/
published: '2011-11-21'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# Buffer-centric IO

This is a small but nifty solution I discovered while working on IO code for [Iggy](http://www.radgametools.com/iggy.htm). I don’t claim to have invented it – as usual in CS, this was probably first published in the 60s or 70s – but I definitely never ran across it in this form before, so it seems worth writing up. Small disclaimer up front: First, this describes a combination of techniques that are somewhat orthogonal, but they nicely complement each other, so I describe them at the same time. Second, it’s definitely not the best approach in every scenario, but it’s nifty and definitely worth knowing about. I’ve found it particularly useful when dealing with compressed data.

### Setting

A lot of code needs to be able to accept data from different sources. Sometimes you want to load data from a file; sometimes it’s already in memory, or it’s a memory-mapped file (boils down to the same thing). If it comes from a file, you may have one file per item you want to load, or pack a bunch of related data into a “bundle” file. Finally, data may be compressed or encrypted.

If possible, the simplest solution is to just write your code to assume one such method and stick with it – the easiest usually being the “already in memory” option. This is fine, but can get problematic depending on the file format: for example, the `SWF`

(Flash) files that Iggy loads are usually Deflate-compressed as a whole, and may contain chunks of image data that are themselves JPEG- or Deflate-compressed. Finally, Iggy wants all the data in its own format, not in the Flash file format, since even uncompressed Flash files involve a lot of bit-packing and implicit information that makes them awkward to deal with directly.

Ultimately, all we want to have in memory is our own data structures; but an implementation that expects all data to be decompressed to memory first will need a lot of extra memory (temporarily at least), which is problematic on memory-constrained platforms.

The standard solution is to get rid of the memory-centric view completely and instead implement a stream abstraction. For read-only IO (which is what I’ll be talking about here), a simple but typical (C++) implementation looks like this:

class SimpleStream { public: virtual ErrorCode Read(U8 *buffer, U32 numBytes, U32 *bytesActuallyRead) = 0; };

Code that needs to read data takes a `Stream`

argument and calls `Read`

when necessary to fill its input buffers. You’ll find designs like this in most C++ libraries that handle at least some degree of IO.

Simple, right?

### The problems

Actually, there’s multiple problems with this approach.

For example, consider the case where the file is already loaded into memory (or memory-mapped). The app expects data to land in `buffer`

, so our `Read`

implementation will end up having to do a `memcpy`

or something similar. That’s unlikely to be a performance problem if it happens only once, but it’s certainly not pretty, and if you have multiple streams nested inside each other, the overhead keeps adding up.

Somewhat more subtly, there’s the business with `numBytes`

and `bytesActuallyRead`

. We request some number of bytes, but may get a different number of bytes back (anything between 0 and `numBytes`

inclusive). So client code has to be able to deal with this. In theory, “stream producer” code can use this to make things simpler; to give an example, lots of compressed formats are internally subdivided into chunks (with sizes typically somewhere between 32KB and 1MB), and it’s convenient to write the code such that a single `Read`

will never cross a chunk boundary. In practice, a lot of the “stream consumer” code ends up being written using memory or uncompressed file streams as input, and will implicitly assume that the only cases where “partial” blocks are returned are “end of file” or error conditions (because that’s all they ever see while developing the code). This behavior may be technically wrong, but it’s common, and the actual cost (slightly more complexity in the producer code) is low enough to not usually be worth making a stand about.

So we have an API where we frequently end up having to check for and deal with what’s basically the same boundary condition on both sides of the fence. That’s a bad sign.

Finally, there’s the issue of error handling. If we’re loading from memory, there’s basically only one error condition that can happen: unexpected end, when we’ve exhausted the input buffer even though we want to read more. But for a general stream, there’s all kinds of errors that can happen: end of file, yes, but also read errors from disk, timeouts when reading from a network file system, integrity-check errors, errors decompressing or decrypting a stream, and so on. Ideally, every single caller should check error codes (and perform error handling if necessary) all the time. Again, in practice, this is rarely done everywhere, and what error-handling code is there is often poorly tested.

The problem is that checking for and reacting to error conditions everywhere is *inconvenient*. One solution is using exception handling; but this is, at least among game developers, a somewhat controversial C++ feature. In the case of Iggy, which is written in C, it’s not even an option (okay, there is `setjmp`

/ `longjmp`

, which we even use in some cases – though not for IO – but let’s not go there). A different option is to write the code such that error checking isn’t required after every `Read`

call; if possible, this is usually much nicer to use.

### A different approach

Without further ado, here’s a different stream abstraction:

struct BufferedStream { const U8 *start; // Start of buffer. const U8 *end; // (One past) end of buffer // i.e. buffer_size = end-start. const U8 *cursor; // Cursor in buffer. // Invariant: start <= cursor <= end. ErrorCode error; // Initialized to NoError. ErrorCode (*Refill)(BufferedStream *s); // Pre-condition: cursor == end (buffer fully consumed). // Post-condition: start == cursor < end. // Always returns "error". };

There’s 3 big conceptual differences here:

- The buffer is owned and managed by the producer – the consumer does
*not*get to specify where data ends up. - The
`Read`

function has been replaced with a`Refill`

function, which reads in an unspecified amount of bytes – the one guarantee here is that at least one more byte will be returned, even in case of error; more about that later. Also note it’s a function pointer, not a virtual function. Again, there’s a good reason for that. - Instead of reporting an error code on every
`Read`

, there’s a persistent`error`

variable – think`errno`

(but local to the given stream, which avoids the serious problems that hamper the ‘real’`errno`

).

Note that this abstraction is both more general and more specific than the stream abstraction above: more general in the sense that it’s easy to implement `SimpleStream::Read`

on top of the `BufferedStream`

abstraction (I’ll get to that in a second), and more specific in the sense that all `BufferedStream`

implementations are, by necessity, buffered (it might just be a one-byte-buffer, but it’s there). It’s also lower-level; the buffer isn’t encapsulated, it’s visible to client code. That turns out to be fairly important. Instead of elaborating, I’m gonna present a series of examples that demonstrate some of the strengths of this approach.

### Example 1: all zeros

Probably the simplest implementation of this interface just generates an infinite stream of zeros:

static ErrorCode refillZeros(BufferedStream *s) { static const U8 zeros[256] = { 0 }; s->start = zeros; s->cursor = zeros; s->end = zeros + sizeof(zeros); return s->error; } static void initZeroStream(BufferedStream *s) { s->Refill = refillZeros; s->error = NoError; s->Refill(s); }

Not much to say here: whenever `Refill`

is called, we reset the pointers to go over the same array of zeros again (the count of 256 is completely arbitrary; you could just as well use 1, but then you’d end up calling `Refill`

a lot).

### Example 2: stream from memory

For the next step up, here’s a stream that reads either directly from memory, or from a memory-mapped file:

static ErrorCode fail(BufferedStream *s, ErrorCode reason) { // For errors: Set the error status, then continue returning // zeros indefinitely. s->error = reason; s->Refill = refillZeros; return s->Refill(s); } static ErrorCode refillMemStream(BufferedStream *s) { // If this gets called, clients wants to read past the end of // the memory buffer, which is an error. return fail(s, ReadPastEOF); } static void initMemStream(BufferedStream *s, U8 *mem, size_t size) { s->start = mem; s->cursor = mem; s->end = mem + size; s->error = NoError; s->Refill = refillMemStream; }

The init function isn’t very interesting, but the `Refill`

part deserves some explanation: As mentioned before, the client calls `Refill`

when it’s finished with the current buffer and still needs more data. In this case, the “buffer” was all the data we had; therefore, if we ever try to refill, that means the client is trying to read past the end-of-file, which is an error, so we call `fail`

, which first sets the error code. We then change the refill function pointer to `refillZeros`

, our previous example: in other words, if the client tries to read past the end of file, they’ll get an infinite stream of zeros (satisfying our above invariant that `Refill`

*always* returns at least one more byte). But the error flag will be set, and since `refillZeros`

doesn’t touch it, it will stay the way it was.

In effect, making `Refill`

a function pointer allows us to implicitly turn any stream into a state machine. This is a powerful facility, and it’s great for this kind of error handling and to deal with certain compressed formats (more later), but like any kind of state machine, it quickly gets more confusing than it’s worth if there’s more than a handful of states.

Anyway, there’s one more thing worth pointing out: *there’s no copying here*. A from-memory implementation of `SimpleStream`

would need to do a *memcpy* (or something equivalent) in its `Read`

function, but since we don’t let the client decide where the data ends up, we can just point it directly to the original bytes without doing any extra work. Because forwarding is effectively free, it makes it easy to decouple “framing” from data processing even in performance-critical code.

### Example 3: parsing JPEG data

Case in point: JPEG data. JPEG files interleave compressed bitstream data and metadata. Metadata exists in several types and is denoted by a special code, a so-called “marker”. A marker consists of an all-1-bits byte (0xff) followed by a nonzero byte. Because the compressed bitstream can contain 0xff bytes too, they need to be escaped using the special code 0xff 0x00 (which is not interpreted as a marker). Thus code that reads JPEG data needs to look at every byte read, check if it’s 0xff, and if so look at the next byte to figure out whether it’s part of a marker or just an escape code. Having to do this in the decoder inner loop is both annoying (because it complicates the code) and slow (because it forces byte-wise processing and adds a bunch of branches). It’s much nicer to do it in a separate pass, and with this approach we can naturally phrase it as a layered stream (I’ll skip the initialization this time):

struct JPEGDataStream : public BufferedStream { BufferedStream *src; // Read from here }; static ErrorCode refillJPEG_lastWasFF(BufferedStream *s); static ErrorCode refillJPEG(BufferedStream *str) { JPEGDataStream *j = (JPEGDataStream *)str; BufferedStream *s = j->src; // Refill if necessary and check for errors if (s->cursor == s->end) { if (s->Refill(s) != NoError) return fail(str, s->error); } // Find next 0xff byte (if any) U8 *next_ff = memchr(s->cursor, 0xff, s->end - s->cursor); if (next_ff) { // return bytes until 0xff, // continue with refillJPEG_lastWasFF. j->start = s->cursor; j->cursor = s->cursor; // EDIT typo fixed (was "current") j->end = next_ff; j->Refill = refillJPEG_lastWasFF; s->cursor = next_ff + 1; // mark 0xff byte as read } else { // return all of current buffer j->start = s->cursor; j->cursor = s->cursor; j->end = s->end; s->cursor = s->end; // read everything } } static ErrorCode refillJPEG_lastWasFF(BufferedStream *str) { static const U8 one_ff[1] = { 0xff }; JPEGDataStream *j = (JPEGDataStream *)str; BufferedStream *s = j->src; // Refill if necessary and check for errors if (s->cursor == s->end) { if (s->Refill(s) != NoError) return fail(str, s->error); } // Process marker type byte switch (*s->cursor++) { case 0x00: // Not a marker, just an escaped 0xff! // Return one 0xff byte, then resume regular parsing. j->start = one_ff; j->cursor = one_ff; j->end = one_ff + 1; j->Refill = refillJPEG; break; // Was a marker. Handle other cases here... case 0xff: // 0xff 0xff is invalid in JPEG return fail(str, CorruptedData); default: return fail(str, UnknownMarker); } }

It’s a bit more code than the preceding examples, but it demonstrates how streams can be “layered” and also nicely shows how the implicit state machine can be useful.

### Discussion

This clearly solves the first issue I raised – there’s no unnecessary copying going on. The interface is also really simple: Everything is in memory. Client code still has to deal with partial results, but because the client never gets to specify how much data to read in the first place, the interface makes it a lot clearer that handling this case is necessary. It also makes it a lot more common, which goes a long way towards making sure that it gets handled. Finally, error handling – this is only partially resolved, but the invariants have been picked to make the life of client code as easy as possible: All errors are “sticky”, so there’s no risk of “missing” an error if you do something else in between doing the read and checking for errors (a typical issue with `errno`

, `GetLastError`

and the like). And our error-“refill” functions still return data (albeit just zeros in these examples). These two things together mean that, in practice, you only really need to check for errors inside loops that might not terminate otherwise. In all other cases, you will fall through to the end of functions eventually; as long as you check the error code before you dispose of the stream, it will be noticed.

One really cool thing you can do with this type of approach (that I don’t want to discuss in full or with code because it would get lengthy and is really only interesting to a handful of people) is give the client pointers into the window in a LZ77-type compressor. This completely removes the need for any separate output buffers, saving a lot of copying and some small amount of memory. This is especially nice on memory-constrained targets like SPUs. In general, giving the producer (instead of the consumer) control over where the buffer is in memory allows producer code to use ring buffers (like a LZ77 window) completely transparently, which I think is pretty cool.

There’s a lot more that could be said about this, and initially I wanted to, but I didn’t want to make this too long; better have two medium-sized posts than one huge post that nobody reads to the finish. Besides, it means I can base a potential second post on actual questions I get, rather than having to guess what questions you might have, which I’m not very good at.

Excellent read.

I wonder, would it be easier to grasp the idea if you renamed BufferedStream to something like BufferedStreamFrame or BufferedStreamWindow? And “Refill” to “MoveFrame” or something like that?

When you mention compression, be sure not to just say ‘LZ’, as there is a huge difference between LZ77 derived algorithms and LZ78, which is designed to compress/decompress streamed data. Just a technicality, but its important to not forget LZ78 exists ;p.

What I mean to say, if this comment gets approved, is that unlike LZ77, in LZ78 there is no window that you need to search back through. Instead, the phrase dictionary is built as the data is streamed in/out. It is just an important distinction, especially in this context, in my opinion ;).

As always, great work though. I love reading your articles. I wrote a BIT I/O class years ago that in many ways is similar to this conceptually, except its intent was to allow for BIT I/O. It does it on a streaming basis, with buffering though. All public F/OSS.

You got me, and on something that’s one of my usual pet peeves no less :). That’ll teach me to blog at 4 in the morning…

Something partially similar exists in various media APIs from Microsoft.

You call a GetNextSample method, which like your refill, gets you a new buffer with data. Most of the times the buffers are allocated by the API from a pool. Sometimes you can also allocate the buffers yourself.

http://msdn.microsoft.com/en-us/library/windows/desktop/bb530123%28v=vs.85%29.aspx

http://msdn.microsoft.com/en-us/library/windows/desktop/dd390166%28v=vs.85%29.aspx

Having only skimmed this briefly, this sounds like co-routines: http://en.wikipedia.org/wiki/Coroutine … I did the same thing in assembler on a 6502 once :)

Coroutines are a great tool for this kind of IO task, but they’re an orthogonal concept to what I’m trying to explain here. The main point of this article is that “opening the black box”, exposing the buffer pointers (which in themselves are pretty standard) to the client, and letting the producer not the consumer control the data flow combine to give you a very nice, if unconventional, IO abstraction.

By the way, C/C++ aren’t exactly the best languages to express this; the buffer pointers are more clearly (and cleanly) expressed as array slices, and “refill” is well-suited to be implemented using either coroutines or continuations.

Is there a reason to have both ‘start’ and ‘cursor’? It doesn’t look like you read from ‘start’ at all here. I suppose it lets the consumer “rewind”, but this isn’t always possible (e.g. if start == cursor), so it seems odd to even support it without some kind of “reverse refill”.

`start`

is there mainly to make the invariants easier to understand: If I just wrote`cursor <= end`

it would be harder to see what’s going on. That said, there’s a good reason for it to be there, though I don’t show it in the code snippets (I meant to go into it, but decided to cut it): it’s useful if you want to be able to get the current file pointer.Keeping track of the file pointer “the naive way” requires client code to update it every time they modify

`cursor`

, which is awkward and error-prone. Instead, if you need the file pointer (necessary for e.g. file formats that align some fields on large power-of-2 boundaries), you do it like this:Two notes/questions :

1. For N-byte reads I think you basically have to do a memcpy. The issue is that if your buffer doesn’t have the N bytes, you have to copy out the bytes it has, then refill, then get the rest of the bytes. So I don’t see how you avoid the memcpy inherent to read except for the case of reading single bytes at a time?

Basically you either have to provide an “fread” type function for N byte reads that does a copy, or the client code has to handle “not enough bytes available” cases itself, which seems unviable.

2. This seems very similar to the way stdio is implemented on most platforms. (your BufferedStream struct is almost identical to FILE). The only difference is that their refill() typically copies into a buffer rather than returning a pointer buffer to the internal buffer, but you could easily change that in most cases and I don’t see how it makes a big difference. Maybe a compare/contrast would help.

1. Yes, you want a Read-style function at the bottom for the client code. The point is that this model allows you to get rid of the copies in the intermediate stages.

Usual setup on e.g. consoles: System IO library (comes with alignment and size requirements, e.g. dest needs to be cache-lined aligned, must read whole sectors at a time, stuff like that) -> Game IO layer (does buffering to make alignment/size restrictions invisible to game) -> PAK file layer (usually just forwards to Game IO, no buffering on its own) -> Decompress (has both input and output buffers) -> Client. This usually has 3 buffering stages that copy memory around (in Game IO, decompress in, and decompress out), plus the final memcpy on the Client side (buffer -> target). This is because buffers are “passed by value” (you get what I mean). The scheme I describe passes buffers “by reference”; alignment/size restrictions just affect the buffer placement and chunking of data, but entail no copying around. The decompress stage can read directly from the raw IO buffers. And on the output end, if it’s already got a “buffer” built in (like LZ77 does), it can just hand out pointers inside the window. The only copy you really need is the one at the end, when you copy the data to its final destination.

We often have to deal with cases that are just moronic but nevertheless exist in our source data, like JPEGs inside DEFLATE data, or DEFLATE data inside DEFLATE data. For obvious reasons, a lot of the “outer” blocks just end up not compressed. Not doing (unaligned!) copies in the middle saves work and wastes less cache space.

And of course, you don’t have to religiously avoid copying, but it’s often convenient to selectively only process some blocks and leave through others unmodified. For example, the JPEG “de-escaping” thing only needs to touch blocks that contain 0xff bytes (it may then either de-escape to a separate buffer or use more slices like the example code does).

2. The buffering itself is just the standard buffering scheme, yes. I don’t claim there’s anything fancy going on here; the ideas here are a) exposing buffers directly and letting the producer not the consumer manage memory (which gives you “perfect forwarding”), b) using a function pointer instead of a static interface to implement the implicit state machine in most IO operations as state machine, not an if tree on every invocation, c) choosing error handling rules and invariants such that all non-data-dependent control flow will terminate, d) making errors “sticky” so they can be handled at natural “decision points” in the program, rather than having to check on every single read.

I don’t claim that any of those ideas are novel. I do claim that their combination is useful and quite elegant, and worth writing about. :)

I’m not going to really comment about this. (But you may want to google e.g. “iteratee”.) Just to mention obvious errors:

whereas

This is the standard (in C and C-derived languages anyway!) convention where all intervals are half-open by default.

`cursor == end`

is a valid state (hence allowed by the invariants) that denotes “no more bytes available in current buffer”, and`end - cursor`

is the number of bytes available. I don’t see any problem with this code, besides the mention of`s->current`

(should be`s->cursor`

, I decided to rename this field in the middle of writing).As for the Iteratee reference: Interesting, that’s indeed

veryclose to what I’m describing here. Haskell certainly is a place I wouldn’t have expected this to turn up.Ah, so you don’t mind storing invalid pointer in

. Okay. Then it’s just a matter of style. (But this could be unexpected: valid usage of non-null invalid pointer. I would be puzzled a little if I had to debug something that used this code. But, again, this is a style.)

Iteratees are kind of framework for writing functions on lazy streams. But one could use lazy input without iteratees. Data.ByteString.Lazy is my favorite feature of Haskell IO, probably.

It’s not an invalid pointer, it’s invalid to dereference (important distinction); as per the C/C++ standards, pointers one past the end of an array are well-defined and supported (though dereferencing them is not). This is precisely because the usage of half-open intervals for such things in C/C++ is idiomatic. You’ll find the exact same convention in all kinds of C/C++ libraries, from stdio (which commonly uses a

`start / cursor / end`

description for stream buffers, but puts the error into errno and isn’t “chainable”) to the STL (all iteratable STL containers have`begin()`

return an iterator to the first element and`end()`

return an iterator one past the last element).In the code given, it relates to the subtle issue of zero-byte files. If you create a zero-byte stream, you’ll have a stream with

`start == cursor == end`

in`NoError`

state. If and only if the app then tries to refill, it will transition to an error state (for reading past the end of file). The convention that`end`

point one past the last character allows handling this case cleanly. If`end`

where inclusive, you would need some special encoding for “empty stream” (e.g. all pointers are`NULL`

), which makes the invariants more complicated by adding two disjoint ranges to check for, and also complicates all producers that might return 0-byte streams because they need to set things up correctly. For the same reason (handling zero-element sequences nicely) it’s employed in the other cases I mentioned.