import re
from pathlib import Path

import streamlit as st
from streamlit_mermaid_interactive import mermaid


st.set_page_config(
    page_title="Data Analytics Decision Tree",
    page_icon="📊",
    layout="wide"
)


DIAGRAMS_DIR = Path("diagrams")


def extract_mermaid(markdown_text):
    pattern = r"```mermaid\s*(.*?)```"
    match = re.search(pattern, markdown_text, re.DOTALL)

    if match:
        return match.group(1).strip()

    return ""


def clean_mermaid_label(value):
    return (
        str(value)
        .replace('"', "'")
        .replace("\n", " ")
        .strip()
    )


def determine_recommendation(answers):
    recommendations = []
    reasons = []
    risks = []
    next_steps = []

    architecture = ""
    modelisation = ""
    storage_mode = ""
    transformation = ""
    semantic_layer = ""
    security = ""
    refresh = ""

    volume = answers["volume"]
    sources_count = answers["sources_count"]
    source_types = answers["source_types"]
    frequency = answers["frequency"]
    history = answers["history"]
    quality = answers["quality"]
    transformations = answers["transformations"]
    multi_reports = answers["multi_reports"]
    realtime = answers["realtime"]
    sensitive_data = answers["sensitive_data"]
    self_service = answers["self_service"]
    business_definitions = answers["business_definitions"]

    excel_only = source_types == ["Excel"]
    multiple_sources = sources_count != "1 source"
    big_volume = volume in ["50M à 500M lignes", "Plus de 500M lignes"]
    medium_volume = volume in ["5M à 50M lignes"]
    very_big_volume = volume == "Plus de 500M lignes"
    frequent_refresh = frequency in ["Horaire", "Temps réel / quasi temps réel"]

    if excel_only and volume in ["Moins de 500k lignes", "500k à 5M lignes"] and not multi_reports:
        architecture = "Power BI simple"
        modelisation = "Modèle Power BI en étoile léger"
        storage_mode = "Import"
        transformation = "Power Query"
        semantic_layer = "Dataset local"
        refresh = "Refresh manuel ou planifié"
        reasons.append("Le besoin semble limité : Excel, faible volume et peu de réutilisation entre rapports.")
        next_steps.append("Structurer les fichiers Excel et créer un modèle Power BI propre.")
    elif realtime or very_big_volume:
        architecture = "Lakehouse / Fabric"
        modelisation = "Star Schema sur couche Gold"
        storage_mode = "Direct Lake ou modèle composite"
        transformation = "Pipeline ELT"
        semantic_layer = "Semantic Model partagé"
        refresh = "Traitement fréquent ou quasi temps réel"
        reasons.append("Le volume ou la fréquence impose une architecture plus scalable qu’un simple modèle Power BI.")
        next_steps.append("Prévoir une architecture en couches Bronze / Silver / Gold.")
    elif big_volume:
        architecture = "Data Warehouse"
        modelisation = "Star Schema"
        storage_mode = "Import avec Incremental Refresh ou Composite Model"
        transformation = "SQL / ELT"
        semantic_layer = "Semantic Model partagé"
        refresh = "Incremental Refresh"
        reasons.append("Le volume important justifie de préparer les données en amont de Power BI.")
        next_steps.append("Créer des tables de faits, des dimensions et une table calendrier.")
    elif multiple_sources or history or multi_reports:
        architecture = "Data Mart ou Data Warehouse"
        modelisation = "Star Schema"
        storage_mode = "Import optimisé"
        transformation = "SQL + Power Query"
        semantic_layer = "Semantic Model partagé"
        refresh = "Refresh planifié"
        reasons.append("Plusieurs sources, l’historisation ou plusieurs rapports nécessitent une couche de données réutilisable.")
        next_steps.append("Définir les clés communes et les règles de rapprochement entre sources.")
    elif medium_volume:
        architecture = "Power BI optimisé"
        modelisation = "Star Schema"
        storage_mode = "Import avec optimisation"
        transformation = "Power Query ou SQL"
        semantic_layer = "Dataset Power BI"
        refresh = "Refresh planifié"
        reasons.append("Le volume est intermédiaire : Power BI peut suffire, mais le modèle doit être optimisé.")
        next_steps.append("Supprimer les colonnes inutiles, réduire la cardinalité et optimiser les mesures DAX.")
    else:
        architecture = "Power BI standard"
        modelisation = "Star Schema simple"
        storage_mode = "Import"
        transformation = "Power Query"
        semantic_layer = "Dataset local"
        refresh = "Refresh planifié"
        reasons.append("Le contexte ne nécessite pas encore une architecture lourde.")
        next_steps.append("Démarrer avec un modèle propre avant de complexifier l’architecture.")

    if quality in ["Moyenne", "Mauvaise"]:
        risks.append("La qualité des données peut fausser les indicateurs.")
        next_steps.append("Mettre en place un contrôle des doublons, valeurs manquantes, formats et clés métier.")

    if not business_definitions:
        risks.append("Les définitions métier ne sont pas encore stabilisées.")
        next_steps.append("Créer un dictionnaire métier et faire valider les KPIs.")

    if history:
        recommendations.append("Historisation : prévoir SCD Type 2 ou snapshots selon le besoin.")
        next_steps.append("Identifier les champs à historiser : client, article, prix, statut, stock ou KPI.")

    if transformations in ["Complexes", "Très complexes"]:
        recommendations.append("Transformations : éviter de tout faire dans Power Query.")
        next_steps.append("Déporter les transformations lourdes en SQL, Dataflow, Fabric Pipeline ou Data Warehouse.")

    if sensitive_data:
        security = "RLS / OLS"
        recommendations.append("Sécurité : prévoir RLS et éventuellement OLS.")
        next_steps.append("Créer une table de sécurité utilisateur / rôle / périmètre.")
    else:
        security = "Accès workspace standard"

    if self_service:
        recommendations.append("Self-service BI : prévoir un Semantic Model documenté et certifié.")
        next_steps.append("Centraliser les mesures DAX et documenter les tables exposées aux utilisateurs.")

    result = {
        "architecture": architecture,
        "modelisation": modelisation,
        "storage_mode": storage_mode,
        "transformation": transformation,
        "semantic_layer": semantic_layer,
        "security": security,
        "refresh": refresh,
        "recommendations": recommendations,
        "reasons": reasons,
        "risks": risks,
        "next_steps": list(dict.fromkeys(next_steps)),
    }

    return result


def build_dynamic_mermaid(answers, result):
    sources = ", ".join(answers["source_types"])

    labels = {
        "A": "Projet Data / BI",
        "B": f"Besoin : {answers['business_need']}",
        "C": f"Sources : {sources}",
        "D": f"Nombre de sources : {answers['sources_count']}",
        "E": f"Volume : {answers['volume']}",
        "F": f"Fréquence : {answers['frequency']}",
        "G": f"Historisation : {'Oui' if answers['history'] else 'Non'}",
        "H": f"Qualité : {answers['quality']}",
        "I": f"Transformations : {answers['transformations']}",
        "J": f"Architecture : {result['architecture']}",
        "K": f"Modélisation : {result['modelisation']}",
        "L": f"Mode stockage : {result['storage_mode']}",
        "M": f"Couche sémantique : {result['semantic_layer']}",
        "N": f"Sécurité : {result['security']}",
        "O": "Dashboard / Rapport Power BI",
        "P": "Publication et monitoring",
    }

    code = f"""
flowchart TD

A["{clean_mermaid_label(labels['A'])}"]
B["{clean_mermaid_label(labels['B'])}"]
C["{clean_mermaid_label(labels['C'])}"]
D["{clean_mermaid_label(labels['D'])}"]
E["{clean_mermaid_label(labels['E'])}"]
F["{clean_mermaid_label(labels['F'])}"]
G["{clean_mermaid_label(labels['G'])}"]
H["{clean_mermaid_label(labels['H'])}"]
I["{clean_mermaid_label(labels['I'])}"]
J["{clean_mermaid_label(labels['J'])}"]
K["{clean_mermaid_label(labels['K'])}"]
L["{clean_mermaid_label(labels['L'])}"]
M["{clean_mermaid_label(labels['M'])}"]
N["{clean_mermaid_label(labels['N'])}"]
O["{clean_mermaid_label(labels['O'])}"]
P["{clean_mermaid_label(labels['P'])}"]

A --> B
B --> C
C --> D
D --> E
E --> F
F --> G
G --> H
H --> I
I --> J
J --> K
K --> L
L --> M
M --> N
N --> O
O --> P
"""

    return code.strip()


def display_existing_diagrams():
    files = sorted(DIAGRAMS_DIR.glob("*.md"))

    if not files:
        st.warning("Aucun fichier .md trouvé dans le dossier diagrams.")
        return

    selected_file = st.sidebar.selectbox(
        "Choisir un diagramme existant",
        files,
        format_func=lambda p: p.name
    )

    content = selected_file.read_text(encoding="utf-8")
    title = content.splitlines()[0].replace("#", "").strip() if content.splitlines() else selected_file.name
    diagram_code = extract_mermaid(content)

    st.subheader(title)

    if diagram_code:
        result = mermaid(
            diagram_code,
            theme="neutral",
            key=f"diagram_{selected_file.name}"
        )

        if isinstance(result, dict) and result.get("entity_clicked"):
            st.info(f"Noeud sélectionné : {result.get('entity_clicked')}")

        with st.expander("Voir le code Mermaid"):
            st.code(diagram_code, language="mermaid")
    else:
        st.error("Aucun bloc Mermaid trouvé dans ce fichier.")


def display_diagnostic():
    st.subheader("Questionnaire de cadrage Data / BI")
    st.write(
        "Réponds aux questions ci-dessous. L’application proposera ensuite "
        "une architecture cible et affichera le chemin décisionnel."
    )

    with st.form("diagnostic_form"):
        col1, col2 = st.columns(2)

        with col1:
            business_need = st.selectbox(
                "1. Quel est le besoin principal ?",
                [
                    "Reporting simple",
                    "Dashboard de pilotage",
                    "Analyse détaillée",
                    "Self-service BI",
                    "Industrialisation Data",
                    "Temps réel / monitoring opérationnel",
                    "Préparation IA / Data Science",
                ]
            )

            sources_count = st.selectbox(
                "2. Combien de sources de données ?",
                [
                    "1 source",
                    "2 à 5 sources",
                    "Plus de 5 sources",
                ]
            )

            source_types = st.multiselect(
                "3. Quels types de sources ?",
                [
                    "Excel",
                    "ERP",
                    "CRM",
                    "SQL",
                    "SharePoint",
                    "API",
                    "IoT",
                    "Fichiers plats",
                    "Data Lake",
                ],
                default=["Excel"]
            )

            volume = st.selectbox(
                "4. Quel volume de données ?",
                [
                    "Moins de 500k lignes",
                    "500k à 5M lignes",
                    "5M à 50M lignes",
                    "50M à 500M lignes",
                    "Plus de 500M lignes",
                ]
            )

            frequency = st.selectbox(
                "5. Quelle fréquence d’actualisation ?",
                [
                    "Mensuelle",
                    "Hebdomadaire",
                    "Quotidienne",
                    "Horaire",
                    "Temps réel / quasi temps réel",
                ]
            )

            quality = st.selectbox(
                "6. Qualité actuelle des données ?",
                [
                    "Bonne",
                    "Moyenne",
                    "Mauvaise",
                    "Inconnue",
                ]
            )

        with col2:
            history = st.checkbox(
                "7. Faut-il historiser les données ?",
                value=False
            )

            transformations = st.selectbox(
                "8. Complexité des transformations ?",
                [
                    "Faibles",
                    "Moyennes",
                    "Complexes",
                    "Très complexes",
                ]
            )

            multi_reports = st.checkbox(
                "9. Plusieurs rapports utiliseront les mêmes données ?",
                value=False
            )

            realtime = st.checkbox(
                "10. Besoin de temps réel ou quasi temps réel ?",
                value=False
            )

            sensitive_data = st.checkbox(
                "11. Données sensibles ou accès différents selon utilisateur ?",
                value=False
            )

            self_service = st.checkbox(
                "12. Besoin de self-service BI ?",
                value=False
            )

            business_definitions = st.checkbox(
                "13. Les définitions métier / KPIs sont validés ?",
                value=False
            )

        submitted = st.form_submit_button("Générer la recommandation")

    if submitted:
        if not source_types:
            st.error("Sélectionne au moins un type de source.")
            return

        answers = {
            "business_need": business_need,
            "sources_count": sources_count,
            "source_types": source_types,
            "volume": volume,
            "frequency": frequency,
            "quality": quality,
            "history": history,
            "transformations": transformations,
            "multi_reports": multi_reports,
            "realtime": realtime,
            "sensitive_data": sensitive_data,
            "self_service": self_service,
            "business_definitions": business_definitions,
        }

        result = determine_recommendation(answers)

        st.session_state["answers"] = answers
        st.session_state["recommendation"] = result
        st.session_state["dynamic_mermaid"] = build_dynamic_mermaid(answers, result)

    if "recommendation" in st.session_state:
        result = st.session_state["recommendation"]

        st.divider()

        st.subheader("Architecture recommandée")

        col_a, col_b, col_c = st.columns(3)

        with col_a:
            st.metric("Architecture", result["architecture"])
            st.metric("Modélisation", result["modelisation"])

        with col_b:
            st.metric("Mode stockage", result["storage_mode"])
            st.metric("Transformation", result["transformation"])

        with col_c:
            st.metric("Couche sémantique", result["semantic_layer"])
            st.metric("Sécurité", result["security"])

        st.subheader("Pourquoi cette recommandation ?")

        for reason in result["reasons"]:
            st.write(f"- {reason}")

        if result["recommendations"]:
            st.subheader("Recommandations complémentaires")

            for recommendation in result["recommendations"]:
                st.write(f"- {recommendation}")

        if result["risks"]:
            st.subheader("Points de vigilance")

            for risk in result["risks"]:
                st.warning(risk)

        st.subheader("Prochaines actions")

        for step in result["next_steps"]:
            st.write(f"- {step}")

        st.subheader("Chemin décisionnel généré")

        diagram_code = st.session_state["dynamic_mermaid"]

        mermaid(
            diagram_code,
            theme="neutral",
            key="dynamic_decision_path"
        )

        with st.expander("Voir le Mermaid généré"):
            st.code(diagram_code, language="mermaid")


def display_methodology():
    st.subheader("Logique de décision")

    st.markdown(
        """
Cette application repose sur une logique simple :

1. Comprendre le besoin métier.
2. Identifier les sources.
3. Évaluer le volume.
4. Évaluer la fréquence d’actualisation.
5. Vérifier l’historisation.
6. Évaluer la qualité des données.
7. Choisir l’architecture cible.
8. Choisir la modélisation.
9. Choisir le mode de stockage Power BI.
10. Proposer les étapes suivantes.

### Règles principales

- **Excel + faible volume + un seul rapport**  
  → Power BI simple avec Power Query.

- **Plusieurs sources + plusieurs rapports**  
  → Data Mart ou Data Warehouse.

- **Historisation + volume important**  
  → Data Warehouse avec Star Schema.

- **Très gros volume ou temps réel**  
  → Lakehouse / Fabric / Direct Lake.

- **Self-service BI**  
  → Semantic Model partagé et documenté.

- **Données sensibles**  
  → RLS / OLS.
"""
    )


st.title("Data Analytics Decision Tree")
st.caption("Questionnaire, recommandations et diagrammes Mermaid pour choisir une architecture Data / BI.")

tab1, tab2, tab3 = st.tabs(
    [
        "Diagnostic interactif",
        "Diagrammes existants",
        "Méthodologie",
    ]
)

with tab1:
    display_diagnostic()

with tab2:
    display_existing_diagrams()

with tab3:
    display_methodology()
