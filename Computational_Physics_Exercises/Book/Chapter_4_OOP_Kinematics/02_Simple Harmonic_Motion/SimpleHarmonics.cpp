#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <ctime>
#include <numeric>
#include <math.h>
#include <stdio.h>

using namespace std;

class SHx
{
public:
    double A_x;   // amplitude
    double w_x;   // circular frequency
    double phi_x; // phase

    double t_totalx; // the timeframe of evaluation
    double dt_x;     // the length of each time interval
    int steps_x;     // total time steps

    SHx(double A_x, double w_x, double phi_x, double dt_x, double t_totalx);
    ~SHx();

    double x(double t);
};

SHx::SHx(double A_x, double w_x, double phi_x, const double dt_x, double t_totalx)
{
    this->A_x = A_x;
    this->w_x = w_x;
    this->phi_x = phi_x;

    this->t_totalx = t_totalx;
    this->dt_x = dt_x;
    this->steps_x = t_totalx / dt_x;
}
SHx::~SHx()
{
    printf("SHx has been destroyed\n");
}

double SHx::x(double t)
{
    double x_pos = A_x * sin(w_x * t + phi_x);
    return x_pos;
}

class SHy
{
public:
    double A_y;   // amplitude
    double w_y;   // circular frequency
    double phi_y; // phase

    double t_totaly; // the timeframe of evaluation
    double dt_y;     // the length of each time interval
    int steps_y;     // total time steps

    SHy(double A_y, double w_y, double phi_y, double dt_y, double t_totaly);
    ~SHy();

    double y(double t);
};

SHy::SHy(double A_y, double w_y, double phi_y, double dt_y, double t_totaly)
{
    this->A_y = A_y;
    this->w_y = w_y;
    this->phi_y = phi_y;

    this->t_totaly = t_totaly;
    this->dt_y = dt_y;
    this->steps_y = t_totaly / dt_y;
}

SHy::~SHy()
{
    printf("SHy has been destroyed\n");
}

double SHy::y(double t)
{
    double y_pos = A_y * sin(w_y * t + phi_y);
    return y_pos;
}

class SHxy : public SHx, public SHy
{
public:
    SHxy(double A_x, double A_y, double w_x, double w_y, double phi_x, double phi_y, double dt_x, double dt_y, double t_totalx, double t_totaly);
    ~SHxy();

    int archive();
};

SHxy::SHxy(double A_x, double A_y, double w_x, double w_y, double phi_x, double phi_y, double dt_x, double dt_y, double t_totalx, double t_totaly) : SHx(A_x, w_x, phi_x, dt_y, t_totalx), SHy(A_y, w_y, phi_y, dt_y, t_totaly)
{
    // no new declarations
}

SHxy::~SHxy()
{
    printf("SHxy has been destroyed\n");
};

SHxy::archive()
{
    double txData = 0; // t data to write
    double tyData = 0; // t data to write
    double xData;      // x data to write
    double yData;      // y data to write

    int steps = max(steps_x, steps_y);

    printf("%i, %i, %i,\n", steps_x, steps_y, steps);

    ofstream myfile;
    myfile.open("Data2D.csv"); // opening the files

    for (int n = 1; n <= steps; n++)
    {
        if (n <= steps_x)
        {
            // put x data if n is smaller than max steps
            xData = x(txData);
            myfile << txData;
            myfile << ",";
            myfile << xData;
            myfile << ",";
        }
        else
        {
            // put empty fields
            myfile << " , ,";
        }

        if (n <= steps_y)
        {
            // put y data if n is smaller than max steps
            yData = y(tyData);
            myfile << tyData;
            myfile << ",";
            myfile << yData;
            myfile << ",";
        }
        else
        {
            // put empty fields
            myfile << " , ,";
        }

        myfile << "\n";

        //printf("%f, %f, %f,\n", tData, xData, yData);

        txData = txData + dt_x;
        tyData = tyData + dt_y;
    }
    myfile.close(); //close the file
    return 5;
}

int main()
{
    double A_x = 1;
    double A_y = 0.5;
    double w_x = 1;
    double w_y = 4;
    double phi_x = 0;
    double phi_y = 0.5 * w_y;
    double dt_x = 0.01;
    double dt_y = 0.01;
    double t_totalx = 10;
    double t_totaly = 10;

    SHxy Harmonic2D(A_x, A_y, w_x, w_y, phi_x, phi_y, dt_x, dt_y, t_totalx, t_totaly);

    Harmonic2D.archive();

    return 0;
}