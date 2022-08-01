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

Pour formatter automatiquement le code :

```
make format
```

Pour valider le code (format, linters, etc) et les organisations :

```
make check
```

## Licence

AGPL 3.0
