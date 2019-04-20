import pandas as pd

class save_csv:
	def __init__(self, table):
		self.table = table

	def save(self):
		save_file = pd.DataFrame(self.table)
		print(save_file)
		save_file.to_csv('Table_Output.csv')

