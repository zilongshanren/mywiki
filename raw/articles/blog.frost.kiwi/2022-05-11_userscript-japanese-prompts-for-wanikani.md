---
title: Userscript - Japanese prompts for WaniKani
url: https://blog.frost.kiwi/wanikani-userscript/
published: '2022-05-11'
source_blog: FrostKiwi's Secrets
source_site: https://blog.frost.kiwi
category: graphics
fetched: '2026-04-13'
---

[WaniKani](https://www.wanikani.com/) is a Japanese [Kanji](https://en.wikipedia.org/wiki/Kanji) study service, with strong community support [extending the service creating all kinds of features](https://community.wanikani.com/t/the-new-and-improved-list-of-api-and-third-party-apps/7694?u=frostkiwi). One of my favorites being a [connection to a huge Anime sentences database](https://community.wanikani.com/t/userscript-anime-context-sentences/54003?u=frostkiwi), which allows to hear the vocabulary you learn in a short snippet from Ghibli movies, among others.

![](../../assets/14f8ac0d7f641b8c.jpeg)


The Question prompts of WaniKani are in English though, which I always found kind of ironic. A Userscript was created to fix this, which Greasyfork user [hoovard](https://greasyfork.org/en/users/9284-hoovard) updated to become [“WK Custom Review Question (KunOn+)”](https://greasyfork.org/en/scripts/8193-wk-custom-review-question-kunon). However, the script didn’t properly function, which [I fixed](https://community.wanikani.com/t/the-new-and-improved-list-of-api-and-third-party-apps/7694/568) by modifying the script. The script was broken again by a big WaniKani update. Now I have rewritten the script from scratch to work with the current (see post modification date) version of WaniKani.

This script now properly replaces the prompts to be Japanese and specifies whether or not it’s supposed to be [OnYomi](https://en.wikipedia.org/wiki/Kanji#On'yomi_(Sino-Japanese_reading)) or [KunYomi](https://en.wikipedia.org/wiki/Kanji#Kun'yomi_(native_reading)). Get it [on Greasyfork](https://greasyfork.org/en/scripts/444836-wanikani-japanese-review-questions) or directly [from the repo of this blog](https://github.com/FrostKiwi/treasurechest/raw/main/posts/wanikani-userscript/WaniKani%20Japanese%20Review%20Questions.user.js). The detection of OnYomi vs KunYomi is provided by [HaraldN](https://greasyfork.org/en/users/856931-haraldn) in his Userscript [WaniKani Katakana For On’yomi](https://greasyfork.org/en/scripts/437497-wanikani-katakana-for-on-yomi).

## Source code of the [Userscript](https://blog.frost.kiwi/WaniKani Japanese Review Questions.user.js)

```
// ==UserScript==
// @name WaniKani Japanese Review Questions
// @namespace WK_CustomQuestion
// @description Changes the text of the Review or Lesson Quiz question. Original created by hoovard, with extra thanks going to previous authors Rui Pinheiro (LordGravewish) and Ethan. Rewritten by FrostKiwi for the new WaniKani version with OnYomi vs KunYomi detection provided by HaraldN
// @author FrostKiwi
// @match *://www.wanikani.com/subjects/review*
// @match *://www.wanikani.com/recent-mistakes*
// @match *://www.wanikani.com/subject-lessons*
// @match *://www.wanikani.com/subjects/extra_study*
// @version 0.5.1
// @license Do what you want with it (Preferably improve it).
// @grant none
// ==/UserScript==
// Version 0.5.0 applies to Reviews, Lesson Quizzes and extra studies
(function () {
const translations = {
'vocabulary': '単語の',
'radical': '部首の',
'kanji': '漢字の',
'reading': '読み',
'onyomi': '音読み',
'kunyomi': '訓読み',
'meaning': '意味',
'name': '名'
};
let reading_type = null;
let container = null;
let categorySpan = null;
let typeSpan = null;
/* Predefine the observers to ensure we don't accidentally create more than
two in some unknown edge case */
const observerType = new MutationObserver(() => replaceText(typeSpan));
const observerCategory = new MutationObserver(() => replaceText(categorySpan));
function initElements() {
container = document.querySelector('.quiz-input__question-type-container');
categorySpan = document.querySelector('.quiz-input__question-category');
typeSpan = document.querySelector('.quiz-input__question-type');
observerType.observe(categorySpan, { childList: true });
observerCategory.observe(typeSpan, { childList: true });
}
function replaceText(element) {
const text = element.innerText.toLowerCase();
if (translations[text]) {
element.innerText = translations[text];
if (reading_type && text == 'reading') {
element.innerText = translations[reading_type];
}
}
}
function clearWhitespace() {
Array.from(container.childNodes).forEach(node => {
if (node.nodeType === Node.TEXT_NODE && !node.textContent.trim()) {
container.removeChild(node);
}
});
}
/* The detection of OnYomi vs KunYomi is provided by HaraldN in his
Userscript "WaniKani Katakana For On’yomi" */
const newQuestion = function (e) {
if (e.detail.subject.type == 'Kanji' && e.detail.questionType == "reading") {
reading_type = e.detail.subject.primary_reading_type;
} else {
reading_type = null;
}
if (!container || !categorySpan || !typeSpan) {
initElements();
}
clearWhitespace();
}
window.addEventListener('willShowNextQuestion', newQuestion);
})();
```


| Original | Modified |
|---|---|
![]() | ![]() |