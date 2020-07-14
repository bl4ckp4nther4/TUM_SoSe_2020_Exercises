#include<stdio.h>
#include<math.h>

// solutions to the equation a*x^2+b*x+c = 0 and the substractive cancellation error


int main(){
    // declare variables
    double a;
    double b;
    double c;

    double x1;
    double x2;
    double x1_;
    double x2_;

    double f_x1;
    double f_x2;
    double f_x1_;
    double f_x2_;

    int j;
    int i;

    // set a, b, c
    a = 1;
    b = 1;
    c = 0.0000000000000001;

    // calculate solutions for x1, ...
    x1 = (-b + sqrt(b*b - 4*a*c) ) / (2*a);
    x2 = (-b - sqrt(b*b - 4*a*c) ) / (2*a);

    x1_ = -2*c/(b + sqrt(b*b-4*a*c));
    x2_ = -2*c/(b - sqrt(b*b-4*a*c));

    // insert values back into the equation (should result in 0)
    f_x1 = a*x1*x1 + b*x1 + c;
    f_x2 = a*x2*x2 + b*x2 + c;

    f_x1_ = a*x1_*x1_ + b*x1_ + c;
    f_x2_ = a*x2_*x2_ + b*x2_ + c;

    // combine solutions and results
    double solutions[2][4] = {
        {x1, x2, x1_, x2_},
        {fabs(f_x1), fabs(f_x2), fabs(f_x1_), fabs(f_x2_)}
    };

    // sorting the solutions

    for (i = 0; i < 4; i++) // going through the array
	{
		for (j = i + 1; j < 4; j++) // going through all the elements further in the array
		{
			if(solutions[1][i] > solutions[1][j]) // if the earlier one is larger 
			{
                // switch them
                double temp[2]; // temporary variable

				temp[0] = solutions[0][i];
				temp[1] = solutions[1][i];

				solutions[0][i] = solutions[0][j];
                solutions[1][i] = solutions[1][j];
                
				solutions[0][j] = temp[0];
				solutions[1][j] = temp[1];
			}
			
		}
	}

    // print the solutions
    
    printf("\n");
    printf("a    b    c\n");
    printf("%.1f  %.1f  %.10f \n", a, b, c);

    printf("\n");
    printf("x Solutions      Error\n"); // title 
    //printing out the table with x solutions and errors
    for (i = 0; i < 4; i++) {
        for (j = 0; j < 2; j++) {
            printf("%.10f    ", solutions[j][i]);
        }
        printf("\n");
    }
    
    

}