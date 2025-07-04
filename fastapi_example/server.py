import contextlib
from fastapi import FastAPI, HTTPException
from echo_server import mcp as echo_mcp
from calculator_server import mcp as calculator_app
from dotenv import load_dotenv
import os

load_dotenv()

PORT = os.getenv("PORT", 10000)

# Cria um lifespan combinado para orquestra os dois gerenciadores de sessao
@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    async with contextlib.AsyncExitStack() as stack:
        await stack.enter_async_context(echo_mcp.session_manager.run())
        await stack.enter_async_context(calculator_app.session_manager.run())
        yield
        
        
app = FastAPI(lifespan=lifespan)
app.mount("/echo", echo_mcp.streamable_http_app())
app.mount("/calculator", calculator_app.streamable_http_app())


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)


# para conectar o mcp deve usar  a seguinte url
# inspector:
#  - http://0.0.0.0:8080/calculator/mcp
#  - http://0.0.0.0:8080/echo/mcp
# aplicações:
#  - http://0.0.0.0:8080/calculator/mcp/
#  - http://0.0.0.0:8080/echo/mcp/