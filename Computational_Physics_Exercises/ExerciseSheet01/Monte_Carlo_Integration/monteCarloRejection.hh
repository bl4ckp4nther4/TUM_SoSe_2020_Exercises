// this file will compute the integral of f(t) with the monte carlo method by rejection

double monteCarloRejection(double noOfPoints,
                           double integralStart,
                           double integralEnd,
                           double integralFloor,
                           double integralCeil)
{
    srand(time(NULL)); // seeding the rand() function with a new seed each time
    double f(double t);
    double x; // random x-coordinate
    double y; // random y-coordinate
    double N_in_pos = 0;
    double N_in_neg = 0;
    double boxArea;
    double rejectionIntegral;

    // summing all the f(t) on top of each other
    for (int i = 0; i < noOfPoints; i++)
    {
        x = (double)rand() / (RAND_MAX) * (integralEnd - integralStart) + integralStart;
        y = (double)rand() / (RAND_MAX) * (integralCeil - integralFloor) + integralFloor;

        if (f(x) >= 0 && y >= 0) // if f(x) and y both positive
        {
            if (y < f(x))
            {
                // add one to the points
                N_in_pos = N_in_pos + 1;
            }
            else
            {
                // do nothing
            }
        }
        if (f(x) < 0 && y < 0) // if f(x) and y both negative
        {
            if (y < f(x))
            {
                N_in_neg = N_in_neg + 1;
            }
            else
            {
                // do nothing
            }
        }
    }

    boxArea = (integralCeil - integralFloor) * (integralEnd - integralStart);
    rejectionIntegral = (N_in_pos - N_in_neg) / (noOfPoints)*boxArea;

    return rejectionIntegral;
}
