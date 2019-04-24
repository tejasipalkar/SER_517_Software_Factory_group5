import json

#input_file = open('sample.json')

store_list = []

MONTHS = ['Jan','Feb','March','April', 'May', 'June', 'July', 'Aug', 'Sept',
            'Oct', 'Nov', 'Dec']
f = open("test_file.tex", "w")
def myfun(y):
    result = []
    for item in y:
        #print(item['title'])
        line1 = []
        line2 = []
        line1.append('\\newcommand{\\')
        line2.append('\\newcommand{\\')
        string = item['title'].split(':')
        store_list.append(string[0])
        start_str = item['start'].split('T')[0]
        store_list.append(start_str)
        end_str = item['end'].split('T')[0]
        store_list.append(end_str)
        start_str = start_str.split('-')
        start_day = start_str[2]
        start_month = start_str[1]
        start_month = MONTHS[int(float(start_month)) - 1]
        end_str = end_str.split('-')
        end_day = end_str[2]
        end_month = end_str[1]
        end_month = MONTHS[int(float(end_month))-1]

        if start_str == end_str:
            line1.append(string[0])
            line1.append('}{')
            line1.append(start_month + ' ' + str(int(float(start_day))) + '}' )
            result.append(str.join('', [temp for temp in line1]) + '\n')
            f.write(str.join('', [temp for temp in line1]) + '\n')
        else:
            line1.append(string[0]+'Start')
            print(line1)
            line1.append('}{')
            line1.append(start_month + ' ' + str(int(float(start_day))) + '}' )
            result.append(str.join('', [temp for temp in line1]) + '\n')
            f.write(str.join('', [temp for temp in line1]) + '\n')
            print(result)
            line2.append(string[0]+'End')
            print(line2)
            line2.append('}{')
            line2.append(end_month + ' ' + str(int(float(end_day))) + '}' )
            result.append(str.join('', [temp for temp in line2]) + '\n')
            f.write(str.join('', [temp for temp in line2]) + '\n')
        print(result)
    return ''.join(result)

def myassign(x):
    result_Assign = []
    for item in x:
        #print(item['title'])
        line1 = []
        line1.append('\\newcommand{\\')
        string = item['title'].split(':')
        store_list.append(string[0])
        date = item['start'].split('T')[1]
        start_str = item['start'].split('T')[0]
        store_list.append(start_str)
        start_str = start_str.split('-')
        start_day = start_str[2]
        start_month = start_str[1]
        start_month = MONTHS[int(float(start_month)) - 1]
        line1.append(string[0])
        line1.append('}{')
        line1.append(start_month + ' ' + str(int(float(start_day))) + ', ' + date + '}' )
        result_Assign.append(str.join('', [temp for temp in line1]) + '\n')
    return ''.join(result_Assign)
if __name__ == '__main__':
    y = [   {"title":"sprintONE", "start":"2019-03-06T23:57:00", "end":"2019-04-06T23:57:00"}]
    x = [{"title":"assignment1", "start":"2019-04-06T23:57"}]
    retval = myfun(y)
    ret_Assign = myassign(x)
    print(retval)
    print(ret_Assign)
