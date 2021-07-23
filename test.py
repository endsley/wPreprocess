#!/usr/bin/env python

import wuml 
import numpy as np
import pandas as pd
import sys


#	We prefer dataFrame where 1st row have feature labels and the 1st column consists of sample id
#df = pd.read_csv ('./data/wine.csv', header=None)
#df = pd.read_csv ('./data/exposures_row_decimated.csv', header='infer',index_col=0)


## Decimate DataFrame with missing data
#df = pd.read_csv ('./data/chem.exposures.csv', header='infer',index_col=0)
#dfSmall = wuml.decimate_data_with_missing_entries(df, column_threshold=0.7, row_threshold=0.7,newDataFramePath='')


# Show label histogram after data decimation
df = pd.read_csv ('./data/exposures_row_decimated.csv', header='infer',index_col=0)
wuml.get_feature_histograms(df['finalga_best'].values, title='Histogram of Data Labels')




#foo = [wPr.center_and_scale]
#X = wPr.read_csv('./data/chem.exposures.csv', preprocess_list=foo)
#X = wPr.read_csv('./data/wine.csv', preprocess_list=foo)


