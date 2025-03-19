import streamlit as st
from PIL import Image
import pandas as pd
import numpy as np
import io
from io import BytesIO
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns
import os

#st.write(print(os.getcwd())) # finds files path of repository

# Name of Script
st.title('Graphs for Reaction Screens and Solubility Studies')  # Replace with your script name

graph = st.radio('Pick one:', ['Solubility Study', 'Reaction Screen'])

# Description
st.markdown('''
    This application helps to Data in a graphical forms
    ''')  #Small description of what the application does


font_path = "/mount/src/solubility-graphs/GOTHIC.TTF"
font_prop = fm.FontProperties(fname=font_path)

# Apply the font globally for all plots
plt.rcParams['font.family'] = font_prop.get_name()

if graph =='Reaction Screen':
    
    #Screen Sheet Download

    data = {
            "Conditions": ['Ethanol, xx (5 eq).', 'Me-THF, xx (5 eq.)', 'Toluene, xx (5 eq.)'],
            "Time": ['1 h', '3 h', '5 h'],
            "SM": [10, 50, 80],
            'Product' : [70, 40, 10],
            'Imp 1' : [5, 3, 10],
            'Imp 2' : [15, 7, 0],
        }  # Random data that can be replaced
    
    excel_template = pd.DataFrame(data) # transformation of the data dictionary to a pandas data frame

    excel_file = io.BytesIO() # in-memory binary stream to store the excel file - will be written into a stream rather than a file to be saved on a disk

    with pd.ExcelWriter(excel_file, engine='xlsxwriter') as writer: # pd.ExcelWriter is a pandas function for converting data into an excel file
        excel_template.to_excel(writer, index=False, sheet_name='Sheet1') # converts the stream file to an excel file

    
    excel_file.seek(0) #  resets pointer back to the beginning
    
    # Downloader for template file

    st.download_button(
                label="Download Screen Sheet Template.xlsx ", # needs to change if you copy it somewhere
                data=excel_file,
                file_name="Screening_Template.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )  # Makes it so you can download the excel file with the streamlit widget
    
    with st.expander("Quick instruction📝"): 
        st.markdown('''
                1. Download Screen sheet template or excel file with a similar format. Columns beginning with imp-x or ukn-x will be combined into a new column named Impurities.
                2. For named reagents in a reaction label in the order SM, P, intermediate/impurity, etc. Please note names of variables need to be typed as they are in the excel file.
                3. Screen bar chart will be generated :)
                4. Any questions please speak with RJ
                ''')
    
    file = st.file_uploader("Choose an '.xlsx' (excel) File for Screen Data", type = ['xlsx']) # streamlit file uploader where the excel type is specified
    if file:
        df = pd.read_excel(file)  # reads the file into the dataframe using pandas
        
        st.write('Preview of Excel file')
        st.write(df.head()) # displays dataframe in the streamlit application

    
        x_axis = st.text_input('Enter x-axis Label', 'Conditions') # collects user inputs for labels using streamlit widget
           
        title = st.text_input('Enter chart title', 'Reaction Screen of XX') # collects user inputs for title using streamlit widget
        size = st.text_input('Enter labelling fontsize', 9)
        
        #Dynamic Variables
        
        variables = []
        num_variables = st.number_input("Number of variables", min_value=1, max_value=20, value=2, step=1)
        
        for x in range(num_variables):
            var_name = st.text_input(f'Enter variable {x+1} name', f'Variable {x+1}')
            variables.append(var_name)
            
        for var in variables:
            if var in df.columns:
                st.write(" ")
            else:
                st.write(f"Warning: Column '{var}' does not exist in File")
                
        
        legend = variables + ['Impurities']
        
        colours_specific = ['#118ab2', '#06d6a0', '#ffd166', '#f48c06', '#ef476f', '#ff8fa3', '#dabfff']
        
        if not df.empty:
           
            df.replace('-', 0, inplace=True)
 
            imp_cols = [col for col in df.columns if col.startswith('imp') or col.startswith('Imp') or col.startswith('imp ') or col.startswith('Imp ') or col.startswith('UnK') or col.startswith('unk')] # select columns starting with a certain word

            df['Impurities'] = df[imp_cols].sum(axis=1) # will create a new column called impurities where the column name starts with imp/unk etc. and will sum this row wise (axis=1) is required

            df.drop(columns=imp_cols, inplace=True) # gets rid of the old columns that were used in the combined column

            selected_columns = ['Conditions'] + [var for var in variables if var in df.columns] + ['Impurities']
            df = df.loc[:, selected_columns] # how can I automate this selection?
            
            st.write('Preview of Data for Screen Chart')
            st.write(df.head())

            df.plot.bar(x='Conditions', stacked=True, color=colours_specific)
            plt.xlabel(x_axis, fontproperties=font_prop)
            plt.ylabel('LCAP / %', fontproperties=font_prop)
            plt.xticks(fontproperties=font_prop)
            plt.yticks(fontproperties=font_prop)
            plt.legend(loc='upper left', bbox_to_anchor=(1,1), prop=font_prop, labels=legend)
            plt.title(title, fontproperties=font_prop)

            bar1 = []
            for y, row in df.iterrows():
                value = row[variables[0]]  # Access the first variable
                bar1.append(value) 
            
            for i, row in df.iterrows():
                value=row.iloc[2]
                plt.text(i,(value/2)+bar1[i], f'{value:.2f}', ha='center', fontdict=font_prop, fontsize=size)

                
            st.pyplot(plt.gcf()) # plots the bar chart
            
        else: # if the dataframe is empty the else phrase will occur
            st.write('Please upload an excel file to proceed')

        
        
    
else:
    
    # Solubility sheet download

    data = {
            "Solvent": ["Solvent A", "Solvent B", "Solvent C"],
            "Solubility (mg/ml)": [10, 15, 20],
            "Temperature": [25, 50, 25]
        }  # Random data that can be replaced
    
    excel_template = pd.DataFrame(data) # transformation of the data dictionary to a pandas data frame

    excel_file = io.BytesIO() # in-memory binary stream to store the excel file - will be written into a stream rather than a file to be saved on a disk

    with pd.ExcelWriter(excel_file, engine='xlsxwriter') as writer: # pd.ExcelWriter is a pandas function for converting data into an excel file
        excel_template.to_excel(writer, index=False, sheet_name='Sheet1') # converts the stream file to an excel file

    
    excel_file.seek(0) #  resets pointer back to the beginning
    
    # Downloader for template file

    st.download_button(
                label="Download Solubility Sheet Template.xlsx ",
                data=excel_file,
                file_name="Solubility_Template.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )  # Makes it so you can download the excel file with the streamlit widget
    
    
    with st.expander("Quick instruction📝"): 
        st.markdown('''
                1. Download solubility sheet template
                2. Fill in sheet with solvents/solvent systems, solubility values and temperature
                3. Drag and drop solubility excel file to submit
                4. Fill out Labels and Titles
                5. Generate your Solubility Graph :)
                6. Any questions please speak with RJ
                ''')
    
    file = st.file_uploader("Choose an '.xlsx' (excel) File for Solubility Data", type = ['xlsx']) # streamlit file uploader where the excel type is specified
    
    if file:
        df = pd.read_excel(file)  # reads the file into the dataframe using pandas
        st.write('Preview of Excel file')
        st.write(df.head()) # displays dataframe in the streamlit application

        for x, row in df.iterrows():  # will iterate of each row and if the value is less than 0 will change value to 0
            if row['Solubility (mg/ml)'] < 0: # if the row of colum solubility is less than 0
                df.at[x, 'Solubility (mg/ml)'] = 0 # value at that point will = 0
            
        label_1 = st.text_input('Enter Label 1', '25 °C') # collects user inputs for labels using streamlit widget
        label_2 =  st.text_input('Enter Label 2', '50 °C')
        title = st.text_input('Enter chart title', 'Solubility Study at 25°C and 50°C') # collects user inputs for title using streamlit widget

        colours = ['#39beea', '#ffa42e'] # specifies the colours, popped in a list so that it stays in order and doesn't assign it randomly

        if not df.empty: # command checks if the dataframe is empty or not, if it's not it will progress with plotting the barchart
            
            
            fig, ax = plt.subplots()
            ax = sns.barplot(x='Solvent', y='Solubility (mg/ml)', hue='Temperature', data=df, palette=colours)
            plt.xticks(rotation=90, fontproperties=font_prop)
            plt.yticks(fontproperties=font_prop)
            plt.title(title, fontproperties=font_prop)
            plt.axhline(y=20, color='#84848b', linestyle='--', linewidth=0.7)

            handles, labels = ax.get_legend_handles_labels() # gets the existing legend but need to define the ax first (see above) and also place this after the graph has been plotted!
            new_labels = [label_1, label_2] # defining labels from the user inputs
            ax.legend(handles=handles, labels=new_labels, loc='upper right', bbox_to_anchor=(1.2,1), prop=font_prop) #handles is the original legend and colours that you have defined previously, and then labels is the new thing you have defined

            st.pyplot(fig) # plots the bar chart
        else: # if the dataframe is empty the else phrase will occur
            st.write('Please upload an excel file to proceed')
