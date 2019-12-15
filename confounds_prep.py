# -*- coding: utf-8 -*-


"""
Created on Wed Jul 19 2018
Last edit: Sat Sep 01 2018
@author: kfinc

"""

import pandas as pd
import numpy as np


def temp_deriv(dataframe, quadratic=False):
    """Simple function that calculates temporal
    derivatives for each column of pandas dataframe.

    Parameters
    ----------
    dataframe: pandas dataframe with variable to
    calculate temporal derivarives

    Returns
    -------
    temp_deriv:  pandas dataframe including
    original columns and their temporal derivatives ('_td')
    and (optional) their quadratic terms

    """

    temp_deriv = dataframe.copy()

    for col in dataframe.columns:
        # --- backward difference algorithm
        temp = np.diff(dataframe[col], 1, axis=0)
        temp = np.insert(temp, 0, 0)
        temp = pd.DataFrame(temp)
        temp_deriv[col + '_td'] = temp

    if quadratic:
        for col in temp_deriv.columns:
            quad = temp_deriv[col] ** 2
            temp_deriv[col + '_quad'] = quad

    return temp_deriv


def outliers_fd_dvars(dataframe, fd=0.5, dvars=3):
    """Function that calculates motion outliers
    (frames with frame-wise displacement (FD)
    and DVARS above predefined threshold).

    Parameters
    ----------
    dataframe: pandas dataframe including columns with DVARS and FD
    fd:        threshold for FD (default: 0.5)
    dvars:     threshold for DVARS (+/-SD, default: 3)

    Returns
    -------
    outliers:  pandas dataframe including all outliers datapoints

    """

    df = dataframe.copy()
    df.fillna(value=0, inplace=True)

    dvars_out = np.absolute(df[df.columns[0]].astype(float)) > dvars
    fd_out = df[df.columns[1]].astype(float) > fd

    outliers = (dvars_out) | (fd_out)
    outliers = pd.DataFrame(outliers.astype('int'))
    outliers.columns = ['scrubbing']

    return outliers


def confounds_prep(confounds, use_compcor=False):
    """Function that calculates motion outliers
    (frames with frame-wise displacement (FD)
    and DVARS above predefined threshold).

    Parameters
    ----------
    confounds: pandas dataframe with fmriprep confound output

    Returns
    -------
    confounds_clean:  pandas dataframe with processed confounds

    """

    confounds_motion = temp_deriv(
        confounds[
            confounds.filter(
                regex='trans_x|trans_y|trans_z|rot_x|rot_y|rot_z').columns],
        quadratic=False)
    confounds_acompcor = confounds[
        confounds.filter(regex='a_comp_cor').columns]
    # NB: THIS IS INCORRECT, SHOULD BE ONE COLUMN PER SCRUBBED
    # LEAVING OUT FOR NOW
    # confounds_scrub = outliers_fd_dvars(
    #    confounds[confounds.filter(
    #       regex='^std_dvars|framewise').columns], fd=0.5, dvars=3)
    confounds_fd_dvars = confounds[
        confounds.filter(regex='^std_dvars|framewise').columns]
    confounds_fd_dvars.iloc[0, :] = [0, 0]

    if use_compcor:
        confounds_clean = pd.concat(
            [confounds_motion,
             confounds_acompcor,
             confounds_fd_dvars],
            axis=1)
    else:
        confounds_clean = pd.concat(
            [confounds_motion,
             confounds_fd_dvars],
            axis=1)

    return confounds_clean
