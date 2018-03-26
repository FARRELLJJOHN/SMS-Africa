# Generate a custom amount of example texts and save them in a .csv

import random
import sqlite3
import csv


# Creates a SQLite database in memory
text_db = sqlite3.connect(':memory:')
print("TextGenerator.py: Database created successfully")

# Function to initialize the database
# INPUT
# 	db: Database generated in memory
def init_db(db):
	db.execute('''CREATE TABLE farmer_texts
				  (NUMBER     INTEGER     PRIMARY KEY     NOT NULL,
				   LAT        BLOB                        NOT NULL,
				   LONG       BLOB                        NOT NULL,
				   CROPS      BLOB                        NOT NULL)''')
	print("TextGenerator.py: Farmer Database initialized")

	db.execute('''CREATE TABLE market_texts
				  (NUMBER     INTEGER     PRIMARY KEY     NOT NULL,
				   LAT        BLOB                        NOT NULL,
				   LONG       BLOB                        NOT NULL,
				   CROP1      BLOB                        NOT NULL,
				   PRICE1     BLOB                        NOT NULL,
				   CROP2      BLOB,
				   PRICE2     BLOB)''')

	print("TextGenerator.py: Market Database intialized")


# Populates the database with the specified amount of random texts
# INPUT
# 	db:  Database generated in memory
#	numTexts:  Number of texts to be generated, specified by user input
def populate_farmer_db(db, numTexts):
	for x in range(numTexts):
		# Generate the random numbers to be used
		num = random.randint(1000000000, 9999999999)
		t_lat = round(random.uniform(-25.0,5.0), 6)
		t_long = round(random.uniform(10.0, 43.0), 6)

		crops_all = ["_yams", "_cassava", "_peanuts", "_maize", 
		             "_sorghum", "_millet", "_sesame", "_plantains"]

		chosen = list_to_string(random.sample(crops_all, 2))

		# Add the numbers into farmer_texts
		db.execute("INSERT INTO farmer_texts (NUMBER, LAT, LONG, CROPS) VALUES (?,?,?,?)",
			       (num, t_lat, t_long, chosen))

	print("TextGenerator.py: Database populated with farmer information")

# Populates the market_texts table with random information
# INPUT
#	db: Memory database
#	numTexts: Number of farmers in the farmer_texts table
def populate_market_db(db, numTexts):

	numMarkets = int(numTexts / 2)

	for x in range(random.randint(3, numMarkets)):
		#Generate random information
		num = random.randint(1000000000, 9999999999)
		t_lat = round(random.uniform(-25.0,5.0), 6)
		t_long = round(random.uniform(10.0, 43.0), 6)

		crops_all = ["_yams", "_cassava", "_peanuts", "_maize", 
		             "_sorghum", "_millet", "_sesame", "_plantains"]

		crop1 = list_to_string(random.sample(crops_all, 1))
		price1 = round(random.uniform(0.0, 100.0), 2)

		crop2 = list_to_string(random.sample(crops_all, 1))
		price2 = round(random.uniform(0.0, 100.0), 2)

		while crop2 == crop1:
			crop2 = list_to_string(random.sample(crops_all, 1))

		db.execute('''INSERT INTO market_texts (NUMBER, LAT, LONG, CROP1, PRICE1, CROP2, PRICE2)
					VALUES (?,?,?,?,?,?,?)''', (num, t_lat, t_long, crop1, price1, crop2, price2))

	print("TextGenerator.py: Database populated with market information")



# Outputs the generated database to the terminal
# INPUT
#	db:  Database generated in memory
def output_term(db):
	cursor_f = db.execute("SELECT * FROM 'farmer_texts'")

	print("\n  Number   |     Lat    |   Long    |       Crops")
	for row in cursor_f:
		print("{} | {:>10f} | {:>9f} | {}".format(row[0],
				 							  row[1],
				 							  row[2],
				 							  row[3]))

	cursor_m = db.execute("SELECT * FROM 'market_texts'")

	print("\n  Number   |     Lat    |   Long    |     C1     |   P1   |     C2     |   P2")
	for row in cursor_m:
		print("{} | {:>10f} | {:>9f} | {:>10} | {:>6} | {:>10} | {:>6}".format(row[0],
																		row[1],
																		row[2],
																		row[3],
																		row[4],
																		row[5],
																		row[6]))



# Outputs the generated database to a txt file
# INPUT
#	db:  Database generated in memory
def output_txt(db):
	cursor = db.execute("SELECT * FROM 'farmer_texts'")

	file = open("Tests/farmer_texts.txt", "w")

	# Loops through each row in the SQLite database and
	# writes it to the txt file
	for row in cursor:
		file.write("{}: {:f},{:f} Crops:{}\n".format(row[0],row[1],row[2],row[3]))
	file.close()

	cursor = db.execute("SELECT * FROM 'market_texts'")
	file = open("Tests/market_texts.txt", "w")

	for row in cursor:
		file.write("{}: {:f},{:f} Prices:'{}:{},{}:{}'\n".format(row[0],row[1],row[2],row[3],row[4],row[5],row[6]))
	file.close()


# Outputs the generated database to a csv file
# INPUT
# 	db:  Database generated in memory
def output_csv(db):
	cursor = db.execute("SELECT * FROM 'farmer_texts'")

	# Opens the csv file to store the data in
	with open("Tests/farmer_texts.csv", "w") as csvfile:
		file = csv.writer(csvfile, delimiter=',', quotechar='|',
												  quoting=csv.QUOTE_MINIMAL)

		for row in cursor:
			file.writerow( [row[0], row[1], row[2], row[3]] )

	cursor = db.execute("SELECT * FROM 'market_texts'")

	with open("Tests/market_texts.csv", "w") as csvfile:
		file = csv.writer(csvfile, delimiter=',', quotechar='|',
												quoting=csv.QUOTE_MINIMAL)

		for row in cursor:
			file.writerow( [row[0], row[1], row[2], row[3], row[4], row[5], row[6]])


# Helper function to convert a list of crops
# into a useable string format
# INPUT
#	crops: List of crops to convert to string
def list_to_string(crops):
	final = ""

	for item in crops:
		final += item

	return final



# ----- Main Body --------

if __name__ == '__main__':
	numObjects = input("How many sample texts would you like? ==> ")
	numObjects = int(numObjects)
	print()

	# Create database
	init_db(text_db)
	populate_farmer_db(text_db, numObjects)
	populate_market_db(text_db, numObjects)

	# Store database
	print("How would you like data stored?")
	outputFormat = input("[csv/txt/term/all]  ==> ").strip()


	if outputFormat == 'term':
		output_term(text_db)
	elif outputFormat == 'txt':
		output_txt(text_db)
	elif outputFormat == 'csv':
		output_csv(text_db)
	elif outputFormat == 'txt,csv':
		output_txt(text_db)
		output_csv(text_db)
	elif outputFormat == 'all':
		output_txt(text_db)
		output_csv(text_db)
		output_term(text_db)


	text_db.close()