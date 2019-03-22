
# coding: utf-8
# Author: Bokyung Choi
# Date: 2018 11 25
# Course: __________

# In[1]:


import os
import pandas as pd
xlsx = pd.ExcelFile('BoardingsReport_____.xlsx')
route_df = pd.read_excel(xlsx, '_____')
route_df.tail()


# In[2]:


#Change those coordinates to string!!!!
route_df['Latitude']=route_df['Latitude'].astype(str)
route_df['Longitude']=route_df['Longitude'].astype(str)
route_df.head()
route_df.dtypes


# In[3]:


#Creating tuples for input
subset=route_df[['Latitude','Longitude']]
stop_coord=[list(x) for x in subset.values]
stop_coord


# In[4]:


#Create combinations
import itertools
from itertools import combinations

comb_coord=list(itertools.combinations(stop_coord,2))
len(comb_coord)

comb_coord[2][1][0],comb_coord[2][1][1]


# In[6]:


#Google API bring distance for each combination
import simplejson, urllib
result_df=pd.DataFrame()
distance_list=[]
time_list=[]

for i in range(0,len(comb_coord)):
    orig = comb_coord[i][0][0],comb_coord[i][0][1]
    orig_coord=','.join(orig)
    dest = comb_coord[i][1][0],comb_coord[i][1][1]
    dest_coord=','.join(dest)
    
    API='AIzaSyAEDuKVUDeKyTX-enRoLSH-UN3btVknMjw'

    url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins="+ orig_coord + "&destinations=" + dest_coord + "&mode=driving&traffic_model=best_guess&departure_time=now&language=en-EN&sensor=false&key=" + API
    
    result= simplejson.load(urllib.request.urlopen(url))
    driving_distance = result['rows'][0]['elements'][0]['distance']['text'] 
    driving_time = result['rows'][0]['elements'][0]['duration']['text']
    distance_list.append(driving_distance)
    time_list.append(driving_time)


# In[7]:


#Organize result_df
result_df['Origin stop, Destination stop']=comb_coord
result_df['Driving distance']=distance_list
result_df['Driving time']=time_list
result_df.head()


# In[8]:


result_df.to_csv('Drivingtime_combination.csv')


# In[9]:


#Read distance matrix csv and change hour/min into MInutes
result_df=result_df[['Origin stop, Destination stop','Driving distance','Driving time']]
minute=list(result_df['Driving time'])
new_minute=[]
for i in minute:
    i=i.replace('mins','min')
    new_minute.append(i)


# In[10]:


#delete 'min'
j=0
for i in new_minute:
        new_minute[j]=new_minute[j][:-4]
        j+=1
#convert into integer    
result_df['Driving minute']=new_minute
result_df['Driving minute']=result_df['Driving minute'].astype(str).astype(int)
result_df.to_csv('Drivingtime_combination_with minute.csv')
result_df.head()

