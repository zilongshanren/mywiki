---
title: Tricks for easily creating BibTeX files
url: https://divisbyzero.com/2010/07/27/tricks-for-easily-creating-bibtex-files/
author: Dave Richeson
published: '2010-07-27'
source_blog: 'David Richeson: Division by Zero'
source_site: https://divisbyzero.com
category: game programming
fetched: '2026-04-13'
---

I wrote [my last book](http://www.eulersgem.com/) (my only book, that is) using [LaTeX](http://en.wikipedia.org/wiki/LaTeX). I had a large bibliography with close to 400 entries. I stored all of the bibliographic items in a [BibTeX](http://en.wikipedia.org/wiki/BibTeX) file (a text file ending in .bib). Each item looks something like this:

`@book {Richeson:2008,`


AUTHOR = {Richeson, David S.},

TITLE = {Euler's gem: The polyhedron formula and the birth of topology},

PUBLISHER = {Princeton University Press},

ADDRESS = {Princeton, NJ},

YEAR = {2008},

PAGES = {xii+317},

ISBN = {978-0-691-12677-7; 0-691-12677-1}

}


The beautiful thing about BibTeX is that after you cite works in your LaTeX document (for example `\cite{Richeson:2008}`

), the references are automatically generated in whichever bibliographic style you specify (APA, MLA, Chicago, etc.).

However, as you can see above, it is a pain to enter the bibliographic information by hand—the syntax is rather cumbersome. Fortunately there are a number of places on the web to get pre-formated BibTeX entries. You can pull them up in your browser, then copy-and-paste them in to your .bib file. Here are a few useful sites for mathematicians (I learned about a few of these from this [MathOverflow conversation](http://mathoverflow.net/questions/20551/sources-for-bibtex-entries)).

[MathSciNet](http://www.ams.org/mathscinet/)(subscription required)—this is the web front-end for the extensive Mathematical Reviews database. It currently has over 2 million items. It gives bibliographic information, reviews, and more.[MR Lookup](http://www.ams.org/mrlookup)—this is the free version of MathSciNet. It gives bibliographic information only.[Zentralblatt Math database](http://www.zentralblatt-math.org/zbmath/)(subscription required)—similar to MathSciNet, it has over 3 million items.[OttoBib](http://www.ottobib.com/)—search for books by ISBN[Lead2Amazon](http://lead.to/amazon/en/)—searches six different Amazon sites[Google Scholar](http://scholar.google.com/)—this is a well-known scholarly search site run by Google. If you click the “Scholar preferences” link you’ll see that under Bibliography Manager, one of the options is to “Show links to import citations into: BibTeX.” Now each Google Scholar search result will have a link to the BibTeX entry (see below).

**Mac-only goodness: BibDesk + TexShop**

I could create the .bib files using a text editor, but instead I use the great, free, Mac-only program [BibDesk](http://sourceforge.net/apps/mediawiki/bibdesk/) (see screenshot below).

I was a huge fan of BibDesk while writing my book, but it turns out I was using only a small fraction of its capabilities. I used it to create, edit, and organize bibliographic entries. It has a simple interface that allows you to enter bibliographic information into the fields provided. The file it creates is a .bib file, not a BibDesk file, so there is no need to export the information for use in LaTeX.![Screen shot 2010-07-27 at 5.27.30 PM](../../assets/eea0c2808066fce7.png)


Even though I spent many, many hours using BibDesk, I never explored its other features (and now I’m kicking my self). I want to share a few of them with you now.

**Importing BibTeX entries. **Above I gave several locations on the web to go to find BibTeX entries for mathematical works. I’ve known for a while if I highlighted a BibTeX entry, then dragged-and-dropped the text onto the BibDesk program that it would create a new entry with the fields filled in. I thought that was cool. That was nothing. Recently I discovered that you can use BibDesk like a mini web browser and import bibliographic entries with one click.

On the side-bar click External>Web. The screen splits vertically into thirds. You get a little browser in the top third with links to MathSciNet, Zentralblatt Math, the arXiv, etc. You can also type in addresses (such as the ones I gave above) or create bookmarks. When you perform a search using one of these websites BibDesk uses the middle screen to list all of the bibliographic items it finds. (The bottom third is used to preview the contents.) Each entry has an “import” button next to it. When you find the item you want, click the button and you’re done (see below).

I also like that when you import an entry from MathSciNet it saves a direct link back to the page that contains the review.

(I see that you can also search databases, like the Library of Congress—these databases are found in the Search menu.)

**Paper archive. **If you have an electronic copy of an article (a pdf for instance), you can drag-and-drop it onto the BibTeX entry for the article. Then BibDesk will place the article into a dedicated folder of your choosing (and a subfolder named for the first author). Then you can access your articles straight from BibDesk. Not only that, you can use BibDesk’s search feature to search inside the articles!

I’ve written before about my love for [DropBox](https://divisbyzero.com/2009/10/04/a-new-way-to-collaborate-dropbox/). I have it set up so that my bibliographic files are in sync and so are my pdfs. Since the folder structures are the same, I can access all my articles through BibDesk on any of my computers.

**TexShop integration.** I’m also a die-hard [TexShop](http://www.uoregon.edu/~koch/texshop/) user. This front-end for LaTeX is another free and elegant Mac-only program (which I may write about in another blog post). It integrates with BibDesk beautifully. If you type the beginning of a citation in TexShop, like `\cite{Ri`

, and then press F5 it will pull up a contextual menu listing all of the entries from your bibliography that could match that fragment. With a couple keystrokes you’re done.

Enjoy!

Have you tried Mendeley ? I like the browser bookmarklet a lot, plus it provides support for storing your reading list online. (http://www.mendeley.com/)

I don’t like Google scholar’s bibtex files. The bibtex I get from them would invariably be malformed (use @misc for @inproceedings, or @article), and lack a lot of information. The best bibtex I get is from ACM digital library. IEEE xplorer has the habit of marking conference papers with @article entries.

I haven’t tried Mendeley. I’ll have to investigate it.

I just discovered the BibTeX feature on Google Scholar, so I haven’t had a chance to form an opinion about the quality. You may be right. I have found that MathSciNet often needs a little tweaking. For example it seems to put a book’s subtitle in as a note, whereas I’d rather have it after the title.

Not to turn this into a “are you familiar with…” list, but I think Zotero (free) does a decent job of automatically pulling bibliographic info from websites (journals, amazon, etc) and you can then convert this to a bibtex file.

I’ve heard good things about Zotero. The problem for me is that Firefox is not my primary browser and I think it only works with FF.

Firefox is not my primary browser either, but with Zotero and zot2bib installed (zot2bib links Zotero to BibDesk), it’s worth running Firefox just for research purposes. Zotero and zot2bib will scrape bibliographic data from an incredible number of sources directly into BibDesk.

http://mackerron.com/zot2bib/

Qiqqa helps you quickly download, catalogue and edit many BibTeX entries from GoogleScholar for your existing PDFs. You can then export this collection into one BibTeX file, or to Word2007 reference XML format for writing up.

Will definitely be looking into the GoogleScholar BibTeX quality issue that Ragib mentioned!

Great tips!

I found that, if you save a book to Google Books (http://books.google.com), there is an option to export to BibTex too.

Thanks! I didn’t know that.

thank you my friend!!

very useful post!!

google exports all bibtexes in the same nice form that i couldn’t find nowhere else!!

Please post the bibtex file for the 400 or so references of your book somewhere, as a service to interested readers.