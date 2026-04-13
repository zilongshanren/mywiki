---
title: Non-blocking packet-oriented sending and receiving data via TCP
url: https://gamedevcoder.wordpress.com/2011/01/14/non-blocking-sending-and-receiving-data-via-tcp/
published: '2011-01-14'
source_blog: Gamedev Coder Diary
source_site: https://gamedevcoder.wordpress.com
category: game programming
fetched: '2026-04-13'
---

Let’s get straight into the topic, here’s our goal for today:

Want to be able to send (and receive) whole data packets without blocking and without having separate “send thread” (or “receive thread”) using TCP. Similar to UDP in that whole packet is either fully sent (or fully received) except we want that to work with TCP.

The first suggestion here is to use non-blocking sockets. That’s obviously a good choice, however, there’s a larger problem to consider to do with the fact that [send](http://pubs.opengroup.org/onlinepubs/009695399/functions/send.html) socket function might not send the whole buffer it’s given.

Now, let’s imagine the following scenario. Application wants to send message that is 20 bytes (assume it has successfully created TCP socket and it has set it up to be non-blocking before). Then it calls send, but it only sends 15 bytes. What are we going to do with remaining 5 bytes?

We could keep calling send until we eventually send the whole message but you never know how much time you could spend doing that. And remember that our primary goal was that all is non-blocking.

Or we could leave it up to user. User would then have to remember how many bytes were successfully sent and thus how much remaining data still needs to be sent. The user would also need to store somewhere the part of message that failed to send. But having to do that would make it highly inconvenient for the user. Wouldn’t it?

Here’s one solution to the problem. The main idea to get around described issue is to encapsulate the process of sending by some helper that would either fully succeed (all bytes sent) or fully fail (zero bytes sent). To be able to do that, our helper needs to have its own buffer of the size at least as large as the size of largest message we’re planning to be sending. This is so that in the event of failing to send part of the message, we can still store the rest of it in a buffer and try to send it later. The only extra requirement is that user frequently calls some `Tick()`

function to make sure any pending data eventually gets sent.

And that’s it. The main idea has been described, here’s what mentioned helper class might look like in C/C++:

class TCPHelper { public: // Creates helper for a given non-blocking TCP socket TCPHelper(int socket, int sendBufferSize); // Sends the data bool Send(const void* data, int dataSize, int& socketError); // Tries to send pending data void Tick(int& socketError); private: bool Buffer(const void* data, int dataSize); int m_socket; byte* m_buffer; int m_bufferSize; int m_bufferCapacity; };

The constructor just sets the socket and allocates internal send buffer:

TCPHelper::TCPHelper(int socket, int sendBufferSize) : m_socket(socket), m_bufferSize(0), m_bufferCapacity(sendBufferSize) { m_buffer = (byte*) malloc(sendBufferSize); }

The `TCPHelper::Send()`

function first tries to send any previous pending data, then it tries to buffer the data and eventually send it.

bool TCPHelper::Send(const void* data, int dataSize, int& socketError) { assert(dataSize <= m_bufferCapacity); Tick(socketError); if (socketError < 0) return false; if (!Buffer(data, dataSize)) return false; Tick(socketError); if (socketError < 0) return false; return true; }

The `TCPHelper::Buffer()`

just copies the data into our buffer:

bool TCPHelper::Buffer(const void* data, int dataSize) { if (m_bufferSize + dataSize > m_bufferCapacity) return false; memcpy(m_buffer + m_bufferSize, data, dataSize); m_bufferSize += dataSize; return true; }

And finally the `TCPHelper::Tick()`

function that sends any pending data stored in a buffer:

void TCPHelper::Tick(int& socketError) { // Nothing to send? if (m_bufferSize == 0) { socketError = 0; return; } // Send the data socketError = send(m_socket, m_buffer, m_bufferSize, 0); if (socketError < 0) { // EAGAIN or EWOULDBLOCK are not critical errors if (socketError == EAGAIN || socketError == EWOULDBLOCK) socketError = 0; return; } // Pop the remaining data to the front of the buffer m_bufferSize -= socketError; if (m_bufferSize > 0) memmove(m_buffer, m_buffer + socketError, m_bufferSize); // Indicate no error socketError = 0; }

In all of the presented functions, `socketError`

always receives either 0 (for no critical socket errors) or negative number being regular socket error. In case of `TCPHelper::Send()`

function, when it returns `false`

and `socketError`

is 0, it means we failed to buffer the message on either socket or custom buffer level.

Note that I have omitted all parts of the code that I would normally implement but were irrelevant for the main topic – for example `TCPHelper`

class destructor. We also don’t properly handle an attempt to send again after there was critical socket error (i.e. when `socketError`

received negative value) and there’s also significant inefficiency to do with always buffering the data first, then sending it. In real life, most of the time immediate send without buffering is possible.

Now that we have done sending part, we can apply similar approach to implementing receiving of the data. To do that we’d have to add to `TCPHelper`

separate buffer for received data and implement one additional method

bool TCPHelper::Receive(void* data, int dataSize, int& socketError)

that either receives all `dataSize`

bytes and returns `true`

or fails to receive any and returns `false`

.

You can get complete C/C++ code implementing both sending and receiving here: [TCPHelper.h](https://github.com/macieks/tcp_helper/blob/master/TCPHelper.h), [TCPHelper.cpp](https://github.com/macieks/tcp_helper/blob/master/TCPHelper.cpp). The only major improvement that I can think of here is avoiding memmove and instead using some kind of ring buffer / fifo queue to push and pop the data.