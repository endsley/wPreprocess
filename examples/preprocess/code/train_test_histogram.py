#!/usr/bin/env python
import os
import sys
if os.path.exists('/home/chieh/code/wPlotLib'):
	sys.path.insert(0,'/home/chieh/code/wPlotLib')
if os.path.exists('/home/chieh/code/wuML'):
	sys.path.insert(0,'/home/chieh/code/wuML')


import wuml
import sklearn
import wplotlib
from wplotlib import histograms


data = wuml.wData(xpath='../../data/Chem_decimated_imputed.csv', batch_size=20, 
					label_type='continuous', label_column_name='finalga_best', 
					first_row_is_label=True, columns_to_ignore=['id'])

# data_path : will save the the files gestAge_train.csv and gestAge_test.csv to ../../data folder
# test_percentage : 0.1 implies that 90% will be training and 10% will be test
X_train, X_test, y_train, y_test = wuml.split_training_test(data, data_name='gestAge', data_path='../../data/', save_as='DataFrame',
															test_percentage=0.1, xdata_type="%.4f", ydata_type="%d")
#	Here, we will plot out the histogram of labels between training and test
H = histograms(y_train, num_bins=10, title='Training Label Distribution', 
			subplot=121, facecolor='green', α=0.5, normalize=False)
histograms(y_test, num_bins=10, title='Test Label Distribution', 
			subplot=122, facecolor='green', α=0.5, normalize=False)
H.show()


