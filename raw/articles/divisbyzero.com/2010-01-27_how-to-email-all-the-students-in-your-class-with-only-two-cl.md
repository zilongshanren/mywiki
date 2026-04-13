---
title: How to email all the students in your class with only two clicks of your mouse
url: https://divisbyzero.com/2010/01/27/how-to-email-all-the-students-in-your-class-with-only-two-clicks-of-your-mouse/
author: Dave Richeson
published: '2010-01-27'
source_blog: 'David Richeson: Division by Zero'
source_site: https://divisbyzero.com
category: game programming
fetched: '2026-04-13'
---

[Update: thanks to one of the comments below, I could rename this post “How to email all the students in your class with only **one** click of your mouse.”]

This post has no math in it. But it may be helpful to teachers (and others who regularly email a group of people).

I often have to send an email message to all the students a class that I’m teaching. To get the addresses in my desktop email program I “simply” have to click the little envelope icon in our college’s online administrative system next to the class. The annoying problem is that to do so I have to click the mouse a total of six times, enter a login name and a password, and close the two browser windows at the end of the procedure. Or I can search in my mail program for the last time I emailed the entire class, hit reply-all, delete the previous subject and message text.

(I could create an alias for the class in my address book, but honestly, I don’t want to put all the students in my address book.)

Today I had an idea for how to make this process much shorter. I made a very simple web page. The body of the page contained only “mailto” links—one for each group that I wanted to mail. I discovered that a single mailto link could have multiple email addresses. For example, the entire text of the web page could be:

*<html><body>
<p><a href=”mailto:emailaddress1@gmail.com, emailaddress2@gmail.com, emailaddress3@gmail.com, emailaddress4@gmail.com”>Calculus III</a></p>
</body></html>*

That produces a link like this:

If you have a desktop email client, try clicking on it. Hopefully it will work (and I hope the email addresses I gave were not real addresses!).

Then I saved this HTML file on my computer (NOT on the internet since this is for my own personal use only), put it in the bookmark bar of my browser, and that’s it.

Now I click the bookmark, then click on the link, and the whole class appears in my mail program. Ta-da!

Just now I found [this web page ](http://yoast.com/guide-mailto-links/)which shows that you can add other things to mailto links—namely, text for the to, cc, bcc, subject, and body fields of the email message. For example, if you want your email address to be in the “to” field and the students’ email addresses to be in the “bcc” field, type your link as follows.

*<a href=”mailto:myemailaddress@gmail.com?bcc=emailaddress1@gmail.com, emailaddress2@gmail.com, emailaddress3@gmail.com, emailaddress4@gmail.com”>Calculus III</a>*

Try it:

I still have to close the browser window after doing this. So I guess it requires three clicks, not the advertised two. If there are any javascript wizards reading this who know how to make the window close automatically after the link is clicked, leave the details in the comments!

[Update: thanks to my former student and current tech wizard Ben, I got the Javascript to work.] Clicking the following link will make the window close automatically:

*<a href=”mailto:emailaddress1@gmail.com, emailaddress2@gmail.com, emailaddress3@gmail.com, emailaddress4@gmail.com” onClick=”javascript:window.close();”>Calculus III</a>*

[Second update: thanks to the commenter David Wees.] If you drag the mailto link to the bookmark bar of your browser, then it creates a bookmarklet. Click on the link once it sends the email addresses to the email client. One click!

This should also work if your default email client is Gmail. So the email client doesn’t necessarily have to be installed on your computer.

Oh, really? Good to know. Thanks!

You should be able to add something like ‘onClick=”javascript:window.close();”‘ ….this should take care of the closure.

If it doesn’t quite work right, it may require a separate JavaScript function that starts a one-second timer to allow appropriate time for the “mailto” action to work.

Also, I’m PRETTY sure onClick is a permitted attribute for the anchor element, but I’m not 100% sure.

What I AM certain of is my own laziness for not answering all of these questions before posting (:

Ben, thanks! Your first suggestion worked perfectly. I’ll update the post right now.

Just get rid of the single quotes that I used to introduce the onClick attribute. It might still work with them in there, but it’s not technically correct syntax.

Got it. Thanks!

You could also drag the url to your bookmarks in your browser and turn it into a bookmarklet, although I recommend removing the onclick stuff.

Then it would be a 1 click email if you had your browser open already (which most of us do 95% of the time right?).

Even better. Thanks.

I actually had this same thought, but thought that I’d have to write some complicated javascript to make a bookmarklet. But you’re correct, just putting the mailto link (even with the extra cc, bcc, etc. stuff in it) in bookmark bar works perfectly. I just made a pull-down folder in my bookmark bar with all my lists. Works great.