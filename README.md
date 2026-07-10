# Data Analytics Decision Tree

Arbre décisionnel permettant de choisir la meilleure architecture Data & BI.

## Vue globale

```mermaid
flowchart TD

A[Projet Data Analytics]

A --> B{Besoin métier identifié ?}

B -- Non --> B1[Clarifier le besoin]

B -- Oui --> C{Combien de sources ?}

C --> D[1 source]
C --> E[Plusieurs sources]

D --> F{Volume > 5M lignes ?}

F -- Non --> G[Power BI Import]

F -- Oui --> H[Incremental Refresh]

E --> I{Historisation nécessaire ?}

I -- Non --> J[Data Mart]

I -- Oui --> K[Data Warehouse]

K --> L{Volume > 100M lignes ?}

L -- Oui --> M[Lakehouse]

L -- Non --> N[Star Schema]

M --> O[Semantic Model]

N --> O

G --> O

H --> O

J --> O

O --> P[Dashboard Power BI]

P --> Q[Publication]
```

## Modules à développer

- Sources
- Volume
- Qualité des données
- Historisation
- Architecture
- Modélisation
- Performance
- Sécurité
- Gouvernance
