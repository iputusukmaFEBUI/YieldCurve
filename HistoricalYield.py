
import streamlit as st
import pandas as pd
import streamlit_pandas as sp
import os
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Yield Curve Dashboard: Historical and Predictive", page_icon=":bar_chart",layout='wide')

st.header('Historical Yield')
st.subheader('by I Putu Sukma Hendrawan')

st.write("This (basic) dashboard provide the historical yield data for Indonesia Government Bond. The data are collected from investing.com and presented in this dashboard - for the both convenience and scientific purpose - using chart and table. The charts themselves are two dimensional and three dimensional line chart. I do hope you enjoy the experience on using this dashboard.")
st.write("iputusukma@pm.me")


st.sidebar.success("-----")

@st.cache_data
def load_data():
    df = pd.read_csv('YCdata.csv')
    return df

df = load_data()
wide_df = df
df = pd.melt(df, id_vars='Date', value_vars=['1', '3', '6','12','36','60','120','180','240','300','360'])
df.columns = ['Date','Maturity','Yield']
wide_df.set_index(['Date'],inplace=True)

#st.dataframe(df)

# ---- SIDEBAR -----



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
    if '1' not in st.session_state.multiselect:
        st.session_state.multiselect = ['1']

maturity = st.multiselect(
    "Select the time to maturity:",
    options = ("1","3","6",'12',"36","60","120","180","240","300","360"),
    default="1",
    on_change=validate,
    key='multiselect'
)


df_selection = df.query(
    "Maturity == @maturity"
)



plotly_figure = px.area(data_frame = df_selection,
x = df_selection['Date'], y=df_selection['Yield'], color = df_selection['Maturity'], template='seaborn', line_shape='spline',
title= 'Yield of INDOGB, Maturity in Month(s)', color_discrete_sequence=px.colors.qualitative.Pastel
)


x = wide_df.columns
y = wide_df.index
z = wide_df.to_numpy()

fig = go.Figure(data=[go.Surface(z=z, x=x, y=y)])
fig.update_layout(title='3-Dimensional Historical Yield | x = Maturity in Months, y = Date, z = Yield',
                  scene = {"aspectratio": {"x": 1, "y": 1, "z": 0.4}},
                  showlegend=False
                  )

st.plotly_chart(plotly_figure, use_container_width=True)

colA,colB,=st.columns(2,gap="large")
with colA:
    st.plotly_chart(fig)
with colB:
    st.dataframe(wide_df)
