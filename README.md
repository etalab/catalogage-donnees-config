# `catalogage-donnees-config`

Ce répertoire contient des fichiers de configuration relatifs à l'instance de production de l'outil [catalogage-donnees](https://github.com/etalab/catalogage-donnees) en cours de développement.

La première instance de l'outil est déployée sur [catalogue.data.gouv.fr](https://catalogue.data.gouv.fr) et est coordonnée par la DINUM.

Pour plus d'informations, consultez la [documentation à destination des utilisateurs](https://github.com/etalab/catalogage-donnees/wiki/Documentation-%C3%A0-destination-des-utilisateurs).

## Utilisation

Si vous voulez ajouter une organisation sur catalogue.data.gouv.fr, avec ou sans catalogue, c'est ici que ça se passe !

L'activation du catalogue d'une organisation peut se faire au même moment que l'ajout de l'organisation elle-même, mais peut également avoir lieu dans un second temps. En effet, une organisation peut exister sans catalogue, par exemple afin de permettre à ses membres d'accéder au service et consulter les catalogues des autres organisations, tout en prenant le temps de préparer la création de son propre catalogue. Le choix du schéma du catalogue est un élément important de cette préparation. Il doit comporter à minima tous les champs du [schéma commun](https://github.com/etalab/schema-catalogue-donnees), auxquels des "champs complémentaires" peuvent être ajoutés.

:warning: Attention, une fois un catalogue activé sur catalogue.data.gouv.fr, il n'est plus possible d'en modifier le schéma.

### Ajouter une organisation

Pour ajouter une nouvelle organisation sur catalogue.data.gouv.fr, nommée par exemple `Mon ministère` :

1. Créez un dossier dans `organizations`, par exemple `organizations/mon-ministere`.
2. Placez-y un fichier `organization.json`. Il doit respecter ce format :

   ```json
   [
     {
       "name": "Mon ministère",
       "siret": "00011122233333"
     }
   ]
   ```

   **N.B.** Il est de votre responsabilité de vérifier que le numéro SIRET de l'organisation est valide et correspond bien à l'organisation cible.

3. Créez une _pull request_ (PR) avec ces changements. Un script automatisé vérifiera la conformité du fichier. La PR sera ensuite passée en revue par l'équipe de catalogue.data.gouv.fr.
4. Une fois la PR acceptée, un script automatisé ajoutera l'organisation sur catalogue.data.gouv.fr avec les informations renseignées.

### Activer le catalogue d'une organisation

_À venir..._

## Développement

Cette section est destinée à l'équipe de développement de ce dépôt.

### Prérequis

* Python 3.8+

### Démarrage rapide

Pour installer les dépendances :

```
make install
```

Pour lancer les tests :

```
make test
```

(Un test supplémentaire qui interagit avec `http://localhost:3579` s'exécute si le serveur local de `catalogage-donnees` tourne et que vous avez [configuré](#configuration) les variables d'environnement en conséquence.)

Pour formatter automatiquement le code :

```
make format
```

Pour valider le code (format, linters, etc) et les organisations :

```
make check
```

Pour mettre en ligne manuellement les organisations nouvelles (ce script est normalement lancé par la CI, vous devrez donc être en possession des variables de configuration adéquates) :

```
make upload
```

### Configuration

| Variable d'environnement | Description | Valeur par défaut |
|---|---|---|
| `CATALOGAGE_API_URL` | URL de l'API de l'instance de `catalogage-donnees` sur laquelle créer les organisations. | _Requis_ |
| `CATALOGAGE_API_KEY` | Clé d'API utilisée pour les requêtes HTTP avec l'API `catalogage-donnees` | _Requis_ |

Les valeurs liées à l'instance https://catalogue.multi.coop sont configurées dans les secrets GitHub Actions de ce dépôt.

En local, des valeurs liées à un serveur `catalogage-donnees` local peuvent être définies dans un fichier `.env` :

```bash
CATALOGAGE_API_URL="http://localhost:3579"
CATALOGAGE_API_KEY="..."  # (1)
```

(1) Doit correspondre à la variable `APP_CONFIG_REPO_API_KEY` côté `catalogage-donnees`. Voir [Configuration (Démarrage rapide) | catalogage-donnees](https://github.com/etalab/catalogage-donnees/blob/6d2c8d9de5069d40fa515d11782ddc66a1026de7/docs/fr/demarrage.md#configuration).

## Licence

AGPL 3.0
