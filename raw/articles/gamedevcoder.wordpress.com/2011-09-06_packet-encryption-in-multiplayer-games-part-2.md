---
title: Packet encryption in multiplayer games – part 2
url: https://gamedevcoder.wordpress.com/2011/09/06/packet-encryption-in-multiplayer-games-part-2/
published: '2011-09-06'
source_blog: Gamedev Coder Diary
source_site: https://gamedevcoder.wordpress.com
category: game programming
fetched: '2026-04-13'
---

The following is continuation of my recent [Packet encryption in multiplayer games – part 1](https://gamedevcoder.wordpress.com/2011/08/28/packet-encryption-in-multiplayer-games-part-1/) article.

In this article I’m going to present sample implementation of the encryption helper that might be used to establish connection using [Diffie-Helman](http://en.wikipedia.org/wiki/Diffie%E2%80%93Hellman_key_exchange) algorithm and then send and receive messages using [Blowfish](http://en.wikipedia.org/wiki/Blowfish_(cipher)) algorithm. All based on [OpenSSL](http://www.openssl.org/) implementation.

Please note that this code is written for educational purposes only and that it is probably far from quality acceptable for exchanging data that needs to be really secure. Also, it is worth reminding that in general the algorithms used here, i.e. Blowfish and Diffie-Helman are considered relatively easy to hack (far from RSA). Using them is more of a “no trespassing” sign to the hackers than the actual protection.

Below is how you’re supposed to use the code.

**Step 1**

First off, let’s declare some buffer and initialize OpenSSL library.

Note: We’re going to test sending messages of both 8-byte aligned and non-8-byte aligned sizes below. This is particularly interesting due to Blowfish algorithm operating on chunks of 8 bytes.

#include "EncryptionHelper.h" void EncryptionHelper_UnitTest() { const int UNIT_TEST_BUFFER_SIZE = 256;

// Make it 8-byte aligned

const int UNIT_TEST_MSG0_SIZE = UNIT_TEST_BUFFER_SIZE - 8;

// Make it non 8-byte aligned

const int UNIT_TEST_MSG1_SIZE = UNIT_TEST_BUFFER_SIZE - 9; int length; unsigned char buffer[UNIT_TEST_BUFFER_SIZE];

// Initialize OpenSSL

EncryptionHelper_StartupOpenSSL();

**Step 2**

Next initialize encryption helper for Alice and Bob (why [Alice and Bob](http://en.wikipedia.org/wiki/Alice_and_Bob)?). If used for multiplayer game, Alice would only be created on one machine whereas Bob would only be created on another machine. It’s up to user to decide who is Alice and who is Bob but in order to get things working with this library it is necessary that one of them is Alice and the other one is Bob.

Note: the ‘check’ is similar to an assertion macro; the difference is that it evaluates expression regardless of whether assertions are enabled or not.

// Initialize Alice and Bob

EncryptionHelper* alice = EncryptionHelper_Create(true); EncryptionHelper* bob = EncryptionHelper_Create(false); assert(alice && bob); check(EncryptionHelper_IsAlice(alice)); check(!EncryptionHelper_IsAlice(bob));

**Step 3**

We’re now going to generate “exchange data” on Alice side. This “exchange data” contains Alice’s public key as well as 2 parameters, P and G, as needed by Diffi-Helman algorithm. Once message is successfully sent (from Alice to Bob), we can mark it as sent.

// Alice generates exchange data and sends it to Bob

check(EncryptionHelper_GetExchangeData(alice, buffer, UNIT_TEST_BUFFER_SIZE, &length));

// [ sending… ]

EncryptionHelper_MarkExchangeDataSent(alice); check(EncryptionHelper_IsExchangeDataSent(alice));

**Step 4**

Once Bob receives “exchange data” from Alice and verifies its correctness, he can then generate his own “exchange data” (containing Bob’s public key) and send it to Alice. Once sent, Bob marks message as sent.

// Bob receives exchange data and sends another exchange data to Alice

check(EncryptionHelper_ReceiveExchangeData(bob, buffer, length)); check(EncryptionHelper_IsExchangeDataReceived(bob)); check(EncryptionHelper_GetExchangeData(bob, buffer, UNIT_TEST_BUFFER_SIZE, &length));

// [ sending… ]

EncryptionHelper_MarkExchangeDataSent(bob); check(EncryptionHelper_IsExchangeDataSent(bob));

**Step 5**

Once Alice receives “exchange data” from Bob, the communication starts. We’re now ready to send and receive messages between Alice and Bob.

// Alice receives exchange data from Bob

check(EncryptionHelper_ReceiveExchangeData(alice, buffer, length));

// Authentication done! // Communication begins…

**Step 6**

Below Bob sends test message to Alice, Alice receives it and verifies that the message is correct.

// Bob encrypts data for Alice; Alice decrypts the data

for (int i = 0; i < UNIT_TEST_MSG0_SIZE; i++) buffer[i] = i; check(EncryptionHelper_Encrypt(bob, buffer, UNIT_TEST_BUFFER_SIZE, UNIT_TEST_MSG0_SIZE, &length)); check(EncryptionHelper_Decrypt(alice, buffer, length, &length)); for (int i = 0; i < length; i++) check(buffer[i] == i);

**Step 7**

And now communication going the other way – Alice sends message to Bob.

// Alice encrypts data for Bob; Bob decrypts the data

for (int i = 0; i < UNIT_TEST_MSG1_SIZE; i++) buffer[i] = i; check(EncryptionHelper_Encrypt(alice, buffer, UNIT_TEST_BUFFER_SIZE, UNIT_TEST_MSG1_SIZE, &length)); check(EncryptionHelper_Decrypt(bob, buffer, length, &length)); for (int i = 0; i < length; i++) check(buffer[i] == i);

**Step 8**

When done, deinitialize encryption helpers for both Alice and Bob.

// Shut down Alice and Bob

EncryptionHelper_Destroy(alice); EncryptionHelper_Destroy(bob); }

Get the source code from here [EncryptionHelper.cpp](https://github.com/macieks/encryption_diffi_helman_blowfish/blob/master/EncryptionHelper.cpp) and here [EncryptionHelper.h](https://github.com/macieks/encryption_diffi_helman_blowfish/blob/master/EncryptionHelper.h) and have fun!

Note: The code has only been tested on windows. Obviously, you’ll need to download [OpenSSL](http://www.openssl.org/) library to compile it.