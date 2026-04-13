---
title: 'Keeping Server and Client Separate :: nklein software'
url: http://nklein.com/keeping-server-and-client-separate
author: Pat
published: '2011-09-08'
source_blog: nklein software
source_site: http://nklein.com
category: game programming
fetched: '2026-04-13'
---

### The problem

Whenever I write client-server applications, I run into the same problem trying to separate the code. To send a message from the server to the client, the server has to serialize that message and the client has to unserialize that message. The server doesn’t need to unserialize that message. The client doesn’t need to serialize that message.

It seems wrong to include both the serialization code and the unserialization code in both client and server when each side will only be using 1/2 of that code. On the other hand, it seems bad to keep the serialization and unserialization code in separate places. You don’t want one side serializing A+B+C and the other side trying to unserialize A+C+D+B.

### One approach: data classes

Some projects deal with this situation by making every message have its own data class. You take all of the information that you want to be in the message and plop it into a data class. You then serialize the data class and send the resulting bytes. The other side unserializes the bytes into a data class and plucks the data out of the data class.

The advantage here is that you can have some metaprogram read the data class definition and generate a serializer or unserializer as needed. You’re only out-of-sync if one side hasn’t regenerated since the data class definition changed.

The disadvantage here is that I loathe data classes. If my top-level interface is going to be `(send-login username password)`

, then why can’t I just serialize straight from there without having to create a dippy data structure to hold my opcode and two strings?

### Another approach: suck it up

Who cares if the client contains both the serialization and unserialization code? Heck, if you’re really all that concerned, then `fmakunbound`

half the universe before you `save-lisp-and-die`

.

Of course, unless you’re using data classes, you’re either going to have code in your client that references a bunch of functions and variables that only exist in your server or your client and server will be identical except for:

#+server (server-main)

#-server (client-main))

Now, of course, your server is going to accidentally depend on OpenGL and OpenAL and SDL and a whole bunch of other -L’s it never actually calls. Meanwhile, your client is going to accidentally depend on Postmodern and Portable-Threads and a whole bunch of other Po-‘s it never actually calls.

### Another approach: tangle and weave, baby

Another way that I’ve got around this is to use literate programming tools to let me write the serialiization and unserialization right next to each other in my document. Then, anyone going to change the serialize code would be immediately confronted with the unserialize code that goes with it.

The advantage here is that you can tangle the client code through an entirely separate path than the server code keeping only what you need in each.

The disadvantage here is that now both your client code and your server code have to be in the same document or both include the same sizable chunk of document. And, while there aren’t precisely name-capturing problems, trying to include the “serialize-and-send” chunk in your function in the client code still requires that you use the same variable names that were in that chunk.

### How can Lisp make this better?

In Lisp, we can get the benefits of a data-definition language and data classes without needing the data classes. Here’s a snippet of the data definition for a simple client-server protocol.

(userial:make-enum-serializer :opcode (:ping :ping-ack))

(defmessage :ping :uint32 ping-payload)

(defmessage :ping-ack :uint32 ping-payload)

I’ve declared there are two different types of messages, each with their own opcode. Now, I have macros for `define-sender`

and `define-handler`

that allow me to create functions which have no control over the actual serialization and unserialization. My functions can only manipulate the named message parameters (the value of `ping-payload`

in this case) before serialization or after unserialization but cannot change the serialization or unserialization itself.

With this protocol, the client side has to handle ping messages by sending ping-ack messages. The `define-sender`

macro takes the opcode of the message (used to identify the message fields), the name of the function to create, the argument list for the function (which may include declarations for some or all of the fields in the message), the form to use for the address to send the resulting message to, and any body needed to set fields in the packet based on the function arguments before the serialization. The `define-handler`

macro takes the opcode of the message (again, used to identify the message fields), the name of the function to create, the argument list for the function, the form to use for the buffer to unserialize, and any body needed to act on the unserialized message fields.

(define-sender :ping-ack send-ping-ack (ping-payload) *server-address*)

(define-handler :ping handle-ping (buffer) buffer

(send-ping-ack ping-payload))

The server side has a bit more work to do because it’s going to generate the sequence numbers and track the round-trip ping times.

(defvar *last-ping-payload* 0)

(defvar *last-ping-time* 0)

(define-sender :ping send-ping (who) (get-address-of who)

(incf *last-ping-payload*)

(setf *last-ping-time* (get-internal-real-time)

ping-payload *last-ping-payload*))

(define-handler :ping-ack handle-ping-ack (who buffer) buffer

(when (= ping-payload *last-ping-payload*)

(update-ping-time who (- (get-internal-real-time) *last-ping-time*))))

### Problems with the above

It feels strange to leave compile-time artifacts like the names and types of the message fields in the code after I’ve generated the functions that I’m actually going to use. But, I guess that’s just part of Lisp development. You can’t (easily) unload a package. I can `makunbound`

a bunch of stuff after I’m loaded if I don’t want it to be convenient to modify senders or handlers at run-time.

There is intentional name-capture going on. The names of the message fields become names in the handlers. The biggest problem with this is that the `defmessage`

calls really have to be in the same namespace as the `define-sender`

and `define-handler`

calls.

I still have some work to do on my macros to support `&key`

and `&optional`

and `&aux`

and `&rest`

arguments properly. I will post those macros once I’ve worked out those kinks.

Anyone care to share how they’ve tackled client-server separation before?

Not directly answering your question…

I believe DDS is one of the best systems available today for client/server separation. Known as “publish/subscribe” or “service-oriented architecture” in many circles. Not for everything; but the extensive set of QoS options outperform most custom code I’ve seen. The “Community Edition” of OpenSplice DDS is freely available under the LGPL.

Another good approach is to clearly specify the message format so others can cleanly implement it. XDR is nice and simple.

Then there’s always the XML crowd. The lisp variant being reading/writing s expressions.

DDS stuff falls definitely into the Data-Classes/Data-Object category, doesn’t it?

Also, my intent here is a client/server for a game. In a game scenario, you rarely want to send the same information to all clients and you want the clients to send requests to the server. One could accomplish this with the server subscribing to each of the clients and having a separate publisher for each client (and maybe some others for publishing to teams or everyone). But, this would be bending the tool to the point of breaking just for the sake of using the tool.

Although very heavyweight for your example, there’s always ASN.1. It’s a great way to rigorously define a protocol and you get a number of serializations (BER, DER, CER, and XER). There’s also some extensions (I believe they are standardized now but are at least draft) for more advanced “integration” with XML allowing you to specify how to assign portions of a data unit to an XML serialization.

Yes. The ASN.1 implementation that I see for Lisp is completely undocumented, but looks to be based on a data-classes approach. You start with your ASN.1 spec and from there generate data-classes.

I’m more partial to an RPC-like scenario, but I loathe XML-RPC and SOAP, too. I want RPC like SunRPC where my data is packed tightly (which uses XDR which is almost BER, IIRC).

If I were going to try to use data-classes in a current Lisp-based game, I’d probably opt for Google protocol buffers because everything else on this list is incomplete or not-binary or otherwise ugly (well, except XDR, which while not ugly isn’t really data-classes based either).

I suppose that I should consider using an XDR implementation or making my own libraries XDR-compatible. Hmmm.

That’s the biggest problem with ASN.1…not many good and free implementations (there are some very good and very expensive ones) since it’s generally geared for the telcom industry. Unless there are better implementations supporting the full extended XER packing format I think it will always be marginalized.

One problem I have with XDR is (AFAIK) there’s no rigorous protocol definition language so use is either adhoc or definitions are free form. I like having the rigor or the ASN.1 definitions with tagging and versioning. I haven’t looking at Google’s Protocol Buffers, I’ll have to check out the implementation.

you described the functional requirements for an rpc framework with an idl. i appreciate your aversion to the heavy-weight variations of that type, but do not yet see what prevents you from using one of the available lighter-weight equivalents to xdr?

I’m not sure which one’s you’re thinking of. I don’t even mind XDR. But, the IDLs that I can think of (already available in Lisp) are CORBA, ILU, XML-RPC, and SOAP. I don’t know if ILU is geared for rapidity. I did see one ONC RPC package for Lisp. I will be checking that out.

at least bert and thrift are available in one or more forms in lisp.