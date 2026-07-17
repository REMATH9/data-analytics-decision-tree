from data.definitions_data import DEFINITIONS


def load_concepts():
    concepts = {}

    for item in DEFINITIONS:

        title = item.get("title", "")

        concepts[title] = {
            "definition": item.get("definition", ""),

            "explication_simple": item.get(
                "definition",
                ""
            ),

            "exemple": item.get(
                "schema",
                ""
            ),

            "quand_utiliser": item.get(
                "when",
                []
            ),

            "avantages": item.get(
                "advantages",
                []
            ),

            "limites": item.get(
                "disadvantages",
                []
            ),

            "exemple_metier": item.get(
                "eloy",
                ""
            ),

            "concepts_lies": []
        }

    return concepts


def get_concept(name):
    concepts = load_concepts()

    return concepts.get(name)


def concept_exists(name):
    concepts = load_concepts()

    return name in concepts


def get_definition(name):
    concept = get_concept(name)

    if not concept:
        return None

    return concept.get("definition")


def get_simple_explanation(name):
    concept = get_concept(name)

    if not concept:
        return None

    return concept.get(
        "explication_simple"
    )


def get_example(name):
    concept = get_concept(name)

    if not concept:
        return None

    return concept.get(
        "exemple"
    )


def get_business_example(name):
    concept = get_concept(name)

    if not concept:
        return None

    return concept.get(
        "exemple_metier"
    )


def get_when_to_use(name):
    concept = get_concept(name)

    if not concept:
        return []

    return concept.get(
        "quand_utiliser",
        []
    )


def get_advantages(name):
    concept = get_concept(name)

    if not concept:
        return []

    return concept.get(
        "avantages",
        []
    )


def get_limits(name):
    concept = get_concept(name)

    if not concept:
        return []

    return concept.get(
        "limites",
        []
    )


def search_concepts(search_text):

    concepts = load_concepts()

    results = []

    search_text = search_text.lower()

    for name, details in concepts.items():

        if search_text in name.lower():

            results.append(name)

            continue

        for value in details.values():

            if isinstance(value, str):

                if search_text in value.lower():

                    results.append(name)

                    break

    return sorted(
        list(set(results))
    )


def get_all_concepts():

    concepts = load_concepts()

    return sorted(
        concepts.keys()
    )


def build_concept_card(name):

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

    concept = get_concept(name)

    if not concept:

        return []

    return concept.get(
        "concepts_lies",
        []
    )
