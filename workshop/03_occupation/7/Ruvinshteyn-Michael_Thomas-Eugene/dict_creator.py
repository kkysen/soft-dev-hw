## Michael Ruvinshteyn and Eugene Thomas
## SoftDev1 pd7
## HW03 -- StI/O: Divine your Destiny!
## 2017-09-14

import random

def dict_creation(f):
    dictionary = {}
    elements = [] 
    try: 
        d = open(f, 'rU')
        c = d.read() 
    except:
        return 'Sorry :( :( :,('
    lines = c.split('\n')
    for i in lines:
        q = i.rsplit(',', 1)
        elements.append(q)
    for b in elements[1:len(elements)-1]:
       dictionary[b[0]] = b[1]
    return dictionary
        
def select(f):
    try: 
       dictionary = dict_creation(f)  
    except:
        return 'Sorry :( :( :,('
    dictionary.pop("Total") 
    dictList = list(dictionary) 
    holder = []
    for d in dictList:
        f = float(dictionary.get(d))
        x = int(f)*10
        i = 0 
        while i < x:
            holder.append(d)
            i += 1
    return random.choice(holder)

        
            
    
    
