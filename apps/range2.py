import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns
import plotly.express as px


def app():

    uploaded_file = st.sidebar.file_uploader("Choose a File",type="csv")
    if uploaded_file:
        df = pd.read_csv(uploaded_file)


        st.subheader("Original Data")
        st.dataframe(df)
        #st.subheader("Top Five Rows of Dataset")
        #df.head(5)
        #st.table(df)

    # Check available features

        #st.subheader("Available Features")
        #df.columns

        #st.subheader("Data Information")
        #df.info()
        #st.subheader("Check the number of rows and columns")
        #df.shape

        #st.subheader("Check Missing Values")
        #df.insnull().sum()

        #st.subheader("Check data type of each column")
        #df.dtypes

        #st.subheader("Check unique values of the dataset")
        #df.nunique()

        #df.describe()


        st.subheader("Electric Vehicle Range VS EV Brand")
        st.bar_chart(df,x="Brand",y="Range_Km")

        st.subheader("Fast Charge VS EV Brand")
        st.scatter_chart(
        df,
        x='Brand',
        y='FastCharge_KmH',
        color='Model',
        size='Range_Km',
    )


        range_df = df.sort_values(by=['Range_Km'], ascending=False)
        range_df= range_df[['Brand','Model','Range_Km']].head(n=1)
        st.table(range_df)


        #Analysis acceleration by EV Brand

        #acceleration_df2 = df.sort_values(by=['AccelSec'], ascending=False)
        #acceleration_df2= acceleration_df2[['Brand','AccelSec']].head(n=1)
        #st.bar_chart(acceleration_df2)

        #speed_df = df.sort_values(by=['TopSpeed_KmH'], ascending=False)
        #speed_df = speed_df[['Brand','Model','TopSpeed_KmH']].head(n=1)
        #st.bar_chart(speed_df)

        fig = px.bar(df,x=df['Model'],y=df['Efficiency_WhKm'],animation_frame=df['Brand'])
        st.write(fig)

        fig1 = px.bar(df,x=df['Model'],y=df['PriceEuro'],animation_frame=df['Brand'])
        st.write(fig1)



        st.sidebar.subheader('Compare Data')
        sorted_brand = sorted(df.Brand.unique())
        selected_brand = st.sidebar.multiselect('Brand',sorted_brand,sorted_brand)

        sorted_range = sorted(df.Range_Km.unique())
        selected_range = st.sidebar.multiselect('Range',sorted_range,sorted_range)
        df_selected_brand = df[(df.Brand.isin(selected_brand))&(df.Range_Km.isin(selected_range))]

        st.header('Display Data')
        st.write('Data:'+str(df_selected_brand.shape[0])+'rows and'+ str(df_selected_brand.shape[1])+ ' columns.')
        st.dataframe(df_selected_brand)

        #df_grouped = (df.groupby(by=["Brand"]).count()[["Range_Km"]].sort_values(by="Range_Km"))
        #bar_chart = px.pie(df_selected_brand,title="Range",values='Range_Km',names='Brand')
        #chart_data = pd.DataFrame({"Brand","Range_Km","TopSpeed_KmH"})
        st.bar_chart(df_selected_brand,x="Brand",y="Range_Km",color="TopSpeed_KmH")



        st.sidebar.subheader('Filter Data')
        sorted_brand = sorted(df.Brand.unique())
        selected_brand = st.sidebar.multiselect('Brand',sorted_brand)

        st.sidebar.subheader('Efficiency Kilometer')
        sorted_km = sorted(df.Efficiency_WhKm.unique())
        selected_km = st.sidebar.multiselect('Efficiency Kilometer',sorted_km)



        df = df.sort_values(by='Brand',ascending=True)
        selected = st.multiselect('Select Brand',df.columns[1:],[df.columns[1]])

        st.write(df[['Brand']+selected].set_index('Brand'))

        fig = px.line(df,x='Brand',y=selected)

        st.write(fig)
