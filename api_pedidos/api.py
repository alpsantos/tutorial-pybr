from http import HTTPStatus
from uuid import UUID

from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse

from api_pedidos.esquema import ErrorResponse, HealthCheckResponse, Item
from api_pedidos.excecao import PedidoNaoEncontradoError

app = FastAPI()


def recuperar_itens_por_pedido(identificacao_do_pedido: UUID) -> list[Item]:
    pass


@app.exception_handler(PedidoNaoEncontradoError)
def tratar_erro_pedido_nao_encontrado(
    request: Request, exc: PedidoNaoEncontradoError
):
    return JSONResponse(
        status_code=HTTPStatus.NOT_FOUND,
        content={"message": "Pedido não encontrado"},
    )


@app.get(
    "/healthcheck",
    tags=["healthcheck"],
    summary="Integridade do sistema",
    description="Checa se o servidor está online",
    response_model=HealthCheckResponse,
)
async def healthcheck():
    return HealthCheckResponse(status="ok")


@app.get(
    "/orders/{identificacao_do_pedido}/items",
    responses={
        HTTPStatus.NOT_FOUND.value: {
            "description": "Pedido não encontrado",
            "model": ErrorResponse,
        },
        HTTPStatus.BAD_GATEWAY.value: {
            "description": "Falha de comunicação com o servidor remoto",
            "model": ErrorResponse,
        },
    },
    tags=["pedidos"],
    summary="Itens de um pedido",
    description="Retorna todos os itens de um determinado pedido",
    response_model=list[Item],
)
def listar_itens(itens: list[Item] = Depends(recuperar_itens_por_pedido)):
    return itens
