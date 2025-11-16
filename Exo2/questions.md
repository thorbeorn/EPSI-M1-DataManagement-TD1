# Expliquez comment une clé de chiffrement symétrique ou asymétrique serait utilisée en production.

## Contexte
Lorsqu'une application stocke des données sensibles dans une base de données (comme un email ou un numéro de carte), il est souvent nécessaire de **chiffrer ces données** afin qu'elles ne puissent être lues qu'avec une autorisation explicite.  

Dans ce contexte, on peut chiffrer la donnée **au moment de l’affichage** (ou juste avant de l’envoyer au client), en utilisant soit **une clé symétrique**, soit **une clé asymétrique**.

---

## 1. Chiffrement symétrique

### Principe
- Une **clé unique** (clé symétrique) est utilisée à la fois pour **chiffrer** et **déchiffrer** les données.
- Cette clé doit être stockée **en sécurité** dans un gestionnaire de clés (KMS/HSM) et ne doit être accessible qu'à l'équipe autorisée.

### Flux typique
1. Lorsqu'une donnée doit être affichée :
   - Le serveur récupère la clé symétrique depuis le KMS/HSM.
   - La donnée est chiffrée avec un algorithme AES (par exemple AES-GCM pour l'authenticité et la confidentialité).
2. Le `ciphertext` est envoyé au client ou stocké temporairement.
3. L'équipe autorisée peut utiliser la même clé pour **déchiffrer** la donnée si nécessaire.

### Avantages
- Très rapide pour de gros volumes.
- Permet de contrôler facilement qui peut accéder à la clé et donc aux données.

### Exemple de schéma
```txt
Utilisateur/Serveur → Récupération donnée → AES-GCM avec clé symétrique → Affichage chiffré
```

---

## 2. Chiffrement asymétrique

### Principe
- Utilise **une paire de clés** : 
  - **Clé publique** pour chiffrer.
  - **Clé privée** pour déchiffrer.
- Seule l’équipe autorisée possède la clé privée, garantissant que personne d’autre ne peut déchiffrer la donnée.

### Flux typique
1. La donnée à afficher est chiffrée avec la **clé publique** de l’équipe autorisée.
2. Le `ciphertext` peut être affiché ou stocké temporairement.
3. Pour lire la donnée en clair, l’équipe autorisée utilise la **clé privée** stockée en sécurité (HSM/KMS) pour la déchiffrer.

### Avantages
- Distribution sûre : tout le monde peut chiffrer la donnée avec la clé publique, mais seule l’équipe autorisée peut la lire.
- Permet un contrôle d’accès très fin sans exposer la capacité de déchiffrement.

### Exemple de schéma
```txt
Utilisateur/Serveur → Récupération donnée → Chiffrement avec clé publique → Affichage chiffré
Equipe autorisée → Déchiffrement avec clé privée → Lecture de la donnée
```

---

## 3. Bonnes pratiques en production
- **Ne jamais stocker les clés dans le code** : utiliser un KMS/HSM.
- **Utiliser des algorithmes sécurisés** (AES-GCM, ChaCha20-Poly1305, RSA-OAEP).
- **Audit et contrôle d’accès** : enregistrer qui a demandé le déchiffrement.
- **Rotation régulière des clés** : pour limiter l’impact en cas de compromission.
- **Envelope encryption** : chiffrer une clé de session (DEK) avec la clé principale (KEK) pour faciliter la rotation et la sécurité.

---

## 4. Conclusion
- Le chiffrement symétrique est efficace et rapide pour un usage interne où l'équipe autorisée peut récupérer la clé.
- Le chiffrement asymétrique permet de séparer clairement les rôles : tout le monde peut chiffrer avec la clé publique, seule l’équipe autorisée peut déchiffrer avec la clé privée.
- Dans les deux cas, le chiffrement à l’affichage protège les données sensibles et limite les risques de fuite ou d’exposition.

---

# Montrez l'exécution de cette fonction pour chaque rôle et décrivez comment vous garantiriez, dans un environnement réel (Cloud, Data Warehouse), que ces règles RBAC sont appliquées de manière infaillible.

## Table des rôles et accès aux colonnes

| Rôle                  | Colonnes accessibles                                                                 | Niveau de confidentialité                       |
|-----------------------|--------------------------------------------------------------------------------------|------------------------------------------------|
| Analyste_Marketing    | `id_client` (pseudonymisé), `montant_achat`, `ville_résidence` (généralisée)       | Données agrégées et anonymisées               |
| Support_Client_N1     | `id_client` (pseudonymisé), `nom` (masqué), `prénom` (masqué), `téléphone` (masqué), `montant_achat` | PII masquées pour identification              |
| Admin_Sécurité        | Toutes les colonnes, y compris les champs chiffrés/hachés (`email`)                 | Accès complet                                  |

---

## Mesures pour garantir le RBAC

### 1. Analyste_Marketing
- **Masquage / pseudonymisation automatique** : `id_client` pseudonymisé, `ville_residence` généralisée.
- **Vues matérialisées ou API dédiées** : accès uniquement aux données agrégées.
- **RBAC natif** : rôle limité aux vues sécurisées, pas d’accès direct aux tables brutes.
- **Audit et logs** : journalisation de toutes les requêtes SQL.
- **Tests automatisés** : scripts simulant des requêtes interdites pour valider les règles.

---

### 2. Support_Client_N1
- **Masquage dynamique des PII** : noms, prénoms, téléphone masqués.
- **Contrôle d’accès basé sur le rôle** : accès uniquement aux colonnes masquées.
- **Séparation des environnements** : sandbox contenant uniquement les données masquées.
- **Monitoring et alertes** : détection des tentatives de contournement.
- **Gestion des clés et chiffrement** : aucune clé de déchiffrement disponible pour ce rôle.

---

### 3. Admin_Sécurité
- **Accès restreint et audité** : toutes actions journalisées pour éviter les abus.
- **Chiffrement et gestion de clés** : accès aux données chiffrées avec rotation de clés.
- **Separation of duties (SoD)** : nombre limité d’admins ayant accès complet.
- **MFA et journalisation** : authentification multi-facteurs obligatoire, logs détaillés.
- **Tests périodiques** : validation que l’admin ne peut contourner le RBAC.

---

## Schéma conceptuel RBAC

```text
Data Warehouse / Cloud
┌──────────────────────────────┐
│          Tables brutes        │
│  (toutes les colonnes, PII)  │
└─────────────┬────────────────┘
              │
              │ Vues / API sécurisées
              ▼
┌─────────────┴─────────────┐
│      Analyste_Marketing    │
│  id_client pseudonymisé    │
│  montant_achat             │
│  ville_residence généralisée│
└────────────────────────────┘
              │
┌─────────────┴─────────────┐
│     Support_Client_N1      │
│  id_client pseudonymisé    │
│  nom/prénom/téléphone masqués │
│  montant_achat             │
└────────────────────────────┘
              │
┌─────────────┴─────────────┐
│       Admin_Sécurité       │
│  Toutes les colonnes       │
│  y compris email chiffré   │
└────────────────────────────┘
```