from flask import Flask, session
from instructorTool.Group_Scripts.group_online import OnlineGroup

class FetchInfo:
    def __init__(self,doc_id, pref, avoid, group_size):
        self.doc_id = doc_id.split("/")[5]
        self.pref = int(pref)
        self.avoid = int(avoid)
        self.group_size = int(group_size)
        print(doc_id)
        self.access_token = session['access_token']

def fetch_document():
    
    r=requests.get("https://www.googleapis.com/drive/v3/files/"+self.doc_id+"/export?mimeType=text/csv", headers={"Authorization":self.access_token})
   
    destname = 'dummy.csv'
    with open(destname, 'w') as wf:
        wf.write(r.text)
        
    count = 0
    with open(destname, 'r') as rf:
        rawtext = rf.read().splitlines()
        myreader = csv.reader(rawtext)
        res = []
        no_of_pref = self.pref
        no_of_avoid = self.avoid
        for row in myreader:
            print("-----------------------------------------------------------------------")
            count = count + 1
            if(count % 2 != 0 and count > 1):
                try:
                    temp = []
                    i = 1
                    temp.append(row[i])
                    i+=1
                    temp.append(row[i])
                    i+=1
                    temp.append(row[i])
                    i+=1
                    temp.append(row[i])
                    i += 1
                    pref = []
                    for k in range(i, no_of_pref+i):
                        #print(line[k])
                        if row[k] != '' and row[k] != ' ':
                            #print(line[k])
                            pref.append(row[k])
                    temp.append(pref)
                    i += no_of_pref
                    avoid = []
                    for k in range(i, no_of_avoid+i):
                        if row[k] != '' and row[k] != ' ':
                            avoid.append(row[k])
                    temp.append(avoid)
                    i += no_of_avoid
                    temp.append(row[i])
                    i += 1
                    date_time = []
                    for idx,word in enumerate(row[i].split(',')):
                        if idx%2 == 0:
                            first = word
                        else:
                            date_time.append(first + '-' + word)

                    temp.append(date_time)
                    i += 1
                    temp.append(row[i])
                    i += 1
                    temp.append(row[i])
                    i += 1
                    temp.append(row[i])
                    res.append(temp)
                    print(count, temp)
                except:
                    traceback.print_exc(file=sys.stdout)

        data = pd.DataFrame(res, columns=['Full Name', 'ASURITE', 'GitHub', 'EmailID', 'Preferences', 'Avoidance', 'TimeZone', 'TimePreference', 'GithubKnowledge', 'ScrumKnowledge', 'Comments'])
        #session['response'] = data.to_json(orient='split')
        print(data)
        print("--------------Done----------------")
    print("calling G")
    g = OnlineGroup(self.group_size, data)
    res = g.assign_group()
    print(res)

    #return session['response']
    return res