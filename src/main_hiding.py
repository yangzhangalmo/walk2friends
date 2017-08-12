import sys

from process import folder_setup, data_process
from defense import para_hiding
from emb import ul_graph_build, para_ul_random_walk, emb_train
from predict import feature_construct, unsuper_friends_predict

city = sys.argv[1]
cicnt = int(sys.argv[2])
ratio = int(sys.argv[3])# 10 20 30 40
ratio = ratio*1.0/100

folder_setup(city)
checkin, friends = data_process(city, cicnt)

defense_name = str(cicnt) + '_hiding_' + str(int(ratio*100))
print defense_name

checkin = para_hiding(city, defense_name, checkin, ratio)

ul_graph, lu_graph = ul_graph_build(checkin, 'locid')

model_name = str(cicnt) + '_locid_hiding_' + str(int(ratio*100))
print model_name

walk_len, walk_times = 100, 20 # maximal 100 walk_len, 20 walk_times

print 'walking'
para_ul_random_walk(city, model_name, checkin.uid.unique(), ul_graph, lu_graph,\
                    walk_len, walk_times)
print 'walk done'

print 'emb training'
emb_train(city, model_name)
print 'emb training done'

feature_construct(city, model_name, friends)
unsuper_friends_predict(city, model_name)
