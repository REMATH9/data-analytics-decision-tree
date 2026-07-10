import re
from pathlib import Path

import streamlit as st
from streamlit_mermaid_interactive import mermaid


st.set_page_config(
    page_title="Data Analytics Decision Tree",
    layout="wide"
)


DIAGRAMS_DIR = Path("diagrams")


CONCEPT_DETAILS = {
    "Power BI simple": {
        "titre": "Power BI simple",
        "definition": "Une solution Power BI simple consiste à connecter directement une ou quelques sources de données à Power BI, puis à construire un rapport avec Power Query et un modèle de données léger.",
        "explication": "C’est adapté quand le besoin est limité, que les données sont peu volumineuses et que peu de rapports doivent être créés.",
        "exemple": """
Fichier Excel
    ↓
Power Query
    ↓
Power BI
    ↓
Dashboard
""",
        "quand_utiliser": [
            "Un seul rapport ou peu de rapports",
            "Peu de sources de données",
            "Volume faible ou moyen",
            "Besoin rapide de reporting"
        ],
        "avantages": [
            "Rapide à mettre en place",
            "Facile à comprendre",
            "Peu coûteux",
            "Idéal pour démarrer un projet"
        ],
        "limites": [
            "Moins adapté si les données grossissent fortement",
            "Risque de duplication des calculs entre rapports",
            "Peut devenir difficile à maintenir avec plusieurs utilisateurs"
        ],
        "exemple_metier": "Un fichier Excel de suivi de production alimenté chaque semaine et analysé dans un seul dashboard Power BI."
    },

    "Power BI standard": {
        "titre": "Power BI standard",
        "definition": "Une architecture Power BI standard utilise Power BI comme outil principal pour importer, transformer, modéliser et visualiser les données.",
        "explication": "C’est un bon choix lorsque les données restent maîtrisables et que le besoin ne nécessite pas encore une architecture Data complète.",
        "exemple": """
Excel / SQL / SharePoint
        ↓
Power Query
        ↓
Modèle Power BI
        ↓
Rapport Power BI
""",
        "quand_utiliser": [
            "Reporting classique",
            "Données pas trop volumineuses",
            "Besoin métier bien cadré",
            "Peu de contraintes d’historisation"
        ],
        "avantages": [
            "Simple à déployer",
            "Accessible aux Data Analysts",
            "Convient à beaucoup de projets BI",
            "Permet de construire rapidement de la valeur"
        ],
        "limites": [
            "Peut devenir fragile si trop de logique est mise dans Power Query",
            "Moins adapté aux très gros volumes",
            "Nécessite de bonnes pratiques de modélisation"
        ],
        "exemple_metier": "Un rapport commercial mensuel basé sur une extraction ERP et quelques fichiers de référence."
    },

    "Power BI optimisé": {
        "titre": "Power BI optimisé",
        "definition": "Power BI optimisé signifie que le modèle reste dans Power BI, mais qu’il est construit avec des règles strictes de performance.",
        "explication": "On garde Power BI comme outil central, mais on fait attention au volume, aux colonnes inutiles, aux relations, aux mesures DAX et à la structure du modèle.",
        "exemple": """
Sources
  ↓
Power Query optimisé
  ↓
Modèle en étoile
  ↓
Mesures DAX optimisées
  ↓
Rapport performant
""",
        "quand_utiliser": [
            "Volume intermédiaire",
            "Besoin de bonnes performances",
            "Pas encore besoin de Data Warehouse",
            "Modèle utilisé par quelques rapports"
        ],
        "avantages": [
            "Bonne performance si bien construit",
            "Moins complexe qu’un Data Warehouse",
            "Convient à beaucoup de projets Power BI",
            "Permet de repousser le besoin d’une architecture plus lourde"
        ],
        "limites": [
            "Demande une bonne maîtrise Power BI",
            "Peut atteindre ses limites si les volumes augmentent",
            "Les transformations lourdes peuvent ralentir les refresh"
        ],
        "exemple_metier": "Un dashboard de production avec plusieurs millions de lignes mais une structure de données propre."
    },

    "Data Mart ou Data Warehouse": {
        "titre": "Data Mart ou Data Warehouse",
        "definition": "Un Data Mart ou un Data Warehouse est une couche centrale où les données venant de plusieurs sources sont nettoyées, organisées et préparées avant d’être utilisées dans Power BI.",
        "explication": "Imagine une bibliothèque commune. Au lieu que chaque service travaille avec ses propres fichiers, tout le monde vient chercher les données dans un espace commun, structuré et fiable.",
        "exemple": """
ERP
CRM
Excel
SharePoint
    ↓
Data Warehouse
    ↓
Power BI
    ↓
Rapports partagés
""",
        "quand_utiliser": [
            "Plusieurs sources de données",
            "Plusieurs rapports utilisent les mêmes données",
            "Besoin d’historisation",
            "Besoin de cohérence entre les chiffres",
            "Besoin de maintenance plus robuste"
        ],
        "avantages": [
            "Une seule source de vérité",
            "Données réutilisables dans plusieurs rapports",
            "Meilleure qualité et cohérence des indicateurs",
            "Maintenance plus simple à long terme",
            "Meilleure base pour la gouvernance Data"
        ],
        "limites": [
            "Plus complexe à mettre en place qu’un rapport Power BI simple",
            "Nécessite des règles métier claires",
            "Demande une organisation minimale autour de la donnée"
        ],
        "exemple_metier": "ERP pour les commandes, CRM pour les clients, Excel pour les objectifs commerciaux : toutes les données sont réunies dans une couche commune avant d’être affichées dans Power BI."
    },

    "Data Warehouse": {
        "titre": "Data Warehouse",
        "definition": "Un Data Warehouse est un entrepôt de données structuré. Il centralise les données importantes de l’entreprise pour le reporting, l’analyse et le pilotage.",
        "explication": "C’est comme un magasin central de données. Les données arrivent depuis les systèmes sources, sont nettoyées, organisées, puis mises à disposition des rapports.",
        "exemple": """
ERP
CRM
Base SQL
Fichiers Excel
    ↓
Data Warehouse
    ↓
Modèle Power BI
    ↓
Dashboards
""",
        "quand_utiliser": [
            "Données volumineuses",
            "Plusieurs sources",
            "Besoin d’historique",
            "Plusieurs équipes utilisent les mêmes données",
            "Besoin de fiabilité et de cohérence"
        ],
        "avantages": [
            "Très adapté au reporting d’entreprise",
            "Permet de fiabiliser les indicateurs",
            "Facilite l’historisation",
            "Réduit les traitements lourds dans Power BI",
            "Bonne base pour un modèle en étoile"
        ],
        "limites": [
            "Demande plus de conception au départ",
            "Nécessite des compétences SQL ou Data",
            "Peut être surdimensionné pour un petit besoin ponctuel"
        ],
        "exemple_metier": "Un Data Warehouse qui consolide les ventes, les stocks, les clients et les articles pour alimenter plusieurs dashboards Power BI."
    },

    "Lakehouse / Fabric": {
        "titre": "Lakehouse / Fabric",
        "definition": "Un Lakehouse combine la souplesse d’un Data Lake avec l’organisation d’un Data Warehouse. Microsoft Fabric permet de construire ce type d’architecture dans l’écosystème Microsoft.",
        "explication": "C’est utile quand l’entreprise doit conserver beaucoup de données, parfois brutes, venant de nombreuses sources, avec des besoins évolutifs.",
        "exemple": """
Fichiers bruts
API
IoT
ERP
    ↓
Lakehouse
    ↓
Tables préparées
    ↓
Semantic Model
    ↓
Power BI
""",
        "quand_utiliser": [
            "Très gros volumes",
            "Données variées ou semi-structurées",
            "Besoin de conserver les données brutes",
            "Temps réel ou quasi temps réel",
            "Préparation à l’IA ou à la Data Science"
        ],
        "avantages": [
            "Très scalable",
            "Permet de conserver les données brutes",
            "Adapté aux gros volumes",
            "Bonne base pour BI, IA et analyse avancée"
        ],
        "limites": [
            "Plus complexe à expliquer aux utilisateurs métier",
            "Nécessite une gouvernance solide",
            "Peut être trop lourd pour un simple reporting"
        ],
        "exemple_metier": "Données de production, historiques machines, fichiers ERP et données IoT conservées dans une architecture commune pour analyses avancées."
    },

    "Star Schema": {
        "titre": "Star Schema",
        "definition": "Le Star Schema, ou modèle en étoile, est une façon d’organiser les tables pour faciliter l’analyse dans Power BI.",
        "explication": "On place une table principale au centre, par exemple les ventes ou la production. Autour, on place les axes d’analyse : date, client, produit, site, fournisseur.",
        "exemple": """
              Dim_Date
                 |
Dim_Client -- Fact_Ventes -- Dim_Produit
                 |
              Dim_Site
""",
        "quand_utiliser": [
            "La majorité des projets Power BI",
            "Besoin de bonnes performances",
            "Besoin d’un modèle simple à comprendre",
            "Analyse par date, produit, client, site ou autre dimension"
        ],
        "avantages": [
            "Très recommandé pour Power BI",
            "Simple à comprendre",
            "Performant",
            "Facilite les mesures DAX",
            "Facile à expliquer aux utilisateurs"
        ],
        "limites": [
            "Demande de bien distinguer les faits et les dimensions",
            "Peut nécessiter une préparation des données en amont",
            "Moins normalisé qu’un Snowflake"
        ],
        "exemple_metier": "Une table Fact_Production contient les quantités produites. Les dimensions autour permettent d’analyser par date, ligne de production, article et équipe."
    },

    "Modèle Power BI en étoile léger": {
        "titre": "Modèle Power BI en étoile léger",
        "definition": "C’est une version simplifiée du Star Schema, directement construite dans Power BI.",
        "explication": "On garde une structure propre avec une table centrale et quelques dimensions, sans mettre en place une architecture Data complète.",
        "exemple": """
Fact_Commandes
    ↓
Dim_Date
Dim_Client
Dim_Article
""",
        "quand_utiliser": [
            "Petit ou moyen projet Power BI",
            "Peu de tables",
            "Besoin de performance raisonnable",
            "Besoin d’un modèle facile à maintenir"
        ],
        "avantages": [
            "Simple",
            "Rapide à construire",
            "Bonnes performances",
            "Bonne base pour évoluer ensuite"
        ],
        "limites": [
            "Moins adapté aux gros volumes",
            "Peut devenir limité si les besoins augmentent",
            "Nécessite tout de même une bonne structure"
        ],
        "exemple_metier": "Un rapport de suivi des commandes avec une table de commandes et quelques tables de référence."
    },

    "Star Schema sur couche Gold": {
        "titre": "Star Schema sur couche Gold",
        "definition": "Dans une architecture Lakehouse, la couche Gold est la couche finale, propre et prête pour le reporting. Le Star Schema y organise les données de façon optimale pour Power BI.",
        "explication": "Les données brutes sont d’abord conservées, puis nettoyées, puis transformées en tables faciles à utiliser pour les dashboards.",
        "exemple": """
Bronze : données brutes
Silver : données nettoyées
Gold : modèle en étoile
    ↓
Power BI
""",
        "quand_utiliser": [
            "Architecture Lakehouse",
            "Gros volumes",
            "Besoin de reporting fiable",
            "Besoin de données préparées pour Power BI"
        ],
        "avantages": [
            "Très robuste",
            "Compatible avec les architectures modernes",
            "Sépare bien les étapes de transformation",
            "Facilite le reporting Power BI"
        ],
        "limites": [
            "Plus complexe qu’un modèle Power BI simple",
            "Demande une vraie organisation des couches de données"
        ],
        "exemple_metier": "Des données machines brutes sont d’abord stockées, puis nettoyées, puis transformées en tables de production prêtes pour Power BI."
    },

    "Import": {
        "titre": "Mode Import",
        "definition": "Le mode Import copie les données dans Power BI. Les rapports utilisent ensuite cette copie interne pour afficher les résultats rapidement.",
        "explication": "C’est comme télécharger une photo des données à un moment donné. Le rapport est rapide, mais il faut rafraîchir les données pour voir les nouveautés.",
        "exemple": """
Source de données
    ↓
Import dans Power BI
    ↓
Rapport rapide
""",
        "quand_utiliser": [
            "Besoin de bonnes performances",
            "Données mises à jour périodiquement",
            "Pas de besoin de temps réel",
            "Volume raisonnable"
        ],
        "avantages": [
            "Très performant dans Power BI",
            "Simple à utiliser",
            "Compatible avec beaucoup de fonctionnalités DAX",
            "Recommandé dans de nombreux cas"
        ],
        "limites": [
            "Les données ne sont pas en temps réel",
            "Le refresh peut devenir long si le volume augmente",
            "Nécessite une planification d’actualisation"
        ],
        "exemple_metier": "Un dashboard de ventes actualisé chaque matin à partir de l’ERP."
    },

    "Import optimisé": {
        "titre": "Import optimisé",
        "definition": "L’Import optimisé consiste à utiliser le mode Import de Power BI, mais avec des bonnes pratiques pour limiter le volume et améliorer les performances.",
        "explication": "On importe uniquement ce qui est utile : bonnes colonnes, bonnes lignes, bon modèle, bonnes mesures.",
        "exemple": """
Source
    ↓
Filtrage des colonnes inutiles
    ↓
Modèle en étoile
    ↓
Import Power BI performant
""",
        "quand_utiliser": [
            "Volume moyen",
            "Besoin de performance",
            "Actualisation planifiée",
            "Pas de temps réel strict"
        ],
        "avantages": [
            "Rapide pour les utilisateurs",
            "Moins complexe que DirectQuery",
            "Très adapté à Power BI",
            "Peut suffire pour beaucoup de projets"
        ],
        "limites": [
            "Le refresh doit être surveillé",
            "Pas adapté si les données doivent être instantanées",
            "Peut devenir insuffisant avec de très gros volumes"
        ],
        "exemple_metier": "Un rapport de production avec plusieurs millions de lignes, mais seules les colonnes nécessaires sont importées."
    },

    "Import avec Incremental Refresh ou Composite Model": {
        "titre": "Import avec Incremental Refresh ou Composite Model",
        "definition": "Cette approche permet de gérer des volumes importants avec Power BI en limitant la quantité de données rechargées ou en combinant plusieurs modes de connexion.",
        "explication": "Au lieu de recharger tout l’historique à chaque fois, Power BI peut ne rafraîchir que les périodes récentes. Cela accélère les traitements.",
        "exemple": """
Historique ancien : conservé
Mois récent : rafraîchi
Jour actuel : mis à jour
""",
        "quand_utiliser": [
            "Volumes importants",
            "Historique long",
            "Refresh trop lent",
            "Besoin de compromis entre performance et fraîcheur"
        ],
        "avantages": [
            "Réduit les temps d’actualisation",
            "Permet de gérer plus de données",
            "Améliore la stabilité",
            "Convient bien aux historiques longs"
        ],
        "limites": [
            "Demande une colonne de date fiable",
            "Plus complexe à configurer",
            "Nécessite une bonne structure de modèle"
        ],
        "exemple_metier": "Un historique de ventes de 5 ans où seules les données du mois en cours sont rafraîchies chaque jour."
    },

    "Direct Lake ou modèle composite": {
        "titre": "Direct Lake ou modèle composite",
        "definition": "Direct Lake et les modèles composites permettent d’analyser de gros volumes de données sans tout importer classiquement dans Power BI.",
        "explication": "C’est utile quand les données sont très volumineuses ou doivent rester proches d’une plateforme Data moderne.",
        "exemple": """
Lakehouse
    ↓
Direct Lake
    ↓
Power BI
""",
        "quand_utiliser": [
            "Très gros volumes",
            "Architecture Fabric ou Lakehouse",
            "Besoin de performance sur données volumineuses",
            "Besoin de limiter les imports classiques"
        ],
        "avantages": [
            "Adapté aux très gros volumes",
            "Moins de duplication",
            "Architecture moderne",
            "Peut améliorer la fraîcheur des données"
        ],
        "limites": [
            "Plus technique",
            "Demande une architecture Data solide",
            "Moins adapté aux projets simples"
        ],
        "exemple_metier": "Un suivi opérationnel avec beaucoup de données historiques stockées dans un Lakehouse."
    },

    "Power Query": {
        "titre": "Power Query",
        "definition": "Power Query est l’outil de transformation de données intégré à Power BI et Excel.",
        "explication": "Il permet de nettoyer, filtrer, fusionner et préparer les données avant de les analyser.",
        "exemple": """
Excel brut
    ↓
Suppression colonnes inutiles
    ↓
Correction des types
    ↓
Table propre
""",
        "quand_utiliser": [
            "Nettoyage simple ou moyen",
            "Fichiers Excel ou SharePoint",
            "Préparation de données dans Power BI",
            "Projets de taille raisonnable"
        ],
        "avantages": [
            "Accessible",
            "Visuel",
            "Intégré à Power BI",
            "Très pratique pour transformer des fichiers"
        ],
        "limites": [
            "Peut devenir lent avec de gros volumes",
            "Moins adapté aux transformations très complexes",
            "Risque de logique dispersée dans plusieurs rapports"
        ],
        "exemple_metier": "Nettoyer un fichier Excel de planning avant de l’utiliser dans Power BI."
    },

    "SQL + Power Query": {
        "titre": "SQL + Power Query",
        "definition": "Cette approche combine SQL pour préparer les données en amont et Power Query pour les ajustements finaux dans Power BI.",
        "explication": "SQL sert à faire les traitements lourds et réutilisables. Power Query sert à finaliser la préparation pour le rapport.",
        "exemple": """
Base SQL
    ↓
Vues SQL préparées
    ↓
Power Query
    ↓
Power BI
""",
        "quand_utiliser": [
            "Plusieurs sources",
            "Transformations moyennes à complexes",
            "Besoin de réutiliser les règles",
            "Volume significatif"
        ],
        "avantages": [
            "Plus robuste que tout faire dans Power Query",
            "Meilleure performance",
            "Transformations réutilisables",
            "Bonne transition vers un Data Warehouse"
        ],
        "limites": [
            "Demande des compétences SQL",
            "Nécessite une bonne organisation des vues ou tables",
            "Peut être moins accessible aux utilisateurs non techniques"
        ],
        "exemple_metier": "Préparer les commandes et les clients en SQL, puis finaliser les libellés et filtres dans Power Query."
    },

    "SQL / ELT": {
        "titre": "SQL / ELT",
        "definition": "ELT signifie Extract, Load, Transform. Les données sont d’abord chargées dans une plateforme, puis transformées en SQL ou avec un moteur Data.",
        "explication": "C’est souvent plus adapté aux gros volumes que de transformer toutes les données directement dans Power BI.",
        "exemple": """
Sources
    ↓
Chargement
    ↓
Transformations SQL
    ↓
Tables prêtes pour Power BI
""",
        "quand_utiliser": [
            "Gros volumes",
            "Transformations lourdes",
            "Besoin de réutilisation",
            "Data Warehouse ou Lakehouse"
        ],
        "avantages": [
            "Robuste",
            "Adapté aux volumes importants",
            "Centralise les règles",
            "Allège Power BI"
        ],
        "limites": [
            "Plus technique",
            "Demande une plateforme Data",
            "Nécessite une bonne gouvernance"
        ],
        "exemple_metier": "Calculer les agrégats de production en SQL avant de les afficher dans Power BI."
    },

    "Pipeline ELT": {
        "titre": "Pipeline ELT",
        "definition": "Un pipeline ELT automatise le chargement et la transformation des données.",
        "explication": "Au lieu de faire les étapes manuellement, le pipeline exécute les traitements dans le bon ordre.",
        "exemple": """
Extraire ERP
    ↓
Charger Lakehouse
    ↓
Nettoyer
    ↓
Préparer Power BI
""",
        "quand_utiliser": [
            "Traitements récurrents",
            "Nombreuses sources",
            "Besoin d’automatisation",
            "Architecture Data moderne"
        ],
        "avantages": [
            "Automatisation",
            "Traçabilité",
            "Moins d’erreurs manuelles",
            "Meilleure industrialisation"
        ],
        "limites": [
            "Demande de la conception",
            "Nécessite un suivi des erreurs",
            "Plus long à mettre en place qu’un refresh simple"
        ],
        "exemple_metier": "Chaque nuit, les données ERP sont chargées, contrôlées, transformées puis mises à disposition des dashboards."
    },

    "Dataset local": {
        "titre": "Dataset local",
        "definition": "Le dataset local est le modèle de données intégré directement dans un rapport Power BI.",
        "explication": "Il est pratique pour un rapport isolé, mais moins adapté si plusieurs rapports doivent partager les mêmes données.",
        "exemple": """
Rapport Power BI
    └── Modèle intégré au rapport
""",
        "quand_utiliser": [
            "Un rapport unique",
            "Besoin simple",
            "Peu de réutilisation",
            "Prototype ou petit projet"
        ],
        "avantages": [
            "Simple",
            "Rapide",
            "Facile à gérer au départ"
        ],
        "limites": [
            "Peu réutilisable",
            "Risque de duplication des mesures",
            "Maintenance plus difficile si plusieurs rapports apparaissent"
        ],
        "exemple_metier": "Un rapport ponctuel pour analyser une extraction Excel."
    },

    "Dataset Power BI": {
        "titre": "Dataset Power BI",
        "definition": "Un dataset Power BI contient les tables, relations et mesures utilisées par un rapport.",
        "explication": "C’est le moteur analytique derrière le rapport. Il transforme les données en informations exploitables.",
        "exemple": """
Tables
Relations
Mesures DAX
    ↓
Dataset Power BI
    ↓
Rapport
""",
        "quand_utiliser": [
            "Rapport Power BI classique",
            "Modèle non forcément partagé",
            "Besoin d’analyse interactive"
        ],
        "avantages": [
            "Intégré à Power BI",
            "Flexible",
            "Permet les mesures DAX",
            "Facile à utiliser"
        ],
        "limites": [
            "Peut devenir complexe",
            "Peut être dupliqué entre rapports",
            "Demande une bonne modélisation"
        ],
        "exemple_metier": "Un dataset contenant les tables ventes, clients, produits et dates."
    },

    "Semantic Model partagé": {
        "titre": "Semantic Model partagé",
        "definition": "Un Semantic Model partagé est un modèle Power BI réutilisable par plusieurs rapports.",
        "explication": "Au lieu de recréer les mêmes tables et les mêmes mesures dans chaque rapport, on les centralise dans un seul modèle.",
        "exemple": """
Semantic Model Commercial
    ↓
Rapport Direction
Rapport Ventes
Rapport Finance
""",
        "quand_utiliser": [
            "Plusieurs rapports utilisent les mêmes données",
            "Besoin de cohérence des KPIs",
            "Self-service BI",
            "Organisation souhaitant standardiser les indicateurs"
        ],
        "avantages": [
            "Un seul endroit pour gérer les mesures",
            "KPIs cohérents entre rapports",
            "Maintenance simplifiée",
            "Base solide pour le self-service BI"
        ],
        "limites": [
            "Demande de la gouvernance",
            "Doit être bien documenté",
            "Les changements peuvent impacter plusieurs rapports"
        ],
        "exemple_metier": "Un seul modèle définit le chiffre d’affaires, la marge et les volumes. Tous les dashboards utilisent ces mêmes définitions."
    },

    "Accès workspace standard": {
        "titre": "Accès workspace standard",
        "definition": "L’accès workspace standard signifie que la sécurité est gérée principalement par les droits d’accès au workspace Power BI.",
        "explication": "Les utilisateurs qui ont accès au workspace ou à l’application voient les mêmes données.",
        "exemple": """
Workspace Power BI
    ↓
Utilisateurs autorisés
    ↓
Même vue des données
""",
        "quand_utiliser": [
            "Tous les utilisateurs peuvent voir les mêmes données",
            "Pas de restriction par site, service ou pays",
            "Données peu sensibles",
            "Projet simple"
        ],
        "avantages": [
            "Simple à gérer",
            "Rapide à mettre en place",
            "Moins complexe que la RLS"
        ],
        "limites": [
            "Ne permet pas de filtrer les données selon l’utilisateur",
            "Pas adapté aux données sensibles",
            "Peut être insuffisant pour plusieurs départements"
        ],
        "exemple_metier": "Tous les managers ont accès au même dashboard global de production."
    },

    "RLS / OLS": {
        "titre": "RLS / OLS",
        "definition": "RLS signifie Row-Level Security : filtrage des lignes. OLS signifie Object-Level Security : masquage de certaines tables ou colonnes.",
        "explication": "Ces sécurités permettent d’adapter ce que chaque utilisateur peut voir.",
        "exemple": """
Utilisateur A → voit son site
Utilisateur B → voit son pays
Utilisateur C → voit tout
""",
        "quand_utiliser": [
            "Données sensibles",
            "Droits différents selon les utilisateurs",
            "Filtrage par site, pays, équipe ou département",
            "Rapports partagés à plusieurs profils"
        ],
        "avantages": [
            "Meilleure sécurité",
            "Un seul rapport pour plusieurs profils",
            "Réduction du risque d’accès non autorisé",
            "Adapté aux organisations multi-sites"
        ],
        "limites": [
            "Demande une table de sécurité fiable",
            "Doit être testé soigneusement",
            "Peut complexifier le modèle"
        ],
        "exemple_metier": "Un responsable de site voit uniquement les données de son site, tandis que la direction voit tous les sites."
    }
}


def extract_mermaid(markdown_text):
    pattern = r"```mermaid\s*(.*?)```"
    match = re.search(pattern, markdown_text, re.DOTALL)

    if match:
        return match.group(1).strip()

    return ""


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
    medium_volume = volume == "5M à 50M lignes"
    very_big_volume = volume == "Plus de 500M lignes"

    if excel_only and volume in ["Moins de 500k lignes", "500k à 5M lignes"] and not multi_reports:
        architecture = "Power BI simple"
        modelisation = "Modèle Power BI en étoile léger"
        storage_mode = "Import"
        transformation = "Power Query"
        semantic_layer = "Dataset local"
        refresh = "Refresh manuel ou planifié"

        reasons.append("Les données viennent principalement d’Excel, avec un volume limité et peu de réutilisation entre plusieurs rapports.")
        reasons.append("Une architecture légère permet de répondre rapidement au besoin sans complexifier inutilement la solution.")

        next_steps.append("Nettoyer et structurer les fichiers Excel sources.")
        next_steps.append("Construire un modèle Power BI simple avec une table principale et quelques tables de référence.")
        next_steps.append("Créer des mesures DAX simples et validées par le métier.")

    elif realtime or very_big_volume:
        architecture = "Lakehouse / Fabric"
        modelisation = "Star Schema sur couche Gold"
        storage_mode = "Direct Lake ou modèle composite"
        transformation = "Pipeline ELT"
        semantic_layer = "Semantic Model partagé"
        refresh = "Traitement fréquent ou quasi temps réel"

        reasons.append("Le volume très important ou le besoin de temps réel dépasse le cadre d’un modèle Power BI classique.")
        reasons.append("Une architecture Lakehouse permet de conserver les données brutes, de les transformer progressivement et de les exposer proprement à Power BI.")

        recommendations.append("Prévoir une architecture en couches : Bronze pour les données brutes, Silver pour les données nettoyées, Gold pour les données prêtes à l’analyse.")
        recommendations.append("Mettre en place une couche sémantique partagée pour éviter que chaque rapport recrée ses propres calculs.")

        next_steps.append("Identifier les sources à intégrer dans le Lakehouse.")
        next_steps.append("Définir les couches Bronze, Silver et Gold.")
        next_steps.append("Construire un Semantic Model partagé pour Power BI.")
        next_steps.append("Prévoir le monitoring des traitements et des refresh.")

    elif big_volume:
        architecture = "Data Warehouse"
        modelisation = "Star Schema"
        storage_mode = "Import avec Incremental Refresh ou Composite Model"
        transformation = "SQL / ELT"
        semantic_layer = "Semantic Model partagé"
        refresh = "Incremental Refresh"

        reasons.append("Le volume de données est important et nécessite de préparer les données avant leur utilisation dans Power BI.")
        reasons.append("Un Data Warehouse permet de structurer les données, d’améliorer les performances et de fiabiliser les indicateurs.")

        recommendations.append("Utiliser un modèle en étoile pour rendre le modèle plus performant et plus simple à comprendre.")
        recommendations.append("Prévoir l’actualisation incrémentielle si l’historique est volumineux.")

        next_steps.append("Identifier les tables de faits et les dimensions.")
        next_steps.append("Créer une table calendrier fiable.")
        next_steps.append("Préparer les transformations lourdes en SQL ou dans une couche Data dédiée.")
        next_steps.append("Mettre en place l’Incremental Refresh si les données historiques sont importantes.")

    elif multiple_sources or history or multi_reports:
        architecture = "Data Mart ou Data Warehouse"
        modelisation = "Star Schema"
        storage_mode = "Import optimisé"
        transformation = "SQL + Power Query"
        semantic_layer = "Semantic Model partagé"
        refresh = "Refresh planifié"

        reasons.append("Plusieurs sources, l’historisation ou plusieurs rapports nécessitent une couche de données réutilisable.")
        reasons.append("Centraliser les données permet d’éviter que chaque rapport travaille avec ses propres règles et ses propres chiffres.")

        recommendations.append("Commencer par un Data Mart si le périmètre est limité à un domaine métier.")
        recommendations.append("Évoluer vers un Data Warehouse si plusieurs domaines doivent partager les mêmes données.")
        recommendations.append("Créer un Semantic Model partagé pour centraliser les mesures importantes.")

        next_steps.append("Définir les clés communes et les règles de rapprochement entre sources.")
        next_steps.append("Identifier les indicateurs utilisés dans plusieurs rapports.")
        next_steps.append("Construire un modèle en étoile avec faits et dimensions.")
        next_steps.append("Documenter les définitions métier principales.")

    elif medium_volume:
        architecture = "Power BI optimisé"
        modelisation = "Star Schema"
        storage_mode = "Import optimisé"
        transformation = "Power Query"
        semantic_layer = "Dataset Power BI"
        refresh = "Refresh planifié"

        reasons.append("Le volume est intermédiaire : Power BI peut suffire, mais le modèle doit être propre et optimisé.")
        reasons.append("Un modèle en étoile permet d’améliorer les performances et la compréhension.")

        recommendations.append("Limiter les colonnes importées dans Power BI.")
        recommendations.append("Éviter les relations complexes et les tables plates trop larges.")

        next_steps.append("Supprimer les colonnes inutiles.")
        next_steps.append("Réduire la cardinalité des colonnes utilisées.")
        next_steps.append("Optimiser les mesures DAX principales.")
        next_steps.append("Vérifier les temps de refresh.")

    else:
        architecture = "Power BI standard"
        modelisation = "Star Schema"
        storage_mode = "Import"
        transformation = "Power Query"
        semantic_layer = "Dataset Power BI"
        refresh = "Refresh planifié"

        reasons.append("Le contexte ne nécessite pas encore une architecture Data lourde.")
        reasons.append("Power BI peut couvrir le besoin si le modèle est bien structuré dès le départ.")

        next_steps.append("Clarifier le besoin métier.")
        next_steps.append("Structurer les sources de données.")
        next_steps.append("Construire un modèle en étoile simple.")
        next_steps.append("Valider les KPIs avec les utilisateurs.")

    if quality in ["Moyenne", "Mauvaise", "Inconnue"]:
        risks.append({
            "titre": "Qualité des données à surveiller",
            "detail": "Si les données contiennent des doublons, des valeurs manquantes ou des formats incohérents, les indicateurs Power BI peuvent devenir faux ou difficiles à expliquer.",
            "action": "Mettre en place des contrôles sur les doublons, les valeurs vides, les types de données et les clés métier."
        })
        next_steps.append("Mettre en place un contrôle qualité sur les données sources.")

    if not business_definitions:
        risks.append({
            "titre": "Définitions métier non stabilisées",
            "detail": "Si chaque service définit les indicateurs différemment, plusieurs rapports peuvent afficher des chiffres différents pour un même KPI.",
            "action": "Créer un dictionnaire métier avec les définitions des KPIs et les faire valider par les utilisateurs."
        })
        next_steps.append("Créer un dictionnaire métier et faire valider les KPIs.")

    if history:
        recommendations.append("Prévoir une stratégie d’historisation : snapshots, SCD Type 2 ou conservation des transactions selon le cas.")
        next_steps.append("Identifier les champs à historiser : client, article, prix, statut, stock ou KPI.")

    if transformations in ["Complexes", "Très complexes"]:
        recommendations.append("Éviter de concentrer toutes les transformations complexes dans Power Query.")
        next_steps.append("Déporter les transformations lourdes en SQL, Dataflow, Pipeline Fabric ou Data Warehouse.")

    if sensitive_data:
        security = "RLS / OLS"
        recommendations.append("Prévoir une sécurité par utilisateur si les données doivent être filtrées par site, service, pays ou rôle.")
        next_steps.append("Créer une table de sécurité avec utilisateurs, rôles et périmètres autorisés.")
    else:
        security = "Accès workspace standard"

    if self_service:
        recommendations.append("Prévoir un Semantic Model documenté pour permettre aux utilisateurs de créer leurs propres rapports de manière maîtrisée.")
        next_steps.append("Centraliser les mesures DAX et documenter les tables exposées aux utilisateurs.")

    result = {
        "architecture": architecture,
        "modelisation": modelisation,
        "storage_mode": storage_mode,
        "transformation": transformation,
        "semantic_layer": semantic_layer,
        "security": security,
        "refresh": refresh,
        "recommendations": list(dict.fromkeys(recommendations)),
        "reasons": list(dict.fromkeys(reasons)),
        "risks": risks,
        "next_steps": list(dict.fromkeys(next_steps)),
    }

    return result


def get_concept_detail(concept_name):
    return CONCEPT_DETAILS.get(concept_name)


def display_concept_card(concept_name):
    detail = get_concept_detail(concept_name)

    if not detail:
        return

    with st.expander(f"Comprendre : {detail['titre']}", expanded=False):
        st.markdown("#### Définition simple")
        st.write(detail["definition"])

        st.markdown("#### Explication avec des mots simples")
        st.write(detail["explication"])

        st.markdown("#### Exemple visuel")
        st.code(detail["exemple"], language="text")

        st.markdown("#### Quand l’utiliser ?")
        for item in detail["quand_utiliser"]:
            st.write(f"- {item}")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### Avantages")
            for item in detail["avantages"]:
                st.write(f"- {item}")

        with col2:
            st.markdown("#### Limites")
            for item in detail["limites"]:
                st.write(f"- {item}")

        st.markdown("#### Exemple concret")
        st.info(detail["exemple_metier"])


def display_recommendation_report(answers, result):
    st.divider()

    st.subheader("Architecture recommandée")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Architecture", result["architecture"])
        st.metric("Modélisation", result["modelisation"])

    with col2:
        st.metric("Mode stockage", result["storage_mode"])
        st.metric("Transformation", result["transformation"])

    with col3:
        st.metric("Couche sémantique", result["semantic_layer"])
        st.metric("Sécurité", result["security"])

    st.markdown("---")

    st.subheader("Résumé exécutif")

    source_list = ", ".join(answers["source_types"])

    st.info(
        f"""
Votre contexte indique un besoin de type **{answers['business_need']}**.

Les données proviennent de : **{source_list}**.

Le volume estimé est : **{answers['volume']}**.

La fréquence d’actualisation souhaitée est : **{answers['frequency']}**.

Dans ce contexte, la recommandation est de partir sur **{result['architecture']}** avec une modélisation **{result['modelisation']}**.

L’objectif est d’obtenir des rapports plus fiables, plus cohérents et plus faciles à maintenir dans le temps.
"""
    )

    st.subheader("Pourquoi cette recommandation ?")

    for reason in result["reasons"]:
        st.write(f"- {reason}")

    st.markdown(
        """
En pratique, cela signifie que l’application ne cherche pas uniquement à afficher des graphiques.
Elle cherche surtout à proposer une organisation des données adaptée au contexte.

Une bonne architecture évite plusieurs problèmes fréquents :

- plusieurs rapports avec des chiffres différents ;
- des fichiers Excel difficiles à maintenir ;
- des refresh trop longs ;
- des indicateurs mal définis ;
- une dépendance trop forte à une seule personne.
"""
    )

    if result["recommendations"]:
        st.subheader("Recommandations complémentaires")

        for recommendation in result["recommendations"]:
            st.write(f"- {recommendation}")

    st.subheader("Comprendre les éléments proposés")

    concepts_to_explain = [
        result["architecture"],
        result["modelisation"],
        result["storage_mode"],
        result["transformation"],
        result["semantic_layer"],
        result["security"],
    ]

    already_displayed = set()

    for concept in concepts_to_explain:
        if concept not in already_displayed:
            display_concept_card(concept)
            already_displayed.add(concept)

    st.subheader("Points de vigilance")

    if result["risks"]:
        for risk in result["risks"]:
            with st.warning(risk["titre"]):
                st.write(risk["detail"])
                st.markdown("**Action recommandée :**")
                st.write(risk["action"])
    else:
        st.success(
            "Aucun point bloquant majeur n’a été détecté avec les réponses fournies. "
            "Il reste toutefois important de valider les données et les indicateurs avec les utilisateurs métier."
        )

    st.subheader("Plan d’action recommandé")

    st.write(
        "L’idée n’est pas de tout construire en une fois, mais d’avancer progressivement avec une logique claire."
    )

    for index, step in enumerate(result["next_steps"], start=1):
        st.write(f"{index}. {step}")

    st.success(
        "Objectif final : obtenir une solution fiable, compréhensible par le métier, maintenable par l’équipe Data et évolutive dans le temps."
    )


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

    if content.splitlines():
        title = content.splitlines()[0].replace("#", "").strip()
    else:
        title = selected_file.name

    diagram_code = extract_mermaid(content)

    st.subheader(title)

    if diagram_code:
        result = mermaid(
            diagram_code,
            theme="neutral",
            key=f"diagram_{selected_file.name}"
        )

        if isinstance(result, dict) and result.get("entity_clicked"):
            clicked = result.get("entity_clicked")
            st.info(f"Nœud sélectionné : {clicked}")

            concept_detail = get_concept_detail(clicked)

            if concept_detail:
                display_concept_card(clicked)
            else:
                st.write(
                    "Aucune fiche explicative détaillée n’est encore disponible pour ce concept."
                )

        with st.expander("Voir le code Mermaid"):
            st.code(diagram_code, language="mermaid")
    else:
        st.error("Aucun bloc Mermaid trouvé dans ce fichier.")


def display_diagnostic():
    st.subheader("Questionnaire de cadrage Data / BI")

    st.write(
        "Réponds aux questions ci-dessous. L’application proposera ensuite une architecture cible "
        "avec une explication claire, des exemples et un plan d’action."
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

    if "recommendation" in st.session_state and "answers" in st.session_state:
        display_recommendation_report(
            st.session_state["answers"],
            st.session_state["recommendation"]
        )


def display_methodology():
    st.subheader("Méthodologie")

    st.markdown(
        """
Cette application sert à aider à choisir une architecture Data / BI en fonction du contexte.

La logique utilisée est la suivante :

1. Comprendre le besoin métier.
2. Identifier les sources.
3. Évaluer le volume.
4. Évaluer la fréquence d’actualisation.
5. Vérifier si l’historisation est nécessaire.
6. Évaluer la qualité des données.
7. Déterminer si plusieurs rapports doivent partager les mêmes données.
8. Choisir une architecture adaptée.
9. Expliquer les concepts avec des exemples simples.
10. Proposer un plan d’action.

### Règles principales

- Excel + faible volume + un seul rapport  
  → Power BI simple.

- Plusieurs sources + plusieurs rapports  
  → Data Mart ou Data Warehouse.

- Gros volume + historique  
  → Data Warehouse avec modèle en étoile.

- Très gros volume ou temps réel  
  → Lakehouse / Fabric.

- Besoin de self-service BI  
  → Semantic Model partagé.

- Données sensibles  
  → RLS / OLS.
"""
    )


st.title("Data Analytics Decision Tree")
st.caption("Assistant interactif pour choisir et comprendre une architecture Data / BI / Power BI.")

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
