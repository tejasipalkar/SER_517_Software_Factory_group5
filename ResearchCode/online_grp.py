import pandas as pd
import csv
import numpy
import pandas as pd

def common_member(a,b):
	return len(a & b)

def main():

	print("Enter number of students in a Team:", end="")
	no_of_stu = int(input())
	print("Enter number of student preference:", end="")
	no_of_pref = int(input())
	print("Enter number of student avoidance:", end="")
	no_of_avoid = int(input())

	#stu_available = set()
	# stu_list = []
	# stu_time_zone = {}
	# stu_pref = {}
	# stu_avoid = {}

	# with open("StudentSurveyOnline.csv") as fp:
	# 	reader = csv.reader(fp)
	# 	count = 0
	# 	for line in reader:
	# 		#print(line)
	# 		if count > 0:
	# 			stu_available.add(line[1])
	# 			stu_list.append(line[1])
	# 			stu_pref[line[1]] = line[2].split(', ')
	# 			stu_avoid[line[1]] = line[3].split(', ')

	# 		count += 1
	# n = len(stu_available)

	# -------------Hardcoded Values---------------
	stu_list = ['s1@asu.edu','s2@asu.edu','s3@asu.edu','s4@asu.edu','s5@asu.edu','s6@asu.edu','s7@asu.edu','s8@asu.edu','s9@asu.edu','s10@asu.edu','s11@asu.edu','s12@asu.edu']
	stu_available = set(stu_list)
	stu_time_zone = {'s1@asu.edu': ["Monday, 9:00 AM - 12:00 PM", "Monday, 6:00 PM - 9:00 PM", "Tuesday, 12:00 PM - 3:00 PM"],
					's2@asu.edu' : ["Thursday, 3:00 PM - 6:00 PM", "Thursday, 6:00 PM - 9:00 PM", "Tuesday, 12:00 PM - 3:00 PM"],
					's3@asu.edu' : ["Monday, 9:00 AM - 12:00 PM", "Wednesday, 3:00 PM - 6:00 PM", "Tuesday, 12:00 PM - 3:00 PM"],
					's4@asu.edu' : ["Wednesday, 9:00 AM - 12:00 PM", "Monday, 6:00 PM - 9:00 PM", "Tuesday, 12:00 PM - 3:00 PM"],
					's5@asu.edu' : ["Friday, 9:00 AM - 12:00 PM", "Friday, 6:00 PM - 9:00 PM", "Friday, 12:00 PM - 3:00 PM"],
					's6@asu.edu' : ["Saturday, 9:00 AM - 12:00 PM", "Saturday, 6:00 PM - 9:00 PM", "Friday, 6:00 PM - 9:00 PM"],
					's7@asu.edu' : ["Saturday, 6:00 PM - 9:00 PM", "Friday, 6:00 PM - 9:00 PM", "Tuesday, 12:00 PM - 3:00 PM"],
					's8@asu.edu' : ["Monday, 9:00 AM - 12:00 PM", "Monday, 6:00 PM - 9:00 PM", "Tuesday, 12:00 PM - 3:00 PM"],
					's9@asu.edu' : ["Tuesday, 3:00 PM - 6:00 PM", "Monday, 3:00 PM - 6:00 PM", "Wednesday, 3:00 PM - 6:00 PM"],
					's10@asu.edu': ["Friday, 6:00 PM - 9:00 PM", "Thursday, 6:00 PM - 9:00 PM", "Wednesday, 6:00 PM - 9:00 PM"],
					's11@asu.edu': ["Saturday, 9:00 AM - 12:00 PM", "Saturday, 6:00 PM - 9:00 PM", "Friday, 6:00 PM - 9:00 PM"],
					's12@asu.edu': ["Tuesday, 9:00 AM - 12:00 PM", "Tuesday, 3:00 PM - 6:00 PM", "Tuesday, 6:00 PM - 9:00 PM"]}

	stu_pref = {'s1@asu.edu' : ["s2@asu.edu", "s6@asu.edu"],
				's2@asu.edu' : ["s4@asu.edu", "s8@asu.edu"],
				's3@asu.edu' : ["s2@asu.edu", "s5@asu.edu"],
				's4@asu.edu' : [],
				's5@asu.edu' : ["s1@asu.edu", "s6@asu.edu"],
				's6@asu.edu' : ["s7@asu.edu"],
				's7@asu.edu' : ["s6@asu.edu"],
				's8@asu.edu' : [],
				's9@asu.edu' : ["s2@asu.edu", "s4@asu.edu"],
				's10@asu.edu' : ["s11@asu.edu"],
				's11@asu.edu' : ["s10@asu.edu"],
				's12@asu.edu' : ["s2@asu.edu"]}

	stu_avoid = {'s1@asu.edu' : ["s11@asu.edu"],
				's2@asu.edu' : ["s12@asu.edu"],
				's3@asu.edu' : [],
				's4@asu.edu' : [],
				's5@asu.edu' : [],
				's6@asu.edu' : ["s2@asu.edu"],
				's7@asu.edu' : ["s2@asu.edu"],
				's8@asu.edu' : [],
				's9@asu.edu' : ["s4@asu.edu"],
				's10@asu.edu' : ["s5@asu.edu"],
				's11@asu.edu' : [],
				's12@asu.edu' : []}


	# --------------Hardcoding End --------------

	n = len(stu_available)
	team_map = {x:[] for x in range(1, (n // no_of_stu) + 1)}
	stu_dist = numpy.zeros(shape=(n,n))

	#-------Create Distance Matrix-------
	for i in range(n):
		
		temp1 = stu_pref[stu_list[i]]
		if len(temp1) > 0 and temp1[0] != ' ':
			a = 0
			while a < len(temp1):
				#print(temp1)
				idx = stu_list.index(temp1[a])
				stu_dist[i][idx] -= n
				if stu_list[i] in stu_pref[stu_list[idx]]:
					stu_dist[i][idx] -= n
				a += 1

		temp2 = stu_avoid[stu_list[i]]
		if len(temp2) > 0 and temp2[0] != ' ':

			b = 0
			while b < len(temp2):
				#print(temp2[b], temp2)
				idx = stu_list.index(temp2[b])
				stu_dist[i][idx] += n
				if stu_list[i] in stu_avoid[stu_list[idx]]:
					stu_dist[i][idx] += n
				b += 1

		for j in range(i+1,n):
			lst1 = stu_time_zone[stu_list[i]]
			lst2 = stu_time_zone[stu_list[j]]
			val = common_member(set(lst1),set(lst2))
			stu_dist[i][j] -= n*val
			stu_dist[j][i] -= n*val


	print(stu_dist)

	#----------formulating team---------
	team_list = []
	for i,s in enumerate(stu_dist):
		if stu_list[i] in stu_available:
			temp_team = []
			#count_member = 1
			temp_team.append(stu_list[i])
			stu_available.remove(stu_list[i])

			while no_of_stu > len(temp_team) and min(s) < 0:
				idx_min = numpy.argmin(s)
				if stu_list[idx_min] in stu_available:
					temp_team.append(stu_list[idx_min])
					stu_available.remove(stu_list[idx_min])
					
				s[idx_min] = 0

				#count_member += 1

			team_list.append(temp_team)

	print(team_list)
	team_list.sort(key=len, reverse=True)
	remaining_students = [item for sublist in team_list[len(team_map):] for item in sublist]
	team_list = team_list[:len(team_map)]

	#------------handling remaining students --------------
	#remaining_students = list(stu_available)
	if len(remaining_students) > 0:
		
		
		print("r",remaining_students)

		for team in team_list:
			idx = 0
			while len(team) < no_of_stu and idx < len(remaining_students):
				remain = remaining_students[idx]
				insert = True
				for t in team:
					if remain in stu_avoid[t]:
						insert = False
				if insert:
					team.append(remain)
					#stu_available.remove(remain)
					remaining_students.pop(idx)
				else:
					idx += 1

	print(len(stu_available), " Students were not alloted teams.")
	for s in stu_available:
		print(s)

	#-------------assigning team------------------
	i = 0
	for k in team_map:
		team_map[k] = team_list[i]
		i += 1

	print(team_map)


				




if __name__ == "__main__":
	main()