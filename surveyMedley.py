"""
class for surveyMedley analysis
"""

import sys
import os
import pandas


class surveyMedley(object):
    def __init__(self, basedir, subcode):
        
        self.basedir = basedir
        assert os.path.exists(basedir)
        
        self.subcode = subcode
        self.subdir = os.path.join(basedir, subcode)
        assert os.path.exists(self.subdir)

    def load_confounds(self):
        """ load confounds"""
        self.confound_file = os.path.join(
            self.basedir,
            self.subcode,,
            'func',
            f'{subcode}_task-surveyMedley_run-1_desc-confounds_regressors.tsv'
        )
        self.confound_data = pandas.read_csv(self.confound_file)


def __main__:
    try:
        sub = sys.argv[1]
    except:
        sub = 'sub-s061'
        print('no sub specified, using default')

    print('=========================================')
    print(f'Processing {sub}')
    print('=========================================')

