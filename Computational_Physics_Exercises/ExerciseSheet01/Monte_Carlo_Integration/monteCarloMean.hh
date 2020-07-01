// this file will compute the integral of f(t) with the monte carlo method by mean

double exponentialWeightFunction(double lambda)
{
    double r = (double)rand() / (RAND_MAX);
    double x = -lambda * log(1 - r);
    return x;
}

double uniformWeightFunction(double integralStart, double integralEnd)
{
    double r = (double)rand() / (RAND_MAX);
    double x = (integralEnd - integralStart) * r + integralStart;
    return x;
}

double monteCarloMean(double noOfPoints,
                      std::string weightFunctionType,
                      double integralStart, double integralEnd,
                      double lambda)
{
    srand(time(NULL)); // seeding the rand() function with a new seed each time
    double f(double t);
    double x; // point of evaluation
    double sum = 0;
    double term = 0;
    double fAverage;
    double MCintegral;

    // summing all the f(t) on top of each other
    for (int i = 0; i < noOfPoints; i++)
    {
        if (!weightFunctionType.compare("uniform"))
        {
            x = uniformWeightFunction(integralStart, integralEnd);
        }
        if (!weightFunctionType.compare("exponential"))
        {
            x = exponentialWeightFunction(lambda);
        }

        term = f(x);
        sum = sum + term;
    }

    //calculate average of f over the integration interval
    fAverage = sum / noOfPoints;

    // multiply by lenth of interval
    if (weightFunctionType == "uniform")
    {
        MCintegral = fAverage * (integralEnd - integralStart);
    }
    if (weightFunctionType == "exponential")
    {
        MCintegral = lambda * fAverage;
    }
    return MCintegral;
}
