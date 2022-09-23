import torch
from torch import autocast
from diffusers import StableDiffusionPipeline
from PIL import Image
import constant

def get_diffusion_image(string):
    experimental_pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4", revision="fp16",
                                                                torch_dtype=torch.float16, use_auth_token=True)
    experimental_pipe = experimental_pipe.to("cuda")

    with autocast("cuda"):
        image_1 = experimental_pipe(string, height=constant.png_px_size, width=constant.png_px_size).images[0]

    return image_1