---
title: Using Spotify Android SDK in Unity
url: https://cmwdexint.com/2024/01/13/using-spotify-android-sdk-in-unity/
author: Ming Wai Chan
published: '2024-01-13'
source_blog: Ming Wai Chan
source_site: https://cmwdexint.com
category: graphics
fetched: '2026-04-13'
---

Unity 2022.3.14f1 + [spotify-app-remote-release-0.8.0](https://developer.spotify.com/documentation/android)

Seeing there is no tutorial about this and I’ve been recently playing with this so hopefully this would help someone like myself 🙂

In my case I’m using AppRemote only as I only want to grab Spotify’s current playing track information on my Android app + trigger song playing. If you are also going to use the Spotify Android SDK, make sure you have installed latest Spotify app on your Android device.

[Unity Project Setup](https://cmwdexint.com/2024/01/13/using-spotify-android-sdk-in-unity/#unity-project-setup)[Install Spotify Android SDK](https://cmwdexint.com/2024/01/13/using-spotify-android-sdk-in-unity/#install-spotify-android-sdk)[From and to Unity C# script and Java](https://cmwdexint.com/2024/01/13/using-spotify-android-sdk-in-unity/#from-and-to-unity-c-script-and-java)[Spotify Android Media Notifications](https://cmwdexint.com/2024/01/13/using-spotify-android-sdk-in-unity/#spotify-android-media-notifications)

### Unity Project Setup

- Create a new Unity project, of course install the Android platform module too
- Once your project is opened
- TopMenu > File > Build Settings > Android > click Switch Platform
- TopMenu > Edit > Project Settings > Player, enter your own names
![](../../assets/8a73bb94ceda067b.jpg)

- Scroll to below, under Other Settings, note the default package name
![](../../assets/efe17ce78973ee40.jpg)

- Scroll to below, under Publish Settings, click Keystore Manager and create a new keystore file
- Use the keystore file on the Publish Settings

(In the future when you open the project again, in order to make a build, you will need to type the passwords again) - TopMenu > File > Save Project
- TopMenu > File > Build Settings > Build Settings >

on Run Device > select your connected Android device

check Development Build checkbox and then click Build and Run - This can confirm if your PC and Unity is setup correctly to build Android application

### Install Spotify Android SDK

- Go to
[https://developer.spotify.com/documentation/android/tutorials/getting-started](https://developer.spotify.com/documentation/android/tutorials/getting-started)

and follow**Register Your App**section.

Fill in your app details like this:![](../../assets/af8d422b4eebecfa.jpg)

- On the app’s Home page, go to Settings page

Add your package name which is same as the one in Unity Project Settings.![](../../assets/29edfe80f0121fd7.jpg)


You will also need the**SHA1 fingerprint**, to get it:

On your Windows search, type`cmd`

, then edit following and type:`cd C:`

`\`

your Unity Editor folder path\Data\PlaybackEngines\AndroidPlayer\OpenJDK\bin`keytool -list -v -keystore C:\your folder path where the keystore file is\user.keystore -alias yourAlias -storepass yourStorePassword -keypass yourKeyPassword`


- The settings page should look something like this.

Note the**Client ID**on the top.![](../../assets/8aadd34494d330bc.jpg)

- Go to
[https://github.com/spotify/android-sdk/releases](https://github.com/spotify/android-sdk/releases) - Download only
**spotify-app-remote-release-0.8.0.aar** - Put this .aar file in your Unity project’s
**Assets/Plugins/Android**folder

Create the folders yourself if there isn’t one.![](../../assets/635ab01583471d9c.jpg)

- TopMenu > Edit > Project Settings > Player > Publish Settings,

check**Custom Main Manifest**and**Custom Main Gradle Template**![](../../assets/88fe5a94c23de80c.jpg)

- Open and edit the generated
**mainTemplate.gradle**file,

add`implementation "com.google.code.gson:gson:2.6.1"`

in dependencies![](../../assets/52ffa108e17c3b44.jpg)

- Open and edit the generated
**AndroidManifest.xml**file,

Change`<activity android:name="com.unity3d.player.UnityPlayerActivity"`


To`<activity android:name=".MainActivity"`

- In
**Assets/Plugins/Android**folder, create a file called**MainActivity.java**, paste the below**[Code for MainActivity.java]**code to it. Remember to edit the client id! - Make sure you have Spotify app running on your Android device
- Build and Run to your Android device.

If success, on your Android device you should see a Spotify permission agreement screen for your app. Click AGREE. After your app starts, Spotify will start playing songs from the playlist “[Feel-Good Indie Rock](https://open.spotify.com/playlist/37i9dQZF1DX2sUQwD7tbmL)“. That means the setup is successful! 🎉 - Tips: TopMenu > Window > Package Manager > select
*Packages: Unity Registry*and Install*Android Logcat*

TopMenu > Window > Analysis > Android Logcat

You can also see the related messages from the java script on Logcat![](../../assets/04b815c3218d8be4.jpg)

- Now you can further edit
**MainActivity.java**to do things you want 🎉

**Code for MainActivity.java**

(The original code comes from: [Spotify Android SDK documentation)](https://developer.spotify.com/documentation/android/tutorials/getting-started)

```
package com.unity3d.player;
import android.os.Bundle;
import com.unity3d.player.UnityPlayerActivity;
import android.content.Intent;
import android.content.IntentFilter;
import android.util.Log;
import com.spotify.android.appremote.api.ConnectionParams;
import com.spotify.android.appremote.api.Connector;
import com.spotify.android.appremote.api.SpotifyAppRemote;
import com.spotify.protocol.client.Subscription;
import com.spotify.protocol.types.PlayerState;
import com.spotify.protocol.types.Track;
public class MainActivity extends UnityPlayerActivity
{
public static MainActivity instance; // For Unity C# to trigger functions here
public static String currentPlaying = ""; // For Unity C# to read current playing info
private static final String CLIENT_ID = "your client id"; // Use your own Client Id
private static final String REDIRECT_URI = "http://localhost:5000/callback"; // Also match this on the app settings page
private SpotifyAppRemote mSpotifyAppRemote;
@Override
protected void onCreate(Bundle savedInstanceState)
{
super.onCreate(savedInstanceState);
instance = this;
}
// Triggered by Unity C# script
public void PlaySong(String trackId)
{
mSpotifyAppRemote.getPlayerApi().play("spotify:track:" + trackId);
}
@Override
protected void onStart()
{
super.onStart();
ConnectionParams connectionParams =
new ConnectionParams.Builder(CLIENT_ID)
.setRedirectUri(REDIRECT_URI)
.showAuthView(true)
.build();
SpotifyAppRemote.connect(this, connectionParams, new Connector.ConnectionListener()
{
public void onConnected(SpotifyAppRemote spotifyAppRemote)
{
mSpotifyAppRemote = spotifyAppRemote;
Log.d("MainActivity", "Connected! Yay!");
// Now you can start interacting with App Remote
connected();
}
public void onFailure(Throwable throwable) {
Log.e("MyActivity", throwable.getMessage(), throwable);
// Something went wrong when attempting to connect! Handle errors here
}
});
}
@Override
protected void onStop()
{
super.onStop();
SpotifyAppRemote.disconnect(mSpotifyAppRemote);
}
private void connected()
{
// Play a playlist
mSpotifyAppRemote.getPlayerApi().play("spotify:playlist:37i9dQZF1DX2sUQwD7tbmL");
// Subscribe to PlayerState
mSpotifyAppRemote.getPlayerApi()
.subscribeToPlayerState()
.setEventCallback(playerState ->
{
final Track track = playerState.track;
if (track != null) {
Log.d("MainActivity", track.name + " by " + track.artist.name);
currentPlaying = track.name + " by " + track.artist.name;
}
});
}
}
```

### From and to Unity C# script and Java

This part is straight-forward, just use [AndroidJavaClass](https://docs.unity3d.com/ScriptReference/AndroidJavaClass.html) and [AndroidJavaObject](https://docs.unity3d.com/ScriptReference/AndroidJavaObject.html) API.

With the above **[Code for MainActivity.java]** code, you can have a C# script to read the Spotify info and trigger to play a song.

**Code for ExampleScript.cs**

```
using System;
using UnityEngine;
using UnityEngine.UI;
public class ExampleScript : MonoBehaviour
{
private AndroidJavaClass mainActivityClass;
private AndroidJavaObject mainActivityObject;
public Text currentPlayingText;
void Start()
{
mainActivityClass = new AndroidJavaClass("com.unity3d.player.MainActivity");
mainActivityObject = mainActivityClass.GetStatic<AndroidJavaObject>("instance");
}
private void Update()
{
UpdateCurrentPlaying();
}
public void PlaySong()
{
mainActivityObject.Call("PlaySong","4SFknyjLcyTLJFPKD2m96o"); // BLACKPINK - How You Like That
}
public void UpdateCurrentPlaying()
{
currentPlayingText.text = mainActivityClass.GetStatic<string>("currentPlaying");
}
}
```

### Spotify Android Media Notifications

Actually, you can get the current playing track info **without the SDK**! You can get:*track id, artist, album, track names and length, as well as playing status and position.*

See [https://developer.spotify.com/documentation/android/tutorials/android-media-notifications](https://developer.spotify.com/documentation/android/tutorials/android-media-notifications)

⭐On your Android device, open Spotify app, click on your profile > Settings and privacy > Playback > enable **Device Broadcast Status**⭐

- In
**Assets/Plugins/Android**folder, create a file called**MyBroadcastReceiver.java**, paste the below**[Code for MyBroadcastReceiver.java]**code to it.

**Code for MyBroadcastReceiver.java**

(The original code comes from:

[Spotify Android SDK documentation)](https://developer.spotify.com/documentation/android/tutorials/android-media-notifications)

```
package com.unity3d.player;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.util.Log;
public class MyBroadcastReceiver extends BroadcastReceiver
{
static final class BroadcastTypes
{
static final String SPOTIFY_PACKAGE = "com.spotify.music";
static final String PLAYBACK_STATE_CHANGED = SPOTIFY_PACKAGE + ".playbackstatechanged";
static final String QUEUE_CHANGED = SPOTIFY_PACKAGE + ".queuechanged";
static final String METADATA_CHANGED = SPOTIFY_PACKAGE + ".metadatachanged";
}
public static String currentPlaying = ""; // For Unity C# to read current playing info
@Override
public void onReceive(Context context, Intent intent)
{
long timeSentInMs = intent.getLongExtra("timeSent", 0L);
String action = intent.getAction();
if (action.equals(BroadcastTypes.METADATA_CHANGED))
{
String trackId = intent.getStringExtra("id");
String artistName = intent.getStringExtra("artist");
String albumName = intent.getStringExtra("album");
String trackName = intent.getStringExtra("track");
int trackLengthInSec = intent.getIntExtra("length", 0);
// Do something with extracted information...
currentPlaying = trackName + " by " + artistName;
}
else if (action.equals(BroadcastTypes.PLAYBACK_STATE_CHANGED))
{
boolean playing = intent.getBooleanExtra("playing", false);
int positionInMs = intent.getIntExtra("playbackPosition", 0);
// Do something with extracted information
}
else if (action.equals(BroadcastTypes.QUEUE_CHANGED))
{
// Sent only as a notification, your app may want to respond accordingly.
}
}
}
```

- Open and edit the
**AndroidManifest.xml**file again, add highlighted:

```
<activity android:name=".MainActivity"
...bla bla bla...
</activity>
<receiver
android:name=".MyBroadcastReceiver"
android:enabled="true"
android:exported="true">
<intent-filter>
<action android:name="com.spotify.music.playbackstatechanged"/>
<action android:name="com.spotify.music.metadatachanged"/>
<action android:name="com.spotify.music.queuechanged"/>
</intent-filter>
</receiver>
```

- Edit above
**[Code for MainActivity.java]**code, in`onCreate`

function, add highlighted:

```
@Override
protected void onCreate(Bundle savedInstanceState)
{
super.onCreate(savedInstanceState);
instance = this;
var receiver = new MyBroadcastReceiver();
var filter1 = new IntentFilter("com.spotify.music.playbackstatechanged");
var filter2 = new IntentFilter("com.spotify.music.metadatachanged");
var filter3 = new IntentFilter("com.spotify.music.queuechanged");
// RECEIVER_EXPORTED is needed for Android 14+
registerReceiver(receiver, filter1, RECEIVER_EXPORTED);
registerReceiver(receiver, filter2, RECEIVER_EXPORTED);
registerReceiver(receiver, filter3, RECEIVER_EXPORTED);
Log.d("MainActivity", "Receiver Registered!");
}
```

- Edit
**[Code for**code to get whatever value from**ExampleScript.cs**]🙂**MyBroadcastReceiver**.java - DONE! If you don’t need the SDK, I guess you know what to remove 😅

If this helped you, please give this post a clap 😀 Thank you

Why?

LikeLike