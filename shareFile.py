from fastapi import FastAPI, WebSocket, HTTPException
import os
import json
from pathlib import Path
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel
import aiofiles  
app = FastAPI()
uplaod_dir: str     = "./uploads"
download_dir: str   = "./donwloads"
html_file_path: str = "./root.html"

os.makedirs(uplaod_dir, exist_ok=True)  # Ensure the upload directory exists
os.makedirs(download_dir, exist_ok=True)  # Ensure the download directory exists

class FileUploadInfo(BaseModel):
    filename: str
    totalChunks: int

class FileInfo(BaseModel):
    filename: str
    file_size: int

@app.get("/")
def root():
    return FileResponse(html_file_path)

@app.get("/files_for_upload")
async def get_files_info()-> list[FileInfo]:
    file_info_list = []
    for filename in os.listdir(uplaod_dir):
        file_path = os.path.join(uplaod_dir, filename)
        if os.path.isfile(file_path): # Check if it is a file (not a folder)
            file_size = os.path.getsize(file_path)
            file_info = FileInfo(filename=filename, file_size=file_size)
            file_info_list.append(file_info)
    return file_info_list

async def file_iterator(file_path: Path, chunk_size=4*1024*1024):  # 4MB chunks
    """Asynchronously yield chunks of the file to stream it efficiently."""
    async with aiofiles.open(file_path, "rb") as file:
        while chunk := await file.read(chunk_size):
            yield chunk

@app.get("/download/{filename}")
async def download_file(filename: str) ->StreamingResponse:
    """
    HTTP download handler that serves large files from the server with asynchronous streaming.
    """
    file_path = Path(uplaod_dir) / filename
    # Check if the file exists
    if not file_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")

    # Get the total file size
    file_size = os.path.getsize(file_path)

    # Return a streaming response with the file size included in the headers
    return StreamingResponse(
        file_iterator(file_path), 
        media_type="application/octet-stream",
        headers={
            "Content-Disposition": f"attachment; filename={filename}",
            "Content-Length": str(file_size)  # Inform the client of the file size
        }
    )

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    total_chunks = 0

    # Step 1: Receive metadata (file name and total chunk count)
    message: str = await websocket.receive_text()
    file_info: FileUploadInfo = FileUploadInfo(**json.loads(message))
    filename: str = file_info.filename
    total_chunks: int = file_info.totalChunks

    file_path = Path(download_dir) / filename

    # Step 2: Open the file asynchronously and reading the chunks one by one
    async with aiofiles.open(file_path, "wb") as f:
        for chunk_index in range(total_chunks):
            chunk = await websocket.receive_bytes()  # Receive binary chunk

            if chunk:
                await f.write(chunk)  # Write chunk asynchronously

            # After receiving each chunk, send progress to frontend-side
            progress = (chunk_index + 1) / total_chunks * 100
            await websocket.send_text(json.dumps({"status": "uploading", "progress": progress}))

    # Step 3: Send confirmation to the client
    await websocket.send_text(json.dumps({"status": "complete", "filePath": str(file_path)}))
    await websocket.close()
