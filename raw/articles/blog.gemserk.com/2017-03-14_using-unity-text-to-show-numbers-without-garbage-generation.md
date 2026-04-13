---
title: Using Unity Text to show numbers without garbage generation
url: https://blog.gemserk.com/2017/03/14/using-unity-text-to-show-numbers-without-garbage-generation/
published: '2017-03-14'
source_blog: Gemserk
source_site: https://blog.gemserk.com/
category: game programming
fetched: '2026-04-13'
---

The idea of this post is to show different ideas and analysis on how to use Unity UI Text to show numbers without garbage generation. I need this for a framerate counter and other debug values.

# Test case

Shows a fixed digit length number in screen, regenerated each frame with a new random value.

![alt text](../../assets/f1f1bbd22937e99a.gif)


# Using Strings

Since strings are immutable in c#, common operations on strings generates new strings and hence allocates new heap memory. If you are using strings as temporary values like showing a changing number in a UI text then that memory becomes garbage. In PC that garbage could go unnoticed but not in mobile devices since that could derive in a hiccup when the garbage collector decides to collect it.

The idea with these tests is to try to use make the label work with strings without garbage generation. To detect generated garbage I am using the Unity profiler and avoiding ToString() of int, float, etc, to just calculate the cost of the string manipulation for now.

## String concatenation

String concatenation generates 30 Bytes per frame since internally String.Concat() calls String.InternallyAllocateStr().

It is not as bad as expected, it is just creating a new string with the length of the first string plus the second and then it copies their values. Obviously it becomes worse when multiple concatenations are done in secuence.

Test code:

```
Text text;
static readonly string[] numbers = { "0", "1", "2", "3", "4", "5", "6", "7", "8", "9" };
void Start () {
text = GetComponent<Text> ();
}
void Update () {
string a = numbers[UnityEngine.Random.Range(0, numbers.Length)];
string b = numbers[UnityEngine.Random.Range(0, numbers.Length)];
text.text = a + b;
}
```


## String format

Using string.Format() generates 176 Bytes per frame, internally is using String.FormatHelper + StringBuilder.ToString(). The first one creates a new StringBuilder and the second is the transform from StringBuilder to string.

Test code:

```
Text text;
static readonly string[] numbers = { "0", "1", "2", "3", "4", "5", "6", "7", "8", "9" };
void Start () {
text = GetComponent<Text> ();
}
void Update () {
string a = numbers[UnityEngine.Random.Range(0, numbers.Length)];
string b = numbers[UnityEngine.Random.Range(0, numbers.Length)];
text.text = string.Format ("{0}{1}", a, b);
}
```


## String Builder Format

Using cached StringBuilder improves the previous one a bit, it generates 86 Bytes per frame, the AppendFormat is generating garbage and then the set_Length() (used to clear the StringBuilder).

Test code:

```
Text text;
StringBuilder stringBuilder = new StringBuilder(20, 20);
static readonly string[] numbers = { "0", "1", "2", "3", "4", "5", "6", "7", "8", "9" };
void Start () {
text = GetComponent<Text> ();
stringBuilder.Length = 3;
}
-j
void Update () {
string a = numbers[UnityEngine.Random.Range(0, numbers.Length)];
string b = numbers[UnityEngine.Random.Range(0, numbers.Length)];
stringBuilder.Length = 0;
stringBuilder.AppendFormat ("{0}{1}", a, b);
text.text = stringBuilder.ToString();
}
```


Note: If I change the StringBuilder starting capacity and max capacity, the cost is the same but goes to ToString() method instead, but internally to the same method String.InternallyAllocateStr().

## String Builder only Append

Instead of using StringBuilder.AppendFormat, change to use only String.Append. This reduces the cost to only 30 Bytes per frame (the same of the first one), the only cost here is the set_Length() which internally calls String.InternallyAllocateStr().

Test code:

```
Text text;
StringBuilder stringBuilder = new StringBuilder(20, 20);
static readonly string[] numbers = { "0", "1", "2", "3", "4", "5", "6", "7", "8", "9" };
void Start () {
text = GetComponent<Text> ();
stringBuilder.Length = 3;
}
void Update () {
string a = numbers[UnityEngine.Random.Range(0, numbers.Length)];
string b = numbers[UnityEngine.Random.Range(0, numbers.Length)];
stringBuilder.Length = 0;
stringBuilder.Append (a);
stringBuilder.Append (b);
text.text = stringBuilder.ToString();
}
```


Note: Does the same behaviour if I change starting and max capacity, the cost is the same but is on ToString() instead of set_Length().

## String Builder by replacing chars

If instead of Append I replace chars directly by using [] and avoid the set_Length(), the cost is the same, 30 Bytes per frame, since the String.InternallyAllocateStr() goes to set_Chars().

Test code:

```
Text text;
StringBuilder stringBuilder = new StringBuilder(20, 20);
static readonly char[] numbers = { '0', '1', '2', '3', '4', '5', '6', '7', '8', '9' };
void Start () {
text = GetComponent<Text> ();
stringBuilder.Length = 3;
}
void Update () {
char a = numbers[UnityEngine.Random.Range(0, numbers.Length)];
char b = numbers[UnityEngine.Random.Range(0, numbers.Length)];
stringBuilder [0] = a;
stringBuilder [1] = b;
text.text = stringBuilder.ToString();
}
```


Note: Again, does the same behaviour if I change starting and max capacity, instead of set_Chars(), the cost is in ToString() method.

## String Builder, access internal string by reflection

There is a suggestion at in [this post](http://www.defectivestudios.com/devblog/garbage-free-string-unity/) to access by refleciton to _str field from StringBuilder class to avoid the cost of ToString() method.

Test code:

```
Text text;
StringBuilder stringBuilder = new StringBuilder(20, 20);
static System.Reflection.FieldInfo _sb_str_info =
typeof(StringBuilder).GetField("_str",
System.Reflection.BindingFlags.NonPublic |
System.Reflection.BindingFlags.Instance);
static readonly char[] numbers = { '0', '1', '2', '3', '4', '5', '6', '7', '8', '9' };
void Start () {
stringBuilder.Length = 3;
text = GetComponent<Text> ();
}
void Update () {
stringBuilder[0] = numbers[UnityEngine.Random.Range(0, numbers.Length)];
stringBuilder[1] = numbers[UnityEngine.Random.Range(0, numbers.Length)];
stringBuilder[2] = (char) 0;
var internalValue = _sb_str_info.GetValue (stringBuilder) as string;
text.text = internalValue;
}
```


In this case, there is no garbage at all. However, I see no change in the UI Text even though the editor shows the text field value is changing, like it is not being redrawn in screen. I suppose that could be because the string pointer is not changing and by taking a look at the [Text code from the Unity UI](https://bitbucket.org/Unity-Technologies/ui/src/0155c39e05ca5d7dcc97d9974256ef83bc122586/UnityEngine.UI/UI/Core/Text.cs?at=5.2&fileviewer=file-view-default) it is comparing with != instead of Equals… not sure here.

```
public virtual string text
{
get
{
return m_Text;
}
set
{
if (String.IsNullOrEmpty(value))
{
if (String.IsNullOrEmpty(m_Text))
return;
m_Text = "";
SetVerticesDirty();
}
else if (m_Text != value)
{
m_Text = value;
SetVerticesDirty();
SetLayoutDirty();
}
}
}
```


I tried by forcing layout and vertices dirty after updating internal string, just in case, but had no luck (sad face).

## Caching strings

Another option suggested in [this blog post](http://catlikecoding.com/unity/tutorials/frames-per-second/) is to precache strings for different numbers but that is only reasonable for a small amount of digits. I like it because it is simple and could be generated at runtime, and works well for debug numbers like FPS where the number is normally between 0 and 60.

I tried it and it works really well and generates 0 Bytes per frame.

Test code:

```
Text text;
string[] generated;
// Use this for initialization
void Start () {
text = GetComponent<Text> ();
generated = new string[100];
// should go from 0 to 99.
for (int i = 0; i < 100; i++) {
generated [i] = string.Format ("{0:00}", i);
}
}
// Update is called once per frame
void Update () {
int random = UnityEngine.Random.Range (0, generated.Length);
text.text = generated [random];
}
```


# Rendering numbers directly

One possible way to avoid all this garbage (I mean both the code and the unused memory) is to not use strings at all but to just render to the screen images for each number digit, where each digit is a different sprite.

When making TinyWarriors prototype I did a basic number rendering where I could specify the number of digits and it just created multiple Unity UI Images inside a horizontal layout.

![alt text](../../assets/5b57cc9bf3ff88b8.gif)


Test code:

```
public Image[] numbers;
// in order, like 0, 1, 2, ..., 9
public Sprite[] numberSprites;
public bool fillZero = true;
void Start()
{
SetNumber (0);
}
public void SetNumber(int number)
{
int tens = (number % 100) / 10;
int ones = (number % 10);
var tensActive = fillZero || tens != 0;
var onesActive = fillZero || number > 0;
numbers [0].gameObject.SetActive (tensActive);
numbers [1].gameObject.SetActive (onesActive);
if (tensActive)
numbers [0].sprite = numberSprites [tens];
if (onesActive)
numbers [1].sprite = numberSprites [ones];
}
public void Update()
{
int random = UnityEngine.Random.Range (0, 100);
SetNumber (random);
}
```


The code could be adapted to support more digits. When profiling it in editor there is a lot of garbage generation, around 1KB per frame, in Canvas.SendWillRendereCanvases() because it is forcing a material rebuild each time a sprite is changed. However, I tested it on devices and it doesn’t so it must be something related with the Unity editor.

# Other strategies

Other strategies include minimizing the garbage generation by reducing the text update frequency, for example, by avoiding updating the text if the number didn’t change and/or updating the text from time to time and not every frame.

# Conclusion

Since I just wanted a solution for a framerate counter (and other debug numbers) the last solutions are perfect and I believe those could even be extrapolated for other game needs, like showing the player points in an arcade game, with a bit of extra thinking.

# References

Here is a list of some articles, forum and blog posts I took a look during the tests and the post writing.

Unity memory optimizations article - [https://unity3d.com/es/learn/tutorials/temas/performance-optimization/optimizing-garbage-collection-unity-games](https://unity3d.com/es/learn/tutorials/temas/performance-optimization/optimizing-garbage-collection-unity-games)

Memory management reference - [http://www.memorymanagement.org/](http://www.memorymanagement.org/)

FPS implementation caching strings - [http://catlikecoding.com/unity/tutorials/frames-per-second/](http://catlikecoding.com/unity/tutorials/frames-per-second/)

Using reflection to set StringBuilder string to avoid garbage - [http://www.defectivestudios.com/devblog/garbage-free-string-unity/](http://www.defectivestudios.com/devblog/garbage-free-string-unity/)

FPS Asset - http://blog.codestage.ru/unity-plugins/fps/

Another FPS Asset - [https://www.assetstore.unity3d.com/en/#!/content/6513](https://www.assetstore.unity3d.com/en/#!/content/6513)

StringBuilder API - [https://msdn.microsoft.com/en-us/library/system.text.stringbuilder(v=vs.110).aspx](https://msdn.microsoft.com/en-us/library/system.text.stringbuilder(v=vs.110).aspx)

Performance tips for Unity for mobile - [https://divillysausages.com/2016/01/21/performance-tips-for-unity-2d-mobile/](https://divillysausages.com/2016/01/21/performance-tips-for-unity-2d-mobile/)

Unity UI Source code - [https://bitbucket.org/Unity-Technologies/ui](https://bitbucket.org/Unity-Technologies/ui)

Untiy Community Library - [https://github.com/UnityCommunity/UnityLibrary](https://github.com/UnityCommunity/UnityLibrary)