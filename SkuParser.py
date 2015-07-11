# #
# © DianaCorp 2015
##


import logging
import time
import csv
import glob


##
# Brand: Peuterey
# This script reads the new season files (in CSV format) and outputs the prepared CSV files to import in Magento
# Fix the kids SKU issue
# Set the new categories
##

oldFiles = "old/*.csv"
newFiles = "new/"
season = "SS15"

jack_list = ['giubbotti', 'cappotti/trench', 'gilet']
acc_list = ['sciarpe', 'guanti', 'cappelli', 'cinture', 'borse', 'portachiavi', 'portafogli']
knit_list = ['maglieria calata', 'maglieria tagliata', 'felpe']
pant_list = ['bermuda', 'pantaloni']
tshirt_list = ['t-shirts', 'polo']


def top_category(c):
    if "donna" in c:
        return "women"
    elif "uomo" in c:
        return "men"
    elif "baby" in c:
        return "baby"
    else:
        return "kid"


def sub_category(s):
    if any(s in knit for knit in knit_list):
        return "knitwear"
    elif any(s in jack for jack in jack_list):
        return "jackets"
    elif "camicie" in s:
        return "shirts"
    elif any(s in pant for pant in pant_list):
        return "pants"
    elif any(s in tshirt for tshirt in tshirt_list):
        return "t-shirts"
    elif any(s in acc for acc in acc_list):
        return "accessories"
    elif "tuta" in s:
        return "jumpsuits"
    elif "abiti" in s:
        return "dresses"
    elif "gonne" in s:
        return "skirts"
    elif "blazer/pantalone" in s:
        return "babysuits"
    else:
        return "other"


def new_category(c, s):
    c = top_category(c)
    s = sub_category(s)
    return season + "/" + c + "/" + s

for oldFile in glob.glob(oldFiles):
    try:
        with open(oldFile) as csvFile:
            readCSV = csv.reader(csvFile, delimiter=',')
            header = readCSV.__next__()
            header[72] = "size"

            try:
                with open('new'+oldFile[4:], 'w', newline='') as fp:
                    a = csv.writer(fp, delimiter=',')
                    a.writerow(header)

                    temp = ""
                    for row in readCSV:
                        signal = False
                        sku = row[0]

                        if row[2] != "":
                            row[2] = "peuterey"

                        if row[6] != "":
                            row[6] = "usa"

                        if "configurable" in oldFile:
                            if sku[:3] in ("PKB", "PKK"):
                                if sku[:-1] == temp:
                                    for i in range(0,64):
                                        row[i] = ""

                                else:
                                    row[0] = sku[:-1]
                                    temp = row[0]

                            if row[4] != "":
                                row[4] = new_category(row[4], row[40])

                            if row[65] == "":
                                signal = True

                            if row[66] == "taglia":
                                row[66] = "size"

                        if signal == False:
                            a.writerow(row)

                print("File "+oldFile[4:]+" is processed.")
                fp.close()

            except IOError:
                print("\nSomething went wrong while writing the new file")
                logging.basicConfig(filename='Error.log', level=logging.DEBUG)
                logging.debug('Something went wrong while writing the new file!')

        logging.basicConfig(filename='Success.log', level=logging.DEBUG)
        logging.debug('File: new'+oldFile[4:]+' was created')
        csvFile.close()

    except IOError:
        print("\nSomething big went wrong!")
        time.sleep(10)
        logging.basicConfig(filename='Error.log', level=logging.DEBUG)
        logging.debug('Something big went wrong!')
