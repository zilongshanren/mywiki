---
title: MDN localization update, February 2021 – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2021/02/mdn-localization-update-february-2021/
author: Chris Mills
published: '2021-02-11'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

In our previous post, [An update on MDN Web Docs’ localization strategy](https://hacks.mozilla.org/2020/12/an-update-on-mdn-web-docs-localization-strategy/), we explained our broad strategy for moving forward with allowing translation edits on MDN again. The MDN localization communities are waiting for news of our progress on unfreezing the top-tier locales, and here we are. In this post we’ll look at where we’ve got to so far in 2021, and what you can expect moving forward.

## Normalizing slugs between locales

Previously on MDN, we allowed translators to localize document URL slugs as well as the document title and body content. This sounds good in principle, but has created a bunch of problems. It has resulted in situations where it is very difficult to keep document structures consistent.

If you want to change the structure or location of a set of documentation, it can be nearly impossible to verify that you’ve moved all of the localized versions along with the `en-US`

versions — some of them will be under differently-named slugs both in the original and new locations, meaning that you’d have to spend time tracking them down, and time creating new parent pages with the correct slugs, etc.

As a knock-on effect, this has also resulted in a number of localized pages being orphaned (not being attached to any parent `en-US`

pages), and a number of `en-US`

pages being translated more than once (e.g. localized once under the existing `en-US`

slug, and then again under a localized slug).

For example, the following table shows the top-level directories in the `en-US`

locale as of Feb 1, 2021, compared to that of the `fr`

locale.

`en-US` |
`fr` |
| games glossary learn mdn mozilla plugins related tools web webassembly |
accessibilité adaptation_des_applications_xul_pour_firefox_1.5 améliorations_dom_dans_firefox_3 améliorations_svg_dans_firefox_3 améliorations_xul_dans_firefox_3 apprendre astuces_css bugs_importants_corrigés_dans_firefox_3 changements_dans_gecko_1.9_affectant_les_sites_web chrome comment_créer_un_arbre_dom compilation_et_installation contrôles_dhtml_personnalisés_navigables_au_clavier css dhtml dom développement_web explorer_un_tableau_html_avec_des_interfaces_dom_et_javascript faq_sur_les_transformations_xsl_dans_mozilla fuel games glossaire glossary html inset-block-end inset-block-start inset-inline-end inset-inline-start inspecteur_dom introduction_(alternative) introduction_à_la_cryptographie_à_clef_publique javascript jeux la_sécurité_dans_firefox_2 learn localization mdn mdn_a_dix_ans mise_à_jour_des_applications_web_pour_firefox_3 mise_à_jour_des_extensions_pour_firefox_2 mise_à_jour_des_extensions_pour_firefox_3 mozilla navigatorusermedia.getusermedia npapi outils référence_dom_gecko sgml svg_dans_firefox tosource tostring type_mime_incorrect_pour_les_fichiers_css un_raycaster_basique_avec_canvas utilisation_de_xpath utilisation_du_cache_de_firefox_1.5 web webapi webassembly webrtc xhtml xmlserializer xpcom xslt_dans_gecko xsltprocessor zoom_pleine_page à_propos_du_document_object_model |

To make the non-`en-US`

locales consistent and manageable, we are going to move to having `en-US`

slugs only — all localized pages will be moved under their equivalent location in the `en-US`

tree. In cases where that location cannot be reliably determined — e.g. where the documents are orphans or duplicates — we will put those documents into a specific storage directory, give them an appropriate prefix, and ask the maintenance communities for each unfrozen locale to sort out what to do with them.

- Every localized document will be kept in a separate repo to the
`en-US`

content, but will have a corresponding`en-US`

document with the same slug (folder path). - At first this will be enforced during deployment — we will move all the localized documents so that their locations are synchronized with their
`en-US`

equivalents. Every document that does not have a corresponding`en-US`

document will be prefixed with`orphaned`

during deployment. We plan to further automate this to check whenever a PR is created against the repo. We will also funnel back changes from the main`en-US`

content repo, i.e. if an`en-US`

page is moved, the localized equivalents will be automatically moved too. - All locales will be migrated, unfortunately, some documents will be marked as orphaned and some others will be marked as conflicting (as in adding a prefix
`conflicting`

to their slug). Conflicting documents have a corresponding`en-US`

document with multiple translations in the same locale. - We plan to delete, archive, or move out orphaned/conflicting content.
- Nothing will be lost since everything is in a git repo (even if something is deleted, it can still be recovered from the git history).

## Processes for identifying unmaintained content

The other problem we have been wrestling with is how to identify what localized content is worth keeping, and what isn’t. Since many locales have been largely unmaintained for a long time, they contain a lot of content that is very out-of-date and getting further out-of-date as time goes on. Many of these documents are either not relevant any more at all, incomplete, or simply too much work to bring up to date (it would be better to just start from nothing).

It would be better for everyone involved to just delete this unmaintained content, so we can concentrate on higher-value content.

The criteria we have identified so far to indicate unmaintained content is as follows:

- Pages that should have compat tables, which are missing them.
- Pages that should have interactive examples and/or embedded examples, which are missing them.
- Pages that should have a sidebar, but don’t.
- Pages where the KumaScript is breaking so much that it’s not really renderable in a usable way.

These criteria are largely measurable; we ran some scripts on the translated pages to calculate which ones could be marked as unmaintained (they match one or more of the above). The results are as follows:

If you look for compat, interactive examples, live samples, orphans, and all sidebars:

- Unmaintained: 30.3%
- Disconnected (orphaned): 3.1%

If you look for compat, interactive examples, live samples, orphans, but not sidebars:

- Unmaintained: 27.5%
- Disconnected (orphaned): 3.1%

This would allow us to get rid of a large number of low-quality pages, and make dealing with localizations easier.

We [created a spreadsheet](https://docs.google.com/spreadsheets/d/1eiChEphhuaGik-MWkUrRgR7xWQR8cSfdfR10nybsGno/edit?ts=601c79ee#gid=949029218) that lists all the pages that would be put in the unmaintained category under the above rules, in case you were interested in checking them out.

## Stopping the display of non-tier 1 locales

After we have unfrozen the “tier 1” locales (`fr`

, `ja`

, `zh-CN`

, `zh-TW`

), we are planning to stop displaying other locales. If no-one has the time to maintain a locale, and it is getting more out-of-date all the time, it is better to just not show it rather than have potentially harmful unmaintained content available to mislead people.

This makes sense considering how the system currently works. If someone has their browser language set to say `fr`

, we will automatically serve them the `fr`

version of a page, if it exists, rather than the `en-US`

version — even if the `fr`

version is old and really out-of-date, and the `en-US`

version is high-quality and up-to-date.

Going forward, we will show `en-US`

and the tier 1 locales that have active maintenance communities, but we will not display the other locales. To get a locale displayed again, we require an active community to step up and agree to have responsibility for maintaining that locale (which means reviewing pull requests, fixing issues filed against that locale, and doing a reasonable job of keeping the content up to date as new content is added to the `en-US`

docs).

If you are interested in maintaining an unmaintained locale, we are more than happy to talk to you. We just need a plan. Please get in touch!

Note: Not showing the non-tier 1 locales doesn’t mean that we will delete all the content. We are intending to keep it available in our [archived-content](https://github.com/mdn/archived-content/) repo in case anyone needs to access it.

## Next steps

The immediate next step is to get the tier 1 locales unfrozen, so we can start to get those communities active again and make that content better. We are hoping to get this done by the start of March. The normalizing slugs work will happen as part of this.

After that we will start to look at stopping the display of non-tier 1 localized content — that will follow soon after.

Identifying and removing unmaintained content will be a longer game to play — we want to involve our active localization communities in this work for the tier 1 locales, so this will be done after the other two items.

## About Chris Mills

Chris Mills is a senior tech writer at Mozilla, where he writes docs and demos about open web apps, HTML/CSS/JavaScript, A11y, WebAssembly, and more. He loves tinkering around with web technologies, and gives occasional tech talks at conferences and universities. He used to work for Opera and W3C, and enjoys playing heavy metal drums and drinking good beer. He lives near Manchester, UK, with his good lady and three beautiful children.