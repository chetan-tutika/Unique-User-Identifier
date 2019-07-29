import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from helpers import *
import ast

train_data = pd.read_csv('/media/chetan/de104728-db4d-4432-a0d9-ddcfc771ae84/CIS520/Project/train.csv')
test_data = pd.read_csv('/media/chetan/de104728-db4d-4432-a0d9-ddcfc771ae84/CIS520/Project/test.csv')
questions = pd.read_csv('/media/chetan/de104728-db4d-4432-a0d9-ddcfc771ae84/CIS520/Project/questions.csv')

## Shape of Train set = (29563983, 5)

## train_data.head()
#         T	            X	       Y	       Z	Device
# 0	1.336645e+12	0.340509	8.308413	4.140585	7
# 1	1.336645e+12	0.381370	8.390134	4.249548	7
# 2	1.336645e+12	0.272407	8.471856	4.018002	7
# 3	1.336645e+12	0.149824	8.430995	4.290409	7
# 4	1.336645e+12	0.272407	8.430995	4.481094	7

## test_data.shape = (27007200, 5)

## test_data.head()
#         T         	X	       Y	        Z	   SequenceId
# 0	1.364277e+12	8.662541	4.018003	-1.334794	100006
# 1	1.364277e+12	12.326415	5.202973	-1.688923	100006
# 2	1.364277e+12	8.090487	1.253072	0.544814	100006
# 3	1.364277e+12	10.923519	-0.858082	-1.021526	100006
# 4	1.364277e+12	7.763598	-0.108963	-1.171350	100006

## questions.shape = (90024, 3)
#  QuestionId	SequenceId	QuizDevice
# 0	1	100006	593
# 1	2	100011	751
# 2	3	100012	1027
# 3	4	100033	761
# 4	5	100044	45

train_dataC = train_data.copy()

## Get the time differnce in each group
time_diff_d = get_timeDiff(train_dataC)

time_diff_w_splitIndex = get_splitIndex(time_diff_d)


time_diff_w_splitIndex = time_diff_w_splitIndex.drop('T', axis = 1)

grouped_data = train_data.groupby(['Device'])

time_diff_w_splitIndex = time_diff_w_splitIndex.reset_index()

time_diff_w_splitIndex = time_diff_w_splitIndex.reindex(columns=[*time_diff_w_splitIndex.columns.tolist(), 'X', 'Y', 'Z'], fill_value=np.nan)

#time_diff_w_splitIndex[['X', 'Y', 'Z']] = time_diff_w_splitIndex.apply(get_series, axis=1)

time_diff_w_splitIndex[['X', 'Y', 'Z']] = time_diff_w_splitIndex.apply(lambda x: get_series(x, grouped_data), axis=1)
#print('key error1')

time_diff_w_splitIndex['seq_id'] = time_diff_w_splitIndex.apply(lambda x: get_series_num(x, grouped_data), axis = 1)

#print('key error')

flat_list_id = get_seqID_list(time_diff_w_splitIndex)
#print('key')

train_dataC["seq_id"] = flat_list_id

print('key1')
time_diff_w_splitIndex.to_csv(r'trainData_seqID.csv')
print('key2')
train_dataC.to_csv(r'sequences.csv')

#time_diff_w_splitIndex = pd.read_csv('trainData_seqID.csv')

#time_small = time_diff_w_splitIndex.head(100000)
prX = proper_format(time_diff_w_splitIndex, ['X'])

prY = proper_format(time_diff_w_splitIndex, ['Y'])

prZ = proper_format(time_diff_w_splitIndex, ['Z'])
#print(proper_data.head())

proper_data = merge_data(prX, prY, prZ, ['Y_f', 'Z_f'])


proper_data.to_csv(r'proper_data.csv')