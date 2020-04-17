from csv import reader
import os
from itertools import islice
import matplotlib.pyplot as pyp
import datetime
from typing import Tuple,List,Dict,Iterable,Optional

DATA_DIR='covid_data\\csse_covid_19_data\\csse_covid_19_daily_reports'
DATA_FILE='*.csv'

def moving_average(data: List,period: int) -> List[Optional[float]]:
    ma : List[Optional[float]] = []
    for i in range(0, len(data)):
        val = sum(data[i-period:i])/period
        ma.append( val if i >= period else None )
    
    return ma

def get_date_from_filename(path: str) -> datetime.date:
    sd = os.path.basename(path)
    sd = sd[0:sd.rfind(".")]
    return datetime.datetime.strptime(sd,"%m-%d-%Y")

def process_file(path: str, states: Iterable) -> Dict[str,int]:  #state/count pair
    def get_cnt_v1(line: List[str],state:str,country:str) -> int:
        return int(line[3]) if line[0] == state and line[1] == country else 0
    def get_cnt_v2(line: List[str],state:str,country:str) -> int:
        return int(line[7]) if line[2] == state and line[3] == country else 0

    with open(path,"tr") as f:
        df = reader(f,delimiter=',',quotechar='"')
        for line in islice(df,1):
            foo_get_cnt = get_cnt_v2 if 'FIPS' in line[0] else get_cnt_v1
        cnt = {key:0 for key in states}
        for line in df:
            for state in states:
                cnt[state] = cnt[state] + foo_get_cnt(line,state,'US')

    return cnt       

if __name__ == "__main__":
    # create a date/filename dictionary, sort the dates, and parse the files in date order
    states = {'New Jersey':"tab:blue",'New York':"tab:red"}
    files : Dict[datetime.date,str]= {}
    with os.scandir(DATA_DIR) as dir:
        for entity in dir:
            if entity.name.lower().endswith('.csv') and entity.is_file():
                files[ get_date_from_filename(entity.path) ] = entity.path 

    # the i-th element of dates is the date corresponding the count of the list
    # in the value of the cases dict
    dates = sorted([x for x in files.keys()]) # sorted list of dates
    cases : Dict[str,List[int]]= {x:[] for x in states.keys()} # key is the state, value is a list of counts

    for date in dates:
        for state,count in process_file(files[date],states.keys()).items():
            cases[state].append(count)    

    # calculate the daily difference (today - yesterday)
    diffs : Dict[str,List[int]] = {x:[] for x in states.keys()}
    reldiffs : Dict[str,List[float]] = {x:[] for x in states.keys()}
    for state in cases.keys():
        for j in range(0,len(dates)):
            diffs[state].append( cases[state][j] - cases[state][j-1] if j > 0 else 0 )
            reldiffs[state].append( diffs[state][j] / float(cases[state][j]) if cases[state][j] > 0 else 0 )

    
    fig,ax1 = pyp.subplots()
    ax2 = ax1.twinx()
    linestyles = ["-","--",":"]
    ax1.set_xlabel('date')
    ax1.set_ylabel('Total Cases')
    ax2.set_ylabel('Rel New Cases')
    for state,color in states.items():
        ax1.plot(dates,cases[state],color=color,linestyle=linestyles[0])
        ax1.plot(dates,moving_average(diffs[state],5),color=color,linestyle=linestyles[1])
        ax2.plot(dates,moving_average(reldiffs[state],5),color=color,linestyle=linestyles[2])    
    
    pyp.show()


