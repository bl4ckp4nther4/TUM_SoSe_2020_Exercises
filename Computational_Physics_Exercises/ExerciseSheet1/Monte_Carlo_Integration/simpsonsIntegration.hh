// this file will compute the integral of f(t) with the simpsons method

double simpsonsInt(int no, double min, double max)
{
    double f(double x);            // function that is integrated
    double epsilon = pow(10, -10); // maximum deviation of the test sum, from expected value

    double h = (max - min) / (no - 1); // width of deviding integrals
    double t;                          // function variable
    double w;                          // weight of points ( Endpoint are weighted only half )
    double w_sum = 0;                  // testsum of the weights

    double sum = 0; // sum for summing the different parts together

    for (int n = 1; n <= no; n++)
    {

        t = min + ((double)n - 1) * h; // value of variable in iteration

        if (n % 2 == 0)
        {
            w = 4 * h / 3; // even n weight
        }
        if (n % 2 == 1 && n != 1 && n != no)
        {
            w = 2 * h / 3; // odd weight n (without endpoints)
        }
        if (n == 1 || n == no)
        {
            w = h / 3; // endpoint weight
        }
        w_sum = w_sum + w;

        sum = sum + w * f(t); // adding all the values of the function f times the width h
    }
    if (w_sum <= (no - 1) * h + epsilon && w_sum >= (no - 1) * h - epsilon) // checking the sum of the weights
    {
        return sum;
    }
    else
    {
        printf("\nERROR: Sum of weights has unexpected value: %.10f, expected value: %.10f \n\n", w_sum, (no - 1) * h);
        return sum;
    }
}