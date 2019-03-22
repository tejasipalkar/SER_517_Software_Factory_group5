# Script to scrape required feilds from survey results into CSV
import csv
import pandas as pd 

def main():
	print("How many student preference is allowed?", end='')
	no_of_pref = int(input())
	print("How many student avoidance is allowed?", end='')
	no_of_avoid = int(input())

	with open("scrape.csv") as fp:
		reader = csv.reader(fp, delimiter=',')
		count = 1
		res = []
		for line in reader:
			temp = []
			i = 0
			if count > 3:
				#print(line)
				temp.append(line[i])
				i+=1
				temp.append(line[i])
				i+=1
				temp.append(line[i])
				i+=1
				temp.append(line[i])
				i += 1
				pref = []
				for k in range(i, no_of_pref+i):
					#print(line[k])
					if line[k] != '' and line[k] != ' ':
						#print(line[k])
						pref.append(line[k])
				temp.append(pref)
				i += no_of_pref
				avoid = []
				for k in range(i, no_of_avoid+i):
					if line[k] != '' and line[k] != ' ':
						avoid.append(line[k])
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
				i += 1
				temp.append(line[i])
				i += 1
				temp.append(line[i])
				i += 1
				temp.append(line[i])
				


				print(temp)
				res.append(temp)



			
			count += 1
	
	data = pd.DataFrame(res, columns=['Full Name', 'ASURITE', 'GitHub', 'EmailID', 'Preferences', 'Avoidance', 'TimeZone', 'TimePreference', 'GithubKnowledge', 'ScrumKnowledge', 'Comments'])
	data.to_csv("Output.csv")

if __name__ == "__main__":
	main()
