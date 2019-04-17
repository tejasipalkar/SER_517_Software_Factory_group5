import pandas as pd
import csv
import numpy
import pandas as pd

def main():

	print("Enter number of students in a Team:", end="")
	no_of_stu = int(input())

	stu_available = set()
	stu_list = []
	stu_pref = {}
	stu_avoid = {}

	with open("StudentSurvey.csv") as fp:
		reader = csv.reader(fp)
		count = 0
		for line in reader:
			#print(line)
			if count > 0:
				stu_available.add(line[1])
				stu_list.append(line[1])
				stu_pref[line[1]] = line[2].split(', ')
				stu_avoid[line[1]] = line[3].split(', ')

			count += 1
	n = len(stu_available)
	
	team_map = {x:0 for x in range(1, (n // no_of_stu) + 1)}
	stu_dist = numpy.zeros(shape=(n,n))
	#print(stu_list)
	#print("map1", stu_pref)
	
	#create distance matrix
	for i in range(n):
		# for j in range(n):
		# 	if i == j:
		# 		stu_dist[i][j] += n
		# 	else:
		temp1 = stu_pref[stu_list[i]]
		if temp1[0] != '' and temp1[0] != ' ':
			a = 0
			while a < len(temp1):
				#print(temp1)
				idx = stu_list.index(temp1[a])
				stu_dist[i][idx] -= n
				if stu_list[i] in stu_pref[stu_list[idx]]:
					stu_dist[i][idx] -= n
				a += 1

		temp2 = stu_avoid[stu_list[i]]
		if temp2[0] != '' and temp2[0] != ' ':

			b = 0
			while b < len(temp2):
				#print(temp2[b], temp2)
				idx = stu_list.index(temp2[b])
				stu_dist[i][idx] += n
				if stu_list[i] in stu_avoid[stu_list[idx]]:
					stu_dist[i][idx] += n
				b += 1
				

	print(stu_dist)
	print(team_map)

	#Assign Preference to the team
	
	team_list = []
	for i,s in enumerate(stu_dist):
		print(s)
		#for i in range(n):
		if stu_list[i] in stu_available:
			temp_team = []
			count_member = 1
			temp_team.append(stu_list[i])
			stu_available.remove(stu_list[i])
			while no_of_stu > len(temp_team) and min(s) < 0:
				idx_min = numpy.argmin(s)
				if stu_list[idx_min] in stu_available:
					temp_team.append(stu_list[idx_min])
					stu_available.remove(stu_list[idx_min])
					
				s[idx_min] = 0

				count_member += 1


			print("updated", s)		
			print(temp_team)
			team_list.append(temp_team)

	# Sort the list in descending order of len
	#print(team_list)
	#sorted(team_list, key = lambda x:len(x) )
	team_list.sort(key=len, reverse=True)
	#print(team_list)
	remaining_stu = [item for sublist in team_list[len(team_map):] for item in sublist]
	team_list = team_list[:len(team_map)]
	print(team_list)
	print(remaining_stu)
	#print()
	#print(stu_available)

	#Assigning left off students 
	for tm in team_list:
		i = 0
		work_with = True
		while len(tm) < no_of_stu and i < len(remaining_stu):
			idx_r = stu_list.index(remaining_stu[i])
			for t in tm:
				if stu_dist[idx_r][stu_list.index(t)] > 0:
					work_with = False

			if work_with:
				tm.append(remaining_stu[i])
				remaining_stu.pop(i)
			else:
				i += 1

	print(team_list)
	print(remaining_stu)

	i = 0
	for k in team_map:
		team_map[k] = team_list[i]
		i += 1

	print(team_map)

	#Write the files to csv
	data = pd.DataFrame(team_map)
	print(data)
	transpose_dat = data.T
	print(transpose_dat)
	transpose_dat.to_csv("TeamList.csv")




			
			





				
	




		#print("set", stu_available)
		
		#print("map2", stu_avoid)

	
	#print(team_map)
	#print(random.sample(stu_available, 1))



	#for t in team_map:
	#	#Randomly pick one student
	#	stu_pick = random.sample(stu_available, 1)



	#for s in stu_available:





if __name__ == "__main__":
	main()
	
	
