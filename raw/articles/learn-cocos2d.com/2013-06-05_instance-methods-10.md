---
title: Instance Methods
url: http://www.learn-cocos2d.com/api-ref/KoboldTouch/6.2/cocos2d-iphone/html/interface_c_c_g_l_program/
published: '2013-06-05'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#import <CCGLProgram.h>`




|
GLuint | **_program** |
| |
GLuint | **_vertShader** |
| |
GLuint | **_fragShader** |
| |
GLint | **_uniforms** [kCCUniform_MAX] |
| |
struct { |
unsigned int **usesTime**: 1 |
| |
unsigned int **usesMVP**: 1 |
| |
unsigned int **usesMV**: 1 |
| |
unsigned int **usesRandom**: 1 |
| |
| } | **_flags** |
| |

|
struct _hashUniformEntry * | **_hashForUniforms** |
| |

[CCGLProgram](../../../../../../api-ref/KoboldTouch/6.2/cocos2d-iphone/html/interface_c_c_g_l_program/) Class that implements a glProgram

- Since
- v2.0.0

| - ((__deprecated__) __attribute__ |
|
|
|

Deprecated alias for setUniformsForBuiltins

| - (void) addAttribute: |
|
(NSString *) |
*attributeName* |
| index: |
|
(GLuint) |
*index* |
|
|
| |

It will add a new attribute to the shader

| - (NSString*) fragmentShaderLog |
|
|
|

returns the fragmentShader error log

| - (id) initWithVertexShaderByteArray: |
|
(const GLchar *) |
*vShaderByteArray* |
| fragmentShaderByteArray: |
|
(const GLchar *) |
*fShaderByteArray* |
|
|
| |

Initializes the [CCGLProgram](../../../../../../api-ref/KoboldTouch/6.2/cocos2d-iphone/html/interface_c_c_g_l_program/) with a vertex and fragment with bytes array

| - (id) initWithVertexShaderFilename: |
|
(NSString *) |
*vShaderFilename* |
| fragmentShaderFilename: |
|
(NSString *) |
*fShaderFilename* |
|
|
| |

Initializes the [CCGLProgram](../../../../../../api-ref/KoboldTouch/6.2/cocos2d-iphone/html/interface_c_c_g_l_program/) with a vertex and fragment with contents of filenames

returns the program error log

| + (id) programWithVertexShaderByteArray: |
|
(const GLchar *) |
*vShaderByteArray* |
| fragmentShaderByteArray: |
|
(const GLchar *) |
*fShaderByteArray* |
|
|
| |

creates the [CCGLProgram](../../../../../../api-ref/KoboldTouch/6.2/cocos2d-iphone/html/interface_c_c_g_l_program/) with a vertex and fragment from byte arrays

| + (id) programWithVertexShaderFilename: |
|
(NSString *) |
*vShaderFilename* |
| fragmentShaderFilename: |
|
(NSString *) |
*fShaderFilename* |
|
|
| |

creates the [CCGLProgram](../../../../../../api-ref/KoboldTouch/6.2/cocos2d-iphone/html/interface_c_c_g_l_program/) with a vertex and fragment with contents of filenames

| - (void) setUniformLocation: |
|
(GLint) |
*location* |
| with2fv: |
|
(GLfloat *) |
*floats* |
| count: |
|
(NSUInteger) |
*numberOfArrays* |
|
|
| |

calls glUniform2fv only if the values are different than the previous call for this same shader program.

| - (void) setUniformLocation: |
|
(GLint) |
*location* |
| with3fv: |
|
(GLfloat *) |
*floats* |
| count: |
|
(NSUInteger) |
*numberOfArrays* |
|
|
| |

calls glUniform3fv only if the values are different than the previous call for this same shader program.

| - (void) setUniformLocation: |
|
(GLint) |
*location* |
| with4fv: |
|
(GLvoid *) |
*floats* |
| count: |
|
(NSUInteger) |
*numberOfArrays* |
|
|
| |

calls glUniform4fv only if the values are different than the previous call for this same shader program.

| - (void) setUniformLocation: |
|
(GLint) |
*location* |
| withF1: |
|
(GLfloat) |
*f1* |
|
|
| |

calls glUniform1f only if the values are different than the previous call for this same shader program.

| - (void) setUniformLocation: |
|
(GLint) |
*location* |
| withF1: |
|
(GLfloat) |
*f1* |
| f2: |
|
(GLfloat) |
*f2* |
|
|
| |

calls glUniform2f only if the values are different than the previous call for this same shader program.

| - (void) setUniformLocation: |
|
(GLint) |
*location* |
| withF1: |
|
(GLfloat) |
*f1* |
| f2: |
|
(GLfloat) |
*f2* |
| f3: |
|
(GLfloat) |
*f3* |
|
|
| |

calls glUniform3f only if the values are different than the previous call for this same shader program.

| - (void) setUniformLocation: |
|
(GLint) |
*location* |
| withF1: |
|
(GLfloat) |
*f1* |
| f2: |
|
(GLfloat) |
*f2* |
| f3: |
|
(GLfloat) |
*f3* |
| f4: |
|
(GLfloat) |
*f4* |
|
|
| |

calls glUniform4f only if the values are different than the previous call for this same shader program.

| - (void) setUniformLocation: |
|
(GLint) |
*location* |
| withI1: |
|
(GLint) |
*i1* |
|
|
| |

calls glUniform1i only if the values are different than the previous call for this same shader program.

| - (void) setUniformLocation: |
|
(GLint) |
*location* |
| withMatrix4fv: |
|
(GLvoid *) |
*matrix_array* |
| count: |
|
(NSUInteger) |
*numberOfMatrix* |
|
|
| |

calls glUniformMatrix4fv only if the values are different than the previous call for this same shader program.

| - (void) setUniformsForBuiltins |
|
|
|

will update the builtin uniforms if they are different than the previous call for this same shader program.

| - (GLint) uniformLocationForName: |
|
(NSString *) |
*name* |
|

calls retrieves the named uniform location for this shader program.

It will create 4 uniforms:

- kCCUniformPMatrix
- kCCUniformMVMatrix
- kCCUniformMVPMatrix
- kCCUniformSampler

And it will bind "kCCUniformSampler" to 0

it will call glUseProgram()

| - (NSString*) vertexShaderLog |
|
|
|

returns the vertexShader error log


The documentation for this class was generated from the following file: