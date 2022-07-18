from httpx import Client, HTTPTransport, MockTransport, Request, Response


def get_handler(request: Request) -> Response:
    return Response(201)


def get_client(env: str) -> Client:
    if env == "production":
        return Client(transport=HTTPTransport())

    transport = MockTransport(get_handler)
    return Client(transport=transport)
