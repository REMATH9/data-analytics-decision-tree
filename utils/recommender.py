def recommend(answers):

    score = calculate_score(answers)

    volume = answers["volume"]
    sources_count = answers["sources_count"]
    source_types = answers["source_types"]

    history = answers["history"]
    multi_reports = answers["multi_reports"]
    realtime = answers["realtime"]
    self_service = answers["self_service"]
    sensitive_data = answers["sensitive_data"]

    architecture = "Power BI standard"
    modelisation = "Star Schema"

    why = []
    risks = []
    next_steps = []
    alternatives = []

    excel_only = source_types == ["Excel"]
    multiple_sources = sources_count != "1 source"

    if (
        excel_only
        and volume in [
            "Moins de 500k lignes",
            "500k à 5M lignes"
        ]
        and not history
        and not multi_reports
    ):

        architecture = "Power BI simple"
        modelisation = "Modèle Power BI en étoile léger"

        why.append(
            "Les données sont peu volumineuses et principalement issues d'Excel."
        )

        why.append(
            "Une architecture légère est suffisante dans ce contexte."
        )

        next_steps.extend([
            "Structurer les fichiers sources.",
            "Construire un modèle Power BI simple.",
            "Valider les indicateurs métier."
        ])

    elif realtime or volume == "Plus de 500M lignes":

        architecture = "Lakehouse / Fabric"
        modelisation = "Star Schema sur couche Gold"

        why.append(
            "Le volume très important ou le besoin de temps réel nécessite une architecture scalable."
        )

        why.append(
            "Un Lakehouse permet de gérer les gros volumes et les données brutes."
        )

        next_steps.extend([
            "Définir les couches Bronze, Silver et Gold.",
            "Construire un modèle analytique partagé.",
            "Mettre en place les pipelines d'alimentation."
        ])

    elif volume in [
        "50M à 500M lignes",
        "Plus de 500M lignes"
    ]:

        architecture = "Data Warehouse"
        modelisation = "Star Schema"

        why.append(
            "Le volume nécessite une préparation des données avant Power BI."
        )

        why.append(
            "Un Data Warehouse améliore les performances et la gouvernance."
        )

        next_steps.extend([
            "Identifier les tables de faits.",
            "Créer les dimensions.",
            "Mettre en place une table calendrier."
        ])

    elif multiple_sources or history or multi_reports:

        architecture = "Data Mart ou Data Warehouse"
        modelisation = "Star Schema"

        why.append(
            "Plusieurs sources ou plusieurs rapports nécessitent une couche centrale."
        )

        why.append(
            "Un modèle partagé permet d'éviter des définitions contradictoires."
        )

        next_steps.extend([
            "Définir les clés communes.",
            "Construire un modèle en étoile.",
            "Centraliser les indicateurs."
        ])

    else:

        why.append(
            "Le contexte reste compatible avec une approche Power BI classique."
        )

        next_steps.extend([
            "Formaliser les besoins métier.",
            "Créer le modèle de données.",
            "Construire les premiers rapports."
        ])

    if sensitive_data:

        risks.append(
            "Les droits d'accès doivent être définis avant publication."
        )

        next_steps.append(
            "Mettre en place une sécurité RLS."
        )

    if answers["quality"] in [
        "Moyenne",
        "Mauvaise",
        "Inconnue"
    ]:

        risks.append(
            "La qualité des données peut impacter la fiabilité des indicateurs."
        )

        next_steps.append(
            "Mettre en place des contrôles qualité."
        )

    if not answers["business_definitions"]:

        risks.append(
            "Les définitions métier des KPIs ne sont pas encore validées."
        )

        next_steps.append(
            "Créer un dictionnaire métier."
        )

    if self_service:

        next_steps.append(
            "Prévoir un Semantic Model partagé."
        )

    executive_summary = (
        f"Architecture recommandée : {architecture}. "
        f"Modélisation recommandée : {modelisation}. "
        f"Volume analysé : {volume}. "
        f"Sources : {', '.join(source_types)}."
    )

    industrialisation = build_industrialisation(score)

    alternatives.append({
        "solution": "Cube OLAP",
        "why_not": (
            "Plus complexe à mettre en œuvre qu'un Semantic Model moderne."
        ),
        "chosen": architecture
    })

    alternatives.append({
        "solution": "Snowflake Schema",
        "why_not": (
            "Plus complexe que le Star Schema pour la majorité des projets Power BI."
        ),
        "chosen": modelisation
    })

    alternatives.append({
        "solution": "DirectQuery",
        "why_not": (
            "Le mode Import offre généralement de meilleures performances."
        ),
        "chosen": architecture
    })

    return {
        "score": score,
        "architecture": architecture,
        "modelisation": modelisation,
        "executive_summary": executive_summary,
        "why": why,
        "industrialisation": industrialisation,
        "alternatives": alternatives,
        "risks": list(dict.fromkeys(risks)),
        "next_steps": list(dict.fromkeys(next_steps))
    }


def calculate_score(answers):

    score = 0

    if answers["sources_count"] == "2 à 5 sources":
        score += 15

    elif answers["sources_count"] == "Plus de 5 sources":
        score += 25

    volume = answers["volume"]

    if volume == "500k à 5M lignes":
        score += 10

    elif volume == "5M à 50M lignes":
        score += 20

    elif volume == "50M à 500M lignes":
        score += 40

    elif volume == "Plus de 500M lignes":
        score += 50

    if answers["history"]:
        score += 15

    if answers["multi_reports"]:
        score += 15

    if answers["self_service"]:
        score += 10

    if answers["sensitive_data"]:
        score += 10

    if answers["realtime"]:
        score += 20

    return min(score, 100)


def build_industrialisation(score):

    if score < 25:
        return (
            "Niveau 1 - Rapport autonome"
        )

    if score < 50:
        return (
            "Niveau 2 - Power BI maîtrisé"
        )

    if score < 75:
        return (
            "Niveau 3 - Semantic Model partagé"
        )

    if score < 90:
        return (
            "Niveau 4 - Data Warehouse"
        )

    return (
        "Niveau 5 - Lakehouse / Fabric entreprise"
    )
