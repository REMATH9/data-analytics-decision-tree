# ETL Packs Definitions

Ce zip contient un fichier `etl_packs_extension.py` avec les 3 packs de definitions ETL / ELT.

## Methode recommandee

1. Extraire le zip.
2. Placer `etl_packs_extension.py` dans le dossier `data/` de ton projet Streamlit.
3. Dans `data/definitions_data.py`, tout en bas, APRES le crochet final de `DEFINITIONS = [...]`, ajouter :

```python
from data.etl_packs_extension import ETL_PACKS
DEFINITIONS.extend(ETL_PACKS)
```

Ainsi tu evites de coller des centaines de lignes avant le dernier `]`.

## Important

- Ne colle pas ce fichier dans `DEFINITIONS = [...]`.
- Ne supprime pas tes anciennes definitions.
- Si tu avais deja ajoute des fiches courtes ETL / ERP / CRM dans `definitions_data.py`, supprime-les pour eviter les doublons.
- Les titres doivent correspondre aux noeuds Mermaid pour que les clics fonctionnent.

## Contenu

- Pack 1 : ETL, ELT, Extract, Transform, Load, ERP, CRM, SQL Databases, Excel Files, APIs, IoT Devices, External Sources.
- Pack 2 : Data Cleaning, Standardization, Normalization, Data Integration, Data Enrichment, Business Rules, Validation, Aggregation, Data Modeling.
- Pack 3 : Load Methods, Full Load, Incremental Load, Append, Insert Only, Upsert, Merge, Watermark, CDC, Delta Load, Partitioning, Processing Types, Batch, Micro-Batch, Streaming, Real-Time, Targets, Bronze, Silver, Gold, Semantic Model.
