from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from video_stream import get_stream_video

app = FastAPI()

@app.get('/video')
def main():
    return StreamingResponse(get_stream_video(), media_type="multipart/x-mixed-replace; boundary=frame")