#include <bits/stdc++.h>
using namespace std;

//f(x) = x^2 - a
//f'(x) = 2x
int main() {
    double a, x;
    scanf("%lf", &a);
    x = a;
    double eps = FLOAT_MIN;
    for (int i = 0; i < 8; i++) {
        x = (x + a/x) / 2;
    }
    printf("%f\n", x);
}