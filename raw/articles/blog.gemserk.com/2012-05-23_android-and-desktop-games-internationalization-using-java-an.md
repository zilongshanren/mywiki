---
title: Android and Desktop games internationalization using Java and LibGDX
url: https://blog.gemserk.com/2012/05/23/android-and-desktop-games-internationalization-using-java-and-libgdx/
published: '2012-05-23'
source_blog: Gemserk
source_site: https://blog.gemserk.com/
category: game programming
fetched: '2026-04-13'
---

Recently, we had to add multiple language support for a game we are developing. As you may know, Java provides classes to simplify the task of making your application available in multiple languages. In this post we want to share a bit our experience when using Java localization classes in a LibGDX application to provide multiple language support for both Android and desktop platforms.

### Quick introduction

Java provides a class named [ResourceBundle](http://docs.oracle.com/javase/6/docs/api/java/util/ResourceBundle.html) which provides a way to store resources (mainly strings) for a given locale, so you can ask for a string identified by a key and it will return the text depending the current locale. You can read the article [Java Internationalization: Localization with ResourceBundles](http://java.sun.com/developer/technicalArticles/Intl/ResourceBundles/) if you want to know more about how to use Java classes for internationalization. The rest of the post assumes you know something about [Locale](http://docs.oracle.com/javase/6/docs/api/java/util/Locale.html) and [ResourceBundle](http://docs.oracle.com/javase/6/docs/api/java/util/ResourceBundle.html) classes.

### Why we don’t use Android resources

Android provides also a way to support multiple locale resources but it depends on Android API, so we prefer to use the Java API instead which should work on all platforms.

### Our experience when using Java internationalization on Android

When letting ResourceBundle to automatically load resources bundles from properties files, Java [expects them to be in ISO-8859-1 encoding](http://docs.oracle.com/javase/6/docs/api/java/util/PropertyResourceBundle.html). However, it seems Android behaves in a different way and expects another encoding by default. So, when resource bundles are automatically loaded in Android from an ISO-8859-1 properties file with special characters, it loads them wrong.

### The first try

The first solution we tried to fix this was to call ResourceBundle.getBundle() method using a custom [Control](http://docs.oracle.com/javase/6/docs/api/java/util/ResourceBundle.Control.html) implementation which creates [PropertyResourceBundles](http://docs.oracle.com/javase/6/docs/api/java/util/PropertyResourceBundle.html) using an InputReader with the correct encoding. Here is a code example to achieve that:

```
public class EncodingControl extends Control {
String encoding;
public EncodingControl(String encoding) {
this.encoding = encoding;
}
@Override
public ResourceBundle newBundle(String baseName, Locale locale, String format, ClassLoader loader, boolean reload)
throws IllegalAccessException, InstantiationException, IOException {
String bundleName = toBundleName(baseName, locale);
String resourceName = toResourceName(bundleName, "properties");
ResourceBundle bundle = null;
InputStream inputStream = null;
try {
inputStream = loader.getResourceAsStream(resourceName);
bundle = new PropertyResourceBundle(new InputStreamReader(inputStream, encoding));
} finally {
if (inputStream != null)
inputStream.close();
}
return bundle;
}
}
```


After that, we customized the Control class to work with LibGDX FileHandle in order to place the properties files in the assets folder. Here is the final code for our Control implementation:

```
public class GdxFileControl extends Control {
private String encoding;
private FileType fileType;
public GdxFileControl(String encoding, FileType fileType) {
this.encoding = encoding;
this.fileType = fileType;
}
public ResourceBundle newBundle(String baseName, Locale locale, String format, ClassLoader loader, boolean reload)
throws IllegalAccessException, InstantiationException, IOException {
// The below is a copy of the default implementation.
String bundleName = toBundleName(baseName, locale);
String resourceName = toResourceName(bundleName, "properties");
ResourceBundle bundle = null;
FileHandle fileHandle = Gdx.files.getFileHandle(resourceName, fileType);
if (fileHandle.exists()) {
InputStream stream = null;
try {
stream = fileHandle.read();
// Only this line is changed to make it to read properties files as UTF-8.
bundle = new PropertyResourceBundle(new InputStreamReader(stream, encoding));
} finally {
if (stream != null)
stream.close();
}
}
return bundle;
}
}
```


And that can be called in this way:

```
ResourceBundle.getBundle("messages", new GdxFileControl("ISO-8859-1", FileType.Internal))
```


That worked really well until we discovered that Android API sucks and [doesn’t support ResourceBundle.Control before API level 9](https://developer.android.com/reference/java/util/ResourceBundle.Control.html), that means our solution works only for users with Android 2.3+. That’s a problem since we want to support 2.0+, so we had to think another way to solve this.

### The second try

After some tests, we discovered that if we construct a PropertyResourceBundle using an InputStream, the expected encoding is ISO-8859-1 for both desktop and Android. That means that, if we use that specific PropertyResourceBundle constructor, we don’t have to force the encoding. So, the new solution consists in building a PropertyResourceBundle for each locale and configuring the hierarchy ourselves by setting their parent ResourceBundle. Here is an example of what we do now:

```
FileHandle rootFileHandle = Gdx.files.internal("data/messages.properties");
FileHandle spanishFileHandle = Gdx.files.internal("data/messages_es.properties");
ResourceBundle rootResourceBundle = new PropertyResourceBundle(rootFileHandle.read());
ResourceBundle spanishResourceBundle = new PropertyResourceBundle(spanishFileHandle.read()) {
{
setParent(rootResourcebundle);
}
};
```


After that we created a map of ResourceBundles for each Locale we support, so we can call something like:

```
ResourceBundle resourceBundle = getResourceBundle(new Locale("es"));
```


The good part is this solution works well for both Android and desktop despite the Android API level (PropertyResourceBudndle seems to be supported from API Level 1). The bad part is that we lost the ResourceBundle logic to automatically build the hierarchy of resources and we had to do that manually now.

UPDATE: The class we use for this stuff is available in our commons-gdx project, resources module with the name of [ResourceBundleResourceBuilder](https://github.com/gemserk/commons-gdx/blob/master/commons-gdx-resources/src/main/java/com/gemserk/commons/gdx/resources/ResourceBundleResourceBuilder.java).

### Conclusion

Supporting multiple languages in an application is a way to say users of all around the world you care about them but translating text to several languages is not cheap at all, however, Java provides a good framework to simplify the job if you decide to support internationalization.

And as a side conclusion: never assume all the Java classes you are using are implemented for the minimum Android API you are targeting.

### References

- Java Internationalization: Localization with ResourceBundles -
[http://java.sun.com/developer/technicalArticles/Intl/ResourceBundles/](http://java.sun.com/developer/technicalArticles/Intl/ResourceBundles/) - How to use UTF-8 in resource properties with ResourceBundle -
[http://stackoverflow.com/questions/4659929/how-to-use-utf-8-in-resource-properties-with-resourcebundle](http://stackoverflow.com/questions/4659929/how-to-use-utf-8-in-resource-properties-with-resourcebundle)