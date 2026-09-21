from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import pyotp
import qrcode
import io
import base64
from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.models.mfa import MFAModel
from app.core.responses import api_response

router = APIRouter()

@router.post("/setup")
async def setup_mfa(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    secret = pyotp.random_base32()
    
    # Store secret in DB
    mfa = MFAModel(user_id=current_user.id, secret=secret)
    db.add(mfa)
    await db.commit()
    
    # Generate QR Code
    uri = pyotp.totp.TOTP(secret).provisioning_uri(name=current_user.email, issuer_name="SentinelAuth")
    img = qrcode.make(uri)
    buf = io.BytesIO()
    img.save(buf)
    qr_b64 = base64.b64encode(buf.getvalue()).decode()
    
    return api_response(status="success", data={"qr_code_b64": qr_b64, "secret": secret})
