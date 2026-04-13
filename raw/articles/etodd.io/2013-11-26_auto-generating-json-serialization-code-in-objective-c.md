---
title: Auto-generating JSON serialization code in Objective C
url: https://etodd.io/2013/11/26/auto-generating-json-serialization-code-in-objective-c/
published: '2013-11-26'
source_blog: Evan Todd
source_site: https://etodd.io/
category: game programming
fetched: '2026-04-13'
---

# Auto-generating JSON serialization code in Objective C

I wrote this article for the [Sidebolt company blog](http://www.sidebolt.com/auto-generating-json-serialization-code-in-objective-c/). Reposting it here for your reading pleasure!

Our latest game [Skyward Slots](http://skywardslots.com) makes extensive use of JSON. We send Gigabytes of it flying back and forth haphazardly between client and server over a WebSocket connection. At first, we wrote code by hand to pack and unpack each message. Later on we decided that life is too short for that.

In the beginning, we just dove into the JSON right where we needed it.

```
-(void) updateUserInterface:(NSDictionary*)message
{
topBar.coinsLabel.string = [[message objectForKey:@"coins"] stringValue];
}
```


This isn't so great because it's a) quite verbose and b) difficult to change. If we change the name of the "coins" parameter to "cash", we'll have to search-and-replace and hope that we get every instance. There's no way to tell if we missed one; it will fail silently.

Our solution was to write a layer of model objects which process JSON dictionaries and expose the data via properties.

```
@interface Product : NSObject
@property BOOL scalable;
@property (strong) NSString* productType;
@property int quantity;
@property (strong) SKProduct* skProduct;
-(id)initWithDictionary:(NSDictionary*)dic;
@end
@implementation Product
-(id)initWithDictionary:(NSDictionary *)dic
{
if (self = [super init])
{
self.scalable = [[dic objectForKey:@"scalable"] boolValue];
self.productType = [dic objectForKey:@"productType"];
self.quantity = [[dic objectForKey:@"quantity"] intValue];
}
return self;
}
```


Now if we change a property name, we'll get a bunch of compiler errors. This technique also gets us code completion, which is great.

The only downside is, writing these model classes gets old FAST. And they're so repetitive and simple, you'd think we could automate it somehow!

I sat down and wrote a gob of macros to do just that. Now we have one header file with all of our models, which now look like this:

```
SBStruct(HSLoginResult)
SBProperty(NSNumber, id)
SBProperty(NSString, token)
SBProperty(NSString, updateURL)
SBEndStruct(HSLoginResult)
```


This generates an Objective C class which can be used like so:

```
HSLoginResult* result = [HSLoginResult decode:dictionary];
NSLog(@"%d", result.id.intValue);
```


Much better! The best part is, we still have code completion. We can also nest these structures.

So how does it work?

Here's the SBStruct and SBProxy macros:

```
#define SBStruct(name) \
@interface name : SBStructure
#define SBProperty(type, name) \
@property (strong, nonatomic) type* name;
#define SBEndStruct(name) @end
```


This generates a valid class definition with all the right properties. Then in the implementation file, we include our definitions again and set up the macros to generate the actual packing/unpacking code:

```
#define SBStruct(name) \
@implementation name (Decode) \
+(id) decode:(id)dict \
{ \
if (dict == [NSNull null]) \
return nil; \
name* instance = [name new];
#define SBProperty(type, name) \
instance.name = [type decode:[dict objectForKey:@#name]];
#define SBEndStruct(name) \
return instance; \
} \
@end
```


The only thing left to do is to add categories to the basic data types to make them implement the decode: method, like so:

```
@implementation NSNumber (Decode)
+(NSNumber*) decode:(id)value
{
return value == [NSNull null] ? nil : (NSNumber*)value;
}
@end
// and so on...
```


If you're like me you may decide to go crazy with this. Our macros actually auto-generate methods that send messages and trigger block callbacks for received messages. They also generate a list class to go with each model class to make it easy to encode and decode NSArrays. Go forth and automate!