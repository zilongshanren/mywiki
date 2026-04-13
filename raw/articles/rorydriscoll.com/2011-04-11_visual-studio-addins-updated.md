---
title: Visual Studio Addins Updated
url: https://www.rorydriscoll.com/2011/04/11/visual-studio-addins-updated/
author: Rory
published: '2011-04-11'
source_blog: CodeItNow
source_site: https://www.rorydriscoll.com
category: graphics
fetched: '2026-04-13'
---

## DoItNow & RevisionItNow

I’ve updated the [Google Code](http://doitnow.googlecode.com) repository for DoItNow with a newer version. I’ve removed all source control features from DoItNow and separated them into their own add-in. This should make it more compatible with other add-ins you may be using to handle source control. I’ve uploaded the Mercurial version of the add-in, but the full source is available should you want to change it back to Perforce.

I’m only using Visual Studio 2010 at home now, so the project files are all in that format at the moment. I provided Addin files which will work for Visual Studio 2008 as well though.

By request from someone at work, the open in solution dialog now performs matches on multiple (space-separated) search terms.

## FindItNow

I’ve been testing out an idea for a replacement for the standard Visual Studio find-in-files. This is the first pass at it (let’s call it an alpha), so download at your own risk! It’s actually sits side-by-side with the existing find-in-files, so it’s pretty safe to install.

Here’s where it’s (possibly) better:

- It can match multiple search terms and will rank results accordingly.
- Remembers all settings from the previous searches. Pushing up or down will set things like ‘match case’ based on the search history.
- It populates the file types drop down based on the files in the solution, and sorts them by frequency.

Here’s where it’s (definitely) worse right now:

- It doesn’t remember the search paths you used in previous Visual Studio sessions.
- Since it ranks results, it doesn’t present them incrementally. This means you might have to wait longer to get results.
- You can’t cancel a search!

FindItNow ranks search results based on the number of hits on each line, as well as hits in the surrounding few lines. In order for a result to even show up, it must have all search terms present in a seven-line block.

The top matches (100% quality) have all search terms on the line in question. Worse quality matches have progressively fewer matches on the line.

e.g. Here are the results for a search I did looking for a quaternion conjugate function on some of my code:

Query: "quat conjugate" Options: case=ignore, match=partial Source: Entire solution Finding... Complete Match Quality: 100% -------------------- c:\Development.old\Libraries\C++\Math\Quaternion.h(79): inline Quaternion Conjugate(const Quaternion& quat) c:\Development.old\Libraries\C++\Math\Quaternion.h(96): return Conjugate(quat) / Length(quat); c:\Development.old\Libraries\C++\Math\Quaternion.h(101): const Quaternion result = quat * Quaternion(vec.x, vec.y, vec.z, 0) * Conjugate(quat); Match Quality: 62% ------------------- c:\Development.old\Libraries\C++\Math\Quaternion.h(76): return Quaternion(lhs.x / f, lhs.y / f, lhs.z / f, lhs.w / f); c:\Development.old\Libraries\C++\Math\Quaternion.h(81): return Quaternion(-quat.x, -quat.y, -quat.z, quat.w); c:\Development.old\Libraries\C++\Math\Quaternion.h(94): inline Quaternion Invert(const Quaternion& quat) c:\Development.old\Libraries\C++\Math\Quaternion.h(99): inline Vector3 Rotate(const Vector3& vec, const Quaternion& quat) Total files searched: 407 Matching lines: 34 Find Time: 90 ms Output Time: 9 ms

I’m finding it pretty useful when exploring for functions I think *should* exist in a large code-base since you don’t have to get the exact string to match.

If you’re interested in either of these, you can grab the binariesÂ [here](http://doitnow.googlecode.com/files/DoItNow-2011-04-11.zip).

Can you make a 2005 version? I tried changing the version number in the .addin file with no luck.

Soon we’ll be rid of the 2005 need… I’ll see if I can get some time to convert our solution to 2010 ….

About time Jim! And yes, the addins do work on Visual Studio 2005.

Link exchange is nothing else except it is just placing the

other person’s webpage link on your page at appropriate place and other person will also do similar

in favor of you.