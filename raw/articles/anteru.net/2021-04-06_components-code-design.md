---
title: Components & code design
url: https://anteru.net/blog/2021/components-code-design
published: '2021-04-06'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

Software architecture requires a lot of good craftmanship, yet it’s somewhat difficult to learn by just looking at the final design and not seeing the decisions along the way. Today, we’ll look at a problem that I’ve faced a few times in different forms which will hopefully give you some ideas how to approach similar problems. A quick note on the code examples in this post: They are written for brevity, especially anything memory related will be just plain pointers, but that’s not the topic today.

Another topic I want to briefly touch upon before we continue: I’m going to take an *object-oriented* approach. There are of course other approaches that have different problems, but that’s a topic for another blog post. If you want to get an idea how this could look in a more data-oriented fashion, I’d like you to recommend [this blog post](https://fgiesen.wordpress.com/2011/11/21/buffer-centric-io/).

With that out of the way, let’s move on to our scenario. We’re working in an object-oriented language (C++ in my case here, but Java, C#, etc. would all work the same), and we have a framework with a stream abstraction as following:

```
class IStream
{
public:
virtual ~IStream() = default;
virtual void Read(int64 count, byte* buffer) = 0;
virtual void Write(int64 count, const byte* buffer) = 0;
virtual int64 GetSize() const = 0;
virtual void Seek(int64 offset) = 0;
virtual bool CanSeek() const = 0;
};
```


This is a quite common design, we have one class or component doing one thing. At some point, an engineer needed compression support, and given a stream abstraction was in place, the decision was made to add compressed streams. Without further ado:

```
class ZipCompressedStream : public IStream
{
public:
ZipCompressedStream(IStream* s);
// Implement interface
private:
IStream* wrappedStream_;
};
```


That’s a very convenient way to add compression support in the current design. Whenever you have a stream, you can just wrap it in another and voilà, it’s compressed. One nice property of this approach is that it directly supports streaming reads & writes instead of forcing users to send the whole data set in bulk.

With those functions in place, we’re now tasked to write a content-addressed store (also know as a CAS.) In a CAS, the data is addressed by the hash of the contents, which gives you free de-duplication. For our very simple example here, we’ll assume we’re writing two files:

- An index with the hash, offset pairs
- A content file file which contains all data concatenated together

After a quick design discussion, we start with a minimal API as following:

```
class ContentAddressedStore
{
public:
Hash AddContent(const int64 size, const byte* data);
IStream* GetContentByHash(Hash hash);
};
```


`AddContent`

calculates the hash of the data, and updates both the index and the data bundle. `GetContentByHash`

returns an `IStream`

for the same reasons as discussed previously: No upfront allocation of the full result buffer.

That was pretty simple. The next day we get asked if we can compress the storage a bit. We’ll say “of course”, given we can simply wrap the stream in a compressed stream – all we do is write a few lines of code and all data ends up compressed. On both the read/write end, we simply need to wrap our existing stream into a compressed stream. Here’s the read-side for example:

```
IStream* ContentAddressedStore::GetContentByHash(Hash hash)
{
return new ZipCompressedStream(
CreateStream(
GetStartOffset(hash), GetContentSize(hash)
)
);
}
```


(I’m assuming here we need to compress each chunk separately as a compressed stream will not allow arbitrary seek operations.)

A few weeks later, we get asked to add the ability to remove entries. Now, we’re at a point where we need to think a bit: Removing entries means there is potentially unused data in the package file. Is this acceptable? If the ratio of deleted content to useful content is very low, that might be perfectly fine. If the ratio is high though we probably want a way to compact a CAS. After some profiling it turns out the holes can become very large, so we decide to compact. Practically speaking, reading all content and writing it to a new file is probably the safest option compared to fiddling around directly inside a file, so we’ll go with that. Let’s assume we added a method to iterate over all hashes in a CAS in the meantime. With that, we could implement as following:

```
std::vector<byte> buffer;
for (const auto& hash : sourceCAS->GetHashes()) {
IStream* sourceStream = sourceCAS->GetContentByHash(hash);
buffer.resize(sourceStream->GetSize());
sourceStream->Read(buffer.size(), buffer.data());
targetCAS->AddContent(buffer.size(), buffer.data());
}
```


It may not be obvious to you yet, but while this is a perfectly valid solution, it will *decompress and re-compress* the whole data set. This may be very bad, or just what you wanted, for instance if you changed the compression algorithm. This is also the moment where we need to take a step back and look at how we arrived here.

So far, all design choices came easily. We made sound technical decisions along the way. The code is clean and individual responsibilities are clearly encapsuled. Yet, we ended up with a design where we can’t efficiently skip the data (re-)compression. You might think that it would be easy to fix by changing the `AddContent()`

function to accept an `IStream`

instead, but that’s not going to cut the mustard as a stream doesn’t provide direct access the underlying compressed bytes. Nor should it – why would you make this a leaky abstraction?

By trying to keep things separate, we created a situation where a certain property of our code is hidden away from us. What we need to do is some way to reach straight through a stream if it happens to be compressed and get the underyling data. If we think a bit further though, we notice that the problem here is that our components can’t talk to each other any more. If you look closely at the copy example, the source stream never interacts with the target stream. We decoupled them and by doing so, we made it impossible for one stream to understand that the data is coming from another stream, potentially of the same class.

That’s the very moment where we’re going to make a new architectural decision. We’re going to keep our components, but we’re trying to express something new: A close coupling between two streams for copies. Where do we place this? The most obvious place is to put it into a stream, as that’s where the decision is made in the end.

Let’s go ahead and introduce this new concept, `CopyTo`

, which allows one stream to copy itself into another stream (`CopyFrom`

would work literally the same):

```
class IStream
{
public:
virtual void CopyTo(IStream* other);
// Rest as before
};
```


With that, and RTTI enabled, the `ZipCompressedStream`

is free to check if the target-stream is of the same class, and if so, it can request the raw bits from the underlying stream. One nice property here for existing code is that we can provide a default implementation of `CopyTo`

, and replace the uses of `Read`

/`Write`

into a buffer with that. This also has the (in my opinion desired) side effect of increasing the abstraction level and providing more information.

The new code for `CopyTo`

inside `ZipCompressedStream`

will look somewhat like this now:

```
void ZipCompressedStream::CopyTo(IStream* other)
{
// Some RTTI mechanism, could be dynamic_cast as well
if (is<ZipCompressedStream>(other)) {
// We know how ZipStreams look like, so we can optimize
// this by dropping down to the underlying stream
wrappedStream_->CopyTo(static_cast<ZipCompressedStream*>(other)->wrappedStream_);
} else {
IStream::CopyTo(other);
}
}
```


If we take a moment to reflect about what we did here: We started with a perfectly valid design for a stream, and over time, we created building blocks which made one particular approach “most natural”. At the same time, we ended up creating a potential performance issue. If we had continued by exposing components this would have required access to the underlying stream, which results in a leaky abstraction. The fix we deployed in the end was to introduce closer coupling. We managed to avoid introducing a leaky abstraction, which in my experience always pays off, as a leaky abstraction usually tells you that your abstraction is not good and not modelling the actual problem.

The other takeaway here is that you also need some proper “big picture” architecture and budget the time for it. Components are a great way to quickly create problem abstractions, but individual component owners will not be aware of cross-cutting concerns. That’s the job of the architect(s) on your team, and if you don’t pay close attention to it, many small-scale isolated decisions will result in code that is incoherent and inadequatly models the underlying issue.

I hope this small example did give you an idea of the kind of thought process required, even for a seemingly trivial problem. Thanks for reading!