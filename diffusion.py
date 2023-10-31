import torch
from torch import autocast
from diffusers import StableDiffusionPipeline
import constant

def get_diffusion_image(string):
    experimental_pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4", revision="fp16",
                                                                torch_dtype=torch.float16, use_auth_token=True)
    try:
        experimental_pipe = experimental_pipe.to("cuda")
    except Exception as e:
        experimental_pipe = experimental_pipe.to("cpu")
        
    with autocast("cuda"):
        image = experimental_pipe(string, height=constant.png_px_size, width=constant.png_px_size).images[0]

    return image
