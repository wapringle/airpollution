import csv, json,pprint
res=[]
idx={}
with open('./slides.csv', newline='') as csvfile:
     reader = csv.DictReader(csvfile,fieldnames=['slide','ratio','filename'])
     j=0
     for i,row in enumerate(reader):
          if i>0 and row['filename'] != '':
               slide=row.pop('slide')
               row["highlights"]=[]
               res.append(dict(row))
               idx[slide]=j
               j+=1
               

with open('./Popup_Summary.csv', newline='') as csvfile:
     fieldnames='slide star tlx_pc tly_pc brx_pc bry_pc text'.split(" ")
     reader = csv.DictReader(csvfile,fieldnames=fieldnames)
     for row in reader:
          slide=row.pop('slide')
          row[None]=None
          del row[None]
          if slide in idx:
               res[idx[slide]]["highlights"].append(dict(row))
          else:
               #print(slide)
               pass
with open('bib.jsonld','w') as f:
     json.dump(res,f)


