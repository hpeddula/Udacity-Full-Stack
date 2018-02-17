from http.server import BaseHTTPRequestHandler,HTTPServer
from database_setup import Base,Employee,Address
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import cgi
engine = create_engine('sqlite:///empData.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/employees"):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()

                emps=session.query(Employee).all()

                output =""
                output +="<html><body>"
                output +="<a href=\"/add\">Creating a new Employee</a><br><br>"
                output +="<center><h2 style=\"color:blue;\">The Employee List</h2></center>"
                for emp in emps:
                    output +="<center><li>Employee Name:"+ emp.name+", Employee Id:"+ str(emp.id)+"</li></center>"
                output +="</body></html>"

                self.wfile.write(str.encode(output))
                print (output)
                # print (server.version_string())
                return
            if self.path.endswith("/add"):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output +="<form method=\"POST\" enctype=\"mulitpart/form-data\" action=\"/add\">"
                output +="<center><h2>Add a new Employee</h2>"
                output +="<input type=\"text\" name=\"emp\">"
                output +="<input type=\"submit\" value=\"Create\"></center>"
                output +="</body></html>"

                self.wfile.write(str.encode(output))
                print (output)
                return

        except IOError:
            self.send_error(404,"File Not Found {}".format(self.path))
    def do_POST(self):
        try:
            if self.path.endswith("/add"):
                self.send_response(301)
                # self.send_header('Location','/employees')
                self.end_headers()

                ctype,pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'mulitpart/form-data':
                    fields = cgi.parse_multipart(self.rfile.pdict)
                    messagecontent = fields.get('emp')


                emp = Employee(name = messagecontent[0])
                session.add(emp)
                session.commit()
                output =""
                output +="<html><body>"
                output +="<h2>You Added:{} </h2>".format(messagecontent[0])
                output +="<form method=\"POST\" enctype=\"mulitpart/form-data\" action=\"/add\">"
                output +="<center><h2>Add a new Employee</h2>"
                output +="<input type=\"text\" name=\"emp\">"
                output +="<input type=\"submit\" value=\"Create\"></center>"
                output +="</body></html>"
                # for i in messagecontent:
                #     output +="<html><body>"
                #     output +="<li>"+messagecontent[i]+"</li>"
                #     output +="</body></html>"
                self.wfile.write(str.encode(output))
                print(output)

        except:
            pass

def main():
    try:
        port = 3000
        server = HTTPServer(('',port),handler)
        print ("Inside the try block")
        print ("Running on port {}".format(port))

        server.serve_forever()
    except KeyboardInterrupt:
        print("^C has been pressed")
        server.socket.close()

if __name__ == "__main__":
    main()
