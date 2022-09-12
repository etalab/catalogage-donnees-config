# Récupérer les chemins de fichier pour les schéma

# Pour chaque chemin
#     Récupérer l'organization
#      Récupérer le SIRET de l'organization
#      Récupérer le schéma

#      Uploader l'organization
#      Si l'upload de l'organization échoue
#         Afficher un message d'erreur
#         Passer à la prochaine itération
#      Si le status code retourné par l'API est 200
#         Indiquer à l'utilisateur que tout est ok
#      Si le status code retourné par l'API est 201
#         Inidquer à l'utilisateur qu'il y a eu une création

#       Uploader le schéma
#       Si l'upload du schéma échoue
#         Afficher un message d'erreur
#         Passer à la prochaine itération

#       Est-ce que le schéma possède des champs complémentaires ?
#             Si oui envoyer à l'API les champs complémentaires
#      Si le status code retourné par l'API est 200
#         Indiquer à l'utilisateur que tout est ok
#      Si le status code retourné par l'API est 201
#         Inidiquer à l'utilisateur qu'il y a eu une création
