#%%
import pandas as pd
#%%
sinistros_excel = 'Sinistros_base (3).xlsx'
cadastros_excel = 'Cadastro_base (3).xlsx'

df_sinistros = pd.read_excel(sinistros_excel)
df_cadastros = pd.read_excel(cadastros_excel)

df_sinistros.columns = [
    'DT_REFERENCIA', 'CODIGO_EVENTO', 'FONTE', 'PLANO', 'TITULARIDADE', 
    'CODIGO_FAMILIA', 'CODIGO_PESSOA', 'DT_EVENTO', 'PRESTADOR', 
    'VL_EVENTO', 'DESCRITOR_EVENTO', 'INTERNACAO'
]

df_cadastros.columns = [
    'MES_REFERENCIA', 'ANO_REFERENCIA', 'CODIGO_FAMILIA', 'CODIGO_PESSOA', 
    'PLANO', 'TITULARIDADE', 'SEXO', 'IDADE', 'DT_NASCIMENTO', 
    'FAIXA_ETARIA', 'CONTRATO_ATIVO'
]
#%%
# Exercício 1
high_user = df_sinistros.groupby('CODIGO_PESSOA')['VL_EVENTO'].sum().idxmax()
high_cost = df_sinistros.groupby('CODIGO_PESSOA')['VL_EVENTO'].sum().max()

print(f'A pessoa que teve mais gastos tem o ID: {high_user} e o custo foi de R$ {high_cost:.2f}')
#%%
# Exercício 2
df_sinistros['DT_EVENTO'] = pd.to_datetime(df_sinistros['DT_EVENTO'])
df_sinistros['PERIODO'] = df_sinistros['DT_EVENTO'].dt.to_period('M').dt.to_timestamp()

df_sinistros['PERIODO_FORMATADO'] = df_sinistros['PERIODO'].dt.strftime('%d-%m-%Y')
#%%
# Custo total por período e plano
custo_total = df_sinistros.groupby(['PERIODO_FORMATADO', 'PLANO'])['VL_EVENTO'].sum().reset_index()
custo_total['VL_EVENTO'] = custo_total['VL_EVENTO'].apply(lambda x: f'{x:,.2f}')

print("Custo total por período e plano:")
print(custo_total)

pessoas_total = df_sinistros.groupby(['PERIODO_FORMATADO', 'PLANO'])['CODIGO_PESSOA'].nunique().reset_index()

dados_sinistro_pessoas = pd.merge(custo_total, pessoas_total, on=['PERIODO_FORMATADO', 'PLANO'], how='left')
#%%
# Custo de sinistro per capita
dados_sinistro_pessoas['CUSTO_PER_CAPITA'] = dados_sinistro_pessoas['VL_EVENTO'].str.replace(',', '').astype(float) / dados_sinistro_pessoas['CODIGO_PESSOA']
dados_sinistro_pessoas['CUSTO_PER_CAPITA'] = dados_sinistro_pessoas['CUSTO_PER_CAPITA'].apply(lambda x: f'{x:,.2f}')

print("\nCusto per capita:")
print(dados_sinistro_pessoas)
#%%
# Custo de sinistro total em % 
total_geral = dados_sinistro_pessoas['VL_EVENTO'].str.replace(',', '').astype(float).sum()
dados_sinistro_pessoas['Custo_PORCENTAGEM'] = (dados_sinistro_pessoas['VL_EVENTO'].str.replace(',', '').astype(float) / total_geral) * 100
dados_sinistro_pessoas['Custo_PORCENTAGEM'] = dados_sinistro_pessoas['Custo_PORCENTAGEM'].apply(lambda x: f'{x:.2f}%')

print("\nCusto total em relação ao total geral em %:")
print(dados_sinistro_pessoas)
#%%
# Exercício 3
df_sinistros['MES_ANO'] = pd.to_datetime(df_sinistros['DT_EVENTO']).dt.to_period('M')
custo_por_mes_ano = df_sinistros.groupby(['MES_ANO'])['VL_EVENTO'].sum().reset_index()
custo_por_mes_ano['VL_EVENTO'] = custo_por_mes_ano['VL_EVENTO'].apply(lambda x: f'{x:,.2f}')

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

print(custo_por_mes_ano)
#%%
# Exercício 4
custo_plano = df_sinistros.groupby('PLANO')['VL_EVENTO'].sum().sort_values(ascending=False)
custo_plano = custo_plano.apply(lambda x: f'{x:,.2f}')

print("Custo de sinistro por plano:")
print(custo_plano)