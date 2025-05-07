from .base import *
from decouple import config


setting_key = config('SETTING_KEY', default='local')
if setting_key == 'local':
    from .local import *

elif setting_key == 'production':
    from .production import *
