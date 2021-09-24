# wuml
## Chieh's quick ML library
## Pip Installation
```sh
pip install wuml
```


## Distribution Modeling
[KDE Example](https://github.com/endsley/wuML/blob/main/examples/distribution_modeling/markdown/basicKDE_estimate.md)



```python
#!/usr/bin/env python

import wuml 

'''
	This code loads data with missing entries at random as a wData type
	It will automatically remove the features and samples that are missing too many entries
	On the decimated data, it will perform imputation
	It will lastly save and export the results to a csv file
'''

data = wuml.wData('../data/chem.exposures.csv', row_id_with_label=0)
dataDecimated = wuml.decimate_data_with_missing_entries(data, column_threshold=0.95, row_threshold=0.9,newDataFramePath='')
#	column_threshold=0.95, this will keep features that are at least 95% full


X = wuml.impute(dataDecimated)		# perform mice imputation
X.to_csv('../data/Chem_decimated_imputed.csv')	

```
![Image](https://github.com/endsley/wuML/blob/main/img/BeforeAfterMissingPercentage.png?raw=true)


#### **Code Feature Results**
## Notice that all the missing entries have been filled

```python
(Pdb) X.info()
<class 'pandas.core.frame.DataFrame'>
Int64Index: 1122 entries, 0 to 1176
Data columns (total 24 columns):
 #   Column        Non-Null Count  Dtype  
---  ------        --------------  -----  
 0   Unnamed: 0    1122 non-null   float64
 1   id            1122 non-null   float64
 2   MBP           1122 non-null   float64
 3   MBzP          1122 non-null   float64
 4   MCNP          1122 non-null   float64
 5   MCOP          1122 non-null   float64
 6   MCPP          1122 non-null   float64
 7   MECPP         1122 non-null   float64
 8   MEHHP         1122 non-null   float64
 9   MEHP          1122 non-null   float64
 10  MEOHP         1122 non-null   float64
 11  MEP           1122 non-null   float64
 12  MiBP          1122 non-null   float64
 13  preBMI        1122 non-null   float64
 14  preBMI_cat    1122 non-null   float64
 15  ppsex         1122 non-null   float64
 16  ISAGE         1122 non-null   float64
 17  mage_cat      1122 non-null   float64
 18  edu_cat       1122 non-null   float64
 19  currjob_cat   1122 non-null   float64
 20  marital_cat   1122 non-null   float64
 21  smk_cat       1122 non-null   float64
 22  alc_cat       1122 non-null   float64
 23  finalga_best  1122 non-null   float64
dtypes: float64(24)
memory usage: 219.1 KB
```





## Example of basic regression requiring Neural Network TensorFlow
```python
#!/usr/bin/env python


#	The idea of training a neural network boils down to 3 steps
#		1. Define a network structure
#			Example: This is a 3 layer network with 100 node width
#				networkStructure=[(100,'relu'),(100,'relu'),(1,'none')]
#		2. Define a cost function
#		3. Call train()


import wuml
import numpy as np
import torch
import wplotlib


data = wuml.wData(xpath='examples/data/regress.csv', ypath='examples/data/regress_label.csv', batch_size=20)

def costFunction(x, y, ŷ, ind):
	ŷ = torch.squeeze(ŷ)
	return torch.sum((y- ŷ) ** 2)	

bNet = wuml.basicNetwork(costFunction, data, networkStructure=[(100,'relu'),(100,'relu'),(1,'none')], max_epoch=500, learning_rate=0.001)
bNet.train()

#	Test out on test data
newX = np.expand_dims(np.arange(0,5,0.1),1)
Ŷ = bNet(newX, output_type='ndarray')		#Takes Numpy array or Tensor as input and outputs a Tensor

#	plot the results out
splot = wplotlib.scatter()
splot.add_plot(data.X, data.Y, marker='o')

lp = wplotlib.lines()	
lp.add_plot(newX, Ŷ)

splot.show(title='Basic Network Regression', xlabel='x-axis', ylabel='y-axis')

```
![Image](https://github.com/endsley/wuML/blob/main/img/Regression.png?raw=true)


## Example of basic classification 
```python
#!/usr/bin/env python

import wuml
import numpy as np
import torch
import torch.nn as nn
import wplotlib


#	The idea of training a neural network boils down to 3 steps
#		1. Define a network structure
#			Example: This is a 3 layer network with 100 node width
#				networkStructure=[(100,'relu'),(100,'relu'),(1,'softmax')]
#		2. Define a cost function
#		3. Call train()

data = wuml.wData(xpath='examples/data/wine.csv', ypath='examples/data/wine_label.csv', batch_size=20)

def costFunction(x, y, ŷ, ind):
	lossFun = nn.CrossEntropyLoss() 
	loss = lossFun(ŷ, y) #weird from pytorch, dim of y is 1, and ŷ is 20x3	
	return loss


#It is important for pytorch that with classification, you need to define Y_dataType=torch.int64
bNet = wuml.basicNetwork(costFunction, data, networkStructure=[(100,'relu'),(100,'relu'),(3,'none')], 
						Y_dataType=torch.int64, max_epoch=3000, learning_rate=0.001)
bNet.train()
netOutput = bNet(data.X)

#	Output Accuracy
_, Ŷ = torch.max(netOutput, 1)

Acc = wuml.accuracy(Y, Ŷ)
#Acc= accuracy_score(data.Y, Ŷ.cpu().numpy())
print('Accuracy: %.3f'%Acc)

```

#### **Code Output**
```python
Network Info:
	Learning rate: 0.001
	Max number of epochs: 3000
	Cuda Available: True
	Network Structure
		Linear(in_features=13, out_features=100, bias=True) , relu
		Linear(in_features=100, out_features=100, bias=True) , relu
		Linear(in_features=100, out_features=3, bias=True) , none
	epoch: 3000, Avg Loss: 0.0442, Learning Rate: 0.00001563Accuracy: 0.989

```


## Distribution Estimation from Samples Via KDE
```python
#!/usr/bin/env python

import wuml 
import numpy as np
import scipy.stats
from wplotlib import histograms
from wplotlib import lines
	

data = wuml.wData(X_npArray=np.random.randn(1000))
Pₓ = wuml.KDE(data)

X = np.arange(-3,3,0.05)
realProb = scipy.stats.norm(0, 1).pdf(X)
estimatedProb = Pₓ(X)
newX = Pₓ.generate_samples(300)

textstr = 'Blue: True Density\nRed: KDE estimated density\nGreen: Histogram sampled from KDE'
lp = lines()
H = histograms()
lp.add_plot(X,realProb, color='blue', marker=',')
lp.add_plot(X,estimatedProb, color='red', marker=',')
lp.add_text(X,estimatedProb, textstr, β=0.8)
H.histogram(newX, num_bins=10, title='Using KDE to Estimate Distributions', facecolor='green', α=0.5, showImg=False, normalize=True)
H.show()

```
![Image](https://github.com/endsley/wuML/blob/main/img/KDE_estimation.png?raw=true)


## Determine Sample weights based on rarity  
```python
#!/usr/bin/env python

import wuml 
import numpy as np
import scipy.stats
from wplotlib import histograms
from wplotlib import lines
	
'''
	Identifies a weight associated with each sample based on its likelihood. 
	Given p(X1) > p(Xi) for all i
	Using KDE if p(X1)/p(X2)=2  the weight for X1 = 1, and X2 = 2
	This means that if X1 is the most likely samples and if X1 is 
	2 times more likely than X2, then X1 would have a weight of 1
	and X2 would have a weight of 2.
	This weight can then be used to balance the sample importance for regression

'''

data = wuml.wData('examples/data/Chem_decimated_imputed.csv', row_id_with_label=0)
data.delete_column('id')	# the id should not be part of the likelihood 
sample_weights = wuml.get_likelihood_weight(data)
sample_weights.to_csv('examples/data/Chem_sample_weights.csv', include_column_names=False)
```

