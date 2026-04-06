## Changelog v0.2
- Ajout du soulignage
- Ajout de mode de texte barré
- Modification : les symboles pour la mise en page disparaîssent lorsque le curseur n'est pas dessus
- Correction d'un bug où le point qui montre que le fichier n'a pas été sauvegardé restait tout le temps. Maintenant il s'en va quand le fichier a été sauvegardé.
- Modification : les symboles pour les couleurs (anciennement ```$@ @$```) a été modifié en &^^& car les dollars de l'ancien trigger interferait avec les autres éditeurs qui disposaient des LaTeX.
- Tentative d'ajout de drag n drop pour ouvrir les fichiers (ne fonctionne pas).
- Ajout d'une fonctionnalitée de recherche dans le document.
- Ajout d'un menu en cas de fermeture de l'app / d'un onglet qui n'est pas sauvegardé qui demande si on veut tout sauvegarder.

## Changelog v0.1
- Ajout d'un thème clair et sombre
- Masquage des symboles "$@ et @$" quand le curseur de texte n'y est plus pour une vue plus dégagée du texte
- Ajout d'onglet pour que la création de fichier se fasse correctement
- Modification du titre de la fenêtre en fonction du nom du fichier sur lequel on est en train d'éditer
- Modification de la police d'écriture en Consolas
- Ajout d'une dépendance python sur PIL*
- Réglage d'un bug (qui vient de la beta v0.1) qui au lancement de l'application, il y avait deux fenêtre (dont une complètement inutilisable)

&^gray *utilisé seulement pour mettre une icône svg pour le bouton thème clair et sombre, mais on ne sait jamais ;)^&

## Changelog beta v0.1
- Ajout de la coloration de texte (avec les symboles $@ et @$)
- Optimisation de performance*
- Réglage d'un bug où quand une mise en page a été créée, impossible de l'enlever si ce n'est de réécrire la phrase
- Ajout de la possibilité d'ouvrir des fichiers déjà créés
- Ajout de créer des fichiers (non utilisable proprement, car il n'ouvrait pas une nouvelle fenêtre mais supprimait complètement l'ancien document s'il n'était pas sauvegardé)
- Ajout de la sauvegarde "sous" de fichiers
- Changement de la police d'écriture en Andale Mono

&^gray *Au lieu de rafraîchir tout le document à chaque mise en page, il rafraîchit un bloc.^&

## Changelog v0.0
- Ajout des titres de 1 à 4
- Ajout de l'italique
- Ajout du gras
- Ajout de la coloration syntaxique en fonction de la mise en page
- Ajout de la sauvegarde de fichier
