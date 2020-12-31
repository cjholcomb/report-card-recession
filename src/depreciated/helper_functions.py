import pandas as pd
import numpy as np 




def third_quarter(index):
    '''imports only every 3rd quarter row- required to import entire dataset (too large)
    Referenced in feature_space

    params: index, int
    returns: boolean'''
    if index == 0:
        return False
    elif (index - 3) % 4 == 0:
        return False
    else:
        return True

### Help functions for target calculation ###

def calc_nadir(s):
    assert isinstance(s, pd.Series)
    return s.min()

def calc_nadir_qtr(s):
    return s.argmin()

def calc_pre_peak(s):
    return s[ : s.argmin()].max()

def calc_pre_peak_quarter(s):
    try:
        qtr = s[ : s.argmin()].argmax()
    except:
        qtr = None
    return qtr

def calc_post_peak(s):
    return s[s.argmin() : ].max()

def calc_post_peak_qtr(s):
    return s[s.argmin() : ].argmax() + s.argmin()