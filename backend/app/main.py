from fastapi import FastAPI

app = FastAPI(
    title="AI Manim Studio",
    description="AI-powered educational animation generation platform",
    version="0.1.0",
)


@app.get("/")
def health_check():
    return {"status": "ok"}