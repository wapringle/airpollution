import csv, json
res={}
with open('../slides.csv', newline='') as csvfile:
     reader = csv.DictReader(csvfile)
     for row in reader:
          if row['Filename'] != '':
               s=row['Slide']
               del row['Slide']
               row["highlights"]=[]
               res[s]=dict(row)
               
                    

with open('../Popup_Summary.csv', newline='') as csvfile:
     reader = csv.DictReader(csvfile)
     for row in reader:
               s=row['Slide Number']
               if s in res.keys():
                    del row['Slide Number']
                    res[s]["highlights"].append(dict(row))
json.dumps(res))
i=1    


