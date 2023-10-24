import os
import openai
import streamlit as st
import requests
from bs4 import BeautifulSoup
import markdownify
from time import perf_counter
from streamlit_pills import pills 


from components.sidebar import sidebar
from functions.writer import writer
from functions.markdown_generator import markdown_generator
from functions.parser import parser
from functions.concurrent_analyzer import concurrent_analyzer
from functions.define_client import define_client
from functions.concurrent_sumerizer import concurrent_sumerizer
from functions.bolder_keywords import bold_keywords
from functions.better_titles import better_titles
from functions.fact_check import fact_check
from functions.completer import completer
from PIL import Image


image = Image.open("assets/favicon.png")
st.set_page_config(
    page_title="Khontenu",
    page_icon=image,
    layout="wide",
    menu_items={
        'Get help': 'mailto:eliott@khlinic.fr'
    }
)



st.header("🧠 Khontenu")
st.markdown("---")

if "shared" not in st.session_state:
   st.session_state["shared"] = True

sidebar()

openai.api_key = st.session_state.get("OPENAI_API_KEY")

st.markdown("### Rédigeons de meilleures pages que les concurrents 👀")

col1, col2 = st.columns(2)

with col1:
    check = pills("", ["Avec fact checking", "Sans fact checking"], ["✅", "🚨"])

with st.expander("Concurrence", expanded=False):
    link_1 = st.text_input("Concurrent n°1", placeholder="Lien")

col1, col2, col3 = st.columns(3)
submit = col3.button("Rédiger ✍🏻", use_container_width=1)
    
if submit:
    st.session_state["total_tokens"] = 0
    st.session_state["completion_tokens"] = 0
    st.session_state["prompt_tokens"] = 0
    st.session_state["error"] = 0

    with st.spinner("Requête en cours..."):
        ts_start = perf_counter()

        if st.session_state["error"] == 0:
            final_text = writer(link_1)
            st.write(final_text)    
  
        if st.session_state["error"] == 0:
            if check == "Avec fact checking":
                st.error("Fact checking en cours...")
                fact = fact_check(final_text)
                with st.expander("Fact checking", expanded=False):
                    st.write(fact)
        
        ts_end = perf_counter()
        st.info(f" {round(((ts_end - ts_start)/60), 3)} minutes d'exécution")
        cost = st.session_state["prompt_tokens"] * 0.00003 + st.session_state["completion_tokens"] * 0.00006
        st.write("Coût de l'article : " + str(cost) + " $")
        col1, col2, col3 = st.columns([2, 2,1])
        rewrite = col3.button("Réécrire ✍🏻", use_container_width=1)

    col1, col2, col3 = st.columns([2, 2,1])
    col3.download_button(
        label="Télécharger 💾",
        data=final_text,
        file_name='texte.md',
        mime='text/markdown',
    )
