import os
import pandas as pd
from pandas.core.frame import DataFrame
import matplotlib.pyplot as plt

os.chdir('C:/Users/youyu/Downloads/combine files[330]')   #Set up directory to the designed folder
# This folder includes all excel files for both Task 1 and Task 2. No subfolders inside. 

# Task 1
def csvname(n):
    # This function is going to read the .csv files with name in specific pattern
    # n: Index of the file, i.e. n=2, then 's2 - Sheet1.csv'
    name = 's'+str(n)+' - Sheet1.csv'
    return name

# Create multiple dataframe
d = {}
for i in range(1,11):
    d[i] = pd.read_csv(csvname(i))

combined = pd.concat([d[1]['DateTime'],d[1]['Temp(in K)']], axis=1)
for i in range(2,11):
    combined = pd.concat([combined,d[i]['Temp(in K)']], axis=1)
combined.to_csv('Task 1 CombinedFiles.csv',header=True, index=True)  #Save dataframe to .csv file


# Task 2

# Read the .xlsx file
t2 = pd.read_excel('long form to short form data conversion[329].xlsx', sheet_name = 'input',header=1)
group = int(t2.shape[1]/6)

# Prepare to add pack serial to the column
pack_serial = pd.read_excel('long form to short form data conversion[329].xlsx', sheet_name = 'input').columns
pack_serial = [pack_serial[0], pack_serial[6],pack_serial[6*2],pack_serial[6*3]] # Choose the column with context

# Rearrange the dataframe
e = {}
for i in range(1,group+1):
    e[i] = pd.DataFrame(t2.iloc[0:,(i-1)*6:i*6].dropna(how='all'))
    e[i]['pack serial'] = pack_serial[i-1]

# Rename the repeated column names
for i in range(2,group+1):
    e[i] = e[i].rename(columns = {'Test date.'+str(i-1):'Test date','Energy throughput/KWh.'+str(i-1):'Energy throughput/KWh','Capacity/Ah.'+str(i-1):'Capacity/Ah',
    'SOH/%.'+str(i-1):'SOH/%','DCIR / mOhm.'+str(i-1):'DCIR / mOhm','pack66 Ri increase/%.'+str(i-1):'pack66 Ri increase/%'})
    
df = pd.concat([e[1], e[2],e[3],e[4]], ignore_index=True)
df.to_csv('Task 2 Outcome.csv',header=True, index=True)  #Save dataframe to .csv file

# Plot the figure
plt.figure(1)
for i in range(1,group+1):
    plt.plot(e[i]['Energy throughput/KWh'],e[i]['SOH/%'])
plt.xlabel('Energy throughput/KWh')
plt.ylabel('SOH/%')
plt.legend(pack_serial)
plt.title('SOH/% vs. Energy throughput/KWh')
plt.savefig('Task 2.jpg')
plt.show()
plt.close(1)