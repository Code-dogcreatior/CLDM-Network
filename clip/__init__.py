from transformers import CLIPProcessor, CLIPVisionModel
from modules import devices

version = 'openai/clip-vit-large-patch14'
clip_proc = None
clip_vision_model = None

def apply_clip(img):
    global clip_proc, clip_vision_model
    
    if clip_vision_model is None:
        clip_proc = CLIPProcessor.from_pretrained(version)
        clip_vision_model = CLIPVisionModel.from_pretrained(version)
        
    clip_vision_model = clip_vision_model.to(devices.get_device_for("controlnet"))
    style_for_clip = clip_proc(images=img, return_tensors="pt")['pixel_values']
    style_feat = clip_vision_model(style_for_clip.to(devices.get_device_for("controlnet")))['last_hidden_state']
    return style_feat

def unload_clip_model():
    global clip_proc, clip_vision_model
    if clip_vision_model is not None:
        clip_vision_model.cpu()