# `catalogage-donnees-config`

Ce répertoire contient des fichiers de configuration relatifs à l'instance de production de l'outil [catalogage-donnees](https://github.com/etalab/catalogage-donnees) en cours de développement.

La première instance de l'outil sera le service connu sous le nom de `catalogue.data.gouv.fr`, coordonné par la DINUM.

## Utilisation

### Ajouter une organisation

Pour créer une nouvelle organisation, nommée par exemple `Mon ministère` :

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

3. Créez une _pull request_ (PR) avec ces changements. Un script automatisé vérifiera la conformité des fichiers au format décrit ci-dessus. La PR devra ensuite être revue.
4. Une fois la PR acceptée et _mergée_ dans la branch `main`, un script automatisé ajoutera l'organisation à l'instance avec les informations renseignées.

En cas d'erreur de saisie, de changement des informations ou de tout autre problème suite à la création, merci de contacter l'équipe de développement, par exemple via le canal `~catalogage` du Mattermost de la communauté BetaGouv, ou via une issue sur ce dépôt.

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
