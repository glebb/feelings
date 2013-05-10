import matplotlib as mpl
mpl.use('Agg')

from matplotlib import pyplot
from matplotlib.dates import date2num
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from datetime import datetime, timedelta
import StringIO

def create_graph(data, cat):
    X = [datetime.strptime(row['date'], '%Y-%m-%d') for row in data]
    Y = [row['feelingavg']for row in data]
    if (len(X) > 0 and len(Y) > 0):
        pyplot.clf()
        pyplot.plot(X, Y)
        pyplot.title(cat)
        pyplot.xlabel( 'Date' )
        pyplot.ylabel( 'Feeling' )
        pyplot.gcf().autofmt_xdate()
        pyplot.gca().set_xticks(X)
        pyplot.ylim([0,2])
        pyplot.gca().set_xticklabels([date.strftime("%d.%m.") for date in X])
        canvas=FigureCanvas(pyplot.gcf())
        png_output = StringIO.StringIO()
        canvas.print_png(png_output)
        return png_output.getvalue() 