// integ . c : Int e g r a t i on using t r ape z o i d , Simpson and Gauss rul e s
/* comment : The de r i va t i on from t h e o r e t i c a l r e s u l t f o r each method
i s s aved in x y1 y2 y3 f o rma t .
Program ne eds gaus s . c in t h e same d i r e c t o r y . */
#include <stdio.h>
#include <math.h>
#include "gauss.cpp" // r e t u r n s Legendre pts , we ights
#define max_in 999   // max number o f i n t e r v a l s
#define vmin 0.0     // range s o f i nt e g r a t i on
#define vmax 2.0
#define ME 2.7182818284590452354E0 // Eul e r ’ s number

main()
{
    int i;
    float result;
    float f(float x);
    float trapez(int no, float min, float max);   // t r ap e zo id rule
    float simpson(int no, float min, float max);  // Simpson ’ s rule
    float gaussint(int no, float min, float max); // Gauss ’ ruleS

    FILE *output; // save data in int eg.dat
    output = fopen("integ.dat", "w");
    // Simpson r e qui r e s odd N
    for (i = 3; i <= max_in; i += 2)
    {
        result = trapez(i, vmin, vmax);
        fprintf(output, "%i\t%e\t", i, result);
        result = simpson(i, vmin, vmax);
        fprintf(output, "%e\t", result);
        result = gaussint(i, vmin, vmax);
        fprintf(output, "%e\n", result);
    }
    printf("data stored in integ.dat\n");
    fclose(output);
}

// end
float f(float x) // fu n c t ion to i n t e g r a t e
{
    return (exp(-x));
}

float trapez(int no, float min, float max)
{
    // trapezoid rule
    int n;
    float interval, sum = 0., x;
    interval = ((max - min) / (no - 1));
    for (n = 2; n < no; n++)
    {
        // sum the midpoints
        x = interval * (n - 1);
        sum += f(x) * interval;
    }
    sum += 0.5 * (f(min) + f(max)) * interval;
    // add t he end p o i n t s
    return (sum);
}

float simpson(int no, float min, float max)
{
    // Simpson ’ s rule int n;
    float interval, sum = 0., x;
    interval = ((max - min) / (no - 1));
    for (int n = 2; n < no; n += 2)
    {
        // l o o p f o r odd poin t s
        x = interval * (n - 1);
        sum += 4 * f(x);
    }
    for (int n = 3; n < no; n += 2)
    {
        // l o o p f o r even po i n t s
        x = interval * (n - 1);
        sum += 2 * f(x);
    }
    sum += f(min) + f(max);
    // add first and last value
    sum *= interval / 3.;
    return (sum);
}

float gaussint(int no, float min, float max)
{
    // Gauss ’ rule
    float quadra = 0.;
    double w[1000], x[1000];
    void gauss(int npts, int job, double a, double b, double x[], double w[]);
    // f o r point s and weights
    gauss(no, 0, min, max, x, w); // Gauss Legendre po int s & wts
    for (int n = 0; n < no; n++)
        quadra += f(x[n]) * w[n];
    // Calcint e g r a l
    return (quadra);
}