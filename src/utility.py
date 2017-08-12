import pandas as pd
from numpy.linalg import norm
from scipy.stats import entropy

def JSD(P, Q):
    _P = P / norm(P, ord=1)
    _Q = Q / norm(Q, ord=1)
    _M = 0.5 * (_P + _Q)
    return 0.5 * (entropy(_P, _M, base=2) + entropy(_Q, _M, base=2))


def js_utility(city, defense_name, checkin):
    ''' calculate the Jen-Shannon divergence as utility
    Args:
        city: city
        defense_name: 20_hiding_20
        checkin: checkin data
    Returns:        
    '''
    utility = pd.DataFrame(columns=['uid', 'js'])
    checkin_obf = pd.read_csv('dataset/'+city+'/defense/'+city+'_'+defense_name+'.checkin')
    
    for u in checkin_obf.uid.unique():
        u_checkin = checkin.loc[checkin.uid==u]
        u_checkin_obf = checkin_obf.loc[checkin_obf.uid==u]
        
        u_loc_distr = pd.DataFrame(u_checkin['locid'].value_counts()).reset_index()
        u_loc_distr.columns = ['locid', 'cnt']
        
        u_loc_distr_obf = pd.DataFrame(u_checkin_obf['locid'].value_counts()).reset_index()
        u_loc_distr_obf.columns = ['locid', 'cnt']
        
        union_loc = set.union(set(u_loc_distr['locid'].values),\
                              set(u_loc_distr_obf['locid'].values))

        extra_loc = list(union_loc-set(u_loc_distr['locid'].values))
        if len(extra_loc)>0:
            extra_loc = pd.DataFrame(extra_loc, columns=['locid'])
            extra_loc['cnt'] = 0
            u_loc_distr = pd.concat([u_loc_distr, extra_loc], ignore_index=True)
    
        extra_loc_obf = list(union_loc-set(u_loc_distr_obf['locid'].values))
        if len(extra_loc_obf)>0:
            extra_loc_obf = pd.DataFrame(extra_loc_obf, columns=['locid'])
            extra_loc_obf['cnt'] = 0
            u_loc_distr_obf = pd.concat([u_loc_distr_obf, extra_loc_obf], ignore_index=True)
        
        u_loc_distr = u_loc_distr.sort_values(by='locid').reset_index(drop=True)
        u_loc_distr_obf = u_loc_distr_obf.sort_values(by='locid').reset_index(drop=True)
        
        u_js = 1-JSD(u_loc_distr.cnt, u_loc_distr_obf.cnt)
        
        utility = utility.append({'uid':u, 'js':u_js}, ignore_index=True)

    utility.uid = utility.uid.apply(int)
    utility.to_csv('dataset/'+city+'/defense/'+city+'_'+defense_name+'.utility', index=False)