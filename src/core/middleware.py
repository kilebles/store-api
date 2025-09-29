from fastapi.middleware.cors import CORSMiddleware

def use_middleware(app, origins: list[str]) -> None:
    """
    Подключает CORS-мидлварь, если задан список разрешённых источников.
    """
    
    if origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
