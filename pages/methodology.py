import streamlit as st

st.title("Méthodologie Data Analytics")

st.markdown("""
Cette application aide à déterminer quelle architecture Data / BI est la plus adaptée à un contexte donné.

L'objectif n'est pas de proposer la solution la plus complexe, mais la solution la plus adaptée.
""")

st.divider()

st.header("Les grandes étapes de décision")

st.markdown("""
### 1. Comprendre le besoin métier

Avant toute décision technique :

- Quel problème doit être résolu ?
- Quels indicateurs doivent être suivis ?
- Qui utilisera les données ?
- À quelle fréquence ?

Une solution technique n'a de valeur que si elle répond à un besoin métier réel.
""")

st.markdown("""
### 2. Identifier les sources de données

Exemples :

- Excel
- ERP
- CRM
- SQL
- SharePoint
- API
- IoT

Plus le nombre de sources augmente, plus la nécessité d'une couche centralisée devient importante.
""")

st.markdown("""
### 3. Évaluer la qualité des données

Questions classiques :

- Données complètes ?
- Doublons ?
- Formats cohérents ?
- Clés métier fiables ?

Des données de mauvaise qualité produisent souvent des indicateurs incorrects.
""")

st.markdown("""
### 4. Évaluer le volume

Ordres de grandeur :

- < 500k lignes
- 500k à 5M lignes
- 5M à 50M lignes
- 50M à 500M lignes
- > 500M lignes

Le volume influence directement l'architecture recommandée.
""")

st.markdown("""
### 5. Déterminer l'historisation

Questions :

- Faut-il conserver l'historique ?
- Combien de temps ?
- Doit-on voir les anciennes valeurs ?

L'historisation est souvent un facteur important pour choisir entre Power BI simple et Data Warehouse.
""")

st.markdown("""
### 6. Choisir l'architecture

Selon le contexte :

- Power BI simple
- Power BI optimisé
- Data Mart
- Data Warehouse
- Lakehouse / Fabric

L'architecture doit rester proportionnée au besoin.
""")

st.markdown("""
### 7. Choisir la modélisation

Les modèles les plus fréquents :

- Star Schema
- Snowflake
- Data Vault

Dans la majorité des projets Power BI :

✅ Star Schema
""")

st.markdown("""
### 8. Choisir la couche analytique

Possibilités :

- Dataset Power BI
- Semantic Model partagé
- Cube OLAP

Aujourd'hui, le Semantic Model est généralement privilégié dans l'écosystème Power BI moderne.
""")

st.markdown("""
### 9. Définir la sécurité

Exemples :

- Accès standard
- RLS (Row Level Security)
- OLS (Object Level Security)

La sécurité dépend du niveau de sensibilité des données.
""")

st.markdown("""
### 10. Publier et gouverner

Une architecture n'est utile que si :

- Les indicateurs sont compris
- Les définitions sont documentées
- Les utilisateurs font confiance aux données
- Les rapports sont maintenables
""")

st.divider()

st.header("Niveaux d'industrialisation")

st.info("""
Niveau 1
→ Rapport autonome

Niveau 2
→ Power BI maîtrisé

Niveau 3
→ Semantic Model partagé

Niveau 4
→ Data Warehouse + Semantic Model

Niveau 5
→ Lakehouse / Fabric entreprise
""")

st.divider()

st.header("Principes de recommandation")

st.markdown("""
### Pourquoi ne recommande-t-on pas toujours la solution la plus avancée ?

Parce qu'une architecture doit répondre au besoin réel.

Exemples :

✅ Besoin simple
→ Power BI simple

✅ Plusieurs rapports et plusieurs sources
→ Data Warehouse

✅ Très gros volume ou temps réel
→ Lakehouse

L'objectif est d'éviter :
- la sur-complexité
- les coûts inutiles
- la maintenance excessive
""")

st.divider()

st.header("Glossaire simplifié")

with st.expander("Star Schema"):

    st.write("""
Un Star Schema est un modèle en étoile.

Une table centrale contient les faits (ventes, commandes, production).

Autour :

- client
- produit
- date
- site

C'est le modèle recommandé pour Power BI.
""")

with st.expander("Data Warehouse"):

    st.write("""
Le Data Warehouse centralise les données provenant de plusieurs systèmes.

Objectifs :

- cohérence
- historisation
- réutilisation
- gouvernance
""")

with st.expander("Semantic Model"):

    st.write("""
Le Semantic Model centralise les mesures et la logique métier.

Exemple :

Chiffre d'affaires

Marge

Quantités

sont calculés une seule fois et réutilisés dans tous les rapports.
""")

with st.expander("Cube OLAP"):

    st.write("""
Un Cube OLAP est une technologie historique d'analyse multidimensionnelle.

Aujourd'hui, les Semantic Models Power BI répondent à la majorité des besoins similaires avec moins de complexité.
""")

with st.expander("Lakehouse"):

    st.write("""
Le Lakehouse est une architecture moderne adaptée :

- aux gros volumes
- aux données brutes
- à l'IA
- aux données IoT
- au temps réel
""")

st.divider()

st.success(
    "Le questionnaire de diagnostic utilise cette méthodologie pour construire ses recommandations."
)
