#!python3
import sys
import json
import sqlite3
from pyedhrec import EDHRec

### VARS ###
scry_active = True
bulk_path='scryData/oracle.json'
db_path='scrydb.sqlite'
commanderCard = "The Ur-Dragon"

#import bulk data from scryfall
def import_bulk(bulk_path):
    with open(bulk_path) as json_data:
        data = json.load(json_data)
        json_data.close()
    return data

def start_db(db_path):
    data = import_bulk(bulk_path)
    con = sqlite3.connect(db_path)
    cursor = con.cursor()
    cursor.execute('DROP TABLE IF EXISTS card_table;')
    con.commit()
    cursor.execute('CREATE TABLE IF NOT EXISTS card_table (id INTEGER PRIMARY KEY AUTOINCREMENT, name text NOT NULL, imgurl text NOT NULL);')
    con.commit()
    for item in data:
        if not item['legalities']['brawl'] == "legal":
            continue
        if 'image_uris' not in item.keys():
            imgurl = item['card_faces'][0]['image_uris']['normal']
        else:
            imgurl = item['image_uris']['normal']

        sql = '''INSERT INTO card_table(name,imgurl)
                 VALUES(?,?) '''
        item_data = (item['name'],imgurl)
        cursor.execute(sql, item_data)
    con.commit()
    con.close()
    

def findMatches(relatives):
    con = sqlite3.connect(db_path)
    cursor = con.cursor()
    cursor.execute('SELECT * FROM card_table')
    data = cursor.fetchall()
    recList = []
    for category in relatives:
        cat1 = relatives[category]
        for i in cat1:
            for card in data:
                #print(card[1])
                if card[1] ==  i['name']:
                    recList.append(card)
    con.close()
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
    #scrydata = import_bulk(bulk_path)
    #setup edhrec api
    edhrec = EDHRec()
    #get related cards from edhrec
    relatives = edhrec.get_commander_cards(commanderCard)
    recList = findMatches(relatives)
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
    cursor = start_db(db_path)
    recList = getMatches(commanderCard)

    #return results to terminal
    for item in recList:
        print("1 "+item[1])
    if args.filename:
        writeHTML(recList, args.filename)


start_db(db_path)
if __name__ == "__main__":
    main()

