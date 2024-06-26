# import services in project
from extentions import (
    Router,
    DataBase,
    Hashing,
)
# library built in python
from http.server import (
    HTTPServer,
    BaseHTTPRequestHandler,
    SimpleHTTPRequestHandler,
)
# helper_function in project
from extentions.utils import processing_front_data


class HttpHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        # Set header with content type
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        # Router service
        router = Router()
        path = router.translate_path(self.path)

        # Open the file, read bytes, serve
        with open(path[1:], 'rb') as file:
            self.wfile.write(file.read())

    def do_POST(self):
        if self.path == "/register":
            self.send_response(200)
            self.send_header(keyword="Content-type", value="text/html")
            self.end_headers()

            content_lenght = int(self.headers["Content-Length"])
            post_data_bytes = self.rfile.read(content_lenght)

            # processing frontend data
            post_dict = processing_front_data(post_data_bytes)

            # hashing service
            hashing = Hashing()
            hash_password = hashing.hash_pass(post_dict["password"])
            post_dict["password"] = hash_password

            # database service
            db = DataBase()
            columns_database = {
                "id": "INT  PRIMARY KEY NOT NULL AUTO_INCREMENT",
                "email": "VARCHAR(255)",
                "username": "VARCHAR(64)",
                "password": "VARCHAR(64)"
            }
            db.create(table="users", col=columns_database)
            db.insert(table="users", values=post_dict)


def run(server_class=HTTPServer, handler_class=HttpHandler, port=8001):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting httpd server on port {port}")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
