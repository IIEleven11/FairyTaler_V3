"""
ComfyUI custom nodes package init.
This file ensures nodes are registered when the folder is loaded by ComfyUI.
"""

# Import node modules to expose their mappings
from .pose_image_selector import (
    NODE_CLASS_MAPPINGS as POSE_NODE_CLASS_MAPPINGS,
    NODE_DISPLAY_NAME_MAPPINGS as POSE_NODE_DISPLAY_NAME_MAPPINGS,
)


# Aggregate mappings so ComfyUI can discover everything from this package
NODE_CLASS_MAPPINGS = {}
NODE_CLASS_MAPPINGS.update(POSE_NODE_CLASS_MAPPINGS)

NODE_DISPLAY_NAME_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS.update(POSE_NODE_DISPLAY_NAME_MAPPINGS)
