import requests
import json

class Local:
    def __init__(self):
        self.entities={}
    
    def lookup(self,qstring):
        if qstring not in self.entities:
            E=request_Entity(qstring)
            self.entities.update({qstring:E})
            

class Entity:
    """Basic wikidata entity, can hold Q and P entities alike. Only represents this single entity, you'll have to look up it's claims.
    """
    def __init__(self,key,raw_data):
        self.key=key
        self.claim_ids=[]
        self.aliases=[]
        self.raw_data=raw_data
        self.extract_info()
        
    def extract_info(self):
        d=self.raw_data
        level = " "
        for firstkey in d:
            level = " "
            #print("firstkey")
            #print(level+firstkey+"\n")
            level="  "
            
            for itemid in d[firstkey]:
                level="  "
                #print("itemid")
                #print(level+itemid+"\n")
                subd=d[firstkey][itemid]
                self.itemid=itemid
                #print("iterating subkeys")
                #print("subdkeys",subd.keys())
                level="   "
                
                self.descriptions=subd["descriptions"]
                
                for a in subd["aliases"]:
                    self.aliases.append(a)
                
                for c in subd["claims"]:
                    self.claim_ids.append(c)

def load_request_data(t):
    d=json.loads(t)
    return d
    
def request_Entity(qstring):
    
    #https://www.mediawiki.org/wiki/API:Tutorial
    
    #base="https://www.wikidata.org/"
    stri = "https://www.wikidata.org/wiki/Special:EntityData/"+qstring+".json"
    
    r    = requests.get(stri)
    t    = r.text
    
    if not r.ok:
        return 

    d     = load_request_data(t)
    E=Entity(qstring,d)
    
    return E
    

def test():
    import random
    doug=request_Entity("Q42")
    print(doug.aliases)
    random_claim_id=random.choice(doug.claim_ids)
    random_claim=request_Entity(random_claim_id)
    
    #P2534 is "mathematical expression"
    me=request_Entity("P2534")
    
if __name__=="__main__":
    test()
