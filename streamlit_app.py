import streamlit as st
import pandas as pd
# from data import isa_universe, get_etf_name, get_score, bond_universe, get_yf_etf_name, get_yf_score
from data import bond_universe, get_yf_etf_name, get_yf_score

st.set_page_config(page_title='Signal', page_icon=':chart_with_upwards_trend:')

# st.title('Duel Momentum Strategy')
st.title('채권자산배분')

# col1, col2 = st.columns(2)

# df = pd.DataFrame(isa_universe, columns=['itemcode'])
# df['itemname'] = df['itemcode'].map(get_etf_name)
# df['score'] = df['itemcode'].map(get_score)
# df.sort_values('score', ascending=False, inplace=True)
# df.set_index('itemcode', inplace=True)
# col1.dataframe(df)

df = pd.DataFrame(bond_universe, columns=['itemcode'])
df['itemname'] = df['itemcode'].map(get_yf_etf_name)
df['score'] = df['itemcode'].map(get_yf_score)
df.sort_values('score', ascending=False, inplace=True)
df.set_index('itemcode', inplace=True)
# col2.dataframe(df)
st.dataframe(df)
