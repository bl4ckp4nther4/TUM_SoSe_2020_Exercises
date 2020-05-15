#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <ctime>
#include <numeric>
#include <math.h>
#include <stdio.h>

using namespace std;

double randZeroToOne() //return a random number between 0 and 1
{
    double randZeroToOne = (double)rand() / (RAND_MAX);
    return randZeroToOne;
}

int main()
{
    for (int i = 0; i < 100000; i++)
    {
        cout << randZeroToOne()
             << "\n";
    }
}