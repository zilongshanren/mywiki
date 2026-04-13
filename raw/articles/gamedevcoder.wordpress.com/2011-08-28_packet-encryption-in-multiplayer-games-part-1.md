---
title: Packet encryption in multiplayer games – part 1
url: https://gamedevcoder.wordpress.com/2011/08/28/packet-encryption-in-multiplayer-games-part-1/
published: '2011-08-28'
source_blog: Gamedev Coder Diary
source_site: https://gamedevcoder.wordpress.com
category: game programming
fetched: '2026-04-13'
---

Sending unencrypted data between peers in multiplayer game can make your game vulnerable to many kinds of hacker attacks.

However, as surprising as it may sound not all multiplayer games require data encryption to stay secure. In some cases only part of the data transmitted requires it and sometimes encryption isn’t needed at all. Instead of encrypting, it’s often enough to verify that the packet received from remote peer isn’t “hacked”. Now, what that means is a very game specific thing. For example, in terms of FPP shooter games like Quake or Unreal such packet verification might, for example, include checking whether the player’s velocity is within reasonable range. If the player was attempting to move faster than the game allows, we could simply consider his/her game being hacked.

It’s great if you’re able to validate data packet in this way and, if possible, it’s probably the best way of detecting if your multiplayer game gets hacked. However, in the case where full packet validation can’t easily be done for some reason or when you not want packet content to be easily readable by anyone (e.g. contains secret text chat), your next option is to encrypt the data using one of the popular encryption algorithms.

There’s large number of methods available but you could probably split them into 2 groups: symmetric key based and asymmetric key based methods. The first group uses one key to encrypt and decrypt the data while the second requires 2 keys – one (public) key for encryption and one (private) key for decryption. For more explanation see [this article on Tech-FAQ](http://www.tech-faq.com/symmetric-and-asymmetric-ciphers.html).

Since asymmetric key based methods are more secure, ideally we’d just be using full-blown asymmetric key based [RSA algorithm](http://en.wikipedia.org/wiki/RSA) for all of our communication. It certainly is very safe method given that:

(a) the keys are large enough (e.g. [2048+ bits](https://en.wikipedia.org/wiki/Key_size))

(b) we are able to verify the public key of remote peer.

While (a) might only create performance challenge, the (b) is difficult to solve in general. The question one shall ask here is: how can I verify that the public key I have received from remote peer hasn’t been hacked halfway through? This problem is well known as MITM ([“Man In The Middle” attack](http://en.wikipedia.org/wiki/Man-in-the-middle_attack)) and the way modern world deals with it is via [Public Key Infrastructure](http://en.wikipedia.org/wiki/Public_key_infrastructure) (PKI). The key element of PKI are [Certificate Authorities](http://en.wikipedia.org/wiki/Certificate_authority) which issue reliable certificates to others. The whole PKI is organized in a tree like structure. Some Certification Authorities issue [root certificates](http://en.wikipedia.org/wiki/Root_certificate) to other Certification Authorities, and then Certification Authorities issue certificates to anyone else. To be able to make use of PKI one needs root certificate that would let them get certificate of any other entity. Such root certificates are typically stored hidden in hardware and/or software (e.g. in your web browser).

One might say all this isn’t very good solution because it is based on assumption that we have some non-hacked root certificate. But in the very darkest scenario you could imagine your hardware and software could be totally hacked and so all your root certificates could be modified! That is true but no matter how much you complain about this solution, it seems this is the best one that humanity came up with so far when it comes to reliable encrypted communication over the internet.

So… ideally what you might want to do when making very secure multiplayer game (that is one that encrypts all of its data) is you should first get certificate issued by CA. Then you should use it to get individual peers to exchange public keys via your certified “master server”. Once that’s done you can start secure communication directly between peers.

Getting certificate from CA sounds scary if you’re a small developer that wants to release multiplayer PC game (assuming you’re not using any 3rd party services offering secure authentication). So, instead of going hardcore you can stick with just using some asymmetric key based method and assume (somewhat naively) that the public key won’t be hacked while exchanging them between peers. Additionally, to somewhat improve security, you could at least do some cheap and simple encryption when exchanging public keys just so they’re not plain readable. However, no matter what, keep in mind that the most common [MITM attack](http://en.wikipedia.org/wiki/Man-in-the-middle_attack) is done on a game running locally. And honestly, when the game is running locally there’s no way of preventing it from being hacked – this is simply because the hacker can see your application process’ memory and so he or she can do whatever they want with messages you send or receive. There is general solution to these problems which is: running your game on [dedicated servers](https://en.wikipedia.org/wiki/Game_server#Dedicated_server) but that is beyond the topic of this post.

Note also that an asymmetric key based encryption might be an overkill for your game due to unacceptable performance. For this reason some multiplayer games, in particular fast paced “real real-time” games, decide to use different approach – a combination of symmetric and asymmetric key based methods. An asymmetric one is typically only used to initially exchange (or establish) symmetric key that is then used for regular data encryption using symmetric key based encryption. Note: while it might be okay for computer games it is most likely not okay for businesses where money is involved.

A common combination of asymmetric and symmetric key based methods used in multiplayer games is, for example, [Diffie-Helman](http://en.wikipedia.org/wiki/Diffie%E2%80%93Hellman_key_exchange) and [Blowfish](http://en.wikipedia.org/wiki/Blowfish_(cipher)) algorithms. Fortunately implementations of both of them are freely available, for example in [OpenSSL](http://www.openssl.org/) library.

In the next part of the article I’m going to present a small C++ library that could be used to facilitate both key-exchange and encryption of the data using mentioned algorithms.

Update: part 2 available [here](https://gamedevcoder.wordpress.com/2011/09/06/packet-encryption-in-multiplayer-games-–-part-2).