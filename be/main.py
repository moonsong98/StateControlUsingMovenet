import uvicorn
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from video_stream import get_stream_video
from starlette.middleware.cors import CORSMiddleware


app = FastAPI()
origins = [
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/video')
async def main():
    return StreamingResponse(get_stream_video(), media_type="multipart/x-mixed-replace; boundary=frame")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)