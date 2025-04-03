class HttpStatusCode:
    """
    Hypertext Transfer Protocol (HTTP) response status codes.
    """

    # 1xx Informational Responses

    # The server has received the request headers and the client should proceed to send the request body.
    CONTINUE = 100

    # The requester has asked the server to switch protocols and the server has agreed to do so.
    SWITCHING_PROTOCOLS = 101

    # A WebDAV request may contain many sub-requests requiring a long time to complete.
    PROCESSING = 102

    # 2xx Success

    # Standard response for successful HTTP requests.
    OK = 200

    # The request has been fulfilled, resulting in the creation of a new resource.
    CREATED = 201

    # The request has been accepted for processing, but the processing has not been completed.
    ACCEPTED = 202

    # The server successfully processed the request, but is returning information from a third-party.
    NON_AUTHORITATIVE_INFORMATION = 203

    # The server successfully processed the request and is not returning any content.
    NO_CONTENT = 204

    # The requester should reset the document view.
    RESET_CONTENT = 205

    # The server is delivering only part of the resource due to a range header sent by the client.
    PARTIAL_CONTENT = 206

    # A WebDAV response containing multiple status codes.
    MULTI_STATUS = 207

    # The members of a DAV binding have already been enumerated in a previous response.
    ALREADY_REPORTED = 208

    # The server has fulfilled a request for the resource.
    IM_USED = 226

    # 3xx Redirection

    # Indicates multiple options for the resource from which the client may choose.
    MULTIPLE_CHOICES = 300

    # This and all future requests should be directed to the given URI.
    MOVED_PERMANENTLY = 301

    # The requested resource has been temporarily moved to another location.
    FOUND = 302

    # The response to the request can be found under another URI using a GET method.
    SEE_OTHER = 303

    # Indicates that the resource has not been modified since the version specified by request headers.
    NOT_MODIFIED = 304

    # The requested resource is available only through a proxy.
    USE_PROXY = 305

    # No longer used. Originally meant "Subsequent requests should use the specified proxy."
    SWITCH_PROXY = 306

    # The request should be repeated with another URI.
    TEMPORARY_REDIRECT = 307

    # The request and all future requests should be repeated using another URI.
    PERMANENT_REDIRECT = 308

    # 4xx Client Errors

    # The server cannot process the request due to client error.
    BAD_REQUEST = 400

    # Authentication is required and has failed or not been provided.
    UNAUTHORIZED = 401

    # Reserved for future use.
    PAYMENT_REQUIRED = 402

    # The request was valid, but the server is refusing action.
    FORBIDDEN = 403

    # The requested resource could not be found.
    NOT_FOUND = 404

    # A request method is not supported for the requested resource.
    METHOD_NOT_ALLOWED = 405

    # The requested resource is capable of generating only content not acceptable according to request headers.
    NOT_ACCEPTABLE = 406

    # The client must first authenticate itself with the proxy.
    PROXY_AUTHENTICATION_REQUIRED = 407

    # The server timed out waiting for the request.
    REQUEST_TIMEOUT = 408

    # The request could not be processed due to conflict.
    CONFLICT = 409

    # The requested resource is no longer available.
    GONE = 410

    # The request did not specify the length of its content.
    LENGTH_REQUIRED = 411

    # The server does not meet one of the preconditions set by the requester.
    PRECONDITION_FAILED = 412

    # The request is larger than the server is willing to process.
    PAYLOAD_TOO_LARGE = 413

    # The URI provided was too long for the server to process.
    URI_TOO_LONG = 414

    # The request entity has a media type which is not supported by the server.
    UNSUPPORTED_MEDIA_TYPE = 415

    # The client has asked for a portion of the file, but the server cannot supply that portion.
    RANGE_NOT_SATISFIABLE = 416

    # The server cannot meet the requirements of the Expect header field.
    EXPECTATION_FAILED = 417

    # Defined in 1998 as an April Fools' joke. Used as an Easter egg in some websites.
    I_AM_A_TEAPOT = 418

    # The request was directed at a server that is not able to produce a response.
    MISDIRECTED_REQUEST = 421

    # The request was well-formed but contained semantic errors.
    UNPROCESSABLE_ENTITY = 422

    # The resource being accessed is locked.
    LOCKED = 423

    # The request failed due to failure of a previous request.
    FAILED_DEPENDENCY = 424

    # The client should switch to a different protocol.
    UPGRADE_REQUIRED = 426

    # The origin server requires the request to be conditional.
    PRECONDITION_REQUIRED = 428

    # The user has sent too many requests in a given amount of time.
    TOO_MANY_REQUESTS = 429

    # The server is unwilling to process the request because of large headers.
    REQUEST_HEADER_FIELDS_TOO_LARGE = 431

    # The server operator has received a legal demand to deny access.
    UNAVAILABLE_FOR_LEGAL_REASONS = 451

    # 5xx Server Errors

    # A generic error message for unexpected server conditions.
    INTERNAL_SERVER_ERROR = 500

    # The server does not recognize the request method or lacks the ability to fulfill the request.
    NOT_IMPLEMENTED = 501

    # The server was acting as a gateway and received an invalid response from the upstream server.
    BAD_GATEWAY = 502

    # The server is currently unavailable due to overload or maintenance.
    SERVICE_UNAVAILABLE = 503

    # The server was acting as a gateway and did not receive a timely response.
    GATEWAY_TIMEOUT = 504

    # The server does not support the HTTP protocol version used in the request.
    HTTP_VERSION_NOT_SUPPORTED = 505

    # Transparent content negotiation resulted in a circular reference.
    VARIANT_ALSO_NEGOTIATES = 506

    # The server is unable to store the representation needed to complete the request.
    INSUFFICIENT_STORAGE = 507

    # The server detected an infinite loop while processing the request.
    LOOP_DETECTED = 508

    # Further extensions are required for the server to fulfill the request.
    NOT_EXTENDED = 510

    # The client needs to authenticate to gain network access.
    NETWORK_AUTHENTICATION_REQUIRED = 511
