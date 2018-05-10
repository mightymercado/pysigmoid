#include <bits/stdc++.h>

using namespace std;

double sin(double x) {
    double sum = 0;
    double mul = x;
    double den = 1;
    for (int i = 0; i < 1000; i++) {
        int sign = (i%2==0?1:-1);
        printf("%f\n", mul);
        sum += (i%2==0?1:-1) * mul;
        mul *= x * x;
        mul /= 2*(i+1)*(2*(i+1)+1);
    }
    return sum;
}
int main() {
    double x;
    scanf("%lf", &x);
    printf("%lf", sin(x));
}