import pandas as pd
import numpy as np

# 1. Carica e pulisce i dati temporali
# Importa il file CSV e imposta la colonna 'date' come indice temporale
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], index_index='date')

# Pulisce i dati rimuovendo il 2.5% dei giorni con visite troppo alte o troppo basse (outliers)
df = df[
    (df['value'] >= df['value'].quantile(0.025)) &
    (df['value'] <= df['value'].quantile(0.975))
]

def draw_line_plot():
    # Restituisce i dati pronti per il grafico a linee (andamento temporale giorno per giorno)
    return df

def draw_bar_plot():
    # 2. Raggruppa i dati per Anno e Mese per il grafico a barre
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month_name()
    
    # Calcola la media delle visite per ogni mese di ogni anno
    df_groupby = df_bar.groupby(['year', 'month'])['value'].mean().unstack()
    
    # Ordina i mesi da Gennaio a Dicembre per i test di freeCodeCamp
    months_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    df_groupby = df_groupby.reindex(columns=months_order)
    
    return df_groupby

def draw_box_plot():
    # 3. Prepara i dati per i Box Plot (confronto della distribuzione tra anni e mesi)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]
    
    # Ordina i mesi in formato abbreviato (Jan, Feb, ecc.)
    month_list = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    df_box['month'] = pd.Categorical(df_box['month'], categories=month_list, ordered=True)
    
    return df_box
