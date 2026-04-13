---
title: Unity Firebase SDK behaviour the docs didn't tell you
url: https://gametorrahod.com/firebase-behaviour-in-unity/
author: Sirawat Pitaksarit
published: '2019-09-15'
source_blog: Game Torrahod
source_site: https://gametorrahod.com/
category: game programming
fetched: '2026-04-13'
---

## There is persistence magically built in

For example if you `FirebaseAuth.DefaultInstance.SignInWithEmailAndPasswordAsync`

and then close the game, when you come back `FirebaseAuth.DefaultInstance.CurrentUser`

exists complete with correct UID! That UID information is there even if no internet connection.

I thought I must sign in again but I was wrong. However I don't know if this persistence could disappear depending on time or not. These are what I found from the debug app I wrote.

![](../../assets/6e1b608ddefa88ce.png)

- If you uninstall the app and reinstall it, the auth is gone.
- If you overwrite the app (e.g.
`adb install -r`

the same APK) the auth is preserved. This maybe telling that app upgrade also preserves the auth. - If you sign in, close the app, then you go delete that user in Firebase Authentication console, then open the app and quickly check the preserved auth, you can see the UID briefly before turning into
`null`

. There is a step that try to sync with server and update the persistence accordingly. - If you do that except while the app is open, you can indefinitely check for UID and it will not go away
**until**you take some kind of Firebase action. This confirms that the check is not continuous in the background, there are some point that it do this including when initialize the app instance when opening the game. - The error message when you try to take action on disappeared user is "There is no user record corresponding to this identifier. The user may have been deleted". (Error code : 14) For example, you sign in, delete the user at console, then try to link additional credential.
- If you press delete app cache on Android, the auth is not gone.
- If you press delete app data on Android, the auth
**is gone.**(The left button on this individual app storage page)

![](../../assets/4598aba1e3c24f74.png)

- I am not sure there is a timed element to preserve the auth or not.

## Multiple FirebaseApp instance individually preserves auth

For example, I can create an another `FirebaseApp`

that use the same option as the default one with : `FirebaseApp.Create(FirebaseApp.DefaultInstance.Options, "Secondary Instance");`

Firebase identify instance by `string`

name it seems, if not keeping the `FirebaseApp`

returned I could get it back with `FirebaseApp.GetInstance("Secondary Instance")`

.

If I sign in to 2 ID on default and on my `Secondary Instance`

, on the next run, if I create an instance named `Secondary Instance`

again I can see the preserved auth. This way I can preserve 2 logins at the same time!

I don't know if I use a different `AppOption`

but the same name, will it be linked or not? Anyways I don't dare to use any other app option at the moment.

## The auth preserving is the only sane way to use `SignInAnonymously`


By knowing this property, one can use `SignInAnonymously`

(SIA) meaningfully. You can make an ID for your player without they knowing, and they can use all online features and have a save backup without providing e-mail or thinking up a new password, which they may reluctant to give their password that they reused on the other services to no name dev like you, or too troublesome to think of a new one. This is a smooth onboarding. You can also write a Firebase Functions to trigger on new registration, so all anonymous ID could get things prepped as if they are a real player. (Or a bit less than real player.)

The point is you must not lightly call `SignOut`

because anonymous is preserved across app run but you can't get it back by any means once it is gone. SIA again results in arriving at a new ID.

You may randomly call sign out and sign in at the start of your app for some reason. The correct approach is to **first check the auth **before doing anything because the auth could be there already, as we learned.

Here are what I found so far :

- SIA and SIA again you will
**not**get a new UID. The code has been prevented. - SIA and sign out and SIA again you will get a new anonymous UID. However there is a limit to prevent this SIA -> sign out loop to create many account built in to the auth which your user may abuse to drain your Firebase money.

![](../../assets/e6ac8391a5289e81.png)

- SIA and
`LinkWithCredential`

can**turn**anonymous ID into a registered ID. It is**not**linking 2 different account with different UID. From preserved auth standpoint the UID didn't change only that the e-mail was added. The "link" is not in the sense as linking 2 Firebase Auth account together, it is like**registering**a new e-mail account with the same UID as the anonymous one, rather. (So the account with that e-mail have to not exist before, the "link" wording may confuse you.) Any work the user had done could be continued since UID is the same and you probably use UID for check in database rules.

```
var cred = Firebase.Auth.EmailAuthProvider.GetCredential("test@test.com", "testtest");
instance.CurrentUser.LinkWithCredentialAsync(cred)...
```


- If you SIA then link, then SIA again, you get a new anonymous UID.
- I don't know if anonymous ID can somehow "expire" on its own or not, and I don't know how to debug it other than leaving the auth preserved for a year without opening the app, then check again. This is quite worrisome because I do not have time for that. However it maybe OK if you check the auth on app start and if it is gone, you get the player a new anonymous UID and try to make that the same as the previous one which is gone.

### Strategies for some action that requires leaving the anonymous auth

For example, your player is still in anonymous state. You provide a dialog to invite the player to make his account to make it real. However, there is an another dialog to sign in to an existing account. The player realized they want to play using the same ID as the other phone so he went to sign in instead. He enters a correct credential.

A warning dialog pops up **after signing in**, showing that the progress you made (while anonymous, or while signed in to other account) will be replaced with that of this ID. (While showing some content from this newly signed in ID, accessible in Firestore rule because you are signed in.)

Then the player hesitates. "Maybe I want to keep playing this ID separately after all. And maybe register a new ID for it but not today."

The problem is you have already signed out of anonymous ID in order to display that warning dialog, and you cannot get to that again!

Because anonymous ID is precious and volatile, the approach maybe use a new `FirebaseApp`

instance to sign in to 2nd ID first "just to take a look", then if it is OK sign in on the main one abandoning the anonymous ID. This allows the player to change his mind later.

Or you can have a dedicated `FirebaseApp`

just for anonymous ID for this device, so you can ensure it will not go away even if the player sign in and sign out how many times. You can name it as `Device Instance`

or something. Indicating that it will always be signed in to anonymous ID, unless linked and become a real ID, then this instance should get a new anonymous ID replaced.