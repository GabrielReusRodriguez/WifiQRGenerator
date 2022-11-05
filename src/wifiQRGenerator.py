#!/usr/bin/env python3

import wifi_qrcode_generator as qr
import sys, getopt

def main(argv):
 
    wifi_name = None
    wifi_pass = None
    outputFile = None
    wifi_auth_Type = None
    wifi_hidden = False

#SSID: MLP22

    try:
        #opts, args = getopt.getopt(argv,"hw:p:t:o:",["ifile=","ofile="])
        opts, args = getopt.getopt(argv,"hw:p:t:of:",["wifiName=","wifiPass=","wifiAuth=","wifiHidden=","oFile="])
    except getopt.GetoptError:
        print ("wifiQRGenerator.py -w <wifi_name> -p <wifi_pass> -t <wifi_Authentication_Type> [WEP|WPA|nopass] -f <Ruta_qr>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ("wifiQRGenerator.py -w <wifi_name> -p <wifi_pass> -t <wifi_Authentication_Type> [WEP|WPA|nopass] -o -f <Ruta_qr>")
            sys.exit()
        elif opt in ("-w", "--wifiName"):
            wifi_name = arg
        elif opt in ("-p", "--wifiPass"):
            #WPA, WEP, nopass
            wifi_pass = arg
        elif opt in ("-t","--wifiAuth"):
            wifi_auth_Type = arg
        elif opt in ("-o","--wifiHidden"):
            wifi_hidden = True
        elif opt in ("-f","--oFile"):
            outputFile = arg


    if ( wifi_auth_Type is None):
        wifi_auth_Type = "nopass" # WEP
    if ( wifi_name is None ):
        print ("Falta por informar el nombre de la wifi")
        sys.exit()
    if ( wifi_pass is None ):
            wifi_auth_Type = "nopass"
    if ( outputFile is None ):
        outputFile = "./qr.png"


    qrImage = qr.wifi_qrcode(wifi_name, wifi_hidden, wifi_auth_Type,wifi_pass)
    qrImage.save(outputFile)


if __name__ == "__main__":
   main(sys.argv[1:])
