import requests 


choice = input("Please type something")


variant = "ENSP00000401091.1%3Ap.Tyr124Cys"

response = []

if (choice == "both"):

    grch37_url = "https://grch37.rest.ensembl.org/vep/human/hgvs/"+variant 
    grch38_url = "https://rest.ensembl.org/vep/human/hgvs/" +variant

    url_lsit = [grch37_url,grch38_url]

    payload = {'content-type':'application/json'}

for x in url_lsit:
    
    r = requests.get(x,params=payload)
    response.append(r)

for y in response:
    print(y.json())
