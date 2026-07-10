def calculate_maturity(score):
    """
    Retourne le niveau de maturité Data
    en fonction du score calculé.
    """

    if score < 25:
        return "Niveau 1"

    if score < 50:
        return "Niveau 2"

    if score < 75:
        return "Niveau 3"

    if score < 90:
        return "Niveau 4"

    return "Niveau 5"


def get_maturity_details(score):
    """
    Retourne les détails complets
    du niveau de maturité.
    """

    level = calculate_maturity(score)

    if level == "Niveau 1":

        return {
            "level": level,
            "title": "Rapport autonome",
            "description": (
                "Le besoin peut être couvert par un rapport "
                "Power BI relativement simple."
            ),
            "characteristics": [
                "Peu de sources",
                "Faible volume",
                "Peu de réutilisation",
                "Architecture légère"
            ],
            "recommendation": (
                "Power BI simple avec Power Query."
            )
        }

    if level == "Niveau 2":

        return {
            "level": level,
            "title": "Power BI maîtrisé",
            "description": (
                "Le besoin nécessite déjà de bonnes pratiques "
                "de modélisation et de performance."
            ),
            "characteristics": [
                "Modèle en étoile",
                "Power Query structuré",
                "Mesures DAX propres",
                "Réduction des colonnes inutiles"
            ],
            "recommendation": (
                "Power BI optimisé."
            )
        }

    if level == "Niveau 3":

        return {
            "level": level,
            "title": "Semantic Model partagé",
            "description": (
                "Plusieurs utilisateurs ou rapports "
                "partagent les mêmes données."
            ),
            "characteristics": [
                "Indicateurs partagés",
                "Mesures centralisées",
                "Réutilisation importante",
                "Documentation nécessaire"
            ],
            "recommendation": (
                "Semantic Model partagé."
            )
        }

    if level == "Niveau 4":

        return {
            "level": level,
            "title": "Data Warehouse",
            "description": (
                "Le volume, les sources ou l'historisation "
                "justifient une architecture plus robuste."
            ),
            "characteristics": [
                "Plusieurs sources",
                "Historisation",
                "Qualité de données contrôlée",
                "Architecture commune"
            ],
            "recommendation": (
                "Data Warehouse + Semantic Model."
            )
        }

    return {
        "level": "Niveau 5",
        "title": "Lakehouse entreprise",
        "description": (
            "Architecture Data moderne pour gros volumes, "
            "temps réel ou IA."
        ),
        "characteristics": [
            "Lakehouse",
            "Fabric",
            "Très gros volumes",
            "Temps réel",
            "IA / Data Science"
        ],
        "recommendation": (
            "Lakehouse / Fabric + Semantic Model."
        )
    }


def get_maturity_color(score):
    """
    Couleur d'affichage selon la maturité.
    """

    if score < 25:
        return "red"

    if score < 50:
        return "orange"

    if score < 75:
        return "yellow"

    if score < 90:
        return "green"

    return "blue"


def get_maturity_label(score):
    """
    Libellé utilisateur.
    """

    if score < 25:
        return (
            "Organisation Data débutante"
        )

    if score < 50:
        return (
            "Organisation Data en progression"
        )

    if score < 75:
        return (
            "Organisation Data structurée"
        )

    if score < 90:
        return (
            "Organisation Data avancée"
        )

    return (
        "Organisation Data industrielle"
    )


def build_maturity_summary(score):
    """
    Résumé complet prêt à afficher
    dans Streamlit.
    """

    details = get_maturity_details(score)

    return {
        "score": score,
        "level": details["level"],
        "title": details["title"],
        "description": details["description"],
        "characteristics": details["characteristics"],
        "recommendation": details["recommendation"],
        "label": get_maturity_label(score),
        "color": get_maturity_color(score)
    }
