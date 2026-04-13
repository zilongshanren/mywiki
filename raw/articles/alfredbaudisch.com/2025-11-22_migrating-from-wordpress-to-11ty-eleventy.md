---
title: Migrating from WordPress to 11ty (Eleventy)
url: https://alfredbaudisch.com/blog/migrating-from-wordpress-to-11ty/
author: Alfred Reinold Baudisch
published: '2025-11-22'
source_blog: Alfred Reinold Baudisch
source_site: https://alfredbaudisch.com
category: game programming
fetched: '2026-04-13'
---

This site was migrated from WordPress to 11ty (Eleventy). Here's how I did it, including how to import and convert WordPress content that relies heavily on custom post types, custom taxonomies and custom meta fields.

## Why 11ty?

My WordPress site had:

- Regular blog posts
- Custom post types:
[Projects](https://alfredbaudisch.com/projects)and[Experiments](https://alfredbaudisch.com/experiments)- Projects and Experiments child content: Project Logs and Experiment Logs. For example, a "Project" could have multiple "Project Logs" which appeared under the Project.

- Custom taxonomies: Project Styles, Project Status, Tools, Project Types, Log Categories, Experiment Types
- Lots of images with lightboxes
- Code syntax highlighting
- A lot of custom WordPress "meta" fields and boxes

I wanted something simpler:

- Markdown files.
- Git-based deployment.
- No databases.

After some research I decided to go with [11ty](https://www.11ty.dev/) (which I've never heard of before).

## Open-source

This website and its content are [open-source](https://github.com/alfredbaudisch/alfredbaudisch.com).

## New Layout/Design

The first thing I did was creating a new design. I never liked using the WordPress' default theme, but I kept using it for almost 6 years, since I have customized it so much in every possible aspect.

The new design is inspired by "[THE OLDSCHOOL PC FONT RESOURCE](https://int10h.org/oldschool-pc-fonts/)" which has a DOS-like feel to it, and it uses the ["IBM VGA 9x16](https://int10h.org/oldschool-pc-fonts/fontlist/font?ibm_vga_9x16)" as the main font.

To be honest there's still A LOT of room for improvement before I get the old IBM/DOS like and feel. But at least this is a start already.

## Custom Post Types and Taxonomies in 11ty

### The Structure

In WordPress, I had custom post types. In 11ty, I use the file system:

```
content/
├── posts/ # Regular blog posts
├── projects/ # Projects
│ └── project-slug/
│ ├── index.md # Project main page
│ └── logs/ # Project logs
│ └── 2021-03-15-log-title.md
├── experiments/ # Experiments
│ └── experiment-slug/
│ ├── index.md
│ └── logs/
└── pages/ # Static pages
```


### Custom Post Types as Collections

11ty uses collections to group content. They are defined in `.eleventy.js`

:

```
eleventyConfig.addCollection("projects", function(collectionApi) {
return collectionApi.getFilteredByGlob("content/projects/**/index.md")
.filter(item => !item.data.draft)
.sort((a, b) => dateB - dateA);
});
eleventyConfig.addCollection("projectLogs", function(collectionApi) {
return collectionApi.getFilteredByGlob("content/projects/**/logs/*.md")
.filter(item => !item.data.draft)
.sort((a, b) => dateB - dateA);
});
```


Same pattern for experiments and experiment logs.

### Taxonomies as Frontmatter

WordPress taxonomies became frontmatter fields:

```
---
title: "My Project"
type: "project"
projectTypes: ["Game Development"]
projectStyles: ["Retro", "Pixel Art"]
projectStatus: "Active"
tools: ["Godot", "Blender"]
---
```


Filters to query by taxonomy:

```
eleventyConfig.addFilter("filterByTaxonomy", function(collection, taxonomyName, value) {
return collection.filter(item => {
const taxonomy = item.data[taxonomyName];
if (Array.isArray(taxonomy)) {
return taxonomy.some(v => String(v).toLowerCase() === String(value).toLowerCase());
}
return String(taxonomy).toLowerCase() === String(value).toLowerCase();
});
});
```


### Dynamic Taxonomy Archives

Taxonomy archive pages are generated automatically:

```
eleventyConfig.addCollection("taxonomyArchives", function(collectionApi) {
const allContent = collectionApi.getAll();
const taxonomies = {
projectTypes: new Set(),
projectStyles: new Set(),
// ... etc
};
// Extract all taxonomy values from content
allContent.forEach(item => {
if (item.data.projectTypes) {
const values = Array.isArray(item.data.projectTypes)
? item.data.projectTypes
: [item.data.projectTypes];
values.forEach(v => taxonomies.projectTypes.add(v));
}
});
// Generate archive entries
const archives = [];
Object.keys(taxonomies).forEach(taxonomyName => {
taxonomies[taxonomyName].forEach(value => {
archives.push({
taxonomy: taxonomyName,
category: value,
url: `/${taxonomyUrlMap[taxonomyName]}/${slug(value)}/`
});
});
});
return archives;
});
```


## Sitemap and RSS

The same [sitemap](https://alfredbaudisch.com/sitemap) structure that I had in WordPress was created with a Nunjuck template in 11ty. For example, here's a snippet from it:

```
<section class="sitemap-section">
<h2>Posts by Category</h2>
{% set postsByCategory = collections.posts | groupBy("categories") %}
{% for category in postsByCategory | keys | sort %}
<h3>{{ category }}</h3>
<ul class="sitemap-list">
{% for post in postsByCategory[category] | sort(false, false, "data.date") %}
<li>
<a href="{{ post.url }}">{{ post.data.title }}</a>
<time datetime="{{ post.data.date | dateISO }}"> ({{ post.data.date | dateDisplay("yyyy-MM-dd") }})</time>
</li>
{% endfor %}
</ul>
{% endfor %}
</section>
```


- There's also a
[sitemap.xml](https://alfredbaudisch.com/sitemap.xml)generator - And a
[RSS feed](https://alfredbaudisch.com/feed.xml)generator

## WordPress Import Scripts

I created Node.js scripts to convert WordPress exports to markdown. This took way more time than I anticipated, because of the amount of custom info and relationships from my WordPress theme and data.

### The Process

- Download WordPress data (I'm used the REST API, i.e.
`domain/wp-json/[post-type]`

) - Process each content type
- Convert and map all media files and all metadata
- Convert HTML to Markdown

### Processing Projects

The script reads WordPress JSON exports and converts them:

```
// scripts/migrate/process-projects.js
const projects = readJSON('data/projects.json');
const projectLogs = readJSON('data/project-logs.json');
const taxonomies = readJSON('data/taxonomies.json');
projects.forEach(project => {
// Extract taxonomies
const projectTypes = getTaxonomyTerms(project, 'project_type', taxonomyLookup);
const projectStyles = getTaxonomyTerms(project, 'project_style', taxonomyLookup);
// Convert HTML content to Markdown
const markdown = htmlToMarkdown(project.content.rendered);
// Get featured image
const featuredImage = getMediaFullUrl(project.featured_media, mediaLookup);
// Create frontmatter
const frontmatter = {
title: project.title.rendered,
date: formatDate(project.date),
type: "project",
projectTypes: projectTypes,
projectStyles: projectStyles,
featuredImage: convertWordPressUrlToLocalPath(featuredImage)
};
// Write markdown file
writeFile(outputPath, frontmatter, markdown);
});
```


### Handling Project Logs

Project logs needed to link to their parent project:

```
// Map logs to projects
const logsByProject = {};
projectLogs.forEach(log => {
const parentProjectId = log.meta.project_log_parent_project;
if (parentProjectId) {
if (!logsByProject[parentProjectId]) {
logsByProject[parentProjectId] = [];
}
logsByProject[parentProjectId].push(log);
}
});
// When processing a project, also process its logs
projects.forEach(project => {
const projectSlug = generateSlug(project.title.rendered);
const logs = logsByProject[project.id] || [];
logs.forEach(log => {
const logPath = path.join(projectDir, 'logs', `${formatDateForFilename(log.date)}-${generateSlug(log.title.rendered)}.md`);
// Process and write log file
});
});
```


### HTML to Markdown Conversion

WordPress content is HTML. I used `turndown`

with custom rules and the `imageGallery`

callback:

```
const turndown = new TurndownService({
headingStyle: 'atx',
codeBlockStyle: 'fenced'
});
// Custom rule for WordPress galleries
turndown.addRule('wpGallery', {
filter: function(node) {
return node.nodeName === 'UL' && node.classList.contains('wp-block-gallery');
},
replacement: function(content, node) {
const images = Array.from(node.querySelectorAll('img'));
const imageArray = images.map(img => ({
src: img.src,
alt: img.alt || ''
}));
return `{` + `% imageGallery ${JSON.stringify(imageArray)} %` + `}`;
}
});
```


### Media Migration

Media was downloaded from `/wp-upload/uploads`

and moved to `/media/wp-content/`

. Old links are preserved via a rule in the nginx file to permanently redirect them to the new permalink format.

Then updated all image references in markdown from WordPress URLs to local paths:

```
function convertWordPressUrlToLocalPath(url) {
if (!url) return url;
return url.replace(
/https?:\/\/alfredbaudisch\.com\/wp-content\/uploads\//g,
'/media/wp-content/'
);
}
```


### Meta Fields

WordPress custom fields became frontmatter:

```
const meta = project.meta || {};
const processImage = getProcessImageUrl(meta.process_image, mediaLookup);
const links = getLinksFromMeta(meta);
const frontmatter = {
// ... other fields
processImage: convertWordPressUrlToLocalPath(processImage),
links: links
};
```


For example, this is the frontmatter for one of [my old experiment](https://alfredbaudisch.com/experiments/3d-art/154-blender-geometry-nodes/) posts. You can see how taxonomies and meta fields are used (including `processImage`

and `links`

, these were all automatically converted from the WordPress post):

```
---
layout: "layouts/experiment.njk"
title: "154: Re-learning Blender 3.0 Geometry Nodes"
date: "2022-01-13T23:44:08.000Z"
updated: "2022-01-14T00:00:00.000Z"
type: "experiment"
tags: ["geometry nodes"]
experimentTypes: ["3D Art"]
tools: ["Blender"]
featuredImage: "/media/wp-content/2022/01/154-blender-geometry-nodes-learning12.gif"
featuredImageThumb: "/media/wp-content/2022/01/154-blender-geometry-nodes-learning12-768x421.gif"
featuredImageSmall: "/media/wp-content/2022/01/154-blender-geometry-nodes-learning12-300x165.gif"
processImage: "/media/wp-content/2022/01/155-process-blender1.jpg"
projectStyles: ["Procedural"]
links:
- name: "Easy Geometry Nodes PLANTS - Blender 3.0"
url: "https://www.youtube.com/watch?v=VTkUVtWbjoE"
- name: "Blender 3.0 New Geometry Nodes Tutorial"
url: "https://www.youtube.com/watch?v=UqRVxosrnGc"
- name: "Geometry Nodes Blender 3.0 Tutorial - Make A Trash Dump Fast"
url: "https://www.youtube.com/watch?v=M14iZxkUUAQ"
- name: "What are Fields? - Geometry Nodes 101"
url: "https://www.youtube.com/watch?v=8FCHcbpnFss"
- name: "Create and Animate a Procedural Castle in Blender"
url: "https://skl.sh/3Fqlcqw"
---
```


## Deployment

### Build Process

The build script:

- Bundles JavaScript (esbuild)
- Copies CSS
- Runs 11ty to generate static site

```
# package.json
"build": "rm -rf _site && NODE_ENV=production npm run build:js && NODE_ENV=production npm run build:css && NODE_ENV=production eleventy"
```


### Deployment Script

Two deployment methods:

#### Local deployment

`scripts/deploy/deploy.sh`

- Builds the site
- Uses rsync to sync
`_site/`

to VPS (since 2020 I use a $5 DigitalOcean VPS) - Easy deployment by calling
`npm run deploy`

locally

rsync:

```
rsync -avz --delete \
-e "ssh -i $SSH_KEY" \
"$BUILD_DIR/" "$VPS_USER@$VPS_HOST:$DEPLOY_DIR/_site/"
```


These are the `package.json`

scripts:

```
"scripts": {
"build": "rm -rf _site && NODE_ENV=production npm run build:js && NODE_ENV=production npm run build:css && NODE_ENV=production eleventy",
"build:js": "node scripts/build-js.js --production",
"build:js:dev": "node scripts/build-js.js",
"build:css": "node scripts/build-css.js --production",
"build:css:dev": "node scripts/build-css.js",
"serve": "eleventy --serve",
"dev": "rm -rf _site && NODE_ENV=development npm run build:js:dev && NODE_ENV=development npm run build:css:dev && NODE_ENV=development eleventy --serve --watch",
"deploy": "bash scripts/deploy/deploy.sh"
}
```


#### GitHub Actions

`.github/workflows/deploy.yml`


```
name: Deploy to VPS
on:
push:
branches: [ master ]
jobs:
deploy:
runs-on: ubuntu-latest
steps:
- name: Checkout code
uses: actions/checkout@v3
- name: Setup Node.js
uses: actions/setup-node@v3
with:
node-version: '18'
cache: 'npm'
- name: Install dependencies
run: npm ci
- name: Build site
run: npm run build
- name: Sync files to VPS using rsync
run: |
rsync -avz --delete --no-owner --no-group \
-e "ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i $" \
_site/ $@$:/var/www/alfredbaudisch.com/_site/
```