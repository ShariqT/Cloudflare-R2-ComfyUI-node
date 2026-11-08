from inspect import cleandoc
import boto3
import io
import uuid
from datetime import datetime


class R2CloudUpload:
    """
    Uploads an image to Cloudflare R2 bucket and returns the public URL.
    """

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        """
        Return a dictionary which contains config for all input fields.
        """
        return {
            "required": {
                "image": ("IMAGE", {"tooltip": "The image to upload to R2"}),
                "bucket_name": ("STRING", {
                    "tooltip": "The name of the R2 bucket",
                    "default": ""
                }),
                "account_id": ("STRING", {
                    "tooltip": "Cloudflare account ID",
                    "default": ""
                }),
                "access_key_id": ("STRING", {
                    "tooltip": "R2 access key ID",
                    "default": ""
                }),
                "secret_access_key": ("STRING", {
                    "tooltip": "R2 secret access key",
                    "default": ""
                }),
                "public_url_base": ("STRING", {
                    "tooltip": "The public URL base for accessing the uploaded file (e.g., https://pub-xxx.r2.dev)",
                    "default": ""
                }),
            },
            "optional": {
                "file_name": ("STRING", {
                    "tooltip": "Custom filename (optional, will auto-generate if empty)",
                    "default": ""
                }),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("url",)
    DESCRIPTION = cleandoc(__doc__)
    FUNCTION = "upload"

    OUTPUT_NODE = True

    CATEGORY = "image"

    def upload(self, image, bucket_name, account_id, access_key_id, secret_access_key, public_url_base, file_name=""):
        """
        Upload an image to Cloudflare R2 bucket.

        Args:
            image: The image tensor from ComfyUI
            bucket_name: The R2 bucket name
            account_id: Cloudflare account ID
            access_key_id: R2 access key ID
            secret_access_key: R2 secret access key
            public_url_base: The public URL base for accessing the file
            file_name: Optional custom filename

        Returns:
            tuple: The public URL of the uploaded file
        """
        # Validate required parameters
        if not all([bucket_name, account_id, access_key_id, secret_access_key]):
            raise ValueError("All R2 credentials (bucket_name, account_id, access_key_id, secret_access_key) are required")

        # Convert image tensor to PIL Image
        import torch
        from PIL import Image
        import numpy as np

        # ComfyUI images are torch tensors in the format (batch, height, width, channels)
        # We take the first image from the batch
        if isinstance(image, torch.Tensor):
            image_np = image[0].cpu().numpy()
        else:
            image_np = image[0]

        # Convert from float [0, 1] to uint8 [0, 255]
        if image_np.dtype == np.float32 or image_np.dtype == np.float64:
            image_np = (image_np * 255).astype(np.uint8)

        # Create PIL Image
        pil_image = Image.fromarray(image_np)

        # Generate filename if not provided
        if not file_name:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            unique_id = str(uuid.uuid4())[:8]
            file_name = f"image_{timestamp}_{unique_id}.png"

        # Ensure filename has extension
        if not file_name.endswith(('.png', '.jpg', '.jpeg', '.webp')):
            file_name += '.png'

        # Save image to bytes buffer
        buffer = io.BytesIO()
        pil_image.save(buffer, format='PNG')
        buffer.seek(0)

        # Create S3 client for R2
        s3_client = boto3.client(
            's3',
            endpoint_url=f'https://{account_id}.r2.cloudflarestorage.com',
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
            region_name='auto'
        )

        # Upload the file
        s3_client.put_object(
            Bucket=bucket_name,
            Key=file_name,
            Body=buffer,
            ContentType='image/png'
        )

        # Construct the public URL
        if public_url_base:
            # Remove trailing slash if present
            public_url_base = public_url_base.rstrip('/')
            url = f"{public_url_base}/{file_name}"
        else:
            # Fallback to R2.dev URL format
            url = f"https://{bucket_name}.{account_id}.r2.dev/{file_name}"

        return (url,)


# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "R2CloudUpload": R2CloudUpload
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "R2CloudUpload": "R2 Cloud Upload"
}
