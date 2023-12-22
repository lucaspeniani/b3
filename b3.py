import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

# Função para analisar o desempenho das ações
def analyze_stock_performance(ticker, start_date, end_date, opening_drop_range):
    # Busca dados históricos das ações
    data = yf.download(ticker, start=start_date, end=end_date)

    # Calcula a variação percentual diária
    data['Daily Change'] = data['Close'].pct_change()

    # Filtra os dias em que a queda foi dentro do intervalo especificado
    drop_mask = (data['Daily Change'] <= -opening_drop_range[0]/100) & (data['Daily Change'] >= -opening_drop_range[1]/100)
    filtered_data = data[drop_mask]

    # Adiciona uma coluna com o ticker
    filtered_data['Ticker'] = ticker

    # Retorna os dados filtrados
    return filtered_data

# Definindo a interface do usuário no Streamlit
def main():
    st.title("Análise de Desempenho de Ações")

    start_date = st.date_input("Data inicial", value=pd.to_datetime("2023-12-01"))
    end_date = st.date_input("Data final", value=pd.to_datetime("2023-12-21"))

    min_drop = st.number_input("Porcentagem de queda mínima", min_value=0.0, max_value=100.0, value=0.10)
    max_drop = st.number_input("Porcentagem de queda máxima", min_value=0.0, max_value=100.0, value=0.50)

    if st.button("Analisar Desempenho"):
        # Insira sua lista de tickers aqui
        tickers = [
            "MGLU3", "HAPV3", "AMER3", "ABEV3", "PETR4", "BBDC4", "B3SA3", "RAIZ4", "ITUB4", "PETZ3", "VALE3", "CIEL3",
            # ... (inclua todos os tickers da lista fornecida)
        ]

        final_performance_results = []

        for ticker in tickers:
            ticker_performance = analyze_stock_performance(ticker + ".SA", start_date, end_date, (min_drop, max_drop))
            final_performance_results.append(ticker_performance)

        # Concatena os resultados em um único DataFrame
        performance_df = pd.concat(final_performance_results)

        # Ordena o DataFrame
        performance_df.sort_values(by=['Ticker', 'Daily Change'], ascending=[True, False], inplace=True)

        st.dataframe(performance_df)

if __name__ == "__main__":
    main()
