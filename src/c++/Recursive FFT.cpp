#include <iostream>
#include <cmath>
#include <complex>
#include <vector>
#include <vector>

using namespace std;

using imaginary = complex<double>;

vector<imaginary> FFT(vector<imaginary> p){
    int n=p.size();
   
    if (n==1){
        return p;
    }
    
    imaginary w = complex<double>(cos(2 * M_PI / n), sin(2 * M_PI / n));
    
    vector<imaginary> pEven , pOdd;
    for(int i=0;i<n;i++){
        if(i%2==0){
            pEven.push_back(p[i]);
        }
        else{
            pOdd.push_back(p[i]);
        }
    }
    
    vector<imaginary> yEven , yOdd;
    yEven=FFT(pEven);
    yOdd=FFT(pOdd);
    
    vector<imaginary> y(n,0);
    for(int j=0;j<n/2;j++){
        y[j] = yEven[j] + (pow(w,j)*yOdd[j]);
        y[j+(n/2)] = yEven[j] - (pow(w,j)*yOdd[j]);
    }
    
    return y;
    
}

int main()
{
    const int N = 32;
    const double fs = 32.0;
    vector<imaginary> signal(N);

    // Create a signal: sum of 3Hz and 7Hz sine waves
    for (int n = 0; n < N; ++n) {
        double t = n / fs;
        double val = sin(2 * M_PI * 3 * t) + sin(2 * M_PI * 7 * t);
        signal[n] = imaginary(val, 0.0); // real part only
    }

    // Perform FFT
    vector<imaginary> result = FFT(signal);

    // Display FFT magnitudes
    cout << "FFT Magnitudes:\n";
    for (int i = 0; i < result.size(); ++i) {
        cout << "Index " << i << ": " << abs(result[i]) << endl;
    }

    return 0;
}

