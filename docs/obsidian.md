# Obsidian

Obsidian est une application de prise de notes basée sur des fichiers Markdown. Les notes générées par le scraper sont compatibles car elles sont en md.

---

## Qu'est-ce qu'un vault ?

Un **vault** dans Obsidian est simplement un dossier sur ton disque. Obsidian lit tous les fichiers `.md` qu'il contient et gère les liens entre eux.

---

## Importer les notes

**1. Télécharger les festivals**

Aller sur GitHub → onglet **Actions** → dernier run → télécharger **festivals-obsidian-2026**.

**2. Extraire dans ton vault**

```
ton-vault/
└── Festivals 2026/
    ├── INDEX.md
    ├── 2026-06-Juin.md
    ├── 2026-07-Juillet.md
    └── festivals/
        ├── Hellfest.md
        ├── Rock en Seine.md
        └── ...
```

**3. Ouvrir INDEX.md**

Les liens sont automatiquement cliquables dans Obsidian.

---

## Les liens

```markdown
[[INDEX|← Retour à l'index]]        # lien avec texte personnalisé
[[festivals/Hellfest|Hellfest]]      # lien vers un sous-dossier
[[2026-07-Juillet]]                  # lien vers la note du mois
```

---

## La vue graphe

Raccourci : `Ctrl + G`

Ca affiche toutes les notes sous forme de map en mode cerveau. L'INDEX est au centre, les notes de mois autour, les festivals tout autour. Si on clique sur une note precis ça enmène sur la bonne page

---

## Mettre à jour

Quand le workflow tourne à nouveau, télécharger le nouveau fichier et remplacer les fichiers dans `Festivals 2026/`. Obsidian détecte les changements automatiquement.