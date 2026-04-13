---
title: Our resources manager and how it helped in localizing Clash of the Olympians
url: https://blog.gemserk.com/2013/05/01/our-resources-manager-and-how-it-helped-in-localizing-clash-of-the-olympians/
published: '2013-05-01'
source_blog: Gemserk
source_site: https://blog.gemserk.com/
category: game programming
fetched: '2026-04-13'
---

In this post we want to share how our resources manager implementation helped us when we had to localize Clash of the Olympians.

### Our resources manager

Some time ago we started a small java project named [jresourcesmanager](https://github.com/gemserk/jresourcesmanager) (yeah, the most creative name in the world) which provides a simple abstraction of what a resource is and how it is loaded. It consists in some basic concepts named Resource, DataLoader and ResourceManager.

#### Resource

Is the concept of an application resource/asset, and provides an API to know if the resource is loaded or not and to load and unload it. Here is the code:

```
public class Resource<T> {
T data = null;
DataLoader<T> dataLoader;
protected Resource(DataLoader<T> dataLoader) {
this(dataLoader, true);
}
protected Resource(DataLoader<T> dataLoader, boolean deferred) {
this.dataLoader = dataLoader;
if (!deferred)
reload();
}
/**
* Returns the data stored by the Resource.
*/
public T get() {
if (!isLoaded())
load();
return data;
}
public void set(T data) {
this.data = data;
}
public DataLoader<T> getDataLoader() {
return dataLoader;
}
public void setDataLoader(DataLoader<T> dataLoader) {
unload();
this.dataLoader = dataLoader;
}
/**
* Reloads the internal data by calling unload and load().
*/
public void reload() {
unload();
load();
}
/**
* Loads the data if it wasn't loaded yet, it does nothing otherwise.
*/
public void load() {
if (!isLoaded())
data = dataLoader.load();
}
/**
* Unloads the data by calling the DataLoader.unload(t) method.
*/
public void unload() {
if (isLoaded()) {
dataLoader.unload(data);
data = null;
}
}
/**
* Returns true if the data is loaded, false otherwise.
*/
public boolean isLoaded() {
return data != null;
}
public Resource<T> clone() {
return new Resource<T>(dataLoader);
}
}
```


#### DataLoader

Provides an API to define a way to load and unload a Resource, here is the code:

```
public abstract class DataLoader<T> {
/**
* Implements how to load the data.
*/
public abstract T load();
/**
* Implements how to unload the data, if it is nod automatic and you need to unload stuff by hand.
*/
public void unload(T t) {
}
/**
* Provides a way to return custom information about the data loader.
*
* @return An object with the custom information.
*/
public Object getMetaData() {
return null;
}
}
```


#### ResourceManager

It is just a map with all the resources identified by a key, which can be a String for example, and an API to store and get resources to and from, respectively.

That is our resources management code, it is really simple and fulfilled our needs in assets loading/unloading for Vampire Runner and Clash of the Olympians.

The interesting part of this library is that it allows you to store whatever you want to consider as a resource/asset, and that feature is what we used in order to solve the localization issue.

### Declaring resources

Another important pillar is how we declare resources in an easy way through the code, and that is by using some builders that simplified the resource declaration. As we were using LibGDX library, we created a resource builder for LibGDX assets and more. This resource builder allowed us to do stuff like this:

```
splitLoadingTextureAtlas("MainTextureAtlas", "data/images/screens/mainmenu/pack");
resource("MainBackgroundTop", sprite2().textureAtlas("MainTextureAtlas", "mainmenu-bg", 1).center(0.5f, 0.5f).trySpriteAtlas());
```


That declares a texture atlas with the name of MainTextureAtlas and then a resource which is a sprite with the name of MainBackgroundTop from a texture atlas resource identified by the previous name. Also, allow us to do stuff like declare that the sprite is centered in the middle (the anchor point) and more.

This code is not important, just an example of some of our builders.

### Declaring localized resources

As we have the power to create complex resource builders and we needed a simple way to switch between assets given the language selected, we created a resource builder which allowed us to declare different resources, depending the current locale, using the same identifier. So, for example, we can do something like this:

```
resource("CreditsButton", new MultilanguageResourceBuilder<Sprite>() //
.defaultLocale(new Locale("en")) //
.resource(new Locale("en"), sprite2().textureAtlas(TextureAtlases.MeinMenu, "mainmenu-but-credits-en", 1).trySpriteAtlas()) //
.resource(new Locale("es"), sprite2().textureAtlas(TextureAtlases.MeinMenu, "mainmenu-but-credits-es", 1).trySpriteAtlas()) //
);
```


That declares a resource named CreditsButton which returns a sprite with index 1 and name “mainmenu-but-credits-en” from a texture atlas in case the locale is English and a sprite with index 1 and name “mainmenu-but-credits-es” in case the locale is Spanish. It also declares that the default locale (in case a resource for the current locale wasn’t found) is English.

This resource builder was very handy because it allowed us to declare any type of resource for different locales, and from the application side it was transparent, we just ask for the resource CreditsButton.

In case you are interested, the code of the MultilanguageResoruceBuilder is:

```
public class MultilanguageResourceBuilder<T> implements ResourceBuilder<T> {
private Map<Locale, ResourceBuilder<T>> resourceBuilders = new HashMap<Locale, ResourceBuilder<T>>();
private Locale defaultLocale;
@Override
public boolean isVolatile() {
if (defaultLocale == null)
throw new IllegalStateException("Multilanguage resource builder needs a default locale");
ResourceBuilder<T> resourceBuilder = resourceBuilders.get(defaultLocale);
if (resourceBuilder == null)
throw new IllegalStateException("Multilanguage resource builder needs a default resource builder");
return resourceBuilder.isVolatile();
}
public MultilanguageResourceBuilder<T> defaultLocale(Locale locale) {
this.defaultLocale = locale;
return this;
}
public MultilanguageResourceBuilder<T> resource(Locale locale, ResourceBuilder<T> resourceBuilder) {
resourceBuilders.put(locale, resourceBuilder);
return this;
}
@Override
public T build() {
Locale locale = Locale.getDefault();
if (defaultLocale == null)
throw new IllegalStateException("Multilanguage resource builder needs a default locale");
if (!resourceBuilders.containsKey(locale))
locale = defaultLocale;
ResourceBuilder<T> resourceBuilder = resourceBuilders.get(locale);
if (resourceBuilder == null)
throw new IllegalStateException("Multilanguage resource builder needs a default resource builder");
return resourceBuilder.build();
}
}
```


### Conclusion

That was the way we used to support multiple languages in a transparent way for the application, we just need to change the current locale and reload the assets.

Hope this blog post idea helps you in case you are about to support multiple languages in your game, and see you next time.