---
title: A quick guide to LaTeX
url: https://divisbyzero.com/2011/08/17/a-quick-guide-to-latex/
author: Dave Richeson
published: '2011-08-17'
source_blog: 'David Richeson: Division by Zero'
source_site: https://divisbyzero.com
category: game programming
fetched: '2026-04-13'
---

This semester I’ll be teaching real analysis. I am going to have the students type their homework in LaTeX. To make this as easy for them as possible, I will give them a template that is all ready for them to enter their solutions. They shouldn’t have to worry about headers, packages, font sizes, margins, etc. Furthermore, I decided that I should give them a LaTeX cheat sheet—a single document that has all the LaTeX information that they will need. I’ve created LaTeX cheat sheets like this before—but one was for real analysis, one was for topology, one was for linear algebra, and one was for discrete math. Each cheat sheet had different symbols.

So, I decided to bring them all together into a one-size-fits-all [LaTeX cheat sheet](http://users.dickinson.edu/~richesod/latex/latexcheatsheet.pdf). I kept it to two pages, so it can be printed (double-sided) on one piece of paper. (I have also posted [the LaTeX code](http://users.dickinson.edu/~richesod/latex/latexcheatsheet.tex). Feel free to take it, edit it, and use it.)

It doesn’t have everything. As I said, I’ve left out all information about headers, etc. Also, since these students will probably not be using figures or tables, I’ve left them out. [Update: I added information about figures. I also added links to some online resources.]

Please let me know in the comments if there is anything that you think I should add. I still have a week and a half to tinker with it before classes begin. Also, please let me know if you find any errors. Thanks!

[Note: When I began this project I intended to modify [this cheat sheet](http://www.stdout.org/~winston/latex/) by Winston Chang to suit my needs. But in the end, I wiped it clean and started from scratch. (I did use his very nice three-column format though.)]

Does the cheat sheet include a linky to the standard LaTeX guide? (lshort.pdf, I think it’s called)

Nope. It also doesn’t have information about software, etc. I’ll probably update this old web page of mine to have that type of info.

The commands for quote marks (and single quotes) are not showing properly (I mean, they are showing as almost proper quote marks instead of the commands you need to type for latex to show quote marks). No idea how to display the proper characters in latex, though (maybe \textquotesingle for the right hand one).

Hey, Fabio! Thanks. Yes, I really wanted characters that looked like primes and backward primes (like on the keyboard), but didn’t (and still don’t) know how to do that. Perhaps someone will respond with a solution.

Don’t teach your students to use double dollar signs, that is not recommended for LaTeX. Instead, use \[ … \] or \begin{equation} … \end{equation}. See l2tabu[1]. (The german version is more updated than the english version, but both feature this tip.)

Also, the amsmath package provides several matrix environments that you can use instead of \left|\begin{array} etc., but that is perhaps more a matter of taste. See the amsmath manual (“texdoc amsmath” in a command line) section 4.1 for a complete list.

[1]http://www.ctan.org/tex-archive/info/l2tabu

That is SO FUNNY that you wrote that. I always use \[ and \], and that’s what I had in there until the very end. I put in the $$ thinking that it would be less confusing. Based on your comment, I think I’ll switch it back. I also debated about whether to use \emph use \textit (I always use the former, but I thought the latter might be easier for them to remember).

Unless I’m severely misreading, you have a typo in there under “Equations,” where you say how to write math inline.

I know that it’s probably too late with the class starting so soon, but since you seem to want to shield your students from the unnecessary complexities of document formatting with LaTeX, I wanted to point out one alternative that I’ve started to like very much.

Namely, using markdown+mathjax just like mathoverflow. You get the strength of LaTeX for writing mathematical formulae (with your cheatsheet) but the light weight and much more human readable markup language that is markdown.

There’s a nice, simple (and open source) text editor called Qute that offers a live preview much like mathoverflow. (disclaimer: it’s written by a friend of mine)

Of course, you can still convert everything to LaTeX later — pandoc is an amazing tool.

Anyway, just a thought.

Cool. Thanks for sharing that.

If it’s really an option and you and the students will actually use it, we should get in touch — Felix is definitely eager for feedback and improvements (other than being bugged by me all the time) and I’d love to hear about how useful it turns out to be.

I had another suggestion for editors. When I first started using LaTeX I used LyX (http://www.lyx.org/) because as you type your mathematical statements, it displays it directly (live preview I suppose – as above). You don’t need to convert to a PDF to make sure that what you typed in was correct.

I don’t think you have as much flexibility as working directly with the LaTeX, but it gives you a really good feel for what you can accomplish with LaTeX without the learning curve.

Also, since you would be using a template anyway, I believe (not 100% sure) you can just open the template in LyX and type away.

Just another option.

This is so beautiful it made me cry a little bit.

You crack me up, Kate. Glad you like it.