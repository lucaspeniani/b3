import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

def analyze_stock_performance(ticker, start_date, end_date):
    # Busca dados históricos das ações
    data = yf.download(ticker, start=start_date, end=end_date)

    # Calcula a variação percentual na abertura
    data['Open Change %'] = ((data['Open'] - data['Close'].shift(1)) / data['Close'].shift(1)) * 100

    # Calcula a média da variação
    avg_open_change = data['Open Change %'].mean()

    # Calcula contagens e porcentagens
    count_higher = data[data['Open Change %'] > avg_open_change].shape[0]
    count_lower = data[data['Open Change %'] < avg_open_change].shape[0]
    percent_higher = (count_higher / data.shape[0]) * 100
    percent_lower = (count_lower / data.shape[0]) * 100

    # Calcula a diferença positiva média
    positive_differences = data[data['Open Change %'] > 0]['Open Change %']
    avg_positive_difference = positive_differences.mean()

    return {
        'Código': ticker,
        'Porcentagem de queda na abertura': avg_open_change,
        'Contagem Maior': count_higher,
        'Contagem Menor': count_lower,
        'Porcentagem Maior': percent_higher,
        'Porcentagem Menor': percent_lower,
        'Diferença Positiva Média': avg_positive_difference
    }

def main():
    st.title("Análise de Desempenho de Ações")

    start_date = st.date_input("Data inicial", value=pd.to_datetime("2023-12-01"))
    end_date = st.date_input("Data final", value=pd.to_datetime("2023-12-21"))

    if st.button("Analisar Desempenho"):
        # Lista de tickers
        tickers = ["WEGE3.SA", "PETR4.SA", "VALE3.SA"] # Adicione todos os tickers

        results = [analyze_stock_performance(ticker, start_date, end_date) for ticker in tickers]

        performance_df = pd.DataFrame(results)
        st.dataframe(performance_df)

if __name__ == "__main__":
    main()
