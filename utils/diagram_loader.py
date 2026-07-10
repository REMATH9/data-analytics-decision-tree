from pathlib import Path
import re


DIAGRAMS_DIR = Path("diagrams")


def get_diagram_files():
    """
    Retourne la liste des fichiers markdown
    présents dans le dossier diagrams.
    """

    if not DIAGRAMS_DIR.exists():
        return []

    return sorted(
        DIAGRAMS_DIR.glob("*.md")
    )


def get_diagram_names():
    """
    Retourne uniquement les noms des diagrammes.
    """

    files = get_diagram_files()

    return [
        file.name
        for file in files
    ]


def load_diagram(filepath):
    """
    Charge le contenu complet
    d'un diagramme markdown.
    """

    path = Path(filepath)

    if not path.exists():
        return ""

    return path.read_text(
        encoding="utf-8"
    )


def load_diagram_by_name(filename):
    """
    Charge un diagramme à partir
    de son nom.
    """

    filepath = DIAGRAMS_DIR / filename

    return load_diagram(filepath)


def extract_title(markdown_text):
    """
    Extrait le titre du fichier markdown.
    """

    lines = markdown_text.splitlines()

    if not lines:
        return "Sans titre"

    first_line = lines[0]

    if first_line.startswith("#"):
        return (
            first_line
            .replace("#", "")
            .strip()
        )

    return "Sans titre"


def extract_mermaid(markdown_text):
    """
    Extrait le bloc Mermaid
    du fichier markdown.
    """

    pattern = r"```mermaid\s*(.*?)```"

    match = re.search(
        pattern,
        markdown_text,
        re.DOTALL
    )

    if match:
        return match.group(1).strip()

    return ""


def get_diagram_info(filename):
    """
    Retourne toutes les informations
    d'un diagramme.
    """

    content = load_diagram_by_name(
        filename
    )

    return {
        "filename": filename,
        "title": extract_title(
            content
        ),
        "content": content,
        "mermaid": extract_mermaid(
            content
        )
    }


def get_all_diagrams():
    """
    Retourne tous les diagrammes
    avec leurs informations.
    """

    results = []

    for file in get_diagram_files():

        results.append(
            get_diagram_info(
                file.name
            )
        )

    return results


def search_diagrams(search_text):
    """
    Recherche dans tous les diagrammes.
    """

    search_text = (
        search_text
        .lower()
        .strip()
    )

    results = []

    for diagram in get_all_diagrams():

        if (
            search_text
            in diagram["content"].lower()
        ):
            results.append(
                diagram
            )

    return results


def get_total_diagrams():
    """
    Retourne le nombre total
    de diagrammes.
    """

    return len(
        get_diagram_files()
    )
