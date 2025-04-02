from fastapi import FastAPI
from routers import customer_routes, trainer_routes, owner_routes
from database import engine, Base
from fastapi.responses import PlainTextResponse
from fastapi.responses import HTMLResponse

# Creating all database tables
Base.metadata.create_all(bind=engine)

app= FastAPI()

# Including routers for API endpoint
app.include_router(customer_routes.router, prefix="/customer", tags=["Customer"])
app.include_router(trainer_routes.router, prefix="/trainer", tags=["Trainer"])
app.include_router(owner_routes.router, prefix="/owner", tags=["Owner"])

@app.get("/health", response_class=PlainTextResponse)
def health_check(): 
    """
    Health check endpoint to verify if the server is running.
    """
    return "Fitness Management System is running!"



@app.get("/", response_class=HTMLResponse)
def home():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Fitness Management System</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f9;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }
            .container {
                text-align: center;
                padding: 20px;
                background: linear-gradient(135deg, #32a852, #3284a8);
                border-radius: 8px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                animation: fadeIn 2s ease-in-out;
            }
            h1 {
                color: #ffffff;
            }
            p {
                color: #e0e0e0;
            }
            @keyframes fadeIn {
                from {
                    opacity: 0;
                    transform: scale(0.9);
                }
                to {
                    opacity: 1;
                    transform: scale(1);
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Welcome to the Fitness Management System</h1>
            <p>Your one-stop solution for managing fitness goals!</p>
        </div>
    </body>
    </html>
    """
    return html_content # returned HTML content
