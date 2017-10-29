import random
from firebase import firebase

firebase = firebase.FirebaseApplication('https://temp-438dc.firebaseio.com/temper', None)
result = firebase.post('/temper',{'ID':random.randrang(100, 99, 6)})
#print ('HEELO EVERYONE')
#print (random.randrang(10000, 99999, 6))
result = firebase.get('/users', None)
print (result)
{'1': 'John Doe', '2': 'Jane Doe'}
