import json

class Tfop(object):
    def __init__(self, index, name, gateway, realm, pref, *args, **kwargs):
        self.index = index
	self.name = name
        self.gateway = gateway
	self.realm = realm
	self.pref = pref
    def obj_dict(obj):
	    return obj.__dict__



class TfopSe(object):
	objlist=[]	
	def add(self,obj):
		self.objlist.append(obj)

	def obj_dict(obj):
		    return obj.__dict__

	def to_json(self):
		return json.dumps(self.objlist, default=Tfop.obj_dict)

	def un_json(self,my_json):
		self.objlist=[]
		obj=json.loads(my_json)
		for x in obj:
			try:
			    self.objlist.append(Tfop(**x))
			except:
                            print "error json"
	def is_index(self,index):
		for x in self.objlist:
			if x.index==index:
				return x			
		return False

	def file_save(self,f_name):
		file = open(f_name,"w")
		file.write(self.to_json())
		file.close()

	def file_load(self,f_name):
		with open(f_name, 'r') as myfile:
			data = myfile.read()
		self.un_json(data)



#tfopse=TfopSe()

#tfopse.add(Tfop(222,"operator_name","10.10.10.2","operator.domain.com"))
#tfopse.add(Tfop(333,"operator_name","10.10.10.2","operator.domain.com"))
#tfopse.add(Tfop(444,"operator_name","10.10.10.2","operator.domain.com"))
#tfopse.add(Tfop(555,"operator_name","10.10.10.2","operator.domain.com"))

#tfopse.file_save('./tfop.json')

#new_tfopse=TfopSe()
#new_tfopse.file_load('./tfop.json')
#print(new_tfopse.is_index(333).index)

#tfopse.to_json()

#import json
#j = json.loads('{"__type__": "User", "name": "John Smith", "username": "jsmith"}')
#u = User(**j)
#print (users)
