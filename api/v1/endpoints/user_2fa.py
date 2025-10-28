from fastapi import APIRouter, Depends, Response, Query, Body, status
from fastapi.responses import JSONResponse
from core.deps import get_db
from services.User_service import UserService
import base64
from schemas.user_schema import UserCreate, RecoveryRequest

router = APIRouter(prefix="/2fa", tags=["2FA"], responses={
        404: {"description": "Recurso não encontrado"},
        400: {"description": "Erro na requisição"},
        500: {"description": "Erro interno no servidor"}
    })

@router.post(
        "/setup",
        summary="Configura o 2FA para um novo usuário",
    description="""
    Gera um novo *secret* e um QR Code compatível com Google Authenticator,
    junto com **códigos de recuperação**.

    - O `identifier` pode ser e-mail, username ou ID interno.
    - Retorna o QR code (base64) e os códigos de recuperação.
    """,
    response_description="Retorna QR Code (em Base64) e códigos de recuperação.",
    status_code=status.HTTP_201_CREATED
)
async def setup_2fa(user: UserCreate = Body(
        ...,
        example={"identifier": "mateus123"}), db=Depends(get_db)):
    """
    Gera o secret e o QRCode de configuração do 2FA para um usuário.
    """
    service = UserService(db)
    data = await service.register_user(user.identifier)
    # response.headers["Content-Type"] = data["media_type"]
    # return Response(content=data["qrcode"], media_type=data["media_type"])
    qrcode_base64 = base64.b64encode(data["qrcode"]).decode("utf-8")

    return JSONResponse(content={
        "qrcode": qrcode_base64,
        "media_type": data["media_type"],
        "recovery": data["recovery"]
    }, status_code=201)


@router.get("/verify",
    summary="Verifica o código de autenticação 2FA",
    description="""
    Valida um código TOTP (Time-based One-Time Password) gerado no app autenticador.

    - O código expira a cada 30 segundos.
    - Retorna `success` se o código for válido.
    """,
    response_description="Retorna o status da verificação."
)
async def verify_2fa(
    identifier: str = Query(..., description="Identificador do usuário."),
    code: str = Query(..., description="Código TOTP do autenticador."), 
    db=Depends(get_db)
):
    service = UserService(db)
    return await service.verify_2fa(identifier, code)


@router.patch("/recovery/generate",
    summary="Valida um código de recuperação",
    description="""
    Valida um código de recuperação e o remove da lista de válidos.
    Use esta rota caso o usuário tenha **perdido o acesso ao app autenticador**.

    - Após validar, o código não poderá ser reutilizado.
    """,
    response_description="Retorna o status da verificação.")
async def regenerate_recovery(req: RecoveryRequest= Body(
        ...,
        example={"identifier": "mateus123", "code": "ABC123XYZ"}
    ), db=Depends(get_db)):
    service = UserService(db)
    return await service.verify_recovery(req.identifier, req.code)
