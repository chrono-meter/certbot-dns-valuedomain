# How to install

```sh
$ sudo pip install certbot-dns-valuedomain

...

$ certbot plugins

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
* certbot-dns-valuedomain:dns
Description: Obtain certificates using a DNS TXT record (if you are using
value-domain for DNS).
Interfaces: IAuthenticator, IPlugin
Entry point: dns = certbot_dns_valuedomain:Authenticator

...

```


# How to use

```sh
$ cat << EOF | sudo tee /etc/letsencrypt/valuedomain.ini
certbot_dns_valuedomain:dns_username = YOUR_VALUEDOMAIN_USERNAME
certbot_dns_valuedomain:dns_password = YOUR_VALUEDOMAIN_PASSWORD
EOF

...

$ sudo chmod 600 /etc/letsencrypt/valuedomain.ini

...

$ sudo certbot certonly --authenticator certbot-dns-valuedomain:dns --domain example.com --domain *.example.com --manual-public-ip-logging-ok --preferred-challenges dns-01

...
```


# Options

```sh
$ certbot --help certbot-dns-valuedomain:dns
usage:
  certbot [SUBCOMMAND] [options] [-d DOMAIN] [-d DOMAIN] ...

Certbot can obtain and install HTTPS/TLS/SSL certificates.  By default,
it will attempt to use a webserver both for obtaining and installing the
certificate.

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG_FILE, --config CONFIG_FILE
                        path to config file (default: /etc/letsencrypt/cli.ini
                        and ~/.config/letsencrypt/cli.ini)

certbot-dns-valuedomain:dns:
  Obtain certificates using a DNS TXT record (if you are using value-domain
  for DNS).

  --certbot-dns-valuedomain:dns-propagation-seconds CERTBOT_DNS_VALUEDOMAIN:DNS_PROPAGATION_SECONDS
                        The number of seconds to wait for DNS to propagate
                        before asking the ACME server to verify the DNS
                        record. (default: 10)
  --certbot-dns-valuedomain:dns-credentials PATH
                        Path to credentials INI file. (default:
                        /etc/letsencrypt/valuedomain.ini)
  --certbot-dns-valuedomain:dns-max-propagation-seconds SECONDS
                        The number of maximum seconds to watch for DNS to
                        propagate before asking the ACME server to verify the
                        DNS record. (default: 3600)
```

# Links
 * https://certbot.eff.org/docs/using.html#certbot-command-line-options
 * https://github.com/certbot/certbot/tree/master/certbot-dns-sakuracloud
 * https://github.com/free2er/certbot-regru/
