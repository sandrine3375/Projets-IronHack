# -*- coding: utf-8 -*-
"""
Created on Fri Jan 14 23:01:16 2022

@author: Lenovo
"""

import streamlit as st
import pandas as pd
import numpy as np
from sklearn import datasets
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly import tools
import plotly.offline as py
import plotly.express as px
from cycler import cycler
import seaborn as sns
import warnings

IBM = pd.read_csv(r'/app/project5_streamlit/IBM.csv')


st.title ("IBM Employees KPI Dashboard")

#fig = px.pie(IBM, values='Attrition', names='Attrition')

#st.plotly_chart(fig)

#plot phik matrix


# Install the image  on the side bar
from PIL import Image
img =Image.open(r'/app/project5_streamlit/attrition.jpg')
st.sidebar.image(img, width=300, caption="It refers also to the turn over")


st.subheader ("Key metrics")
if st.checkbox('show/hide data table'):
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric(label = 'Total number of employees' , value = 1470)
    kpi2.metric(label = 'Total number of active employees' , value = 1233, delta = '83,9' , delta_color ='inverse')
    kpi3.metric(label = 'Total nummber of non active employees' , value = 237, delta = '16,1')
  
    st.table (IBM.head(5))
    
#################### information on dataset ##################################
# Install the widget on the side bar/ 1er selection

if st.checkbox('Click here to select general information on DATASET'):
    st.sidebar.title("Selection1 -in general")
    add_selectbox1 = st.sidebar.selectbox("Choose your table:",("", "Descriptive statistique", "Employees and income by Department", "Salary, max, min and mean",
            "IBM Employees Job Satisfaction"))

    if add_selectbox1=="Descriptive statistique":
        st.write('Theme: List of IBM Employees')
        st.write ('Shape : ', IBM.shape)
        st.write ('Describe : ', IBM.describe())

    elif add_selectbox1=="Employees and income by Department":
        st.markdown('**Total of employee** by department.')
        st.table(IBM['Department'].value_counts())
        
        st.markdown('**Montly Income in average** by department.')
        st.table(IBM.groupby(by=['Department'])['MonthlyIncome'].mean())
        
       
    elif add_selectbox1=="Salary, max, min and mean":
      
       # We want 3 colomsn
       kpi4, kpi5, kpi6 = st.columns(3)
       kpi4.metric(label = 'Maximum Salary $  ' , value= round( IBM['MonthlyIncome'].max()))
       kpi5.metric(label = 'Average Salary $ ', value = round (IBM['MonthlyIncome'].mean()))
       kpi6.metric(label = 'Average Salary $ ', value= round (IBM['MonthlyIncome'].min()))
       st.table(IBM.pivot_table(index=["Department"], values=['MonthlyIncome'],aggfunc=['sum','count']))
       

    elif add_selectbox1=="IBM Employees Job Satisfaction":
        st.table(IBM.JobSatisfaction.value_counts())
        
        fig3, ax = plt.subplots()
        ax=IBM.JobSatisfaction.value_counts().plot(kind='pie', autopct='%1.1f%%', #format which work with non numeric value
    startangle=90, shadow=True, legend = True, fontsize=10)
        ax.set_title("Job Satisfaction")
        st.pyplot(fig3)
        
    #we want two other  charts
        df= IBM['JobSatisfaction'].value_counts()
        st.bar_chart(df)
        st.line_chart(df)
        
#################### scatter Logic - relatif on attrition ##################################
if st.checkbox('Click here to Scatter Chart, relatif to the attrition'):
    st.sidebar.markdown("### Scatter Chart: According Attrition status explore different caracteristics")

    #name of columns in lists
    measurements = IBM.drop(labels=["Attrition"], axis=1).columns.tolist()

    x_axis = st.sidebar.selectbox("X-Axis", measurements)
    y_axis = st.sidebar.selectbox("Y-Axis", measurements, index=1)


    if x_axis and y_axis:
        scatter_fig = plt.figure(figsize=(6,4))

        scatter_ax = scatter_fig.add_subplot(111)
        #dataframe : one with attriction-yes, one with a-no
        attrition_df = IBM[IBM["Attrition"] == "Yes"]
        no_attrition_df = IBM[IBM["Attrition"] == "No"]

        attrition_df.plot.scatter(x=x_axis, y=y_axis, s=120, c="tomato", alpha=0.6, ax=scatter_ax, label="Attrition")
        no_attrition_df.plot.scatter(x=x_axis, y=y_axis, s=120, c="dodgerblue", alpha=0.6, ax=scatter_ax,
                               title="{} vs {}".format(x_axis.capitalize(), y_axis.capitalize()), label="Employed");

        st.pyplot(scatter_fig)
 
  

########## Bar Chart Logic - relatif to attrition  ##################
if st.checkbox('Click here to Bar Chart, relatif to the attrition'):
    st.sidebar.markdown("### Bar Chart: According Attrition Status, explore caracterist  : ")

    # we delete from measure nn-numeric colums": 'Department','EducationField','MaritalStatus','MaritalStatus',
    indexbarshart=['Age', 'DistanceFromHome',
     'Education',
     
     'EnvironmentSatisfaction',
     'JobSatisfaction',
     
     'MonthlyIncome',
     'NumCompaniesWorked',
     'WorkLifeBalance',
     'YearsAtCompany']
    avg_IBM = IBM.groupby("Attrition").mean()
    bar_axis = st.sidebar.multiselect(label="Average of columns Per Attrition Status",
                                      options=indexbarshart,
                                      default=["Education","Age"])

    if bar_axis:
        bar_fig = plt.figure(figsize=(6,4))

        bar_ax = bar_fig.add_subplot(111)

        sub_avg_IBM = avg_IBM[bar_axis] #colum d'une dataframe

        sub_avg_IBM.plot.bar(alpha=0.8, ax=bar_ax, title="Average Per Attrition Status Type");
        st.pyplot(bar_fig)

    else:
        bar_fig = plt.figure(figsize=(6,4))

        bar_ax = bar_fig.add_subplot(111)

        sub_avg_IBM = avg_IBM[["Education","Age"]]

        sub_avg_IBM.plot.bar(alpha=0.8, ax=bar_ax, title="Average Per Attrition Status Type");
        st.pyplot(bar_fig)


################# Histogram Logic -relatif to all compagny ########################
if st.checkbox('Click here to Histogram, relatif to the whole compagny'):
    st.sidebar.markdown("### Histogram: Explore caracterict of the whole compagny : ")
    #name of columns in lists
    measurements = IBM.drop(labels=["Attrition"], axis=1).columns.tolist()
    
    hist_axis = st.sidebar.multiselect(label="Histogram Ingredient", options=measurements, default=["Education", "Age"])
    
    bins = st.sidebar.radio(label="Bins :", options=[10,20,30,40,50], index=4)

    if hist_axis:
        hist_fig = plt.figure(figsize=(6,4))

        hist_ax = hist_fig.add_subplot(111)

        sub_IBM = IBM[hist_axis]

        sub_IBM.plot.hist(bins=bins, alpha=0.7, ax=hist_ax, title="Distribution of Measurements");
        st.pyplot(hist_fig)
    else:
        hist_fig = plt.figure(figsize=(6,4))

        hist_ax = hist_fig.add_subplot(111)

        sub_IBM =IBM[["Education", "Age"]]

        sub_IBM.plot.hist(bins=bins, alpha=0.7, ax=hist_ax, title="Distribution of Measurements");

        st.pyplot(hist_fig)
#################### Hexbin Chart Logic - relatif to all compagny##################################

if st.checkbox('Click here to Hexbin Chart, relatif to the whole compagny'):
    st.sidebar.markdown("### Hexbin Chart: Explore compapny caracteristic:")
    #name of columns in lists
    indexbarshart=['Age', 'DistanceFromHome', 
     'Education',
     
     'EnvironmentSatisfaction',
     'JobSatisfaction',
     
     'MonthlyIncome',
     'NumCompaniesWorked',
     'WorkLifeBalance',
     'YearsAtCompany']
    hexbin_x_axis = st.sidebar.selectbox("Hexbin-X-Axis", indexbarshart, index=0)
    hexbin_y_axis = st.sidebar.selectbox("Hexbin-Y-Axis", indexbarshart, index=1)

    if hexbin_x_axis and hexbin_y_axis:
        hexbin_fig = plt.figure(figsize=(6,4))

        hexbin_ax = hexbin_fig.add_subplot(111)

        IBM.plot.hexbin(x=hexbin_x_axis, y=hexbin_y_axis,
                                     reduce_C_function=np.mean,
                                     gridsize=25,
                                     #cmap="Greens",
                                     ax=hexbin_ax, title="Concentration of Measurements")
        st.pyplot(hexbin_fig)

        

   #################### selection on attrition ##################################  

if st.checkbox('Click here to select information on ATTRITION'):
    
    # Install the widget on the side bar / 1er selection
    st.sidebar.title("Selection2 - for attrition")
    selection = st.sidebar.selectbox("Choose your graph:", {"", "Attrition", "Department","Income", "Marital Status", "WorkLifeBalance"})


    if selection == 'Attrition':
        st.subheader ("Attrition Key Metrics")
        #Display 2 charts
        
        #Chart 1 - Bar chart
        
        fig1, ax = plt.subplots(figsize=(10,4))   
        
        ax = IBM['Attrition'].value_counts().plot(kind='bar',  color = ['paleturquoise', 'dodgerblue'], edgecolor='black', fontsize = 8)
        ax.set_title('Employee Attrition in number', fontsize = 18)
        plt.xlabel("Attrition", fontsize =12)
        plt.ylabel("Number of employees", fontsize =12)
        st.pyplot(fig1)

        #Chart 2 - Pie Chart
        
        fig2, ax = plt.subplots(figsize=(10,4))  
        
        colors = ['mediumturquoise', 'dodgerblue']
        ax = IBM['Attrition'].value_counts().plot(kind='pie' , autopct='%1.1f%%', colors = colors, startangle=100, legend = True, labeldistance=1.15, wedgeprops = { 'linewidth' : 3, 'edgecolor' : 'white' }, fontsize=5)
        ax.set_title("Employee Attrition in percentage", fontsize = 7)
        plt.legend(fontsize=5) 
        ax.set_ylabel('') # remove the 'Attrition' foor axis 'Y'
        # ax.legend(loc=2, labels= ax.index)
        st.pyplot(fig2)
            

    if selection == "Department":
        #Chart 4 
        fig4, axs= plt.subplots(figsize=(10,4)) 
        
        axs = sns.barplot(x="Department", y='YearsAtCompany', hue="Attrition", data=IBM)
        axs.set_xticklabels(axs.get_xticklabels(),rotation=45)
        plt.suptitle('')
        axs.set_title('Attrition and Years in the company per department')
        plt.show()
        st.pyplot(fig4)          
          
              
        
    elif selection == 'Income':
        st.subheader('Monthly Income distribution')
        
         
        with st.echo(code_location='below'):
            fig = plt.figure()
            ax6 = fig.add_subplot(1,1,1)
            ax6.scatter(IBM["Attrition"],IBM["MonthlyIncome"],   )
            ax6.set_xlabel("Attrition");
            ax6.set_ylabel("Monthly Income");
            st.write(fig)
            st.balloons()
            

    elif selection == "Marital Status":
        y=IBM.loc[(IBM['Attrition']=="Yes")]
        
        fig4, ay = plt.subplots()
        ay=y.MaritalStatus.value_counts().plot(kind='pie', autopct='%1.1f%%', #format which work with non numeric value
    startangle=5, shadow=True, legend = False, fontsize=10)
        plt.suptitle('')
        ay.set_xlabel("")
        ay.set_ylabel("")
        ay.set_title('Marital Satus, for the ones who left compagny')
        st.pyplot(fig4) 
        
        
        #WorkLifeBalance, for the ones who left compagny
    elif selection == "WorkLifeBalance":
        y=IBM.loc[(IBM['Attrition']=="Yes")]
        fig9, ab = plt.subplots()
        ab=y.WorkLifeBalance.value_counts().plot(kind='pie', autopct='%1.1f%%', #format which work with non numeric value
         startangle=5, shadow=True, legend = False, fontsize=10)
        plt.suptitle('')
        ab.set_xlabel("")
        ab.set_ylabel("")
        ab.set_title('Work Life Balance, for the ones who left compagny')
        st.pyplot(fig9)
        
