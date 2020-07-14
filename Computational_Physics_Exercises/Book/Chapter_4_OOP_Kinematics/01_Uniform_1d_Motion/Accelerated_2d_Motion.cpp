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

    double x(double t);
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
        
        printf("%f, %f, \n", tData, xData);

        tData = tData + dt;
    }
    myfile.close();         //close the file
    return(5);
}

class Um2D :        // child class
public Um1D {      
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
        
        //printf("%f, %f, %f,\n", tData, xData, yData);

        tData = tData + dt;
    }
    myfile.close();         //close the file
    return(5);
}

class Am2D :        // second child class
public Um2D {       
public:
    double a_x;     // accelaration in x direction
    double a_y;     // accelaration in y direction

    Am2D( double x_0, double y_0, double v_x, double v_y, double a_x, double a_y, double dt, double t_total );
    ~Am2D(void);

    double x_acc(double t);
    double y_acc(double t);
    int archive();

    
};

Am2D::Am2D(double x_0, double y_0, double v_x, double v_y, double a_x, double a_y, double dt, double t_total ):
Um2D(x_0, y_0, v_x, v_y, dt, t_total){
    this -> a_y = a_y;
    this -> a_x = a_x;
}

Am2D::~Am2D(void){
    printf("Am2D has been destroyed\n");
}

double Am2D::x_acc(double t) {
    double x_pos = x(t) + 0.5*a_x * t*t;
    return x_pos;
}

double Am2D::y_acc(double t) {
    double y_pos = y(t) + 0.5*a_y * t*t;
    return y_pos;
}

int Am2D::archive() {
    printf("archiving...\n");
    double tData = 0;               // t data to write
    double xData;               // t data to write
    double yData;               // t data to write
    
    ofstream myfile;
    myfile.open ("DataAccelerated2D.csv");       // opening the file
    for (int n = 1; n <= steps; n++) {
        xData = x_acc(tData);  //reading x position from the x_acc function which takes acc into account    
        yData = y_acc(tData);

        //writing data to file
        myfile << tData;
        myfile << ",";
        myfile << xData;
        myfile << ",";
        myfile << yData;
        myfile << ",";
        myfile << "\n";
        
        printf("%f, %f, %f,\n", tData, xData, yData);

        tData = tData + dt;
    }
    myfile.close();         //close the file
    return(5);
}

int main() {
    double x_0 = 0;         // initial x-position
    double y_0 = 0;         // initial y-position
    double v_x = 14;         // speed in x-direction
    double v_y = 14;         // speed in y-direction
    double a_x = 0;         // acceleration in x-direction
    double a_y = -9.81;     // acceleration in x-direction
    double dt = 0.01;      // time interval length
    double t_total = 3;     // total time

    Am2D FootballFlight( x_0, y_0, v_x, v_y, a_x, a_y, dt, t_total );
    FootballFlight.archive();
    Um2D Boring( x_0, y_0, v_x, v_y, dt, t_total);

    //Boring.archive();

    return 0;
}