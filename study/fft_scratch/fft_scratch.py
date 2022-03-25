"""FFT Scratch
    Reference. 
        Kor, proof of formula,
          https://ghebook.blogspot.com/2020/09/dft-discrete-fourier-transform.html
        Eng, Cooley and Tukey,
          http://jakevdp.github.io/blog/2013/08/28/understanding-the-fft/
"""
import time
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, dct, ifft, idct

"""Base on formula"""


def fft_scratch(f, M=0):
    """fft, exactly dft
        fft formula
          F(w) = integ_{-inf}^inf f(t) * exp(-j * w * t) dt
        dft formula
          F_k = sigma_{m=0}^{M-1} f_m * exp(-j * 2 * pi * m * k / M)
    """
    if M == 0:
        M = len(f)
    fft_result = np.zeros(M, dtype=np.complex128)
    for k in range(len(fft_result)):
        sumation_f = 0
        for m in range(len(f)):
            sumation_f += f[m] * np.exp(-1j * 2 * np.pi * m * k / M)
        fft_result[k] = sumation_f

    return fft_result


def ifft_scratch(f, M=0):
    """fft, exactly dft
        ifft formula
          f(t) = (1/2*pi)*integ_{-inf}^inf F(w) * exp(j * w * t) dw
        idft formula
          f_k  = (1/M)   *sigma_{m=0}^{M-1} F_m * exp(j * 2 * pi * m * k / M)
    """
    if M == 0:
        M = len(f)
    ifft_result = np.zeros(M, dtype=np.complex128)
    for k in range(len(ifft_result)):
        sumation_f = 0
        for m in range(len(f)):
            sumation_f += f[m] * np.exp(1j * 2 * np.pi * m * k / M)
        ifft_result[k] = sumation_f / M

    return ifft_result


def dct_scratch(f, M=0):
    """
        DCT-1, T = 2M-2
        Fk  = sigma_{m=0}^{2M-3}*f_m*e^{-j*pi*k/(M-1)*m}
            = f_0 + (-1)^k*f_{M-1} + 2*sigma_{m=1}^{M-2}*f_m*cos(pi*k*(m-1)/(M-1)*m)
        
        DCT-1, Xk = Fk/2

        DCT-2, T = 4M
        F_k = 2*sigma_{m=0}^{M-1}*f_{2m+1}*cos(pi*k/2M*m)
    """
    raise NotImplementedError


def idct_scratch(f, M=0):
    """
        iDCT-1
        x_m = 1/(M-1) * [X_0 + (-1)^m*X_{M-1} + 2*sigma_{m=1}^{M-2}*X_m*cos(pi*m*(m-1)/(M-1)*m)] ]
    """
    raise NotImplementedError


"""Base. Cooley and Tukey """


def DFT_slow(x):
    """Compute the discrete Fourier Transform of the 1D array x"""
    x = np.asarray(x, dtype=float)
    N = x.shape[0]
    n = np.arange(N)
    k = n.reshape((N, 1))
    M = np.exp(-2j * np.pi * k * n / N)
    return np.dot(M, x)


def FFT(x):
    """A recursive implementation of the 1D Cooley-Tukey FFT
        Big O: O(NlogN)
    """

    x = np.asarray(x, dtype=float)
    N = x.shape[0]

    if N % 2 > 0:
        raise ValueError("size of x must be a power of 2")
    elif N <= 32:  # this cutoff should be optimized
        return DFT_slow(x)
    else:
        X_even = FFT(x[::2])
        X_odd = FFT(x[1::2])
        factor = np.exp(-2j * np.pi * np.arange(N) / N)
        return np.concatenate(
            [X_even + factor[: N // 2] * X_odd, X_even + factor[N // 2 :] * X_odd]
        )


def FFT_vectorized(x):
    """A vectorized, non-recursive version of the Cooley-Tukey FFT"""
    x = np.asarray(x, dtype=float)
    N = x.shape[0]

    if np.log2(N) % 1 > 0:
        raise ValueError("size of x must be a power of 2")

    # N_min here is equivalent to the stopping condition above,
    # and should be a power of 2
    N_min = min(N, 32)

    # Perform an O[N^2] DFT on all length-N_min sub-problems at once
    n = np.arange(N_min)
    k = n[:, None]
    M = np.exp(-2j * np.pi * n * k / N_min)
    X = np.dot(M, x.reshape((N_min, -1)))

    # build-up each level of the recursive calculation all at once
    while X.shape[0] < N:
        X_even = X[:, : X.shape[1] // 2]
        X_odd = X[:, X.shape[1] // 2 :]
        factor = np.exp(-1j * np.pi * np.arange(X.shape[0]) / X.shape[0])[:, None]
        X = np.vstack([X_even + factor * X_odd, X_even - factor * X_odd])

    return X.ravel()


def hfft_scratch(f, M=0):
    raise NotImplementedError


def ihfft_scratch(f, M=0):
    raise NotImplementedError


def rfft_scratch(f, M=0):
    raise NotImplementedError


def irfft_scratch(f, M=0):
    raise NotImplementedError


if __name__ == "__main__":
    print("Checking function operation...")
    print("-" * 40)

    x = np.random.random(1024)
    print(np.allclose(fft_scratch(x), np.fft.fft(x)))
    print(np.allclose(DFT_slow(x), np.fft.fft(x)))
    print(np.allclose(fft(x), np.fft.fft(x)))
    print(np.allclose(FFT(x), np.fft.fft(x)))
    print(np.allclose(FFT_vectorized(x), np.fft.fft(x)))

    print("-" * 40)

    x = np.random.random(1024)
    curr_time = time.perf_counter()

    fft_scratch(x)
    print("fft_scratch:", time.perf_counter() - curr_time)
    curr_time = time.perf_counter()

    DFT_slow(x)
    print("DFT_slow:", time.perf_counter() - curr_time)
    curr_time = time.perf_counter()

    FFT(x)
    print("FFT:", time.perf_counter() - curr_time)
    curr_time = time.perf_counter()

    FFT_vectorized(x)
    print("FFT_vectorized:", time.perf_counter() - curr_time)
    curr_time = time.perf_counter()

    fft(x)
    print("scipy fft:", time.perf_counter() - curr_time)
    curr_time = time.perf_counter()

    np.fft.fft(x)
    print("numpy fft:", time.perf_counter() - curr_time)
    curr_time = time.perf_counter()

    np.fft.rfft(x)
    print("numpy rfft:", time.perf_counter() - curr_time)
    curr_time = time.perf_counter()

    np.fft.hfft(x)
    print("numpy hfft:", time.perf_counter() - curr_time)

    print("-" * 40)

    x = np.random.random(1024 * 16)
    curr_time = time.perf_counter()

    FFT(x)
    print("FFT:", time.perf_counter() - curr_time)
    curr_time = time.perf_counter()

    FFT_vectorized(x)
    print("FFT_vectorized:", time.perf_counter() - curr_time)
    curr_time = time.perf_counter()

    fft(x)
    print("scipy fft:", time.perf_counter() - curr_time)
    curr_time = time.perf_counter()

    np.fft.fft(x)
    print("numpy fft:", time.perf_counter() - curr_time)
    curr_time = time.perf_counter()

    # In jupyter notebook
    # %timeit DFT_slow(x)
    # %timeit FFT(x)
    # %timeit np.fft.fft(x)

    print("Check function operation in frequency domain...")
    fs = 1000
    total_time = 0.1
    frequency = 100
    sample_list = np.arange(0, total_time * fs)
    a_0 = np.sin(2 * np.pi * frequency * sample_list / fs)
    a_1 = np.sin(2 * np.pi * 2 * frequency * sample_list / fs)
    a = (a_0 + a_1) / 2
    n = len(a)
    bins = np.arange(0, n) * fs / n

    a_fft_scratch = fft_scratch(a)
    a_fft_numpy = np.fft.fft(a)
    a_fft_scipy = fft(a)

    a_ifft_scratch = ifft_scratch(a_fft_scratch)
    a_ifft_numpy = np.fft.ifft(a_fft_numpy)
    a_ifft_scipy = ifft(a_fft_scipy)

    a_dct_scipy = dct(a)
    a_idct_scipy = idct(a_dct_scipy)

    # plt.plot(bins, np.abs(a_fft_numpy/n), "o")
    # plt.plot(bins, np.abs(a_fft_scipy/n), "x")
    # try:
    #     plt.plot(bins, np.abs(a_fft_scratch/n), ".", color="r")
    # except ValueError:
    #     pass
    # plt.xticks(np.arange(0, 1100, 100))
    # plt.yticks(np.arange(-1, 1.2, 0.2))
    # plt.grid()
    # plt.show()
