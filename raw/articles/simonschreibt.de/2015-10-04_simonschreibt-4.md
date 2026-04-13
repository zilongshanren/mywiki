---
title: Simonschreibt.
url: https://simonschreibt.de/wft/watchdog-mail/
author: Simon
published: '2015-10-04'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

Sending mails as an status or error report is essential because you don’t want to manually check all the folders and images for an error every day. Whenever a higher pixel difference (than our threshold) appears, a mail is sent out to a responsible person. This mail looks like below and contains:

- name of the material
- the newest image
- the older image
- a difference image (shows differences via blue pixels, created via
[compare process](http://simonschreibt.de/wft/watchdog-compare)) - a link to the difference via browser (see the chapter about the
[Watchdog Gallery](http://simonschreibt.de/wft/watchdog-gallery)) - the direct link/path to the image files

![](../../assets/ebe450f92e093152.png)

![](../../assets/b8e5764b091814ab.png)


The program we’re using for sending these mails is called [Blat](https://simonschreibt.de/www.blat.net) and can be accessed via command line which makes it easy to use it via BAT/C# to send mails. There are different ways to send a mail but I preferred to first write the whole Mail-HTML-Code into a TXT file and then hand it over to the mail program:

blat.exe mailcontent.txt -server yourserver.de -f sender@yourserver.com -u username -pw god -to you@mailprovider.de -subject “Hello World” -html

If you want to embed the pictures like we did, you have to already refer their file-names (without path) in the HTML code of your mail …

…

<img src=”cid:test1.png“>

…

… and then use the **-embed** parameter to embed them:

blat.exe mailcontent.txt -server yourserver.de -f sender@yourserver.com -u username -pw god -to you@mailprovider.de -subject “Hello World” -html -embed “d:\test1.png” -embed “d:\test2.png” -embed “d:\diff.png”

I would suggest to put the pixel difference directly into the mail-subject to be able to see how drastic the change is even without opening the mail (but just looking at the list in your inbox):

![](../../assets/34729c737321fc8c.png)


When the program finished it sends a final conclusion mail. Two good reasons to do this:

- There are two reasons for
**not**getting error reports:**1.**There are no errors**2.**the whole script broke. If there’s no final report, you never can be sure that the system still works if no error happened (which is hopefully the case most of the time) - You can add some nice global statistics into your report to impress people:
![](../../assets/ea612f129b6a4df1.png)


Let’s now talk about how to keep overview about all this data.