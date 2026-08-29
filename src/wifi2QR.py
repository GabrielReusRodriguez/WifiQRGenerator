#!/usr/bin/env python3

import getopt
import sys

PROGRAM_NAME = "wifi2QR"
USAGE = f"{PROGRAM_NAME} -w <wifi_name> -p <wifi_pass> -t <wifi_Authentication_Type> [WEP|WPA|nopass] -o -f <Ruta_qr>"


def securityFactory(arg: str):
    from WiFiQRGen import WifiSecurity

    if arg == "WEP":
        return WifiSecurity.WEP
    if arg == "WPA":
        return WifiSecurity.WPA
    return WifiSecurity.NONE


def parse_args(argv):
    wifi_name = None
    wifi_pass = None
    output_file = "./qr.png"
    wifi_auth_type = None
    wifi_hidden = False

    try:
        opts, _ = getopt.getopt(
            argv,
            "hw:p:t:of:",
            ["wifiName=", "wifiPass=", "wifiAuth=", "wifiHidden=", "oFile="],
        )
    except getopt.GetoptError as exc:
        raise ValueError(USAGE) from exc

    for opt, arg in opts:
        if opt == "-h":
            raise SystemExit(0)
        if opt in ("-w", "--wifiName"):
            wifi_name = arg
        elif opt in ("-p", "--wifiPass"):
            wifi_pass = arg
        elif opt in ("-t", "--wifiAuth"):
            wifi_auth_type = securityFactory(arg)
        elif opt in ("-o", "--wifiHidden"):
            wifi_hidden = True
        elif opt in ("-f", "--oFile"):
            output_file = arg

    if wifi_name is None:
        raise ValueError("Error - Falta por informar el nombre de la wifi")

    if wifi_auth_type is None or wifi_pass is None:
        wifi_auth_type = securityFactory("nopass")

    return {
        "ssid": wifi_name,
        "password": wifi_pass,
        "security": wifi_auth_type,
        "hidden": wifi_hidden,
        "output_file": output_file,
    }


def generate_qr(settings):
    from WiFiQRGen import WifiNetworkSettings

    wifi_settings = WifiNetworkSettings(
        ssid=settings["ssid"],
        security=settings["security"],
        hidden=settings["hidden"],
        **{"password": settings["password"]},
    )
    qr_image = wifi_settings.generate_qrcode()
    qr_image.save(settings["output_file"])


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    try:
        settings = parse_args(argv)
    except SystemExit:
        print(USAGE)
        return 0
    except ValueError as exc:
        print(str(exc))
        if str(exc) == USAGE:
            return 2
        return 1

    generate_qr(settings)
    return 0


if __name__ == "__main__":
    sys.exit(main())
