from csv import reader
import os
from itertools import islice
import matplotlib.pyplot as pyp
import datetime

DATA_DIR='covid_data\\csse_covid_19_data\\csse_covid_19_time_series'
DATA_FILE='time_series_covid19_confirmed_global.csv'
if __name__ == "__main__":
    with open(os.path.join(DATA_DIR,DATA_FILE)) as f:
        dr = reader(f,delimiter=',',quotechar='"')
        for line in islice(dr,1):
            dates = [datetime.datetime.strptime(x,"%m/%d/%y") for x in line[4:]]
            #print(','.join(dates))
        for line in islice(dr,1,None):
            if line[1] == 'US':
                data = [int(x) for x in line[4:]]

    diff=[0]
    for x in range(1,len(data)):
        diff.append(data[x]-data[x-1])

    pyp.plot(dates,diff)
    pyp.show()


