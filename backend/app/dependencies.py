from fastapi import Depends, Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt
from app.config import config
import datetime
from uuid import UUID
from app.utils.logger import get_logger

logger = get_logger(__name__)

security = HTTPBearer()


class TokenManager:
    def __init__(self):
        self.secret_key = config.JWT_SECRET_KEY.get_secret_value()
        self.algorithm = config.JWT_ALGORITHM

    def create_access_token(self, user_id: UUID | str) -> str:
        """创建访问令牌"""
        payload = {
            "sub": str(user_id),
            "exp": datetime.datetime.now(datetime.timezone.utc)
            + datetime.timedelta(minutes=config.JWT_ACCESS_TOKEN_EXPIRE_MINUTES),
            "type": "access",
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def create_refresh_token(self, user_id: UUID | str) -> str:
        """创建刷新令牌"""
        payload = {
            "sub": str(user_id),
            "exp": datetime.datetime.now(datetime.timezone.utc)
            + datetime.timedelta(days=config.JWT_REFRESH_TOKEN_EXPIRE_DAYS),
            "type": "refresh",
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def verify_token(self, token: str, token_type: str = "access") -> dict:
        """验证令牌并返回payload"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            if payload.get("type") != token_type:
                raise HTTPException(
                    status_code=401, detail=f"无效的令牌类型: 需要 {token_type} 令牌"
                )
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="令牌已过期")
        except jwt.JWTError:
            raise HTTPException(status_code=401, detail="无效的令牌")

    def decode_token(self, token: str) -> str:
        """解码令牌 如果解码失败返回游客"""
        try:
            res = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return res.get("sub")
        except jwt.JWTError:
            return "游客"

    def refresh_token(self, refresh_token: str) -> tuple[str, str]:
        """使用刷新令牌创建新的访问令牌和刷新令牌"""
        payload = self.verify_token(refresh_token, token_type="refresh")
        user_id = UUID(payload.get("sub"))
        new_access_token = self.create_access_token(user_id)
        new_refresh_token = self.create_refresh_token(user_id)
        return new_access_token, new_refresh_token


token_manager = TokenManager()


def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
) -> UUID:
    if not credentials:
        return None

    token = None
    if hasattr(request.state, "new_access_token"):
        token = request.state.new_access_token
    try:
        if not token:
            token = credentials.credentials
        payload = jwt.decode(
            token,
            config.JWT_SECRET_KEY.get_secret_value(),
            algorithms=[config.JWT_ALGORITHM],
        )
        user_id = UUID(payload.get("sub"))
        return user_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="授权已过期")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="无效的授权")
