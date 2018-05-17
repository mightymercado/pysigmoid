#include <bits/stdc++.h>

long double area(long double a, long double b, long double c) {
    long double s = (a + b + c) / 2.0L;
    return sqrtl(s)*sqrt(s-a)*sqrtl(s-b)*sqrtl(s-c);
}

long double powow(int w) {
    long double r = 1;
    while (w--) {
        r /= 2.0L;
        printf("%.70Lf\n", r);
    }
    return r;
}
int main() {
    long double a = 7.0L;
    long double b = 7.0L / 2.0L + 3.0L * powow(111);
    long double c = b;
    printf("%0.200Lf", area(a, b, c)); 
}