from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.db import connections, DEFAULT_DB_ALIAS


class DatabaseRouterMiddleware(MiddlewareMixin):
    def process_request(self, request):
        host = request.get_host()
        if '127.0.0.1' in host:
            settings.DATABASES['default'] = settings.DATABASES['db_localhost']
        elif '.vercel.app' in host:
            settings.DATABASES['default'] = settings.DATABASES['db_vercel']
        else:
            settings.DATABASES['default'] = settings.DATABASES['db_localhost']  # Imposta un database predefinito

        # Reimposta la connessione al database in base alle nuove impostazioni
        connections[DEFAULT_DB_ALIAS].close()
