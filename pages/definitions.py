# -*- coding: utf-8 -*-
import streamlit as st
from data.definitions_data import DEFINITIONS

st.set_page_config(page_title="Définitions Data & BI", page_icon="📚", layout="wide")

SECTION_ORDER = [
    ("definition", "Définition simple"),
    ("why", "Pourquoi ça existe ?"),
    ("when", "Quand l'utiliser ?"),
    ("eloy", "Exemple concret chez Eloy"),
    ("schema", "Schéma"),
    ("advantages", "Avantages"),
    ("disadvantages", "Inconvénients"),
    ("questions", "Questions qu'on pourrait se poser"),
    ("errors", "Erreurs classiques à éviter"),
]

CATEGORY_RULES = {
    "Architecture": ["warehouse", "mart", "lakehouse", "bronze", "silver", "gold", "fabric", "databricks", "vault"],
    "Modélisation": ["star", "snowflake", "flat", "dimension", "fait", "transactionnelle", "snapshot", "pont", "relation", "many"],
    "Sécurité": ["rls", "ols", "sécurité", "gateway"],
    "Pipelines & ingestion": ["pipeline", "etl", "elt", "factory", "ssis", "staging", "cdc", "streaming", "rejet"],
    "Power BI / Semantic": ["semantic", "dataset", "cube", "analysis", "direct lake", "composite", "agrégation", "cardinalité"],
    "Gouvernance": ["gouvernance", "steward", "culture", "dictionnaire", "self-service"],
}


def normalize(txt):
    return str(txt or "").lower().strip()


def detect_category(item):
    title = normalize(item.get("title", ""))
    blob = title + " " + normalize(item.get("definition", ""))
    for cat, keys in CATEGORY_RULES.items():
        if any(k in blob for k in keys):
            return cat
    return "Autres"


def as_text(value):
    if isinstance(value, list):
        if value and isinstance(value[0], tuple):
            return " ".join([f"{q} {a}" for q, a in value])
        return " ".join(map(str, value))
    return str(value or "")


def match_definition(item, query):
    if not query:
        return True
    q = normalize(query)
    haystack = " ".join([
        item.get("title", ""),
        item.get("definition", ""),
        as_text(item.get("why", [])),
        as_text(item.get("when", [])),
        item.get("eloy", ""),
        item.get("schema", ""),
        as_text(item.get("advantages", [])),
        as_text(item.get("disadvantages", [])),
        as_text(item.get("questions", [])),
        as_text(item.get("errors", [])),
    ])
    return q in normalize(haystack)


def render_list(items):
    for x in items:
        st.markdown(f"- {x}")


def render_questions(qas):
    for q, a in qas:
        st.markdown(f"**{q}**")
        st.markdown(a)


def render_card(item, compact=False):
    title = item.get("title", "Sans titre")
    category = detect_category(item)
    with st.expander(f"{title}  ·  {category}", expanded=False):
        if compact:
            st.markdown("#### Définition simple")
            st.write(item.get("definition", ""))
            st.markdown("#### Exemple concret chez Eloy")
            st.info(item.get("eloy", ""))
            return

        for key, label in SECTION_ORDER:
            value = item.get(key)
            if value in (None, "", []):
                continue
            st.markdown(f"#### {label}")
            if key == "schema":
                st.code(value, language="text")
            elif key in ["why", "when", "advantages", "disadvantages", "errors"]:
                render_list(value)
            elif key == "questions":
                render_questions(value)
            elif key == "eloy":
                st.info(value)
            else:
                st.write(value)


def main():
    st.title("Définitions Data, BI, Fabric & Power BI")
    st.caption("Glossaire avec recherche, exemples Eloy, questions/réponses et erreurs classiques à éviter.")

    enriched = []
    for item in DEFINITIONS:
        tmp = dict(item)
        tmp["category"] = detect_category(tmp)
        enriched.append(tmp)

    categories = sorted({x["category"] for x in enriched})

    col1, col2, col3 = st.columns([2.2, 1.2, 1])
    with col1:
        query = st.text_input(
            "Rechercher une définition",
            placeholder="Exemples : RLS, Direct Lake, table de faits, incremental refresh, Bronze...",
        )
    with col2:
        selected_categories = st.multiselect(
            "Catégorie",
            categories,
            default=categories,
        )
    with col3:
        compact = st.toggle("Vue courte", value=False)

    results = [
        x for x in enriched
        if x["category"] in selected_categories and match_definition(x, query)
    ]
    results = sorted(results, key=lambda x: x.get("title", ""))

    st.markdown("---")
    st.write(f"**{len(results)} définition(s) trouvée(s)** sur {len(DEFINITIONS)}.")

    if not results:
        st.warning("Aucune définition trouvée. Essaie un autre mot-clé, par exemple : modèle, sécurité, pipeline, Fabric, fait, dimension.")
        return

    tabs = st.tabs(["Résultats", "Vue par catégorie", "Index rapide"])

    with tabs[0]:
        for item in results:
            render_card(item, compact=compact)

    with tabs[1]:
        for cat in categories:
            cat_items = [x for x in results if x["category"] == cat]
            if cat_items:
                st.subheader(cat)
                for item in cat_items:
                    render_card(item, compact=compact)

    with tabs[2]:
        cols = st.columns(3)
        for i, item in enumerate(results):
            with cols[i % 3]:
                st.markdown(f"- **{item.get('title', '')}**")


if __name__ == "__main__":
    main()

