# Authentication

**Table of contents**

- [Login](#login)
- [Cache](#cache)
  - [Force login attempt](#force-login-attempt)
  - [Logout](#logout)
- [uid-key bypass](#uid-key-bypass)

## Login

With the [new version of the website](index.md#z-library-seizure) authentication is required to surf the library. To login using the email and the password of your z-library account you can use the `.login(email: str, password: str)` function:

```python
from zeniba import Zeniba

client = Zeniba().login(config.EMAIL, password.EMAIL)
```

If the client isn't logged in, it will throw a `AuthenticationError` exception.

By default the login is executed on the `https` page `singlelogin.me`, which works only as a login and status page, but is (opinionatedly) significantly faster than the onion login. To force the login with onion set the `use_onion` flag:

```python
client.login(config.EMAIL, password.EMAIL, use_onion=True)
```

## Cache

User authentication is cached after any successful `.login()`. The `key-id` of the last logged-in user is saved in `appdirs.user_cache_dir`: for example, in linux the path of the cache file is `~/.cache/zeniba`. Caching the login speeds up the whole login process and avoid being banned for too many login attempts (yes, it can happen).

```python
from zeniba import Zeniba

# When a client is created, it automatically checks for cached login keys
client = Zeniba()

if not client.is_authenticated():
    client.login(config.EMAIL, config.PASSWORD)

client.is_authenticated() # True
```

### Force login attempt

If you attempt a `login` after the client has retrieved a cached login key the login operation won't be executed. In fact, this is the same as the code above:

```python
client = Zeniba().login(config.EMAIL, config.PASSWORD)
```

To force the login attempt you can set the `force` flag to `True`:

```python
# If there is a cached login, won't attempt the new login
client.login(config.EMAIL, config.PASSWORD)

# Force the attempt
client.login(config.EMAIL, config.PASSWORD, force=True)
```

### Logout

Logout means to delete any cached logins. To do such:

```python
client.logout()
```

## `uid`-`key` bypass

If for any reason providing directly the user `uid` and `key` is preferable, you can pass them as parameters at the creation of the client. The newly created client will ignore any cached login.

```python
from zeniba import Zeniba

client = Zeniba(config.UID, config.KEY)
```

The user `uid` and `key` can be found in the cookies of the website, for example by running `document.cookie` into the browser console, which should return a string containing

```
remix_userkey=USER_KEY; remix_userid=USER_ID;
```
