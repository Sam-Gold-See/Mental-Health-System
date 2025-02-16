import datetime
import time
from fastapi import Request, HTTPException, Depends, status
from starlette.middleware.base import BaseHTTPMiddleware
from app.utils.logger import get_logger
from app.config import config
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlmodel import select
from app.db.main import SessionDB

logger = get_logger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


class JWTAuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, exclude_paths: list = None):
        super().__init__(app)
        self.secret_key = config.JWT_SECRET_KEY
        # 扩展默认排除路径
        self.exclude_paths = exclude_paths or [
            "/auth/login",
            "/auth/register",
            "/docs",
            "/openapi.json",
            "/redoc",
        ]

    async def dispatch(self, request: Request, call_next):
        # 检查是否为排除的路径
        if any(request.url.path.startswith(path) for path in self.exclude_paths):
            return await call_next(request)

        # 获取token
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="未提供有效的授权令牌",
                headers={"WWW-Authenticate": "Bearer"},
            )

        try:
            # 验证token
            token = auth_header.split(" ")[1]
            payload = jwt.decode(
                token, self.secret_key, algorithms=[config.JWT_ALGORITHM]
            )
            request.state.user_id = payload.get("sub")
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="授权已过期")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="无效的授权")

        return await call_next(request)


class RequestLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 记录请求开始时间
        start_time = time.time()

        # 记录请求信息
        logger.info(
            f"开始处理请求: {request.method} {request.url.path} {request.json() if request.json() else ''} {request.headers}"
        )

        # 处理请求
        response = await call_next(request)

        # 计算处理时间
        process_time = time.time() - start_time

        # 记录响应信息
        logger.info(
            f"请求处理完成: {request.method} {request.url.path} - 状态码: {response.status_code} - 处理时间: {process_time:.2f}s"
        )

        return response


class TokenRefreshMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, refresh_threshold: int = 300):
        super().__init__(app)
        self.secret_key = config.JWT_SECRET_KEY
        self.refresh_threshold = refresh_threshold  # 刷新阈值（秒）

    async def dispatch(self, request: Request, call_next):
        token = request.headers.get("Authorization")
        if token and token.startswith("Bearer "):
            try:
                # 解析token
                token = token.split(" ")[1]
                payload = jwt.decode(
                    token, self.secret_key, algorithms=[config.JWT_ALGORITHM]
                )

                # 检查是否需要刷新
                exp = payload.get("exp", 0)
                current_time = datetime.datetime.now(datetime.timezone.utc).timestamp()

                if exp - current_time < self.refresh_threshold:
                    # 生成新token
                    new_payload = payload.copy()
                    new_payload["exp"] = (
                        datetime.datetime.now(datetime.timezone.utc).timestamp()
                        + config.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60
                    )
                    new_token = jwt.encode(
                        new_payload, self.secret_key, algorithm=config.JWT_ALGORITHM
                    )

                    # 处理请求
                    response = await call_next(request)

                    # 在响应头中添加新token
                    response.headers["Authorization"] = f"Bearer {new_token}"
                    return response

            except jwt.InvalidTokenError:
                pass

        return await call_next(request)


async def get_current_user(
    token: str = Depends(oauth2_scheme), sessionDB: SessionDB = Depends()
) -> str:
    try:
        payload = jwt.decode(
            token, config.JWT_SECRET_KEY, algorithms=[config.JWT_ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            logger.error(f"用户ID不存在: {token}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户ID不存在",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except JWTError:
        logger.error(f"无效的JWT令牌: {token}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的JWT令牌",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user_id
