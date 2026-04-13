---
title: Rust Game Series - Part 14 - DDS Parser | Jendrik Illner
url: https://www.jendrikillner.com/post/rust-game-part-14/
author: Jendrik Illner
published: '2020-09-15'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

This is the first part about the texture loading implementation for the Match 3 game.

In this part, I am going to cover

- Error Handling
- Unit testing
- Integration Testing
- Development Only Dependencies
- Parsing binary files

Lots to talk about, so let us get started.

## Overview

Textures formats such as png and jpg are aimed at reducing size on disk. But GPUs cannot read these directly, and therefore texture data needs to be decompressed before they can be read.

Block compressed formats allow texture data to remain compressed at all times. This reduces memory usage and reduces memory bandwidth when accessing the textures; an example of a block compressed format is .dds

The process for loading DDS files can be broken down into 4 high-level steps.

- Parse the DDS file and unpack the texture data
- Create a D3D11 texture from the data parsed information
- Update the shaders to enable reading from textures
- Bind the texture to the pipeline

This blog post will only cover step 1 and 2

The .dds format is fundamentally quite simple, but the number of variations and exceptions makes it a tricky format to parse in practice.

For this example parser implementation, I will restrict myself to only what is required for the time being.

- 2D Textures only
- BC1 to BC7 + uncompressed RGBA8

To learn more about the different BC formats, I recommend this article [Understanding BCn Texture Compression Formats](https://web.archive.org/web/20200624115519/http://www.reedbeta.com/blog/understanding-bcn-texture-compression-formats/)

## Architecture

The DDS parser receives a binary blob of data, parses the necessary information, and fills out the D3D11 descriptors.

In Rust function terms, it looks like this:

```
pub struct ParsedTextureData {
pub desc: D3D11_TEXTURE2D_DESC,
pub subresources_data: Vec<D3D11_SUBRESOURCE_DATA>,
}
pub fn parse_dds_header(src_data: &[u8]) -> Result<ParsedTextureData, DdsParserError>
```


The function returns a `Result<ParsedTextureData, DdsParserError>`


# Error handling

I tend to think about error handling in two distinct categories.

- Unexpected Failure
- Expected Failure

I prefer the program to [panic](https://doc.rust-lang.org/std/macro.panic.html) and abandon the application for unexpected failure. These kinds of failures happen if the application enters a state that was never expected to happen.

I prefer to panic early so that the application crashes as soon as an invalid state is detected instead of causing more subtle and hard to debug problems.

For expected failure cases, Rust offers an excellent method build around [Result](https://doc.rust-lang.org/std/result/). This type is used to represent a return value that can either contain a success or failure value.

`parse_dds_header`

will return a DdsParserError in case of failure, and only if parsing was successful, the ParsedTextureData is returned.

Currently, the parser returns the following error codes.

```
pub enum DdsParserError {
InvalidHeader(& 'static str),
InvalidFlags(& 'static str),
FormatNotSupported,
ImageSizeNotMultipleOf4,
}
```


In my opinion, each function that can fail should return a unique error enum that lists all possible failure cases. This way, it’s apparent to the caller what kind of failures can be expected and can decide how to handle each possibility.

If you would like to learn more about Error Handling in Rust, look at this talk [RustConf 2020 - Error handling Isn’t All About Errors by Jane Lusby](https://www.youtube.com/watch?v=rAF8mLI0naQ).

Great talk; I disagree with Jane on the use of [non_exhaustive](https://doc.rust-lang.org/reference/attributes/type_system.html#the-non_exhaustive-attribute) however.

Rust enums need to be exhaustively matched by default (meaning all possible cases need to be handled). Therefore each addition of a new valie will also be a breaking API change.

If you have a custom error enum for each function, then introducing a new error value means the function has a new Expected Failure case that didn’t exist before.

This is a breaking API change and should force all users to think about how to handle the new failure case.

`non_exhaustive`

hides the introduction of a new failure from the user.
And a user might only detect that a new error was introduced when the error happens at runtime instead of seeing the new unhandled error case at compile time.

I don’t think that’s the right decision but decide that for yourself.

### Testing

We had a look at the API and how to handle different failure cases. The API surface is minimal and makes for a great candidate to show two types of testing supported by Cargo.

- Unit Testing
- Integration Testing

Unit testing is a testing level where individual components of an application are tested in isolation with optimally no dependencies on other components.

Integration tests verify that the interactions of two or more components achieve the expected goal.

For this parser, the tests are as follows:

- Unit Test: validate that the expected information is returned
- Integration test: validate that the returned information also creates valid D3D11 texture

#### Unit Testing

Adding a Unit Tests to a Rust project is simple.

Just add the following code to any rust file, and you got yourself a Unit Test.

```
pub fn add_two(a: i32) -> i32 {
a + 2
}
#[cfg(test)]
mod tests {
use super::*;
#[test]
fn it_adds_two() {
assert_eq!(4, add_two(2));
}
}
```


Running `cargo test`

will run all unit tests found in the current project.

The same concept in a more complete example from the parser is below.

```
#[test]
fn validate_texture_header_black_4x4_bc1() {
let texture_header_ref = D3D11_TEXTURE2D_DESC {
...
};
let texture_data_desc = D3D11_SUBRESOURCE_DATA {
pSysMem: std::ptr::null_mut(), // can't validate this, will be pointing into the dynamic memory adresse
SysMemPitch: 8, // 4x4 texture = 1 BC1 block = 8 bytes
SysMemSlicePitch: 8, // 1 block
};
let texture_load_result = parse_dds_header(paintnet::BLACK_4X4_BC1);
assert_eq!(texture_load_result.is_ok(), true);
let texture_header = texture_load_result.unwrap();
validate_texture_header(&texture_header_ref, &texture_header.desc);
// should contain one subresource
assert_eq!(texture_header.subresources_data.len(), 1);
assert_eq!(
texture_data_desc.SysMemPitch,
texture_header.subresources_data[0].SysMemPitch
);
assert_eq!(
texture_data_desc.SysMemSlicePitch,
texture_header.subresources_data[0].SysMemSlicePitch
);
}
```


Firstly we define what values the D3D11 header is supposed to contain.
We then use several `assert_eq`

to validate that the parser’s values are what we expected.

One part that stands out is how the texture parsing is called.

```
let texture_load_result = parse_dds_header(paintnet::BLACK_4X4_BC1);
```


You might remember that the function accepts a slice to binary data as a parameter. But how do we get access to the data that contains the texture?

One option would be to load the file from disk. However, loading from disk can fail for several reasons. Instead of introducing opportunities for random failures, I am embedding the file directly into the unit test executable.

Rust provides a very convenient macro for this. This macro takes any file (path is relative to the current file) and will embed the binary data directly into the executable.

```
// embed the data we will be testing against
mod paintnet {
pub static BLACK_4X4_BC1: &'static [u8; 136] =
include_bytes!("../tests/data/paintnet/black_4x4_bc1.dds");
pub static BLACK_4X4_MIPS_BC1: &'static [u8; 152] =
include_bytes!("../tests/data/paintnet/black_4x4_mips_bc1.dds");
}
```


This is ideal for small binary files, such as the texture data used for the unit tests.

For the parser, I only used a unit test to get the first parsing logic verified but did all other testing using integration testing.

### Integration Testing

The integration tests will verify that parsed texture information will create a valid texture. Valid in this context means that the D3D11 debug layer will not generate any warnings or errors.

It does not mean that the texture actually looks like we expect it. For example, if we are expecting all pixels to be black, but for some reason, they are red, these integration tests will not fail.

From a code perspective, integration tests look the same:

```
#[test]
fn load_and_create_black_4x4_bc1() {
test_texture_load_and_creation2( paintnet::BLACK_4X4_BC1 );
}
#[test]
fn load_and_create_black_4x4_mips_bc1() {
test_texture_load_and_creation2( paintnet::BLACK_4X4_MIPS_BC1 );
}
```


Integration tests are located in a separate directory from the code they are testing.

```
dds_parser
- src/
dds_parser_lib.lib // Unit tests
- tests/
dds_parser_integration_tests.lib // Integration tests
```


This also means integration tests are located in a separate module and are only allowed to call the public interface.

All integration tests for the parser call a single function with different binary data, as you saw above. The function implementation looks like below:

```
fn test_texture_load_and_creation(data: &[u8]) {
let debug_device = true;
let graphics_layer: GraphicsDeviceLayer =
graphics_device::create_device_graphics_layer_headless(debug_device).unwrap();
// parse the header
let texture_load_result = dds_parser::parse_dds_header(&data).unwrap();
let (_texture, _texture_view) = graphics_device::create_texture(
&graphics_layer.device,
texture_load_result.desc,
texture_load_result.subresources_data,
)
.unwrap();
}
```


It’s a 3 step process.

- Create the Graphics layer
- Parse the DDS header information
- pass the parsed data into the
`create_texture`

function

Every step is followed by an unwrap() call; this will ensure that if any of the steps fails, the integration test will also fail.

One beneficial aspect of the Rust testing framework is that we can also test for expected failures:

```
#[test]
#[should_panic(expected = r#"called `Result::unwrap()` on an `Err` value: InvalidDimensions"#)]
fn load_and_create_black_5x4_bc1() {
test_texture_load_and_creation("paintnet/white_5x4_bc1.dds");
}
```


Here I tell Cargo that this test is expected to panic and that the panic message should contain a specified text. This is very useful to make sure that invalid data triggers the Expected Failure case you expected to happen.

I am verifying that the parser correctly detects textures that are not a multiple of the block size.

You might have noticed one problem with the integration test setup in terms of library dependencies.
The integration tests are part of the `dds_parser`

crate, and we are using the `graphics_device`

crate for the integration tests.

I don’t really want to introduce a dependency on the `graphics_device`

crate just to use it for integration tests.

But Cargo has a trick up its sleeve to deal with this situation.

## Development Only Dependencies

These kinds of dependencies are used to specify dependencies that are only required for tests or benchmarks.

These are added to the cargo.toml, just like other dependencies.

```
[dev-dependencies]
graphics_device = { path = "../graphics_device" }
```


The difference is that these dependencies are not propagated to users of a crate.

In this case, using the `dds_parser`

will not create a dependency on `graphics_device`

.
But all tests still have full access to all functionality of the `graphics_device`

crate just as if it would be a regular dependency.

## Reading binary files

After looking at testing, error handling strategy, and testing dependencies, we miss one crucial part. How to actually parse a .dds file.

This process is quite long; please have a look at `dds_parser\src\dds_parser_lib.rs`

in the code provided on GitHub to see all the details.

I will provide an introduction to how I decided to approach parsing binary files using Rust without crates.

The DDS format is broken into distinct parts.

- DWORD with value “DDS ” 0x20534444
- DDS_HEADER
- optionally: DDS_HEADER_DXT10
- BYTES (main surface data)

The file starts with a DWORD that contains a “magic value”. This concept can be found in many file formats and is an easy way to detect if the data provided could be a valid DDS file.

A DWORD refers to a double word, or also known as 32-bit unsigned integer.

This is the start of the parser:

```
pub fn parse_dds_header(src_data: &[u8]) -> Result<ParsedTextureData, DdsParserError> {
// a valid DDS file needs at least 128 bytes to store the DDS dword and DDS_HEADER
// if the file is smaller it cannot be a valid file
if src_data.len() < 128 {
return Err(DdsParserError::InvalidHeader("smaller than 128 bytes"));
}
let mut file_cursor = 0;
// DDS files are expected to start with "DDS " = 0x20534444
// if this is not the case the file is not a valid DDS file
// try_into could panic if src_data is too short
// but we checked the data length before
let dw_magic: u32 =
u32::from_le_bytes(src_data[file_cursor..(file_cursor + 4)].try_into().unwrap());
file_cursor += 4;
if dw_magic != 0x2053_4444 {
return Err(DdsParserError::InvalidHeader(
"file is missing DDS DWORD at start of the file",
));
}
```


First, we validate that the file is large enough to store the minimum information required. If the file is smaller, it cannot be a valid DDS file, and we return an error code to indicate this.

Then we parse the magic dword that is expected to be at the start of the file. Rust provides a few functions to enable parsing for primitive types such as u32.

```
from_le_bytes(bytes: [u8; 4]) -> u32
```


This function accepts a slice of 4 bytes and returns a u32.
The _le refers to little-endian byte order as opposed to big-endian.
Refer to [for the difference](https://web.archive.org/web/20200501222745/https://chortle.ccsu.edu/AssemblyTutorial/Chapter-15/ass15_3.html)

But how do we convert a slice of unknown length into a fixed-length slice? The way to achieve this might not be immediately apparent.

The solution is this:

```
let u32slice : [u8;4] = src_data[0..4].try_into().unwrap()
```


But how did I end up with this?

The first apparent thing to try would be

```
let u32slice : [u8;4] = src_data[0..4]
```


I did this and expected it to work because clearly, we know these are 4 entries, and the compiler should figure this out too.

So let us try this and see what the compiler thinks:

```
1>49 | let u32slice : [u8;4] = src_data[0..4];
1> | ------ ^^^^^^^^^^^^^^ expected array `[u8; 4]`, found slice `[u8]`
```


But it’s not so easy. This will only work if we are 100% sure that the slice is at least 4 u8 entries long.
We cannot guarantee this since `src_data: &[u8]`

is of unknown length.

So what can we do instead?

```
1>49 | let u32slice : [u8;4] = src_data[0..4].try_into();
1> | ------ ^^^^^^^^^^^^^^^^^^^^^^^^^ expected array `[u8; 4]`, found enum `std::result::Result`
```


Ok, we are getting closer. TryInto is a trait that allows types to be converted into another type. These support conversions that might fail or could be expensive.

As you can see above, try_into returns a Result. So we should handle the failure condition.

```
let u32slice : [u8;4] = src_data[0..4].try_into().unwrap()
```


In the parser, I use unwrap() on the result. This call could fail if the slice doesn’t contain enough bytes for the requested range. But we covered this case with an earlier if that validates that we have at least 128 bytes of data.

With this slice, we can now parse the data.

```
let dw_magic: u32 =
u32::from_le_bytes(u32slice);
if dw_magic != 0x2053_4444 {
return Err(DdsParserError::InvalidHeader);
}
```


And with that, we have done all the necessary parsing steps to parse a u32 value from a binary file.

If you had a look at the code on GitHub, you would see the line looks slightly different.

```
src_data[file_cursor..(file_cursor + 4)].try_into().unwrap()
```


What is file_cursor?

I tend to use a single variable to store how many bytes have been parsed and make all parsing operations relative to the file’s progress.

This makes the parser easier to read, and it also makes it possible to do a quick sanity check at the end of the parser.

```
// all data needs to be used, otherwise therer was a problem with parsing
assert!(file_cursor == src_data.len());
```


If we reached the parsing logic’s end, we should have parsed each byte in the file. If not, there might be a bug in the parsing logic, or the file contains sections that we didn’t process.

This is an unexpected failure case, better to fail early, and let us know we have a problem with the parser logic. If you expect your parser to be used on untrusted data, you might want to make this an expected failure case instead.

With this, we have seen the core of the parsing logic; the same idea is applied to many more entries in the DDS file.

If you are interested in the DDS specifics, look at the [Github code](https://github.com/jendrikillner/RustMatch3/releases/tag/rust-game-part-14), and if you have any questions, feel free to comment below or send me a message.

## Next Part

It’s all good, we seem to be able to load D3D11 textures, but we will not be sure that they actually work until we have seen them.

So how do we render the textures on the screen?

That’s a topic for the next post :)

The code is available on [GitHub](https://github.com/jendrikillner/RustMatch3/releases/tag/rust-game-part-14)