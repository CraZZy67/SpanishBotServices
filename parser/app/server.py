from fastapi import FastAPI
from fastapi.responses import Response

from parser_ import Parser


app = FastAPI(debug=True)

@app.get('/get_video/')
def get_content():
    return Response(content=Parser.get_video(), media_type='video/mp4')