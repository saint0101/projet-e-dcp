from django.core.exceptions import PermissionDenied


class UserHasAccessMixin:
  """
  Class qui vérifie si l'utilisateur peut avoir accès à un objet, si :
    - il est propriétaire de l'objet ;
    - il est membre du staff.
  Utilisée comme mixin pour l'affichage des objets dans les vues DetailView.
  """
  user_field = 'user'  # Champ utilisateur (par défaut)

  def get_object(self, queryset=None):
    obj = super().get_object(queryset)

    # Vérifie si l'objet a un champ 'user'
    if not hasattr(obj, self.user_field):
        raise AttributeError(f"L'objet n'a pas de champ '{self.user_field}'.")

    # Vérifie si le champ 'user' correspond à l'utilisateur connecté
    if getattr(obj, self.user_field) != self.request.user and not self.request.user.is_staff:
        raise PermissionDenied
    
    return obj