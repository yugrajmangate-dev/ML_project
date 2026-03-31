import os
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Cache instance (initialized in create_app via init_app)
cache = Cache()

# Limiter instance — storage uri is read from environment at import time
limiter = Limiter(key_func=get_remote_address, default_limits=["60 per minute"], storage_uri=os.environ.get('RATELIMIT_STORAGE_URL', 'memory://'))
