---
title: The 100% Markdown Expedition – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2022/09/the-100-percent-markdown-expedition/
author: Schalk Neethling
published: '2022-09-08'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

In June 2021, we decided to start converting the source code for MDN web docs from HTML into a format that would be easier for us to work with. The goal was to get 100% of our manually-written documentation converted to Markdown, and we really had a mountain of source code to climb for this particular expedition.

In this post, we’ll describe why we decided to migrate to Markdown, and the steps you can take that will help us on our mission.

## Why get to 100% Markdown?

We want to get all active content on MDN Web Docs to Markdown for several reasons. The top three reasons are:

- Markdown is a much more approachable and friendlier way to contribute to MDN Web Docs content. Having all content in Markdown will help create a unified contribution experience across languages and repositories.

- With all content in Markdown, the MDN engineering team will be able to clean up a lot of the currently maintained code. Having less code to maintain will enable them to focus on improving the tooling for writers and contributors. Better tooling will lead to a more enjoyable contribution workflow.

- All content in Markdown will allow the MDN Web Docs team to run the same linting rules across all active languages.

Here is the [tracking issue](https://github.com/mdn/translated-content/issues/7486) for this project on the translated content repository.

## Tools

This section describes the tools you’ll need to participate in this project.

### Git

If you do not have git installed, you can follow the steps described on this getting started page.

If you are on Linux or macOS, you may already have Git. To check, open your terminal and run: `git --version`


On Windows, there are a couple of options:

### GitHub

We’re tracking source code and managing contributions on GitHub, so the following will be needed:

• A [GitHub account](https://github.com).

• The [GitHub CLI](https://cli.github.com/) to follow the commands below. (Encouraged, but optional, i.e., if you are already comfortable using Git, you can accomplish all the same tasks without the need for the GitHub CLI.)

### Nodejs

First, install nvm – [https://github.com/nvm-sh/nvm#installing-and-updating](https://github.com/nvm-sh/nvm#installing-and-updating) or on Windows [https://github.com/coreybutler/nvm-windows](https://github.com/coreybutler/nvm-windows)

Once all of the above is installed, install Nodejs version 16 with NVM:

```
nvm install 16
nvm use 16
node --version
```


This should output a Nodejs version number that is similar to v16.15.1.

## Repositories

You’ll need code and content from several repositories for this project, as listed below.

You only need to fork the `translated-content`

repository. We will make direct clones of the other two repositories.

Clone the above repositories and your fork of `translated-content`

as follows using the GitHub CLI:

```
gh repo clone mdn/markdown
gh repo clone mdn/content
gh repo clone username/translated-content # replace username with your GitHub username
```


### Setting up the conversion tool

```
cd markdown
yarn
```


You’ll also need to add some configuration via an `.env`

file. In the root of the directory, create a new file called `.env`

with the following contents:

`CONTENT_TRANSLATED_ROOT=../translated-content/files`


### Setting up the content repository

```
cd .. # This moves you out of the `markdown` folder
cd content
yarn
```


## Converting to Markdown

I will touch on some specific commands here, but for detailed documentation, please check out the `markdown`

[ repo’s README](https://github.com/mdn/markdown#how-to-use).

We maintain a list of documents that need to be converted to Markdown [in this Google sheet](https://docs.google.com/spreadsheets/d/1Mk3bQoHXozN2rUWn9rxVHA5MiO0whDLuj71KKC0iMSg/edit?usp=sharing). There is a worksheet for each language. The worksheets are sorted in the order of the number of documents to be converted in each language – from the lowest to the highest. You do *not* need to understand the language to do the conversion. As long as you are comfortable with Markdown and some HTML, you will be able to contribute.

NOTE: You can find a useful

[reference]to the flavor of Markdown supported on MDN Web Docs. There are some customizations, but in general, it is based on[GitHub flavoured][Markdown].

### The steps

### Creating an issue

On the `translated-content`

[repository](https://github.com/mdn/translated-content) go to the Issues tab and click on the “New issue” button. As mentioned in the introduction, there is a tracking issue for this work and so, it is good practice to reference the tracking issue in the issue you’ll create.

You will be presented with three options when you click the “New issue” button. For our purposes here, we will choose the “Open a blank issue” option. For the title of the issue, use something like, “chore: convert mozilla/firefox/releases for Spanish to Markdown”. In your description, you can add something like the following:

As part of the larger 100% Markdown

[project], I am converting the set of documents under mozilla/firefox/releases to Markdown.

NOTE: You will most likely be unable to a assign an issue to yourself. The best thing to do here is to mention the localization

[team member for the appropriate][locale]and ask them to assign the issue to you. For example, on GitHub you would add a comment like this: “Hey @mdn/yari-content-es I would like to work on this issue, please assign it to me. Thank you!”You can find a

[list of teams here].

### Updating the spreadsheet

The tracking spreadsheet contains a couple of fields that you should update if you intend to work on speific items. The first item you need to add is your GitHub username and link the text to your GitHub profile. Secondly, set the status to “In progress”. In the issue column, paste a link to the issue you created in the previous step.

### Creating a feature branch

It is a common practice on projects that use Git and GitHub to follow a [feature branch workflow](https://www.atlassian.com/git/tutorials/comparing-workflows/feature-branch-workflow). I therefore need to create a feature branch for the work on the `translated-content`

repository. To do this, we will again use our issue as a reference.

Let’s say your issue was called ” chore: convert mozilla/firefox/releases for Spanish to Markdown” with an `id`

of 8192. You will do the following at the root of the `translated-content`

repository folder:

NOTE: The translated content repository is a very active repository. Before creating your feature branch, be sure to pull the latest from the remote using the command

`git pull upstream main`


```
git pull upstream main
git switch -c 8192-chore-es-convert-firefox-release-docs-to-markdown
```


NOTE: In older version of Git, you will need to use

`git checkout -B 8192-chore-es-convert-firefox-release-docs-to-markdown`

.

The above command will create the feature branch and switch to it.

## Running the conversion

Now you are ready to do the conversion. The Markdown conversion tool has a couple of modes you can run it in:

- dry – Run the script, but do not actually write
*any*output

- keep – Run the script and do the conversion but,
*do not*delete the HTML file

- replace – Do the conversion and delete the HTML file

You will almost always start with a `dry`

run.

NOTE: Before running the command below, esnure that you are in the root of the markdown repository.


`yarn h2m mozilla/firefox/releases --locale es --mode dry`


This is because the conversion tool will sometimes encounter situations where it does not know how to convert parts of the document. The markdown tool will produce a report with details of the errors encountered. For example:

```
# Report from 9/1/2022, 2:40:14 PM
## All unhandled elements
- li.toggle (4)
- dl (2)
- ol (1)
## Details per Document
### [/es/docs/Mozilla/Firefox/Releases/1.5](<https://developer.mozilla.org/es/docs/Mozilla/Firefox/Releases/1.5>)
#### Invalid AST transformations
##### dl (101:1) => listItem
type: "text"
value: ""
### [/es/docs/Mozilla/Firefox/Releases/3](<https://developer.mozilla.org/es/docs/Mozilla/Firefox/Releases/3>)
### Missing conversion rules
- dl (218:1)
```


The first line in the report states that the tool had a problem converting four instances of `li.toggle`

. So, there are four list items with the `class`

attribute set to `toggle`

. In the larger report, there is this section:

```
### [/es/docs/Mozilla/Firefox/Releases/9](<https://developer.mozilla.org/es/docs/Mozilla/Firefox/Releases/9>)
#### Invalid AST transformations
##### ol (14:3) => list
type: "html"
value: "<li class=\\"toggle\\"><details><summary>Notas de la Versión para Desarrolladores de Firefox</summary><ol><li><a href=\\"/es/docs/Mozilla/Firefox/Releases\\">Notas de la Versión para Desarrolladores de Firefox</a></li></ol></details></li>",type: "html"
value: "<li class=\\"toggle\\"><details><summary>Complementos</summary><ol><li><a href=\\"/es/Add-ons/WebExtensions\\">Extensiones del navegador</a></li><li><a href=\\"/es/Add-ons/Themes\\">Temas</a></li></ol></details></li>",type: "html"
value: "<li class=\\"toggle\\"><details><summary>Firefox por dentro</summary><ol><li><a href=\\"/es/docs/Mozilla/\\">Proyecto Mozilla (Inglés)</a></li><li><a href=\\"/es/docs/Mozilla/Gecko\\">Gecko</a></li><li><a href=\\"/es/docs/Mozilla/Firefox/Headless_mode\\">Headless mode</a></li><li><a href=\\"/es/docs/Mozilla/JavaScript_code_modules\\">Modulos de código JavaScript (Inglés)</a></li><li><a href=\\"/es/docs/Mozilla/js-ctypes\\">JS-ctypes (Inglés)</a></li><li><a href=\\"/es/docs/Mozilla/MathML_Project\\">Proyecto MathML</a></li><li><a href=\\"/es/docs/Mozilla/MFBT\\">MFBT (Inglés)</a></li><li><a href=\\"/es/docs/Mozilla/Projects\\">Proyectos Mozilla (Inglés)</a></li><li><a href=\\"/es/docs/Mozilla/Preferences\\">Sistema de Preferencias (Inglés)</a></li><li><a href=\\"/es/docs/Mozilla/WebIDL_bindings\\">Ataduras WebIDL (Inglés)</a></li><li><a href=\\"/es/docs/Mozilla/Tech/XPCOM\\">XPCOM</a></li><li><a href=\\"/es/docs/Mozilla/Tech/XUL\\">XUL</a></li></ol></details></li>",type: "html"
value: "<li class=\\"toggle\\"><details><summary>Crear y contribuir</summary><ol><li><a href=\\"/es/docs/Mozilla/Developer_guide/Build_Instructions\\">Instrucciones para la compilación</a></li><li><a href=\\"/es/docs/Mozilla/Developer_guide/Build_Instructions/Configuring_Build_Options\\">Configurar las opciones de compilación</a></li><li><a href=\\"/es/docs/Mozilla/Developer_guide/Build_Instructions/How_Mozilla_s_build_system_works\\">Cómo funciona el sistema de compilación (Inglés)</a></li><li><a href=\\"/es/docs/Mozilla/Developer_guide/Source_Code/Mercurial\\">Código fuente de Mozilla</a></li><li><a href=\\"/es/docs/Mozilla/Localization\\">Localización</a></li><li><a href=\\"/es/docs/Mozilla/Mercurial\\">Mercurial (Inglés)</a></li><li><a href=\\"/es/docs/Mozilla/QA\\">Garantía de Calidad</a></li><li><a href=\\"/es/docs/Mozilla/Using_Mozilla_code_in_other_projects\\">Usar Mozilla en otros proyectos (Inglés)</a></li></ol></details></li>"
```


The problem is therefore in the file `/es/docs/Mozilla/Firefox/Releases/9`

. In this instance, we can ignore this as we will simply leave the HTML as is in the Markdown. This is sometimes needed as the HTML we need cannot be accurately represented in Markdown. The part you cannot see in the output above is this portion of the file:

```
<div><section id="Quick_links">
<ol>
<li class="toggle">
```


If you do a search in the main `content`

repo you will find lots of instances of this. In all those cases, you will see that the HTML is kept in place and this section is *not* converted to Markdown.

The next two problematic items are two `dl`

or description list elements. These elements will require manual conversion using the guidelines in [our documentation](https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Howto/Markdown_in_MDN#definition_lists). The last item, the `ol`

is actually related to the `li.toggle`

issue. Those list items are wrapped by an `ol`

and because the tool is not sure what to do with the list items, it is also complaining about the ordered list item.

Now that we understand what the problems are, we have two options. We can run the exact same command but this time use the `replace`

mode or, we can use the `keep`

mode. I am going to go ahead and run the command with `replace`

. While the previous command did not actually write anything to the translated content repository, when run with `replace`

it will create a new file called `index.md`

with the converted Markdown and delete the `index.html`

that resides in the same directory.

`yarn h2m mozilla/firefox/releases --locale es --mode replace`


Following the guidelines from the report, I will have to pay particular attention to the following files post conversion:

`/es/docs/Mozilla/Firefox/Releases/1.5`


`/es/docs/Mozilla/Firefox/Releases/3`


`/es/docs/Mozilla/Firefox/Releases/9`


After running the command, run the following at the root of the translated content repository folder, `git status`

. This will show you a list of the changes made by the command. Depending on the number of files touched, the output can be verbose. The vital thing to keep an eye out for is that there are no changes to folders or files you did not expect.

## Testing the changes

Now that the conversion has been done, we need to review the syntax and see that the pages render correctly. This is where the `content`

repo is going to come into play. As with the `markdown`

repository, we also need to create a `.env`

file at the root of the content folder.

`CONTENT_TRANSLATED_ROOT=../translated-content/files`


With this in place we can start the development server and take a look at the pages in the browser. To start the server, run `yarn start`

. You should see output like the following:

```
❯ yarn start
yarn run v1.22.17
$ yarn up-to-date-check && env-cmd --silent cross-env CONTENT_ROOT=files REACT_APP_DISABLE_AUTH=true BUILD_OUT_ROOT=build yari-server
$ node scripts/up-to-date-check.js
[HPM] Proxy created: / -> <https://developer.mozilla.org>
CONTENT_ROOT: /Users/schalkneethling/mechanical-ink/dev/mozilla/content/files
Listening on port 5042
```


Go ahead and open [http://localhost:5042](http://localhost:5042/) which will serve the homepage. To find the URL for one of the pages that was converted open up the Markdown file and look at the slug in the frontmatter. When you ran `git status`

earlier, it would have printed out the file paths to the terminal window. The file path will show you exactly where to find the file, for example, `files/es/mozilla/firefox/releases/1.5/index.md`

. Go ahead and open the file in your editor of choice.

In the frontmatter, you will find an entry like this:

```
slug: Mozilla/Firefox/Releases/1.5
```


To load the page in your browser, you will always prepend `http://localhost:5042/es/docs/`

to the slug. In other words, the final URL you will open in your browser will be `http://localhost:5042/es/docs/Mozilla/Firefox/Releases/1.5`

. You can open the English version of the page in a separate tab to compare, but be aware that the content could be wildly different as you might have converted a page that has not been updated in some time.

What you want to look out for is anything in the page that looks like it is not rendering correctly. If you find something that looks incorrect, look at the Markdown file and see if you can find any syntax that looks incorrect or completely broken. It can be extremely useful to use a tool such as [VSCode](https://code.visualstudio.com/) with a [Markdown tool](https://marketplace.visualstudio.com/items?itemName=yzhang.markdown-all-in-one) and [Prettier](https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode) installed.

Even if the rendered content looks good, do take a minute and skim over the generated Markdown and see if the linters bring up any possible errors.

NOTE: If you see code like this {{FirefoxSidebar}} this is a macro call. There is not a lot of documentation yet but, these macros come from

[KumaScript][in Yari].

A couple of other things to keep in mind. When you run into an error, before you spend a lot of time trying to understand what exatly the problem is or how to fix it, do the following:

- Look for the same page in the
`content`

repository and make sure the page still exists. If it was removed from the`content`

repository, you can safely remove it from`translated-content`

as well.

- Look at the same page in another language that has already been converted and see how they solved the problem.

For example, I ran into an error where a page I loaded simply printed the following in the browser: `Error: 500 on /es/docs/Mozilla/Firefox/Releases/2/Adding_feed_readers_to_Firefox/index.json: SyntaxError: Expected "u" or ["bfnrt\\\\/] but "_" found.`

. I narrowed it down to the following piece of code inside the Markdown:

`{{ languages( { "en": "en/Adding\\_feed\\_readers\\_to\\_Firefox", "ja": "ja/Adding\\_feed\\_readers\\_to\\_Firefox", "zh-tw": "zh\\_tw/\\u65b0\\u589e\\u6d88\\u606f\\u4f86\\u6e90\\u95b1\\u8b80\\u5de5\\u5177" } ) }}`


In French it seems that they removed the page, but when I looked in `zh-tw`

it looks like they simply removed this macro call. I opted for the latter and just removed the macro call. This solved the problem and the page rendered correctly. Once you have gone through all of the files you converted it is time to open a pull request.

## Preparing and opening a pull request

```
# the dot says add everything
git add .
```


Start by getting all your changes ready for committing:

If you run `git status`

now you will see something like the following:

```
❯ git status
On branch 8192-chore-es-convert-firefox-release-docs-to-markdown
Changes to be committed: # this be followed by a list of files that has been added, ready for commit
```


Commit your changes:

```
git commit -m 'chore: convert Firefox release docs to markdown for Spanish'
```


Finally you need to push the changes to GitHub so we can open the pull request:

```
git push origin 8192-chore-es-convert-firefox-release-docs-to-markdown
```


You can now head over to the [translated content repository on GitHub](https://github.com/mdn/translated-content) where you should see a banner that asks whether you want to open a pull request. Click the “Compare and pull button” and look over your changes on the next page to ensure nothing surprises.

At this point, you can also add some more information and context around the pull request in the description box. It is also critical that you add a line as follows, “Fix #8192”. Substitute the number with the number of the issue you created earlier. The reason we do this is so that we link the issue and the pull request. What will also happen is, once the pull request is merged, GitHub will automatically close the issue.

Once you are satisfied with the changes as well as your description, go ahead and click the button to open the pull request. At this stage GitHub will auto-assign someone from the appropriate localization team to review your pull request. You can now sit back and wait for feedback. Once you receive feedback, address any changes requested by the reviewer and update your pull request.

Once you are both satisfied with the end result, the pull request will be merged and you will have helped us get a little bit closer to 100% Markdown. Thank you! One final step remains though. Open the [spreadsheet](https://docs.google.com/spreadsheets/d/1Mk3bQoHXozN2rUWn9rxVHA5MiO0whDLuj71KKC0iMSg/edit) and update the relevant rows with a link to the pull request, and update the status to “In review”.

Once the pull request has been merged, remember to come back and update the status to done.

### Reach out if you need help

If you run into any problems and have questions, please join our MDN Web Docs channel on Matrix.


Photo by [Cristian Grecu](https://unsplash.com/@taguwan?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on [Unsplash](https://unsplash.com/s/photos/mountain-peak?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)

## About
[
Schalk Neethling ](http://schalkneethling.com)

I am a Mozillian, an evangelist, writer and developer with a passion for open source, web standards and accessibility. I have been so involved with these worlds that I feel they have become a part of me and cannot foresee a future where these topics will not be a part of my daily life.