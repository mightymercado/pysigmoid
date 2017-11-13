#include <bits/stdc++.h>

using namespace std;

int main() {
    double a[] = {3.2e8, 1, -1, 8.0e8};
    double b[] = {4.0e8, 1, -1, -1.6e8};
    double sum = 0;
    for (int i = 0; i < 4; i++) {
        sum += a[i] * b[i];
    }
    cout << sum << endl;
}