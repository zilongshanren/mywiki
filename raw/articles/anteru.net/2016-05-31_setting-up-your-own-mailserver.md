---
title: Setting up your own mailserver
url: https://anteru.net/blog/2016/setting-up-your-own-mailserver
published: '2016-05-31'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

Today we’re going to look at yet another use for [your own home server](https://anteru.net/blog/2015/01/19/2678/) - handling all your emails. There’s a couple of reasons why you want to do this, so let’s start with some motivation. I always used to download my emails from my email account using POP3. That works fine as long as you only use one machine to access it, as the emails get immediately deleted after fetching. This didn’t use to be an issue at first for me, but once you get access to your mail account from your mobile phone and notebook it starts to become an issue.

The easy solution is to change it to IMAP and just let all emails on the server. While that works, I did accumulate a lot of emails over the years - my inbox contains several tens of thousands of emails, and uses a couple GiB of disk space. Even though space is not so much of an issue these days, it’s still slow to sync with an inbox that has thousands of emails, and there’s not much reason for me to keep a lot of the old emails around.

With a home server in place, it was time to consolidate this. My goal was to achieve the following:

- Have all emails on my server, so I don’t need to worry about backups. That means the server needs to pull them from my web accounts.
- Have all emails in an easy to process format - something where I can search through them manually, if ever needed.
- Remove old emails from my web accounts after a grace period.

Turns out, all of this is possible, with the help of a couple tools and some scripting. Let’s dive in how to do this!

## The mail server

First we need a mail server. The mail server is the thing we’ll connect to in the future - my Thunderbird at home doesn’t connect to my web account any more, but to my home server instead. My server of choice is [dovecot](http://www.dovecot.org/) which you can install on Ubuntu using `apt install dovecot-imapd`

. Next we need to configure it. There’s a couple of files we need to edit. In the following, I’ll assume we’re going to store our emails on `/tank/mail`

in a per-user directory.

In `/etc/dovecot/dovecot.conf`

, add `protocols = imap`

as the last line to enable IMAP. Next, you’ll need to edit `/etc/dovecot/conf.d/10-mail.conf`

where you specify the `mail_location`

. I’m using `mail_location = maildir:/tank/mail/%u/.maildir`

- `maildir`

ensures the emails are stored in the [maildir](https://en.wikipedia.org/wiki/Maildir) format, which you can for instance read using the Python [mailbox](https://docs.python.org/3.5/library/mailbox.html) module. If you don’t set this up, a default path would be used which requires a home directory to exist for the user `vmail`

.

We also need to setup a way to connect to the server, so we edit `/etc/dovecot/conf.d/10-auth.conf`

and enable the `passwdfile`

authentication - just remove the `#`

at the beginning of the `!include auth-passwdfile.conf.ext`

line. You can also disable `system`

authentication by adding a `#`

there.

Before we continue, I’m going to set up a new user which will *own* all the emails - this user will be called `vmail`

. This is straightforward:

```
$ adduser --disabled-password --shell=/bin/false --no-create-home vmail
$ chown -R vmail /tank/mail
```


We also need the user-id and the group-id of that user - check it using:

```
id vmail
```


With that, we can finally add users to access our email server. I have a couple of mailboxes and one user per mailbox. I’ll be using a simple password file here. In `/etc/dovecot/conf.d/10-auth.conf`

, check that `auth_mechanisms = plain`

is set, as well as `disable_plaintext_auth = no`

. By default, dovecot only allows secure connections, but here we’re connecting within our local network only, so we don’t have to bother setting up SSL. Now we’re ready to add the users - put them into `/etc/dovecot/users`

, with one line per user like this:

```
username:{plain}passwort:vmail-user-id:vmail-group-id::
```


`vmail-user-id`

and `vmail-group-id`

is the user and group id of the `vmail`

user, respectively. Phew! You can actually try to connect now using the username and (plain-text) password you just specified. Make sure to *not* use `mail`

as the username – that one already exists and dovecot will not let you log in as that user. I’ve been using one user name per mailbox, as the default path we’ve set up above for the mail location has `%u`

in it – that’s will get replaced with the username.

Note

If you’re not comfortable with plain because you’re not the only root
on your server, you can also use [encrypted
passwords](http://wiki2.dovecot.org/Authentication/PasswordSchemes).

## Getting email

The next part is to load the emails from your web account into dovecot. The easiest solution I’ve found is to stuff them directly into dovecot using [getmail](http://pyropus.ca/software/getmail/). getmail can write into a maildir directly, and dovecot - as we’ve set it up above - stores all emails in a maildir, so let’s have getmail fetch it right in there!

Installing getmail is simple, just use `apt install getmail`

, and then we need to set up one file per mail account we want to fetch. Those files go into `/etc/getmail`

, and look like this (let’s call it `your-email_example_com.conf`

):

```
[retriever]
type = SimpleIMAPSSLRetriever
server = mymail.server.com
username = your-email@example.com
password = swordfish
[destination]
type = Maildir
path = /tank/mail/your-email_example_com/.maildir/
user = vmail
[options]
verbose = 2
delete = false
messsage_log_syslog = true
read_all = false
delivered_to = false
received = false
```


All that is left is to set up a cron job to fetch the emails. I’m running it every 5 minutes - this is how my `/etc/cron.d/get-mail`

job looks like:

```
PATH="/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin"
*/5 * * * * root getmail --rcfile your-email_example_com.conf --getmaildir /etc/getmail/
```


You can pass in as many `--rcfile`

options into getmail as you want. Notice that it’s also possible to use IMAP idle to get instant emails - it’s a bit tricky to set up and I didn’t bother with it as I don’t need this.

All right, emails are coming in, now we only need to clean up the mail folder somehow!

## Cleaning up

Unfortunately, I didn’t find a solution for mail cleanup, so I ended up writing [my own script for it](https://github.com/anteru/delete-old-email). It works very similar to getmail: For every account, you set up a configuration file. For the account above, we’d put the following content into `/etc/delmail/your-email_example_com.conf`

:

```
[mailbox]
server = mymail.server.com
username = your-email@example.com
password = swordfish
[backup]
type = Maildir
path = /tank/mail/your-email_example_com/.backup/
[options]
min_age = 28
```


`min_age`

specifies the age of emails before they get deleted. I’m also erring on the side of safety, so all emails the script is about to delete will be backed up into the path specified in the `[backup]`

section.

All that is left is now a cron job for this, which doesn’t have to run with the same frequency. Here’s the contents of my `/etc/cron.d/delete-mail`

:

```
PATH="/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin"
2 */4 * * * vmail delete-old-emails.py -config /etc/delmail/your-email_example_com.conf
```


Notice that the server only handles receiving emails, not sending them. For sending, I still go directly to my web email server, but I store the copy locally if sending from home.

And that’s it! I’ve been using this setup since a couple of years now, and so far, I’m very pleased. While traveling, I can always look up my recent emails. At home, I have access to *all* emails I have ever received, and I have every backed up nicely. My web accounts run with 100 MiB of storage instead of several GiB as they used, and if I fire up my mobile phone or notebook occasionally, there’s only a couple of emails it needs to synchronize because the web inbox is nearly empty all the time.