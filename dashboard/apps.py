from django.apps import AppConfig

class DashboardConfig(AppConfig):
    """
    This class configures the 'dashboard' app for the Django project.
    
    The AppConfig class is used to store metadata for an application such as its name
    and the default auto field for models.
    """
    
    default_auto_field = 'django.db.models.BigAutoField'
    # Sets the default field type for auto-generated primary keys.
    # 'BigAutoField' is an integer field that is automatically incremented 
    # and can store larger values than the standard 'AutoField'.

    name = 'dashboard'
    # Specifies the name of the app as 'dashboard'. This is the name used 
    # when referring to this app throughout the project.
