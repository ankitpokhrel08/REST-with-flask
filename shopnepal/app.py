import os
from flask import Flask, request
from flask_smorest import Api
from resources.shop import blueprint as ShopBluePrint
from resources.product import blueprint as ProductBluePrint
from db import db
# This will import the models and create the tables from dunder init file
import models


app = Flask(__name__)
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config['API_TITLE'] = 'Shop API'
app.config['API_VERSION'] = 'v1'
app.config['OPENAPI_VERSION'] = '3.0.2'
app.config['OPENAPI_URL_PREFIX'] = '/doc'
app.config['OPENAPI_SWAGGER_UI_PATH'] = '/'
app.config['OPENAPI_SWAGGER_UI_URL'] = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/'
app.config['OPENAPI_REDOC_PATH'] = '/redoc'
app.config['OPENAPI_REDOC_URL'] = 'https://cdn.jsdelivr.net/npm/redoc/bundles/redoc.standalone.js'

#This will create the tables in the database 
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///shop.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)

with app.app_context():
    db.create_all()

api.register_blueprint(ShopBluePrint)
api.register_blueprint(ProductBluePrint)


#GET - If we want some list/ite from the server
#POST - If we want to send some data to the server i.e create new data on the server    
#PUT - If we want to update some data on the server
#DELETE - If we want to delete some data on the server

# ### 1xx Informational Responses
# 100 Continue: The client can continue with its request.
# 101 Switching Protocols: The server is switching protocols as requested by the client.
# 102 Processing: The server has received and is processing the request but no response is available yet (WebDAV).

# ### 2xx Success
# 200 OK: The request was successful.
# 201 Created: A resource was successfully created.
# 202 Accepted: The request has been accepted for processing but is not complete.
# 203 Non-Authoritative Information: The returned meta-information is not from the original server.
# 204 No Content: The server successfully processed the request, but there’s no content to send back.
# 205 Reset Content: Informs the client to reset the document view.
# 206 Partial Content: The server is delivering part of the resource due to a range header sent by the client.
# 207 Multi-Status: Provides multiple status codes for different operations (WebDAV).

# ### 3xx Redirection
# 300 Multiple Choices: There are multiple options for the resource.
# 301 Moved Permanently: The resource has been moved to a new URL.
# 302 Found: The resource is temporarily available at a different URL.
# 303 See Other: Redirect to another URL using a GET request.
# 304 Not Modified: The resource has not been modified since the last request.
# 305 Use Proxy: The requested resource must be accessed through a proxy.
# 307 Temporary Redirect: The request should be repeated with another URL.
# 308 Permanent Redirect: The resource has been permanently moved to a new URL.

# ### 4xx Client Errors
# 400 Bad Request: The request is malformed or invalid.
# 401 Unauthorized: Authentication is required.
# 402 Payment Required: Reserved for future use.
# 403 Forbidden: The server understands the request but refuses to authorize it.
# 404 Not Found: The requested resource could not be found.
# 405 Method Not Allowed: The request method is not supported by the resource.
# 406 Not Acceptable: The server cannot generate a response acceptable to the client.
# 407 Proxy Authentication Required: The client must authenticate with the proxy.
# 408 Request Timeout: The client took too long to send a request.
# 409 Conflict: The request could not be processed due to a conflict.
# 410 Gone: The resource is no longer available.
# 411 Length Required: The server requires the Content-Length header.
# 412 Precondition Failed: A precondition in the request headers is not met.
# 413 Payload Too Large: The request entity is too large.
# 414 URI Too Long: The request URI is too long for the server to process.
# 415 Unsupported Media Type: The server does not support the media type sent in the request.
# 416 Range Not Satisfiable: The client requested a range not satisfiable by the resource.
# 417 Expectation Failed: The server cannot meet the requirements of the Expect header.
# 418 I'm a Teapot: A joke response from an April Fools' RFC.
# 422 Unprocessable Entity: The request was well-formed but contains semantic errors (WebDAV).
# 423 Locked: The resource is locked (WebDAV).
# 424 Failed Dependency: The request failed due to another request's failure (WebDAV).
# 426 Upgrade Required: The client should upgrade to a different protocol.
# 428 Precondition Required: The server requires the request to be conditional.
# 429 Too Many Requests: The client has sent too many requests in a given time frame.
# 431 Request Header Fields Too Large: The server refuses to process the request because the header fields are too large.
# 451 Unavailable For Legal Reasons: The resource is unavailable due to legal reasons.

# ### 5xx Server Errors
# 500 Internal Server Error: A generic error occurred on the server.
# 501 Not Implemented: The server does not recognize the request method or lacks the ability to process it.
# 502 Bad Gateway: The server received an invalid response from an upstream server.
# 503 Service Unavailable: The server is temporarily unavailable, often due to maintenance or overload.
# 504 Gateway Timeout: The server did not receive a timely response from an upstream server.
# 505 HTTP Version Not Supported: The server does not support the HTTP version used in the request.
# 506 Variant Also Negotiates: A variant for the requested resource is configured to engage in content negotiation itself.
# 507 Insufficient Storage: The server cannot store the representation needed to complete the request (WebDAV).
# 508 Loop Detected: The server detected an infinite loop while processing the request (WebDAV).
# 510 Not Extended: Further extensions are required for the server to fulfill the request.
# 511 Network Authentication Required: The client needs to authenticate to gain network access.

