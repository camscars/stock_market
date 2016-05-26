
# coding: utf-8

# In[41]:

import pandas as pd
import numpy as np
from pandas import Series, DataFrame

import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')
get_ipython().magic('matplotlib inline')

from pandas.io.data import DataReader
from datetime import datetime

tech_list = ['AAPL', 'GOOG', 'MSFT', 'AMZN'] #Apple, Google, Microsoft, Amazon
end = datetime.now()
start = datetime(end.year-1,end.month,end.day)


# In[2]:

for stock in tech_list:
    #globals takes stock ticker and makes it into global variable
    globals()[stock] = DataReader(stock,'yahoo',start,end)


# In[6]:

#Charting the closes for Apple
AAPL['Adj Close'].plot(legend=True, figsize=(10,4))


# In[8]:

#Charting the volume monthly
AAPL['Volume'].plot(legend=True,figsize=(10,4))


# In[9]:

ma_day = [10,20,50] #moving averages

for ma in ma_day:
    column_name = "MA for %s days" %(str(ma))
    AAPL[column_name] = pd.rolling_mean(AAPL['Adj Close'],ma)


# In[14]:

AAPL[['Adj Close', 'MA for 10 days', 'MA for 20 days', 'MA for 50 days']].plot(subplots=False,figsize=(10,4))


# In[17]:

#Create new column based off pct change of the closing
#shows whether you gained or lost
AAPL['Daily Return'] = AAPL['Adj Close'].pct_change()

AAPL['Daily Return'].plot(legend=True, figsize=(10,4),linestyle='--',marker='o')


# In[18]:

#plot a historgram of daily returns for a year
sns.distplot(AAPL['Daily Return'].dropna(), bins=100, color='purple')


# In[21]:

###AAPL['Daily Return'].hist(bins=100) Removed, overlayed graphs better


# In[22]:

#New dataframe from ayhoo finance with just the adj closing
closing_df = DataReader(tech_list, 'yahoo',start,end)['Adj Close']


# In[23]:

closing_df.head()


# In[24]:

tech_returns = closing_df.pct_change()


# In[29]:

sns.jointplot('GOOG','MSFT', tech_returns,kind='scatter', color='green')


# In[31]:

sns.pairplot(tech_returns.dropna())


# In[32]:

returns_fig = sns.PairGrid(tech_returns.dropna())

returns_fig.map_upper(plt.scatter,color='purple')

returns_fig.map_lower(sns.kdeplot,cmap='cool_d')

returns_fig.map_diag(plt.hist,bins=30)


# In[35]:

returns_fig = sns.PairGrid(closing_df)

returns_fig.map_upper(plt.scatter,color='purple')

returns_fig.map_lower(sns.kdeplot,cmap='cool_d')

returns_fig.map_diag(plt.hist,bins=30)


# In[38]:

#to get numerical correlation values
sns.corrplot(tech_returns.dropna(),annot=True)


# In[37]:

#to get numerical correlation values, but for closing
sns.corrplot(closing_df,annot=True)


# In[39]:

rets = tech_returns.dropna()


# In[44]:

area = np.pi*20

plt.scatter(rets.mean(),rets.std(),s=area)

#Making axis titles
plt.xlabel('Expected Return')
plt.ylabel('Risk')

#for every column in the dataframe let x be the mean and y be the std dev
for label, x, y in zip(rets.columns, rets.mean(), rets.std()):
    plt.annotate(
        label,
        xy = (x, y), xytext=(50,50),
        textcoords = 'offset points', ha='right', va='bottom',
        arrowprops = dict(arrowstyle = '-', connectionstyle='arc3,rad=-0.3'))


# In[ ]:



