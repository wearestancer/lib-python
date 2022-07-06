"""Test device object"""

import pytest

from stancer import Device
from stancer.core import AbstractObject
from stancer.exceptions import InvalidIpAddressError
from stancer.exceptions import InvalidPortError
from .TestHelper import TestHelper


class TestDevice(TestHelper):
    def test_class(self):
        assert issubclass(Device, AbstractObject)

    def test_city(self):
        obj = Device()
        city = self.random_string(10)

        assert obj.city is None

        obj.city = city

        assert obj.city == city
        assert obj.to_json().find('"city":"{}"'.format(city)) > 0

    def test_country(self):
        obj = Device()
        country = self.random_string(10)

        assert obj.country is None

        obj.country = country

        assert obj.country == country
        assert obj.to_json().find('"country":"{}"'.format(country)) > 0

    def test_http_accept(self):
        obj = Device()
        http_accept = self.random_string(10)

        assert obj.http_accept is None

        obj.http_accept = http_accept

        assert obj.http_accept == http_accept
        assert obj.to_json().find('"http_accept":"{}"'.format(http_accept)) > 0

    def test_hydrate_from_env(self, monkeypatch):
        obj = Device()

        accept = self.random_string(100)
        agent = self.random_string(100)
        ip = '.'.join([str(self.random_integer(1, 254)) for _ in range(4)])
        languages = self.random_string(32)
        port = self.random_integer(1, 65535)

        monkeypatch.setenv('SERVER_ADDR', ip)
        monkeypatch.setenv('SERVER_PORT', str(port))
        monkeypatch.setenv('HTTP_ACCEPT', accept)
        monkeypatch.setenv('HTTP_ACCEPT_LANGUAGE', languages)
        monkeypatch.setenv('HTTP_USER_AGENT', agent)

        assert obj.to_json() == '{}'
        assert obj.hydrate_from_env() == obj

        exported = obj.to_json()

        assert exported.find('"ip":"{}"'.format(ip)) > 0
        assert exported.find('"port":{}'.format(port)) > 0
        assert exported.find('"http_accept":"{}"'.format(accept)) > 0
        assert exported.find('"languages":"{}"'.format(languages)) > 0
        assert exported.find('"user_agent":"{}"'.format(agent)) > 0

        # Assert a valid IP address is mandatory
        monkeypatch.delenv('SERVER_ADDR', raising=False)

        with pytest.raises(InvalidIpAddressError):
            Device().hydrate_from_env()

        monkeypatch.setenv('SERVER_ADDR', ip)

        # Assert a valid port is mandatory
        monkeypatch.delenv('SERVER_PORT', raising=False)

        with pytest.raises(InvalidPortError):
            Device().hydrate_from_env()

        monkeypatch.setenv('SERVER_PORT', str(port))

        # Will keep initial values
        obj = Device()

        accept = self.random_string(100)
        agent = self.random_string(100)
        ip = '.'.join([str(self.random_integer(1, 254)) for _ in range(4)])
        languages = self.random_string(32)
        port = self.random_integer(1, 65535)

        obj.http_accept = accept
        obj.ip = ip
        obj.languages = languages
        obj.port = port
        obj.user_agent = agent

        monkeypatch.setenv('SERVER_ADDR', '.'.join([str(self.random_integer(1, 254)) for _ in range(4)]))
        monkeypatch.setenv('SERVER_PORT', str(self.random_integer(1, 65535)))
        monkeypatch.setenv('HTTP_ACCEPT', self.random_string(100))
        monkeypatch.setenv('HTTP_ACCEPT_LANGUAGE', self.random_string(32))
        monkeypatch.setenv('HTTP_USER_AGENT', self.random_string(100))

        exported = obj.to_json()

        assert exported.find('"ip":"{}"'.format(ip)) > 0
        assert exported.find('"port":{}'.format(port)) > 0
        assert exported.find('"http_accept":"{}"'.format(accept)) > 0
        assert exported.find('"languages":"{}"'.format(languages)) > 0
        assert exported.find('"user_agent":"{}"'.format(agent)) > 0

        assert obj.hydrate_from_env() == obj

        exported = obj.to_json()

        assert exported.find('"ip":"{}"'.format(ip)) > 0
        assert exported.find('"port":{}'.format(port)) > 0
        assert exported.find('"http_accept":"{}"'.format(accept)) > 0
        assert exported.find('"languages":"{}"'.format(languages)) > 0
        assert exported.find('"user_agent":"{}"'.format(agent)) > 0

    def test_ip(self):
        obj = Device()

        assert obj.ip is None

        with pytest.raises(InvalidIpAddressError):
            obj.ip = self.random_string(10)

        for ip in self.ip_provider():
            obj.ip = ip

            assert obj.ip == ip
            assert obj.to_json().find('"ip":"{}"'.format(ip)) > 0

    def test_languages(self):
        obj = Device()
        languages = self.random_string(10)

        assert obj.languages is None

        obj.languages = languages

        assert obj.languages == languages
        assert obj.to_json().find('"languages":"{}"'.format(languages)) > 0

    def test_port(self):
        obj = Device()
        port = self.random_integer(1, 65534)

        assert obj.port is None

        obj.port = port

        assert obj.port == port
        assert obj.to_json().find('"port":{}'.format(port)) > 0

        with pytest.raises(InvalidPortError):
            obj.port = self.random_integer(65536, 70000)

    def test_user_agent(self):
        obj = Device()
        user_agent = self.random_string(10)

        assert obj.user_agent is None

        obj.user_agent = user_agent

        assert obj.user_agent == user_agent
        assert obj.to_json().find('"user_agent":"{}"'.format(user_agent)) > 0
