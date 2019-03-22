
# coding: utf-8
# Author: Bokyung Choi
# Date: 2018 11 25
# Course: OMIS 4000 A

# In[1425]:


import pandas as pd
import pulp as pulp
import os
import folium


# In[1426]:


#Change working directory
os.getcwd()
os.chdir(r"C:\Users\최보경\Desktop\2018JUNIOR\02-Models Applications in Operational Research\Model_final")


# In[1427]:


#Read the excel file
xlsx=pd.ExcelFile('BoardingsReport2017.xlsx')
boardings_df=pd.read_excel(xlsx,'R00D')
boardings_df.tail()


# In[1428]:


#converting the bus stop names to 1 - 18
stop_list=[]
stop_list=list(range(1,len(boardings_df['Stop Name'])+1))
stop_list


# In[1429]:


#Read the distance file and create a list of driving minute
resultdf=pd.read_csv('Drivingtime_combination_with minute.csv')
minute_list=result_df['Driving minute'].tolist()
len(minute_list)


# In[1430]:


#Make 'demand' series to list
demand_list=boardings_df['Boardings'].tolist()
sort_demand_list=boardings_df['Boardings'].tolist()
sort_demand_list.sort(reverse=True)
new_limit=sum(sort_demand_list[0:4])
new_limit


# In[1431]:


#Start the model
model=pulp.LpProblem("Chatham - Kent Bus stop Optimization",pulp.LpMinimize)
x={}
y={}
X=[]
Y=[]


# In[1432]:


#Add variables to the model

for i in stop_list:
    for j in range(i+1,len(stop_list)+1):
        x[i,j]=pulp.LpVariable("x(%s,%s)"%(i,j),cat='Binary')
        X.append(x[i,j])


# In[1433]:


#Add the objective
n=0
objective=[]
for i in range(1,len(stop_list)):
    for j in range(i+1,len(stop_list)+1):
        objective+=x[i,j]*minute_list[n]
        n+=1
        
for i in range(1,len(stop_list)):
    for j in range(i+1,len(stop_list)+1):
        objective+=(0.5*x[i,j])
       
#add to model
model+=pulp.lpSum(objective)


# In[1434]:


#Add constraint
#1 The number of total revised bus stops should be under certain limit
constraint1=[]
for i in range(1,len(stop_list)):
    for j in range(i+1,len(stop_list)+1):
        constraint1+=x[i,j]
        
model+=pulp.lpSum(constraint1)<=len(stop_list)*1
model+=pulp.lpSum(constraint1)>=len(stop_list)*0.4444


# In[1435]:


#2 Bus stop spacing constraint 
n=0
for i in range(1,len(stop_list)):
    for j in range(i+1,len(stop_list)+1):
        if [i,j] in ([2,3],[3,4],[4,5],[5,6],[6,7],[7,8],[8,9],[17,18]):
            pass
        else:
            model+=pulp.lpSum(x[i,j]*minute_list[n])<=12
        n+=1


# In[1436]:


#New 3 demand high keep
constraint3_1=[]
constraint3_2=[]
constraint3_3=[]
constraint3_4=[]

for j in range(2,len(stop_list)+1):
        constraint3_1+=x[1,j]
for j in range(3,len(stop_list)+1):
        constraint3_2+=x[2,j]
for j in range(12,len(stop_list)+1):
        constraint3_3+=x[11,j]
for j in range(18,len(stop_list)+1):
        constraint3_4+=x[17,j]

model+=pulp.lpSum(constraint3_1)>=1
model+=pulp.lpSum(constraint3_2)>=1
model+=pulp.lpSum(constraint3_3)>=1
model+=pulp.lpSum(constraint3_4)>=1


# In[1437]:


#4 Sum demand of each bus stop

constraint3=[]
for i in range(1,len(stop_list)):
    for j in range(i+1,len(stop_list)+1):
        constraint3+=(x[i,j]*demand_list[i-1]+x[i,j]*demand_list[j-1])

model+=pulp.lpSum(constraint3)>=new_limit


# In[1438]:


#5 keep one stop in each city
constraint5_1=[]
constraint5_2=[]
constraint5_3=[]
constraint5_4=[]
constraint5_5=[]
constraint5_6=[]

for j in range(4,len(stop_list)+1):
        constraint5_1+=x[3,j]
for j in range(5,len(stop_list)+1):
        constraint5_2+=x[4,j]
for j in range(6,len(stop_list)+1):
        constraint5_3+=x[5,j]
for j in range(7,len(stop_list)+1):
        constraint5_4+=x[6,j]
for j in range(8,len(stop_list)+1):
        constraint5_5+=x[7,j]
for j in range(9,len(stop_list)+1):
        constraint5_6+=x[8,j]
        
for i in range(1,3):
        constraint5_1+=x[i,3]
for i in range(1,4):
        constraint5_2+=x[i,4]
for i in range(1,5):
        constraint5_3+=x[i,5]
for i in range(1,6):
        constraint5_4+=x[i,6]
for i in range(1,7):
        constraint5_5+=x[i,7]
for i in range(1,8):
        constraint5_6+=x[i,8]
        
model+=pulp.lpSum(constraint5_1)>=1
model+=pulp.lpSum(constraint5_2)>=1
model+=pulp.lpSum(constraint5_3)>=1
model+=pulp.lpSum(constraint5_4)>=1
model+=pulp.lpSum(constraint5_5)>=1
model+=pulp.lpSum(constraint5_6)>=1


# In[1439]:


#Status check
model.solve()
pulp.LpStatus[model.status]


# In[1440]:


#Model information
model.variables


# In[1441]:


#Figure out the variable values
bus_stop_binary={}
for v in model.variables():
    bus_stop_binary[v.name]=v.varValue

#find values in dictionary
def getKeysByValues(dictOfElements, Value):
    listOfKeys = list()
    listOfItems = bus_stop_binary.items()
    for item  in listOfItems:
        if item[1]==Value:
            listOfKeys.append(item[0])
    return  listOfKeys 
#only get the bus stop numbers
keys=getKeysByValues(bus_stop_binary,1.0)
new_stop="".join(keys)
numbers=[]
for item in new_stop:
    for subitem in item.split():
        if(subitem.isdigit()):
            numbers.append(subitem)
            
#organizing the answer
new_stop=new_stop.replace("x(","")
new_stop=new_stop.replace(")",",")
new_stop=new_stop.split(",")
final_answer=list(set(new_stop))
final_answer.remove("")
final_answer.sort()
final_answer=list(map(int,final_answer))
final_answer# which bus stops to keep


# In[1442]:


comb_coord=[]
comb_coord=list(zip(boardings_df.Latitude,boardings_df.Longitude))  


# In[1443]:


#Draw map with current stops
sug_map=None
sug_map=folium.Map(location=[42.334826,-82.213680],zoom_start=10)
#input in the format of [(82.2345,-32.33),(84.2345,-31.2)]

for coord in range(0,len(comb_coord)):
    folium.Marker(comb_coord[coord],
                          popup=boardings_df['Stop Name'][coord],
                 icon=folium.Icon(color='red'
                                 ,icon='bus',angle=0,prefix='fa')).add_to(sug_map)
   
sug_map.save('Current Route D.html')
sug_map


# In[1444]:


#Draw map with changed stops
for i in final_answer:
    folium.Marker(comb_coord[i-1],
                          popup=boardings_df['Stop Name'][i-1],
                 icon=folium.Icon(color='green'
                                 ,icon='bus',angle=0,prefix='fa')).add_to(sug_map)
   
sug_map.save('Our suggestion.html')
sug_map


# In[1445]:


print("*******************Final Solution********************")
print("<Stations to Keep>")
final_answer.sort()
for i in final_answer:
    print(boardings_df['Stop Name'][i-1])
print("")

print("<Stations to Remove>")
for j in stop_list:
    if j not in final_answer:
        print(boardings_df['Stop Name'][j-1])
        
print("")
print("<Total demand of new Route D>")
boarding=[]
for i in final_answer:
    boarding.append(boardings_df['Boardings'][i-1])
print(sum(boarding))

print("")
print("<Total travelling time of revised Route D>")
print( pulp.value(model.objective))
      
print("")
print("<Selected travelling distance of Route D>")
print(keys)


# In[1446]:


#Add stops in our recommednation
new_coord=[(42.314883, -82.074444)]
for coord in range(0,len(new_coord)):
    folium.Marker(new_coord[coord],
                          popup='Chatham-Kent Municipal Airport',
                 icon=folium.Icon(color='blue',icon='bus',angle=0,prefix='fa')).add_to(sug_map)

folium.Marker((42.27949,-82.03172),popup='Cedar Springs',
             icon=folium.Icon(color='red',icon='bus',angle=0,prefix='fa')).add_to(sug_map)

sug_map.save('Our Suggestion_with new stop.html')
sug_map

