---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_identifiable/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <CC3Identifiable.h>`


| id |
|

This is a base subclass for any class that uses tags or names to identify individual instances.

Instances can be initialized with either or both a tag and a name. Instances initialized without an explcit tag will have a unique tag automatically generated and assigned.

You can assign your own data to instances of [CC3Identifiable](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_identifiable/) or its subclasses through the userData property.

When overriding initialization, subclasses typically need only override the most generic initializer, initWithTag:withName:.

| id CC3Identifiable::copy | ( | ) | ` [virtual]` |

Returns a newly allocated (retained) copy of this instance.

The new copy will have the same name as this instance, but will have a unique tag.

The returned instance is retained. It is the responsiblity of the caller to manage the lifecycle of the returned instance and perform the corresponding invocation of the release method at the appropriate time.

This copy operation is a deep copy. Copies of most of the content of the original will be created as well. For structural subclasses, such as [CC3Node](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_node/), copies will be made of each structual element (eg- child nodes). Some exceptions are made. For instance, copies are generally not made for fixed, voluminous content such as mesh data. In addition, subclasses may excuse themselves from being copied through the shouldIncludeInDeepCopy property.

This copy operation is a deep copy. Copies of most of the content of the original will be created as well. For structural subclasses, such as [CC3Node](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_node/), copies will be made of each structual element (eg- child nodes). Some exceptions are made. For instance, copies are generally not made for fixed, voluminous content such as mesh data. In addition, subclasses may excuse themselves from being copied through the shouldIncludeInDeepCopy property.

The copy... methods may often be used to duplicate an instance many times, to create large number of similar instances to populate a game. To help you verify that you are correctly releasing and deallocating all these copies, you can use the instanceCount class method to get a current count of the total number of instances of all subclasses of [CC3Identifiable](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_identifiable/),

Subclasses that extend copying should not override this method, but should override the populateFrom: method instead.

Implemented in [CC3Node](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_node/#a7bda04af22d4853e65cbb1b2a7be0097).

Invoked automatically when this instance has been created as a copy of the specified instance.

In this abstract class, this method does nothing. You can override this method by creating extension categories for the concrete subclasses ([CC3Node](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_node/), [CC3Mesh](http://www.learn-cocos2d.com/), [CC3Material](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_material/), [CC3Texture](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_texture/), etc.), to copy the userData referenced in the userData property of the specified instance to the userData property of this instance.

| id CC3Identifiable::copyWithName: | ( | NSString * | aName | ) | ` [virtual]` |

Returns a newly allocated (retained) copy of this instance.

The new copy will have its name set to the specified name, and will have a unique tag.

The returned instance is retained. It is the responsiblity of the caller to manage the lifecycle of the returned instance and perform the corresponding invocation of the release method at the appropriate time.

This copy operation is a deep copy. Copies of most of the content of the original will be created as well. For structural subclasses, such as [CC3Node](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_node/), copies will be made of each structual element (eg- child nodes). Some exceptions are made. For instance, copies are generally not made for fixed, voluminous content such as mesh data. In addition, subclasses may excuse themselves from being copied through the shouldIncludeInDeepCopy property.

The copy... methods may often be used to duplicate an instance many times, to create large number of similar instances to populate a game. To help you verify that you are correctly releasing and deallocating all these copies, you can use the instanceCount class method to get a current count of the total number of instances of all subclasses of [CC3Identifiable](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_identifiable/),

Subclasses that extend copying should not override this method, but should override the populateFrom: method instead.

Implemented in [CC3Node](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_node/#aec0fbbf1cbbbf174ec68f2322856db97).

| id CC3Identifiable::copyWithName:asClass: | ( | NSString * | aName, |
| [asClass] Class | aClass |
||
| ) | ` [virtual]` |

Returns a newly allocated (retained) copy of this instance.

The new copy will be an instance of the specified class, will have its name set to the specified name, and will have a unique tag.

Care should be taken when choosing the class to be instantiated. If the class is different than that of this instance, the populateFrom: method of that class must be compatible with the contents of this instance.

The returned instance is retained. It is the responsiblity of the caller to manage the lifecycle of the returned instance and perform the corresponding invocation of the release method at the appropriate time.

This copy operation is a deep copy. Copies of most of the content of the original will be created as well. For structural subclasses, such as [CC3Node](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_node/), copies will be made of each structual element (eg- child nodes). Some exceptions are made. For instance, copies are generally not made for fixed, voluminous content such as mesh data. In addition, subclasses may excuse themselves from being copied through the shouldIncludeInDeepCopy property.

The copy... methods may often be used to duplicate an instance many times, to create large number of similar instances to populate a game. To help you verify that you are correctly releasing and deallocating all these copies, you can use the instanceCount class method to get a current count of the total number of instances of all subclasses of [CC3Identifiable](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_identifiable/),

Subclasses that extend copying should not override this method, but should override the populateFrom: method instead.

| id CC3Identifiable::copyWithZone:withName: | ( | NSZone * | zone, |
| [withName] NSString * | aName |
||
| ) | ` [virtual]` |

Returns a newly allocated (retained) copy of this instance.

The new copy will have its name set to the specified name, and will have a unique tag.

The returned instance is retained. It is the responsiblity of the caller to manage the lifecycle of the returned instance and perform the corresponding invocation of the release method at the appropriate time.

This copy operation is a deep copy. Copies of most of the content of the original will be created as well. For structural subclasses, such as [CC3Node](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_node/), copies will be made of each structual element (eg- child nodes). Some exceptions are made. For instance, copies are generally not made for fixed, voluminous content such as mesh data. In addition, subclasses may excuse themselves from being copied through the shouldIncludeInDeepCopy property.

The copy... methods may often be used to duplicate an instance many times, to create large number of similar instances to populate a game. To help you verify that you are correctly releasing and deallocating all these copies, you can use the instanceCount class method to get a current count of the total number of instances of all subclasses of [CC3Identifiable](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_identifiable/),

Subclasses that extend copying should not override this method, but should override the populateFrom: method instead.

| id CC3Identifiable::copyWithZone:withName:asClass: | ( | NSZone * | zone, |
| [withName] NSString * | aName, |
||
| [asClass] Class | aClass |
||
| ) | ` [virtual]` |

Returns a newly allocated (retained) copy of this instance.

The new copy will be an instance of the specified class, will have its name set to the specified name, and will have a unique tag.

Care should be taken when choosing the class to be instantiated. If the class is different than that of this instance, the populateFrom: method of that class must be compatible with the contents of this instance.

The returned instance is retained. It is the responsiblity of the caller to manage the lifecycle of the returned instance and perform the corresponding invocation of the release method at the appropriate time.

This copy operation is a deep copy. Copies of most of the content of the original will be created as well. For structural subclasses, such as [CC3Node](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_node/), copies will be made of each structual element (eg- child nodes). Some exceptions are made. For instance, copies are generally not made for fixed, voluminous content such as mesh data. In addition, subclasses may excuse themselves from being copied through the shouldIncludeInDeepCopy property.

The copy... methods may often be used to duplicate an instance many times, to create large number of similar instances to populate a game. To help you verify that you are correctly releasing and deallocating all these copies, you can use the instanceCount class method to get a current count of the total number of instances of all subclasses of [CC3Identifiable](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_identifiable/),

Subclasses that extend copying should not override this method, but should override the populateFrom: method instead.

| NSString* CC3Identifiable::fullDescription | ( | ) | ` [virtual]` |

Returns a string containing a more complete description of this object.

This implementation simply invokes the description method. Subclasses with more substantial content can override to provide much more information.

| id CC3Identifiable::init | ( | ) | ` [virtual]` |

| id
|

` [virtual]`

Initializes this instance from the data of this type at the specified index within the specified POD resource.

| void CC3Identifiable::initUserData | ( | ) | ` [virtual]` |

Invoked automatically from the init* family of methods to initialize the userData reference.

In this abstract class, this method does nothing. You can override this method by creating extension categories for the concrete subclasses, ([CC3Node](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_node/), [CC3Mesh](http://www.learn-cocos2d.com/), [CC3Material](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_material/), [CC3Texture](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_texture/), etc.), if the userData can be initialized and retained in self-contained manner.

| id CC3Identifiable::initWithName: | ( | NSString * | aName | ) | ` [virtual]` |

| id CC3Identifiable::initWithTag: | ( | GLuint | aTag | ) | ` [virtual]` |

| id CC3Identifiable::initWithTag:withName: | ( | GLuint | aTag, |
| [withName] NSString * | aName |
||
| ) | ` [virtual]` |

| GLint CC3Identifiable::instanceCount | ( | ) | ` [static, virtual]` |

Indicates the total number of active instances, over all subclasses, that have been allocated and initialized, but not deallocated.

This can be useful when creating hordes of 3D objects, to verify that your application is properly deallocating them again when you are done with them.

| GLuint CC3Identifiable::nextTag | ( | ) | ` [virtual]` |

Returns a unique tag value to identify instances.

This value is unique across all instances of all subclasses. The initial value returned will be one, and subsequent calls will increment the value retuned on each call. The starting value can be reset back to one via the resetTagAllocation method.

| void CC3Identifiable::releaseUserData | ( | ) | ` [virtual]` |

Invoked automatically from the dealloc method to release or dispose of the data referenced in the userData property.

In this abstract class, this method does nothing. You can override this method by creating extension categories for the concrete subclasses ([CC3Node](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_node/), [CC3Mesh](http://www.learn-cocos2d.com/), [CC3Material](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_material/), [CC3Texture](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_texture/), etc.), to release or dispose of the data referenced in the userData property.

| void CC3Identifiable::resetTagAllocation | ( | ) | ` [static, virtual]` |

Resets the allocation of new tags to resume at one again.

NSString * CC3Identifiable::name` [read, write, retain]` |

An arbitrary name for this node.

It is not necessary to give all identifiable objects a name, but can be useful for retrieving objects at runtime, and for identifying objects during development. Names need not be unique, are not automatically assigned, and leaving the name as nil is acceptable.

The index of this object in the POD resource data.

This generally means the podIndex'th type of object of the class.

BOOL CC3Identifiable::shouldIncludeInDeepCopy` [read, assign]` |

Returns whether this instance should be included in a deep copy.

This method simply returns YES by default, and in most cases this is sufficient. However, for some structural subclasses (notably subclasses of [CC3Node](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_node/)) it may be desirable to not copy some components.

This property is not universally automatically applied or honoured. It is up to the invoker and invokee to agree on when to make use of this property.

GLuint CC3Identifiable::tag` [read, write, assign]` |

An arbitrary identification.

Useful for keeping track of instances. Unique tags are not explicitly required, but are highly recommended. In most cases, it is best to just let the tag be assigned automatically by using an initializer that does not explicitly set the tag.

void * CC3Identifiable::userData` [read, write, assign]` |

Application-specific data associated with this object.

You can use this property to add any data you want to an instance of [CC3Identifiable](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_identifiable/) or its concrete subclasses ([CC3Node](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_node/), [CC3Mesh](http://www.learn-cocos2d.com/), [CC3Material](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_material/), [CC3Texture](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_texture/), etc.). Since this is a generic pointer, you can store any type of data, such as an object, structure, primitive, or array.

This data is not retained by this instance, and is not managed by the cocos3d framework. It is the responsibility of the application to manage the allocation, retention, and disposal of this data.

To assist in managing this data, the methods initUserData and releaseUserData are invoked automatically during the initialization and deallocation of each instance of this class. In this abstract class, these methods do nothing, but, if appropriate, you can override these methods by adding extention categories to the concrete subclasses of [CC3Identifiable](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_identifiable/), ([CC3Node](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_node/), [CC3Mesh](http://www.learn-cocos2d.com/), [CC3Material](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_material/), [CC3Texture](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_texture/), etc.), to create, retain and dispose of the data.

Similarly, when copying instances of [CC3Identifiable](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_identifiable/) and its subclasses, the copyUserDataFrom: method is invoked in the new copy so that it can copy the data in the original instance to the new instance copy. In this abstract class, the copyUserDataFrom: method does nothing, but, if appropriate, you can override the method by adding extention categories to the concrete subclasses of [CC3Identifiable](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_identifiable/), ([CC3Node](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_node/), [CC3Mesh](http://www.learn-cocos2d.com/), [CC3Material](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_material/), [CC3Texture](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_texture/), etc.), to copy whatever data you have in the userData property.

In this abstract class, this property is not retained. You can override the accessor methods by creating extension categories for the concrete subclasses, ([CC3Node](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_node/), [CC3Mesh](http://www.learn-cocos2d.com/), [CC3Material](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_material/), [CC3Texture](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_texture/), etc.), in order to retain the data if appropriate.