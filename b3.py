import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

# Função para analisar o desempenho das ações
def analyze_stock_performance(ticker, start_date, end_date, opening_drop_range):
    performance_list = []

    if start_date >= end_date:
        st.error('A data inicial deve ser anterior à data final.')
        return performance_list

    for opening_drop_percentage in np.arange(opening_drop_range[0], opening_drop_range[1], 0.1):
        stock_data = yf.download(ticker, start=start_date, end=end_date)

        if stock_data.empty:
            continue

        stock_data['Adjusted Opening'] = stock_data['Close'].shift(1) * (1 - opening_drop_percentage / 100)
        higher_count = (stock_data['Close'] > stock_data['Adjusted Opening']).sum()
        lower_count = (stock_data['Close'] < stock_data['Adjusted Opening']).sum()
        positive_differences = stock_data[stock_data['Close'] > stock_data['Adjusted Opening']]['Close'] / stock_data['Adjusted Opening'] - 1
        average_positive_difference = positive_differences.mean() * 100
        total_days = len(stock_data)
        higher_percentage = (higher_count / total_days) * 100 if total_days > 0 else 0
        lower_percentage = (lower_count / total_days) * 100 if total_days > 0 else 0

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

# Definindo a interface do usuário no Streamlit
def main():
    st.title("Análise de Desempenho de Ações")

    start_date = st.date_input("Data inicial", value=pd.to_datetime("2022-01-01"))
    end_date = st.date_input("Data final", value=pd.to_datetime("2023-01-01"))
    min_drop = st.number_input("Porcentagem de queda mínima", min_value=0.0, max_value=100.0, value=0.10)
    max_drop = st.number_input("Porcentagem de queda máxima", min_value=0.0, max_value=100.0, value=0.50)

    if st.button("Analisar Desempenho"):
        tickers = ["WEGE3", "ITSA4"]
        tickers_b3 = [ticker + ".SA" for ticker in tickers]
        final_performance_results = []

        for ticker in tickers_b3:
            ticker_performance = analyze_stock_performance(ticker, start_date, end_date, (min_drop, max_drop))
            final_performance_results.extend(ticker_performance)

        if not final_performance_results:
            st.error("Não foram encontrados dados para os critérios selecionados.")
            return

        performance_df = pd.DataFrame(final_performance_results)

        if performance_df.empty:
            st.error("Nenhum resultado foi retornado. Por favor, verifique os critérios de pesquisa.")
        else:
            try:
                performance_df.sort_values(by=['Ticker', 'Average Positive Difference'], ascending=[True, False], inplace=True)
                st.dataframe(performance_df)
            except KeyError as e:
                st.error(f"Erro ao ordenar o DataFrame: {e}")

if __name__ == "__main__":
    main()
