from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, PlainTextResponse
import json
import os

app = FastAPI()

# Enable CORS for all origins (matching previous behavior)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

JSON_FILE = 'participants_master.json'

@app.get("/", response_class=PlainTextResponse)
def health_check():
    """Health check endpoint for Render monitoring."""
    return "AX26 Sync Server is Online."

@app.post("/save-json")
async def save_json(request: Request):
    """Saves the dashboard state to participants_master.json."""
    try:
        data = await request.json()
        # Ensure the file exists or create it
        with open(JSON_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        
        print(f"[*] Updated {JSON_FILE} with current dashboard state.")
        return {"status": "success", "message": f"Data written to {JSON_FILE}"}
    except Exception as e:
        print(f"[!] Error saving data: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    # Render and other platforms provide PORT environment variable
    PORT = int(os.environ.get('PORT', 8000))
    uvicorn.run(app, host="0.0.0.0", port=PORT)
