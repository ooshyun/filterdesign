"""Test for c file
    
    TODO LIST
    ---
    [ ] 1. Test for _filt.c in python file
"""
import matplotlib.pyplot as plt
import numpy as np
import math
import scipy.signal as signal


def test_filt():
    result = [
        0.000000, 0.000137, 0.000815, 0.002562, 0.005889, 0.011288, 0.019233,
        0.030185, 0.044583, 0.062853, 0.085405, 0.112631, 0.144910, 0.182604,
        0.226062, 0.275616, 0.331587, 0.394279, 0.463984, 0.540980, 0.625531,
        0.717891, 0.818299, 0.926982, 1.044156, 1.170025, 1.304781, 1.448605,
        1.601668, 1.764128, 1.936137, 2.117832, 2.309343, 2.510789, 2.722282,
        2.943923, 3.175803, 3.418008, 3.670611, 3.933681, 4.207277, 4.491451,
        4.786247, 5.091702, 5.407845, 5.734700, 6.072283, 6.420604, 6.779668,
        7.149473, 7.530011, 7.921267, 8.323222, 8.735851, 9.159125, 9.593012,
        10.037474, 10.492467, 10.957944, 11.433850, 11.920131, 12.416726,
        12.923575, 13.440613, 13.967767, 14.504963, 15.052124, 15.609171,
        16.176022, 16.752590, 17.338791, 17.934534, 18.539730, 19.154285,
        19.778101, 20.411081, 21.053123, 21.704124, 22.363983, 23.032598,
        23.709864, 24.395668, 25.089903, 25.792459, 26.503225, 27.222088,
        27.948938, 28.683664, 29.426155, 30.176296, 30.933973, 31.699070,
        32.471466, 33.251049, 34.037704, 34.831326, 35.631794, 36.438988,
        37.252792, 38.073097, 38.899784, 39.732742, 40.571857, 41.417011,
        42.268093, 43.124989, 43.987579, 44.855755, 45.729412, 46.608437,
        47.492718, 48.382149, 49.276615, 50.176014, 51.080242, 51.989189,
        52.902752, 53.820824, 54.743305, 55.670090, 56.601078, 57.536167,
        58.475258, 59.418255, 60.365063, 61.315582, 62.269718, 63.227379,
        64.188477, 65.152924, 66.120621, 67.091476, 68.065414, 69.042343,
        70.022179, 71.004852, 71.990273, 72.978340, 73.968979, 74.962112,
        75.957657, 76.955536, 77.955681, 78.958015, 79.962479, 80.968987,
        81.977470, 82.987839, 84.000031, 85.013985, 86.029640, 87.046936,
        88.065819, 89.086227, 90.108093, 91.131348, 92.155922, 93.181763,
        94.208824, 95.237045, 96.266380, 97.296791, 98.328224, 99.360619,
        100.393929, 101.428101, 102.463081, 103.498833, 104.535309, 105.572472,
        106.610275, 107.648682, 108.687660, 109.727165, 110.767143, 111.807549,
        112.848343, 113.889503, 114.930992, 115.972778, 117.014832, 118.057129,
        119.099640, 120.142326, 121.185150, 122.228088, 123.271103, 124.314178,
        125.357292, 126.400429, 127.443565, 128.486679, 129.529724, 130.572693,
        131.615585, 132.658371, 133.701035, 134.743515, 135.785797, 136.827866,
        137.869690, 138.911270, 139.952606, 140.993683, 142.034485, 143.075012,
        144.115250, 145.155182, 146.194809, 147.234131, 148.273117, 149.311783,
        150.350113, 151.388092, 152.425720, 153.462982, 154.499817, 155.536209,
        156.572174, 157.607712, 158.642807, 159.677460, 160.711685, 161.745453,
        162.778793, 163.811707, 164.844177, 165.876221, 166.907822, 167.938995,
        168.969727, 170.000000, 171.029846, 172.059235, 173.088135, 174.116547,
        175.144455, 176.171875, 177.198807, 178.225266, 179.251236, 180.276733,
        181.301773, 182.326340, 183.350464, 184.374146, 185.397385, 186.420181,
        187.442535, 188.464462, 189.485962, 190.507034, 191.527664, 192.547836,
        193.567551, 194.586823
    ]

    x = np.arange(0, 256)
    b, a =  [0.00013651, 0.00027302, 0.00013651], \
            [1., -1.96668139 , 0.96722743]

    sos = [0.00013651, 0.00027302, 0.00013651, 1., -1.96668139, 0.96722743]
    y_sos = signal.sosfilt(sos, x)
    y_lfilter = signal.lfilter(b, a, x)

    print(y_sos)
    print(y_lfilter)

    for i in range(len(y_sos)):
        print(y_sos[i] - result[i], y_lfilter[i] - result[i],
              y_sos[i] - y_lfilter[i])


if __name__ == '__main__':
    test_filt()
