# Script to scrape required feilds from survey results into CSV
import csv
import pandas as pd 

def main():
	print("How many student preference is allowed?", end='')
	no_of_pref = int(input())
	print("How many student avoidance is allowed?", end='')
	no_of_avoid = int(input())

	with open("Scrape.csv") as fp:
		reader = csv.reader(fp, delimiter=',')
		count = 1
		res = []
		for line in reader:
			temp = []
			i = 0
			if count > 3:
				#print(line)
				temp.append(line[i] + '@asu.edu')
				i += 1
				pref = []
				for k in range(i, no_of_pref):
					if line[k] != '' and line[k] != ' ':
						#print(line[k])
						pref.append(line[k] + '@asu.edu')
				temp.append(pref)
				i += no_of_pref
				avoid = []
				for k in range(i, no_of_avoid):
					if line[k] != '' or line[k] != ' ':
						avoid.append(line[k] + '@asu.edu')
				temp.append(avoid)
				i += no_of_avoid
				temp.append(line[i])
				i += 1
				date_time = []
				for idx,word in enumerate(line[i].split(',')):
					if idx%2 == 0:
						first = word
					else:
						date_time.append(first + '-' + word)

				temp.append(date_time)

				print(temp)
				res.append(temp)



			
			count += 1
	
	data = pd.DataFrame(res)
	data.to_csv("Output.csv")

if __name__ == "__main__":
	main()
