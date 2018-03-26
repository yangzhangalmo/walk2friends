import multiprocessing as mp

import pandas as pd
import numpy as np
from joblib import Parallel, delayed

from gensim.models import word2vec

def ul_graph_build(checkin, loc_type):
    ''' build all the network
    Args:
        checkin: checkin data
        loc_type: locid, gridcatid...
    Returns:
        ul_graph: graph data
        lu_graph:
    '''

    ul_graph = checkin.groupby('uid')[loc_type].value_counts()*1.0/checkin.groupby('uid').size()
    ul_graph = pd.DataFrame(ul_graph)
    ul_graph.columns = ['weight']
    ul_graph = pd.DataFrame(ul_graph).reset_index()
    ul_graph.columns = ['uid', 'node2', 'weight']

    lu_graph = checkin.groupby(loc_type).uid.value_counts()*1.0/checkin.groupby(loc_type).size()
    lu_graph = pd.DataFrame(lu_graph)
    lu_graph.columns = ['weight']
    lu_graph = pd.DataFrame(lu_graph).reset_index()
    lu_graph.columns = ['locid', 'node2', 'weight']

    return ul_graph, lu_graph

def para_ul_random_walk(city, model_name, ulist, ul_graph, lu_graph, walk_len, walk_times):
    ''' parallel random walk on user location network
    Args:
        city: city
        model_name: 20_locid
        ulist: user list
        ul_graph, lu_graph: graph data (pandas df)
        walk_len: walk length
        walk_times: walk times
    Returns:
    '''

    core_num = mp.cpu_count()
    print core_num
    # do not use shared memory
    Parallel(n_jobs = core_num)(delayed(ul_random_walk_core)(\
        city, model_name, u, ul_graph, lu_graph, walk_len, walk_times) for u in ulist)

def ul_random_walk_core(city, model_name, start_u, ul_graph, lu_graph, walk_len, walk_times):
    ''' random walks from start_u on user location network
    Args:
        city: city
        model_name: 20_locid
        start_u: starting user in a random walk
        ul_graph, lu_graph: graph data (pandas df)
        walk_len: walk length
        walk_times: walk times
    Returns:
    '''

    np.random.seed()
    temp_walk = np.zeros((1, walk_len))# initialize random walk

    for i in range(walk_times):
        temp_walk[:, 0] = start_u#
        curr_u = start_u
        flag = 0 # flag 0, user, flag 1, location
        for j in range(walk_len-1):
            if flag == 0:# at social network
                temp_val = ul_graph.loc[ul_graph.uid==curr_u]
                flag = 1
            elif flag == 1: # at location
                temp_val = lu_graph.loc[lu_graph.locid==curr_u]
                flag = 0
            # sample with weights
            next_u = np.random.choice(temp_val['node2'].values, 1, p=temp_val['weight'])[0]
            curr_u = next_u
            if flag == 1: temp_walk[:, j+1] = -next_u # location id is minus
            else: temp_walk[:, j+1] = next_u

        pd.DataFrame(temp_walk).to_csv('dataset/'+city+'/emb/'+\
                                       city+'_'+model_name+'.walk',\
                                       header=None, mode='a', index=False)

def emb_train(city, model_name, walk_len=100, walk_times=20, num_features=128):
    ''' train vector model
    Args:
        city: city
        model_name: 20_locid
        walk_len: walk length
        walk_times: walk times
        num_features: dimension for vector
    Returns:
    '''

    walks = pd.read_csv('dataset/'+city+'/emb/'+city+'_'+model_name+'.walk',\
                        header=None, error_bad_lines=False)

    walks = walks.loc[np.random.permutation(len(walks))]
    walks = walks.reset_index(drop=True)
    walks = walks.applymap(str) # gensim only accept list of strings
    
    print 'walk_len', walk_len, 'walk_times', walk_times, 'num_features', num_features

    min_word_count = 10
    num_workers = mp.cpu_count()
    context = 10
    downsampling = 1e-3

    # gensim does not support numpy array, thus, walks.tolist()
    walks = walks.groupby(0).head(walk_times).values[:,:walk_len].tolist()

    emb = word2vec.Word2Vec(walks,\
                            sg=1,\
                            workers=num_workers,\
                            size=num_features, min_count=min_word_count,\
                            window=context, sample=downsampling)
    print 'training done'
    emb.wv.save_word2vec_format('dataset/'+city+'/emb/'+city+'_'+model_name+'_'+\
                                str(int(walk_len))+'_'+str(int(walk_times))+'_'+str(int(num_features))+'.emb')
