from app import init_app

app = init_app()

@app.get("/")
async def index():
    return {'message': 'OK!'}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)