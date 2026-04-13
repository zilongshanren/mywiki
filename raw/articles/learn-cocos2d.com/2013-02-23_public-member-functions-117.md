---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_g_l_program/
published: '2013-02-23'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

![]() |
cocos2d-iphone
2.1
Improved Cocos2D API Reference (iOS version) for www.kobold2d.com developers
|

`#import <CCGLProgram.h>`


| - (void) addAttribute: | (NSString *) | attributeName |
|
| index: | (GLuint) | index |
|

It will add a new attribute to the shader

| - (id) initWithVertexShaderByteArray: | (const GLchar *) | vShaderByteArray |
|
| fragmentShaderByteArray: | (const GLchar *) | fShaderByteArray |
|

| - (id) initWithVertexShaderFilename: | (NSString *) | vShaderFilename |
|
| fragmentShaderFilename: | (NSString *) | fShaderFilename |
|

| - (void) setUniformLocation: | (GLint) | location |
|
| with2fv: | (GLfloat *) | floats |
|
| count: | (NSUInteger) | numberOfArrays |
|

calls glUniform2fv only if the values are different than the previous call for this same shader program.

| - (void) setUniformLocation: | (GLint) | location |
|
| with3fv: | (GLfloat *) | floats |
|
| count: | (NSUInteger) | numberOfArrays |
|

calls glUniform3fv only if the values are different than the previous call for this same shader program.

| - (void) setUniformLocation: | (GLint) | location |
|
| with4fv: | (GLvoid *) | floats |
|
| count: | (NSUInteger) | numberOfArrays |
|

calls glUniform4fv only if the values are different than the previous call for this same shader program.

| - (void) setUniformLocation: | (GLint) | location |
|
| withF1: | (GLfloat) | f1 |
|

calls glUniform1f only if the values are different than the previous call for this same shader program.

| - (void) setUniformLocation: | (GLint) | location |
|
| withF1: | (GLfloat) | f1 |
|
| f2: | (GLfloat) | f2 |
|

calls glUniform2f only if the values are different than the previous call for this same shader program.

| - (void) setUniformLocation: | (GLint) | location |
|
| withF1: | (GLfloat) | f1 |
|
| f2: | (GLfloat) | f2 |
|
| f3: | (GLfloat) | f3 |
|

calls glUniform3f only if the values are different than the previous call for this same shader program.

| - (void) setUniformLocation: | (GLint) | location |
|
| withF1: | (GLfloat) | f1 |
|
| f2: | (GLfloat) | f2 |
|
| f3: | (GLfloat) | f3 |
|
| f4: | (GLfloat) | f4 |
|

calls glUniform4f only if the values are different than the previous call for this same shader program.

| - (void) setUniformLocation: | (GLint) | location |
|
| withI1: | (GLint) | i1 |
|

calls glUniform1i only if the values are different than the previous call for this same shader program.

| - (void) setUniformLocation: | (GLint) | location |
|
| withMatrix4fv: | (GLvoid *) | matrix_array |
|
| count: | (NSUInteger) | numberOfMatrix |
|

calls glUniformMatrix4fv only if the values are different than the previous call for this same shader program.

will update the builtin uniforms if they are different than the previous call for this same shader program.

calls retrieves the named uniform location for this shader program.

It will create 4 uniforms:

And it will bind "kCCUniformSampler" to 0