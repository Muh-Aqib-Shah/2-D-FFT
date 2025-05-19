#include <iostream>
#include <vector>
#include <cmath>
#include <complex>
#include <algorithm>

using namespace std;
using imaginary = complex<double>;


void bitReversal(vector<imaginary>& data) {
    int n = data.size();
    int numBits = ceil(log2(n));

    for (int i = 1; i < n; ++i) {
        int j = 0;
        int i_copy = i;

        for (int k = 0; k < numBits; ++k) {
            j <<= 1;                   // Shift j to the left to make room
            j |= (i_copy & 1);         // Add the LSB of i_copy to j
            i_copy >>= 1;              // Shift i_copy right to move to next bit
        }


        if (i < j) {
            swap(data[i], data[j]);
        }

    }
}

void fft(vector<imaginary>& data){
    int n = data.size();
    
    bitReversal(data);
    
    for(int len=2; len<=n; len*=2){
        
        double angle = (2*M_PI)/len;
        imaginary wlen = complex<double>(cos(angle),sin(angle));
        
        for(int j=0; j < n; j+=len){
            imaginary w(1,0);
            for(int k=0;k<(len/2);k++){
                imaginary u = data[j+k];
                imaginary v = data[j+k+ len/2]*w;
                
                data[j+k] = u + v;
                data[j+k+len/2] = u - v;
                w*=wlen;
                
            }
        }
    }
}
int main()
{

    const int N = 32;
    const double fs = 32.0;
    vector<imaginary> s(N);

    // Create a signal: sum of 3Hz and 7Hz sine waves
    for (int n = 0; n < N; ++n) {
        double t = n / fs;
        double val = sin(2 * M_PI * 3 * t) + sin(2 * M_PI * 7 * t);
        s[n] = imaginary(val, 0.0); // real part only
    }

    
    fft(s);
    
    for(int i=0;i<N;i++){
        cout<<"Index "<<i<<": "<<abs(s[i])<<endl;
    }


    return 0;
}