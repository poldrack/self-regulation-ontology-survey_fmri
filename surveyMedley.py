"""
class for surveyMedley analysis
"""

import sys
import os
import pandas
from confounds_prep import confounds_prep

class surveyMedley(object):
    def __init__(self,
                 basedir,
                 subcode):
        self.basedir = basedir
        assert os.path.exists(basedir)
        self.subcode = subcode
        self.subdir = os.path.join(basedir, subcode)
        assert os.path.exists(self.subdir)

    def loadConfounds(self):
        """ load confounds"""
        self.confound_file = os.path.join(
            self.basedir,
            self.subcode,
            'func',
            f'{self.subcode}_task-surveyMedley_run-1_desc-confounds_regressors.tsv'
        )
        confound_data = pandas.read_csv(self.confound_file,
                                        sep='\t')
        self.confounds = confounds_prep(
            confound_data,
            use_compcor=True)


if __name__ == "__main__":
    try:
        sub = sys.argv[1]
    except IndexError:
        sub = 'sub-s061'
        print('no sub specified, using default')

    print('=========================================')
    print(f'Processing {sub}')
    print('=========================================')

    basedir = '/Users/poldrack/data_unsynced/surveyMedley/surveyMedleyData'
    sm = surveyMedley(basedir, sub)
    sm.loadConfounds()