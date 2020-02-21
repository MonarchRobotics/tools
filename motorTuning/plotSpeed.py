
################################################################################
## File: plotspeed.py
## Author: Chris Morroni
## 
## Description: Imports an encoder signal CSV, calculates the motor speed,
##   and plots motor speed versus time
##
## Saleae Logic Export Settings:
##   Export only one channel
##   Output one row per change
## 
## Usage: $> python plotSpeed.py path/to/file.csv
################################################################################

import argparse
import numpy
import pandas
import plotly.graph_objects as graph

parser = argparse.ArgumentParser(description="Plot speed from an encoder signal CSV")
parser.add_argument("file", help="the CSV file to parse")
args = parser.parse_args()

path = args.file

data = pandas.read_csv(path)
data = data.drop(columns=[" Data[binary]"]) # drop unused data column
data = data[ data["Time[s]"] >= 0] # drop time before initial trigger
data["Speed"] = 1/data.diff()["Time[s]"]/4096*60 # calculate speed from elapsed time
data["Filtered Speed"] = data["Speed"].rolling(1024, center=True).mean()

fig = graph.Figure()

fig.add_trace( graph.Scatter( x=data["Time[s]"], y=data["Speed"],
                              mode="lines", name="Raw Speed", opacity=0.25,
                              line=dict(color="royalblue", width=0.5)) )
                             
fig.add_trace( graph.Scatter( x=data.dropna()["Time[s]"], y=data.dropna()["Filtered Speed"],
                              mode="lines", name="Filtered Speed",
                              line=dict(color="royalblue", width=2)) )
                             
fig.show()
