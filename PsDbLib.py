import psycopg2

class PsDbLib():
    cursor = ''  
    conn = ''	 


    def connect(self):
        conn_string = "host='*.46.26.*' dbname='control' user='voip' password='voip'"
        print "Connecting to database\n ->%s" % (conn_string)
        self.conn = psycopg2.connect(conn_string)
        self.cursor=  self.conn.cursor()
        

    def check_call(self, user_name, did, user_ip, destenation, gateway_ip):
        
	try:           
		self.cursor.execute("SELECT check_call('"+user_name+"','"+did+"','"+user_ip+"','"+destenation+"','"+gateway_ip+"',0,4);")
		records = self.cursor.fetchall()
                self.conn.commit()
	except:
		self.connect()
		self.cursor.execute("SELECT check_call('"+user_name+"','"+did+"','"+user_ip+"','"+destenation+"','"+gateway_ip+"',0,4);")
		records = self.cursor.fetchall()
                self.conn.commit()
	
	return records[0][0]
        
		
        
		#response =  ''.join(records[0]).split(',')

		
		
		
		
		
		
		
		
