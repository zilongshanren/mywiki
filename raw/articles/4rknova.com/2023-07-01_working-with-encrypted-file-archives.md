---
title: Working with encrypted file archives
url: https://www.4rknova.com/blog/2023/07/01/encrypted-archives
author: Nikolaos Papadopoulos
published: '2023-07-01'
source_blog: Nikos Papadopoulos - Portfolio
source_site: https://www.4rknova.com/
category: graphics
fetched: '2026-04-19'
---

There are many use cases for creating encrypted file archives. One such use case is managing file backups. In this short blog post we look into how to use tar and gpg to achieve that.

# Creating the archive

Generating an encrypted archive is fairly trivial:

$ tar -cvzf - directory | gpg -c > directory.tar.gz.gpg

In the above snippet, tar creates a compressed archive of the directory specified, using gzip, and pipes the data to gpg for encryption, before writing to the output file. The *‘-c’* flag instructs gpg to create a prompt for the user to enter a passphrase that will serve as the encryption key.

Alternatively, the passphrase can be inlined as shown below:

$ tar -cvzf - directory | gpg -c --passphrase a_passphrase > directory.tar.gz.gpg

The *’–passphrase’* switch will suppress the prompt and will use the next argument as the passphrase.

There are many ways to generate a random key, a simple approach is to use tr and /dev/urandom.

$ tr -dc A-Za-z0-9 </dev/urandom | head -c 13; echo

# Extracting the archive

It’s equally simple to decrypt and decompress the encrypted file as shown below.

$ gpg -d directory.tar.gz.gpg | tar -xvzf -