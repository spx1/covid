from csv import reader
import os
from itertools import islice
import matplotlib.pyplot as pyp
import datetime
from typing import Tuple,List

DATA_DIR='covid_data\\csse_covid_19_data\\csse_covid_19_daily_reports'
DATA_FILE='*.csv'

def moving_average(data: List[int],period: int) -> List[float]:
    ma = []
    for i in range(0,min(period,len(data))):
        ma.append(None)

    for i in range(min(period,len(data)),len(data)):
        ma.append(sum(data[i-period:i]) / period)   
    return ma

def get_date_from_filename(path: str) -> datetime.date:
    sd = os.path.basename(path)
    sd = sd[0:sd.rfind(".")]
    return datetime.datetime.strptime(sd,"%m-%d-%Y")

def process_file(path: str) -> Tuple[datetime.date,int]:
    def get_cnt_v1(line: List[str],state:str,country:str) -> int:
        return int(line[3]) if line[0] == state and line[1] == country else 0
    def get_cnt_v2(line: List[str],state:str,country:str) -> int:
        return int(line[7]) if line[2] == state and line[3] == country else 0

    with open(path,"tr") as f:
        df = reader(f,delimiter=',',quotechar='"')
        for line in islice(df,1):
            foo_get_cnt = get_cnt_v2 if 'FIPS' in line[0] else get_cnt_v1
        cnt = 0
        for line in df:
            cnt = cnt + foo_get_cnt(line,'New Jersey','US')

    return (get_date_from_filename(path),cnt)
        

if __name__ == "__main__":
    data={}
    with os.scandir(DATA_DIR) as dir:
        for entity in dir:
            if entity.name.lower().endswith('.csv') and entity.is_file():
                dt,cnt = process_file(entity.path)
                data[dt]=cnt

    dates = sorted([x for x in data.keys()])
    counts = []
    diffs = []
    for j in dates:
        counts.append(data[j])
        ts = datetime.timedelta(days=1)
        diffs.append( (data[j] - data[j-ts]) if (j-ts) in dates else 0)
    rdiffs = []
    for i in range(0,len(counts)):
        rdiffs.append( diffs[i] / counts[i] if counts[i] > 0 else 0 )

    
    
    fig,ax1 = pyp.subplots()
    color = ["tab:red","tab:blue","tab:green"]
    ax1.set_xlabel('date')
    ax1.set_ylabel('Total Cases',color=color[0])
    ax1.plot(dates,counts,color=color[0])
    ax1.plot(dates,moving_average(diffs,3),color=color[2])
    ax2 = ax1.twinx()
    ax2.set_ylabel('Rel New Cases',color=color[1])
    ax2.plot(dates,moving_average(rdiffs,3),color=color[1])
    pyp.show()


