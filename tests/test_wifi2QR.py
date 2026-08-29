import importlib
import sys
import types

import pytest


@pytest.fixture
def wifi_module(monkeypatch):
    fake_module = types.ModuleType("WiFiQRGen")

    class FakeWifiSecurity:
        WEP = "WEP"
        WPA = "WPA"
        NONE = "NONE"

    class FakeImage:
        last_saved_path = None

        def save(self, path):
            FakeImage.last_saved_path = path

    class FakeWifiNetworkSettings:
        last_kwargs = None

        def __init__(self, **kwargs):
            FakeWifiNetworkSettings.last_kwargs = kwargs

        def generate_qrcode(self):
            return FakeImage()

    fake_module.WifiSecurity = FakeWifiSecurity
    fake_module.WifiNetworkSettings = FakeWifiNetworkSettings

    monkeypatch.setitem(sys.modules, "WiFiQRGen", fake_module)
    monkeypatch.syspath_prepend("/home/runner/work/WifiQRGenerator/WifiQRGenerator/src")

    wifi2qr = importlib.import_module("wifi2QR")
    wifi2qr = importlib.reload(wifi2qr)

    return wifi2qr, FakeWifiSecurity, FakeWifiNetworkSettings, FakeImage


def test_security_factory_maps_values(wifi_module):
    wifi2qr, fake_security, *_ = wifi_module

    assert wifi2qr.securityFactory("WEP") == fake_security.WEP
    assert wifi2qr.securityFactory("WPA") == fake_security.WPA
    assert wifi2qr.securityFactory("nopass") == fake_security.NONE


def test_parse_args_defaults(wifi_module):
    wifi2qr, fake_security, *_ = wifi_module

    settings = wifi2qr.parse_args(["-w", "HomeWifi"])

    assert settings["ssid"] == "HomeWifi"
    assert settings["password"] is None
    assert settings["security"] == fake_security.NONE
    assert settings["hidden"] is False
    assert settings["output_file"] == "./qr.png"


def test_parse_args_with_all_flags(wifi_module):
    wifi2qr, fake_security, *_ = wifi_module

    settings = wifi2qr.parse_args(["-w", "HomeWifi", "-p", "1234", "-t", "WPA", "-o", "-f", "qr.png"])

    assert settings["ssid"] == "HomeWifi"
    assert settings["password"] == "1234"
    assert settings["security"] == fake_security.WPA
    assert settings["hidden"] is True
    assert settings["output_file"] == "qr.png"


def test_parse_args_requires_wifi_name(wifi_module):
    wifi2qr, *_ = wifi_module

    with pytest.raises(ValueError, match="Falta por informar el nombre de la wifi"):
        wifi2qr.parse_args([])


def test_main_generates_qr_file(wifi_module):
    wifi2qr, _, fake_settings, fake_image = wifi_module

    result = wifi2qr.main(["-w", "Office", "-p", "abcd", "-t", "WPA", "-f", "out.png"])

    assert result == 0
    assert fake_settings.last_kwargs["ssid"] == "Office"
    assert fake_settings.last_kwargs["security"] == "WPA"
    assert fake_image.last_saved_path == "out.png"


def test_main_help_returns_zero_and_prints_usage(wifi_module, capsys):
    wifi2qr, *_ = wifi_module

    result = wifi2qr.main(["-h"])

    assert result == 0
    out = capsys.readouterr().out
    assert "wifi2QR -w <wifi_name>" in out
