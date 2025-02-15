#!/usr/bin/env python3

#import wifi_qrcode_generator as qr
from WiFiQRGen import WifiSecurity, WifiEapMethod, WifiPhase2Auth, WifiNetworkSettings
import sys, getopt

#Constants....
PROGRAM_NAME ="wifi2QR" 

#Inits....
wifi_name = None
wifi_pass = None
outputFile = None
wifi_auth_Type = None
wifi_hidden = False

argv = sys.argv[1:]
#print (str(argv))

#Functions...
def securityFactory(arg: str):
	if arg == "WEP":
		return WifiSecurity.WEP
	elif arg == "WPA":
		return WifiSecurity.WPA
	else:
		return WifiSecurity.NONE


#main...
try:
	#opts, args = getopt.getopt(argv,"hw:p:t:o:",["ifile=","ofile="])
	opts, args = getopt.getopt(argv,"hw:p:t:of:",["wifiName=","wifiPass=","wifiAuth=","wifiHidden=","oFile="])
except getopt.GetoptError:
		#print ("wifiQRGenerator.py -w <wifi_name> -p <wifi_pass> -t <wifi_Authentication_Type> [WEP|WPA|nopass] -f <Ruta_qr>")
		print (f"{PROGRAM_NAME} -w <wifi_name> -p <wifi_pass> -t <wifi_Authentication_Type> [WEP|WPA|nopass] -f <Ruta_qr>")
		sys.exit(2)
for opt, arg in opts:
	if opt == '-h':
		print (f"{PROGRAM_NAME} -w <wifi_name> -p <wifi_pass> -t <wifi_Authentication_Type> [WEP|WPA|nopass] -o -f <Ruta_qr>")
		sys.exit()
	elif opt in ("-w", "--wifiName"):
		wifi_name = arg
	elif opt in ("-p", "--wifiPass"):
		#WPA, WEP, nopass
		wifi_pass = arg
	elif opt in ("-t","--wifiAuth"):
		wifi_auth_Type = securityFactory(arg)
	elif opt in ("-o","--wifiHidden"):
		wifi_hidden = True
	elif opt in ("-f","--oFile"):
		outputFile = arg

if ( wifi_auth_Type is None):
	wifi_auth_Type = "nopass" # WEP
if ( wifi_name is None ):
	print (f"Error - Falta por informar el nombre de la wifi")
	sys.exit()
if ( wifi_pass is None ):
	wifi_auth_Type = WifiSecurity.NONE
if ( outputFile is None ):
	outputFile = "./qr.png"

wifi_settings = WifiNetworkSettings(
	ssid		= wifi_name,
	password	= wifi_pass,
	security 	= wifi_auth_Type,
	#security=WifiSecurity.WPA2,
	#eap_method=WifiEapMethod.PEAP,
	#phase_2_auth=WifiPhase2Auth.MSCHAPV2,
	hidden		= wifi_hidden
	#identity="MyUsername"
)
#qrImage =  wifi_settings.generate_qrcode('path/to/logo.png')
qrImage =  wifi_settings.generate_qrcode()
qrImage.save(outputFile)
