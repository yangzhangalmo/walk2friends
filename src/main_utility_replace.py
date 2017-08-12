import sys

from process import data_process
from utility import js_utility

city = sys.argv[1]
cicnt = int(sys.argv[2])
ratio = int(sys.argv[3])# 10 20 30 40
ratio = ratio*1.0/100
step = int(sys.argv[4])

checkin, _ = data_process(city, cicnt)

defense_name = str(cicnt) + '_replace_' + str(int(ratio*100)) + '_' + str(int(step))

js_utility(city, defense_name, checkin)
