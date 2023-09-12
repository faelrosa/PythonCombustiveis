import streamlit as st
import pandas as pd
import altair as alt
from PIL import Image



st.set_page_config(layout="wide")

@st.cache_data
def gerar_df():
  df = pd.read_excel(
    io = "combustivel.xlsx",
    engine="openpyxl",
    sheet_name="Planilha1",
    usecols="A:Q",
    nrows=20323,
  )
  return df

df = gerar_df()

colunasUteis = ['MÊS', 'PRODUTO', 'REGIÃO', 'ESTADO', 'PREÇO MÉDIO REVENDA', ]

df = df[colunasUteis]

with st.sidebar:
  # st.subheader('Preços Combustiveis')
  logo_teste = Image.open('posto-de-gasolina.png')
  st.image(logo_teste, use_column_width=True)
  # st.subheader('SELEÇÃO DE FILTROS')
  fProduto = st.selectbox(
    "Selecione o combustível:",
    options=df['PRODUTO'].unique()
  )

  fEstado = st.selectbox(
    "Selecione o Estado:",
    options= df['ESTADO'].unique()
  )

  dadosUsuario = df.loc[(
    df['PRODUTO'] == fProduto) &
    (df['ESTADO'] == fEstado)
  ]

updateDatas = dadosUsuario['MÊS'].dt.strftime('%Y/%b')
dadosUsuario['MÊS'] = updateDatas[0:]

st.header('PREÇOS DOS COMBUSTIVEIS NO BRASIL: 2013 À 2022')
st.markdown('**Combustível selecionado** ' + fProduto)
st.markdown('**Estado** ' + fEstado)


grafComEstado = alt.Chart(dadosUsuario).mark_line(
  point=alt.OverlayMarkDef(color='red' , size=20)
).encode(
  x = 'MÊS:T',
  y = 'PREÇO MÉDIO REVENDA',
  strokeWidth = alt.value(3)
).properties(
  height = 700,
  width = 1500
)
st.altair_chart(grafComEstado)