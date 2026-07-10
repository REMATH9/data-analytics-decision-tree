import re
from pathlib import Path

import streamlit as st
from streamlit_mermaid_interactive import mermaid

st.set_page_config(
    page_title="Data Analytics Decision Tree",
    layout="wide"
)

st.title("Data Analytics Decision Tree")
st.caption("Arbre décisionnel Data / BI / Power BI")

DIAGRAMS_DIR = Path("diagrams")

def extract_mermaid_code(markdown_text: str) -> str:
    pattern = r"```mermaid\s*(.*?)```"
    match = re.search(pattern, markdown_text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return ""

files = sorted(DIAGRAMS_DIR.glob("*.md"))

if not files:
    st.warning("Aucun fichier .md trouvé dans le dossier diagrams.")
else:
    selected_file = st.sidebar.selectbox(
        "Choisir un module",
        files,
        format_func=lambda p: p.name
    )

    content = selected_file.read_text(encoding="utf-8")
    title = content.splitlines()[0].replace("#", "").strip()

    st.header(title)

    code = extract_mermaid_code(content)

    if code:
        result = mermaid(
            code,
            theme="neutral",
            key=selected_file.name
        )

        clicked = result.get("entity_clicked") if isinstance(result, dict) else None

        if clicked:
            st.info(f"Noeud sélectionné : {clicked}")
    else:
        st.error("Aucun bloc Mermaid trouvé dans ce fichier.")

    with st.expander("Voir le code Mermaid"):
        st.code(code, language="mermaid")
