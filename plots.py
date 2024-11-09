import math
import plotly
import plotly.graph_objs as go
x = [x/10 for x in range(100)]
y = [math.sin(c) for c in x]
fig = go.Scatter(x=x, y=y)
# fig = go.Bar(x=x, y=y)
# fig = go.Pie(labels=['a', 'b', 'c'], 
#              values = [0.4, 0.2, 0.4])
graph_div = plotly.offline.plot({"data": [fig],})
# graph_div = plotly.offline.plot({"data": [fig],}, auto_open=False, output_type="div")
