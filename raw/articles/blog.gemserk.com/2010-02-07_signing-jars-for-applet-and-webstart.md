---
title: Signing JARs for Applet and Webstart
url: https://blog.gemserk.com/2010/02/07/signing-jars-for-applet-and-webstart/
published: '2010-02-07'
source_blog: Gemserk
source_site: https://blog.gemserk.com/
category: game programming
fetched: '2026-04-13'
---

We are developing our games using Java and deploying them as Applets and Webstart applications.

By default, applications launched with Java Webstart or as an Applet run in a restricted environment. We are using some technologies which require unrestricted access like [Lwjgl](http://lwjgl.org/), [Jinput](https://jinput.dev.java.net/) and custom ClassLoaders. In order to have access to these features, every jar must be signed with a certificate.

Once the jars have been downloaded on the client machine and the signature is validated, the user is requested whether he trust or not the provider of the certificate and if he wants to accept it permanently.

In the beginning, one option is to generate a new certificate every time we sign the jars of an application but this means that although the user might have accepted a certificate permanently, he will have to accept the new one.

A better option is to generate a certificate once and use it every time we sign an application, so that whenever the user accepts our certificate permanently he won’t be bothered again.

A way to create a certificate and manually sign an application with it is explained at [Sun’s Java Documentation](http://java.sun.com/j2se/1.5.0/docs/guide/javaws/developersguide/development.html#signing).

In our case, we are using [maven](http://maven.apache.org/) as our build tool with [maven-webstart-plugin](http://mojo.codehaus.org/webstart/webstart-maven-plugin/) to automatically sign our jars. This plugin allow us to use both options.

In order to easily choose between them, we configure the plugin using properties instead of fixed values, so we can override them with profiles. Using the default values of these properties, the plugin generates a new certificate each time.

If we want to make a public build, we activate a maven profile overriding these properties to use an existent certificate used by all of our applications.

Here are some snippets of our configuration files:

### pom.xml - maven-webstart-plugin configuration

<configuration> <sign> <keystore>${gemserk.keystore}</keystore> <keypass>${gemserk.keypass}</keypass> <storepass>${gemserk.storepass}</storepass> <alias>${gemserk.alias}</alias> <!-- default values if gen is true --> <validity>3560</validity> <dnameCn>Gemserk</dnameCn> <dnameOu>Gemserk</dnameOu> <dnameO>Gemserk</dnameO> <dnameL>Montevideo</dnameL> <dnameSt>Montevideo</dnameSt> <dnameC>UY</dnameC> <verify>true</verify> <keystoreConfig> <delete>${gemserk.keystore.delete}</delete> <gen>${gemserk.keystore.gen}</gen> </keystoreConfig> </sign> </configuration>

We use our company name as a prefix for the property keys in order to have a common scope when setting the values.

### pom.xml - default values

<properties> <!-- Properties for keystore generation --> <gemserk.keystore>/tmp/keystore-gemserk</gemserk.keystore> <gemserk.keypass>m2m2m2</gemserk.keypass> <gemserk.storepass>m2m2m2</gemserk.storepass> <gemserk.alias>gemserk.com</gemserk.alias> <gemserk.keystore.delete>true</gemserk.keystore.delete> <gemserk.keystore.gen>true</gemserk.keystore.gen> </properties>

### settings.xml - profile declaration

<profile> <id>useDeploymentCertificate</id> <properties> <gemserk.keystore>/opt/gemserk-keystore</gemserk.keystore> <gemserk.keypass>password</gemserk.keypass> <gemserk.storepass>password</gemserk.storepass> <gemserk.alias>gemserk.com</gemserk.alias> <gemserk.keystore.delete>false</gemserk.keystore.delete> <gemserk.keystore.gen>false</gemserk.keystore.gen> </properties> </profile>

In order to build an application for deployment, you can activate this profile from the command line using:

```
<br />
mvn package -PuseDeploymentCertificate<br />
```


If you have any questions leave a comment.