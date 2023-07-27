from io import StringIO
import unittest.mock
import responses
from responses import GET
import requests

import my_public_ip

EXIT_SUCCESS = 0
EXIT_FAILURE = 1


class TestMyPublicIp(unittest.TestCase):

    def setUp(self) -> None:
        self.responses = responses.RequestsMock()
        self.responses.start()
        self.http_bin_org = my_public_ip.HttpBinOrg()
        self.url_ip = f"{self.http_bin_org.BASE_URL}/ip"

    def tearDown(self) -> None:
        self.addCleanup(self.responses.stop)
        self.addCleanup(self.responses.reset)

    def test_ip_return_ip(self):
        """Must return the correct ip address"""
        self.responses.add(method=GET, url=self.url_ip, body='{"origin": "192.168.0.1"}', status=200)
        self.assertEqual("192.168.0.1", self.http_bin_org.ip())

    def test_ip_invalid_response_from_host(self):
        """Inform about invalid responses from host"""
        err_msg = "Invalid response from host"
        self.responses.add(method=GET, url=self.url_ip, body='{}', status=200)
        self.assertEqual(err_msg, self.http_bin_org.ip())

        self.responses.add(method=GET, url=self.url_ip, body='', status=200)
        self.assertEqual(err_msg, self.http_bin_org.ip())

    def test_ip_raise_http_error_exception(self):
        """Must raise HTTPError exception on HTTP error responses"""
        self.responses.add(method=GET, url=self.url_ip, body='', status=404)
        self.assertRaises(requests.HTTPError, self.http_bin_org.ip)

        self.responses.add(method=GET, url=self.url_ip, body='', status=500)
        self.assertRaises(requests.HTTPError, self.http_bin_org.ip)

    @unittest.mock.patch('sys.stdout', new_callable=StringIO)
    def test_main_stdout_and_exit_code(self, stdout):
        """Must provide correct output to stdout and return correct exit code to the environment"""
        self.responses.add(method=GET, url=self.url_ip, body='{"origin": "192.168.0.1"}', status=200)
        with self.assertRaises(SystemExit) as cm:
            my_public_ip.main()
        self.assertEqual(EXIT_SUCCESS, cm.exception.code)
        self.assertEqual("192.168.0.1\n", stdout.getvalue())

        self.responses.add(method=GET, url=self.url_ip, body='', status=404)
        with self.assertRaises(SystemExit) as cm:
            my_public_ip.main()
        self.assertEqual(EXIT_FAILURE, cm.exception.code)


if __name__ == '__main__':
    unittest.main()
