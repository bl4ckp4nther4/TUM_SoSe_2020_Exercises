#include<iostream>
#include<fstream>
#include<string>
#include<vector>
#include<ctime>
#include<numeric>
#include<math.h>
#include<stdio.h>

using namespace std;

class Um1D {        // Base Class
public:
    double x_0;     // initial position
    double v_x;     //  velocity 

    double t_total;    // total time
    double dt;    // time interval
    int steps;      // time steps

    Um1D(double x_0, double v_x, double dt, double t_total);     // constructor
    ~Um1D(void);                                           // destructor

    double x(double t_total);
        int archive();
};

Um1D::Um1D(double x_0, double v_x, double dt, double t_total) {
    this -> x_0 = x_0;
    this -> v_x = v_x;
    this -> t_total = t_total;
    this -> dt = dt;
    this -> steps = t_total / dt;
}

Um1D::~Um1D(void){
    printf("Class Um1D destroyed\n");
}

double Um1D::x(double t){
    return x_0 + t * v_x;
}

int Um1D::archive() {
    double xData;                   // x data to write
    double tData = 0;               // t data to write

    ofstream myfile;
    myfile.open ("Data.csv");       // opening the files
    for (int n = 1; n <= steps; n++) {
        xData = x(tData);

        myfile << tData;
        myfile << ",";
        myfile << xData;
        myfile << ",";
        myfile << "\n";
        
        printf("%e, %e, \n", tData, xData);

        tData = tData + dt;
    }
    myfile.close();         //close the file
    return(5);
}

class Um2D : 
public Um1D {      // child class
public:
    double y_0;     // initial position
    double v_y;     //  velocity

    Um2D( double x_0, double y_0, double v_x, double v_y, double dt, double t );
    ~Um2D(void);

    double y(double t);
        int archive();
};

Um2D::Um2D( double x_0, double y_0, double v_x, double v_y, double dt, double t_total ):
Um1D(x_0, v_x, dt, t_total) {
        this -> y_0 = y_0;
        this -> v_y = v_y;
}

Um2D::~Um2D(void){
    printf("Class Um2D destroyed\n");
}

double Um2D::y(double t) {
    return y_0 + t * v_y;
}

int Um2D::archive() {
    double tData = 0;               // t data to write
    double xData;                   // x data to write
    double yData;                   // y data to write
    
    ofstream myfile;
    myfile.open ("Data2D.csv");       // opening the files
    for (int n = 1; n <= steps; n++) {
        xData = x(tData);
        yData = y(tData);

        myfile << tData;
        myfile << ",";
        myfile << xData;
        myfile << ",";
        myfile << yData;
        myfile << ",";
        myfile << "\n";
        
        printf("%e, %e, %e,\n", tData, xData, yData);

        tData = tData + dt;
    }
    myfile.close();         //close the file
    return(5);
}

int main() {
    double x_0 = 0;         // initial x-position
    double y_0 = 0;         // initial y-position
    double v_x = 2;         // speed in x-direction
    double v_y = 1;         // speed in y-direction
    double dt = 0.001;      // time interval length
    double t_total = 1;     // total time


    Um2D motion2D(x_0, y_0, v_x, v_y, dt, t_total);

    motion2D.archive();
    return 0;
}