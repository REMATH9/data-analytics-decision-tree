# pages/definitions.py
# -*- coding: utf-8 -*-

import re
import streamlit as st

try:
    from data.definitions_data import DEFINITIONS
except Exception:
    try:
        from definitions_data import DEFINITIONS
    except Exception:
        DEFINITIONS = []


CATEGORY_RULES = {
    "Architecture Data": [
        "data warehouse",
        "data mart",
        "lakehouse",
        "bronze",
        "silver",
        "gold",
        "fabric",
        "databricks",
        "data vault",
        "warehouse",
    ],
    "Modélisation BI": [
        "star",
        "snowflake",
        "flat",
        "dimension",
        "fait",
        "faits",
        "transactionnelle",
        "snapshot",
        "pont",
        "many",
        "relation",
        "schema",
    ],
    "Sécurité": [
        "rls",
        "ols",
        "sécurité",
        "security",
        "gateway",
    ],
    "Pipelines et ingestion": [
        "pipeline",
        "etl",
        "elt",
        "factory",
        "ssis",
        "staging",
        "cdc",
        "streaming",
        "rejet",
        "zone de rejet",
        "dataflows",
    ],
    "Power BI et modèles sémantiques": [
        "semantic",
        "dataset",
        "datasets",
        "cube",
        "analysis services",
        "direct lake",
        "composite",
        "agrégation",
        "agregation",
        "cardinalité",
        "cardinalite",
        "tabulaire",
    ],
    "Gouvernance": [
        "gouvernance",
        "steward",
        "self-service",
        "dictionnaire",
        "culture data",
    ],
}


LEVEL_RULES = {
    "Débutant": [
        "flat table",
        "data mart",
        "dimension modèle simple",
        "pipeline simple",
        "datasets",
        "gateway",
    ],
    "Intermédiaire": [
        "data warehouse",
        "star schema",
        "snowflake",
        "rls",
        "ols",
        "incremental refresh",
        "dataflows",
        "semantic model",
        "semantic model partagé",
        "table d’agrégation",
        "table d'agrégation",
        "réduire la cardinalité",
        "reduire la cardinalite",
        "scd type 1",
        "tables de faits",
        "relations many-to-one",
    ],
    "Avancé": [
        "lakehouse",
        "direct lake",
        "composite model",
        "data vault",
        "cdc",
        "event streaming",
        "scd type 2",
        "fabric",
        "databricks",
        "azure analysis services",
        "relations many-to-many",
        "table de pont",
    ],
}


RELATED_RULES = {
    "Data Warehouse": [
        "Data Mart",
        "Star Schema",
        "Semantic Model partagé",
        "SQL View",
    ],
    "Data Mart": [
        "Data Warehouse",
        "Star Schema",
        "Semantic Model partagé",
    ],
    "Lakehouse": [
        "Couches Bronze / Silver / Gold",
        "Direct Lake",
        "Microsoft Fabric",
        "Databricks",
    ],
    "Couches Bronze / Silver / Gold": [
        "Lakehouse",
        "Pipeline ELT",
        "Donnée rejetée et zone de rejet",
        "Direct Lake",
    ],
    "Direct Lake": [
        "Lakehouse",
        "Microsoft Fabric",
        "Semantic model tabulaire",
        "Composite Model",
    ],
    "Star Schema": [
        "Tables de faits",
        "Dimension conforme",
        "Relations many-to-one",
        "Table de pont",
    ],
    "Snowflake Schema": [
        "Star Schema",
        "Dimension modèle simple",
        "Relations many-to-one",
    ],
    "Incremental Refresh": [
        "CDC - Change Data Capture",
        "Staging avec date de modification",
        "Table d’agrégation",
        "Réduire la cardinalité",
    ],
    "CDC - Change Data Capture": [
        "Incremental Refresh",
        "Staging avec date de modification",
        "Pipeline ELT",
        "Log technique minimal",
    ],
    "RLS - Row Level Security": [
        "OLS - Object Level Security",
        "Semantic model tabulaire",
        "Gouvernance",
    ],
    "OLS - Object Level Security": [
        "RLS - Row Level Security",
        "Semantic model tabulaire",
        "Gouvernance",
    ],
    "Composite Model": [
        "Direct Lake",
        "Semantic model tabulaire",
        "Table d’agrégation",
    ],
    "Table de pont": [
        "Relations many-to-many",
        "Tables de faits",
        "Dimension conforme",
    ],
    "Relations many-to-many": [
        "Table de pont",
        "Relations many-to-one",
        "Star Schema",
    ],
    "Gouvernance": [
        "Data Steward",
        "Semantic Model partagé",
        "Self-service BI",
    ],
    "Self-service BI": [
        "Semantic Model partagé",
        "Gouvernance",
        "Data Steward",
    ],
}


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


LEVEL_COLORS = {
    "Débutant": "#2e7d32",
    "Intermédiaire": "#ef6c00",
    "Avancé": "#c62828",
}


CATEGORY_COLORS = {
    "Architecture Data": "#1f4e79",
    "Modélisation BI": "#5b2c83",
    "Sécurité": "#8b0000",
    "Pipelines et ingestion": "#006064",
    "Power BI et modèles sémantiques": "#b8860b",
    "Gouvernance": "#455a64",
    "Autres": "#616161",
}


def safe_key(value):
    value = str(value or "")
    value = value.lower()
    value = re.sub(r"[^a-z0-9_]+", "_", value)
    value = re.sub(r"_+", "_", value)
    return value.strip("_") or "key"


def rerun_app():
    try:
        st.rerun()
    except Exception:
        st.experimental_rerun()


def normalize(value):
    return str(value or "").lower().strip()


def to_text(value):
    if value is None:
        return ""

    if isinstance(value, str):
        return value

    if isinstance(value, list):
        parts = []

        for element in value:
            if isinstance(element, tuple) and len(element) == 2:
                parts.append(f"{element[0]} {element[1]}")
            else:
                parts.append(str(element))

        return " ".join(parts)

    if isinstance(value, tuple):
        return " ".join(str(x) for x in value)

    return str(value)


def detect_category(item):
    title = normalize(item.get("title", ""))
    definition = normalize(item.get("definition", ""))
    blob = f"{title} {definition}"

    for category, keywords in CATEGORY_RULES.items():
        for keyword in keywords:
            if keyword in blob:
                return category

    return "Autres"


def detect_level(item):
    title = normalize(item.get("title", ""))
    definition = normalize(item.get("definition", ""))
    blob = f"{title} {definition}"

    for level, keywords in LEVEL_RULES.items():
        for keyword in keywords:
            if keyword in blob:
                return level

    return "Intermédiaire"


def build_search_blob(item):
    values = [
        item.get("title", ""),
        item.get("definition", ""),
        item.get("category", ""),
        item.get("level", ""),
        to_text(item.get("why", [])),
        to_text(item.get("when", [])),
        item.get("eloy", ""),
        item.get("schema", ""),
        to_text(item.get("advantages", [])),
        to_text(item.get("disadvantages", [])),
        to_text(item.get("questions", [])),
        to_text(item.get("errors", [])),
    ]

    return normalize(" ".join(values))


def match_query(item, query):
    if not query:
        return True

    query = normalize(query)
    blob = build_search_blob(item)

    terms = [x.strip() for x in query.split() if x.strip()]

    if not terms:
        return True

    return all(term in blob for term in terms)


def get_initial_letter(item):
    title = item.get("title", "").strip()

    if not title:
        return "#"

    return title[0].upper()


def enrich_definitions():
    enriched = []

    for item in DEFINITIONS:
        clean_item = dict(item)
        clean_item["category"] = detect_category(clean_item)
        clean_item["level"] = detect_level(clean_item)
        clean_item["letter"] = get_initial_letter(clean_item)
        enriched.append(clean_item)

    return sorted(enriched, key=lambda x: normalize(x.get("title", "")))


def render_badge(label, color):
    st.markdown(
        f"""
        <span style="
            display:inline-block;
            background:{color};
            color:white;
            padding:4px 10px;
            border-radius:999px;
            font-size:12px;
            font-weight:600;
            margin-right:6px;
            margin-bottom:6px;
            white-space:nowrap;
        ">
            {label}
        </span>
        """,
        unsafe_allow_html=True,
    )


def render_meta_side(item):
    category = item.get("category", "Autres")
    level = item.get("level", "Intermédiaire")

    category_color = CATEGORY_COLORS.get(category, "#616161")
    level_color = LEVEL_COLORS.get(level, "#616161")

    st.markdown("##### Informations")
    render_badge(category, category_color)
    render_badge(level, level_color)


def render_bullets(items):
    if not items:
        st.write("Non renseigné.")
        return

    for item in items:
        st.markdown(f"- {item}")


def render_questions(items):
    if not items:
        st.write("Non renseigné.")
        return

    for question_answer in items:
        if isinstance(question_answer, tuple) and len(question_answer) == 2:
            question, answer = question_answer
            st.markdown(f"**{question}**")
            st.write(answer)
        else:
            st.markdown(f"- {question_answer}")


def render_section(item, key, label):
    value = item.get(key)

    if value in [None, "", []]:
        return

    st.markdown(f"#### {label}")

    if key == "schema":
        st.code(value, language="text")

    elif key in ["why", "when", "advantages", "disadvantages", "errors"]:
        render_bullets(value)

    elif key == "questions":
        render_questions(value)

    elif key == "eloy":
        st.info(value)

    else:
        st.write(value)


def render_definition_full(item):
    for key, label in SECTION_ORDER:
        render_section(item, key, label)


def render_definition_short(item):
    st.markdown("#### Définition simple")
    st.write(item.get("definition", "Non renseigné."))

    st.markdown("#### Exemple concret chez Eloy")
    st.info(item.get("eloy", "Non renseigné."))

    errors = item.get("errors", [])

    if errors:
        st.markdown("#### Erreurs classiques à éviter")
        render_bullets(errors[:4])


def render_related_links(current_title, all_items, context):
    related_titles = RELATED_RULES.get(current_title, [])

    if not related_titles:
        return

    available_titles = {x.get("title", "") for x in all_items}
    related_titles = [x for x in related_titles if x in available_titles]

    if not related_titles:
        return

    st.markdown("#### Voir aussi")

    key = f"related_select_{safe_key(context)}_{safe_key(current_title)}"

    selected = st.selectbox(
        "Concept lié",
        ["-- Sélectionner --"] + related_titles,
        key=key,
    )

    if selected != "-- Sélectionner --":
        st.session_state["selected_definition"] = selected
        rerun_app()


def render_card(item, all_items, compact=False, force_open=False, context="default"):
    title = item.get("title", "Sans titre")

    with st.expander(title, expanded=force_open):
        left, right = st.columns([4, 1.4])

        with left:
            st.markdown(f"### {title}")

        with right:
            render_meta_side(item)

        st.markdown("---")

        if compact:
            render_definition_short(item)
        else:
            render_definition_full(item)

        render_related_links(title, all_items, context=context)


def render_direct_access(items):
    titles = [x.get("title", "") for x in items]

    if not titles:
        return None

    current = st.session_state.get("selected_definition")

    if current not in titles:
        current = titles[0]

    selected = st.selectbox(
        "Aller directement à une définition",
        titles,
        index=titles.index(current),
        key="definition_selector",
    )

    st.session_state["selected_definition"] = selected

    return selected


def render_filters(items):
    categories = sorted({x["category"] for x in items})
    levels = ["Débutant", "Intermédiaire", "Avancé"]
    letters = ["Toutes"] + sorted({x["letter"] for x in items if x["letter"]})

    with st.expander("Recherche et filtres", expanded=True):
        query = st.text_input(
            "Recherche",
            placeholder="Exemples : RLS, Direct Lake, table de faits, incremental refresh, Bronze...",
            key="definition_query",
        )

        selected_categories = st.multiselect(
            "Catégories",
            categories,
            default=categories,
            key="definition_categories",
        )

        selected_levels = st.multiselect(
            "Niveaux",
            levels,
            default=levels,
            key="definition_levels",
        )

        selected_letter = st.selectbox(
            "Accès rapide par lettre",
            letters,
            key="definition_letter",
        )

        compact = st.checkbox(
            "Vue courte",
            value=True,
            key="definition_compact_view",
        )

    return query, selected_categories, selected_levels, selected_letter, compact


def filter_items(items, query, categories, levels, letter):
    results = []

    for item in items:
        if item["category"] not in categories:
            continue

        if item["level"] not in levels:
            continue

        if letter != "Toutes" and item["letter"] != letter:
            continue

        if not match_query(item, query):
            continue

        results.append(item)

    return results


def render_results_tab(results, all_items, compact):
    if not results:
        st.warning(
            "Aucune définition trouvée. Essaie un autre mot-clé comme : RLS, Fabric, modèle, sécurité, pipeline, fait, dimension."
        )
        return

    for item in results:
        render_card(
            item,
            all_items,
            compact=compact,
            context=f"results_{item.get('title', '')}",
        )


def render_category_tab(results, all_items, compact):
    if not results:
        st.warning("Aucune définition à afficher.")
        return

    categories = sorted({x["category"] for x in results})

    for category in categories:
        category_items = [x for x in results if x["category"] == category]

        st.subheader(category)

        for item in category_items:
            render_card(
                item,
                all_items,
                compact=compact,
                context=f"category_{category}_{item.get('title', '')}",
            )


def render_index_tab(results):
    if not results:
        st.warning("Aucun résultat dans l’index.")
        return

    for item in results:
        title = item.get("title", "")

        if st.button(
            title,
            key=f"index_{safe_key(title)}",
            use_container_width=True,
        ):
            st.session_state["selected_definition"] = title
            rerun_app()


def render_focus_tab(items, compact):
    selected = render_direct_access(items)

    if not selected:
        st.warning("Aucune définition disponible.")
        return

    selected_item = None

    for item in items:
        if item.get("title", "") == selected:
            selected_item = item
            break

    if selected_item is None:
        st.warning("Définition introuvable.")
        return

    render_card(
        selected_item,
        items,
        compact=compact,
        force_open=True,
        context=f"focus_{selected_item.get('title', '')}",
    )


def render_summary(results, total):
    st.markdown(
        f"""
        <div style="
            background:#FF0000;
            border:1px solid #e2e8f0;
            border-radius:12px;
            padding:12px 16px;
            margin-bottom:12px;
        ">
            <strong>{len(results)}</strong> définition(s) trouvée(s) sur <strong>{total}</strong>.
        </div>
        """,
        unsafe_allow_html=True,
    )


def main():
    st.title("Définitions Data, BI, Fabric et Power BI")
    st.caption(
        "Glossaire avec recherche, filtres, exemples Eloy, questions/réponses et erreurs classiques à éviter."
    )

    if not DEFINITIONS:
        st.error(
            "Le fichier data/definitions_data.py n’a pas été trouvé ou ne contient pas la variable DEFINITIONS."
        )
        st.stop()

    items = enrich_definitions()

    query, categories, levels, letter, compact = render_filters(items)

    results = filter_items(
        items=items,
        query=query,
        categories=categories,
        levels=levels,
        letter=letter,
    )

    st.markdown("---")

    render_summary(results, len(items))
    render_mobile_tips()

    tab_focus, tab_results, tab_categories, tab_index = st.tabs(
        [
            "Accès direct",
            "Résultats",
            "Par catégorie",
            "Index",
        ]
    )

    with tab_focus:
        render_focus_tab(items, compact)

    with tab_results:
        render_results_tab(results, items, compact)

    with tab_categories:
        render_category_tab(results, items, compact)

    with tab_index:
        render_index_tab(results)


if __name__ == "__main__":
    main()
