---
title: fp64 approximations for sin/cos for OpenGL
url: https://outerra.blogspot.com/2017/06/fp64-approximations-for-sincos-for.html
author: Outerra
published: '2017-06-13'
source_blog: Outerra
source_site: https://outerra.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Minimax approximations for missing fp64 functions in GLSL, using


//sin approximation, error < 5e-9

double sina_9(double x)

{

//minimax coefs for sin for 0..pi/2 range

const double a3 = -1.666665709650470145824129400050267289858e-1LF;

const double a5 = 8.333017291562218127986291618761571373087e-3LF;

const double a7 = -1.980661520135080504411629636078917643846e-4LF;

const double a9 = 2.600054767890361277123254766503271638682e-6LF;


const double m_2_pi = 0.636619772367581343076LF;

const double m_pi_2 = 1.57079632679489661923LF;


double y = abs(x * m_2_pi);

double q = floor(y);

int quadrant = int(q);


double t = (quadrant & 1) != 0 ? 1 - y + q : y - q;

t *= m_pi_2;


double t2 = t * t;

double r = fma(fma(fma(fma(a9, t2, a7), t2, a5), t2, a3), t2*t, t);


r = x < 0 ? -r : r;


return (quadrant & 2) != 0 ? -r : r;

}


//sin approximation, error < 2e-11

double sina_11(double x)

{

//minimax coefs for sin for 0..pi/2 range

const double a3 = -1.666666660646699151540776973346659104119e-1LF;

const double a5 = 8.333330495671426021718370503012583606364e-3LF;

const double a7 = -1.984080403919620610590106573736892971297e-4LF;

const double a9 = 2.752261885409148183683678902130857814965e-6LF;

const double ab = -2.384669400943475552559273983214582409441e-8LF;


const double m_2_pi = 0.636619772367581343076LF;

const double m_pi_2 = 1.57079632679489661923LF;


double y = abs(x * m_2_pi);

double q = floor(y);

int quadrant = int(q);


double t = (quadrant & 1) != 0 ? 1 - y + q : y - q;

t *= m_pi_2;


double t2 = t * t;

double r = fma(fma(fma(fma(fma(ab, t2, a9), t2, a7), t2, a5), t2, a3),

t2*t, t);


r = x < 0 ? -r : r;


return (quadrant & 2) != 0 ? -r : r;

}




Cos can be just offset by π/2


//cos approximation, error < 5e-9

double cosa_9(double x)

{

//sin(x + PI/2) = cos(x)

return sina_9(x + DBL_LIT(1.57079632679489661923LF));

}


//cos approximation, error < 2e-11

double cosa_11(double x)

{

//sin(x + PI/2) = cos(x)

return sina_11(x + DBL_LIT(1.57079632679489661923LF));

}

[remez exchange toolbox.](http://lolengine.net/wiki/doc/maths/remez)For additional details see[Double precision approximations for map projections in OpenGL](http://outerra.blogspot.com/2014/05/double-precision-approximations-for-map.html).//sin approximation, error < 5e-9

double sina_9(double x)

{

//minimax coefs for sin for 0..pi/2 range

const double a3 = -1.666665709650470145824129400050267289858e-1LF;

const double a5 = 8.333017291562218127986291618761571373087e-3LF;

const double a7 = -1.980661520135080504411629636078917643846e-4LF;

const double a9 = 2.600054767890361277123254766503271638682e-6LF;

const double m_2_pi = 0.636619772367581343076LF;

const double m_pi_2 = 1.57079632679489661923LF;

double y = abs(x * m_2_pi);

double q = floor(y);

int quadrant = int(q);

double t = (quadrant & 1) != 0 ? 1 - y + q : y - q;

t *= m_pi_2;

double t2 = t * t;

double r = fma(fma(fma(fma(a9, t2, a7), t2, a5), t2, a3), t2*t, t);

r = x < 0 ? -r : r;

return (quadrant & 2) != 0 ? -r : r;

}

//sin approximation, error < 2e-11

double sina_11(double x)

{

//minimax coefs for sin for 0..pi/2 range

const double a3 = -1.666666660646699151540776973346659104119e-1LF;

const double a5 = 8.333330495671426021718370503012583606364e-3LF;

const double a7 = -1.984080403919620610590106573736892971297e-4LF;

const double a9 = 2.752261885409148183683678902130857814965e-6LF;

const double ab = -2.384669400943475552559273983214582409441e-8LF;

const double m_2_pi = 0.636619772367581343076LF;

const double m_pi_2 = 1.57079632679489661923LF;

double y = abs(x * m_2_pi);

double q = floor(y);

int quadrant = int(q);

double t = (quadrant & 1) != 0 ? 1 - y + q : y - q;

t *= m_pi_2;

double t2 = t * t;

double r = fma(fma(fma(fma(fma(ab, t2, a9), t2, a7), t2, a5), t2, a3),

t2*t, t);

r = x < 0 ? -r : r;

return (quadrant & 2) != 0 ? -r : r;

}

Cos can be just offset by π/2

//cos approximation, error < 5e-9

double cosa_9(double x)

{

//sin(x + PI/2) = cos(x)

return sina_9(x + DBL_LIT(1.57079632679489661923LF));

}

//cos approximation, error < 2e-11

double cosa_11(double x)

{

//sin(x + PI/2) = cos(x)

return sina_11(x + DBL_LIT(1.57079632679489661923LF));

}

## No comments:

Post a Comment