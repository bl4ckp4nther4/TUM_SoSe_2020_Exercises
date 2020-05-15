#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <ctime>
#include <numeric>
#include <math.h>
#include <stdio.h>
#include <string>

#include "gaussIntegration.hh"
#include "simpsonsIntegration.hh"
#include "trapezoidIntegration.hh"
#include "monteCarloMean.hh"
#include "monteCarloRejection.hh"

using namespace std;

// Computational Physics II Exercise Sheet 1
// =========================================
// 2.Numerical Integration

// User input:
// ============================================================
int equationNo = 4;                     // select which one of the equations to use
bool plotAccuracyVsEvaluations = false; // output the plot data for 2)
double maxPlotNo = 1001;                // max N for the rel accuracy plot in 2a), needs to be UNEVEN
double monteCarloNo = 1e6;              // no of numbers generated for the monte carlo calculations
// ============================================================

// calculates the relative error of the calculation result
double
relativeError(double calculatedResult, double expectedResult)
{
    double relErr = fabs(calculatedResult - expectedResult) / fabs(expectedResult);
    return relErr;
}

// function of which the integral is calculated
double f(double x)
{
    if (equationNo == 2)
    {
        return exp(-x);
    }

    if (equationNo == 3)
    {
        return sin(x);
    }

    if (equationNo == 4)
    {
        return log(cos(x)) / x;
    }
    if (equationNo == 5)
    {
        return cos(x) * log(x) / sqrt(x)
    }
    else
    {
        return x;
        cout << "No function selected output: f(x) = x \n";
    }
}

int main()
{
    // declarations
    double integralStart;
    double integralEnd;
    double integralFloor;
    double integralCeil;
    string weightFunctionType;
    double lambda;
    double expectedResult;

    // definitions for each of the equations
    if (equationNo == 2)
    {
        integralStart = 0;
        integralEnd = INFINITY;
        integralFloor = 0;
        integralCeil = 1;
        weightFunctionType = "exponential";
        lambda = 100;
        expectedResult = exp(-integralStart); // -exp(-inf) - (-exp(-0))
    }

    if (equationNo == 3)
    {
        integralStart = 0;
        integralEnd = 3.14159265359;
        integralFloor = -1;
        integralCeil = 1;
        weightFunctionType = "uniform";
        lambda = 0;
        expectedResult = cos(integralStart) - cos(integralEnd);
    }

    if (equationNo == 4)
    {
        integralStart = 0;
        integralEnd = 1;
        integralFloor = -INFINITY;
        integralCeil = 0;
        weightFunctionType = "uniform";
        lambda = 0;
        expectedResult = -0.27568727380043716;
    }

    if (equationNo == 5)
    {
        integralStart = 0;
        integralEnd = 1;
        integralFloor = -INFINITY;
        integralCeil = 0;
        weightFunctionType = "uniform";
        lambda = 0;
        expectedResult = -3.92203;
    }

    // 2a) i)
    cout << "\n2a) i) Integration with Gauss, Simpsons and Trapezoid methods\n";

    double gaussResult = gaussInt(maxPlotNo, integralStart, integralEnd);
    double simpsonsResult = simpsonsInt(maxPlotNo, integralStart, integralEnd);
    double trapezoidResult = trapezoidInt(maxPlotNo, integralStart, integralEnd);

    cout << "\nFunction: (" << equationNo << ")\n\n"
         << "Gauss method: " << gaussResult << "\n"
         << "Simpsons method: " << simpsonsResult << "\n"
         << "Trapezoid method: " << simpsonsResult << "\n";

    // 2a) ii output plot data of errof vs evaluations
    if (plotAccuracyVsEvaluations == true)
    {
        // plot no of evaluations vs relative accuracy
        cout << "\n2a) Plot data with relative error for various methods of calculating the Integrals,\n"
             << "Importance sampling enables for eq (2) "
             << "\nFunction: (" << equationNo << ")\n"
             << "\nlog_10(N), Gauss, Simpson, Trapezoid\n\n";

        for (double noOfEvaluations = 3; noOfEvaluations < maxPlotNo; noOfEvaluations = noOfEvaluations + 2)
        {
            //calculate result with various methods
            double gaussResult = gaussInt(noOfEvaluations, integralStart, integralEnd);
            double simpsonsResult = simpsonsInt(noOfEvaluations, integralStart, integralEnd);
            double trapezoidResult = trapezoidInt(noOfEvaluations, integralStart, integralEnd);

            // output log log plot data of number of intervals vs relative error
            cout
                << log(noOfEvaluations) / log(10) << ","
                << log(relativeError(gaussResult, expectedResult)) / log(10) << ","
                << log(relativeError(simpsonsResult, expectedResult)) / log(10) << ","
                << log(relativeError(trapezoidResult, expectedResult)) / log(10) << ","
                << "\n";
        }
    }

    // 2b) i)
    cout << "\n2b) i) Monte Carlo integration by mean and by rejection\n";

    double MCMeanResult = monteCarloMean(monteCarloNo,
                                         weightFunctionType,
                                         integralStart, integralEnd,
                                         lambda);
    double MCRejectionResult = monteCarloRejection(monteCarloNo,
                                                   integralStart, integralEnd,
                                                   integralFloor, integralCeil);

    cout << "\nFunction: (" << equationNo << ")\n\n"
         << "Monte Carlo by Mean: " << MCMeanResult << "\n"
         << "Monte Carlo by Rejection: " << MCRejectionResult << "\n";

    // 2b) ii)
    cout << "\n2b) ii) Monte Carlo integration by rejection with boundries two orders of magnitude too large\n";

    double integralFloor_2bii = integralFloor * 100;
    double integralCeil_2bii = integralCeil * 100;
    double MCRejectionResult_2bii = monteCarloRejection(monteCarloNo,
                                                        integralStart, integralEnd,
                                                        integralFloor_2bii, integralCeil_2bii);

    cout << "\nFunction: (" << equationNo << ")\n\n"
         << "Monte Carlo by Rejection: " << MCRejectionResult_2bii << "\n";

    // 2b) iii)
}
