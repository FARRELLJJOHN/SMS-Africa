import csv
import sqlite3



db = sqlite3.connect('data/marketdb')
c = db.cursor()


def db_init(c):
	c.execute('''
		CREATE TABLE IF NOT EXISTS MARKET_DATA
		(NUMBER    INTEGER  PRIMARY KEY  NOT NULL,
		 M_LAT     BLOB                  NOT NULL,
		 M_LONG    BLOB                  NOT NULL,
		 CASSAVA   TEXT    DEFAULT '0',
		 DATE1     DATE    DEFAULT 0,
		 PLANTAINS TEXT    DEFAULT '0',
		 DATE2	   DATE    DEFAULT 0,
		 PEANUTS   TEXT    DEFAULT '0',
		 DATE3     DATE    DEFAULT 0,
		 MAIZE     TEXT    DEFAULT '0',
		 DATE4     DATE    DEFAULT 0,
		 SORGHUM   TEXT    DEFAULT '0',
		 DATE5     DATE    DEFAULT 0,
		 YAMS      TEXT    DEFAULT '0',
		 DATE6     DATE    DEFAULT 0,
		 SESAME    TEXT    DEFAULT '0',
		 DATE7     DATE    DEFAULT 0,
		 MILLET    TEXT    DEFAULT '0',
		 DATE8     DATE    DEFAULT 0)
		''')

	print("db_init.py: Market Database initialized")

	c.execute('''
		CREATE TABLE IF NOT EXISTS FARMER_DATA
		(NUMBER    INTEGER  PRIMARY KEY  NOT NULL,
		 F_LAT     BLOB                  NOT NULL,
		 F_LONG    BLOB                  NOT NULL,
		 CASSAVA   INTEGER,
		 PLANTAINS INTEGER,
		 PEANUTS   INTEGER,
		 MAIZE     INTEGER,
		 SORGHUM   INTEGER,
		 YAMS      INTEGER,
		 SESAME    INTEGER,
		 MILLET    INTEGER)
		''')
	print("db_init.py: Farmer Database initialized", end="\n\n")


def db_populate(c):

	# Read in data from market_texts.csv
	with open('Tests/market_texts.csv', 'r') as csvfile:
		reader = csv.reader(csvfile, delimiter=',', quotechar='|')
		# row[0] = number   row[1] = lat    row[2] = long
		# row[3] = crop1    row[4] = price1
		# row[5] = crop2    row[6] = price2
		for row in reader:
			# print(len(row))
			# print(row)
			c.execute('''
			 	INSERT INTO MARKET_DATA
			    (NUMBER, M_LAT, M_LONG, %s) values (?, ?, ?, ?)
			 	''' % (row[3].strip('_').upper()), (row[0], row[1], row[2], row[4]))
			c.execute('''
			 	UPDATE MARKET_DATA SET %s = %s WHERE NUMBER = %s
			 	''' % (row[5].strip('_').upper(), row[6], row[0]))

	# Read in data from farmer_texts.csv
	with open('Tests/farmer_texts.csv', 'r') as csvfile:
		reader = csv.reader(csvfile, delimiter=',', quotechar='|')

		for row in reader:
			crops = row[3].split('_')
			crops.pop(0)

			c.execute('''
				INSERT INTO FARMER_DATA
				(NUMBER, F_LAT, F_LONG, %s) values (?,?,?,?)
				''' % (crops[0].upper() ), (row[0], row[1], row[2], 1))
			c.execute('''
				UPDATE FARMER_DATA SET %s = %s WHERE NUMBER = %s
				''' % (crops[1].upper(), 1, row[0]))

	db.commit()


def db_print(c):
	print("  NUMBER        LAT     LONG      CASSAVA|DATE  \
PLANTAIN|DATE   PEANUTS|DATE   MAIZE|DATE  \
SORGHUM|DATE   YAM|DATE   SESAME|DATE  MILLET|DATE")
	for row in c:
		print("{} {:>10} {:>9} {:>9}|{} {:>12}|{} {:>12}|{} {:>10}|{} {:>11}|{} {:>8}|{} {:>11}|{} {:>10}|{}".format(
				row[0], row[1], row[2], row[3], row[4], row[5], row[6],
				row[7], row[8], row[9], row[10], row[11], row[12], row[13],
				row[14], row[15], row[16], row[17], row[18]))



if __name__ == "__main__":

	db_init(c)

	db_populate(c)

	market_reader = c.execute("SELECT * FROM MARKET_DATA")

	db_print(market_reader)

	db.close()
