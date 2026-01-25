from dotenv import load_dotenv
import os
from imagekitio import ImageKit

load_dotenv()

imagekit = ImageKit(
    private_key=os.environ["IMAGEKIT_PRIVATE_KEY"],
    base_url =os.environ["IMAGEKIT_URL_ENDPOINT"]
)
