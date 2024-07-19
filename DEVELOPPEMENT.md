# NOTES DE DEVELOPPEMENT

## 1. Choix technologiques

### Intégration de Boostrap

Bootstrap v5 a été choisi pour le design du site. L'intégration de Boostrap peut s'effectuer grâce à la bibliothèque [django-bootstrap-v5](https://django-bootstrap-v5.readthedocs.io/en/latest/installation.html).

Toutefois cette bibliothèque utilise la version de Bootstrap en ligne (via CDN), ce qui peut poser des problèmes d'affichage du site en cas d'accès hors-ligne. Cette bibliothèque, bien qu'installée, n'est toutefois pas activée dans la variable `INSTALLED_APPS` du fichier `settings.py`.

Afin de personnaliser le design en modifiant les variables Sass de Bootstrap, il a été décidé d'utiliser les versions sources locales.

Les fichiers de Boostratp sont donc situé dans : `app_edcp/static/bootstrap`.
La personnalisation des variables, essentiellement pour le jeu de couleur se fait dans le fichier `theme-apdcp.scss` du dossier `static`.

**NB:**

- l'ajout des variables personnalisées dans le fichier `theme-apdcp.scss` doit se faire **avant** l'importation du fichier `bootstrap.css`.
- le fichier `bootstrap.bundle.min.js` (_et non bootstrap.min.js_) est utilisé tel quel.

### Live reload

Les modifications du CSS exigeant des rafraichissements fréquents des pages, la bibliothèque `django-livereload-server`a été utilisée.

## 2. Bibliothèques ajoutées

- **django-bootstrap-v5** : intégration de bootstrap. Désactivé ;
- **django-livereload-server** : rechargement automatique des pages web. Lancer la commande avec `python manage.py livereload`, avant de lancer `runserver` ;
- **django-compress** et **django-libsass** : utilisés conjointement pour la compilation des fichiers `scss` en `css` et la compression des fichiers statiques CSS et JS.
- **django-crispy-form** et **crispy-bootstrap5** : utilisés pour la mise en forme automatique des formulaires django avec bootstrap ;
