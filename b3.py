import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

# Simulando um banco de dados de usuários (em produção, use um banco de dados real)
usuarios = {
    "admin": "admin123",
    "usuario2": "senha2"
}

def verificar_credenciais(usuario, senha):
    """Verifica se as credenciais estão corretas."""
    return usuario in usuarios and usuarios[usuario] == senha

# Página de Login
def mostrar_pagina_login():
    st.title("Login")
    usuario = st.sidebar.text_input("Usuário")
    senha = st.sidebar.text_input("Senha", type="password")

    if st.sidebar.button("Login"):
        if verificar_credenciais(usuario, senha):
            st.session_state['autenticado'] = True
        else:
            st.error("Usuário ou senha incorretos.")

# Função para análise do desempenho das ações
def analyze_stock_performance(ticker, start_date, end_date, opening_drop_range):
    performance_list = []
    for opening_drop_percentage in np.arange(opening_drop_range[0], opening_drop_range[1], 0.1):
        try:
            stock_data = yf.download(ticker, start=start_date, end=end_date)
            if stock_data.empty:
                continue
            stock_data['Adjusted Opening'] = stock_data['Close'].shift(1) * (1 - opening_drop_percentage / 100)
            higher_count = (stock_data['Close'] > stock_data['Adjusted Opening']).sum()
            lower_count = (stock_data['Close'] < stock_data['Adjusted Opening']).sum()
            higher_percentage = (higher_count / len(stock_data)) * 100 if len(stock_data) > 0 else 0
            lower_percentage = (lower_count / len(stock_data)) * 100 if len(stock_data) > 0 else 0
            avg_open_close_percentage = ((stock_data['Close'] / stock_data['Adjusted Opening'] - 1).mean()) * 100
            performance_list.append({
                'Ticker': ticker,
                'Drop Percentage': f"{opening_drop_percentage:.1f}%",
                'Higher Count': higher_count,
                'Lower Count': lower_count,
                'Higher Percentage': f"{higher_percentage:.2f}%",
                'Lower Percentage': f"{lower_percentage:.2f}%",
                'Avg Open-Close %': f"{avg_open_close_percentage:.2f}%"
            })
        except Exception as e:
            st.error(f"Falta de dados para: {ticker}: {e}")
    return performance_list

# Página principal com análise de desempenho das ações
def mostrar_pagina_principal():
    st.title("Análise de Desempenho de Ações")

    start_date = st.date_input("Data de Início", value=pd.to_datetime("2023-12-01"))
    end_date = st.date_input("Data de Fim", value=pd.to_datetime("2023-12-21"))
    opening_drop_start = st.number_input("Queda Inicial (%)", min_value=0.1, max_value=100.0, value=0.10, step=0.1)
    opening_drop_end = st.number_input("Queda Final (%)", min_value=0.1, max_value=100.0, value=0.50, step=0.1)
    opening_drop_range = (opening_drop_start, opening_drop_end)
    
    # Lista de tickers
    tickers = [
    "MGLU3", "HAPV3", "AMER3", "ABEV3", "PETR4", "BBDC4", "B3SA3", "RAIZ4", "ITUB4", "PETZ3", "VALE3", "CIEL3",
    "ITSA4", "CMIG4", "SEQL3", "COGN3", "EMBR3", "CPLE6", "AZUL4", "SOMA3", "RAIL3", "EQTL3", "GGBR4", "GOAU4",
    "CVCB3", "VBBR3", "LREN3", "PETR3", "CRFB3", "BBDC3", "JBSS3", "PDGR3", "BRFS3", "BEEF3", "GOLL4", "BRKM5",
    "CCRO3", "BBAS3", "MRFG3", "PCAR3", "MRVE3", "USIM5", "IFCM3", "TRPL4", "CSNA3", "AERI3", "BBSE3", "ANIM3",
    "CMIN3", "STBP3", "CPLE3", "TIMS3", "RENT3", "ENEV3", "RDOR3", "ASAI3", "UGPA3", "ELET3", "CSAN3", "WEGE3",
    "NTCO3", "AURE3", "POMO4", "GMAT3", "CEAB3", "PRIO3", "DXCO3", "RADL3", "GFSA3", "RRRP3", "SUZB3", "SLCE3",
    "QUAL3", "LWSA3", "YDUQ3", "VAMO3", "BRAP4", "BMGB4", "EGIE3", "OIBR3", "CYRE3", "CBAV3", "SBSP3", "KLBN4",
    "BPAN4", "BRSR6", "ALPA4", "AZEV4", "ESPA3", "GGPS3", "SMFT3", "TTEN3", "ONCO3", "ZAMP3", "CXSE3", "SAPR4",
    "RECV3", "HBSA3", "GUAR3", "RCSL4", "ENAT3", "TEND3", "LJQQ3", "PLPL3", "TOTS3", "MTRE3", "SBFG3", "MULT3",
    "CSMG3", "RCSL3", "ECOR3", "RAPT4", "CASH3", "FLRY3", "CURY3", "SIMH3", "MOVI3", "DIRR3", "IRBR3", "HBRE3",
    "HYPE3", "SMTO3", "CPFE3", "ARZZ3", "AESB3", "JHSF3", "EZTC3", "VIVT3", "LIGT3", "MLAS3", "PSSA3", "KLBN3",
    "MYPK3", "EVEN3", "INTB3", "VIVA3", "ABCB4", "ELET6", "VVEO3", "AMBP3", "SEER3", "MBLY3", "PGMN3", "MDIA3",
    "TRIS3", "HBOR3", "KEPL3", "AZEV3", "JALL3", "ODPV3", "RANI3", "NEOE3", "ORVR3", "MEAL3", "GRND3", "CAML3",
    "AALR3", "POSI3", "BRIT3", "WIZC3", "SGPS3", "MDNE3", "MILS3", "VULC3", "WEST3", "AGRO3", "LUPA3", "NGRD3",
    "PINE4", "CMIG3", "FRAS3", "DESK3", "SHUL4", "ROMI3", "AMAR3", "BLAU3", "LEVE3", "TASA4", "KRSA3", "PNVL3",
    "PTBL3", "USIM3", "OPCT3", "CSED3", "SAPR3", "ITSA3", "TRAD3", "ALPK3", "MATD3", "CLSA3", "BMOB3", "LAVV3",
    "ITUB3", "VLID3", "TUPY3", "MELK3", "ETER3", "CTNM4", "ENJU3", "IGTI3", "IGTI3", "TGMA3", "UNIP6", "SOJA3",
    "FIQE3", "RNEW3", "VITT3", "VIVR3", "PRNR3", "ALLD3", "ARML3", "TAEE4", "TCSA3", "SHOW3", "RNEW4", "JSLG3",
    "DASA3", "GGBR3", "PORT3", "DMVF3", "SYNE3", "PFRM3", "CAMB3", "TAEE3", "NINJ3", "FESA4", "TFCO4", "SANB3",
    "CTSA3", "TECN3", "CSUD3", "SANB4", "RSID3", "LOGG3", "GOAU3", "INEP3", "ELMD3", "CTSA4", "ATMP3", "EQPA3",
    "JFEN3", "EUCA4", "PDTC3", "BIOM3", "VSTE3", "TEKA4", "POMO3", "LOGN3", "BRKM3", "LPSB3", "LVTC3", "LAND3",
    "DEXP3", "SNSY5", "DOTZ3", "INEP4", "UCAS3", "BOBR4", "BRAP3", "CEBR5", "AGXY3", "TASA3", "DOHL4", "RAPT3",
    "OIBR4", "OSXB3", "CEBR6", "SCAR3", "CLSC4", "CGRA4", "ALUP4", "TPIS3", "COCE5", "HAGA4", "WHRL4", "UNIP3",
    "BEES3", "ALUP3", "RDNI3", "HOOT4", "PMAM3", "ATOM3", "WHRL3", "PTNT4", "FHER3", "CEBR3", "REDE3", "RPMG3",
    "OFSA3", "CEDO4", "APER3", "BPAC3", "BEES4", "TRPL3", "ENGI4", "BRSR3", "CGRA3", "BMEB4", "BAZA3", "MTSA4",
    "DEXP4", "FRTA3", "EMAE4", "AVLL3", "EALT4", "RSUL4", "BPAC5", "FRIO3", "EPAR3", "NUTR3", "CRPG5", "MNPR3",
    "ALPA3", "CGAS5", "BGIP4", "GEPA4", "NEXP3", "BRIV4", "ENGI3", "BAHI3", "BALM4", "WLMM4", "CSRN3", "BSLI3",
    "CLSC3", "HETA4", "EQMA3B", "EUCA3", "TELB4", "ESTR4", "CTNM3", "AFLT3", "SNSY3", "MNDL3", "CEEB3", "CEED4",
    "BSLI4", "EALT3", "PLAS3", "BMIN3", "CTKA4", "BMIN4", "PTNT3", "RPAD5", "FESA3", "EKTR4", "CRPG6", "CSRN6",
    "MWET4", "HAGA3", "BMKS3", "ENMT3", "IGTI4", "IGTI4", "BALM3", "FIEI3", "MRSA3B", "RPAD6", "CALI3", "BMEB3",
    "TELB3", "BRGE12", "NORD3", "CGAS3", "BNBR3", "CPLE5", "MGEL4", "BRSR5", "BRGE11", "DTCY3", "CEED3", "BAUH4",
    "BDLL4", "CRIV4", "UNIP5", "PATI3", "CEDO3", "MRSA5B", "LIPR3", "CSAB4", "PEAB3", "LUXM4", "BRKM6", "BDLL3",
    "BRGE8", "RPAD3", "CRIV3", "BRGE6", "ENMT4", "MERC4", "GEPA3", "CTKA3", "BRIV3", "JOPA3", "WLMM3", "AHEB3",
    "DOHL3", "CBEE3", "BRGE3", "MAPT4", "GSHP3", "CSAB3", "MOAR3", "EQPA7", "CRPG3", "MEGA3", "EQPA5", "HBTS5",
    "BGIP3", "DMFN3", "CEEB5", "CSRN5", "BRGE5", "TKNO4", "ELET5", "SOND6", "SOND5", "GPAR3", "SQIA3", "ESTR3",
    "BRGE7", "MRSA6B", "ALSO3", "BRPR3", "PATI4", "MTSA3", "SLED4", "SLED3", "EQPA6", "AHEB6", "PINE3", "VIIA3",
    "EKTR3", "MWET3", "USIM6", "AHEB5", "ENBR3", "BOAS3", "PEAB4", "COCE3", "JOPA4", "MODL3", "MERC3", "CEGR3",
    "MAPT3", "CRDE3", "IGBR3", "MSPA4", "ODER4", "PARD3", "CASN3", "WIZS3", "LLIS3", "MSPA3", "BRML3", "DMMO3",
    "GETT3", "GETT4", "SULA4", "SULA3", "CEPE5", "TCNO4", "TCNO3", "CEPE6", "BKBR3", "MTIG4", "BLUT4", "BLUT3",
    "MODL4", "CARD3", "SHUL3", "FIGE3", "FNCN3", "TEKA3", "HETA3", "LCAM3", "BIDI4", "BIDI3", "EEEL4", "EEEL3",
    "BBRK3", "SOND3", "CESP6", "CESP3", "CESP5", "ECPR4", "MOSI3", "POWE3", "ECPR3", "GNDI3", "LAME4", "LAME3",
    "OMGE3", "IGTA3", "JPSA3", "BRDT3", "JBDU4", "JBDU3", "HGTX3", "CCPR3", "DTEX3", "VVAR3", "PNVL4", "TESA3",
    "BTOW3", "LINX3", "BTTL3", "GPCP3", "GPCP4", "SMLS3", "MMXM3", "BSEV3", "CNTO3", "TIET4", "TIET3", "CORR4",
    "CEPE3", "CALI4", "SNSY6", "CASN4", "EMAE3", "BPAR3", "APTI4", "VSPT3", "MTIG3", "FIGE4", "LUXM3", "TKNO3",
    "COCE6", "MGEL3", "CTSA8", "MMAQ4"
] # Complete com a lista de tickers completa
    tickers_b3 = [ticker + ".SA" for ticker in tickers]

    if "final_performance_results" not in st.session_state:
        st.session_state.final_performance_results = []

    if st.button("Analisar"):
        st.session_state.final_performance_results = []
        progress_bar = st.progress(0)
        progress_text = st.caption("0% Completo")  # Elemento de texto para a porcentagem
        total_tickers = len(tickers_b3)

        for i, ticker in enumerate(tickers_b3):
            ticker_performance = analyze_stock_performance(ticker, start_date, end_date, opening_drop_range)
            st.session_state.final_performance_results.extend(ticker_performance)
            progress = (i + 1) / total_tickers
            progress_bar.progress(progress)
            progress_text.caption(f"{progress * 100:.0f}% Completo")  # Atualizando a porcentagem

        progress_bar.empty()

    if st.session_state.final_performance_results:
        performance_df = pd.DataFrame(st.session_state.final_performance_results)
        performance_df['Avg Open-Close %'] = performance_df['Avg Open-Close %'].str.rstrip('%').astype(float)

        st.sidebar.title("Filtros")
        num_best_stocks = st.sidebar.slider("Número de Melhores Ações", 1, len(tickers_b3), 5)
        selected_ticker = st.sidebar.selectbox("Selecionar Ticker", tickers_b3)
        sort_by = st.sidebar.selectbox("Classificar por", performance_df.columns)
        ascending = st.sidebar.checkbox("Ordem Crescente", True)

        if num_best_stocks > 0 and num_best_stocks <= len(performance_df):
            best_stocks_df = performance_df.nlargest(num_best_stocks, 'Avg Open-Close %')
            st.subheader(f"{num_best_stocks} Ações Classificadas com Rentabilidade:")
            st.dataframe(best_stocks_df)

        selected_stock_df = performance_df[performance_df['Ticker'] == selected_ticker]
        if selected_ticker:
            st.subheader(f"Desempenho para {selected_ticker}:")
            st.dataframe(selected_stock_df)

        sorted_df = performance_df.sort_values(by=[sort_by], ascending=[ascending])
        st.subheader(f"Classificado por {sort_by}:")
        st.dataframe(sorted_df)
    else:
        st.error("Nenhum dado foi retornado para os tickers selecionados.")

# Verificando se o usuário está autenticado
if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False

if st.session_state['autenticado']:
    mostrar_pagina_principal()
else:
    mostrar_pagina_login()
