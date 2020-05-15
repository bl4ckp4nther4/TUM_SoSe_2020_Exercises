#include <stdio.h>
#include <math.h>
#include <iostream>
#include <fstream>

using namespace std;

class RNG
{
private:
    int a;
    int c;
    int M;

public:
    int r;

    RNG(int, int, int, int);
    ~RNG();
    int getNextR();
};

RNG::RNG(int a, int c, int M, int r)
{
    this->a = a;
    this->c = c;
    this->M = M;
    this->r = r;
}

RNG::~RNG() { cout << "class RNG has been destroyed\n"; }

int RNG::getNextR()
{
    r = (r * a + c) % M;
    return r;
}

int main()
{
    int N = 1000;         //number of random numbers generated
    int randomNumbers[N]; // random numbers in array

    RNG RNG1(57, 13, 256, 10);
    RNG RNG2(47, 25, 256, 41);

    int n = 0;
    while (n < N)
    {
        RNG1.getNextR();
        RNG2.getNextR();

        if (RNG2.r % 2 == 0 || RNG2.r % 3 == 0 || RNG2.r % 5 == 0 || RNG2.r % 7 == 0 || RNG2.r % 13 == 0)
        {
            // take r_1
            cout << (randomNumbers[n] = RNG1.r) << "\n";
            n = n + 1;
        }
        else
        {
            // reject r_2 and go through the next loop, calculating the next r_1, r_2
        }
    }

    // create 2D random number pairs for visual verification
    int random2D[2][N / 2];
    for (int i = 0; i < N; i++)
    {
        if (i % 2 == 0)
        {
            cout << (random2D[0][i / 2] = randomNumbers[i]) << ",";
        }
        if (i % 2 == 1)
        {
            cout << (random2D[1][(i - 1) / 2] = randomNumbers[i]) << ",\n";
        }
    }
}