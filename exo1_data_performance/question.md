# Calculez et commentez le taux de réduction de l'espace de stockage du Parquet simple et du Parquet compressé par rapport au CSV.

## 📊 Interprétation et commentaires

| Format | Taille (MB) | Réduction vs CSV | Commentaire |
|:--|--:|--:|:--|
| **CSV** | 1309.01 | — | Format brut textuel, très volumineux et redondant. Aucune optimisation du stockage. |
| **Parquet (non compressé)** | 199.96 | **−84.7 %** | Grâce au stockage en colonnes et à la gestion typée des données, le format Parquet réduit significativement la taille des fichiers sans compression. |
| **Parquet (compressé – Brotli)** | 133.32 | **−89.8 %** | L’ajout de la compression Brotli améliore encore la compacité du fichier, offrant un **gain supplémentaire d’environ 33 %** par rapport au Parquet non compressé. |

### 🧠 Synthèse

- Le **format Parquet** (même sans compression) offre déjà une réduction notable de la taille du fichier d’environ **85 %** par rapport au CSV.  
- En utilisant **Brotli**, on atteint près de **90 % de réduction** — soit une division par **10 de l’espace disque** requis.  
- Cette efficacité s’explique par :
  - La **structuration en colonnes**, qui élimine la redondance des noms de colonnes.
  - Une **meilleure typage** des données.
  - La **compression Brotli**, particulièrement performante pour les données textuelles et répétitives.

✅ **Conclusion :** Le format *Parquet compressé (Brotli)* combine compacité et performance, ce qui en fait un excellent choix pour le stockage et le traitement de gros volumes de données.

# Expliquez en détail pourquoi le temps de lecture ciblée est significativement plus rapide pour le format Parquet que pour le CSV, en vous basant sur la nature du stockage (ligne vs. colonne).

## ⚡ Analyse du temps de lecture ciblée : Parquet vs CSV

| Format | Temps de lecture (s) | Gain vs CSV | Gain vs Parquet (No Compression) |
|:--|--:|--:|--:|
| **CSV** | 10.52 s | — | — |
| **Parquet (non compressé)** | 0.67 s | **−9.85 s** | — |
| **Parquet (compressé – Brotli)** | 0.50 s | **−10.02 s** | **−0.17 s** |

### 🚀 Constats clés

- Le **CSV** met environ **10,5 secondes** à être lu.
- Le **Parquet non compressé** est lu en **0,67 seconde**, soit environ **15 fois plus rapide**.
- Le **Parquet compressé (Brotli)** reste le plus rapide : **0,50 seconde**, soit **plus de 20 fois plus rapide** que le CSV.

---

## 🧩 Explication : stockage en lignes vs stockage en colonnes

### 🔸 1. Format CSV : stockage **en lignes**
- Le **CSV** est un format **texte brut**, où les données sont stockées **ligne par ligne**.
- Pour lire une seule colonne, le moteur doit **parcourir toutes les lignes** et **analyser chaque champ** séparé par des délimiteurs (souvent des virgules ou points-virgules).
- Cela implique :
  - Une **lecture séquentielle complète du fichier**, même si seule une colonne est nécessaire.
  - Une **parsing coûteuse** (conversion de texte → types numériques).
  - Une **absence d’indexation** ou de métadonnées permettant un accès direct.

🧱 → En conséquence, le CSV n’est pas adapté aux lectures ciblées : il faut tout charger pour extraire un petit sous-ensemble.

---

### 🔹 2. Format Parquet : stockage **en colonnes**
- Le **Parquet** est un format **columnaire** et **binaire**.
- Les données d’une même colonne sont stockées **ensemble**, de manière contiguë sur le disque.
- Lorsqu’une lecture cible seulement quelques colonnes :
  - Seules ces colonnes sont **chargées en mémoire**, les autres ne sont **jamais lues**.
  - Les valeurs sont déjà **typiquement encodées** (entiers, floats, chaînes) → pas besoin de parsing textuel.
  - Des **métadonnées intégrées** (filtres, statistiques, index) permettent d’**éviter la lecture** des blocs non pertinents.

📦 → Résultat : le système lit beaucoup **moins de données physiques**, et le **décodage est plus rapide**.

---

### 🔹 3. Impact de la compression (Brotli)
- La **compression Brotli** réduit encore la taille des blocs de colonnes, ce qui :
  - Diminue les **I/O disque** (moins de données à lire).
  - Maintient une **décompression rapide**, optimisée pour les flux séquentiels.
- Ainsi, même compressé, le **temps de lecture reste plus court** que celui du Parquet non compressé.

---

## 🧠 Conclusion

| Aspect | CSV (ligne) | Parquet (colonne) |
|:--|:--|:--|
| Structure | Données stockées par ligne | Données regroupées par colonne |
| Lecture ciblée | Nécessite la lecture complète du fichier | Lecture sélective de colonnes uniquement |
| Parsing | Conversion texte → nombre coûteuse | Données déjà typées et encodées |
| Métadonnées | Aucune | Index, statistiques, filtres |
| Performance | Lente, surtout pour gros fichiers | Très rapide, même sur gros volumes |

✅ **En résumé :**  
Le format **Parquet** surpasse largement le **CSV** en lecture ciblée, grâce à son **stockage en colonnes**, à sa **structuration binaire optimisée**, et à l’usage de **métadonnées intelligentes** permettant de **charger uniquement les données nécessaires**.
