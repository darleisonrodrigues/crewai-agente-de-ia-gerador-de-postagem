import streamlit as st
from app import gerar_publicacao
import pyperclip

st.set_page_config(page_title="Gerador de Conteúdo LinkedIn")
st.title("🚀 Gerador de Conteúdo ")

if "post_gerado" not in st.session_state:
    st.session_state.post_gerado = None

tema = st.text_input("Tema do post:", placeholder="Ex: Liderança, Marketing Digital, Inovação...")

if st.button("✨ Gerar Post"):
    if tema.strip():
        with st.spinner("🤖 Criando..."):
            st.session_state.post_gerado = gerar_publicacao(tema)

if st.session_state.post_gerado:
    texto = st.text_area("", value=st.session_state.post_gerado, height=400)
    if st.button("📋 Copiar"):
        pyperclip.copy(texto)
        st.success("Copiado!")

 
