import json
from pathlib import Path


DATA_DIR = Path("data")
CONCEPTS_FILE = DATA_DIR / "concepts.json"


def load_concepts():
    """
    Charge tous les concepts depuis data/concepts.json
    """

    if not CONCEPTS_FILE.exists():
        return {}

    with open(
        CONCEPTS_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


def get_concept(name):
    """
    Retourne un concept spécifique
    """

    concepts = load_concepts()

    return concepts.get(name)


def concept_exists(name):
    """
    Vérifie qu'un concept existe
    """

    concepts = load_concepts()

    return name in concepts


def get_definition(name):
    """
    Retourne uniquement la définition
    """

    concept = get_concept(name)

    if not concept:
        return None

    return concept.get("definition")


def get_simple_explanation(name):
    """
    Retourne l'explication simple
    """

    concept = get_concept(name)

    if not concept:
        return None

    return concept.get(
        "explication_simple"
    )


def get_example(name):
    """
    Retourne l'exemple
    """

    concept = get_concept(name)

    if not concept:
        return None

    return concept.get(
        "exemple"
    )


def get_business_example(name):
    """
    Retourne l'exemple métier
    """

    concept = get_concept(name)

    if not concept:
        return None

    return concept.get(
        "exemple_metier"
    )


def get_when_to_use(name):
    """
    Retourne la liste des cas d'utilisation
    """

    concept = get_concept(name)

    if not concept:
        return []

    return concept.get(
        "quand_utiliser",
        []
    )


def get_advantages(name):
    """
    Retourne la liste des avantages
    """

    concept = get_concept(name)

    if not concept:
        return []

    return concept.get(
        "avantages",
        []
    )


def get_limits(name):
    """
    Retourne la liste des limites
    """

    concept = get_concept(name)

    if not concept:
        return []

    return concept.get(
        "limites",
        []
    )


def search_concepts(search_text):
    """
    Recherche simple dans les concepts
    """

    concepts = load_concepts()

    results = []

    search_text = search_text.lower()

    for name, details in concepts.items():

        if search_text in name.lower():

            results.append(name)

            continue

        for value in details.values():

            if isinstance(
                value,
                str
            ):

                if search_text in value.lower():

                    results.append(name)

                    break

    return sorted(
        list(set(results))
    )


def get_all_concepts():
    """
    Retourne la liste des concepts
    """

    concepts = load_concepts()

    return sorted(
        concepts.keys()
    )


def build_concept_card(name):
    """
    Crée un objet standardisé
    pouvant être affiché dans Streamlit
    """

    concept = get_concept(name)

    if not concept:

        return {
            "exists": False,
            "name": name
        }

    return {
        "exists": True,
        "name": name,
        "definition": concept.get(
            "definition",
            ""
        ),
        "explication_simple": concept.get(
            "explication_simple",
            ""
        ),
        "exemple": concept.get(
            "exemple",
            ""
        ),
        "quand_utiliser": concept.get(
            "quand_utiliser",
            []
        ),
        "avantages": concept.get(
            "avantages",
            []
        ),
        "limites": concept.get(
            "limites",
            []
        ),
        "exemple_metier": concept.get(
            "exemple_metier",
            ""
        )
    }


def get_related_concepts(name):
    """
    Retourne les concepts liés
    """

    concept = get_concept(name)

    if not concept:
        return []

    return concept.get(
        "concepts_lies",
        []
    )
