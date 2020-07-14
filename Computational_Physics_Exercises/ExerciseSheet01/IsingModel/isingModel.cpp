#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <ctime>
#include <numeric>
#include <math.h>
#include <stdio.h>
#include <string>
#include <bits/stdc++.h>

#include "metropolisAlgorithm.hh"
#include "metropolisAlgorithm2D.hh"

using namespace std;

// this program will apply the Metropolis Algorithm tosimulate the 1D ising chain
int plot = 3;

int main()
{
    // initialisation
    int N = 20; // Number of dipoles
    double kT;  // energy value of k_B * T
    double J = 1;
    bool coldStart = false;

    // exercise 1a) - 1b)
    kT = 0.1;

    vecto r<int> exercise1e = metropolisAlgorith(N, 10 * N, J, kT, coldStart);
    configurationPlot(exercise1e);

    // exercise 1f)
    kT = 0.01;
    vector<int> exercise1f = metropolisAlgorith(N, 100 * N, J, kT, coldStart);
    configurationPlot(exercise1f);

    kT = 0.1;
    exercise1f = metropolisAlgorith(N, 100 * N, J, kT, coldStart);
    configurationPlot(exercise1f);

    kT = 1;
    exercise1f = metropolisAlgorith(N, 100 * N, J, kT, coldStart);
    configurationPlot(exercise1f);

    // exercise 1g)
    coldStart = true;
    kT = 1;
    vector<int> exercise1g = metropolisAlgorith(N, 100 * N, J, kT, coldStart);
    configurationPlot(exercise1g);

    // exercise 1h)
    int M = N;
    vector<vector<int>> exercise1h = metropolisAlgorith2D(N, M, 100 * N, J, kT, coldStart);
    configurationPlot2D(exercise1h);
}