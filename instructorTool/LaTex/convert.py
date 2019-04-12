import json
from pprint import pprint
from datetime import datetime

with open('my_json_data.json') as f:
     data = json.load(f)


header = "\\documentclass[10pt]{article}\n\\usepackage{calendar}\n\\usepackage[landscape, a4paper, margin=1cm]{geometry}\n\\usepackage{palatino}\n\\begin{document}\n\\pagestyle{empty}\n\\setlength{\parindent}{0pt}\n\\StartingDayNumber=1\n"

name = "Events"

event = "test"
information = "test information"
start = 1
title = "\\begin{center}\n\\textsc{\LARGE " + name + "}\n\\textsc{\large "+ month_day +"}\n\\end{center}"


config1 = "\\begin{calendar}{\\textwidth}\n"

end = "\\finishCalendar\n\\end{calendar}\n\\end{document}"

blank_day = "\\BlankDay"

body = ""

tex_file = open("test.tex", "w")

tex_file.write(header + '\n')
tex_file.write(config1 + '\n')


for item in data:
    keys = item.keys()
    if "start_at" in keys:
        date_key = "start_at"
    else:
        date_key = "end_at"
    split_date = str(item[date_key]).split('T')
    split_date = split_date[0].split('-')
    year = split_date[0]
    month = split_date[1]
    day = split_date[2]
    title = "\\begin{center}\n\\textsc{\LARGE " + name + "}\n\\textsc{\large "+ month +"}\n\\end{center}"
    start = datetime(int(year), int(month), 1).weekday() - 1
    normal_day = "\\day{{{}}}{{\\textbf{{{}}}".format(name,event)

    tex_file.write(normal_day)
tex_file.write(end + '\n')
tex_file.close()
#     i = 0
#     while i < 30:
#         i+=1
#         if i == int(day):
#             body = body + "\n" + normal_day
#         else:
#             body + "\n" + blank_day
# elif k == "title":
#     information = v
# elif k == "context_code":
#     event = v
#
# month_day = month + "/" + year
# title = "\\begin{center}\n\\textsc{\LARGE " + name + "}\n\\textsc{\large "+ month_day +"}\n\\end{center}"
# config2 = "\\setcounter{calendardate}{"+str(start)+"}"
#
#
# print(header)
# print(title)
# print(config1)
# print(config2)
# print(body)
# print(end)
