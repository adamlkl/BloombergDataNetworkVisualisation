#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 16:04:51 2019

@author: Adamlkl
"""

import networkx as nx
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
plotly.tools.set_credentials_file(username='adamlkl', api_key='IRt8PniwKeuYgg1zTEoz')

import json

with open('bloomberg_network_data.json') as json_file:  
    data = json.load(json_file)

L=len(data['links'])
Edges=[(data['links'][k]['source'], data['links'][k]['target']) for k in range(L)]
G = nx.Graph()
G.add_edges_from(Edges)


labels=[]
group=[]
for node in data['nodes']:
    labels.append(node['name'])
    group.append(node['group'])

N = len(data['nodes'])
pos = nx.kamada_kawai_layout(G)

Xn=[]# x-coordinates of nodes
Yn=[]# y-coordinates
for k in pos:
    Xn.append(pos[k][0])
    Yn.append(pos[k][1])

Xe=[]
Ye=[]
for e in Edges:
    Xe+=[pos[e[0]][0],pos[e[1]][0], None]# x-coordinates of edge ends
    Ye+=[pos[e[0]][1],pos[e[1]][1], None]  

trace1=go.Scatter(x=Xe,
               y=Ye,
               mode='lines',
               line=dict(color='rgb(125,125,125)', width=1),
               hoverinfo='none'
               )

trace2=go.Scatter(x=Xn,
               y=Yn,
               mode='markers',
               name='actors',
               marker=dict(symbol='circle',
                             size=6,
                             color=group,
                             colorscale='Viridis',
                             line=dict(color='rgb(50,50,50)', width=0.5)
                             ),
               text=labels,
               hoverinfo='text'
               )

axis=dict(showbackground=False,
          showline=False,
          zeroline=False,
          showgrid=False,
          showticklabels=False,
          title=''
          )

layout = go.Layout(
         title="Bloomberg Github Repository Language Network Visualisation",
         width=1000,
         height=1000,
         showlegend=False,
         scene=dict(
             xaxis=dict(axis),
             yaxis=dict(axis),
        ),
     margin=dict(
        t=100
    ),
    hovermode='closest',
    annotations=[
           dict(
           showarrow=False,
            xref='paper',
            yref='paper',
            x=0,
            y=0.1,
            xanchor='left',
            yanchor='bottom',
            font=dict(
            size=14
            )
            )
        ],    )

data=[trace1, trace2]
fig=go.Figure(data=data, layout=layout)

py.iplot(fig, filename='sth')
plotly.offline.plot(fig, auto_open=True)