import requests

url = "https://maps-data.p.rapidapi.com/searchmaps.php"

querystring = {"query":"fancy restaurants","limit":"20","country":"us","lang":"en","lat":"40.7244714","lng":"-74.0057078","offset":"0","zoom":"13"}

headers = {
	"X-RapidAPI-Key": "4578ad90c0msh7185e76eb4a1d1ap1676a0jsn80fa8c573e3d",
	"X-RapidAPI-Host": "maps-data.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())