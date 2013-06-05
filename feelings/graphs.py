import matplotlib as mpl
mpl.use('Agg')

from matplotlib import pyplot
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from datetime import datetime
import StringIO

def create_graph(data, cat):
    if not cat:
        cat = ""
    x_ax = [datetime.strptime(row['date'], '%Y-%m-%d') for row in data]
    y_ax = [row['feelingavg']for row in data]
    if (len(x_ax) > 0 and len(y_ax) > 0):
        pyplot.clf()
        pyplot.plot(x_ax, y_ax)
        pyplot.title(cat)
        pyplot.xlabel( 'Date' )
        pyplot.ylabel( 'Feeling' )
        pyplot.gcf().autofmt_xdate()
        pyplot.gca().set_xticks(x_ax)
        pyplot.ylim([0, 2])
        pyplot.gca().set_xticklabels([date.strftime("%d.%m.") for date in x_ax])
        canvas = FigureCanvas(pyplot.gcf())
        png_output = StringIO.StringIO()
        canvas.print_png(png_output)
        return png_output.getvalue() 