def recommend(answers):
    score = calculate_score(answers)

    architecture = ""
    modelisation = ""
    storage_mode = ""
    transformation = ""
    semantic_layer = ""
    security = ""

    why = []
    risks = []
    next_steps = []
    alternatives = []

    volume = answers["volume"]
    sources_count = answers["sources_count"]
    source_types = answers["source_types"]
    frequency = answers["frequency"]
    history = answers["history"]
    multi_reports = answers["multi_reports"]
    self_service = answers["self_service"]
    sensitive_data = answers["sensitive_data"]
    realtime = answers["realtime"]
    quality = answers["quality"]
    transformations = answers["transformations"]
    business_definitions = answers["business_definitions"]

    excel_only = source_types == ["Excel"]
    multiple_sources = sources_count != "1 source"
    medium_volume = volume == "5M à 50M lignes"
    big_volume = volume in ["50M à 500M lignes", "Plus de 500M lignes"]
    very_big_volume = volume == "Plus de 500M lignes"
    frequent_refresh = frequency in ["Horaire", "Temps réel"]

    if excel_only and volume in ["Moins de 500k lignes", "500k à 5M lignes"] and not multi_reports and not history:
        architecture = "Power BI simple"
        modelisation = "Modèle Power BI en étoile léger"
        storage_mode = "Import"
        transformation = "Power Query"
        semantic_layer = "Dataset local"

        why.append(
            "Les données semblent simples, peu volumineuses et principalement basées sur Excel."
        )
        why.append(
            "Un modèle Power BI simple permet de répondre rapidement au besoin sans mettre en place une architecture trop lourde."
        )

        next_steps.append("Nettoyer et structurer les fichiers Excel sources.")
        next_steps.append("Créer un modèle Power BI simple avec une table principale et quelques dimensions.")
        next_steps.append("Valider les indicateurs avec les utilisateurs métier.")
        next_steps.append("Documenter les sources utilisées.")

    elif realtime or very_big_volume:
        architecture = "Lakehouse / Fabric"
        modelisation = "Star Schema sur couche Gold"
        storage_mode = "Direct Lake ou modèle composite"
        transformation = "Pipeline ELT"
        semantic_layer = "Semantic Model partagé"

        why.append(
            "Le volume très important ou le besoin de temps réel dépasse le cadre d’un simple modèle Power BI."
        )
        why.append(
            "Une architecture Lakehouse permet de conserver les données brutes, de les nettoyer progressivement et de les exposer proprement à Power BI."
        )
        why.append(
            "Cette approche est plus adaptée lorsque les données doivent évoluer vers des usages avancés comme l’IA, l’IoT ou l’analyse temps réel."
        )

        next_steps.append("Identifier les sources à intégrer dans le Lakehouse.")
        next_steps.append("Définir les couches Bronze, Silver et Gold.")
        next_steps.append("Créer les tables prêtes à l’analyse dans la couche Gold.")
        next_steps.append("Construire un Semantic Model partagé pour Power BI.")
        next_steps.append("Mettre en place un monitoring des traitements et des rafraîchissements.")

    elif big_volume:
        architecture = "Data Warehouse"
        modelisation = "Star Schema"
        storage_mode = "Import avec Incremental Refresh ou Composite Model"
        transformation = "SQL / ELT"
        semantic_layer = "Semantic Model partagé"

        why.append(
            "Le volume de données est important et nécessite de préparer les données avant leur chargement dans Power BI."
        )
        why.append(
            "Un Data Warehouse permet de centraliser, nettoyer et structurer les données pour plusieurs rapports."
        )
        why.append(
            "Le modèle en étoile améliore la lisibilité, les performances et la maintenance des rapports Power BI."
        )

        next_steps.append("Identifier les tables de faits : ventes, commandes, production, stock, etc.")
        next_steps.append("Identifier les dimensions : date, client, produit, site, équipe, fournisseur, etc.")
        next_steps.append("Créer une table calendrier fiable.")
        next_steps.append("Préparer les transformations lourdes en SQL ou dans une couche Data dédiée.")
        next_steps.append("Mettre en place l’actualisation incrémentielle si l’historique est important.")

    elif multiple_sources or history or multi_reports:
        architecture = "Data Mart ou Data Warehouse"
        modelisation = "Star Schema"
        storage_mode = "Import optimisé"
        transformation = "SQL + Power Query
