# Redis Cache & Session Configuration Guide

This document explains how Redis is configured for caching and sessions in Finory IA.

## Prerequisites

1. **Install Redis Server**
   ```bash
   # Ubuntu/Debian
   sudo apt-get update
   sudo apt-get install redis-server
   
   # macOS (using Homebrew)
   brew install redis
   
   # Start Redis
   sudo systemctl start redis  # Linux
   brew services start redis   # macOS
   ```

2. **Install Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   
   This will install:
   - `redis==5.0.1` - Redis Python client
   - `hiredis==2.2.3` - Fast Redis protocol parser
   - `celery==5.3.4` - Task queue (also uses Redis)

## Configuration

### Environment Variables

Add these to your `.env` file:

```env
# Redis Configuration
REDIS_URL=redis://127.0.0.1:6379/1
CACHE_URL=redis://127.0.0.1:6379/1
SESSION_CACHE_URL=redis://127.0.0.1:6379/2

# Session Configuration
SESSION_ENGINE=django.contrib.sessions.backends.cached_db
SESSION_CACHE_ALIAS=session
SESSION_COOKIE_AGE=86400
SESSION_COOKIE_SECURE=False  # Set to True in production with HTTPS
SESSION_COOKIE_SAMESITE=Lax
SESSION_SAVE_EVERY_REQUEST=False
SESSION_EXPIRE_AT_BROWSER_CLOSE=False

# Celery (also uses Redis)
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

### Redis URL Format

```
redis://[:password]@host:port/db
```

Examples:
- `redis://127.0.0.1:6379/1` - No password, database 1
- `redis://:mypassword@127.0.0.1:6379/1` - With password
- `redis://localhost:6379/0` - Default database

### Database Allocation

- **Database 0**: Celery broker and result backend
- **Database 1**: Default cache (`CACHE_URL`)
- **Database 2**: Session cache (`SESSION_CACHE_URL`)

## Cache Configuration

The system uses Redis for caching with automatic fallback to database cache if Redis is unavailable.

### Cache Aliases

1. **`default`**: General application cache
   - Key prefix: `finory_cache`
   - Default timeout: 300 seconds (5 minutes)
   - Used for: General caching, tenant information, etc.

2. **`session`**: Session storage cache
   - Key prefix: `finory_session`
   - Used for: User sessions

3. **`dummy`**: Dummy cache (for testing)
   - No actual storage

## Session Configuration

### Session Backend Options

1. **`django.contrib.sessions.backends.cached_db`** (Recommended)
   - Uses Redis cache with database fallback
   - Best performance with data persistence
   - Sessions survive Redis restarts

2. **`django.contrib.sessions.backends.cache`**
   - Pure Redis cache
   - Fastest performance
   - Sessions lost if Redis restarts

3. **`django.contrib.sessions.backends.db`**
   - Database only
   - Fallback if Redis unavailable
   - Slower but most reliable

### Session Security Settings

- **SESSION_COOKIE_AGE**: 86400 (24 hours)
- **SESSION_COOKIE_SECURE**: False (set True with HTTPS)
- **SESSION_COOKIE_HTTPONLY**: True (prevents JavaScript access)
- **SESSION_COOKIE_SAMESITE**: Lax (CSRF protection)

## Testing Redis Connection

### Test from Python

```python
import redis
r = redis.from_url('redis://127.0.0.1:6379/1')
r.ping()  # Should return True
```

### Test from Django Shell

```bash
python manage.py shell
```

```python
from django.core.cache import cache
cache.set('test_key', 'test_value', 60)
cache.get('test_key')  # Should return 'test_value'
```

### Test Redis CLI

```bash
redis-cli ping  # Should return PONG
redis-cli -n 1  # Connect to database 1
redis-cli -n 2  # Connect to database 2
```

## Fallback Behavior

If Redis is unavailable, the system automatically falls back to:

1. **Cache**: Database cache (`django.core.cache.backends.db.DatabaseCache`)
2. **Sessions**: Database sessions (`django.contrib.sessions.backends.db`)

This ensures the application continues to work even if Redis is down.

## Production Recommendations

1. **Use Redis with Password**
   ```env
   REDIS_URL=redis://:strong_password@127.0.0.1:6379/1
   ```

2. **Enable SSL/TLS** (if supported)
   ```env
   REDIS_URL=rediss://:password@host:port/db
   ```

3. **Set Secure Session Cookies**
   ```env
   SESSION_COOKIE_SECURE=True
   SESSION_COOKIE_SAMESITE=Strict
   ```

4. **Use Redis Persistence**
   - Configure Redis with AOF (Append Only File) or RDB snapshots
   - This ensures session data survives Redis restarts

5. **Monitor Redis**
   - Use `redis-cli INFO` to monitor memory usage
   - Set up alerts for memory limits
   - Monitor connection counts

## Troubleshooting

### Redis Connection Errors

1. **Check if Redis is running**
   ```bash
   redis-cli ping
   ```

2. **Check Redis logs**
   ```bash
   sudo tail -f /var/log/redis/redis-server.log
   ```

3. **Check firewall/network**
   - Ensure port 6379 is accessible
   - Check if Redis is bound to 127.0.0.1 or 0.0.0.0

### Session Issues

1. **Sessions not persisting**
   - Check `SESSION_ENGINE` setting
   - Verify Redis connection
   - Check session cookie settings

2. **Sessions expiring too quickly**
   - Adjust `SESSION_COOKIE_AGE`
   - Check `SESSION_EXPIRE_AT_BROWSER_CLOSE`

## Cache Table Creation (Fallback)

If using database cache fallback, create the cache table:

```bash
python manage.py createcachetable
```

This creates the `cache_table` in your database.

## Performance Tips

1. **Use Connection Pooling**: Already configured with max_connections=50
2. **Set Appropriate Timeouts**: Default is 300 seconds
3. **Monitor Cache Hit Rates**: Use Redis INFO command
4. **Use Key Prefixes**: Prevents key collisions (already configured)

## Additional Resources

- [Django Cache Framework](https://docs.djangoproject.com/en/4.2/topics/cache/)
- [Django Sessions](https://docs.djangoproject.com/en/4.2/topics/http/sessions/)
- [Redis Documentation](https://redis.io/documentation)
- [Redis Python Client](https://redis-py.readthedocs.io/)
