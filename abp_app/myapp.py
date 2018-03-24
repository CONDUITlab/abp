import pandas as pd
import numpy as np
from bokeh.models import ColumnDataSource, TapTool
from bokeh.plotting import figure
from bokeh.layouts import row
#from bokeh.plotting import show
from bokeh.io import curdoc

# data for plot 2
df2 = pd.DataFrame({"A" : np.linspace(10, 20, 10),
                    "B" : np.linspace(20, 30, 10),
                    "C" : np.linspace(30, 40, 10),
                    "D" : np.linspace(40, 50, 10),
                    "E" : np.linspace(50, 60, 10),})
source2 = ColumnDataSource(
        data=dict(
            x=list(df2.index.values),
            y=list(df2.iloc[:,0].values)
        )
    )

# data for plot 1
df1 = np.mean(df2)
source1 = ColumnDataSource(
        data=dict(
            x=list(range(0,df1.shape[0])),
            y=list(df1.values),
            colnames = list(df1.index.values)
        )
    )

# Plot graph one with data from df1 and source 1 as barplot
plot1 = figure(plot_height=300, plot_width=400, tools="tap")
plot1.vbar(x='x',top='y',source=source1, bottom=0,width =0.5)


# Plot graph two with data from df2 and source 2 as line
plot2 = figure(plot_height=300, plot_width=400, title="myvalues", 
              tools="crosshair,box_zoom,reset,save,wheel_zoom,hover")    
r1 = plot2.line(x='x',y='y',source =source2, line_alpha = 1, line_width=1)
# safe data from plot 2 for later change in subroutine
ds1 = r1.data_source

def update_plot2(mycolumn):
    try:
        ds1.data['y'] = df2[mycolumn].values
    except:   
        pass

# add taptool to plot1
taptool = plot1.select(type=TapTool)
taptool.callback = update_plot2(mycolumn="@colnames")

#show(row(plot1,plot2))
curdoc().add_root(row(plot1,plot2))