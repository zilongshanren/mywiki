---
title: Mozilla Persona for the non-web – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2013/04/mozilla-persona-for-the-non-web/
author: Luke Howard
published: '2013-04-29'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

My good friend Nico Williams reckons that HTTP is the new TCP, and TCP the new IP. If this is the case, then perhaps the rest of this article isn’t worth reading. However, not every application – particularly in the slower-moving corporate world – is going to move to the web overnight, and even though off-line web-based applications continue to improve, some of us still prefer our thick-client mail readers, amongst other things. Further, remote logon protocols such as SSH, and file sharing protocols such as CIFS and NFS, don’t always have direct web equivalents.

Now, [Mozilla Persona](https://persona.org) solves a bunch of interesting authentication problems: it has the best properties of public key infrastructure (in particular, the server doesn’t need to share a key with the identity provider), without of some of its drawbacks (because certificates are short-lived, the [revocation issue](http://en.wikipedia.org/wiki/Certificate_Revocation_List#Problems_with_CRLs) becomes less important). Another really nice property of Persona is that it doesn’t require you to initially authenticate in a particular way – one might use passwords, [one time passwords](http://en.wikipedia.org/wiki/One-time_password), [smartcards](http://en.wikipedia.org/wiki/Smart_card), [PKIX certificates](http://en.wikipedia.org/wiki/X.509), [Kerberos tickets](http://en.wikipedia.org/wiki/Kerberos_%28protocol%29), [EAP](http://tools.ietf.org/html/draft-ietf-abfab-gss-eap), some combination of the above – and as long as your identity provider knows who you are and can issue a Persona certificate, you’re good to go.

So, one might think: can we bring the benefits of Persona to non-web applications? We can. In the non-web world, many network protocols abstract away authentication using the [Simple Authentication and Security Layer](http://en.wikipedia.org/wiki/Simple_Authentication_and_Security_Layer) (SASL) or [Generic Security Service Application Program Interface](http://en.wikipedia.org/wiki/Generic_Security_Services_Application_Program_Interface) (GSS-API). We’re going to gloss over the details of these, suffice to say that in return for an application exchanging an arbitrary number of messages within its own protocol, the server is able to authenticate the client (and possibly vice versa). There may also be a shared key which can be used to encrypt or sign subsequent traffic.

Protocols that can use SASL or GSS-API for authentication include the acronym soup of [IMAP](https://en.wikipedia.org/wiki/Internet_Message_Access_Protocol), [SMTP](http://en.wikipedia.org/wiki/Simple_Mail_Transfer_Protocol), [XMPP](http://en.wikipedia.org/wiki/XMPP), [LDAP](http://en.wikipedia.org/wiki/Lightweight_Directory_Access_Protocol), [CIFS](http://en.wikipedia.org/wiki/Server_Message_Block), [NFS](http://en.wikipedia.org/wiki/Network_File_System), [SSH](http://en.wikipedia.org/wiki/Secure_Shell) and even [HTTP](http://en.wikipedia.org/wiki/Hypertext_Transfer_Protocol) itself. So, if we profile Persona for SASL and GSS-API, we can authenticate using a Persona identity – that is, a verified e-mail address or similar – within any of these application protocols.

This is indeed what we have been working on. Myself and Nico have written an [Internet Draft](http://tools.ietf.org/html/draft-howard-gss-browserid) that profiles BrowserID as a SASL and GSS-API security mechanism (we use “BrowserID” to refer to the actual protocol). My company, [PADL](http://www.padl.com/), has developed an open source implementation which is [available on Github](http://github.com/PADL/gss_browserid). (We have also prototyped a Windows [Security Support Provider](http://en.wikipedia.org/wiki/Security_Support_Provider_Interface) which enables applications such as Outlook, Exchange and Internet Explorer to work with Persona. Plug: we are exploring commercial possibilities for this in conjunction with our partner Painless Security.)

In the rest of this article, we’ll take a look at how Persona for the non-web differs from normal web-based authentication, and show an example demonstrating signing into an IMAP server with Persona from the Apple Mail client.

## Persona recap

There are plenty of articles on how Persona works, but we’ll recap the protocol here for convenience. Persona is a federated, decentralised authentication protocol. Users sign-in using a browser to an identity provider (IdP), which is an entity that can authenticate their e-mail address, although it can be any verifiable address that looks like an e-mail address.

When attempting to authenticate to a server (termed a Relying Party, or RP), the browser generates a private/public key pair, and asks the IdP to issue a certificate vouching for the public key. (These certificates may be cached.) The browser then generates an assertion, which contains the RP URL and a timestamp, and signs it with the user’s private key. The browser presents this and the user’s certificate to the web server, which validates the URL and timestamp and uses the user’s and IdP’s public keys to authenticate the user.

More information on Persona is available in the [Mozilla Persona web site](https://developer.mozilla.org/en-US/docs/persona). It has been written about on this blog in [Persona Beta 2 launch](https://hacks.mozilla.org/2013/04/persona-beta-2-launch/) and [the first Persona release post](https://hacks.mozilla.org/2012/09/first-beta-release-of-mozilla-persona-login-without-passwords/).

## Extending to the non-web

At its simplest, using Persona for the non-web is identical to the web case, with the exception that the assertion contains a service principal name instead of a HTTPS URL. Service principal names are a construct inherited from the Kerberos that identify a service (for example, “imap” or “xmpp”) running on a particular host. (They may also identify a specific instance of a service running on a host.) For example, the service principal name for the IMAP server on mail.example.com would be “imap/mail.example.com”. Because Persona audiences have to be URLs, we encapsulate the service principal name inside a URN.

We don’t say anything about how the application sends the assertion to the server, because neither the SASL nor GSS-API abstractions do. This is the application protocol’s business: typically, it will have a particular message in its own protocol that can encapsulate an authentication token (in IMAP, for example, this is the “AUTHENTICATE” message). All we do say is that the application must allow the user to sign into their IdP and generate an assertion, which means they must have the ability to run an embedded web browser. Most operating systems provide a plug-in interface for new security mechanisms, so this is usually possible.

So far, this is pretty simple: throw up a web browser control, use a slightly strange-looking URL to identify the server, get an assertion and send it to the server. The server verifies the assertion, identifies the user as per normal, and all is well. And indeed, this is pretty much the protocol; it’s testament to the designers of Persona that it can so easily be re-purposed.

However, there are a few small tweaks that we have made to make Persona more useful for the non-web case. We describe these below.

### Replay detection

The Persona specification doesn’t say anything about whether it’s safe to replay an assertion to a server or not. We’re a little paranoid, particularly because we don’t know whether the application is using transport security such as SSL/TLS. So we have built replay detection into the protocol. This works by either having the server maintain a cache of assertions it has received within a particular time frame, or having the client cryptographically sign a server-generated nonce.

### Channel binding

Even if the client is using TLS, it can be desirable to protect against a man-in-the-middle that has a valid server certificate, but is not the party that authenticated the client. Channel binding allows the client to bind the assertion to a TLS server certificate or session. The server verifying the assertion can then verify that it matches the certificate it sent to the client. (The channel binding is simply an additional claim in the assertion, protected by the same chain of trust as the other claims.)

### Key exchange

Not every application protocol uses TLS. Some protocols, such as NFS and CIFS, rely on a key negotiated by the authentication protocol to sign and potentially encrypt messages. Other protocols might support TLS but not require it. As such, having the client and server agree on a session key can be useful. We accomplish this by having the client and server perform an [Elliptic Curve Diffie-Hellman](http://en.wikipedia.org/wiki/Elliptic_curve_Diffie%E2%80%93Hellman) (ECDH) key exchange. The resulting shared secret can be used to sign and encrypt messages using the SHA-1 hash algorithm and 128-bit or 256-bit AES.

Other hash and encryption algorithms may be used without changing the base protocol; these are the ones we have defined for now, which are based on what contemporary Kerberos implementations do. A well-designed implementation should be field-upgradable to support new algorithms.

We also provide a pseudo-random function so applications that do their own encryption or integrity protection can derive a key.

### Mutual authentication

Again, for applications that don’t use channel-bound TLS, it’s nice for the client to be able to authenticate the server, not just the converse. We do this by allowing the server to send back a certificate, just as it would in TLS. In this case, we actually use standard X.509/PKIX certificates, rather than Persona ones: we felt that trading architectural symmetry for the ability to re-use existing keying infrastructure was the right compromise.

(We could also specify Persona certificates, but that would require IdPs to issue host certificates. And given IdPs are ultimately authenticated using X.509 certificates, this approach has questionable value. Its primary advantage is that it would sidestep the CA infrastructure for host authentication, as only IdPs would need to be issued X.509 certs.)

### Fast re-authentication

Applications such as mail clients tend to make and tear down a lot of connections, most often concurrently. Explicitly signing in with Persona and/or performing public key operations in JavaScript would make Persona for a non-starter for these protocols. To solve this, we allow the server to return a cookie (called a “ticket”, a homage to Kerberos) which can be used to subsequently re-authenticate. Unlike web cookies, this cookie is bound to a cryptographic key, so subsequent authentications have the same degree of security as the original private key signed one. Instead of sending an assertion signed with a user’s private key, we sign the assertion using a HMAC with a key derived from the initial key exchange.

### Putting it all together

An assertion for authenticating to the IMAP server on mail.example.com might look like the following:

```
{
"opts": [
"ma"
],
"exp": 1360158396188,
"ecdh": {
"crv": "P-256",
"x": "JR5UPDgMLFPZwOGaKKSF24658tB1DccM1_oHPbCHeZg",
"y": "S45Esx_6DfE5-xdB3X7sIIJ16MwO0Y_RiDc-i5ZTLQ8"
},
"nonce": "bbqT10Gyx3s",
"aud": "urn:x-gss:imap/mail.example.com"
}
```

The “ma” in the “opts” claim indicates that mutual authentication is desired. The “ecdh” claim contains the selected ECDH curve and client public key, for session key agreement. The “nonce” claim is used for mutual authentication, to bind the request and response assertions together. The remaining claims, “exp” and “aud” are identical to a Persona web assertion, except the audience contains a service principal name. (We have omitted the signature on the assertion and the user’s certificate, as these do not differ from the web use case.)

One other difference is that the server will send back its own assertion, either signed in the exchanged key or in a long-term private key. This looks something like the following:

```
{
"exp": 1362960258000,
"nonce": "bbqT10Gyx3s",
"ecdh": {
"x": "bvNF6V1rpMeQyGOKCj0kBaOaSh3tlhUcbffaji4uCEI",
"y": "Iuqs650FXzXFUD9kHknETfbqiB8XBbCHlJXoysx3rvw"
},
"tkt": {
"tid": "Jgg7vKX2sEKlCWBfmLTg_n4qz3NVZxOU-a2B4qYMkXI",
"exp": 1362992660000
}
}
```

The response assertion contains an advisory expiry time, an echoed nonce, the server’s ECDH public key, and an optional ticket for fast re-authentication.

## Implementation

Protocol specifications are all very well, but it’s also important to have an implementation that will work with existing applications. Ours is available at [https://github.com/PADL/gss_browserid](https://github.com/PADL/gss_browserid).

The client side runs on OS X, and the server should run on any modern POSIX-compliant system that has a Kerberos library, [libcurl](http://curl.haxx.se/) and [OpenSSL](http://www.openssl.org/) installed. Porting the client UI to other operating systems should be reasonably straightforward; the most difficult part is finding a library that can display a web browser control, and implementing a function that returns an assertion. On OS X, we use the built-in WebKit framework to accomplish this. (There is also the beginning of a Windows port that uses MSHTML, but it isn’t fully baked yet. We expect it should be complete by the end of 2013.)

Our implementation is divided into two components, libbrowserid and mech_browserid, which we discuss below.

### libbrowserid

[libbrowserid](https://github.com/PADL/gss_browserid/tree/browserid/libbrowserid) is a general-purpose C library for acquiring and verifying Persona assertions. You can if you wish build it without building the SASL/GSS-API mechanism; this might be useful if you want a native code local verifier. (As with all local verifiers, beware that the Persona protocol is subject to change. We’ll be tracking any changes.)

If you want a taste of how you might use this library independently of SASL/GSS-API, have a look at [sample/bidget.c](https://github.com/PADL/gss_browserid/blob/browserid/sample/bidget.c) and [sample/bidverify.c](https://github.com/PADL/gss_browserid/blob/browserid/sample/bidverify.c): these two short programs (~50 LOC) demonstrate respectively how to acquire and verify a Persona assertion using libbrowserid.

### mech_browserid

The [mech_browserid](https://github.com/PADL/gss_browserid/tree/browserid/mech_browserid) module is a plugin, built on top of libbrowserid, that allows SASL and GSS-API consuming applications to seamlessly use Persona. You’ll need to have a recent version of [MIT Kerberos](http://web.mit.edu/kerberos/) or [Heimdal](http://www.h5l.org/) installed, as well as [Cyrus SASL](http://asg.web.cmu.edu/sasl/sasl-library.html) (if your application uses SASL). You will also need a recent version of OpenSSL with ECDH enabled, as well as libcurl; the versions that ship with OS X 10.8 work fine. (Building against the version of Heimdal that ships with OS X is difficult and not recommended.)

To build, run the “autogen.sh” script in the top-level directory, and then it’s the usual “configure” and “make” dance. You may need the –with-krb5 option to configure in order to specify where you installed Kerberos. The build/ subdirectory has some sample scripts for invoking configure, which you can tweak to suit. You will need to build with -DGSSBID_DEBUG in order for the SASL examples to work, for the reason described in [#ifdef GSSBID_DEBUG on GitHub](https://github.com/PADL/gss_browserid/blob/browserid/libbrowserid/bid_webkit.m#L551).

For example, assuming Kerberos has been installed in /usr/local, one might type:

```
% ./autogen.sh
% OBJC=clang CC=clang CXX=clang++ OBJCFLAGS="-g -Wall -DGSSBID_DEBUG -Wno-deprecated-declarations" CXXFLAGS="-g -Wall -DGSSBID_DEBUG -Wno-deprecated-declarations" CFLAGS="-g -Wall -DGSSBID_DEBUG -Wno-deprecated-declarations" ./configure --with-krb5=/usr/local
% make
% sudo make install
```

After you’ve installed (with “make install”) you’ll need to add a line to /usr/local/etc/gss/mech that looks like the following:

```
browserid-aes128 1.3.6.1.4.1.5322.24.1.17 /usr/local/lib/gss/mech_browserid.so
```

Replace /usr/local in both the configuration file and library paths above with the prefix in which you installed Kerberos and mech_browserid, respectively.

### Testing

You can test gss_browserid using the samples distributed with the Cyrus SASL distribution. You will need a recent version of Cyrus SASL that supports GS2 (you can tell by whether libgs2.so is installed into the sasl2 directory). If you’re not configuring mutual authentication (i.e. you haven’t generated a server certificate) then you will also need a small patch to Cyrus, which can be found in [contrib/cyrus-sasl.patch](https://github.com/PADL/gss_browserid/blob/browserid/contrib/cyrus-sasl.patch). Apply that and “make install” in the plugins directory of Cyrus SASL before running the tests.

First, make sure your SASL_PATH environment variable is set to where the GS2 SASL plugin is installed. For example, if the GS2 SASL plugin is installed in /usr/local/lib/sasl2:

```
% export SASL_PATH=/usr/local/lib/sasl2
```

Start the server program below, replacing host.example.com with your canonical hostname (but not “-s host”, as that specifics the service name):

```
% server -c -p 5556 -s host -h host.example.com
```

And then the client:

```
% client -c -p 5556 -s host -m BROWSERID-AES128 host.example.com
```

If it works, you should see the Persona sign-in page pop up (remember, this currently works on OS X only). After typing in your e-mail address and password, you should be able to authenticate (you will see “successful authentication” on the server side).

If you try it again, it should work without prompting, as you will have a cached ticket. You can list your tickets with the bidtool command:

```
% bidtool tlist
Ticket cache: /Users/lukeh/Library/Caches/com.padl.gss.BrowserID/browserid.tickets.json
Identity Audience Issuer Expires
--------------------------------------------------------------------------------
lukeh@padl.com host/host.example.com login.persona Tue Apr 23 22:40:36 2013
```

To remove the ticket cache, use “bidtool tdestroy”. (Kerberos users should find these commands familiar. Other useful commands include “bidtool rlist”, to show the replay cache, and “bidtool certlist”, to show the IdP public key cache. There are similar commands to purge expired entries, and to destroy, each type of cache.)

If it doesn’t work, well: it’s true that error reporting is sub-optimal right now, and debugging can be difficult. Ensure you:

- built libbrowserid with -DGSSBID_DEBUG;
- that SASL_PATH points to a directory in which libgs2.so resides, and
- that /usr/local/etc/gss/mech (replacing path as appropriate) points to where mech_browserid.so is installed.

If you see the Persona dialog but authentication fails, make sure the hostname you specified matches the name the server is using. If you’re comfortable with a debugger, setting a breakpoint on gssBidInitSecContext can be useful. If all else fails, [drop me a line](mailto:lukeh@padl.com) or post to the [dev-identity](https://lists.mozilla.org/listinfo/dev-identity) mailing list.

To keep this article short, we haven’t touched on configuring mutual authentication (or, more correctly, server authentication). Configuring this is briefly described in [README.md](https://github.com/PADL/gss_browserid/blob/browserid/README.md) in the top-level directory of the source distribution. gss_browserid can also do other fun things such as surface certificate attributes to applications, even if they’re embedded in a SAML assertion tunnelled inside the user’s certificate. We’ll talk about those things in a future article.

## Applications

So, why would you want to use this when you can authenticate to your (for example) IMAP server using passwords, DIGEST-MD5 or Kerberos? Here are some possibilities: your webmail provider wants to standardize on Persona authentication and deprecate password-based authentication (it could happen). You work in an enterprise that requires some complex multi-factor authentication using, say, hardware tokens and client certificates: it’s relatively trivial to build a Persona IdP than a new authentication protocol, so this allows you to deploy this authentication policy with all clients that support GSS-API or SASL. (This might be particularly useful for accessing e-mail outside the firewall.)

In this example, we demonstrate how to use Persona to authenticate using the OS X Mail client. You should be warned that this is not for the faint of heart: it involves installing a plugin that fools Mail into using Persona when you ask for Kerberos authentication. (Note that this will prevent you from using Kerberos from Mail. And it is completely unsupported by Apple. But this is the Mozilla Hacks blog, right?)

First, you’ll need to setup your IMAP server to support Persona, but as long as it supports Cyrus SASL, and you’ve got the SASL examples above working on the same machine, it should “just work”. Again, make sure SASL_PATH is set correctly and the IMAP server has read/write access to its authority and replay cache files (on OS X, these will be created in ~/Library/Caches/com.padl.gss.BrowserID; on other platforms, they will be in /tmp or $XDG_RUNTIME_DIR).

You can test your IMAP SASL configuration with the cyradm tool (presuming you’re using Cyrus imapd). For example:

```
% cyradm --user lukeh@lukktone.com --port 143 --auth BROWSERID-AES128 rand.mit.de.padl.com
```

If there are any problems getting this to work (you don’t see the cyradm prompt with your IMAP server name), then you’ll need to troubleshoot this before proceeding. Otherwise, proceed to install the “masquerade as Kerberos” plugin, which may be found in the [contrib/BrowserIDHelper](https://github.com/PADL/gss_browserid/tree/browserid/contrib/BrowserIDHelper) directory of gss_browserid. In that directory, you can simply type “make && make install” to build and install. (To remove it, delete ~/Library/Mail/Bundles/BrowserIDHelper.mailbundle.)

You will also need to modify the application sandbox so that the gss_browserid mechanism and its configuration files can be loaded. As root, apply the patch in application.sb.patch, adjusting paths as necessary. Then, delete ~/Library/Containers/com.apple.mail/Container.plist, and start Mail.

In Preferences/Accounts/Advanced for the mail server that you wish to authenticate to with Persona, set Authentication to “Kerberos Version 5 (GSSAPI)”. This kludge is necessary because Mail is not SASL mechanism agnostic; it only supports a fixed set of mechanisms, such as GSSAPI and DIGEST-MD5.

![](../../assets/7da76a2553b70e9c.png)


All going to plan, you should be prompted to sign in:

![](../../assets/eba9f10af70c9814.png)


There you have it.

## Conclusion

It’s possible to use Persona for non-web applications today, but there’s still a way to go before it’s ready for prime time. We want to finish defining the protocol and publish it as an RFC, which in turn will require the underlying BrowserID (and JOSE) specifications to be stable. The implementation needs testing with more applications and complete ports to Linux and Windows. Applications that assume a specific set of SASL or GSS-API mechanisms need to be updated to be mechanism agnostic. Enterprise use cases will require IdPs that can bridge from Active Directory and other common authentication providers.

We look forward to seeing how Persona evolves and how it can be applied to the non-web in the coming months.

Finally, if you are planning on building your own implementation of [draft-howard-gss-browserid](http://tools.ietf.org/html/draft-howard-gss-browserid), please get in touch [directly](mailto:lukeh@padl.com) or on the [ietf-kitten](http://tools.ietf.org/wg/kitten/) mailing list.

### Acknowledgments

My draft co-author, Nico Williams, provided much advice on the protocol design. The gss_browserid implementation was based on the Moonshot GSS EAP mechanism, sponsored by JANET(UK). Thanks also to Sam Hartman at Painless Security, and the identity team at Mozilla.

## About
[
Luke Howard ](http://www.lukehoward.com)

Luke Howard founded PADL Software in 1999. He is the author of RFC 2307 and has contributed to many open source projects including OpenLDAP, MIT Kerberos and Heimdal. He built the first commercially shipping Active Directory replacement, XAD, and has worked for both Apple and Novell. In 2013, he is working on bringing Mozilla Persona to non-web applications. He is also a composer and musician who has played on more than 50 albums and once made lunch for Brian Eno.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 3 comments

JoakimApril 29th, 2013 at 03:33Robert Nyman [Editor]April 29th, 2013 at 23:21Kathy WishartApril 30th, 2013 at 20:43