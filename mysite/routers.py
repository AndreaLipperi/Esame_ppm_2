# routers.py

class IngrossoRouter:
    """
    Un router per controllare tutte le operazioni di database per i modelli ingrosso.
    """
    def db_for_read(self, model, **hints):
        """
        Tentativi di lettura dei modelli ingrosso vanno al database ingrosso.
        """
        if model._meta.app_label == 'myPage':
            return 'ingrosso'
        return None

    def db_for_write(self, model, **hints):
        """
        Tentativi di scrittura dei modelli ingrosso vanno al database ingrosso.
        """
        if model._meta.app_label == 'myPage':
            return 'ingrosso'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Permetti relazioni se un modello nella ingrosso_app è coinvolto.
        """
        if obj1._meta.app_label == 'myPage' or \
                obj2._meta.app_label == 'myPage':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Assicurati che la app ingrosso_app app vada solo al database ingrosso.
        """
        if app_label == 'myPage':
            return db == 'ingrosso'
        return None
