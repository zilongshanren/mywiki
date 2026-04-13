---
title: From game jam to mobile and Firefox OS – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2015/12/from-game-jam-to-mobile-and-firefox-os/
author: Belén Albeza
published: '2015-12-04'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

I love participating in [game jams](https://en.wikipedia.org/wiki/Game_jam), where game developers get together to craft games in a very short amount of time. I thought it would be cool to take one of my past Game Jam games, [Metal vs Hipsters](http://lab.belenalbeza.com/games/ldjam-32/), and **port it to the mobile web and Firefox OS**.

## Adapting to mobile

My **starting point** was an HTML5 game built for **desktop**. It had a fixed resolution, was controlled by the keyboard, etc. Some minor (and major!) tweaks would be required to make it a mobile game.

The game uses the open source game engine [Phaser](http://www.phaser.io), so some of the code shown here will make use of Phaser’s API.

You can check out and play the final mobile version [here](http://belen-albeza.github.io/ldjam-32-fxos/).


### Visualising the game

The first tool I used was Firefox’s **Responsive Design View**. It allows you to crop the screen and simulate different screen sizes. You can access it from the Firefox browser Tools drop-down menu under **Tools>Web Developer>Responsive Design View**.

The other tool was an actual **mobile phone**! I have an Android device with several browsers installed. By running the game in `localhost`

and then connecting my phone to my local Wi-Fi network, I could access the game at my computer’s IP.

And this would yield the first problems…

## Scaling

This is how bad the game looked in the responsive design view with no scaling at 320×480 size (landscape):

![Scaling issues](../../assets/ac7867991972141e.png)


The solution was to use Phaser’s `ScaleManager`

to scale the game so it would fit well on the screen (with letter-boxing if needed):

```
var BootScene = {
init: function () {
// make the game occuppy all available space, but respecting
// aspect ratio – with letterboxing if needed
this.game.scale.scaleMode = Phaser.ScaleManager.SHOW_ALL;
this.game.scale.pageAlignHorizontally = true;
this.game.scale.pageAlignVertically = true;
},
// ...
};
```


Furthermore, in the original game I used a wrapping `div`

element to center the game on the page and also add some padding, text, etc. Now, all these page elements would have to be removed for the game to access all the available screen space.

![Proper scale](../../assets/00821d329b794393.png)


Much better now!

## Input

The next issue was **controls**. My desktop game used the arrow keys to move and jump the main character. I opted to include a virtual gamepad, so I created a new image for it:

![Virtual gamepad](../../assets/9fa8f4d40ec7cf8e.png)


I needed three buttons: two for moving left and right and another one for jumping. I created three `Phaser.Button`

instances. This was done in a helper function:

`var upBtn = new Phaser.Button(this.game, ...);`


Since `Phaser.Button`

doesn’t have a flag that tells us whether a button is pressed or not, I needed to add it myself. This is easily done by listening to `inputDown`

and `inputUp`

events.

```
[leftBtn, rightBtn, upBtn].forEach(function (btn) {
// register callbacks
btn.isDown = false;
btn.events.onInputDown.add(function () { btn.isDown = true; });
btn.events.onInputUp.add(function () { btn.isDown = false; });
```


We also need to listen to the Up button’s `inputDown`

, to enable the character to jump, since jumping in the desktop game was triggered by a `keyDown`

event:

```
btnUp.events.onInputDown.add(this.tryJump, this);
```


For moving, it was just a matter of checking the `isDown`

flag I’d already set, in addition to the previous check against the `this.keys.left`

keyboard key.

```
if (this.keys.left.isDown || this.keys.btnLeft.isDown) {
this.hero.move(-1);
}
```


![Added virtual gamepad](../../assets/f9dad9fea53eaeb8.png)


The game was then playable on my device in the Firefox and Chrome for Android mobile browsers. However, play testing revealed even more issues…

## Reposition elements

While I was playing the game I noticed that my own fingers would hide the game characters. This was a huge deal, since it made the game very difficult and annoying to play.

The solution was to make the group bigger (100 pixels) and then shift all the game elements up.

![Reposition ground and characters](../../assets/3fb8e14f1ed51645.png)


## Allow tapping on additional areas

I also found out that tapping on the **click to restart** text was a bit hard. So I made the **Game Over** text, which was bigger, clickable too.

```
// create game over text
var banner = this.game.add.text(...);
banner.inputEnabled = true;
banner.events.onInputUp.add(this.restartGame, this);
```


In addition to that, I substituted **click to restart** for **tap to restart**, which makes more sense in mobile environments.

### Revamping the splash screen

The splash screen needed some love too, since it was originally hardcoded to a fixed resolution.

The first step was to resize the background to take up the whole screen space, while maintaining its aspect ratio:

```
.overlay {
background-size: cover;
}
```


Then I resized some of the existing text and buttons, and deleted the controls help diagram, since it referred to desktop arrow keys.

![Splash screen](../../assets/86e3b5ef8fbc3188.png)


### Re-playability

Finally, the game was fully playable… but now it was **too short**! The original game had five predefined waves of enemies. It was fine for the game jam, since most people only try the games for a very short amount of time (there are literally thousands of games to try out).

For a mobile game, one quick minute of gameplay is not good enough. So I tweaked the gameplay code to get rid of the predefined waves and make them **random and infinite**. Unlimited playtime!

## Transform into a Firefox OS app

Once the game worked decently and was fun to play, it was time to turn it into a Firefox OS app.

### Run in the simulator as a hosted app

The first step was to run it as a hosted app in a Firefox OS Simulator.

You can get the Simulator from the WebIDE (**Tools > Web Developer > WebIDE**) by clicking **Install Simulator** in the right sidebar. I installed Firefox OS version 2.6.

![Install simulator](../../assets/9c82063f944d7bb5.png)


To create a hosted web app, we need an **icon** referenced in a JSON file with some metadata. This file is called the [web app manifest](https://developer.mozilla.org/en-US/Apps/Build/Manifest).

While you can provide different sized icons, the minimum requirement is to have a `128x128`

one:

![Icon 128x128](../../assets/d535270f971fc753.png)


The [manifest file](https://developer.mozilla.org/en-US/Apps/Build/Manifest) is just a JSON file in our app’s root. It contains some metadata about our app: the name of the app, the author, locales, etc. This is what the initial version of my `manifest.webapp`

looked like.

```
{
"name": "Metal vs Hipsters",
"description": "Arcade game",
"launch_path": "/index.html",
"icons": {
"128": "/images/icon-128.png"
},
"developer": {
"name": "Belén 'Benko' Albeza",
"url": "http://www.belenalbeza.com"
},
"default_locale": "en",
"version": "1.0.0"
}
```


To run Metal vs Hipsters in the Simulator from the WebIDE, click on **Open Hosted App** and then point to the location of the manifest in the running local server:

![Open Hosted App](../../assets/0e3cbb560b599654.png)


![Manifest URL](../../assets/982f65eae43cbb35.png)


Now my project has been added…

![Hosted web app](../../assets/3e2915131a737690.png)


…and we can finally run it in the simulator.

![Game running on simulator](../../assets/5c0b20356db3863a.png)


### Run in the phone as a packaged app

Running a game in the simulator is cool, but nothing beats playing **your game on a real device**. I wanted to create a [packaged app](https://developer.mozilla.org/en-US/Marketplace/Options/Packaged_apps) in addition to a hosted app for Firefox Marketplace.

I had an Xperia Z3 Compact with Firefox OS on it ready for action. Once plugged in via USB and with [developer mode](https://developer.mozilla.org/en-US/Firefox_OS/Developer_Mode) enabled, it was listed in the WebIDE on the `USB devices`

list.

![Devices list](../../assets/42f9e7a28be614ae.png)


The workflow for creating a packaged app is very similar to the one I described for a hosted app. In the WebIDE click on **Open Packaged App** and then point to the game’s folder:

![Packaged app](../../assets/bb3832c6f61553db.png)


With my phone selected as a device, I clicked on the “play” button in the top bar and… boom!

![Game running on Firefox OS phone](../../assets/97496d2397f6ed6c.png)


Now that I had the game running on a phone I could take advantage of some **settings available only for apps** and not just mobile websites. I wanted the game to run in **fullscreen** (without any prompting!) and I wanted to force a **landscape** orientation. I was able to do this by adding some more settings to the manifest.

```
{
...
"fullscreen": "true",
"orientation": ["landscape"]
}
```


![Game running in fullscreen](../../assets/bb31c703031d2d62.png)


### Local assets

Now that I’d built the game as a packaged app, I needed to include all the assets needed to run it. The game uses one font from Google Fonts, `Bangers`

. For the game jam, I included the font using one of Google’s suggested methods: linking to CSS on their servers that contains the font definition.

```
<link href='http://fonts.googleapis.com/css?family=Bangers'
rel='stylesheet' type='text/css'>
```


As you can see, this won’t work for a packaged app, since it’s possible for a player to launch the game for the first time **while offline**, and they would not be able to access the font. Luckily, these fonts are also available for download and distribution with your projects (yay for open source!), so I did just that.

I copied the content of Google’s CSS file to my own CSS, changed the `src`

URL to point to my local copy, and everything was set!

```
@font-face {
font-family: 'Bangers';
font-style: normal;
font-weight: 400;
src: url(../fonts/Bangers.woff2) format('woff2');
}
```


## Into the Firefox Marketplace

### Packaging for Firefox OS

A packaged app is distributed via a single **zip file** with our application on it. I was using a task runner, Gulp, to automate some parts of the development; so I added a new task to generate this zip file automatically. I made use of the `gulp-zip`

module.

```
npm install gulp-zip --save
gulp.task('release', ['dist'], function () {
var data = JSON.parse(fs.readFileSync('./package.json'));
var filename = data.name + '-' + data.version + '.zip';
return gulp.src('./dist/**/*')
.pipe(zip(filename))
.pipe(gulp.dest('.'));
});
```


Tip: once generated, *always* unzip your file to make sure everything is there!

### Submitting your app to Firefox Marketplace

You can [submit your app to the Marketplace](https://marketplace.firefox.com/developers/submit/), but you will need to create an account first.

Once logged in, I selected **Free App**, then **Packaged** and uploaded the zip file. Then the manifest and app files were validated.

![App validation](../../assets/5156e8b12ba4171a.png)


There were some **warnings related to the CSP**, but since the game doesn’t ask for special permissions (like access to the contacts), it’ll be OK. These CSP warnings were due to Phaser using

`document.createElement('script')`

when using bitmap fonts. Since my game wasn’t using these fonts, I could just monkey patch Phaser and remove that code bit if I really needed special permissions for my game.In order to submit the game, I had to provide a privacy policy. The game wasn’t collecting or storing any sort of data, so I settled by writing just that:

```
This application does not store or collect personal information or any kind of user data.
```


If your game does collect data, check out the [privacy policy guidelines](https://developer.mozilla.org/en-US/Marketplace/Publishing/Policies_and_Guidelines/Privacy_policies) in the MDN to help you draft one.

I also needed some `320x480`

screenshots:

![Marketplace screenshot](../../assets/c2dcf7f947bca1a9.png)


As the last step, I was asked to setup **content rating**. The submission form takes you to the [IARC tool](https://www.globalratings.com/IARCProdRating/Submission.aspx), which is a wizard to help you rate your game depending on some criteria. Since my game features a form of fantasy violence –I guess a guitar of flames that destroys hipsters and cupcakes counts as so–, this ended up rated as PEGI-12.

![PEGI rating](../../assets/1a9fac9443af4288.png)


All done! Now time to wait a bit until it gets reviewed and approved.

## More tweaks and potential improvements

**Not all browsers have the same support** of features or file formats. While testing the game in different devices, I found out some issues with Safari on iOS: the webfont wasn’t loaded properly and the background music tracks was not being played. The issue was that Safari for iOS doesn’t support neither Woff nor OGG as formats for fonts and audio (tip: you can check these things in [Can I use?](http://caniuse.com)). All I had to add to be able to play the game in my iPad was to add those assets in TTF and MP4 as well.

The game should be playable in major major mobile browsers (Firefox, Chrome and Safari). I expect trouble with IE/Edge, but I don’t have a Windows device at hand to test this.

Although the current version is fun to play in browsers, there are other **improvements that could make this a better game**: use of the [vibration API](https://developer.mozilla.org/en-US/docs/Web/API/Vibration_API) when the main character gets killed, store the high-score with [localStorage](https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage), allow [installation of the app](https://developer.mozilla.org/en-US/Marketplace/Options/Self_publishing) directly from the game’s website, support for [offline mode](https://developer.mozilla.org/en-US/Apps/Build/Offline) in the web version, etc.

## Play!

The game is already [available in the Firefox Marketplace](https://marketplace.firefox.com/app/metal-vs-hipsters/) for downloading. You can also [play the game from your mobile browser here](http://belen-albeza.github.io/ldjam-32-fxos/), and grab the full [source code at Github](https://github.com/belen-albeza/ldjam-32-fxos) as well.

I hope this article can help to port your HTML 5 games to mobile and Firefox OS. Most of the times they don’t need much tweaking and you could expand your player base. Plus **playing your own game while commuting** is priceless :)

## About
[
Belén Albeza ](http://www.belenalbeza.com)

Belén is an engineer and game developer working at Mozilla Developer Relations. She cares about web standards, high-quality code, accesibility and game development.

## One comment

Ben LaanDecember 7th, 2015 at 16:25