import pandas as pd
import csv
import numpy

class OnlineGroup:
	def __init__(self, team_size, dataframe):
		self.no_of_stu = team_size
		self.stu_list = dataframe['ASURITE']
		self.stu_time_zone = {x:y for x,y in zip(dataframe['ASURITE'],dataframe['TimePreference'])}
		self.stu_pref = {x:y for x,y in zip(dataframe['ASURITE'],dataframe['Preference'])}
		self.stu_avoid = {x:y for x,y in zip(dataframe['ASURITE'],dataframe['Avoidance'])}
		self.stu_utc = {x:y for x,y in zip(dataframe['ASURITE'],dataframe['TimeZone'])}
		
		

	def common_member(self, a,b):
		return len(a & b)
	
	def read_data(self):
		# This will read data from organized csv file for input
		# with open("Output.csv") as fp:
		# 	reader = csv.reader(fp)
		# 	count = 0
		# 	for line in reader:
		# 		#print(line)
		# 		if count > 0:
		# 			self.stu_list.append(line[2])
		# 			self.stu_pref[line[2]] = [x.replace("'",'') for x in line[5][1:-1].split(', ')]
		# 			self.stu_avoid[line[2]] = [x.replace("'",'') for x in line[6][1:-1].split(', ')]
		# 			self.stu_utc[line[2]] = line[7]
		# 			self.stu_time_zone[line[2]] = line[8][1:-1].split(', ')
		# 		count += 1
		
		self.stu_available = set(self.stu_list)

	def generate_cost_matrix(self):
		
		self.read_data()
		
		max_factor = max(len(self.stu_time_zone[d]) for d in self.stu_time_zone)
		n = len(self.stu_available)
		self.team_map = {x:[] for x in range(1, (n // self.no_of_stu) + 1)}
		stu_dist = numpy.zeros(shape=(n,n))

		#-------Create Distance Matrix-------
		for i in range(n):
			
			temp1 = self.stu_pref[self.stu_list[i]]
			if len(temp1) > 0 and temp1[0] != ' ':
				a = 0
				while a < len(temp1):
					#print(temp1)
					try:

						idx = self.stu_list.index(temp1[a])
						stu_dist[i][idx] -= n
						if self.stu_list[i] in self.stu_pref[self.stu_list[idx]]:
							stu_dist[i][idx] -= n
						
					except:
						print(temp1[a], " Not in the list")
					a += 1

			temp2 = self.stu_avoid[self.stu_list[i]]
			if len(temp2) > 0 and temp2[0] != ' ':

				b = 0
				while b < len(temp2):
					#print(temp2[b], temp2)
					try:

						idx = self.stu_list.index(temp2[b])
						stu_dist[i][idx] += n
						if self.stu_list[i] in self.stu_avoid[self.stu_list[idx]]:
							stu_dist[i][idx] += 2*n
						
					except:
						print(temp2[b], " Not in the list")
					b += 1
			for j in range(i+1, n):
				if i != j:
					if self.stu_utc[self.stu_list[i]] == self.stu_utc[self.stu_list[j]]:
						stu_dist[i][j] -= n
						stu_dist[j][i] -= n

			for j in range(i+1,n):
				lst1 = self.stu_time_zone[self.stu_list[i]]
				lst2 = self.stu_time_zone[self.stu_list[j]]
				val = self.common_member(set(lst1),set(lst2))
				if val != 0:
					factor = int((float(val)/max_factor)*n)
					#print(factor)

					stu_dist[i][j] -= factor
					stu_dist[j][i] -= factor

		return stu_dist

	def generate_group(self):

		stu_dist = self.generate_cost_matrix()

			#----------formulating team---------
		team_list = []
		for i,s in enumerate(stu_dist):
			if self.stu_list[i] in self.stu_available:
				temp_team = []
				#count_member = 1
				temp_team.append(self.stu_list[i])
				self.stu_available.remove(self.stu_list[i])
				c = 1
				while self.no_of_stu > len(temp_team) and c < self.no_of_stu:
					idx_min = numpy.argmin(s)
					if self.stu_list[idx_min] in self.stu_available:
						temp_team.append(self.stu_list[idx_min])
						self.stu_available.remove(self.stu_list[idx_min])
						
					s[idx_min] = 0
					c += 1

					#count_member += 1

				team_list.append(temp_team)

		print(team_list)
		team_list.sort(key=len, reverse=True)
		remaining_students = [item for sublist in team_list[len(self.team_map):] for item in sublist]
		team_list = team_list[:len(self.team_map)]

		#------------handling remaining students --------------
		#remaining_students = list(stu_available)
		if len(remaining_students) > 0:
			
			
			print("remaining", remaining_students)

			for team in team_list:
				idx = 0
				while len(team) < self.no_of_stu and idx < len(remaining_students):
					remain = remaining_students[idx]
					insert = True
					for t in team:
						if remain in self.stu_avoid[t]:
							insert = False
					if insert:
						team.append(remain)
						#stu_available.remove(remain)
						remaining_students.pop(idx)
					else:
						idx += 1

		print(len(remaining_students), " Students were not alloted teams.")
		for s in remaining_students:
			print(s)

		return team_list


	def assign_group(self):

		team_list = self.generate_group()

			#-------------assigning team------------------
		i = 0
		for k in self.team_map:
			self.team_map[k] = team_list[i]
			i += 1

		print(self.team_map)

		#-----------Allot Team numbers for excel----------
		group_assign = [0]*len(self.stu_list)
		print(self.stu_list)
		for t in self.team_map:
			for val in self.team_map[t]:
				idx = self.stu_list.index(val)
				group_assign[idx] = t
		print(group_assign)
		
		read_pd = pd.read_csv('Output.csv')
		read_pd['Group Name'] = group_assign
		read_pd.to_csv('FinalOutput.csv')






# This method is purely for testing purpose
# def main():
# 	#Read the group size
# 	print("Enter number of students in a Team:", end="")
# 	no_of_stu = int(input())

# 	obj = OnlineGroup(no_of_stu)
# 	obj.assign_group()

	
# if __name__ == "__main__":
# 	main()





