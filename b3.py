import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

# Função para análise do desempenho das ações
def analyze_stock_performance(ticker, start_date, end_date, opening_drop_range):
    performance_list = []

    for opening_drop_percentage in np.arange(opening_drop_range[0], opening_drop_range[1], 0.1):
        # Carrega dados históricos da ação entre as datas especificadas
        stock_data = yf.download(ticker, start=start_date, end=end_date)

        # Verifica se há dados suficientes para análise
        if stock_data.empty:
            continue

        # Calcula o preço de abertura ajustado pela porcentagem de queda
        stock_data['Adjusted Opening'] = stock_data['Close'].shift(1) * (1 - opening_drop_percentage / 100)

        # Calcula métricas
        higher_count = (stock_data['Close'] > stock_data['Adjusted Opening']).sum()
        lower_count = (stock_data['Close'] < stock_data['Adjusted Opening']).sum()
        positive_differences = stock_data[stock_data['Close'] > stock_data['Adjusted Opening']]['Close'] / stock_data['Adjusted Opening'] - 1
        average_positive_difference = positive_differences.mean() * 100  # Convertendo para porcentagem
        total_days = len(stock_data)
        higher_percentage = (higher_count / total_days) * 100 if total_days > 0 else 0
        lower_percentage = (lower_count / total_days) * 100 if total_days > 0 else 0

        # Adiciona os resultados à lista
        performance_list.append({
            'Ticker': ticker,
            'Drop Percentage Range': f"{opening_drop_percentage:.1f}%",
            'Higher Count': higher_count,
            'Lower Count': lower_count,
            'Higher Percentage': higher_percentage,
            'Lower Percentage': lower_percentage,
            'Average Positive Difference': average_positive_difference
        })

    return performance_list

# Lista de tickers (mantenha a sua lista original)
tickers = ["WEGE3", "ITSA4"] # Sua lista de tickers

# Adiciona o sufixo '.SA' necessário para o yfinance
tickers_b3 = [ticker + ".SA" for ticker in tickers]

# Título do aplicativo
st.title("Análise de Desempenho de Ações")

# Seletores de entrada para o usuário definir as variáveis
start_date = st.date_input("Data de Início", value=pd.to_datetime("2023-12-01"))
end_date = st.date_input("Data de Fim", value=pd.to_datetime("2023-12-21"))
opening_drop_start = st.number_input("Queda Inicial (%)", min_value=0.1, max_value=100.0, value=0.10, step=0.1)
opening_drop_end = st.number_input("Queda Final (%)", min_value=0.1, max_value=100.0, value=0.50, step=0.1)
opening_drop_range = (opening_drop_start, opening_drop_end)

# Botão para realizar a análise
if st.button("Analisar"):
    final_performance_results = []
    for ticker in tickers_b3:
        ticker_performance = analyze_stock_performance(ticker, start_date, end_date, opening_drop_range)
        final_performance_results.extend(ticker_performance)

    performance_df = pd.DataFrame(final_performance_results)
    performance_df.sort_values(by=['Ticker', 'Average Positive Difference'], ascending=[True, False], inplace=True)

    # Mostra o DataFrame no Streamlit
    st.dataframe(performance_df)

# Rodapé
st.write("Desenvolvido por [Seu Nome ou Organização]")
