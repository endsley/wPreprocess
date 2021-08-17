#!/usr/bin/env python

import wuml 
import numpy as np
import scipy.stats
from wplotlib import histograms
from wplotlib import lines
	
#l2x_synthetic_blocks.csv  l2x_synthetic.csv         l2x_synthetic_label.csv

wuml.set_terminal_print_options(precision=2)
data = wuml.wData(xpath='examples/data/l2x_synthetic.csv', ypath='examples/data/l2x_synthetic_label.csv', label_type='continuous', batch_size=20)
d = data.X.shape[1]

θˢ = [(20,'relu'),(20,'relu'),(20,'relu'),(d*2,'none')]
#θᴾ = [(200,'relu'),(10,'relu'),(10,'relu'),(1,'none')]
θᴾ = [(1,'none')]

P = wuml.l2x(data, max_epoch=5000, learning_rate=0.001,
				selector_network_structure=θˢ,predictor_network_structure=θᴾ)
P.train()
ŷ = P(data.X)

S = P.get_Selector(data.X)
import pdb; pdb.set_trace()
#out = wuml.output_regression_result(data.Y, ŷ)

