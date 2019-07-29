import pandas as pd 
import numpy as np
import ast
def split_seq_index(x):
    ind = np.where(x > 500)
    if 0 not in ind[0]:
        z = np.zeros(len(ind[0]) + 1, dtype = int)
        k = np.asarray(ind[0])
        z[1:len(x) + 1] = ind[0].reshape(len(k))
        return z
    else:
        return ind[0]

def get_timeDiff(dFrame):
	time_stamp = dFrame.groupby(['Device'])['T']
	time_diff = time_stamp.apply(np.ediff1d)
	time_diff_data = pd.Series.to_frame(time_diff)

	return time_diff_data

def get_splitIndex(dFrame):
	dFrame['split_index'] = dFrame['T'].apply(split_seq_index)


	return dFrame


def get_series(x, grouped_data):
    #print(dev.values[0])
    device_n = x['Device']
    #print(grouped_data.get_group(device_n))
    gd = grouped_data.get_group(device_n)
    split0 = x['split_index'].tolist()
    split0.append(len(gd))
    lx = []
    ly = []
    lz = []
    for ind, i in enumerate(split0):
        #print(len(split[0]))
        if ind == len(split0) - 1:
            #print('k')
            break
            
        else:
            lx.append(gd.iloc[i:split0[ind+1], 1].tolist())
            ly.append(gd.iloc[i:split0[ind+1], 2].tolist())
            lz.append(gd.iloc[i:split0[ind+1], 3].tolist())
    return pd.Series([lx, ly, lz])


def get_series_num(x, grouped_data):
#     print(split)
#     print(dev)
    device_n = x['Device']
    
    #print(grouped_data.get_group(device_n))
    gd = grouped_data.get_group(device_n)
    #print(device_n)
    lx = []
    split0 = x['split_index'].tolist()
    split0.append(len(gd))
    #print(split0)
    #print(x['Device'], len(gd))

    for ind, i in enumerate(split0):
        #print(len(split[0]))
        if ind == len(split0) -1:
            #print('k')
            break
            
        else:
            #print((np.ones(split0[ind + 1] - i) + ind + 1))
            lx += (np.ones(split0[ind + 1] - i, dtype=int) + ind).tolist()
            
    return lx

def get_seqID_list(dFrame):
	list_id = dFrame['seq_id'].tolist()
	f_list_id = [item for sublist in list_id for item in sublist]

	return f_list_id

def proper_format(data_f, col):
    df2 = pd.DataFrame()
    df2['Device'] = data_f['Device']
    for i in col:
        #print(i)
        try:
            data_f[i] = data_f[i].apply(ast.literal_eval)
        except:
            pass
        s = data_f.apply(lambda x: pd.Series(x[i]), axis=1).stack().reset_index(level=1, drop=True)
        re_name = i + '_f'
        print(re_name)
        s.name = re_name

        #df2 = data_f.drop(i, axis=1).join(s)
        df2 = df2.join(s)

        #df2[re_name] = pd.Series(df2[re_name], dtype=object)
        #print(df2.columns)
    return df2

def merge_data(A, B, C, col_list):
    k = pd.concat([A, B[col_list[0]], C[col_list[1]]], axis = 1)
    return k