import os

import pandas as pd
import numpy as np
from sklearn.metrics import roc_auc_score
from scipy.spatial.distance import cosine, euclidean, correlation, chebyshev,\
    braycurtis, canberra, cityblock, sqeuclidean


def pair_construct(u_list, friends):
    ''' construct users pairs
    Args:
        u_list: user list
    Returns:
        pair: u1, u2, label
    '''
    
    pair_p = friends.loc[(friends.u1.isin(u_list))&\
                        (friends.u2.isin(u_list))].copy()

    pair_n = pd.DataFrame(np.random.choice(u_list, 3*pair_p.shape[0]),\
                          columns=['u1'])
    pair_n['u2'] = np.random.choice(u_list, 3*pair_p.shape[0])

    pair_n = pair_n.loc[pair_n.u1!=pair_n.u2]
    pair_n = pair_n.loc[pair_n.u1<pair_n.u2]
    pair_n = pair_n.drop_duplicates().reset_index(drop=True)
    # delete friends inside
    pair_n = pair_n.loc[~pair_n.set_index(list(pair_n.columns)).index.isin(pair_p.set_index(list(pair_p.columns)).index)]
    pair_n = pair_n.loc[np.random.permutation(pair_n.index)].reset_index(drop=True)
    
    pair_n = pair_n.loc[0:1*pair_p.shape[0]-1, :]# down sampling

    pair_p['label'] = 1
    pair_n['label'] = 0

    pair = pd.concat([pair_p, pair_n], ignore_index=True)
    pair = pair.reset_index(drop=True)

    return pair

def feature_construct(city, model_name, friends, walk_len=100, walk_times=20, num_features=128):
    '''construct the feature matrixu2_checkin
    Args:
        city: city
        model_name: 20_locid
        friends: friends list (asymetric) [u1, u2]
        walk_len: walk length
        walk_times: walk times
        num_features: dimension for vector        
    Returns:
    '''

    if os.path.exists('dataset/'+city+'/feature/'+city+'_'+model_name+'_'+\
                      str(int(walk_len))+'_'+str(int(walk_times))+'_'+str(int(num_features))+'.feature'):
        os.remove('dataset/'+city+'/feature/'+city+'_'+model_name+'_'+\
                  str(int(walk_len))+'_'+str(int(walk_times))+'_'+str(int(num_features))+'.feature')

    emb = pd.read_csv('dataset/'+city+'/emb/'+city+'_'+model_name+'_'+\
                      str(int(walk_len))+'_'+str(int(walk_times))+'_'+str(int(num_features))+'.emb',\
                      header=None, skiprows=1, sep=' ')
    emb = emb.rename(columns={0:'uid'})# last column is user id
    emb = emb.loc[emb.uid>0]# only take users, no loc_type, not necessary

    pair = pair_construct(emb.uid.unique(), friends)

    for i in range(len(pair)):
        u1 = pair.loc[i, 'u1']
        u2 = pair.loc[i, 'u2']
        label = pair.loc[i, 'label']

        u1_vector = emb.loc[emb.uid==u1, range(1, emb.shape[1])]
        u2_vector = emb.loc[emb.uid==u2, range(1, emb.shape[1])]

        i_feature = pd.DataFrame([[u1, u2, label,\
                                   cosine(u1_vector, u2_vector),\
                                   euclidean(u1_vector, u2_vector),\
                                   correlation(u1_vector, u2_vector),\
                                   chebyshev(u1_vector, u2_vector),\
                                   braycurtis(u1_vector, u2_vector),\
                                   canberra(u1_vector, u2_vector),\
                                   cityblock(u1_vector, u2_vector),\
                                   sqeuclidean(u1_vector, u2_vector)]])

        i_feature.to_csv('dataset/'+city+'/feature/'+city+'_'+model_name+'_'+\
                         str(int(walk_len))+'_'+str(int(walk_times))+'_'+str(int(num_features))+'.feature',\
                         index = False, header = None, mode = 'a')

def unsuper_friends_predict(city, model_name, walk_len=100, walk_times=20, num_features=128):
    ''' unsupervised prediction
    Args:
        city: city
        model_name: 20_locid
        walk_len: walk length
        walk_times: walk times
        num_features: dimension for vector
    Returns:
    ''' 
    feature = pd.read_csv('dataset/'+city+'/feature/'+city+'_'+model_name+'_'+\
                         str(int(walk_len))+'_'+str(int(walk_times))+'_'+str(int(num_features))+'.feature',\
                          names = ['u1', 'u2', 'label',\
                                   'cosine', 'euclidean', 'correlation', 'chebyshev',\
                                   'braycurtis', 'canberra', 'cityblock', 'sqeuclidean'])

    auc_res = []
    for i in ['cosine', 'euclidean', 'correlation', 'chebyshev',\
              'braycurtis', 'canberra', 'cityblock', 'sqeuclidean']:
        i_auc = roc_auc_score(feature.label, feature[i])
        if i_auc < 0.5: i_auc = 1-i_auc
        print i, i_auc
        auc_res.append(i_auc)

    pd.DataFrame([auc_res],\
                 columns=['cosine', 'euclidean', 'correlation', 'chebyshev',\
                          'braycurtis', 'canberra', 'cityblock', 'sqeuclidean']).to_csv(\
                 'dataset/'+city+'/result/'+city+'_'+model_name+'_'+\
                 str(int(walk_len))+'_'+str(int(walk_times))+'_'+str(int(num_features))+'.result', index=False)
