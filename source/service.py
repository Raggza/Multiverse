from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

# from source.modules.chatbot import Chatbot
from source.utils.log_utils import get_logger
from source.schemas.input import CharacterInput
from source.pipeline import Pipeline

app = FastAPI()
# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to specific origins if needed
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Create an APIRouter
api_router = APIRouter(prefix="/api/v1")  # Create an APIRouter

pipeline = Pipeline()  # Initialize your chatbot instance
logger = get_logger(__file__)


@api_router.post("/image_generation")
async def get_answer(request_data: CharacterInput):  # Use Pydantic model here
    try:
        response = pipeline.invoke(request_data)
        return {
            "status": 200,
            "content": response,
        }

    except Exception as e:
        logger.error(f"Error processing request: {e}")
        return {
            "status": 500,
            "content": "An error occurred while processing your request.",
        }

app.include_router(api_router)  # Include the APIRouter in your FastAPI app

