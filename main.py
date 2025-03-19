from src.app import app
from src.utils.config import Config

import uvicorn

settings = Config()


if __name__ == '__main__':
    uvicorn.run(app, host=settings.host, port=settings.port)
