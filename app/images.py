from dotenv import load_dotenv
import os
from imagekitio import ImageKit

load_dotenv()
print("ImageKit client initialized")

imagekit = ImageKit(
    public_key=os.environ["IMAGEKIT_PUBLIC_KEY"],
    private_key=os.environ["IMAGEKIT_PRIVATE_KEY"],
    url_endpoint=os.environ["IMAGEKIT_URL_ENDPOINT"],
)

# imagekit = ImageKit(
#         "publicKey": os.environ["IMAGEKIT_PUBLIC_KEY"],
#         "privateKey": os.environ["IMAGEKIT_PRIVATE_KEY"],
#         "urlEndpoint": os.environ["IMAGEKIT_URL_ENDPOINT"]
# )