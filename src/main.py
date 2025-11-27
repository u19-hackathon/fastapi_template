from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get("/")
async def root():
    html_content = '<h2>Hello gays!</h2>'
    return HTMLResponse(content=html_content, status_code=200)
