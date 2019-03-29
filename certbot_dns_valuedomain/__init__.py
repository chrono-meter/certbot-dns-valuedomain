import time
import subprocess
import logging
import certbot.interfaces, certbot.errors, certbot.plugins.dns_common
import zope.interface
import requests
from bs4 import BeautifulSoup


logger = logging.getLogger(__name__)


class ValueDomain(object):

    def __init__(self):
        self.session = requests.Session()

    def login(self, username, password):
        response = self.session.post('https://www.value-domain.com/login.php', data={
            'username': username,
            'password': password,
            'action': 'login2',
            'location': '',
            # 'submit': 'ログイン',
        })
        assert 'var is_login = 1;' in response.text

    def logout(self):
        self.session.get('https://www.value-domain.com/logout.php')

    def _moddns(self, **kwargs):
        return self.session.get('https://www.value-domain.com/moddns.php', **kwargs)

    def get_dns_records(self, domain):
        response = self._moddns(params={'action': 'moddns2', 'domainname': domain})
        soup = BeautifulSoup(response.text, features='html.parser')
        form = soup.find('form', attrs={'name': 'formMAIN'})

        return form.find('textarea', attrs={'name': 'records'}).contents[0]

    def set_dns_records(self, domain, records):
        response = self._moddns(params={'action': 'moddns2', 'domainname': domain})
        soup = BeautifulSoup(response.text, features='html.parser')
        form = soup.find('form', attrs={'name': 'formMAIN'})

        data = {}
        for el in form.find_all('input'):
            data[el.attrs['name']] = el.attrs['value']
        data['records'] = records

        self.session.post(requests.compat.urljoin(response.url, form.attrs['action']), data=data)


@zope.interface.implementer(certbot.interfaces.IAuthenticator)
@zope.interface.provider(certbot.interfaces.IPluginFactory)
class Authenticator(certbot.plugins.dns_common.DNSAuthenticator):
    """DNS Authenticator for value-domain.
    """

    description = 'Obtain certificates using a DNS TXT record (if you are using value-domain for DNS).'

    def __init__(self, *args, **kwargs):
        super(Authenticator, self).__init__(*args, **kwargs)
        self.credentials = None
        self.api = ValueDomain()

    @classmethod
    def add_parser_arguments(cls, add):  # pylint: disable=arguments-differ
        super(Authenticator, cls).add_parser_arguments(add)
        # https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.add_argument
        add('credentials',
            # default=os.path.join(certbot.compat.misc.get_default_folder('config'), 'value-domain.ini'),
            metavar='PATH',
            default='/etc/letsencrypt/valuedomain.ini',
            help='Path to credentials INI file.')
        add('max-propagation-seconds',
            type=int,
            metavar='SECONDS',
            default=3600,
            help='The number of maximum seconds to watch for DNS to propagate before asking the ACME server '
                 'to verify the DNS record.')

    def more_info(self):  # pylint: disable=missing-docstring,no-self-use
        return 'This plugin configures a DNS TXT record to respond to a dns-01 challenge using ' + \
                'value-domain web.'

    def _setup_credentials(self):  # pylint: disable=missing-docstring
        self.credentials = self._configure_credentials(
            'credentials',
            'value-domain credentials INI file',
            {
                'username': 'Username of the value-domain account.',
                'password': 'Password of the value-domain account.',
            }
        )

        self.api.login(self.credentials.conf('username'), self.credentials.conf('password'))

    def _perform(self, domain, validation_name, validation):  # pylint: disable=missing-docstring
        records = self.api.get_dns_records(domain)
        self.api.set_dns_records(
            domain, records + '\n' + self._build_record_string(domain, validation_name, validation))

        t = time.time()
        while (time.time() - t) < self.conf('max-propagation-seconds'):

            if validation in subprocess.run(['nslookup', '-type=txt', validation_name], stdout=subprocess.PIPE,
                                            stderr=subprocess.DEVNULL, universal_newlines=True).stdout:
                break

            time.sleep(self.conf('propagation-seconds'))

        else:
            raise certbot.errors.PluginError('max-propagation-seconds is exceeded.')

    def _cleanup(self, domain, validation_name, validation):  # pylint: disable=missing-docstring
        records = self.api.get_dns_records(domain).splitlines()
        record = self._build_record_string(domain, validation_name, validation)

        try:
            records.remove(record)
            self.api.set_dns_records(domain, '\n'.join(records))
        except LookupError:
            logger.exception('Failed to cleanup, validation record (%s) is not found.', record)

    def _build_record_string(self, domain, validation_name, validation):  # pylint: disable=missing-docstring
        assert validation_name.endswith('.' + domain)
        subdomain = validation_name[:-(1 + len(domain))]

        return 'txt %s %s' % (subdomain, validation)
