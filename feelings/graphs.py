from matplotlib import pyplot
from matplotlib.dates import date2num
from datetime import datetime, timedelta
import os

def create_graph(data, pic_name):
    X=[]
    for row in data:
        temp = datetime.strptime(row['date'], '%Y-%m-%d')
        X.append(temp)
	Y = [row['feelingavg']for row in data]
    if (X and Y):
        pyplot.clf()
        pyplot.plot(X, Y)
        pyplot.title( 'Graph' )
        pyplot.xlabel( 'Date' )
        pyplot.ylabel( 'Feeling' )
        pyplot.gcf().autofmt_xdate()
        pyplot.gca().set_xticks(X)
        pyplot.ylim([0,2])
        pyplot.gca().set_xticklabels([date.strftime("%d.%m.") for date in X])
        pyplot.savefig(os.path.dirname(os.path.abspath(__file__))+'/static/'+pic_name )
