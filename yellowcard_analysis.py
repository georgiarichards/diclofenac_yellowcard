#!/usr/bin/env python
# coding: utf-8

# # Reports of spontaneous suspected Adverse Drug Reactions (ADRs) reported to the UK's MHRA Yellow Card Scheme 

# #### This notebook visualises the data openly available at Yellow Card [here](https://info.mhra.gov.uk/drug-analysis-profiles/dap.html?drug=./UK_EXTERNAL/NONCOMBINED/UK_NON_000129175942.zip&agency=MHRA) which was extracted on Monday, November 23 2020. 

# In[1]:


# import libraries required for analysis 
import numpy as np 
import pandas as pd
from pylab import savefig
import seaborn as sns
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


# import data 
df = pd.read_csv("data.csv",thousands=',')


# In[3]:


df.head()


# In[4]:


df.describe()


# In[5]:


# plotting the number of cases overtime using seaborn

plt.figure(figsize=(18,8))
ax = sns.countplot(data=df, x="YEAR", color="navy")
plt.xlabel(' ')
plt.ylabel('No. of people with adverse drug reactions')

plt.savefig("fig1_cases_time.png", dpi=600)


# In[6]:


df['SEX'].value_counts()


# In[7]:


df['SEVERITY'].value_counts()


# In[8]:


def rel_freq(x):
    freqs = [(value, x.count(value) / len(x)) for value in set(x)] 
    return freqs

rel_freq(list(df['SEVERITY']))


# In[13]:


# plotting the severity of cases using seaborn 

plt.figure(figsize=(12,8))
ax = sns.countplot(data=df, x="SEVERITY", color="navy")
plt.xlabel(' ')
plt.ylabel('No. of people with adverse drug reactions')

plt.savefig("fig2_severity.png", dpi=600)


# In[11]:


year_severity = pd.crosstab(index=df["YEAR"], columns=df["SEVERITY"])
year_severity


# In[48]:


ax = df.groupby(['SEVERITY', 'YEAR']).size().reset_index().pivot(columns='SEVERITY', index='YEAR', values=0)
ax.plot.bar(stacked=True, figsize=(15,10))

plt.ylabel('Number of people reporting suspected adverse drug reactions')
plt.legend(["fatal", "non-serious", "serious"])

plt.savefig("fig3_severity_year.png", dpi=600)


# In[19]:


df_long = pd.wide_to_long(df, stubnames=['PT', 'HLT', 'HLGT', 'SOC_ABBREV', 'FATAL_YN'],
i=['ID','SEX','YEAR','SEVERITY'],
j='ADVERSE_EVENT',
sep='_')

df_long = df_long.reset_index()
df_long = df_long.dropna(subset=['PT', 'HLT', 'HLGT', 'SOC_ABBREV', 'FATAL_YN'])


# In[20]:


df_long.tail()


# In[21]:


df_long.describe()


# In[22]:


df_long['SOC_ABBREV'].value_counts()


# In[23]:


rel_freq(list(df_long['SOC_ABBREV']))


# In[24]:


ADR = pd.crosstab(index=df_long["SOC_ABBREV"], columns=df_long["SEVERITY"])
ADR


# In[26]:


# plotting the number of adverse drug reactions using seaborn

plt.figure(figsize=(15,8))
ax = sns.countplot(data=df_long, 
                   x="SOC_ABBREV", 
                   color="navy", 
                   order=df_long['SOC_ABBREV'].value_counts().index)
plt.xlabel(' ')
plt.ylabel('No. of adverse drug reactions')

plt.savefig("fig4_system.png", dpi=600)


# In[53]:


ax = df_long.sort_values('SOC_ABBREV', ascending=False).groupby(['SEVERITY', 'SOC_ABBREV']).size().reset_index().pivot(columns='SEVERITY', index='SOC_ABBREV', values=0)
ax.plot.bar(stacked=True, figsize=(14,10))

plt.xlabel('organ systems')
plt.ylabel('Number of adverse drug reactions')
plt.legend(["fatal", "non-serious", "serious"])

plt.savefig("fig5_severity_year.png", dpi=600)


# In[ ]:




