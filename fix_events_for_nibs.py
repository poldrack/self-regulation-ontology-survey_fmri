"""
fix event files for use with nibs
per https://nibetaseries.readthedocs.io/en/stable/auto_examples/plot_run_nibetaseries.html#display-the-minimal-dataset-necessary-to-run-nibs

1. the correct column has 1’s and 0’s corresponding to correct and incorrect, respectively. 
2. the condition column is renamed to trial_type 

nibs currently depends on the “correct” column being binary and the “trial_type” column to contain the trial types of interest.

we already meet #2 so we will recode our "Junk" regressor to meet #1

"""

import os
import pandas

subcode = 'sub-s061'
basedir = '/Users/poldrack/data_unsynced/surveyMedley/surveyMedleyData'

events_file = os.path.join(
    basedir,
    subcode,
    'func',
    f'{subcode}_task-surveyMedley_run-1_events.tsv'
)
events = pandas.read_csv(events_file, sep='\t')
correct = [int(not i) for i in events.junk]
events = events.assign(correct=correct)
events.to_csv(events_file,sep='\t')

