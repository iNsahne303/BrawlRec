#!python3
import sys
import json
from pyedhrec import EDHRec

### VARS ###
scry_active = True
bulk_path='scryData/oracle.json'
commanderCard = "The Ur-Dragon"

#import bulk data from scryfall
def import_bulk(bulk_path):
    with open(bulk_path) as json_data:
        data = json.load(json_data)
        json_data.close()
    return data

def findMatches(relatives, data):
    recList = []
    for category in relatives:
        cat1 = relatives[category]
        for i in cat1:
            for card in data:
                if card['name'] ==  i['name']:
                    if card['legalities']['brawl'] == 'legal':
                        recList.append(card)
    return recList

def writeHTML(recList, filename):
    filename = filename+".html"
    with open(filename, 'w') as f:
        f.writelines('<html><body><table>\n')
        for item in recList:
            line = '<tr><td>'+item['name']+'</td><td><img src="'+item['image_uris']['normal']+'"></td></tr>\n'
            f.writelines(line)
        f.writelines('</table></body></html>\n')

def getMatches(commanderCard):
    #load scryfall data
    scrydata = import_bulk(bulk_path)
    #setup edhrec api
    edhrec = EDHRec()
    #get related cards from edhrec
    relatives = edhrec.get_commander_cards(commanderCard)
    recList = findMatches(relatives, scrydata)
    return recList

def main():
    #args only for terminal use
    import argparse
    parser = argparse.ArgumentParser(description="BrawlRec, find EDHRec matches legal in Brawl for Arena")
    parser.add_argument("commander", nargs="?", help="Name of the commander card")
    parser.add_argument("-f", "--file", dest="filename", help="Path to output HTML file")
    args = parser.parse_args()
    if len(sys.argv) <= 1:
        parser.print_help()
        sys.exit(1)
    if not args.commander:
        print("Commander required!")
        parser.print_help()
        sys.exit(1)
    
    commanderCard = args.commander
    recList = getMatches(commanderCard)

    #return results to terminal
    for item in recList:
        print("1 "+item['name'])
    if args.filename:
        writeHTML(recList, args.filename)

if __name__ == "__main__":
    main()

