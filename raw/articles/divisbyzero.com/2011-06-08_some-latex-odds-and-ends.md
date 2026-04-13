---
title: Some LaTeX odds and ends
url: https://divisbyzero.com/2011/06/08/some-latex-odds-and-ends/
author: Dave Richeson
published: '2011-06-08'
source_blog: 'David Richeson: Division by Zero'
source_site: https://divisbyzero.com
category: game programming
fetched: '2026-04-13'
---

Here are a few [LaTeX](http://en.wikipedia.org/wiki/LaTeX) tricks I’d like to share. None of them are earth-shattering, but maybe they’d be useful to some of you. (If you want to try these out, you can download this [sample tex file and bib file](http://users.dickinson.edu/~richesod/funwithlatex.zip) that contains these tricks.)

1. I have always wanted LaTeX to support inline comments. In many computer programming languages you can insert comments /* like this */ in the middle of a line. You can’t in LaTeX. You can add comments using a % symbol, but then everything on the line after it is commented out.

The chief reason I would like to have inline comments is because I like to leave little notes to myself in the LaTeX—facts that I’ve decided to omit, clarifying details, word choices that I haven’t decided on, etc. Wouldn’t it be nice to write this?

The rain in Spain /* or is it France? */ falls mainly on the plain.

Of course, you can effectively leave inline comments like this (with no space between the two lines):

The rain in Spain%or is it France? falls mainly on the plain.

But I’ve never been happy with the look of that in my code.

Today I had an idea for how to get inline comments in my LaTeX code. I defined a new function that takes one argument and does nothing with it:

\newcommand{\comment}[1]{}

Now I can write inline comments like this:

The rain in Spain\comment{or is it France?} falls mainly on the plain.

2. That inspired me to work on something else on my wish list. When you put

\cite[p. 100]{richeson:2008}

in your article it leaves a citation to the book, includes the page number, and puts the book in the bibliography. When you put

\nocite{richeson:2008}

in your article it does NOT put a citation in the article, but it does put the book in the bibliography. Great. But what I would like to do is put this in my code:

\nocite[p. 100]{richeson:2008}

I want to do this not for the reader, but for me. If I’ve obtained a piece of information from a book, I’d like to make note of it in the body of my text so that I can go back and find it later. For long books, page numbers are crucial. I could use my new comment system

Euler's formula is $V-E+F=2$.\nocite{richeson:2008}\comment{p. 100} Isn't that cool?

Instead, I defined a new command:

\newcommand{\pgnocite}[2]{\nocite{#2}}

This new command takes two arguments—the page numbers and the citation. It ignores the page number and does a “nocite” on the citation. So I write

Euler's formula is $V-E+F=2$.\pgnocite{p. 100}{richeson:2008} Isn't that cool?

3. I do a lot of collaborating using [DropBox](http://db.tt/c8nOEkH) and LaTeX. When I get the document back from my collaborator, it is difficult to tell what edits he made. So my collaborator and I came up with these commands to highlight new or changed text:

```
\usepackage[normalem]{ulem}
\usepackage[usenames,dvipsnames]{color}
\newcommand{\remove}[1]{{\color{Red}\sout{#1}$^{\text{remove}}$}}
\newcommand{\moved}[1]{{\color{ForestGreen}#1$^{\text{moved}}$}}
\newcommand{\fix}[1]{{\color{Orange}\uwave{#1}$^{\text{fix}}$}}
\newcommand{\new}[1]{{\color{NavyBlue}#1$^{\text{new}}$}}
When I add a new sentence to the document I put
\new{This is a new sentence.}
```

in the text. It appears blue with a little superscript “new” next to it. After I’ve read it, I can remove the \new tag. We also defined \remove, \moved, and \fix. You can create your own, add your own colors, and even decorate it with underlines from the [ulem package](http://mirror.math.ku.edu/tex-archive/macros/latex/contrib/ulem/ulem.pdf) (in the example above, \remove has a strike-through and \fix is underlined with a wavy line).

4. Lastly, we created a command that allows us to put notes in the margin.

\newcommand{\marginnote}[1]{\mbox{}\marginpar{\raggedleft\hspace{0pt}#1}}

Now we type this to get a margin note.

Here's a neat proof of this result.\marginnote{Jim, is this proof correct?}

For your items 1, 2, 4, I rather use todonotes (http://www.tex.ac.uk/CTAN/macros/latex/contrib/todonotes/todonotes.pdf). It supports several types of notes, is easily deactivated, you can display a list of all notes, etc. Useful for any kind of annotations, not only todos.

For item 3, I believe some VCS is the way to go (git on top of Dropbox is my favorite). Then you can use latexdiff to see the differences.

Wow, thanks for introducing me to the todonotes package. Very cool. Just playing around with it I modified my code to this:

\usepackage[shadow]{todonotes}

\newcommand{\marginnote}[1]{\todo{#1}}

\newcommand{\remove}[1]{{\color{Red}#1}\todo[color=red!40]{remove}\,}

\newcommand{\moved}[1]{{\color{ForestGreen}#1}\todo[color=green!40]{moved}\,}

\newcommand{\fix}[1]{{\color{Orange}#1}\todo[color=orange]{fix}\,}

\newcommand{\new}[1]{{\color{NavyBlue}#1}\todo[color=blue!40]{new}\,}

Looks great!

My collaborators are often keen on marking edits with tags like the ones you suggest. It doesn’t work so well if more than two people edit the document though. I prefer to get a version control system to tell me what the changes were. A problem can be that if you reflow a paragraph, diff says that the whole paragraph has changed. However, it is possible to color which words have changed, ignoring the reflowing: http://homepages.inf.ed.ac.uk/imurray2/compnotes/cwdiff/

I’ve never done anything with VCS’s. I should probably look into it. Thanks.

For 2, you could just do:

\renewcommand{\nocite}[2][]{\nocite{#2}}

This makes the first argument optional and gives it a null default value so you can do \nocite{foo:bar} if you don’t want to include a page number and \nocite[pp. 100]{foo:bar} if you do. This makes the syntax for \nocite identical to that for \cite.

You may be leery of redefining the \nocite command in case other packages also redefine it or depend on its syntax. Since you are only introducing an optional argument, I don’t expect you will encounter too many problems, but if you do then you can always make a new command instead via:

\newcommand{\mynocite}[2][]{\nocite{#2}}

For 3, I would second the use of a version control system combined with latexdiff. Personally, I use Mercurial, which I find more intuitive than git. It’s a matter of personal preference and, more importantly, what you can persuade your collaborators to learn.

Using Dropbox has less of a learning curve than using a full-blown VCS, which makes it appealing, since it is a tough sell to persuade all your collaborators to learn a VCS. In my opinion, it is still worthwhile to learn a VCS as it is much more flexible, e.g. you can have people working on different sections of the paper simultaneously and then merge them automatically. If people accidentally edit the same section then you can control how the changes get merged in a sensible way. The behaviour of Dropbox is unpredictable in similar circumstances — it would typically just update to the version that was most recently edited and the changes from other edits would have to be fished out from the history.

Of course, Dropbox is using a VCS as its backend (I think it is svn), so it may be possible to do all the same tricks with it if the VCS stuff is exposed in the API. I don’t know if this is the case or not.

It would be great if someone built an online LaTeX collaboration tool that was based on a VCS, exposed the VCS to users, but did a lot of stuff automatically like Dropbox so that lazy collaborators did not have to learn anything new.

Thank you for these tips. Your first suggestion (renewcommand) wouldn’t compile for me (it didn’t give an error message—it just hangs partway through the process). But the second one works great. I spent a little while looking at how to add options to a newcommand, but decided it was too complicated. That’s why I chose my method. But your suggestion is simple and works well. Thanks.

As for VCS—I’m intrigued, and I know that it is the “right” thing to do. But I just wonder if it is worth the investment of time (it probably is!). I’m only moderately savvy when it comes to these things. I use TexShop, BibDesk, and DropBox, all of which are elementary to use. I should consider moving to “the next level.”

Thanks again.

P.S. I should clarify that I was imagining using a VCS with your own webserver (or a hosted platform like github or bitbucket) rather than VCS+Dropbox. Putting a VCS repository in a Dropbox folder is not a great idea for two reasons:

1. You are doubling up on your VCS because Dropbox uses a VCS as its backend.

2. Dropbox will behave unpredictably when you push changes to it, since if someone else syncs to Dropbox who doesn’t have the new changes in their repository then the Dropbox version will get overwritten with the old version. This is precisely the sort of thing that using a VCS is meant to avoid.

Running a decent VCS on top of Dropbox does work without any problems, even when you are collaborating with other people. I use git on top of Dropbox for multiple projects, one of which is shared amongst some people without any problem (however, I am the only one using the git part). Sometime you need to clean the mess Dropbox leaves (i.e. ‘conflicted copies’ or ‘case conflicts’). But you end up with a clean history in Git (no partial commits) and you could retrieve those partial edits from Dropbox if you need to (and you can keep the generated files (i.e. files you don’t want inside your actual version control) shared across multiple machines).

However, I think that due to the clear file structure of git, this DVCS runs smoothly on top of Dropbox. I don’t know how Subversion or something else would react inside Dropbox.

With regard to the usage of VCSs: it is certainly worthwhile. Dropbox is a stripped-down VCS, you can already taste the power you get, but it is cumbersome to use it as such (e.g. try reverting a whole directory). At the moment there is a lot of buzz around distributed VCSs (DVCSs) such as git, mercurial, monotone, bazaar, darcs (and rightly so, I think). If you don’t have any experience with version control, try these out. If somebody on your team has the experience, you might as well go for their VCS of choice.

On Twitter Dana Ernst pointed out the changes LaTeX package.

Very nice. For your #4 I’ve been using:

\newcommand{\marginnote}[1]{\marginpar{\sffamily{\tiny #1 \par}\normalfont}}

Very similar of course, but I particularly like the small font and the san serif.

What you call \comment I call \junk. It is mainly useful when I want to kill a bunch of text, I think, but I’m not _totally_ sure I want it gone; instead I put \junk{} around it. Much easier than putting % at the beginning of lots of lines.

the ‘latexdiff’ command allows you to just make changes as you want in the normal text, no markup, and it will highlight add/remove/change for you.