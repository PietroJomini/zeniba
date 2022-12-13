# Config

**Table of contents**

- [TOR proxy](config.md#tor-proxy)
- [Endpoints](config.md#endpoints)

## TOR proxy

Since [z-library domains have been seized by UPS](index.md#z-library-seizure) , now the website is only accessible through tor. Installing / setting up the tor proxies is hence left as an exercise for the reader.

The only requirement as of Zeniba is to modify them if they differ from the default ones, which are:

```toml
[net.onion.proxies]
http = "socks5h://127.0.0.1:9150"
https = "socks5h://127.0.0.1:9150"
```

## Endpoints

The default onion endpoints are:

| key     | endpoint                                                               |
| ------- | ---------------------------------------------------------------------- |
| login   | http://loginzlib2vrak5zzpcocc3ouizykn6k5qecgj2tzlnab5wcbqhembyd.onion/ |
| lybrary | http://bookszlibb74ugqojhzhg2a63w5i2atv5bqarulgczawnbmsb6s6qead.onion3 |

They can be modified in `config/config.toml`.
