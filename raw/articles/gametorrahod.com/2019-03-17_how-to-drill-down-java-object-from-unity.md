---
title: How to drill down Java object from Unity
url: https://gametorrahod.com/how-to-drill-down-java-object-from-unity/
author: Sirawat Pitaksarit
published: '2019-03-17'
source_blog: Game Torrahod
source_site: https://gametorrahod.com/
category: game programming
fetched: '2026-04-13'
---

This article is assuming you got an `AndroidJavaObject`

already from somewhere. That's your Java object that Unity had JNI-ed for you.

## You can specify <AndroidJavaObject> in various places

For example If you made a `static`

method returning `int`

waiting at Java, then you have `AndroidJavaClass`

, you might know you can use `ajc.CallStatic<int>`

. But if you are returning Java object, you can do `ajc.CallStatic<AndroidJavaObject>`

regardless of what type of object it is.

## AndroidJavaObject.Get

This is the most basic. Just specify the field's name like when you are making custom editor and trying to drill down into `SerializedObject`

. Here's some simple usage.

This is a Java `class`

.

```
public class DeviceAudioInformation
{
int nativeSamplingRate;
int optimalBufferSize;
boolean lowLatencyFeature;
boolean proAudioFeature;
AudioDeviceInfo[] outputDevices; //difficult
}
```


Meanwhile at C#, supposed you have got `AndroidJavaObject`

that you know is of type `DeviceAudioInformation`

in Java.

```
this.nativeSamplingRate = jo.Get<int>("nativeSamplingRate");
this.optimalBufferSize = jo.Get<int>("optimalBufferSize");
this.lowLatencyFeature = jo.Get<bool>("lowLatencyFeature");
this.proAudioFeature = jo.Get<bool>("proAudioFeature");
```


Yeah, `<bool>`

works for `boolean`

too. But what about that last one? `AudioDeviceInfo[]`


This `AudioDeviceInfo`

is a class from Google. Not only that, it is an array. How to go further? **My objective **is to not only iterate on them, I want to call instance method on each to extract further data. That `AudioDeviceInfo`

got `.getType()`

I want to call from C#, for example.

## How to get into array : JNI manually

First, you need to realize you can `AndroidJavaObject.Get<AndroidJavaObject>`

to get an another object, effectively drilling down recursively.

`AndroidJavaObject outputDevicesJo = jo.Get<AndroidJavaObject>("outputDevices");`


But to get into an array, we are entering the land of `IntPtr`

. So with `AndroidJavaObject`

and the like Unity is managing pointer to Java things for us. Now we have to do it.

The first step to manual JNI is `GetRawObject`

. Then we have access to various `AndroidJNI`

static helper methods, like getting array length.

```
IntPtr outputDevicesRaw = outputDevicesJo.GetRawObject();
int outputDeviceAmount = AndroidJNI.GetArrayLength(outputDevicesRaw);
```


Any method from `AndroidJNI`

can **hard crash **Unity if you are doing it wrong! Usually with SIGSEGV, as it is doing pointer gymnastic and if it lands somewhere strange then you get that.

With length, and `AndroidJNI.GetObjectArrayElement`

you can now get an another `IntPtr`

representing an item in that array. (If the items is of primitive type, you can use `GetIntArrayElement`

for example to end your journey into Java.)

```
for (int i = 0; i < outputDeviceAmount; i++)
{
IntPtr outputDevice = AndroidJNI.GetObjectArrayElement(outputDevicesRaw, i);
}
```


You can feel that after you left `AndroidJavaObject`

to `IntPtr`

, you cannot go back to `AndroidJavaObject`

anymore. It's always `IntPtr`

from this point.

## How to call an instance method on JNI-ed object

You will need a "method ID". And to get that you will need "class ID" too. This feel just like when we are doing C# reflection where we need the class type then `MethodInfo`

of the thing we want to use.

`AndroidJNI.FindClass`

can create a class ID out of thin air, but it is difficult to get the argument right. If you are up to the challenge then ...

But I am not, so an easier way is to ask the class from the object we have already got.

`IntPtr audioDeviceInfoClass = AndroidJNI.GetObjectClass(outputDevice);`


Next is the method ID. `AndroidJNI.GetMethodID`

is again, can create that out of a class ID and something something. But I have never get the argument right again lol. If you are up to the challenge again however ...

But I am not going to, so instead use `AndroidJNIHelper.GetMethodID`

. By using the helper, you can use just the method **name** and class ID.

`IntPtr getTypeMethod = AndroidJNIHelper.GetMethodID(audioDeviceInfoClass, "getType");`


Finally you can call the method with a combination of instance and method ID, just like C# reflection. In all, it would look like this.

```
for (int i = 0; i < outputDeviceAmount; i++)
{
IntPtr outputDevice = AndroidJNI.GetObjectArrayElement(outputDevicesRaw, i);
IntPtr audioDeviceInfoClass = AndroidJNI.GetObjectClass(outputDevice);
IntPtr getTypeMethod = AndroidJNIHelper.GetMethodID(audioDeviceInfoClass, "getType");
int type = AndroidJNI.CallIntMethod(outputDevice, getTypeMethod, new jvalue[] { });
this.outputDevices[i] = (AndroidAudioDeviceType) type;
}
```


I have successfully iterate over an array of Java objects, and moreover call an instance method on each of them and keep the return value. I think this is enough to drill down any kind of Java object already.