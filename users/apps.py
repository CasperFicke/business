# users/apps.py

# django
from django.apps import AppConfig

# 
class UsersConfig(AppConfig):
  default_auto_field = 'django.db.models.BigAutoField'
  name = 'users'
  
  # registrastion of the signal
  def ready(self):
    import users.signals
