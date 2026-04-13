---
title: Migrating this Blog to Next.js from Gatsby
url: https://blog.eyas.sh/2021/08/gatsby-to-next-js/
author: Eyas Sharaiha
published: '2021-08-20'
source_blog: Eyas's Blog
source_site: https://blog.eyas.sh/
category: game programming
fetched: '2026-04-13'
---

In February 2020, I migrated this blog from WordPress to
[Gatsby](https://www.gatsbyjs.com/). Using Gatsby also allowed me to switch from
hosting my site on a paid plan on [SiteGround](https://www.siteground.com/) to a
(usually free) plan on [Netlify](https://www.netlify.com/).

The migration made sense to me at the time: static-site generation was all the rage, and Gatsby was the exciting new thing. It promised better performance and improved my authoring workflow with Markdown and React. Saving a few dollars a month on hosting didn’t hurt either.

## My Initial Migration to Gatsby

Throughout that first migration, I had a couple of goals:

**Keep the URL structure**I want to be a good internet citizen and prevent*exactly*the same.[link rot](https://en.wikipedia.org/wiki/Link_rot)where I can. I also did not want to pay the (temporary) cost of an SEO hit if all my links changed.[1](https://blog.eyas.sh#user-content-fn-1)**Maintain feature parity with the old site.**I want my RSS feeds Sitemaps to look and work the same way. WordPress also supported[AMP](https://amp.dev/)for each blog post by appending an`/amp`

to the permalink. I wanted to keep the same URL schema for AMP.

The goals had some side-effects:

- I had to support pages (e.g.,
`/about`

), - blog posts (
`/yyyy/mm/my-slug`

), an index page with pagination (`/page/2`

), - paginated archives for all my tags (
`/tag/software/`

and`/tag/software/page2/`

), and - year (
`/yyyy/`

) and month (`/yyyy/mm/`

) archives, which are also themselves paginated.

I also had to make some compromises on my goals:

- WordPress also had
*day archives*, so that`/yyyy/mm/dd/`

would show archives of posts written in that one day. But I rarely write multiple posts a day. And I couldn’t find external links to day archives on my blog, so I decided to remove them. - WordPress has
*Categories*, not just*Tags*. I ended up merging these two concepts, and writing a permanent redirect from`/category/*/`

to`/tag/*/`

.

I still felt like the spirit of my goals was met by these two compromises.

## Growing Pains with Gatsby

About a year after the migration, I was increasingly running into problems with Gatsby:

-
**Performance**. While Gatsby initially gave better performance, it started slipping. My Lighthouse scores slipped with each Gatsby update, and as Google shifted to Lighthouse scores based on[end-user vitals](https://web.dev/vitals/), new issues that weren’t apparent started popping up.In some cases, a subsequent Gatsby update fixed these.

But it was also true that Gatsby’s promise of performance & tuning out-of-the-box (e.g., with its Image component) was not totally true.

-
**Build flakiness**. What ended being the deal-breaker with Gatsby were build failures and outputs that I could not explain.I ended up running into a bug where some of my AMP blog posts did not render any

`<meta>`

or`<link rel="canonical">`

tags. It was a different set of pages each time and kept happening as I removed most plugins I was using.There was probably a bug somewhere in my code; I’m not saying Gatsby was necessarily the culprit (although I sometimes think it might have been). However, the real issue is that there is

*too much magic*going on in a Gatsby build. Magic is great when everything works, but it’s horrible when something is wrong.

The AMP flakiness bug I ran into started happening after upgrading a recent Gatsby version. After losing hope on fixing the issue myself, I still hoped a newer version of Gatsby would fix it. After a couple of months of waiting and a few more attempts at finding the root cause, I made a decision: I’ll migrate away from Gatsby.

## Migrating to Next.js

The
[Next.js documentation on migrating from Gatsby](https://nextjs.org/docs/migrating/from-gatsby)
was a great starting point. I also consulted Josh W. Comeau’s
[“How I Built my Blog”](https://www.joshwcomeau.com/blog/how-i-built-my-blog/)
post, which uses a similar stack as my intended outcome.

### Existing Gatsby Structure

My Gatsby stack heavily used Markdown and [MDX](https://mdxjs.com/) for all my
content. I also used plugins for:

[AMP support](https://www.npmjs.com/package/@eyassh/gatsby-plugin-google-amp),- site-search via
[Algolia](https://www.algolia.com/), - sitemap generation,
- RSS feed generation,
- Google Analytics, and
- font prefetching.

I also heavily used Gatsby’s Image plugin, which optimizes images during build time.

Gatsby’s Markdown and MDX plugins use Remark, which in turn supports plenty of
plugins. I used Gatsby versions of remark plugins for
[PrismJS](https://prismjs.com/), video embeds, responsive iframes in MDX, and
[SmartyPants](https://github.com/retextjs/retext-smartypants) 2.

My existing URL structure (described [above](https://blog.eyas.sh#initial-migration)) also proved to
be a constant source of headaches.

### Migration Goals

My general ethos around this migration was still very similar to the first one:

-
**Keep the URL structure**. With a few exceptions (outlined below), I will do my best to prevent link rot and keep external links to my content valid.*almost exactly*the same -
**Maintain feature parity,**. Generating sitemaps and RSS feeds is crucial to me. I also wanted to take this opportunity to support new feed formats, like Atom and JSON feeds.*almost*

But I also have a few new requirements:

-
For the

*migration*,**the site should look exactly the same**. I like the theme that I have for my site, and while I’m open to iterating on it eventually, I don’t want obvious regressions.The easiest way for me to guarantee this is to make sure my site is largely identical, pixel-by-pixel. Diffs are easy to notice, and I can make a quick call whether it’s a regression.

-
The site’s bundle & core web vitals should be no worse than those of the Gatsby site.


I’m less interested in AMP these days, however. The cost of maintaining valid
AMP pages that *look exactly the same* as the non-AMP pages. Google also no
longer gives special treatment to AMP, making it much less compelling.

## Challenges

Following the Next.js documentation made it easy to make sure the core
components, styles, and site’s building blocks were working with Next.js.
Swapping over Gatsby’s `Link`

with `next/link`

, static Gatsby Images with
`next/image`

got me *mostly there*. I was using SCSS modules in my old site, and
Next.js supported that just fine (I wanted to switch to `styled-jsx`

for some
parts later, but getting things working out-of-the-box is very helpful).

After that, a few pieces were annoying but primarily mechanical, while a few others were fundamentally complex.

### Replacing Gatsby’s GraphQL static page queries (Easy)

Most static queries were doing one of two things:

-
**Looking up basic site metadata**. Here, I factored out the metadata in`gatsby-config.js`

into its own exported`.ts`

file:`export const metadata = { title: `Eyas's Blog`, author: "Eyas Sharaiha", description: "Occasional musings on software development, tech, " + "and anything else.", social: { twitter: `EyasSH`, }, siteUrl: "https://blog.eyas.sh/", };`

and I replaced any query looking for

`siteTitle`

with simply importing`metadata`

and referencing`metadata.title`

. -
**Loading local images.**Here, instead of:`import * as React from "react"; import { useStaticQuery, graphql } from "gatsby"; import { GatsbyImage } from "gatsby-plugin-image"; const Bio: React.FC = () => { const data = useStaticQuery<GatsbyTypes.ProfilePicQuery>(graphql` query ProfilePic { avatar: file(absolutePath: { regex: "/profile-pic.jpg/" }) { childImageSharp { gatsbyImageData(width: 50, height: 50, layout: FIXED) } } } `); return ( <> {/* ... */} <GatsbyImage image={data.avatar.childImageSharp.gatsbyImageData} alt="Eyas's Picture" /> </> ); }; export default Bio;`

we can do simply:

`import * as React from "react"; import Image from "next/image"; import ProfilePic from "../../public/assets/profile-pic.jpg"; const Bio: React.FC = () => { return <> {/* ... */} <Image src={ProfilePic} alt="" {/* other attrs as needed */} /> </>; }; export default Bio;`


I was left with one static query that was non-trivial: looking up all posts sorted by a “featured” annotation in the frontmatter and returning the featured posts. I use this to display curated featured posts at the top of the blog home page.

I stubbed the implementation and removed the query for the time being, as I
hadn’t yet actually implemented any code that loads & processes my `.md`

and
`.mdx`

content.

### Loading all .mdx pages (Medium)

In Gatsby, the MDX plugin automatically scans all your *.mdx files in a configured directory, sets up fast-refresh when your content changes, and can then be coupled with GraphQL queries over MDX documents to create corresponding pages.

In Next.js, you’re on your own. You’ll need to decide how to (a) read your .mdx files & frontmatter, (b) map that data to page routes, and (c) display the MDX on your page.

While MDX can have dynamic pages that fetch content from an `/api/`

endpoint on
request-time, I’m interested in keeping my site fully static. That means I’ll
want my post pages generated at build time, ideally with MDX content that is
fully parsed and ready to consume statically.

#### Next.js Page Structure

Since our goal is to generate static pages at build time, we should first understand how to generate static pages.

Next.js uses
[file-system based pages](https://nextjs.org/docs/basic-features/pages). Every
page on your website corresponds to a `/pages/**/*.(js|jsx|tsx)`

file. A single
file under `/pages/`

can correspond to one or more pages. For example,
`/pages/about.js`

creates a single page at `/about`

, while
`/pages/posts/[slug].js`

creates any number of pages under `/posts/:slug`

.

In Next.js, any page is static-generated if it can be. A page that fetches no
data is completely static. If you need to fetch data, you’ll need to decide
whether to do that server-side (using `getInitialProps`

or `getServerSideProps`

)
or statically on build-time (using `getStaticProps`

). The
[Next.js Data Fetching documentation](https://nextjs.org/docs/basic-features/data-fetching)
describes these.

In our case, we want to create *static pages* from a *dynamic* route. Most
Next.js blogs will have a page set up like `pages/posts/[slug].tsx`

corresponding to all of their blog posts. Mine ended up being a little bit more
complicated due to the URL structure that I need.
[I discuss how I got my URL structure working in the next section](https://blog.eyas.sh#url-structure).

Before I try to get my fancy URL scheme to work, let’s start with the basics. To get static pages to be created for a dynamic route, we’ll want our Next.js page to export two functions:

`getStaticPaths`

— which tells us at build time what all the available values for`[slug]`

are, and`getStaticProps`

— which performs all the build time computations needed to get an initial set of React props passed to the page template.

#### Processing .mdx files

You can roughly think of each `.mdx`

file as going through a few stages of
processing:

`.mdx`

file + frontmatter in my file system,- server-side in-memory representation of a post in Node.js
**during build**, - serialized JSON representation,
**generated during build**, which can be fetched later by the on request time, - fully parsed HTML in output page.

I separated the server-side `Post`

type from the shared client-server
`SerializedPost`

type.

```
export interface Post {
title: string;
slug: string;
created: Date;
tags: string[];
hero?: HeroImage;
featured: number;
___fileContent: string;
}
export interface HeroImage {
src: string;
width: number;
height: number;
title?: string;
ref?: string;
license?: string;
}
```


```
export interface SerializedPost {
title: string;
slug: string;
created: FormattedDate;
tags: string[];
path: string;
hero: SerializedHeroImage | null;
featured: number;
}
export interface SerializedHeroImage extends StaticImageData {
title: string | null;
ref: string | null;
license: string | null;
}
export interface FormattedDate {
iso: string;
long: string;
}
```


If I want to get a list of all blog posts, I can:

- scan all
`*.mdx`

files in my blog’s`content/posts/`

directory, and - turn the frontmatter and MDX of each file into a
`Post`

object.

If I want to create a page for a particular blog post, I can:

- find the corresponding
`Post`

file, - turn it into a
`SerializedPost`

object and parse the MDX, and - propagate the serialized object as a set of React props to the template that will eventually render it.

Other blogs might simply want to find and parse the `*.mdx`

file on demand when
a given page is processed. E.g., if your blog posts are on:
`mysite.com/blog/[slug]`

, your `[slug].tsx`

page can lazily fetch the page then.

I decided this didn’t make sense in my case: I inherited the WordPress URL
structure, so my posts are on `blog.eyas.sh/[YYYY]/[MM]/[slug]`

. But my `*.mdx`

pages are laid out flat in `content/posts/[yyyy]-[mm]-[dd]-[slug].mdx`

, making
it hard to infer the post’s source file path from the page URL.

Under the hood, build-time processing code for Blog Posts returns a
`Map<string, Post>`

mapping each `slug`

into a `Post`

. I represent this as a
memoized internal function called `initialize()`

. Both `getAllPosts()`

and
`getPost(slug: string)`

will call `initialize()`

if the Map is not yet created.

My `initialize`

function looks something like this:

```
import { readFile, readdir } from "fs/promises";
import path from "path";
import matter from "gray-matter";
import yaml from "js-yaml";
async function initialize(): Promise<Map<string, Post>> {
const paths = await readdir(postsDirectory);
const mdx = paths.filter((path) => path.endsWith(".mdx"));
const postContents = await Promise.all(
mdx.map(async (fullPath) => {
const fileContents = await readFile(fullPath, { encoding: "utf8" });
// Use gray-matter to parse the post metadata section
const matterResult = matter(fileContents, {
engines: {
yaml: (s) =>
yaml.load(s, { schema: yaml.JSON_SCHEMA }) as object,
},
});
const matterData = matterResult.data as {
title?: string;
slug?: string;
tags?: string[];
date?: string;
hero?: string;
heroTitle?: string;
heroLink?: string;
heroLicense?: string;
featured?: number;
};
const post: Post = {
title: matterData.title!,
slug: matterData.slug!,
created: new Date(matterData.date!),
tags: matterData.tags || [],
featured: matterData.featured || 0,
___fileContent: matterResult.content,
};
if (matterData.hero) {
// TODO: Get Hero Images Working.
}
return post;
})
);
return new Map(postContents.map((post) => [post.slug, post] as const));
}
```


Now that I have a server-side representation of my MDX post working, I’ll need
to figure out how to propagate that to rendered MDX content on the client.
Next.js provides its own [ @next/mdx](https://www.npmjs.com/package/@next/mdx)
package, and

[and](https://github.com/kentcdodds/mdx-bundler)

`mdx-bundler`

[are two others that are mentioned often.](https://github.com/hashicorp/next-mdx-remote)

`next-mdx-remote`

`@next/mdx`


Made by Next.js to support MDX, `@next/mdx`

is a safe bet when all you want to
do is use MDX in your pages.

It has some advantages:

- Allows you to have your own
`.mdx`

files in your`pages/`

directory - Supports local
`imports`


But some limitations:

- Limited resources & documentation
- Does not support frontmatter
- Does not support sourcing content from other directories or with non-1:1 path mappings

This isn’t entirely appropriate for my needs, where I have lots of MDX content
with frontmatter. I need dynamic URL routing based on this
frontmatter—structuring my `pages/`

directory with manually-created `yyyy/mm/`

directories doesn’t sound desirable.

`next-mdx-remote`


This library by Hashicorp is itself a replacement of another previously popular
MDX library by Hashicorp, `next-mdx-enhanced`

. This library allows MDX to be
loaded within `getStaticProps`

and hydrated on the client.

It has some advantages:

- You can source your
`.mdx`

files (other directories locally, or remotely, even) - Has tiny output
- MDX HTML is already correctly rendered server-side on page load

But some limitations:

- Does not support imports

As a lower-level library, you can read the MDX however you want. This means that you can use frontmatter just fine, as long as you parse it out first before handing the MDX content string to the MDX parser.

`mdx-bundler`


Kent C Dodds provides a similar option: mdx-bundler takes in your MDX source as a string and outputs the code to generate the React code corresponding to the markdown content.

It has some advantages:

- You can source your
`.mdx`

files from anywhere (other directories locally, or remotely, even) - You can use
`import`

statements, but you’ll need to specify the universe of possible imported files (and their contents) on build time - Natively supports frontmatter
- Uses
`xdm`

, which is the “preview” version of the next version of MDX

But some limitations:

- Will need some one-time
[workarounds](https://github.com/kentcdodds/mdx-bundler#nextjs-esbuild-enoent)for Next.js - Produces a larger output than
`next-mdx-remote`


The benefits of `mdx-bundler`

are not necessarily worthwhile for me. I did not
have any imports of other TS or JS files in my MDX, only a few static imports
for Videos, etc.

For me, `next-mdx-remote`

was the right choice. For `getStaticProps`

, I created
this helper:

```
// /lib/server/posts/props.ts
import { serialize } from "next-mdx-remote/serialize";
import type { Post } from "./types";
import { Serialize } from "./serialize";
import { mdxOptions } from "../../shared/posts/_options";
export async function BlogPost_GetProps(post: Post) {
const details = Serialize(post);
const mdxSource = await serialize(post.___fileContent, {
mdxOptions,
});
return {
source: mdxSource,
details,
};
}
```


When it came time to render the MDX, I used the `source`

prop and
`next-mdx-remote`

to get the job done:

```
import React from "react";
import { MDXRemote } from "next-mdx-remote";
import { PostPage } from "../components/post/post-page";
const components = {
/* ... */
};
export default function BlogPost(props) {
return (
<>
<PostPage post={props.details}>
<MDXRemote
{...props.source}
components={components}
></MDXRemote>
</PostPage>
</>
);
}
```


### (Medium) Getting Images working

#### Images should at least show up

In Gatsby, my source structure looked like this:

`content/posts/`

`yyyy-mm-dd-slug/`

`index.mdx`

`images/`

`image-name.jpg`





In `index.mdx`

, I referred to images by using
`![image](./images/image-name.jpg)`

. Gatsby then copied the image output to the
appropriate place under its `public/`

directory and served it properly. All
links worked as expected.

With Next.js, this is now *my* responsibility. I tried all sorts of “tricks” to
get locally-referenced images working, but it didn’t quite work. Next.js doesn’t
like serving static files outside of the `public/`

directory, and I didn’t quite
figure out a clean way to intercept the build process to copy these files
myself.

I ended up giving up here. I changed my image references from relative to
absolute paths. I moved all my images out of `content/posts/**/`

and into
`public/blog-static-content/`

, then referenced them as such.
`![image](./images/image-name.jpg)`

became
`![image](/blog-static-content/image-name.jpg)`

. I lost co-locating images with
my blog posts in a folder, which was a bit of a bummer.

When I was sure this was the right path, I took the liberty of flattening my source structure so that it is now:

`content/posts/`

`yyyy-mm-dd-slug.mdx`



#### Using `next/image`

in the blog

To get images working *well*, I’d like to take advantage of `next/image`

’s
features, namely:

- lazy loading images,
- image optimization,
- automatically generating source sets for different dimensions.

The key inputs the `<Image>`

component needs to render an image are:

```
interface StaticImageData {
src: string;
height: number;
width: number;
blurDataURL?: string;
}
```


We spent the last section figuring out how to get `src`

propagated correctly.
Next, we want to make sure we can find `width`

and `height`

for our images
during build time. Doing so allows us to render our HTML with image elements at
the correct size without causing content to jump around when the image loads.

I expanded my MDX parsing options to include an “image metadata” plugin:

```
import { SerializeOptions } from "next-mdx-remote/dist/types";
import remarkHeadingId from "remark-heading-id";
import prism from "remark-prism";
import remarkUnwrapImages from "remark-unwrap-images";
import { smartypants } from "../../plugins/smartypants";
import { imageMetadata } from "../../plugins/image-metadata";
export const mdxOptions: SerializeOptions["mdxOptions"] = {
rehypePlugins: [imageMetadata],
remarkPlugins: [smartypants, prism, remarkHeadingId, remarkUnwrapImages],
};
```


[Kyle Pformer’s post on Next.js MDX images](https://kylepfromer.com/blog/nextjs-image-component-blog)
is excellent here. His implementation of `imageMetadata`

is the basis for mine.

Then, I added an `MdxImg`

component, which acts as a shim for an `<img>`

in an
MDX document, and passes it on to `next/image`

:

```
// src/components/mdx-img.tsx
import Image, { ImageProps } from "next/image";
/** MdxImg can receive any attribute from a native <img> element. */
interface MdxImgProps extends React.ImgHTMLAttributes<HTMLImageElement> {
blurDataURL?: string;
}
export const MdxImg: React.FC<MdxImgProps> = ({
src,
width,
height,
alt,
blurDataURL,
// Explicitly discard the following props:
srcSet, // next/image will generate a better srcSet
loading, // always use "lazy"
style, // next/image doesn't accept inline styles
placeholder, // driven by blurDataURL
...otherProps
}) => {
const props: ImageProps = {
// If we care about the generated srcSet, we might still want
// "responsive".
//
// "intrinsic" is closest to the default GatsbyImage & <img> elements:
// It grows until its size & stops growing.
// "responsive" keeps growing to fit the width of the container.
//
// "intrinsic" only has a srcSet for "1x" and "2x" sizes, rather than
// adapting for many widths.
layout: "intrinsic", // Matches behavior of native `<img>` element.
loading: "lazy",
src: src!,
height: height!,
width: width!,
blurDataURL,
placeholder: blurDataURL ? "blur" : "empty",
...otherProps,
} as const;
return <Image alt={alt} {...props} />;
};
```


Now, we can pass this component to the `components`

prop of `<MDXRemote>`

:

```
import React from "react";
import { MDXRemote } from "next-mdx-remote";
import { PostPage } from "../components/post/post-page";
+import { MdxImg } from "../components/mdx-img";
const components = {
+ img: MdxImg,
/* ... */
};
export default function BlogPost(props) {
return (
<>
<PostPage post={props.details}>
<MDXRemote
{...props.source}
components={components}
></MDXRemote>
</PostPage>
</>
);
}
```


Ideally, we will also want the blur-up placeholder effect to work on our
MDX-loaded images. Given our setup in `MdxImage`

, we only need to add a
blurDataURL base64 string similar to that expected by `next/image`

.

By default, Next.js doesn’t expect you to pass a `blurDataURL`

by hand; any
`import`

ed file will automatically include a `blurDataURL`

property. A
[custom Webpack loader](https://github.com/vercel/next.js/blob/canary/packages/next/build/webpack/loaders/next-image-loader.js)
achieves this for images.

The
[source code](https://github.com/vercel/next.js/blob/canary/packages/next/build/webpack/loaders/next-image-loader.js)
for `next-image-loader.js`

shows how the default behavior generates `src`

,
`height`

, `width`

, and `blurDataURL`

. In particular, the `blurDataURL`

is an
encoded version of a resized image:

```
// Constants at the top of next-image-loader.js
const BLUR_IMG_SIZE = 8;
const BLUR_QUALITY = 70;
const VALID_BLUR_EXT = ["jpeg", "png", "webp"];
// Simplified version of the relevant code, later on in the file:
const resizedImage = await resizeImage(
content,
dimension,
BLUR_IMG_SIZE,
extension,
BLUR_QUALITY
);
blurDataURL = `data:image/${extension};base64,${resizedImage.toString(
"base64"
)}`;
```


You can look at `resizeImage`

itself in the server-side
[image optimizer](https://github.com/vercel/next.js/blob/canary/packages/next/server/image-optimizer.ts).

We can extend the `imageMetadata`

rehype plugin to set a blurDataURL attribute
on an `<img>`

:

```
// src/plugins/image-metadata.ts
// Showing only modified version of the original code.
// https://kylepfromer.com/blog/nextjs-image-component-blog
async function addMetadata(node: ImageNode): Promise<void> {
const imagePath = path.join(process.cwd(), "public", node.properties.src);
const res = await sizeOf(imagePath);
if (!res) throw Error(`Invalid image with src "${node.properties.src}"`);
node.properties.width = res.width;
node.properties.height = res.height;
const imageBlurExt = imagePath.match(/\.(png|webp|jpg|jpeg)$/);
if (imageBlurExt && res.width && res.height) {
// Compure Blur URL for these types of images.
// This code is based on next/build/webpack/loaders/next-image-loader.js
// Shrink the image's largest dimension
const dimension = res.width >= res.height ? "width" : "height";
const extension = imageBlurExt[1].replace("jpg", "jpeg");
const content = await readFile(imagePath);
const resizedImage = await resizeImage(
content,
dimension,
BLUR_IMG_SIZE,
extension,
BLUR_QUALITY
);
const blurDataURL = `data:image/${extension};base64,${resizedImage.toString(
"base64"
)}`;
node.properties.blurDataURL = blurDataURL;
}
}
```


#### Last Modified Time

I also want my blog posts to have a “Last Modified” timestamp. This can be
included in my RSS feeds, `<meta>`

tags, and JSON-LD metadata.

There are different strategies to do this, but I liked what
[ gatsby-transformer-gitinfo](https://github.com/kraynel/gatsby-transformer-gitinfo)
does: use the last commit time from a

`git log`

command on a file to determine
when it was last modified.```
export interface Post {
title: string;
slug: string;
created: Date;
+ lastModified: Date;
tags: string[];
hero?: HeroImage;
featured: number;
___fileContent: string;
}
function getAllPosts(): Post[] {
const paths = await readdir(postsDirectory);
const mdx = paths.filter((path) => path.endsWith(".mdx"));
const postContents = await Promise.all(
mdx.map(async (fullPath) => {
- const fileContents = await readFile(fullPath, { encoding: "utf8" });
+ // Fetch fileContents and lastModified in parallel...
+ const [fileContents, lastModified] = await Promise.all([
+ readFile(fullPath, { encoding: "utf8" }),
+ getLastModifiedTime(fullPath),
+ ]);
@@ -1,6 +1,6 @@
const post: Post = {
title: matterData.title!,
slug: matterData.slug!,
created: new Date(matterData.date!),
+ lastModified: lastModified || new Date(matterData.date!),
tags: matterData.tags || [],
featured: matterData.featured || 0,
___fileContent: matterResult.content,
};
```


#### Excerpts

I also want to generate excerpts of my blog posts to preview in my index and archive pages. Excerpts are one area where I planned to go beyond parity with Gatsby.

Gatsby’s MDX plugin didn’t allow me to fetch formatted excerpts; instead, it
simply took the first `N`

characters of the markdown—converted to
plaintext—and returned that as the excerpt.

Ideally, my index and archive pages will include the first few paragraphs of MDX in all of their glory: with formatting & links.

The `gray-matter`

loader can receive an `excerpt`

function that defines what the
excerpt string should look like. Some might implement that to split the document
until a predefined string (e.g., `<!-- more -->`

, or simply the first `---`

) is
found. I wanted to do something automatically (so I don’t have to worry about
placing an excerpt separator manually), so I decided to take the first two
paragraphs.

The straightforward approach *mostly* worked:

```
(file_, options) => {
// Typings think file_ is a string, but it isn't.
const file = file_ as {} as matter.GrayMatterFile<string>;
const firstTwoParagraphs = file.content
.replace(/\r\n/g, "\n") // Normalize line endings
.split(/\n\n+/, 2) // Take first two paragraphs
.join("\n\n");
// The assignment is what's important, though typings say otherwise.
file.excerpt = firstTwoParagraphs;
return firstTwoParagraphs;
};
```


But I ran into a few issues:

- Some of my markdown had
`import`

statements.[3](https://blog.eyas.sh#user-content-fn-3) - Sometimes I had a heading as my first or second paragraph.
- I had images, videos, and other MDX components appear in the excerpt.
- I had old posts with more lines than necessary, or lines with spaces in them, etc.
- I had code blocks early on in a few posts. I decided to strip these away.

```
export interface Post {
@@ -12,6 +12,7 @@
hero?: HeroImage;
featured: number;
___fileContent: string;
+ ___excerptContent: string | undefined;
}
function getAllPosts(): Post[] {
@@ -32,7 +33,25 @@
yaml: (s) =>
yaml.load(s, { schema: yaml.JSON_SCHEMA }) as object,
},
+ excerpt: (file_, options) => {
+ const file = file_ as {} as matter.GrayMatterFile<string>;
+
+ const firstTwoParagraphs = file.content
+ .replace(/^import [a-zA-Z_][a-zA-Z0-9_]* from ".*";$/gm, "") // Strip imports
+ .replace(/^#.*$/gm, "") // Remove headings if they show up this soon
+ .replace(/\r\n/g, "\n") // Normalize line endings
+ .replace(/<[^>]*>?/gm, "") // Strip HTML
+ .replace(/^\s*\n/gm, "\n") // Strip lines with just spaces
+ .split("```", 1)[0] // Ignore anything after the first code block.
+ .trimStart()
+ .split(/\n\n+/, 2) // Take first two paragraphs
+ .join("\n\n");
+
+ // The assignment is what's important, though typings say otherwise.
+ file.excerpt = firstTwoParagraphs;
+ return firstTwoParagraphs;
+ },
});
const matterData = matterResult.data as {
title?: string;
slug?: string;
@@ -54,6 +73,7 @@
featured: matterData.featured || 0,
___fileContent: matterResult.content,
+ ___excerptContent: matterResult.excerpt,
};
if (matterData.hero) {
```


The result is that now `___excerptContent`

looks like simpler Markdown that only
contains two paragraphs. MDX, code blocks, fancy HTML, and headings are not
included in the string, but the paragraphs still have links, formatting, etc.

I don’t want the excerpt to always be included in the `SerializedPost`

, so
instead, I created a separate type & function:

```
import { MDXRemoteSerializeResult } from "next-mdx-remote";
export interface SerializedPostWithExcerpt extends SerializedPost {
excerpt: MDXRemoteSerializeResult | null;
}
```


```
export async function SerializeWithExcerpt(
post: LinkedPost
): Promise<SerializedPostWithExcerpt> {
return {
...Serialize(post),
excerpt: post.___excerptContent
? await serialize(post.___excerptContent)
: null,
};
}
```


### Getting my URL structure to work

You can expect a blog to make quite a lot of use of Next.js
[dynamic routes](https://nextjs.org/docs/routing/dynamic-routes). Posts, tags,
and paginated archives are all dynamic and change with the contents of the blog.

My basic routes look something like this:

`/`

: the home page`/page/:page/`

: the home page with pagination`/tag/:tag/`

: a tag page`/tag/:tag/page/:page/`

: a tag page with pagination

`/:md-page/`

: a static page from a Markdown file (e.g., About, Contact, etc.)`/:yyyy/`

: a year archive`/:yyyy/page/:page/`

: a year archive with pagination`/:yyyy/:mm/`

: a month archive`/:yyyy/:mm/page/:page/`

: a month archive with pagination`/:yyyy/:mm/:slug/`

: a blog post




Naively, I thought I could create both a `[md-page].tsx`

route and a `[yyyy]/`

folder (with `index.tsx`

and a `[mm]/`

folder, etc.), but then `[md-page]`

and
`[yyyy]`

would collide. Instead, Next.js wants you to make sure these variables
are the same. I tried renaming it to `[year-or-page]`

. But things got pretty
complicated. When I got it to work, nested pages of `[year-or-page]`

broke.

In many cases, my fix to these complicated conflicts was to create a unified
component that switches between the two routes. In other words, I created a
“parent” route that returned the union of both `getStaticPaths`

and used the
path to determine which sub-function to call into for `getStaticProps`

.

This fixed some cases but kept ballooning. Eventually, I decided to embrace chaos and ditch Next.js routing altogether, and create my own super-router.

#### Enter `[[...chunks]].tsx`


The idea was this: create all of my routes imperatively from looking up blog
posts, tags, etc. and define these in a `Map<string, AnyRoute>`

, where the key
is the path and the value contains my definition of the route.

I’ll stress that this isn’t something I recommend if you have a URL scheme that the built-in dynamic routing could handle. I still expect to move away from this at some point.

```
// src/lib/shared/router.ts
import {
BlogIndexProps,
BlogPostProps,
CalendarArchiveProps,
MdPageProps,
TagArchiveProps,
} from "../../_pages/shared/props";
export interface TemplateProps {
BlogIndex: BlogIndexProps;
CalendarArchives: CalendarArchiveProps;
TagArchiveTemplate: TagArchiveProps;
MdPage: MdPageProps;
BlogPost: BlogPostProps;
}
export interface ChunkRouterProps<T extends keyof TemplateProps> {
Template: T;
CanonicalUrl: string;
InnerProps: TemplateProps[T];
}
```


```
// src/pages/[[...chunks]].tsx
import React, { FC } from "react";
import { GetStaticPaths, GetStaticProps } from "next";
import { ChunkRouterProps, TemplateProps } from "../lib/shared/router";
import { getPaths, getProps } from "../lib/server/router";
/** (collapsed): Import BlogIndex et al. from ../pages/ */
type PageTemplatesType = {
[TName in keyof TemplateProps]: FC<TemplateProps[TName]>;
};
const PageTemplates: PageTemplatesType = {
BlogIndex,
CalendarArchives,
TagArchiveTemplate,
MdPage,
BlogPost,
} as const;
function ChunkRouter<T extends keyof typeof PageTemplates>(
props: ChunkRouterProps<T>
) {
const Component = PageTemplates[props.Template];
return <Component {...(props.InnerProps as any)} />;
}
export default ChunkRouter;
export const getStaticProps: GetStaticProps = getProps;
export const getStaticPaths: GetStaticPaths = getPaths;
```


```
// src/lib/server/router.ts : Scaffolding
import type { GetStaticPaths, GetStaticProps } from "next";
import type { ChunkRouterProps, TemplateProps } from "../shared/router";
import { metadata } from "../../metadata";
import { paginate } from "../paginator";
import { getAllPosts } from "./posts";
import { BlogPost_GetProps } from "../../_pages/server/blog-post";
import { BlogIndex_GetProps } from "../../_pages/server/blog-index";
// (collapsed): Import other props from _pages/server/
type TemplateType = keyof TemplateProps;
interface Route<
Template extends TemplateType,
TProps extends TemplateProps[Template]
> {
path: string;
component: TemplateType;
props: () => Promise<TProps>;
}
type AnyRoute = Route<TemplateType, TemplateProps[TemplateType]>;
type Routes = Map<string, AnyRoute>;
function createPage<
Template extends TemplateType,
TProps extends TemplateProps[Template]
>(route: Route<Template, TProps>, routes: Routes) {
const routeCopy = { ...route };
routeCopy.path = routeCopy.path.replace(/\/$/, "").replace(/^\//, "");
routes.set(slimPath, routeCopy);
}
```


```
// src/lib/server/router.ts (continued): Page Generation
let _rp: Promise<Routes>;
function initialize(): Promise<Routes> {
if (!_rp) _rp = RoutesPromise();
return _rp;
}
async function RoutesPromise(): Promise<Routes> {
const routes = new Map();
const mdx = await getAllPosts();
const makePage = (route) => createPage(route, routes);
// 1. .mdx Posts
for (const post of mdx) {
makePage({
path: `${post.Y}/${post.MM}/${post.slug}`,
component: "BlogPost",
props: () => BlogPost_GetProps(post),
});
}
// 2. Blog Archive (+ Pages)
for (const archivePage of paginate(mdx, "")) {
makePage({
path: archivePage.path,
component: "BlogIndex",
props: () => BlogIndex_GetProps(archivePage),
});
}
// (do the same for the other archives & their pages)
return routes;
}
```


```
// src/lib/server/router.ts (continued): Exports
export const getPaths: GetStaticPaths<{ chunks?: string[] }> = async () => {
const routes = await initialize();
return {
paths: Array.from(routes.values()).map(({ path }) => ({
params: { chunks: path.split("/") },
})),
fallback: false,
};
};
export const getProps: GetStaticProps<
ChunkRouterProps<TemplateType>,
{} | { chunks: string[] }
> = async function getProps(context) {
const routes = await initialize();
const path =
("chunks" in context.params && context.params.chunks.join("/")) || "";
const route = routes.get(path);
if (!route) return { notFound: true };
return {
props: {
Template: route.component,
CanonicalUrl: `${metadata.siteUrl}${route.path}/`,
InnerProps: await route.props(),
},
};
};
```


The risk here is that the `[[...chunks]].tsx`

file loads the templates for all
my pages. I wasn’t sure how smart Next.js would be about splitting it. I wasn’t
sure if it *needed* to be split; how large are the bundled .js when including
all these different templates?

I implemented this solution and took a look at the resulting bundle size. I was
surprised that it was *already* smaller than what I had with Gatsby.

Having `src/lib/server/router.ts`

was also a nice full-circle moment with
Gatsby. A lot of the logic here, where pages are created imperatively, mirrors
exactly the logic I had in my `gatsby-node.js`

file where I created pages from
GraphQL queries.

### Implementing Sitemaps and Feeds

To get sitemaps & feeds working, I had to create my own Node scripts to do this.
I had previously used the [sitemap](https://www.npmjs.com/package/sitemap)
package in my old blog and had a good experience. I’ll do the same here.

```
// scripts/generate-sitemap.ts
import path from "path";
import { writeFile } from "fs/promises";
import {
SitemapStream,
ErrorLevel,
streamToPromise,
SitemapIndexStream,
} from "sitemap";
import { sitemapRoutes } from "../src/lib/server/router";
import { metadata } from "../src/metadata";
const PUBLIC_PATH = "./public/";
async function generateSitemap() {
const sitemap = new SitemapStream({
hostname: metadata.siteUrl.replace(/\/$/, ""),
level: ErrorLevel.THROW,
});
const sitemapIndex = new SitemapIndexStream({
level: ErrorLevel.THROW,
});
for (const entry of await sitemapRoutes()) {
sitemap.write({
url: entry.canonicalUrl,
lastmod: entry.lastModified,
});
}
sitemap.end();
sitemapIndex.write({
url: path.posix.join(metadata.siteUrl, "sitemap-1.xml"),
});
sitemapIndex.end();
await writeFile(
path.posix.join(PUBLIC_PATH, `sitemap-1.xml`),
await streamToPromise(sitemap)
);
await writeFile(
path.posix.join(PUBLIC_PATH, `sitemap.xml`),
await streamToPromise(sitemapIndex)
);
}
generateSitemap();
```


```
// src/lib/server/router.ts (continued): Sitemap Generation
interface Entry {
canonicalUrl: string;
lastModified?: string;
}
export const sitemapRoutes = async (): Promise<Entry[]> => {
const routes = await initialize();
const allRoutes = Array.from(routes.values());
return Promise.all(
allRoutes.map(async ({ path, props }) => {
const p = await props();
return {
canonicalUrl: joinPath(siteUrl, path, "/"),
lastModified: getLastModified(p),
};
})
);
};
```


Since I used TypeScript here, I’ll need a TSConfig file that a TypeScript runner
like [ts-node](https://www.npmjs.com/package/ts-node) could use. I created this
in my top-level directory:

```
// tsconfig.commonjs.json
{
"extends": "./tsconfig.json",
"compilerOptions": {
"module": "CommonJS",
"jsx": "react"
}
}
```


Then I add a `"generate-sitemap"`

script to my `package.json`

, which roughly
corresponds to:

```
cross-env TS_NODE_PROJECT='./tsconfig.commonjs.json' \
ts-node -T ./scripts/generate_sitemap.ts
```


We could do something similar for feeds. I like Jean-Philippe Monette’s
[feed](https://www.npmjs.com/package/feed) package.

```
// scripts/generate-feed.ts : Main function
async function generateFeed() {
const feed = new Feed({
id: metadata.siteUrl,
title: metadata.title,
copyright: "All rights reserved",
updated: new Date(),
feedLinks: {
rss: join(metadata.siteUrl, PATHS.rss),
atom: join(metadata.siteUrl, PATHS.atom),
},
});
// Want tags in Title Case, I already have this in a Map.
const tagDetails = await getTagDetails();
for (const details of tagDetails.values()) {
feed.addCategory(details.tagTitle);
}
for (const entry of await getAllPosts()) {
// We only want to process blog posts for our feed.
const props = blogPostProps(entry);
if (!props) continue;
const {
details: { lastModified, created, title, tags },
source,
} = props;
feed.addItem({
id: entry.canonicalUrl,
link: entry.canonicalUrl,
title,
content: renderToString(source),
date: new Date(lastModified.iso),
published: new Date(created.iso),
category: tags.map((tag) => ({
name: tagDetails.get(tag)!.tagTitle,
})),
});
}
await writeFile(join("./public", PATHS.rss), feed.rss2());
await writeFile(join("./public", PATHS.atom), feed.atom1());
}
const PATHS = {
rss: "feed/rss.xml",
atom: "feed/atom.xml",
};
generateFeed();
```


```
// Render helpers
import React, { FC } from "react";
import ReactDOMServer from "react-dom/server";
import { MDXRemote } from "next-mdx-remote";
import type { MDXRemoteSerializeResult } from "next-mdx-remote";
// Renders our MDX component in simplified HTML for consumption
// by feeds.
export function renderToString(source: MDXRemoteSerializeResult) {
return ReactDOMServer.renderToString(
<MDXRemote {...source} components={components} />
).replace(/<!--[\s\S]*?-->/g, "");
}
// Stub versions of our shortcodes, to be rendered in plain HTML.
const DropCap: FC = ({ children }) => <>{children}</>;
const Block: FC = ({ children }) => <div>{children}</div>;
function Img({ blurDataURL, ...props }: MdxImgProps) {
return <img {...props} />;
}
const components = { DropCap, Block, img: Img }; // etc.
```


```
// Fetching helpers
export async function blogPostProps(entry: Entry) {
// Infer chunks from entry. Alternatively, we can change
// sitemapRoutes to include chunks in the entry.
const chunks = entry.canonicalUrl
.replace(metadata.siteUrl, "")
.split("/")
.filter((chunk) => !!chunk);
const getPropsResult = await getProps({ params: { chunks } });
if ("notFound" in getPropsResult)
throw new Error("Sitemap Entry should always be found");
if ("redirect" in getPropsResult)
throw new Error("Unexpected redirect in Sitemap Entry");
const props = _gp.props;
if (!isTemplate(props, "BlogPost")) return undefined;
return porps;
}
export function isTemplate<T extends keyof TemplateProps>(
props: ChunkRouterProps<keyof TemplateProps>,
template: T
): props is ChunkRouterProps<T> {
return props.TemplateName === template;
}
```


### Implementing Search Indexing

In my Gatsby site, I used [Algolia](https://www.algolia.com/) for search. They
provided a
[useful Gatsby plugin](https://www.npmjs.com/package/gatsby-plugin-algolia) and
[instructions](https://www.gatsbyjs.com/docs/adding-search-with-algolia/) that
made it easier.

Now, I wanted to port that logic over to Next.js. I decided to implement indexing similar to what I had done for the sitemap and RSS feeds.

In Gatsby, my indexing logic looked like a GraphQL query and a mapping function. My mapping function can remain the same, but instead of a GraphQL query, I can now loop over all my pages.

Given [my setup using [[...chunks]].tsx](https://blog.eyas.sh#chunks) as an optional catch-all
route, I can loop over all pages in my site and index them.

In Gatsby, I only indexed my posts, so I did the same here.

```
async function generateIndex() {
dotenv.config();
const client = algoliasearch(
process.env.NEXT_PUBLIC_ALGOLIA_APP_ID,
process.env.ALGOLIA_SEARCH_ADMIN_KEY
);
const index = client.initIndex("Posts");
const routes = await sitemapRoutes();
const props = await Promise.all(
routes.map(
async (entry) => [entry, await blogPostProps(entry)] as const
)
);
const records = props
.filter((e): e is [Entry, BlogPostProps] => !!e[1])
.map(([entry, props]) => ({
objectID: entry.canonicalUrl,
title: props.details.title,
date: props.created.iso,
tags: props.details.tags,
slug: props.details.slug,
image: props.details.hero?.src,
path: entry.canonicalUrl.replace(metadata.siteUrl, ""),
featured: props.details.featured,
}));
await index.saveObjects(records);
}
```


I needed to explicitly install [dotenv](https://www.npmjs.com/package/dotenv)
and add my Algolia keys to my .env file. The .env file should be in your
.gitignore so that you don’t leak secrets to git. You can then specify the
environment variable directly in Netlify and Vercel.

My client-side search logic looked the same:

```
import React, { useState } from "react";
import { useRouter } from "next/router";
import { InstantSearch } from "react-instantsearch-dom";
import algoliasearch from "algoliasearch/lite";
import { SearchBox } from "../components/search/search-box";
import { SearchResult } from "../components/search/search-result";
const indices = [{ name: `Posts`, title: `Posts` }] as const;
const SearchPage: React.FunctionComponent = () => {
function makeSearchUrl(query: string | null | undefined) {
if (!query) return "";
return `?q=${query}`;
}
const router = useRouter();
const { q } = router.query;
const [query, setQuery_] = useState<string | undefined>(() => {
return q as string | undefined;
});
const setQuery = (queryString: string) => {
router.replace(makeSearchUrl(queryString));
setQuery_(queryString);
};
const searchClient = algoliasearch(
process.env.NEXT_PUBLIC_ALGOLIA_APP_ID!,
process.env.NEXT_PUBLIC_ALGOLIA_SEARCH_API_KEY!
);
return (
<InstantSearch
searchClient={searchClient}
indexName={indices[0].name}
searchState={{ query: query }}
onSearchStateChange={({ query }) => setQuery(query)}
>
<h1>
{!!query ? (
<>Search results for “{query}”</>
) : (
<>Search</>
)}
</h1>
<SearchBox />
<SearchResult
show={!!(query && query.length > 0)}
indices={indices}
/>
</InstantSearch>
);
};
export default SearchPage;
```


My `<SearchBox>`

and `<SearchResult>`

components are pretty much the same as
Gatsby’s guides for
[search box](https://www.gatsbyjs.com/docs/adding-search-with-algolia/#search-box)
and
[displaying results](https://www.gatsbyjs.com/docs/adding-search-with-algolia/#displaying-search-results).

### Explicit `prebuild`

& `postbuild`


Gatsby plugins generate sitemaps and index your site, usually by plugging into
Gatsby’s `onPostBuild`

step within `gatsby build`

.

I couldn’t find a straightforward way to do this within Next.js, but I ended up
taking advantage of NPM’s `"prebuild"`

and `"postbuild"`

steps to do this
automatically:

```
{
"scripts": {
"dev": "next dev",
"prebuild": "npm run generate-sitemap && npm run generate-feed && npm run update-index",
"build": "next build",
"start": "next start",
"format": "prettier --write \"**/*.{js,jsx,json,md}\"",
"generate-sitemap": "node ./scripts/generate_sitemap.js",
"generate-feed": "node ./scripts/generate_feed.js",
"update-index": "node ./scripts/update_index.js"
}
}
```


I put sitemap and feed generation in `"prebuild"`

because it outputs files to
the `/public/`

directory, which Next.js still needs to pick up during the build.
Indexing can go pretty much anywhere.

We can now add the prebuilt outputs (`sitemap.xml`

, `feed/rss.xml`

, etc.) to our
.gitignore and count on our continuous deployment scripts to create those files
on each build.

Note the simplified script for `"generate-sitemap"`

*et al.* here. These are
just there for brevity. If you use plain JS, it will be this simple. If you want
to use TypeScript in these scripts, you’ll need something that looks like this:

```
cross-env TS_NODE_PROJECT='./tsconfig.commonjs.json' \
ts-node -T ./scripts/generate_sitemap.ts
```


## Optimizations

Once I had the site up and running, it was time to look at load times and bundle sizes to see where there’s headroom to improve things.

### Explicit `Image.sizes`


Images wrapped with `next/image`

are already optimized and only load when
they’re in the viewport. But I still noticed that a lot of the images loaded
were unnecessarily large.

Next.js chooses `srcSet`

and `sizes`

values based on the `layout`

property
passed to `<Image>`

:

`layout` | Behavior | `srcSet` | `sizes` |
|---|---|---|---|
`fill` | Grow in X and Y axes to fill container | `640w` , `750w` , … `2048w` , `3840w` | `100vw` |
`fixed` | Sized to `width` and `height` exactly | `1x` , `2x` | N/A |
`intrinsic` | Scale down to fit width of container, up to image size | `1x` , `2x` | N/A |
`responsive` | Scale to fit width of container | `640w` , `750w` , … `2048w` , `3840w` | `100vw` |

A few interesting things to note:

- Your
`intrinsic`

images will always be loaded at their`width`

and`height`

. If you have a huge image that can scale down quite a bit,`next/image`

will still request a higher resolution image than you need. - Your
`responsive`

images will pick an image to use based on`100vw`

. In cases where the container is much smaller than`100vw`

(e.g., fixed max-width or a flex/grid layout taking up a certain percentage of the width), you’ll still pay the price of whatever your viewport size is.

Knowing this, I had to make a few decisions:

-
I knew I wanted to change my

`MdxImg`

component to set`layout="responsive"`

.Most of the images in my MDX are large images or photos, and I don’t want the user to pay the

`1x`

cost of a huge image. The side effect here will be that a few smaller images will now scale up to the entire width of the container. But I don’t think it looks too silly.I could, of course, override the

`srcSet`

for`intrinsic`

images, but I was too lazy for that. -
I needed to give my

`responsive`

images a more reasonable width hint that can be used to generate a more realistic`sizes`

field.I have a specified structure of “Blocks” that I use to lay out my content. Therefore, I can know pretty well the width of each block.


#### Width Hint Context

First, I wanted a way to express the “width hint” affecting a given image. I came up with this:

```
// src/components/width-hint.ts
export type Size = {
size: number;
unit: "vw" | "rem" | "px";
};
export interface WidthHintProps {
/** Screen Width <= 580px*/
S: Size;
/** 580px < Screen Width <= 700px */
M: Size;
/** 700px < Screen Width */
L: Size;
___shortcutSizes?: string;
}
export function toSizes({ S, M, L, ___shortcutSizes }: WidthHintProps): string {
if (___shortcutSizes) return ___shortcutSizes;
const sS =
S.unit === "vw"
? `${S.size}${S.unit}`
: `(max-width: ${S.size}${S.unit}) ${S.size}${S.unit}, 100vw`;
const sM =
M.size !== S.size || M.unit !== S.unit
? `(min-width: 580px) ${M.size}${M.unit}, `
: "";
const sL =
L.size !== M.size || L.unit !== M.unit
? `(min-width: 700px) ${L.size}${L.unit}, `
: "";
return `${sL}${sM}${sS}`;
}
```


I decided to implement a width hint that implies a particular image’s size (in
`vw`

, `rem`

, or `px`

) at given breakpoints. It might not always be exact, but it
should be closer to the available width of the image than the default from a
`"responsive"`

layout. I’m sure there are much better ways to do this (if you
think of one, [let me know on Twitter](https://twitter.com/Eyas) or
[email](mailto:hello@eyas.sh)).

I also added `__shortcutSizes`

to the interface. This serves two purposes:
first, to save the browser some string generation when the string is known at
build time, and second, to start from clearer (and more accurate) sizes in some
instances.

Now, I want to make `WidthHintProps`

available as a
[Context](https://reactjs.org/docs/context.html) to any component that asks
about it:

```
// src/components/width-hint.ts (continued)
import { createContext } from "react";
export const WidthHintContext = createContext<WidthHintProps>({
S: { size: 100, unit: "vw" },
M: { size: 100, unit: "vw" },
L: { size: 100, unit: "vw" },
___shortcutSizes: "100vw",
});
```


Here, we see that the initial `WidthHintContext`

is set to `100vw`

since we
start with no elements constraining the width of our images.

We can use this in `MdxImg`

:

```
// src/components/mdx-img.tsx
import Image, { ImageProps } from "next/image";
+import { useContext } from "react";
+import { toSizes, WidthHintContext } from "./width-hint";
/** MdxImg can receive any attribute from a native <img> element. */
interface MdxImgProps extends React.ImgHTMLAttributes<HTMLImageElement> {
blurDataURL?: string;
}
export const MdxImg: React.FC<MdxImgProps> = ({
@@ -22 +24 @@
const props: ImageProps = {
- layout: "intrinsic", // Matches behavior of native `<img>` element.
+ layout: "responsive",
loading: "lazy",
src: src!,
+ sizes: toSizes(useContext(WidthHintContext)),
height: height!,
width: width!,
blurDataURL,
placeholder: blurDataURL ? "blur" : "empty",
...otherProps,
} as const;
return <Image alt={alt} {...props} />;
};
```


Now, we need our “Blocks” to override the `WidthHintContext`

as they change and
constrain the layout.

##### This Blog’s Building Block

Let me first describe the “blocks” that I have available:

| Block | Description | Max Width | Direct Child Max Width |
|---|---|---|---|
`WidthManaged` | Top root of hierarcy
| N/A (fits container) | `40rem` , unless `Wider` or `FullWidth` |
`Wider` | Child of `WidthManaged` that is a bit wider. | `58rem` | N/A |
`FullWidth` | Child of `WidthManaged` that is full width. | `100%` | N/A |
`FullWidth.WidthManaged` | A `FullWidth` can itself be `WidthManaged` , useful in rare situations. | `100%` | `40rem` , unless `Wider` or `FullWidth` |
`Block` | A regular Block whose width is constrained by its parent. Can be `Wider` or `FullWidth` . Can have other properties. | Inherited | N/A |
`Column` | A child of any `Block` with `columns={2 or 3}` . | `1/N%` | N/A |

A `Block`

can have some properties:

`columns={2|3}`

: How many columns a Block should span.`float={"left"|"right"}`

: At larger screen sizes, takes up only a portion of the screen width.

For example, a `WidthManaged`

`div`

definition could look like this:

```
export const WidthManaged = {
div({
className,
children,
...rest
}: React.PropsWithChildren<{ className?: string }>) {
return (
<>
<div
className={`${wmStyles.className} wm ${className}`}
{...rest}
>
<WidthHintContext.Provider
value={{
L: { size: 40, unit: "rem" },
M: { size: 40, unit: "rem" },
S: { size: 40, unit: "rem" },
___shortcutSizes: `(min-width: 40rem) 40rem, 100vw`,
}}
>
{children}
</WidthHintContext.Provider>
</div>
{wmStyles.styles}
</>
);
},
};
```


We might repeat this a few times to express other elements we might want to make
`WidthManaged`

. We can make a factory that makes this easier to generalize:

```
// src/components/width-managed.ts (Partial)
import React, { FC, PropsWithChildren } from "react";
import css from "styled-jsx/css";
import { WidthHintContext, WidthHintProps } from "./width-hint";
function makeRemWidthHint(w: number): WidthHintProps {
const s = { size: w, unit: "rem" } as const;
const sizes = `(min-width: ${w}rem) ${w}rem, 100vw`;
return {
L: s,
M: s,
S: s,
___shortcutSizes: sizes,
};
}
type WProps<P> = PropsWithChildren<P & { className?: string }>;
type Wrapper<P> = FC<WProps<P>>;
type Styler = { className: string; styles: JSX.Element };
function make<P>(
styler: Styler,
name: string,
Inner: Wrapper<P>,
hints: WidthHintProps
): Wrapper<P> {
return function WidthManagedWrapper(props) {
const { className, children, ...rest } = props;
return (
<>
<Inner
className={classNames(
props.className,
name,
styler.className
)}
{...(rest as unknown as P)}
>
<WidthHintContext.Provider value={hints}>
{children}
</WidthHintContext.Provider>
</Inner>
{styler.styles}
</>
);
};
}
```


```
// Example: WidthManaged definition
const WM_DEFAULT_WIDTH_REM = 40;
const WM_DEFAULT_WIDTHS = makeRemWidthHint(WM_DEFAULT_WIDTH_REM);
const wmStyle = css.resolve`
.wm > :global(*:not(.full):not(.wider)) {
max-width: ${2 + WM_DEFAULT_WIDTH_REM}rem;
margin-right: auto;
margin-left: auto;
padding-left: 1rem;
padding-right: 1rem;
}
/* Define more 'width managed' CSS here */
`;
export function WidthManaged<P>(Inner: Wrapper<P>) {
return make(wmStyle, "wm", Inner, WM_DEFAULT_WIDTHS);
}
WidthManaged.div = WidthManaged((p) => <div {...p} />);
WidthManaged.main = WidthManaged((p) => <main {...p} />);
```


```
// Example: FullWidth definition
const FULL_WIDTHS: WidthHintProps = {
L: { size: 100, unit: "vw" },
M: { size: 100, unit: "vw" },
S: { size: 100, unit: "vw" },
___shortcutSizes: "100vw",
};
const fullStyle = css.resolve`
.full {
width: 100%;
margin-top: 1rem;
margin-bottom: 1rem;
clear: both;
}
`;
export function FullWidth<P>(Inner: Wrapper<P>) {
return make(fullStyle, "full", Inner, FULL_WIDTHS);
}
FullWidth.div = FullWidth((p) => <div {...p} />);
FullWidth.article = FullWidth((p) => <article {...p} />);
FullWidth.WidthManaged = {
div: WidthManaged(FullWidth.div),
article: WidthManaged(FullWidth.article),
};
```


The definition of `Wider`

is similar to that of `WidthManaged`

.

Our `WidthManaged`

styled component and its siblings define all the top-level
styles for the blog.

We can now create a `Block`

shortcode that understands columns & widths and
updates `WidthHintContext`

accordingly.

```
// src/components/blocks.tsx : Shortcodes
export function Block(p: BlockProps) {
const RawElement = getRawElement(p);
const classes = classNames(p.float, {
[wmFloat.className]: !!p.float,
[wmColumns.className]: !!p.columns,
["two"]: p.columns === 2,
["three"]: p.columns === 3,
});
return (
<>
<RawElement className={classes}>
<ProvideWidth float={float} columns={columns}>
{children}
</ProvideWidth>
</RawElement>
{float && wmFloat.styles}
{columns && wmColumns.styles}
</>
);
}
export function Column(
p: Pick<BlockProps, "figure" | "aside" | "children">
): React.ReactElement {
const RawElement = getRawElement(p);
return (
<RawElement className={classNames("column", p.className)}>
{children}
</RawElement>
);
}
```


```
// src/components/blocks.tsx : WidthHintContext Helpers
/**
* Adjust WidthHintContext if the container has columns or is
* floating.
*/
function ProvideWidth(
props: Pick<BlockProps, "columns" | "float" | "children">
) {
// By now, the parent `RawElement` already updated the
// WidthHintContext to account for simply block "width".
let current = React.useContext(WidthHintContext);
if (props.float) current = FLOAT_WIDTHS;
if (props.columns)
current = {
S: current.S,
M: scale(current.M, (size) => size / props.columns),
L: scale(current.L, (size) => size / props.columns),
};
return (
<WidthHintContext.Provider value={current}>
{props.children}
</WidthHintContext.Provider>
);
}
function scale(s: Size, scaler: (size: number) => number): Size {
return {
size: scaler(s.size),
unit: s.unit,
};
}
```


```
// src/components/blocks.tsx : Other Helpers
type BlockProps = PropsWithChildren<{
/** If set, represents a FullWidth or Wider block. */
width?: "full" | "wider";
/** If set, represents a floating block. */
float?: "left" | "right";
/** Render this block as an <aside> element. */
aside?: true;
/** Render this block as a <figure> element. */
figure?: true;
/** This Block has {N} child columns. */
columns?: 2 | 3;
}>;
/**
* Returns <div>, <figure>, or <aside> with the appropiate width.
*/
function getRawElement(
p: Pick<BlockProps, "width" | "figure" | "aside">
): Container {
let RawElement: Container =
(p.figure && ((props) => <figure {...props} />)) ||
(p.aside && ((props) => <aside {...props} />)) ||
((props) => <div {...props} />);
if (p.width === "full") RawElement = FullWidth(RawElement);
else if (p.width === "wider") RawElement = Wider(RawElement);
return RawElement;
}
type Container = FC<PropsWithChildren<{ className?: string }>>;
```


I didn’t provide implementations for `wmFloat`

and `wmColumns`

. These are also
Styled JSX elements specified to achieve a certain effect. They are structurally
similar to `wmStyle`

and `fullStyle`

defined above.

Given all this, we now can define intricate nestings of `Block`

s and `Column`

s,
and each will infer the correct width of its children. `MdxImg`

components can
look this width up and restrict the `sizes`

of the image to the correct size.

I include `Block`

and `Column`

as shortcodes for my MDX component. I actively
use these in writing my blog posts, including this one! For example, this
section roughly looks like this:

```
## Heading
Example of a "wider" block:
<Block width="wider">
| Block | Description | Max Width | Direct Child Max Width |
| ----- | ----------- | --------- | ---------------------- |
| ... | ... | ... | ... |
| ... | ... | ... | ... |
</Block>
A full width block with columns:
<Block width="full" columns={2}><Column>
```tsx
// column 1 code block.
```
</Column><Column>
```tsx
// column 2 code block.
```
</Column></Block>
```


### Disable unnecessary prefetching

The `next/link`

component fetches the contents of its target page in two cases:
(a) when the link is simply in the viewport (disabled with `prefetch={false}`

),
or (b) when the link is hovered (always).

I like prefetching content when a link is hovered (Gatsby’s `Link`

does that
too), but the default of fetching all links in the viewport seems too
aggressive. It makes sense for a vital Call to Action button, but not the
default for all content.

I liberally added `prefetch={false}`

attributes in a few places. I closely
looked at my **above-the-fold** links (i.e., links that appear in the initial
viewport of the page as it loads). Most links in the *header* don’t need to be
prefetched. For example, if your site title is linkified (to go “Back to home”),
most users won’t click on that. I ended up disabling prefetching for all links
in my header. Remember: Next.js will still prefetch links on hover, so the user
will still have a pretty good experience.

### Dropping unnecessary props

Another thing I decided to do is make sure that the `.json`

data for each page
does not contain more than we need. For example, a `SerializedPost`

contains
many fields. Some are useful only in the blog post, and others are useful only
in an archive listing, etc.

I used TypeScript’s `Pick<>`

type to drop types and see when nested components
complain. For example:

`BlogPostProps`

looks like this:

```
export const BLOG_POST_FIELDS = [
"tags",
"hero",
"title",
"created",
"lastModified",
"slug",
"next",
"prev",
] as const;
export type BlogPostData = Pick<
SerializablePost,
typeof BLOG_POST_FIELDS[number]
>;
export interface BlogPostProps {
source: MDXRemoteSerializeResult;
details: BlogPostData;
}
```


… while `ArchiveListingProps`

looks like this:

```
export const ARCHIVE_PAGE_ITEM_FIELDS = [
"tags",
"hero",
"title",
"created",
"lang",
"path",
"excerpt",
"slug",
] as const;
export type ArchivePageItem = Pick<
SerializablePostWithExcerpt,
typeof ARCHIVE_PAGE_ITEM_FIELDS[number]
>;
export interface ArchiveListingProps extends Paginated {
items: ArchivePageItem[];
}
```


I then define helper functions like `pickOnly`

which pick only the specified
fields. For instance, I now update my `*_GetProps`

functions to pick only the
relevant fields:

```
// /lib/server/posts/props.ts
export async function BlogPost_GetProps(post: Post) {
- const details = Serialize(post);
+ const details = pickOnly(Serialize(post), BLOG_POST_FIELDS);
const mdxSource = await serialize(post.___fileContent, {
mdxOptions,
});
return {
source: mdxSource,
details,
};
}
```


### Unnecessary optimizations for the fun of it!

When your bundle size is 95kb, it becomes fun to look at your bundle output and
see how to make it shorter. If you find yourself wondering how to get a 95kb
bundle down to 93kb on a **blog**, then you clearly hate yourself (or just have
a very strange sense of what is *fun* in life). In my case, it’s both.

Anyways, none of this is serious advice, but read on if you must!

#### Spread Operators

I was noticing a lot of large-ish blocks of code in my bundled output. Looking more closely, these were object and array spread operators that were transpiled down. I liberally use these spread operators for concatenating arrays and merging objects.

What’s more annoying is that the spread function helpers are defined once per source file, even in merged bundles. That means that I had spread functions defined a dozen or so times in a bundle.

At this point, I have a few options: (a) do something fancy with the bundler so that these helper functions are reused, (b) change my Babel settings to not transpile spread operators down, or (c) remove or replace unnecessary uses of spread operators.

(a) is a non-starter for me because I’m just not that smart. So I first considered (b) before moving on to (c).

As of this post, spread operators are supported in
[94.8% of browsers for Array spreads](https://caniuse.com/mdn-javascript_operators_spread_spread_in_arrays)
and
[93.4% of browsers for Object spreads](https://caniuse.com/mdn-javascript_operators_spread_spread_in_object_literals).
I’m sure the average user of my blog skews more tech-savvy and is more likely to
be running an up-to-date browser. But still, delivering broken JavaScript to
4-6% of my readers sounds horrible. So I opted for (c).

Many array merges were easy, `[a, b, c, ...d]`

is just `[a, b, c].concat(d)`

.
Ideally, Terser would figure that out. But it doesn’t, and I’m on a mission.

Object literal merging was a mixed bag. A few instances were unused. Other instances were merging known objects with a single field. I replaced these with simply passing the one field.

#### Fun with /*#__PURE__*/

I have a few cases where I use `assert`

functions to constrain types and show me
errors during development. I especially use these if a field is null, etc.

I ended up annotating a few places as `/*#__PURE__*/`

, e.g.:

```
const dontCapitalize = /*#__PURE__*/ new Set([
"and",
"or",
"of",
"with",
"a",
"an",
]);
```


In this case, `dontCapitalize`

was used in some function that was not used in
most chunks. The optimizer stripped the functions away, as was the
`const dontCapitalize = `

part of the assignment. But my bundle still ended up
with:

```
new Set(["and", "or", "of", "with", "a", "an"]);
```


… because the optimizer couldn’t figure out if instantiating a `Set`

had any
side effects. I marked the expression as `/*#__PURE__*/`

, and it worked.

## Thinking about Hosting (Vercel vs. Netlify)


Update 2025:These reflections from 2021 are largely obsolete. While some of the licensing concerns I had with Vercel around commercial use still exist, the quality of the Netlify offering for Next.js has greatly improved.Netlify with Next.js now works out-of-the-box with

`next/image`

, for instance. Netlify also no longer requires any installation steps for a Next.js plugin, etc. Further, new Next.js features introduced since this post, like server actions, are automatically ‘compiled’ and converted into Netlify Functions that ‘just work’.After Vercel CEO Guillermo Rauch’s recent

[public posts feature Benjamin Netanyahu], I was encouraged to see if Netlify’s developer experience had improved. I found that it had, and I have since moved all my projects back to Netlify.

The original 2021 text follows:

I was very happy using Netlify as my host. The experience hosting the Gatsby blog there was great. My

[personal website], written in Next.js, was also hosted on Netlify.I had a few concerns with hosting a Next.js site on Netlify, and I was curious what Vercel could offer.

My main concern was seeing if Vercel handled

`next/image`

better than Netlify. Unlike Gatsby, which optimizes these images during build time, Next.js uses an image optimizer (by default at`/_next/image?url=...&w=32&q=32`

) that returns an optimized image.Netlify does this using Netlify Functions, which optimize an image the first time it’s requested and caching it for subsequent requests. This produces a pretty lackluster experience the first time an image is loaded. I wasn’t sure how serious this is: since the images do get cached

eventually. But I was curious enough to see if the experience felt different at Vercel.My initial thought was to try both Vercel and Netlify and see which one does better.

[Raw data]shows that Netlify tends to have better[5]fundamentals, but I was hoping to see if Vercel offers anything better.

### Getting Netlify Next.js Builds Working…

**Obsolete as of 2025**:

I had gotten my Next.js personal website working on Netlify using Netlify’s

[Essential Next.js Build Plugin], but I ran into trouble getting the same working for my much larger blog codebase.First, I ran into a build failure:

`Failed to compile. ModuleNotFoundError: Module not found: Error: Can't resolve 'canvas' in '/opt/build/repo/node_modules/jsdom/lib/jsdom' > Build error occurred Error: > Build failed because of webpack errors at /opt/build/repo/node_modules/next/dist/build/index.js:390:19 at async Span.traceAsyncFn (/opt/build/repo/node_modules/next/dist/telemetry/trace/trace.js:60:20)`

This appears to be

[related]to my use of PrismJS. When I attempted to add`'canvas'`

as a webpack external, I got a similar error complaining about`'critters'`

, etc. When I added all of the modules it complained about, the build proceeded, but function bundling failed:`Error message A Netlify Function failed to require one of its dependencies. Please make sure it is present in the site's top-level "package.json". In file "/opt/build/repo/netlify/functions/next_chunks/next_chunks.js" Cannot find module 'canvas'`

At this point, I decided getting Netlify to work might not be worthwhile. I decided to look into Vercel more seriously.


### Vercel’s Free Tier vs Netlify’s Free Tier

There are two key differences between Vercel and Netlify’s free tiers, largely in their terms:

#### Non-commercial use is disallowed in Vercel

Vercel’s Fair Use policy says that you cannot use the free tier for commercial purposes. My blog is not a commercial endeavor by any means, but I do try to monetize a few aspects of it to break even.

So I asked Vercel:

What about a blog that uses Google Ads, but is not set up for the purpose of advertising a product?

Having ads in your deployments counts as commercial use.

What about a blog that contains affiliate links, but at a low frequency?

As long as it is not the primary purpose of the site then it’s fine.


In other words, ad-supported content is not okay in Vercel. Affiliate links are fine, but primarily affiliate-driven sites are not. Got it. Netlify, on the other hand, has no such restrictions.

#### Bandwidth limits

Vercel’s fair use policy also states that websites should stick to 100 GB / month in bandwidth. This is the same as Netlify’s free limit.

The main difference is that Vercel has no way of letting you buy additional bandwidth. In contrast, Netlify allows free tier users to purchase extra bandwidth if they need it.

My website runs on the free bandwidth most months, but if it reaches the top of HackerNews (which it does once every few months), I will usually need extra.

So I asked Vercel’s sales team:

Hobby accounts have a 100 GB maximum limit for bandwidth. This is more than enough most months, but once in a while my site requires more bandwidth than that. What is the expectation for bursty usage? Can a Hobby account pay for extra bandwidth for some months?

You will receive a notification email to warn you against additional usage. Currently, your deployments will not be blocked until they exceed 300% of the allocated resource (this might change in the future without notice).

More so, is there auto billing where I can add bandwidth to my Hobby account if I’m about to go over the limit?

You cannot pay for extra resources in hobby account. You will need to upgrade to our paid plans for it.


This is a mixed bag. The policy allows up to 300 GB / month for bursty usage, which is more than enough for me. But this might change at any time.

If that policy ever changes, I’ll be locked in a place where I can *only* pay a
monthly fee.

I decided the risk is worthwhile for me: It’s easy to switch between Vercel and Netlify (as long as I get Next.js building again in Netlify), so the downside of Vercel changing their bandwidth policy at a later time isn’t as pressing.

### Decisions

**As of 2025**, I am back to using Netlify overall.

From 2021:

I decided to go with Vercel: It provided a gorgeous developer experience, its Next.js builds were substantially faster, the performance is quite good,

andthe free tier had acceptable terms to me.Choosing Vercel meant I had to adjust my blog to comply with their fair use policy. I dropped ads (which I was already mulling) and removed all Google AdSense code from my site. Their support desk’s response reassured me that I could keep using affiliate links.

If Vercel’s fair use policy disallowed

anymonetization, I would have likely stuck with Netlify. My blog doesn’t earn my 20/month bill for a blog with a few affiliate links and some ads was just not worth it.

## Next.js vs. Gatsby: Comparing the Results

I decided to do a simple series of tests between Gatsby and Next.js. These are not at all rigorous; a lot of the timings vary a lot between runs.

I disabled Google Analytics for both sites and hard-refreshed each page a few times. I used my Network tab in Developer Tools to measure the # of Requests, Bytes Transferred, Resources (Bytes), and Time for each page, and a few other scenarios.

My main attempt here is to get a rough sense of whether Next.js is leaving me better off or worse off.

Also, note that this is not an apples-to-apples comparison. Before I did any optimizations to Next.js, Gatsby was a lot faster. My Gatsby setup wasn’t particularly optimized beyond what Gatsby gave me out of the box.

I still think this is a *fair* comparison, even though it’s not
apples-to-apples. After all, I didn’t optimize Gatsby precisely because I found
it hard to play around with its internals well enough to optimize things.
Next.js, on the other hand, was a double-edged sword: to make sure my Markdown
images used `next/image`

manually. Yes, I had to do all sorts of fun magic to
infer the right sizes. But at least I *could*. With Next.js, it felt easier to
open the truck and just move things around to my liking. This made it easier to
optimize.

### Home Page

| # Requests | Transferred | Resources | Time | |
|---|---|---|---|---|
| Gatsby | 115 | 1.8 MB | 2.6 MB | 302ms |
| Next.js | 47 | 820 kB | 1.3 MB | 274ms |

| # Requests | Transferred | Resources | |
|---|---|---|---|
| Gatsby | 134 | 1.8 MB | 2.8 MB |
| Next.js | 60 | 1.1 MB | 1.8 MB |

Total Home Page resources after scrolling through on desktop.

| # Requests | Transferred | Resources | Time | |
|---|---|---|---|---|
| Gatsby | 98 | 1.1 MB | 1.8 MB | 302ms |
| Next.js | 37 | 533 kB | 1.1 MB | 169ms |

| # Requests | Transferred | Resources | |
|---|---|---|---|
| Gatsby | 132 | 1.1 MB | 2.1 MB |
| Next.js | 56 | 604 kB | 1.6 MB |

Total Home Page resources after scrolling through on iPhone X.

### Blog Post

| # Requests | Transferred | Resources | Time | |
|---|---|---|---|---|
| Gatsby | 80 | 745 kB | 1.3 MB | 240ms |
| Next.js | 42 | 427 kB | 739 kB | 196ms |

| # Requests | Transferred | Resources | |
|---|---|---|---|
| Gatsby | 94 | 1.3 MB | 1.9 MB |
| Next.js | 54 | 702 kB | 1.1 MB |

Total rich post resources after scrolling through on desktop.

| # Requests | Transferred | Resources | Time | |
|---|---|---|---|---|
| Gatsby | 80 | 670 kB | 1.2 MB | 247ms |
| Next.js | 42 | 407 kB | 719 kB | 193ms |

| # Requests | Transferred | Resources | |
|---|---|---|---|
| Gatsby | 94 | 999 kB | 1.6 MB |
| Next.js | 54 | 431 kB | 1.2 MB |

Total rich post resources after scrolling through on iPhone X.

### Home to Blog Post Navigation

| # Requests | Transferred | Resources | |
|---|---|---|---|
| Gatsby | 25 | 2.9 kB | 316 kB |
| Next.js | 16 | 67.7 kB | 104 kB |

Requests on navigation from home page to a post on desktop.

| # Requests | Transferred | Resources | |
|---|---|---|---|
| Gatsby | 27 | 19.9 kB | 256 kB |
| Next.js | 17 | 67.8 kB | 116 kB |

Requests on navigation from home page to a post on mobile.

## Conclusion

For me, moving to Next.js was definitely a worthwhile investment. I’m happy with how faster and snappier my Next.js blog feels.

I enjoy the extra control I have over my blog. The journey of *getting* that
control (and replacing out-of-the-box Gatsby magic) was tough— but probably
worth it.

Moving to Next.js did force me to consider Vercel over Netlify, however. If
Netlify had just a *bit* less friction with Next.js, I probably would have stuck
with it. But I fundamentally have few complaints about Vercel, other than the
extra burden of adhering to their fair use policy.

## Footnotes

-
I still maintain my old domain name (eyas-sharaiha.com) and set up permanent redirects to keep any old links working.

[↩](https://blog.eyas.sh#user-content-fnref-1) -
SmartyPants is

[originally by John Gruber](https://daringfireball.net/projects/smartypants/).[↩](https://blog.eyas.sh#user-content-fnref-2) -
I had to remove these eventually since my chosen approach (

`next-mdx-remote`

) didn’t support them. But I decided to strip these in regex too.[↩](https://blog.eyas.sh#user-content-fnref-3) -
or a

`FullWidth`

element; see the following lines in the table.[↩](https://blog.eyas.sh#user-content-fnref-4) -
TTFB & Total Time, as fetched on 2021-08-18.

[↩](https://blog.eyas.sh#user-content-fnref-5)