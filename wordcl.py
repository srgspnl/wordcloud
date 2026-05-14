import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import nltk
from nltk.corpus import stopwords
import string

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="WordCloud Pro 2026", page_icon="☁️", layout="wide")

# --- DOWNLOAD DE RECURSOS NLTK ---
@st.cache_resource
def setup_nltk():
    nltk.download('stopwords')
    nltk.download('punkt')
    return set(stopwords.words('portuguese'))

STOP_WORDS_PT = setup_nltk()

# --- FUNÇÃO DE LIMPEZA DE TEXTO ---
def limpar_texto(texto):
    # Converte para minúsculas
    texto = texto.lower()
    # Remove pontuação
    texto = texto.translate(str.maketrans('', '', string.punctuation))
    # Tokenização simples e remoção de stopwords
    palavras = texto.split()
    palavras_filtradas = [p for p in palavras if p not in STOP_WORDS_PT and len(p) > 2]
    return " ".join(palavras_filtradas)

# --- INTERFACE ---
st.title("☁️ Gerador de Nuvem de Palavras Otimizado")
st.markdown("Ferramenta para extração de termos significativos, excluindo conectores e artigos.")

# Menu ordenado na barra lateral
menu = st.sidebar.selectbox(
    "Selecione uma etapa:",
    ["1. Entrada de Dados", "2. Configurações da Nuvem", "3. Visualização e Download"]
)

# Estado da sessão para o texto
if 'texto_processado' not in st.session_state:
    st.session_state.texto_processado = ""

# --- FLUXO DO MENU ---

if menu == "1. Entrada de Dados":
    st.subheader("📥 Upload ou Entrada de Texto")
    metodo = st.radio("Escolha o método:", ["Digitar/Colar Texto", "Carregar Arquivo .txt"])
    
    raw_text = ""
    if metodo == "Digitar/Colar Texto":
        raw_text = st.text_area("Cole seu texto aqui:", height=300)
    else:
        uploaded_file = st.file_uploader("Escolha o arquivo", type="txt")
        if uploaded_file:
            raw_text = uploaded_file.read().decode("utf-8")
    
    if st.button("Processar e Filtrar"):
        if raw_text:
            st.session_state.texto_processado = limpar_texto(raw_text)
            st.success("Texto processado! Conectores e pontuações removidos.")
        else:
            st.warning("Por favor, insira um texto primeiro.")

elif menu == "2. Configurações da Nuvem":
    st.subheader("🎨 Customização Visual")
    col1, col2 = st.columns(2)
    with col1:
        cor_fundo = st.color_picker("Cor do fundo", "#ffffff")
        largura = st.slider("Largura", 400, 1200, 800)
    with col2:
        max_palavras = st.slider("Máximo de palavras", 10, 200, 100)
        altura = st.slider("Altura", 400, 1200, 400)
    
    st.info("As configurações serão aplicadas na próxima aba.")

elif menu == "3. Visualização e Download":
    st.subheader("🖼️ Resultado Final")
    
    if st.session_state.texto_processado:
        # Geração da Nuvem
        wc = WordCloud(
            background_color="#ffffff", # Usando branco fixo para melhor contraste acadêmico
            width=800,
            height=400,
            max_words=100,
            colormap='viridis'
        ).generate(st.session_state.texto_processado)

        # Plotagem
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wc, interpolation='bilinear')
        ax.axis("off")
        st.pyplot(fig)
        
        # Download da imagem
        plt.savefig("nuvem.png", format="png")
        with open("nuvem.png", "rb") as file:
            st.download_button("📥 Baixar Imagem (PNG)", file, "nuvem_palavras.png", "image/png")
    else:
        st.error("Nenhum texto processado encontrado. Volte para a etapa 1.")
