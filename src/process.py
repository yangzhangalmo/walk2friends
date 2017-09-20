import os
import pandas as pd

def folder_setup(city):
    '''setup folders for each city
    Args:
        city: city
    Returns:
    '''
    if not os.path.exists('dataset/'+city):
        os.mkdir('dataset/'+city)
        os.mkdir('dataset/'+city+'/process/')
        os.mkdir('dataset/'+city+'/emb/')
        os.mkdir('dataset/'+city+'/feature/')
        os.mkdir('dataset/'+city+'/result/')
        os.mkdir('dataset/'+city+'/defense/')

def data_process(city, cicnt):
    ''' process the raw dataset
    Args:
        city: city
    Returns:
        checkin: processed check-in data
        friends: friends list (asymetric) [u1, u2]
    '''

    checkin = pd.read_csv('dataset/'+city+'_'+str(cicnt)+'.checkin')
    friends = pd.read_csv('dataset/'+city+'_'+str(cicnt)+'.friends')

    return checkin, friends