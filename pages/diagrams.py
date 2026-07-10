from pathlib import Path
import re

import streamlit as st
from streamlit_mermaid_interactive import mermaid

from utils.concepts import load_concepts


st.title("Diagrammes")


DIAGRAMS_DIR = Path("diagrams")


def extract_mermaid(markdown_text):

    pattern = r"```mermaid\s*(.*?)```"

    match = re.search(
        pattern,
        markdown_text,
        re.DOTALL
    )

    if match:
        return match.group(1).strip()

    return ""


def enhance_mermaid(
    diagram_code,
    font_size
):

    return f"""
%%{{init: {{
  "theme": "default",
  "flowchart": {{
      "useMaxWidth": false,
      "htmlLabels": true
  }},
  "themeVariables": {{
      "fontSize": "{font_size}px"
  }}
}}}}%%

{diagram_code}
"""


def display_concept(
    concept_name,
    concepts
):

    if concept_name not in concepts:

        st.info(
            f"Aucune fiche trouvée pour : {concept_name}"
        )

        return

    detail = concepts[concept_name]

    st.divider()

    st.subheader(
        f"📚 {concept_name}"
    )

    if "definition" in detail:

        st.markdown(
            "### Définition"
        )

        st.write(
            detail["definition"]
        )

    if "explication_simple" in detail:

        st.markdown(
            "### Explication simple"
        )

        st.write(
            detail[
                "explication_simple"
            ]
        )

    if "exemple" in detail:

        st.markdown(
            "### Exemple"
        )

        st.code(
            detail["exemple"],
            language="text"
        )

    if "quand_utiliser" in detail:

        st.markdown(
            "### Quand utiliser ?"
        )

        for item in detail[
            "quand_utiliser"
        ]:

            st.write(
                f"✅ {item}"
            )

    if "avantages" in detail:

        st.markdown(
            "### Avantages"
        )

        for item in detail[
            "avantages"
        ]:

            st.write(
                f"✅ {item}"
            )

    if "limites" in detail:

        st.markdown(
            "### Limites"
        )

        for item in detail[
            "limites"
        ]:

            st.write(
                f"⚠️ {item}"
            )

    if "exemple_metier" in detail:

        st.markdown(
            "### Exemple métier"
        )

        st.info(
            detail[
                "exemple_metier"
            ]
        )


concepts = load_concepts()

files = sorted(
    DIAGRAMS_DIR.glob("*.md")
)

if not files:

    st.warning(
        "Aucun diagramme trouvé."
    )

else:

    col1, col2, col3 = st.columns(
        [4, 1, 1]
    )

    with col1:

        selected_file = st.selectbox(
            "Diagramme",
            files,
            format_func=lambda x: x.name
        )

    with col2:

        diagram_height = st.slider(
            "Hauteur",
            1000,
            6000,
            3000,
            100
        )

    with col3:

        font_size = st.slider(
            "Texte",
            14,
            80,
            28,
            2
        )

    content = selected_file.read_text(
        encoding="utf-8"
    )

    lines = content.splitlines()

    title = selected_file.stem

    if lines:

        first_line = lines[0]

        if first_line.startswith("#"):

            title = (
                first_line
                .replace("#", "")
                .strip()
            )

    st.header(title)

    diagram_code = extract_mermaid(
        content
    )

    if not diagram_code:

        st.error(
            "Aucun diagramme Mermaid trouvé."
        )

    else:

        diagram_code = enhance_mermaid(
            diagram_code,
            font_size
        )

        st.markdown(
            f"""
            <style>
            iframe {{
                min-height:{diagram_height}px !important;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

        result = mermaid(
            diagram_code,
            theme="default",
            key=f"{selected_file.name}_{font_size}_{diagram_height}"
        )

        if (
            isinstance(
                result,
                dict
            )
            and result.get(
                "entity_clicked"
            )
        ):

            clicked = result.get(
                "entity_clicked"
            )

            st.success(
                f"Concept sélectionné : {clicked}"
            )

            display_concept(
                clicked,
                concepts
            )

    with st.expander(
        "Voir le markdown source"
    ):

        st.code(
            content,
            language="markdown"
        )
