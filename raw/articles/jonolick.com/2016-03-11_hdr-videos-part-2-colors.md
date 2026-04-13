---
title: 'HDR Videos Part 2: Colors'
url: https://www.jonolick.com/home/hdr-videos-part-2-colors
author: Blaine Foster link
published: '2016-03-11'
source_blog: Jon Olick - Home
source_site: https://www.jonolick.com/home
category: graphics
fetched: '2026-04-13'
---

|
In this series of blog posts, I'm going to cover various parts of the research and development behind Bink 2 HDR.
There are 4 different color standards, namely Rec.601, Rec.709, Rec.2020, and Rec.2100. Rec.601, Rec.709 and Rec.2020 all have different definitions of R,G and B. Rec.2020 notably defines a "wide color gamut". Rec.2100 has the same color gamut as Rec.2020, but defines Percentual Quantiers (PQ) and Hybrid Log-Gamma (HLG) for UHDR. First, when working with HDR color spaces, be sure to use linear RGB inputs. No sRGB, Adobe RGB, etc...What about if your loading a floating point format like EXR or HDR? These are both linear, so no conversion *should* be necessary. There are three color spaces in Rec.2100.
## Non-Constant Luminance (NCL) YCbCr
This color space is very similar to LDR YCbCr after tone mapping from 10k Luma to LDR range.
The code for converting to/from linear RGB to NCL Y'Cb'Cr' is as follows... void RGBtoYCbCr2100(float *rgbx, float *ycbcr, int num) { for(int i = 0; i < num*4; i+=4) { float r = rgbx[i+0], g = rgbx[i+1], b = rgbx[i+2]; r = smpte2084_encodef(r); g = smpte2084_encodef(g); b = smpte2084_encodef(b); ycbcr[i+0] = 0.2627f*r + 0.6780f*g + 0.0593f*b; ycbcr[i+1] = -0.13963f*r - 0.36037f*g + 0.5f*b; ycbcr[i+2] = 0.5f*r - 0.45979f*g - 0.040214f*b; ycbcr[i+3] = rgbx[i+3]; } } void YCbCrtoRGB2100(float *ycbcrx, float *rgbx, int num) { for(int i = 0; i < num*4; i+=4) { float Y = ycbcrx[i+0], Cb = ycbcrx[i+1], Cr = ycbcrx[i+2]; float r = Y + 1.4746f*Cr; float g = Y - 0.164552f*Cb - 0.571352f*Cr; float b = Y + 1.8814f*Cb; r = smpte2084_decodef(r); g = smpte2084_decodef(g); b = smpte2084_decodef(b); rgbx[i+0] = r; rgbx[i+1] = g; rgbx[i+2] = b; rgbx[i+3] = ycbcrx[i+3]; } }
We can display these color spaces using LDR images via tone mapping - as shown below.
## Constant Luminance ICtCp
Rec.2100, the latest standard, defines a new color space for HDR which improves on the NCL & CL YCbCr called ICtCp.
The code for converting from Rec.2020 linear RGB to ICtCp is as follows... void RGBtoICtCp(float *rgbx, float *ictcpx, int num) { for(int i = 0; i < num*4; i+=4) { double r = rgbx[i+0], g = rgbx[i+1], b = rgbx[i+2]; double L = 0.4121093750000000*r + 0.5239257812500000*g + 0.0639648437500000*b; double M = 0.1667480468750000*r + 0.7204589843750000*g + 0.1127929687500000*b; double S = 0.0241699218750000*r + 0.0754394531250000*g + 0.9003906250000000*b; L = smpte2084_encodef(L); M = smpte2084_encodef(M); S = smpte2084_encodef(S); ictcpx[i+0] = 0.5*L + 0.5*M; ictcpx[i+1] = 1.613769531250000*L - 3.323486328125000*M + 1.709716796875000*S; ictcpx[i+2] = 4.378173828125000*L - 4.245605468750000*M - 0.132568359375000*S; ictcpx[i+3] = rgbx[i+3]; } } The inverse transform of ICtCp back to Rec.2020 RGB is as follows: void ICtCptoRGB(float *ictcpx, float *rgbx, int num) { for(int i = 0; i < num*4; i+=4) { double I = ictcpx[i+0], T = ictcpx[i+1], P = ictcpx[i+2]; double L = I + 0.00860903703793281*T + 0.11102962500302593*P; double M = I - 0.00860903703793281*T - 0.11102962500302593*P; double S = I + 0.56003133571067909*T - 0.32062717498731880*P; L = smpte2084_decodef(L); M = smpte2084_decodef(M); S = smpte2084_decodef(S); rgbx[i+0] = 3.4366066943330793*L - 2.5064521186562705*M + 0.0698454243231915*S; rgbx[i+1] = -0.7913295555989289*L + 1.9836004517922909*M - 0.1922708961933620*S; rgbx[i+2] = -0.0259498996905927*L - 0.0989137147117265*M + 1.1248636144023192*S; rgbx[i+3] = ictcpx[i+3]; } }
ICtCp claims that it provides an improved color representation that is designed for high dynamic range (HDR) and wide color gamut (WCG). It also claims that for CIEDE2000 color quantization errors 10-bit ICtCp would be equal to 11.5 bit YCbCr. Constant luminance is also improved with ICtCp which has a luminance relationship of 0.998 between the luma and encoded brightness while YCbCr has a luminance relationship of 0.819. An improved constant luminance is an advantage for color processing operations such as chroma subsampling and gamut mapping where only color information is changed.
Note, that I haven't verified these claims yet... Again, here is this color space converted to LDR via tone mapping. ## Evaluation of Color Spaces
To evaluate the color spaces, I am looking for a few different properties (that come to mind)
## Additional Snippets
static double smpte2084_decodef(double fv) { double num, denom; fv = pow(fv, 1/SMPTE_2084_M2); num = fv - SMPTE_2084_C1; num = num < 0 ? 0 : num; denom = SMPTE_2084_C2 - SMPTE_2084_C3 * fv; return pow(num / denom, 1/SMPTE_2084_M1); } static double smpte2084_encodef(double v) { double tmp = pow(v, SMPTE_2084_M1); return pow((SMPTE_2084_C1 + SMPTE_2084_C2 * tmp) / (1 + SMPTE_2084_C3 * tmp), SMPTE_2084_M2); } ## References
Probably others, but these are the important ones.
|
## Archives
## Categories |