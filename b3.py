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
    drop_mask = (data['Daily Change'] <= -opening_drop_range[0]) & (data['Daily Change'] >= -opening_drop_range[1])
    filtered_data = data[drop_mask]

    # Retorna os dados filtrados (ou qualquer outra métrica desejada)
    return filtered_data

# Definindo a interface do usuário no Streamlit
def main():
    st.title("Análise de Desempenho de Ações")

    # Campo para escolher a data inicial e final
    start_date = st.date_input("Data inicial", value=pd.to_datetime("2023-12-01"))
    end_date = st.date_input("Data final", value=pd.to_datetime("2023-12-21"))

    # Campos para escolher o range da porcentagem de queda
    min_drop = st.number_input("Porcentagem de queda mínima", min_value=0.0, max_value=100.0, value=0.10)
    max_drop = st.number_input("Porcentagem de queda máxima", min_value=0.0, max_value=100.0, value=0.50)

    # Botão para executar a análise
    if st.button("Analisar Desempenho"):
        tickers = ["AAPL", "MSFT", "GOOG"]  # Use os tickers desejados aqui
        tickers_b3 = [ticker + ".SA" for ticker in tickers]

        final_performance_results = []
        for ticker in tickers_b3:
            ticker_performance = analyze_stock_performance(ticker, start_date, end_date, (min_drop, max_drop))
            final_performance_results.extend(ticker_performance)

        performance_df = pd.DataFrame(final_performance_results)
        performance_df.sort_values(by=['Ticker', 'Daily Change'], ascending=[True, False], inplace=True)

        # Exibe o DataFrame
        st.dataframe(performance_df)

if __name__ == "__main__":
    main()