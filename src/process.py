import pandas as pd

def data_process(city, cicnt):
    ''' process the raw dataset
    Args:
        city: city
    Returns:
        checkin: processed check-in data
        friends: friends list (asymetric) [u1, u2]
    '''

    checkin = pd.read_csv('dataset/'+city+'/process/'+\
                          city+'_'+str(cicnt)+'.checkin')
    checkin['time'] = pd.to_datetime(checkin['time'], format='%Y-%m-%d %H:%M:%S')
    friends = pd.read_csv('dataset/'+city +'/process/'+\
                          city+'_'+str(cicnt)+'.friends')

    return checkin, friends