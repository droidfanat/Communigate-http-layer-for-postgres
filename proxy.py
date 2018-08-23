#!/usr/bin/env python
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import urlparse
import psycopg2
import sys
import pprint
import re
from TfopLib import TfopSe
import PsDbLib
import os

class S(BaseHTTPRequestHandler):
	user_name=''
	user_ip=''
	fromAddress=''
	destenation=''
	gateway_ip=''

	def _post_headers(self):
		self.send_response(200)
		self.send_header('Content-type', 'text/plain')
		self.end_headers()

	def _set_headers(self):
		if urlparse.urlparse(self.path).path != '/index' and urlparse.urlparse(self.path).path != '/tfop':
			self.send_response(404)
			self.end_headers()
		else:
			self.send_response(200)
			self.send_header('Content-type', 'text/plain')
			self.end_headers()

	def do_GET(self):
		self._set_headers()
		parsed = urlparse.urlparse(self.path)
		if parsed.path=='/index':
				querys=urlparse.parse_qs(parsed.query)
		if ''.join(querys.get('fn'))=="check_call":
			self.user_name=''.join(querys['u'])
			self.user_ip=''.join(querys['ipa']).replace("[",'').replace("]",'')
			self.destenation=''.join(querys['b'])
			self.fromAddress=''.join(querys['fromAddress'])
			self.gateway_ip=''.join(querys['ipb'])
			print('SysLog '+'User: '+self.user_name+'  User_ip: '+self.user_ip+' Destenation Phone: '+self.destenation+' Sip Geteway: '+self.gateway_ip)
			#try:
			data=ps_db_lib.check_call(self.user_name, self.fromAddress ,'1',self.destenation, '1').split(",")
			if data[0]=="200":

				data.pop(0)
				count = 0
				a=''
				b=''
				for x in data:
					count +=1
					if count==1:
						b = b+x+','
					elif count==2:
						a = a+x+','
						count=0
				cgp = '{ Head = 200; p = ('+b[0:-1]+'); a=('+a[0:-1]+');}'
				self.wfile.write(cgp)
			else:
				cgp = '{ Head = '+data[0]+'; }'
				self.wfile.write(cgp)
			#except:
			#	print('SysLog Error Communicate to billing base.')
			#	self.wfile.write('500')

		if ''.join(querys.get('fn'))=="check_route":
			pref=''.join(querys['index'])
			phoneNumber=''.join(querys['phoneNumber'])
			tfop=tfopse.is_index(pref)
			print (pref)
			if tfop != False:

				self.wfile.write('{name="'+tfop.name+'"; gateway="'+tfop.gateway+'"; realm="'+tfop.realm+'";  phoneNumber='+tfop.pref.replace("-", "")+phoneNumber[tfop.pref.count("-"):]+';  }')

	def do_HEAD(self):
		self._set_headers()

	def do_POST(self):
		# Doesn't do anything with posted data
		parsed = urlparse.urlparse(self.path)
		if parsed.path=='/set-tfop':
			content_length = int(self.headers['Content-Length'])
			post_data = self.rfile.read(content_length) # <--- Gets the data itself
			print (post_data )
			tfopse.un_json(post_data)
			tfopse.file_save("./tfop_z.json")
			self._post_headers()
			self.wfile.write("200")




def run(server_class=HTTPServer, handler_class=S, port=80):
	#sys.stdout = open('cgp-proxy.log', 'w')
	server_address = ('', port)
	httpd = server_class(server_address, handler_class)
	print 'Starting cgp deamon...'
	global ps_db_lib
	ps_db_lib = PsDbLib()
	print 'Load db lib...'
	print 'Load tfop lib...'
	global tfopse
	tfopse=TfopSe()
	print 'Load tfop json...'
	try:
		tfopse.file_load('./tfop_z.json')
	except:
		print "Except: tfop did't load !"
	print "Write Pid"
	pid = str(os.getpid())
	f = open('cgp-proxy.pid', 'w')
	f.write(pid)
	f.close()
	print "my pid: "+pid
	print 'Starting httpd...'
	httpd.serve_forever()



if __name__ == "__main__":
	from sys import argv
	from PsDbLib import PsDbLib
	if len(argv) == 2:
		run(port=int(argv[1]))
	else:
		run()
