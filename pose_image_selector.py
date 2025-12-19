import os
import random
from typing import List, Tuple

import numpy as np
import torch
from PIL import Image


# Base poses directory (fixed as per instructions)
POSES_DIR = r"K:\PROJECTS\SillyTavern-Launcher\image-generation\ComfyUI\custom_nodes\ComfyUI_FairyTaler_v2\poses"


def _list_folders(base_dir: str) -> List[str]:
    try:
        return [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]
    except Exception:
        return []


def _list_images(folder_path: str) -> List[str]:
    exts = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}
    files = []
    try:
        for name in os.listdir(folder_path):
            fp = os.path.join(folder_path, name)
            if os.path.isfile(fp) and os.path.splitext(name)[1].lower() in exts:
                files.append(fp)
    except Exception:
        pass
    return files


def _pil_to_comfy(image: Image.Image):
    """Convert PIL image to ComfyUI IMAGE tensor format: torch.float32 [1,H,W,C] in range 0..1."""
    if image.mode != "RGB":
        image = image.convert("RGB")
    arr = np.array(image).astype(np.float32) / 255.0  # H,W,C
    arr = np.expand_dims(arr, axis=0)  # 1,H,W,C
    tensor = torch.from_numpy(arr)  # on CPU by default
    return tensor


class FairyTalerPoseImageSelector:
    """
    ComfyUI node: Given a keyword, looks for a matching folder in POSES_DIR.
    If found, loads a random image from that folder and outputs it as IMAGE.
    """

    @classmethod
    def INPUT_TYPES(cls):
        # Provide available folder names for convenience in the UI as an enum, plus free text
        folders = _list_folders(POSES_DIR)
        return {
            "required": {
                "keyword": ("STRING", {"default": "cuddle", "multiline": False}),
                "match_mode": ("STRING", {"default": "exact", "choices": ["exact", "case-insensitive"]}),
                "fallback_to_any": ("BOOLEAN", {"default": True}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 2**31 - 1}),
            },
        }

    RETURN_TYPES = ("IMAGE", "STRING")
    RETURN_NAMES = ("image", "prompt")
    FUNCTION = "select"
    CATEGORY = "FairyTaler/Poses"

    def select(self, keyword: str, match_mode: str = "exact", fallback_to_any: bool = True, seed: int = 0):
        rng = random.Random(seed) if seed else random.Random()

        # Resolve target folder by keyword
        folders = _list_folders(POSES_DIR)
        target = None

        # Clean keyword: strip whitespace/newlines, replace spaces with underscores, and lowercase (snake_case)
        key = keyword.strip().replace(" ", "_").lower()
        
        for d in folders:
            if match_mode == "exact":
                if d == key:
                    target = d
                    break
            else:  # case-insensitive
                if d.lower() == key:
                    target = d
                    break

        # Fallback to any folder if requested
        if target is None and fallback_to_any and folders:
            target = rng.choice(folders)

        if target is None:
            # No folders found or no match without fallback
            raise ValueError(f"No matching folder for keyword '{keyword}'. Available: {folders}")

        folder_path = os.path.join(POSES_DIR, target)
        images = _list_images(folder_path)
        if not images:
            raise ValueError(f"Folder '{target}' contains no supported image files.")

        img_path = rng.choice(images)
        # Load image with PIL
        with Image.open(img_path) as im:
            im.load()
            image_tensor = _pil_to_comfy(im)
        # Load corresponding .txt prompt if present (same stem)
        stem, _ = os.path.splitext(os.path.basename(img_path))
        txt_path = os.path.join(folder_path, f"{stem}.txt")
        prompt_text = ""
        try:
            if os.path.isfile(txt_path):
                with open(txt_path, "r", encoding="utf-8", errors="ignore") as f:
                    prompt_text = f.read().strip()
        except Exception:
            # If reading fails, keep prompt empty
            prompt_text = ""

        return (image_tensor, prompt_text)


NODE_CLASS_MAPPINGS = {
    "FairyTalerPoseImageSelector": FairyTalerPoseImageSelector,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "FairyTalerPoseImageSelector": "FairyTaler Pose Image Selector",
}
