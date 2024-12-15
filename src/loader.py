import uvicorn

from core.fastapi_factory import create_app

app = create_app()


if __name__ == "__main__":
    uvicorn.run(
        "loader:app",
        host="0.0.0.0",
        port=5555,
        reload=True,
    )
