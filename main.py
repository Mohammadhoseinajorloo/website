from database import DataBase
from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO
import bcrypt


class HttpHandler(BaseHTTPRequestHandler):

    def set_headers(self) -> None:
        self.send_header(keyword="countent-type", value="text/css")
        self.end_headers()
        return 


    def create_salt(self) -> str:
        return bcrypt.gensalt(rounds=12)


    def hash_pass(self, password:str):
        salt = self.create_salt()
        return bcrypt.hashpw(password, salt)


    def rendering_page(self, path, route="/"):
        if path == path:
            type = "text/html"
        elif path == "static/css/style.css":
            type = "text/css"
        elif path == "/favicon.ico":
            path = "/static/icon/favicon.ico"
            type = "image/x-icon"
        else:
            # Wild-card/default
            if not path == f"{route}":
                print("UNRECONGIZED REQUEST: ", path)

                path = path
                type = "text/html"

        return path, type

       
    def do_GET(self):
        global type

        path = self.path

        if path == "/":
            path = "/templates/index.html"
            path, type = self.rendering_page(path)
           

        elif path == "/Register":
            path = "/templates/register.html"
            path , type = self.rendering_page(path, route="/Register")
        

        # Set header with content type
        self.send_response(200)
        self.send_header("Content-type", type)
        self.end_headers()

        # Open the file, read bytes, serve
        with open(path[1:], 'rb') as file:
            self.wfile.write(file.read())


    def do_POST(self):

        if self.path == "/Register":
            self.send_response(200)
            self.set_headers()

            content_lenght = int(self.headers["Content-Length"])
            post_data_bytes = self.rfile.read(content_lenght)

            post_data_str = post_data_bytes.decode("UTF-8")

            post_data_split = post_data_str.split("&")

            post_dict = {}

            for item in post_data_split:
                key = item.split("=")[0]
                value = item.split("=")[1]
                post_dict[key] = value


            encode_password = post_dict["password"].encode()
            hashed_password = self.hash_pass(encode_password)
            decode_password = hashed_password.decode()
            post_dict["password"] = decode_password

            columns_dict = {"id": "INT  PRIMARY KEY NOT NULL AUTO_INCREMENT",
                            "name": "VARCHAR(64)",
                            "password": "VARCHAR(64)"}

            db = DataBase()
            db.create(table="users", col=columns_dict)
            db.insert(table="users", values=post_dict)

            response = BytesIO()
            response.write(b"done")
            self.wfile.write(response.getvalue())



def run(server_class=HTTPServer, handler_class=HttpHandler, port=8000 ):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting httpd server on port {port}")
    httpd.serve_forever()


if __name__ == "__main__":
     run()