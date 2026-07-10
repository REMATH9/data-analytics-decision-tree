# pages/definitions.py
# -*- coding: utf-8 -*-

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
        "data warehouse", "data mart", "lakehouse", "bronze", "silver", "gold",
        "fabric", "databricks", "data vault", "warehouse"
    ],
    "Modélisation BI": [
        "star", "snowflake", "flat", "dimension", "fait", "faits",
        "transactionnelle", "snapshot", "pont", "many", "relation", "schema"
    ],
    "Sécurité": [
        "rls", "ols", "sécurité", "security", "gateway"
    ],
    "Pipelines et ingestion": [
        "pipeline", "etl", "elt", "factory", "ssis", "staging", "cdc",
        "streaming", "rejet", "zone de rejet", "dataflows"
    ],
    "Power BI et modèles sémantiques": [
        "semantic", "dataset", "datasets", "cube", "analysis services",
        "direct lake", "composite", "agrégation", "cardinalité", "tabulaire"
    ],
    "Gouvernance": [
        "gouvernance", "steward", "self-service", "dictionnaire", "culture data"
    ],
}


LEVEL_RULES = {
    "Débutant": [
        "flat table", "data mart", "dimension", "table de faits",
        "pipeline simple", "datasets", "gateway"
    ],
    "Intermédiaire": [
        "data warehouse", "star schema", "snowflake", "rls", "ols",
        "incremental refresh", "dataflows", "semantic model", "table d’agrégation",
        "table d'agrégation", "réduire la cardinalité", "scd type 1"
    ],
    "Avancé": [
        "lakehouse", "direct lake", "composite model", "data vault",
        "cdc", "event streaming", "scd type 2", "fabric", "databricks",
        "azure analysis services"
    ],
}


RELATED_RULES = {
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


def render_related_links(current_title, all_items):
    related_titles = RELATED_RULES.get(current_title, [])

    if not related_titles:
        return

    available_titles = {x.get("title", "") for x in all_items}
    related_titles = [x for x in related_titles if x in available_titles]

    if not related_titles:
        return

    st.markdown("#### Voir aussi")

    cols = st.columns(1)

    for related_title in related_titles:
        if st.button(related_title, key=f"related_{current_title}_{related_title}", use_container_width=True):
            st.session_state["selected_definition"] = related_title
            st.rerun()


def render_card(item, all_items, compact=False, force_open=False):
    title = item.get("title", "Sans titre")
    category = item.get("category", "Autres")
    level = item.get("level", "Intermédiaire")

    label = f"{title} | {category} | {level}"

    with st.expander(label, expanded=force_open):
        if compact:
            render_definition_short(item)
        else:
            render_definition_full(item)

        render_related_links(title, all_items)


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
        render_card(item, all_items, compact=compact)


def render_category_tab(results, all_items, compact):
    if not results:
        st.warning("Aucune définition à afficher.")
        return

    categories = sorted({x["category"] for x in results})

    for category in categories:
        category_items = [x for x in results if x["category"] == category]

        st.subheader(category)

        for item in category_items:
            render_card(item, all_items, compact=compact)


def render_index_tab(results):
    if not results:
        st.warning("Aucun résultat dans l’index.")
        return

    for item in results:
        title = item.get("title", "")
        category = item.get("category", "Autres")
        level = item.get("level", "Intermédiaire")

        if st.button(
            f"{title} | {category} | {level}",
            key=f"index_{title}",
            use_container_width=True,
        ):
            st.session_state["selected_definition"] = title
            st.rerun()


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
    )


def render_mobile_tips():
    with st.expander("Conseils d’utilisation mobile", expanded=False):
        st.markdown(
            """
- Utilise la recherche pour aller directement au concept voulu.
- Active la vue courte pour éviter de trop scroller.
- Utilise l’onglet `Accès direct` pour ouvrir une seule définition à la fois.
- Utilise les boutons `Voir aussi` pour passer d’un concept lié à l’autre.
- Les schémas restent en bloc texte afin de rester lisibles sur smartphone.
"""
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
    st.write(f"**{len(results)} définition(s) trouvée(s)** sur {len(items)}.")

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
