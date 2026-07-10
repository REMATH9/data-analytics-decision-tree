import streamlit as st

from utils.recommender import recommend
from utils.maturity import calculate_maturity


st.title("Diagnostic interactif")

st.markdown("""
Répondez aux questions ci-dessous afin d'obtenir :

- une architecture recommandée
- une modélisation recommandée
- un niveau d’industrialisation
- une explication détaillée
- les points de vigilance
- un plan d’action
""")


with st.form("diagnostic_form"):

    col1, col2 = st.columns(2)

    with col1:

        business_need = st.selectbox(
            "Quel est le besoin principal ?",
            [
                "Reporting simple",
                "Dashboard de pilotage",
                "Analyse détaillée",
                "Self-Service BI",
                "Industrialisation Data",
                "Temps réel",
                "IA / Data Science"
            ]
        )

        sources_count = st.selectbox(
            "Combien de sources de données ?",
            [
                "1 source",
                "2 à 5 sources",
                "Plus de 5 sources"
            ]
        )

        source_types = st.multiselect(
            "Types de sources",
            [
                "Excel",
                "ERP",
                "CRM",
                "SQL",
                "SharePoint",
                "API",
                "IoT",
                "Data Lake"
            ],
            default=["Excel"]
        )

        volume = st.selectbox(
            "Volume estimé",
            [
                "Moins de 500k lignes",
                "500k à 5M lignes",
                "5M à 50M lignes",
                "50M à 500M lignes",
                "Plus de 500M lignes"
            ]
        )

        frequency = st.selectbox(
            "Fréquence d'actualisation",
            [
                "Mensuelle",
                "Hebdomadaire",
                "Quotidienne",
                "Horaire",
                "Temps réel"
            ]
        )

    with col2:

        history = st.checkbox(
            "Historisation nécessaire",
            value=False
        )

        multi_reports = st.checkbox(
            "Plusieurs rapports utilisent les mêmes données",
            value=False
        )

        self_service = st.checkbox(
            "Self-Service BI attendu",
            value=False
        )

        sensitive_data = st.checkbox(
            "Données sensibles",
            value=False
        )

        realtime = st.checkbox(
            "Besoin de temps réel",
            value=False
        )

        quality = st.selectbox(
            "Qualité actuelle des données",
            [
                "Bonne",
                "Moyenne",
                "Mauvaise",
                "Inconnue"
            ]
        )

        transformations = st.selectbox(
            "Complexité des transformations",
            [
                "Faibles",
                "Moyennes",
                "Complexes",
                "Très complexes"
            ]
        )

        business_definitions = st.checkbox(
            "KPIs déjà définis et validés",
            value=False
        )

    submit = st.form_submit_button(
        "Générer la recommandation"
    )


if submit:

    answers = {
        "business_need": business_need,
        "sources_count": sources_count,
        "source_types": source_types,
        "volume": volume,
        "frequency": frequency,
        "history": history,
        "multi_reports": multi_reports,
        "self_service": self_service,
        "sensitive_data": sensitive_data,
        "realtime": realtime,
        "quality": quality,
        "transformations": transformations,
        "business_definitions": business_definitions
    }

    result = recommend(answers)

    maturity = calculate_maturity(
        result["score"]
    )

    st.divider()

    st.header("Résultat de l'analyse")

    st.success(
        f"""
Architecture recommandée :
{result['architecture']}
"""
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Architecture",
            result["architecture"]
        )

    with col2:

        st.metric(
            "Modélisation",
            result["modelisation"]
        )

    with col3:

        st.metric(
            "Niveau maturité",
            maturity
        )

    st.divider()

    st.subheader("Résumé exécutif")

    st.info(
        result["executive_summary"]
    )

    st.subheader("Pourquoi cette recommandation ?")

    for item in result["why"]:
        st.write(f"✅ {item}")

    st.subheader(
        "Niveau d'industrialisation recommandé"
    )

    st.info(
        result["industrialisation"]
    )

    st.subheader(
        "Pourquoi certaines solutions ne sont pas retenues ?"
    )

    for alternative in result["alternatives"]:

        with st.expander(
            alternative["solution"]
        ):

            st.write(
                alternative["why_not"]
            )

            st.write(
                f"Alternative retenue : "
                f"{alternative['chosen']}"
            )

    st.subheader(
        "Points de vigilance"
    )

    if result["risks"]:

        for risk in result["risks"]:
            st.warning(risk)

    else:

        st.success(
            "Aucun point bloquant majeur identifié."
        )

    st.subheader(
        "Plan d'action recommandé"
    )

    for i, step in enumerate(
        result["next_steps"],
        start=1
    ):
        st.write(f"{i}. {step}")
