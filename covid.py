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

    diff=[0.0]
    for x in range(1,len(data)):
        diff.append( (data[x]-data[x-1]) / data[x] if data[x] > 0 else 0 )

    fig,ax1 = pyp.subplots()
    color = ["tab:red","tab:blue"]
    ax1.set_xlabel('date')
    ax1.set_ylabel('Total Cases',color=color[0])
    ax1.plot(dates,data,color=color[0])
    ax2 = ax1.twinx()
    ax2.set_ylabel('Rel New Cases',color=color[1])
    ax2.plot(dates,diff,color=color[1])
    pyp.show()


