---
title: The simplest registering system in the world
url: https://dewitters.com/the-simplest-most-easy-login-system-in-the-world/
published: '2012-08-14'
source_blog: deWiTTERS
source_site: https://dewitters.com
category: game programming
fetched: '2026-04-13'
---

[RPG Playground](http://rpgplayground.com) needs a way to save and load levels. But for that to happen, it needs a proper login system, to store your data online.

I thought a lot about a proper login and registering system, and I think I found the perfect one.

![login_dialog login_dialog](../../assets/059f52474bed16d0.png)


I didn’t copy any other system found on the web. I just hate it when you create a new account for some service, and have to provide a bunch-load of info, double fields for email and password, wait for a confirmation email, etc. I know a lot of people, including myself, think this is a barrier for signing up to a new service.

So what I did is drop everything but the absolutely necessary.

As it turned out, it seems you can drop almost everything. Creating an account is as easy as logging in. All you have to do is enter your email and password, and click on the “Create Account” button. I dropped all the usual bloated features that other systems use:

- Second password field for validation: This is used to make sure you typed in your password correctly. But since you can reset your password at any time (in case you forgot it for example), entering a wrong password is not a big deal, so RPG Playground doesn’t require you to enter your password twice.
- Login name: Why need a login name when you have an email address? I sometimes forget my login name at certain websites, but I never forget my own email address. Besides, it’s unique, so no need for those annoying “there is already a user named johndoe85, please try another name”.
- Email validation: RPG Playground doesn’t validate your email address. The only reason I need your email address is for when you forgot your password. When that happens, you can request an email which allows you to reset your password. So you can enter a fake email address or that from someone else, but when you do, you cannot reset your password, or even worse, the one with the real email address can reset it and take over your account. So filling in a wrong email address is not a problem for me, but it can be for you. Since I won’t use this email address for bugging you with commercial mails, I don’t see the need to validate it.
- Personal info: Name, address, telephone number, …, I don’t see why I would need this. You won’t receive phone calls or bulk emails that have your name in it to look personalized.

So basically registering is as easy as logging in, you just need to click the “Create Account” button instead of the “Log in” button.

There was one other issue that I had trouble with: the names for the buttons. For logging in, possible names are “Login”, “Log in”, “Sign in”, and for registering: “Join”, “Register”, “Sign up” and “Create Account”. Every website seems to handle this differently. I found a bunch of good information on this, and went for the “Log in”/”Create Account” combo. See

[Web Form Design Patterns: Sign-Up Forms](http://uxdesign.smashingmagazine.com/2008/07/04/web-form-design-patterns-sign-up-forms/)[When to use “join,” “register,” or “sign up”?](http://ux.stackexchange.com/questions/11936/when-to-use-join-register-or-sign-up)[Using “Sign in” vs using “Log in”](http://ux.stackexchange.com/questions/1080/using-sign-in-vs-using-log-in)[Why Sign Up and Sign In Should Never Go Together](http://uxmovement.com/navigation/why-sign-up-and-sign-in-should-never-go-together/)

So I will create the easiest registering system in the world for [my RPG Editor](http://rpgplayground.com). But unfortunately for now, it won’t remember your login, so you will have to log in after you close it. That’s one feature I would like to add in the future.


Everything should be made as simple as possible, but not simpler. — Albert Einstein

## 3 Comments

## Steven Jeuris · August 21, 2012 at 08:04

You raise some very valid points, but why not use OpenID? http://openid.net/get-an-openid/what-is-openid/

## Koen Witters · August 21, 2012 at 10:30

I thought about using OpenID, but I decided that I could add support for that later on. For people who don’t have an OpenID yet (and I have no idea how many there are), it’s easy to register. So for now, it’s all proprietary. Shame on me ;).

## RPG Playground 0.2 is a fact – Koonsolo Games · September 23, 2012 at 11:26

[…] I tried to make it as easy as possible to create a new account on RPG Playground, and I think the final result is perfect. You can read more about it in my previous blog post. […]