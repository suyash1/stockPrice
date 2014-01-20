#Author : Suyash Kant Srivastava
'''
Maximum share price problem

the following script is designed to run test case for displaying the max share
price for a company in a particular year and month

also, if a company has same maximum share price in 1 or more years, both years 
with maximum share prices are populated

'''

import unittest
from os import remove
from csv import DictReader

def MaxSharePrice(csvfile):
	'''
	Returns a dictionary with company name as key and their max share price.
	value in the dictionary a list of list(s) containins share price, month(s) and 
	year(s) in which share price was maximum
	for example:
	{
		'Microsoft': [[77, ' Oct', '2013'], [77, ' Dec', '2013']], 
		'Facebook': [[19, ' Mar', '2011'], [19, ' Dec', '2013']], 
		'Google': [[201, ' Jan', '2011'], [201, ' Dec', '2013']]
	}
	'''
	with open(csvfile, 'rb') as f:
		sharePriceData = {}
		csvreader = DictReader(f)
		year = csvreader.fieldnames[0]
		month = csvreader.fieldnames[1]

		# creating keys in sharePriceData dict as company names
		for i in xrange(2, len(csvreader.fieldnames)):
			sharePriceData[csvreader.fieldnames[i]] = [[0, "", ""]]
		
		companyNamesList = sharePriceData.keys()
		
		# iterating over all the company share data in a row of a file
		# for share prices which are the earlier highest price, replacing that
		# that sublist with new one
		# if share prices (highest ones) are equal, then simply appending the
		# new sublist in the value of the key (i.e., company name) 
		
		for row in csvreader:
			for company in companyNamesList:
				try:
					currSharePrice = int(row[company])
					maxSharePriceDetailsList = sharePriceData[company]
					for price in maxSharePriceDetailsList:
						temp1 = []
						if currSharePrice >= price[0]: 
							# checkng if the new share price is greater or equal
							# to what we already have in the sublist present
							# against a key's value
							temp2 = []
							temp2.append(currSharePrice)
							temp2.append(row[month])
							temp2.append(row[year])
							temp1.append(temp2)
					
					if temp1:
						for i in temp1:
							for j in maxSharePriceDetailsList:
								if i[0] > j[0]:
									# removing sublists with smaller share price
									# value
									maxSharePriceDetailsList.pop(maxSharePriceDetailsList.index(j))
							maxSharePriceDetailsList.append(i)

							
				except:
					# ignoring errors for now
					pass
				
		print sharePriceData
		return sharePriceData




class MaxSharePriceTestCase(unittest.TestCase):
	"""Populate sample data into a csv file and test the method 'MaxSharePrice' by verifying 
	   that the result it returns, matches the expected result. Delete the file in the end."""
	def setUp(self):
		data = """Year,Month,Microsoft,Facebook,Google
2011, Jan, 65, 12, 201
2011, Feb, 11, 14, 200
2011, Mar, 9, 19, 200
2011, Apr, 76, 17, 200
2012, May, 65, 10, 15
2012, Jun, 53, 10, 15
2012, Jul, 49, 10, 15
2012, Aug, 36, 16, 15
2013, Sep, 50, 10, 15
2013, Oct, 77, 10, 15
2013, Nov, 12, 10, 15
2013, Dec, 77, 19, 201"""
		self.csvfile = "sample_data.csv"
		with open(self.csvfile, 'wb') as f:
			f.write(data)
		# expected output
		self.expectedOutput = {
		'Microsoft': [[77, ' Oct', '2013'], [77, ' Dec', '2013']], 
		'Facebook': [[19, ' Mar', '2011'], [19, ' Dec', '2013']], 
		'Google': [[201, ' Jan', '2011'], [201, ' Dec', '2013']]
		}

	def testSharePriceData(self):
		# assert that the max share price details returned by 'MaxSharePrice' function matches expected result
		self.assertEqual(MaxSharePrice(self.csvfile), self.expectedOutput, 'wrong max share prices details')

	def delFile(self):
		# deleting the csv file
		os.remove("sample_data.csv")

if __name__ == "__main__":
	unittest.main()
