---
title: MediaWiki and ModSecurity
url: http://hacksoflife.blogspot.com/2010/11/mediawiki-and-modsecurity.html
author: Benjamin Supnik
published: '2010-11-10'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

The server encountered an internal error or misconfiguration and was unable to complete your request.My host finally figured out what was going wrong. This was in /www/logs/error_log:

Please contact the server administrator, webmaster@xsquawkbox.net and inform them of the time the error occurred, and anything you might have done that may have caused the error.

More information about this error may be available in the server error log.

Wed Nov 10 12:48:15 2010] [error] [client 71.248.161.106] ModSecurity: Access denied with code 500 (phase 2). Pattern match "(insert[[:space:]]+into.+values|select.*from.+[a-z|A-Z|0-9]|select.+from|bulk[[:space:]]+insert|union.+select|convert.+\\(.*from)" at ARGS:wpTextbox1. [file "/usr/local/apache/conf/modsec2.user.conf"] [line "355"] [id "300016"] [rev "2"] [msg "Generic SQL injection protection"] [severity "CRITICAL"] [hostname "www.xsquawkbox.net"] [uri "/xpsdk/mediawiki/index.php"] [unique_id "TNra30PhuxAAAE8SUkMAAAAQ"]Whoa. What is that? The server has

[ModSecurity](http://www.modsecurity.org/)installed, including a bunch of rules (as defined by regular expressions) designed to reject, um, bad stuff. The rule seems to come from

[here](http://www.gotroot.com/downloads/ftp/mod_security/all-rules.conf)and MediaWiki isn't the only program that it can hose.

If you pull apart the regular expression, you can see how things go wrong. Loosely speaking the rule matches text in this form:

insert ___ into ___ values|select ___ from ___ from ___ insert|union ___ select|convertwhere the blanks can be anything, can pipe indicates that either word is acceptable. So...insert, into, values, from, form, insert, convert. Those words appear in that sequence of comments in my OpenAL sample. And frankly, it's not a very remarkable sequence, hence it matching

[this](https://www.modsecurity.org/tracker/browse/CORERULES-16).

So I thought the problem was long posts, but it wasn't. The longer the post, the more likely that a particular sequence of words would show up.

From what I can tell, white-listing URLs from the rule is the "standard" fix.

## No comments:

## Post a Comment