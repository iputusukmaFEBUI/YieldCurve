
import streamlit as st
import pandas as pd
import streamlit_pandas as sp
import os
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import altair as alt

st.set_page_config(page_title="Yield Curve Dashboard: Historical and Predictive", page_icon=":bar_chart",layout='wide')

st.header('Historical Yield')
st.write('by I Putu Sukma Hendrawan - iputusukma@pm.me')

st.write("This (basic) dashboard provides the historical yield data for Indonesian Government Bonds. The data are collected from investing.com and presented in this dashboard - for both convenience and scientific purposes - using a chart and table. The charts themselves are two-dimensional and three-dimensional line charts. I do hope you enjoy the experience of using this dashboard.")


#st.sidebar.success("select the dashboard menu")

@st.cache_data
def load_data():
    df = pd.read_csv('YCdata.csv')
    return df

df = load_data()
wide_df = df
df = pd.melt(df, id_vars='Date', value_vars=['1', '3', '6','12','36','60','120','180','240','300','360'])
df.columns = ['Date','Maturity','Yield']
wide_df.set_index(['Date'],inplace=True)


st.write("The latest yield is at 2024-08-23. The delta is daily change of yield")
# ---- MAIN PAGE ----

st.markdown('##')

col1,col2,col3,col4,col5,col6=st.columns(6)

with col1:
    st.metric(label='1-Month Yield',value=str(wide_df.iloc[0,0])+"%", delta=str(format((wide_df.iloc[0,0]/wide_df.iloc[1,0]-1)*100,'.3F'))+"%")
with col2:
    st.metric(label='3-Month Yield',value=str(wide_df.iloc[0,1])+"%", delta=str(format((wide_df.iloc[0,1]/wide_df.iloc[1,1]-1)*100,'.3F'))+"%")
with col3:
    st.metric(label='1-Year Yield',value=str(wide_df.iloc[0,3])+"%", delta=str(format((wide_df.iloc[0,3]/wide_df.iloc[1,3]-1)*100,'.3F'))+"%")
with col4:
    st.metric(label='5-Year Yield',value=str(wide_df.iloc[0,5])+"%", delta=str(format((wide_df.iloc[0,5]/wide_df.iloc[1,5]-1)*100,'.3F'))+"%")
with col5:
    st.metric(label='10-Year Yield',value=str(wide_df.iloc[0,6])+"%", delta=str(format((wide_df.iloc[0,6]/wide_df.iloc[1,6]-1)*100,'.3F'))+"%")
with col6:
    st.metric(label='30-Year Yield',value=str(wide_df.iloc[0,10])+"%", delta=str(format((wide_df.iloc[0,10]/wide_df.iloc[1,10]-1)*100,'.3F'))+"%")


def validate():
    if '12' not in st.session_state.multiselect:
        st.session_state.multiselect = ['12']

st.markdown('##')

maturity = st.multiselect(
    "Select the time to maturity (in month):",
    options = ("1","3","6",'12',"36","60","120","180","240","300","360"),
    default="12",
    on_change=validate,
    key='multiselect'
)


df_selection = df.query(
    "Maturity == @maturity"
)



plotly_figure = px.line(data_frame = df_selection,
x = df_selection['Date'], y=df_selection['Yield'], color = df_selection['Maturity'], template='seaborn', line_shape='spline',
title= 'Yield of INDOGB, Maturity in Month(s)', color_discrete_sequence=px.colors.qualitative.Pastel
)

#c = (
#   alt.Chart(df_selection)
#   .mark_line()
#   .encode(x="Date", y="Yield", color="Maturity", tooltip=["Date", "Yield"])
#)

#st.altair_chart(c, use_container_width=True)



x = wide_df.columns
y = wide_df.index
z = wide_df.to_numpy()

fig = go.Figure(data=[go.Surface(z=z, x=x, y=y)])
fig.update_layout(title='3-Dimensional Historical Yield | x = Maturity in Months, y = Date, z = Yield',
                  scene = {"aspectratio": {"x": 1, "y": 1, "z": 0.4}},
                  showlegend=False
                  )

st.plotly_chart(plotly_figure, use_container_width=True)

st.markdown('##')

colA,colB,=st.columns(2,gap="large")
with colA:
    st.plotly_chart(fig)
with colB:
    st.dataframe(wide_df)
