from urllib2 import Request, urlopen, URLError

from wordnik import *
apiUrl = 'http://api.wordnik.com/v4'
apiKey = '810e3e6d0084bc5c8200f024bb5062c4074589bfeba2e58f7'
client = swagger.ApiClient(apiKey, apiUrl)

# baseUrl = "http://developer.wordnik.com/v4/word.json/"
# api_key = "/api_key=810e3e6d0084bc5c8200f024bb5062c4074589bfeba2e58f7"

# request = Request(baseUrl+"potato"+api_key)
# try:
#     response = urlopen(request)
#     print (response)
# except URLError, e:
#     print('error')

wordApi = WordApi.WordApi(client)
example = wordApi.getDefinitions('irony')
print example
