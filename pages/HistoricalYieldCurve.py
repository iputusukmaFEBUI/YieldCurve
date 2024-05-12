import streamlit as st
import pandas as pd
import streamlit_pandas as sp
import os
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(page_title="Yield Curve Dashboard: Historical and Predictive", page_icon=":bar_chart",layout='wide')

st.header('Historical Yield Curve')
st.subheader('by I Putu Sukma Hendrawan')

st.write("Term structure of interest rate i.e., yield curve has many applications in viewing market conditions (Reinicke, 2019), fixed-income portfolio management and risk management (Lee, 2016). Despite such a significance role, the information regarding Indonesia yield curve are relatively limited, in terms of the data is commonly statically presented, and the access for particular information are commonly not available for free. Aspire to provide an alternative channel for such information, we create this dashboard presenting an interactive view of daily yield curve for 10-years period since 2024 to early May 2024. The yield curve are theoretical curves fitted from available Indonesia Government Bonds yield data from investing.com. We fitted the curve using the parsimonious model suggested by Nelson-Siegel (1987) and Diebold & Li (2006) as follows:")
st.latex(r'''
    r(T)=\beta_0 + \beta_1\left [ \frac{1-e^{\frac{-T}{\lambda} }}{\frac{-T}{\lambda}} \right ]+\beta_2\left [ \frac{1-e^{\frac{-T}{\lambda} }}{\frac{-T}{\lambda}} - e^{\frac{-T}{\lambda}}\right ]
''')
st.write("iputusukma@pm.me") 

@st.cache_data
def load_data():
    df = pd.read_csv('pages/HistYieldCurve.csv')
    return df

df = load_data()

wide_df = df
df = pd.melt(df, id_vars='Date', value_vars=['0.083','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30'])
df.columns = ['Date','Maturity','Yield']

wide_df.set_index(['Date'],inplace=True)

first_date = df['Date'].iloc[0]

def validate():
    if len(st.session_state.multiselect)==0:
        st.session_state.multiselect = first_date


input_date = st.multiselect(
    "Select the date to view the Yied Curve:",
    options = df['Date'],
    default=first_date,
    on_change=validate,
    key='multiselect',
    max_selections=4
)

df_selection = df.query("Date == @input_date")


plotly_figure = px.line(data_frame = df_selection,
                        x = df_selection['Maturity'],
                        y=df_selection['Yield'], 
                        color = df_selection['Date'], 
                        template='ggplot2', 
                        line_shape='spline',
                        color_discrete_sequence=px.colors.qualitative.Pastel, 
                        width=600, height=600
)

plotly_figure.update_xaxes(showgrid=True,
                            showline=True, linewidth=2, linecolor='grey')
plotly_figure.update_yaxes(showgrid=True,
                            showline=True, linewidth=2, linecolor='grey')
plotly_figure.update_xaxes(nticks=5)

plotly_figure.update_layout(xaxis_title="Time to Maturity (year)",
    yaxis_title="Yield (%)",
    font=dict(
        family="Tahoma",
        size=12,
        color="Black"),
    title=dict(text="Yield Curve", font=dict(size=30), automargin=True, yref='paper')
)

view_df = wide_df.query("Date == @input_date")
view_df_select = view_df.transpose()

colA,colB,colC=st.columns([1, 1,1.5],gap="medium")
with colA:
    st.table(view_df_select[:15])
with colB:
    st.table(view_df_select[16:])
with colC:
    st.plotly_chart(plotly_figure, use_container_width=True)
