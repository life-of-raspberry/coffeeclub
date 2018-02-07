#!/usr/bin/python

import os, sys
import ast
import signal
import json
import argparse
import subprocess
import time

try:
    #if os.path.isfile("main.pid"):
     #   file = open("main.pid","r")
      #  pid = file.read()
       # try:
        #    os.kill(int(pid),signal.SIGKILL)
         #   print "Main process stopped"
       # except:
        #    pass

    stop = open("stop.txt","w")
    stop.write("1")
    stop.close()
    time.sleep(2)

    # second try
    parser = argparse.ArgumentParser()
    parser.add_argument('strings',metavar='str',type=str,nargs=3,
       help='Kndnr Vorname Nachname')
    args = parser.parse_args()
    print args.strings
    arg = []
    arg.append(args.strings)

    #arg = []
    #jj = 1
    #while jj < len(sys.argv):
    #    arg.append(ast.literal_eval(sys.argv[jj]))
    #    jj += 1

    cust_file = open('customer_list','r')
    customer_dict = json.loads(cust_file.read())
    cust_file.close()

    for ii in arg:
        assert len(ii)==3, "Incorrect Input. Try ID Vorname Nachname"
        for key in customer_dict:
            if customer_dict[key]["Kdnr"] == int(ii[0]):
                customer_dict[key]["Vorname"] = unicode(ii[1])
                customer_dict[key]["Nachname"] = unicode(ii[2])
                print "Updated Name of ID %s to %s %s" % (ii[0],ii[1],ii[2])

    fout = open('customer_list','w')
    json.dump(customer_dict, fout,indent=True)

finally:
    stop = open("stop.txt","w")
    stop.write("0")
    stop.close

