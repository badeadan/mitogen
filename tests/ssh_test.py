import sys

import mitogen
import mitogen.ssh
import mitogen.utils

import unittest2

import testlib
import plain_old_module


class FakeSshTest(testlib.RouterMixin, unittest2.TestCase):
    def test_okay(self):
        context = self.router.ssh(
                hostname='hostname',
                username='mitogen__has_sudo',
                ssh_path=testlib.data_path('fakessh.py'),
        )
        #context.call(mitogen.utils.log_to_file, '/tmp/log')
        #context.call(mitogen.utils.disable_site_packages)
        self.assertEquals(3, context.call(plain_old_module.add, 1, 2))


class SshTest(testlib.DockerMixin, unittest2.TestCase):
    stream_class = mitogen.ssh.Stream

    def test_stream_name(self):
        context = self.docker_ssh(
            username='mitogen__has_sudo',
            password='has_sudo_password',
        )
        name = 'ssh.%s:%s' % (
            self.dockerized_ssh.get_host(),
            self.dockerized_ssh.port,
        )
        self.assertEquals(name, context.name)

    def test_via_stream_name(self):
        context = self.docker_ssh(
            username='mitogen__has_sudo_nopw',
            password='has_sudo_nopw_password',
        )
        sudo = self.router.sudo(via=context)

        name = 'ssh.%s:%s.sudo.root' % (
            self.dockerized_ssh.host,
            self.dockerized_ssh.port,
        )
        self.assertEquals(name, sudo.name)

    def test_password_required(self):
        try:
            context = self.docker_ssh(
                username='mitogen__has_sudo',
            )
            assert 0, 'exception not thrown'
        except mitogen.ssh.PasswordError:
            e = sys.exc_info()[1]

        self.assertEqual(e[0], self.stream_class.password_required_msg)

    def test_password_incorrect(self):
        try:
            context = self.docker_ssh(
                username='mitogen__has_sudo',
                password='badpw',
            )
            assert 0, 'exception not thrown'
        except mitogen.ssh.PasswordError:
            e = sys.exc_info()[1]

        self.assertEqual(e[0], self.stream_class.password_incorrect_msg)

    def test_password_specified(self):
        context = self.docker_ssh(
            username='mitogen__has_sudo',
            password='has_sudo_password',
        )

        self.assertEqual(
            'i-am-mitogen-test-docker-image\n',
            context.call(plain_old_module.get_sentinel_value),
        )

    def test_pubkey_required(self):
        try:
            context = self.docker_ssh(
                username='mitogen__has_sudo_pubkey',
            )
            assert 0, 'exception not thrown'
        except mitogen.ssh.PasswordError:
            e = sys.exc_info()[1]

        self.assertEqual(e[0], self.stream_class.password_required_msg)

    def test_pubkey_specified(self):
        context = self.docker_ssh(
            username='mitogen__has_sudo_pubkey',
            identity_file=testlib.data_path('docker/mitogen__has_sudo_pubkey.key'),
        )
        self.assertEqual(
            'i-am-mitogen-test-docker-image\n',
            context.call(plain_old_module.get_sentinel_value),
        )


if __name__ == '__main__':
    unittest2.main()
