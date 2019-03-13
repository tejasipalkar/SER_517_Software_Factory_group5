import json
from pprint import pprint

header = "\\documentclass[10pt]{article}\n\\usepackage{calendar}\n\\usepackage[landscape, a4paper, margin=1cm]{geometry}\n\\usepackage{palatino}\n\\begin{document}\n\\pagestyle{empty}\n\\setlength{\parindent}{0pt}\n\\StartingDayNumber=1\n" 
print(header)

name = "Events"
month_day = "Febraury 2019" 
event = "test"
information = "test information"
start = "-2"
title = "\\begin{center}\n\\textsc{\LARGE " + name + "}\n\\textsc{\large "+ month_day +"}\n\\end{center}"
print(title)    
print("\n")
print("\n")
config1 = "\\begin{calendar}{\\textwidth}"
config2 = "\\setcounter{calendardate}{"+start+"}"
end = "\\finishCalendar\n\\end{calendar}\n\\end{document}"
print(config1)
print(config2)
print("\n")
blank_day = "\\BlankDay"
normal_day = "\\day{"+event+"}{\\textbf{"+event+"}{"+information+"}}"
body = ""
i = 0
while i < 31:
    if i%2==0:
        body = body + "\n" + blank_day
    else:
        body = body + "\n" + normal_day
    i+=1
print(body)

print(normal_day)
print("\n")
print(end)


# with open('my_json_data.json') as f:
#     data = json.load(f)

# pprint(data)
# """
# data = data["data"]
# keys = data[0].keys()
# for i in data:
#     print("++++++++++++++++")
#     for key in keys:
#         print("---------")
#         print(i[key])
#         """

# for (k, v) in data.items():
#    print("+++++")
#    print(str(v))



#    print(data)