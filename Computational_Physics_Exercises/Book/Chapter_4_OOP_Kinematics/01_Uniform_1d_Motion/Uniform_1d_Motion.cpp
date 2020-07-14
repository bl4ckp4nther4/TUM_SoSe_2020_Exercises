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

    double t;    // time
    double dt;    // time interval
    int steps;      // time steps

    Um1D(double x_0, double v_x, double dt, double t);     // constructor
    ~Um1D(void);                                           // destructor

    double x(double t);
        int archive();
};

Um1D::Um1D(double x_0, double v_x, double dt, double t) {
    this -> x_0 = x_0;
    this -> v_x = v_x;
    this -> t = t;
    this -> dt = dt;
    this -> steps = t / dt;
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

int main() {
    Um1D motion(1.0, 2.0, 0.1, 10.0);
    motion.archive();


    return 0;
}