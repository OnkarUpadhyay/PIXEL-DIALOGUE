from langchain.tools import tool
from langchain_tavily import TavilySearch
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
from ultralytics import YOLO
from PIL import Image
from diffusers import StableDiffusionPipeline
from accelerate import Accelerator
import easyocr
import cv2
import uuid
from datetime import datetime
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file
os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")


# ------------- For web search tool -------------

@tool("tavily_search", description="Useful for searching information on the web")
def tavily_search(query: str) -> str:
    """Search for information on the web."""
    tavily_search_tool = TavilySearch(
        api_key=os.getenv("TAVILY_API_KEY"),
        max_results=10,
        topic="general",
    )
    response = tavily_search_tool.invoke(query)
    return response

# ------------- For image caption  -------------

@tool("image_caption_tool", description="Useful for captioning images")
def image_caption_tool(image_path: str) -> str:
    """Generate a short caption for the provided image."""
    
    image = Image.open(image_path).convert("RGB")

    model_name = "Salesforce/blip-image-captioning-large"
    device = "cuda" if torch.cuda.is_available() else "cpu"

    processor = BlipProcessor.from_pretrained(model_name, use_fast = True)
    model = BlipForConditionalGeneration.from_pretrained(model_name).to(device)

    inputs = processor(image, return_tensors="pt").to(device)
    output = model.generate(**inputs, max_new_tokens = 20)

    caption = processor.decode(output[0], skip_special_tokens=True)

    return str(caption)

# ------------- For object detection -------------

@tool("object_detection_tool", description="Detect objects in an image")
def object_detection_tool(image_path: str) -> str:
    """Detect objects in the provided image and return a summary """
    
    model = YOLO("yolo11s.pt")
    results = model(image_path)
    
    detections = []
    for result in results:
        for box in result.boxes:
            class_name = model.names[int(box.cls[0])]
            conf = round(float(box.conf[0]), 2)
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            detections.append(f"(class: {class_name}, confidence: {conf}, bounding box: {x1, y1, x2, y2};)")   
    
    final_detection = str(detections)
    if not detections:
        return "No objects detected in the image."

    return final_detection

# ------------- For image generation -------------


_GEN_DIR = Path(".gen")  # align with your Streamlit app
_GEN_DIR.mkdir(exist_ok=True)

def _unique_gen_path(stem: str = "gen", ext: str = ".png") -> Path:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    return _GEN_DIR / f"{stem}_{ts}_{uuid.uuid4().hex[:6]}{ext}"



@tool("image_generation_tool", description = "Useful for generating images")
def image_generation_tool(prompt: str) -> str:

    """
    Useful for generating images based on a text prompt.
    Input should be a descriptive prompt of the image you want to create.
    Returns the exact local file path (under ./.gen).
    """

    # 1) Init accelerator & model
    accelerator = Accelerator(mixed_precision="fp16")
    device = accelerator.device

    pipe = StableDiffusionPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5",
        torch_dtype=torch.float16
    )
    pipe = pipe.to(device)
    pipe.enable_attention_slicing()

    # 2) Generate image with autocast for VRAM optimization
    autocast_ctx = accelerator.autocast()
    
    with autocast_ctx:
        result = pipe(prompt=prompt, height=512, width=512)
        image: Image.Image = result.images[0]

    # 3) Save under ./.gen with a unique filename
    out_path = _unique_gen_path(stem="generated", ext=".png")
    image.save(out_path)

    # 4) Cleanup VRAM & objects
    try:
        del pipe
        torch.cuda.empty_cache()
    except Exception:
        pass

    # 5) Return absolute path as string
    return str(out_path.resolve())


@tool("extract_text_tool", description = "Useful for extracting text from images")
def extract_text_tool(image_path: str) -> str:
    """Extract text from the provided image using OCR"""
    # Initialize reader
    reader = easyocr.Reader(['en'])
    
    # Load image with OpenCV
    img = cv2.imread(image_path)
    
    # Convert to grayscale
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Run OCR
    results = reader.readtext(img_gray)
    
    # Extract text
    lines = [res[1] for res in results if res[1].strip()]
    text = " ".join(lines)
    
    return text


if __name__ == "__main__":
    test_image_path = r"C:\Users\onkar\Downloads\coffee-vintage-retro-poster-15913361747bD.jpg"
    # Test the tools
    #print(tavily_search("What is the capital of France?"))
    #print(image_caption_tool(test_image_path))
    #print(object_detection_tool(test_image_path))
    #print(image_generation_tool("A futuristic cityscape at sunset"))
    #print(extract_text_tool(test_image_path))
    