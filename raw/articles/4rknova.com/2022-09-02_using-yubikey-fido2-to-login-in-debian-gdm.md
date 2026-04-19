---
title: Using Yubikey FIDO2 to login in Debian/GDM
url: https://www.4rknova.com/blog/2022/09/02/yubikey-login
author: Nikolaos Papadopoulos
published: '2022-09-02'
source_blog: Nikos Papadopoulos - Portfolio
source_site: https://www.4rknova.com/
category: graphics
fetched: '2026-04-19'
---

This guide shows how to add Yubikey U2F authentication as an optional login method in Debian with Gnome desktop environment. Using this configuration, if the key is not present on the computer, the user will still be able to login by means of another method. Depending on your security needs this may or may not be desirable.

# Resetting the FIDO2 Yubikey application

If you get the PIN wrong a few times, the key will be locked and you will have to reset the FIDO2 application. Here’s how to do that:

- Download the
[Yubikey Manager](https://www.yubico.com/products/services-software/download/yubikey-manager)application. - Insert your Yubikey.
- Run the Yubikey Manager and navigate to Applications > FIDO2.
- Click Reset FIDO, then YES.
- Follow the prompts from Yubikey Manager to remove, re-insert, and touch your key.

# Install dependencies

Install the dependencies with:

$ sudo apt install libpam-u2f

# Associate a U2F key with your account

We want to associate a key to a specific user so the configuration will live in the user’s home directory.

Insert your Yubikey and issue the following commands:

$ mkdir -p ~/.config/Yubico $ pamu2fcfg > ~/.config/Yubico/u2f_keys

When your device begins flashing, touch the metal contact to confirm the association.

# Enable U2F as a login method for GDM

Edit PAM configuration for GDM

$ vim /etc/pam.d/gdm-password

At the top of the file, before the common-account include line add the following:

```
auth sufficient pam_u2f.so
```


This will add your yubikey as a login mechanism but will still allow using alternative login methods (eg. password, fingerprint, etc.).