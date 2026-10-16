"""A demo view: composition + events with pyscript.web, sockets with
pyscript.WebSocket. Views return the element the router should display.

Note on listeners: pyscript invokes event listeners synchronously and discards
coroutine objects, so handlers here must be plain sync functions.
"""

from pyscript import WebSocket, web, window

CONTENT = "hello world"


def _socket_url() -> str:
    """ws:// or wss:// for this origin, matching the page protocol."""
    scheme = "wss" if window.location.protocol == "https:" else "ws"
    return f"{scheme}://{window.location.host}/ws"


def test_page() -> web.div:
    container = web.div(classes=["test-page"])

    out = web.p("socket idle", id="ws-output")
    ws = WebSocket(url=_socket_url())

    def socket_open(event) -> None:
        out.textContent = "socket open — ready to send"

    def socket_closed(event) -> None:
        out.textContent = f"socket closed (code {event.code})"

    def socket_error(event) -> None:
        out.textContent = "socket error — check the server is running"

    def on_message(event) -> None:
        data = event.data  # str for text frames, memoryview for binary frames
        text = bytes(data).decode() if not isinstance(data, str) else data
        out.textContent = f"received: {text}"

    def send_frames(event) -> None:
        if ws.readyState != ws.OPEN:
            out.textContent = "socket not open yet — try again in a moment"
            return
        for x in range(10):
            ws.send(f"{CONTENT} x{x}".encode())  # binary frames -> /ws echoes bytes
        out.textContent = "sent 10 frames"

    def close_socket(event) -> None:
        if ws.readyState == ws.OPEN:
            ws.close(code=1000, reason="demo done")
        else:
            out.textContent = "socket already closed"

    ws.onopen = socket_open
    ws.onmessage = on_message
    ws.onclose = socket_closed
    ws.onerror = socket_error

    container.append(
        web.h2("Test Page"),
        web.p(
            "This page is a plain function composing pyscript.web elements — no "
            "wrapper classes, no boilerplate.",
            classes=["muted"],
        ),
        web.div(
            web.button("send 10 frames", on_click=send_frames, classes=["btn"]),
            web.button("close socket", on_click=close_socket, classes=["btn"]),
            out,
            id="ws-demo",
        ),
    )
    return container
