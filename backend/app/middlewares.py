import datetime
import time
from fastapi import Request, HTTPException, Depends, status
from fastapi.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.utils.logger import get_logger
from app.config import config
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlmodel import select
from app.dependencies import get_current_user, token_manager

logger = get_logger(__name__)


class RequestLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        # 记录请求信息
        await self._log_request(request)

        try:
            response = await call_next(request)
            process_time = time.time() - start_time

            # 记录响应信息
            await self._log_response(request, response, process_time)
            return response

        except Exception as e:
            logger.error(f"请求处理发生错误: {str(e)}")
            raise

    async def _log_request(self, request: Request):
        """记录请求详情"""
        request_body = ""
        try:
            if request.method in ["POST", "PUT", "PATCH"]:
                request_body = await request.json()
        except Exception:
            request_body = "无法解析的请求体"

        query_params = dict(request.query_params)
        headers = dict(request.headers)
        # 移除敏感信息
        if "authorization" in headers:
            self.user_id = token_manager.decode_token(
                headers["authorization"].split(" ")[1]
            )
            headers["authorization"] = "Bearer [FILTERED]"
            logger.debug(f"user_id: {self.user_id}")
        else:
            self.user_id = "游客"
        logger.info(
            f"收到请求: {self.user_id}\n"
            f"方法: {request.method}\n"
            f"路径: {request.url.path}\n"
            f"查询参数: {query_params}\n"
            f"请求体: {request_body}\n"
            f"客户端: {request.client.host if request.client else 'unknown'}"
        )

    async def _log_response(
        self, request: Request, response: Response, process_time: float
    ):
        """记录响应详情"""
        try:
            response_headers = dict(response.headers)
            content_length = response_headers.get("content-length", "未知")

            logger.info(
                f"请求处理完成: {self.user_id}\n"
                f"方法: {request.method}\n"
                f"路径: {request.url.path}\n"
                f"状态码: {response.status_code}\n"
                f"响应大小: {content_length} bytes\n"
                f"处理时间: {process_time:.3f}s"
            )
        except Exception as e:
            logger.error(f"记录响应信息时发生错误: {str(e)}")


class TokenRefreshMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            try:
                # 验证当前令牌
                payload = token_manager.verify_token(token)
                # 如果令牌即将过期（例如剩余时间小于1天），则刷新
                exp = datetime.datetime.fromtimestamp(
                    payload.get("exp"), tz=datetime.timezone.utc
                )
                if (exp - datetime.datetime.now(datetime.timezone.utc)).seconds < 5 * 60:
                    logger.info("刷新令牌")
                    new_access_token, new_refresh_token = token_manager.refresh_token(
                        token
                    )
                    request.state.new_access_token = new_access_token
                    request.state.new_refresh_token = new_refresh_token
                    response = await call_next(request)
                    response.headers["X-New-Access-Token"] = new_access_token
                    response.headers["X-New-Refresh-Token"] = new_refresh_token
                    return response
            except HTTPException:
                # 如果验证失败，不中断请求，让后续的认证中间件处理
                pass

        # 在所有其他情况下，继续处理请求并返回响应
        return await call_next(request)
