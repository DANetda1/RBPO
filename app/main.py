from uuid import uuid4

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from app.logging_config import setup_logging
from app.reading import router as reading_router
from app.settings import get_settings

logger = setup_logging()

app = FastAPI(title="SecDev Course App", version="0.1.0")
settings = get_settings()


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response: Response = await call_next(request)
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("X-Frame-Options", "DENY")
        response.headers.setdefault("Referrer-Policy", "no-referrer")
        response.headers.setdefault("Content-Security-Policy", "default-src 'none'")
        return response


class CorrelationIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        cid = request.headers.get("X-Correlation-ID") or str(uuid4())
        request.state.correlation_id = cid
        response: Response = await call_next(request)
        response.headers["X-Correlation-ID"] = cid
        return response


class ContentLengthLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        cl = request.headers.get("content-length")
        if cl and cl.isdigit() and int(cl) > settings.MAX_CONTENT_LENGTH:
            return problem_json(
                status=413,
                title="Payload Too Large",
                detail=f"Body exceeds limit {settings.MAX_CONTENT_LENGTH} bytes",
                request=request,
                type_url="about:blank",
            )
        return await call_next(request)


def problem_json(
    *,
    status: int,
    title: str,
    detail: str,
    request: Request,
    type_url: str = "about:blank",
):
    cid = getattr(request.state, "correlation_id", None) or str(uuid4())
    return JSONResponse(
        status_code=status,
        media_type="application/problem+json",
        content={
            "type": type_url,
            "title": title,
            "status": status,
            "detail": detail,
            "correlation_id": cid,
            "error": {"code": title, "message": detail},
        },
    )


app.add_middleware(CorrelationIdMiddleware)
app.add_middleware(ContentLengthLimitMiddleware)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ApiError(Exception):
    def __init__(self, code: str, message: str, status: int = 400):
        self.code = code
        self.message = message
        self.status = status


@app.exception_handler(ApiError)
async def api_error_handler(request: Request, exc: ApiError):
    cid = getattr(request.state, "correlation_id", None)
    logger.warning(
        f"ApiError: {exc.code} - {exc.message}",
        extra={"correlation_id": cid, "status": exc.status},
    )
    return problem_json(
        status=exc.status,
        title=exc.code,
        detail=exc.message,
        request=request,
        type_url="about:blank",
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    cid = getattr(request.state, "correlation_id", None)
    detail = exc.detail if isinstance(exc.detail, str) else "http_error"
    logger.warning(
        f"HTTPException: {exc.status_code} - {detail}",
        extra={"correlation_id": cid, "status": exc.status_code},
    )
    return problem_json(
        status=exc.status_code,
        title="http_error",
        detail=detail,
        request=request,
        type_url="about:blank",
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    cid = getattr(request.state, "correlation_id", None)
    logger.error(
        f"Unhandled exception: {type(exc).__name__}",
        exc_info=True,
        extra={"correlation_id": cid},
    )
    return problem_json(
        status=500,
        title="internal_error",
        detail="An internal error occurred",
        request=request,
        type_url="about:blank",
    )


@app.get("/health")
def health():
    return {"status": "ok"}


_DB = {"items": []}


@app.post("/items")
def create_item(name: str):
    if not name or len(name) > 100:
        raise ApiError(
            code="validation_error", message="name must be 1..100 chars", status=422
        )
    item = {"id": len(_DB["items"]) + 1, "name": name}
    _DB["items"].append(item)
    return item


@app.get("/items/{item_id}")
def get_item(item_id: int):
    for it in _DB["items"]:
        if it["id"] == item_id:
            return it
    raise ApiError(code="not_found", message="item not found", status=404)


app.include_router(reading_router)
