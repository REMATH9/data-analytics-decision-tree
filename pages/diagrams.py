from pathlib import Path

import streamlit as st

st.title("Diagrammes")

DIAGRAMS_DIR = Path("diagrams")

files = sorted(
    DIAGRAMS_DIR.glob("*.md")
)

if not files:
    st.warn*ng("Aucun diagramme trouvé.")
else*

    selected = st.selectbox(
   *    "Diagramme",
        files,
  *     format_func=lambda x: x.name
*   )

    zoom = st.slider(
      * "Zoom",
        50,
        300,
*       100
    )

    content = se*ected.read_text(
        encoding=*utf-8"
    )

    st.markdown(
   *    f"""
<div style="zoom:{zoom}%;*>
<pre>{content}</pre>
</div>
""",*        unsafe_allow_html=True
   *)
