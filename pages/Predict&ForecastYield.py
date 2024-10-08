import streamlit as st
import pandas as pd
import streamlit_pandas as sp
import os
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from statsmodels.tsa.arima_model import ARIMA
import pmdarima as pm
import numpy as np

st.set_page_config(page_title="Yield Curve Dashboard: Historical and Predictive", page_icon=":bar_chart",layout='wide')

st.header('Yield Forecasting')


@st.cache_data
def load_data():
    df = pd.read_csv('pages/LFYield.csv')
    return df

df = load_data()

df['Date']=pd.to_datetime(df['Date'])
df.set_index(['Date'],inplace=True)


dfset = df.reindex(
           pd.date_range(start=df.index.min(),
                         end=df.index.max(),
                         freq='M'),
           method='ffill')


colA,colB,colC=st.columns([1,1,1],gap="large")
with colA:
    st.write("The term structure of interest rate i.e., yield curve has many applications in viewing market conditions (Reinicke, 2019), fixed-income portfolio management, and risk management (Lee, 2016). I follow the parsimonious model by Nelson-Siegel (1987) and Diebold & Li (2006) arguing that the yield curve is determined by rather latent factors - derived from a mathematical model - which are: Level (the long-term factor/beta 0), Slope (the short term factor/beta 1), and Curvature (the medium-term factor/beta 2), accompanied by Lambda as the decay term. I estimate these parameters using a curve-fitting mechanism employing the following equation:")
    st.latex(r'''
    r(T)=\beta_0 + \beta_1\left [ \frac{1-e^{\frac{-T}{\lambda} }}{\frac{-T}{\lambda}} \right ]+\beta_2\left [ \frac{1-e^{\frac{-T}{\lambda} }}{\frac{-T}{\lambda}} - e^{\frac{-T}{\lambda}}\right ]
    ''') 
    st.write("The AR(1) model is then used to forecast the Level while the latest Slope and Curvature are used. The decay term Lambda that is used for forecasting is the arithmetic average of Lambda within the entire historical dataset, following the approach used by Reinicke (2019). Our dataset for this forecasting is the monthly yield curve (presented on per annum basis).")   
    st.write("Forecasted yield can be used for the purpose of portfolio and risk management, as well as providing a base rate for income-approach project/real estate appraisal.")
with colB:
    st.dataframe(df, width=400, height=600)
with colC:
    tenure = st.text_input("Input the maturity or tenure of the bond/project (in years), decimal is eligible for calculation:")

    if st.button('Calculate'):
        
        tenure = float(tenure)
        #beta0 = 0.07243947681522271 #result from Auto ARIMA
        beta0 = df['Level'][0]
        beta1 = df['Slope'][0]
        beta2 = df['Curvature'][0]
        constant = dfset.loc[:, 'Lambda'].mean()

        calc_yield =beta0+(beta1*((1-np.exp(-tenure/constant))/(tenure/constant)))+(beta2*(((1-np.exp(-tenure/constant))/(tenure/constant))-(np.exp(-tenure/constant))))


        st.metric(label='Yield:',value=str(format(calc_yield*100,'.3F')+"%"))
        st.write("You can use this yield as an alternative base rate or a direct discount factor for whatever kind of appraisal you currently conducted.")

        st.metric(label='Tenure:',value=str(format(tenure,'.3F')+" year"))
        st.metric(label='Level:',value=str(format(beta0,'.3F')))
        st.metric(label='Slope:',value=str(format(beta1,'.3F')))
        st.metric(label='Curvature:',value=str(format(beta2,'.3F')))
        st.metric(label='Decay term:',value=str(format(constant,'.3F')))


st.write('by I Putu Sukma Hendrawan - iputusukma@pm.me')



