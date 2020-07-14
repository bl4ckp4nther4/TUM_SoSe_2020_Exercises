#include<stdio.h>
#include<math.h>

int main(){
	// define variables
	float pi = 3.14159265359;
	
	float radius;
	float area;
	
	// user input	
	printf("\n");
    printf("Calculate Circle Area \n");
	printf("============= \n");
	printf("Input integer radius: ");
	scanf("%f", &radius);  
	
	// calculate radius
	area = pi * radius * radius;
	
	// output radius and area
	printf("Radius: ");
	printf("%f\n", radius);
	printf("Area: ");
	printf("%f\n", area);
}