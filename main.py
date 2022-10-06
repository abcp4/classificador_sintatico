import streamlit as st

from analise_sintatica import processa


st.title("Identificação e classificação de sujeitos sintáticos - versão 0.1")


st.text_input("Digite o sua frase aqui", key="frase")
button = st.button('Enviar!')


if button:
    st.text(processa(st.session_state.frase))