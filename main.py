import streamlit as st
import pandas as pd
import numpy as np
from streamlit_extras.metric_cards import style_metric_cards
import plotly as pl
import plotly.express as px

#load dataframe
@st.cache_data
def load_data() -> pd.DataFrame:
        dataframe = pd.read_excel("dados.xlsx")
        dataframe["Data"] = dataframe["Data"].astype("string")
        
        return dataframe.head(200)

def build_where_clause(filter_results: dict) -> str:
    clause_list = list()
    for column in FILTER_LIST:
        if filter_results[column] != []:
            clause_list.append(f"`{column}` in {filter_results[column]}")
    
    clause_treated = str(clause_list) \
                        .replace('", "',' & ')[1:-1] \
                        .replace('[','(') \
                        .replace(']',')')
    return clause_treated

def set_sidebar(

    dataframe: pd.DataFrame = None, 
    filtered: pd.DataFrame = None) -> dict:
    
    st.sidebar.image("img/db1.png")
    st.sidebar.title("Selecione o Filtro: ")
    if filtered is None:
        df = dataframe
    else:
        df = filtered
    filter_results = dict()
    for i, name in enumerate(FILTER_LIST):
        component = st.sidebar.multiselect(
            key=i,
            label=name,
            options=df[name].unique(),
            help=f"Select a {name}"
        )
        filter_results.update({str(name) : component})


    return filter_results



# st.set_page_config(
#     page_title="Dagoberto Barcellos",
#     page_icon="🧊",
#     layout="wide",
#     initial_sidebar_state="expanded",
#     menu_items={
#         'Get Help': 'https://www.extremelycoolapp.com/help',
#         'Report a bug': "https://www.extremelycoolapp.com/bug",
#         'About': "# This is a header. This is an *extremely* cool app!"
#     }
# )


# with st.sidebar:
#     st.sidebar.image("img\db1.png", use_column_width=True)

#     option = st.radio(
#     "Produção :chart_with_upwards_trend:",
#     ["Total :chart:","Rebritagem :pick:", "Britagem :rock:", "Fertilizantes :mountain:","Cal :construction_worker:","Argamassa :bricks:"],

#     )



def build_visualizations(dataframe: pd.DataFrame):
    #KPI'S
    total_hs_paradas = round(dataframe["Hora Parada"].sum(),2)
    dif_hs_paradas =round((total_hs_paradas * 100) / 234.49,2) 
    total_hs_prod = round(dataframe["Hora Produção"].sum(),2)
    dif_hs_prod = round((total_hs_prod * 100) / 1833.34,2)
    total_quant_sc = dataframe["Quant. (SC)"].sum()
    dif_quant_sc = round((total_quant_sc * 100) / 69473,2)
    total_quant_ton = dataframe["Quant. (TN)"].sum()
    dif_quant_ton = round((total_quant_ton * 100) / 5319.7,2)
    custo_total = (
        float(round(dataframe["Custo (R$)"].sum()))
    )
    dif_custo_total = round((custo_total * 100) / 492795,2)
    ton_hs =  total_hs_prod / total_quant_ton
    
    
    

    

    st.info("Indicadores Gerais :bar_chart:")
    col1,col2,col3,col4,col5 = st.columns(5)
    
    col1.metric(
        label="Horas Paradas :clock1:",
        value=total_hs_paradas,
        delta=f"{dif_hs_paradas} % do total",
                )
    col2.metric(
        label="Horas Produção :clock1: ", 
        value=total_hs_prod,
        delta=f"{dif_hs_prod} % do total"
                )
    col3.metric(
        label="Quantidade (SC) :clipboard:",
        value=f"{total_quant_sc} sc",
        delta=f"{dif_quant_sc} % do total" 
                )
    col4.metric(
        label="Quantidade (TON) :clipboard:",
        value=f"{total_quant_ton} t",
        delta=f"{dif_quant_ton} % do total " 
                )
    col5.metric(
        label="Custo Total :moneybag:",
        value=f"{custo_total} R$",
        delta=f"{dif_custo_total} % do total",
                )
    st.divider()
    style_metric_cards()

    fig_total_hs_paradas = px.bar(
        dataframe,
        title="Horas Paradas por Fabrica",
        y='Hora Parada',
        x="Fabrica",
        color='Fabrica',
        color_discrete_sequence=["#00b036","#ffb100","#004eae"],
        
    )
    fig_total_hs_prod = px.pie(
        dataframe,
        title="Horas em Produção por Fabrica",
        labels='Hora Produção',
        names='Fabrica',
        color='Fabrica',
        color_discrete_sequence=["#00b036","#ffb100","#004eae"]
         
     )
    fig_custo_total = px.bar(
         dataframe,
         title="Custo por Fabrica",
         x='Custo Total (R$)',
         y='Fabrica',
         color='Fabrica',
         color_discrete_sequence=["#00b036","#ffb100","#004eae"]
         
        
    )
    
    fig_total_quant_ton = px.bar(
         dataframe,
         title="Produção por hora trabalhada (TN)",
         y='Quant. (TN)',
         x='Turno',
         color='Fabrica',
         color_discrete_sequence=["#00b036","#ffb100","#004eae"]
         
        
    )
# 

    coluna1,coluna2 = st.columns(2)
    with coluna1:
        with st.container(border=True,):
            st.plotly_chart(fig_total_hs_paradas)        
    with coluna2:
         with st.container(border=True,):
            st.plotly_chart(fig_total_hs_prod)
        
    coluna1,coluna2 = st.columns(2)    
    with coluna1:
        with st.container(border=True,):
            st.plotly_chart(fig_custo_total)
    with coluna2:
        with st.container(border=True,):
            st.plotly_chart(fig_total_quant_ton)
    st.divider()
    st.divider()
    col4,col5,x3,x4,x5,x6,x7,x8 = st.columns(8)
    with x8:
        st.image("img/db3.png",width=200)
    #st.dataframe(dataframe.head(20))

def main(dataframe):
    
    filter_results = set_sidebar(dataframe=dataframe)
    # print("STATE HERE", filter_results)
    filter_pattern = build_where_clause(filter_results=filter_results)
    # print("FILTER PATTERN", filter_pattern)
    df_selection = dataframe.query(
        expr=eval(filter_pattern),
        engine='python'
    ) if filter_pattern else dataframe
    
    build_visualizations(dataframe=df_selection)
    #hide_syle()

if __name__ == "__main__":
    st.set_page_config(
        page_title="Dagoberto Barcellos", 
        page_icon=":bar_chart:",
        layout="wide"
    )

    FILTER_LIST = ["Fabrica","Etapa","Turno"]

    dataframe = load_data()
    main(dataframe=dataframe)
#st.dataframe(dataframe) 
