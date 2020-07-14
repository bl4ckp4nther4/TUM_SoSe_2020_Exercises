#include<stdio.h>
#include<math.h>
#include <iostream>
#include <fstream>

using namespace std;

/*
Definitions:
E_apprx = 1/N^2
E_tot = sqrt(N) * Eps_m

total Error minimum
N^(5/2) = 4/E_m

*/

int main(){
    double E_m = pow(10, -16);
    double N = pow(4.0/E_m, 0.4);
    double E_tot = sqrt(N) * E_m;

    printf("%.10e\n\n", E_tot);

    double power = 2.0/9.0;
    N = pow(16.0/E_m, 2.0);
    E_tot = 2.0 * pow(N, - 4.0) + sqrt(N) * E_m;

    printf("%.10e", E_tot);

}