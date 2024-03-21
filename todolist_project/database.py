import json

class Database:

    def get_data(self):
        with open('db.json','r') as rf:
            data = json.load(rf)
        return data

    def create_data(self,item):
        with open('db.json','r') as rf:
            data = json.load(rf)

        with open('db.json','w') as wf:
            data.append(item)
            new_data = json.dump(data,wf)

        return new_data

    def done_data(self,index):
        with open('db.json','r') as rf:
            data = json.load(rf)

        with open('db.json','w') as wf:
            data[index]['Status'] = not data[index]['Status']
            new = json.dump(data,wf)
            return new


