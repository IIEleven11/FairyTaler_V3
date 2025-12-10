# FairyTaler Pose Image Selector

A simple ComfyUI custom node that takes a keyword, matches it to a folder inside `poses/`, selects a random image from that folder, and outputs it as an `IMAGE`. If a `.txt` file with the same basename as the chosen image exists, its contents are also output as a `STRING` prompt.

## Location
- Base poses directory: `K:\PROJECTS\SillyTavern-Launcher\image-generation\ComfyUI\custom_nodes\ComfyUI_FairyTaler_v2\poses`

## Inputs
- `keyword` (string): Folder name to match (e.g., `cuddle`).
- `match_mode` (enum): `exact` or `case-insensitive` name matching.
- `fallback_to_any` (boolean): If no match is found, pick a random folder.
- `seed` (int): Seed for deterministic random selection.
- `choose_from` (optional enum): Directly pick a folder from discovered options.

## Output
- `image` (`IMAGE`): A ComfyUI-compatible image tensor ([1, H, W, C], float32, 0..1).
- `prompt` (`STRING`): Contents of a `.txt` file with the same basename as the selected image (empty if absent).

## Usage
1. Place this folder under `ComfyUI/custom_nodes`.
2. Start ComfyUI. The node appears under category `FairyTaler/Poses` as `FairyTaler Pose Image Selector`.
3. Provide a `keyword` (e.g., `cuddle`). If a matching folder exists in `poses/`, a random image from that folder will be loaded and output. If a corresponding `.txt` is present (e.g., `image1.png` + `image1.txt`), its text will be returned in the second output which you can connect to a `CLIP Text Encode (Positive)` node.

## Notes
- Supported image formats: PNG, JPG/JPEG, WEBP, BMP.
- If the folder is empty or contains no supported files, the node raises an error.
- Non-RGB images are converted to RGB automatically.
 - Text files are read using UTF-8 with errors ignored; if not found or unreadable, `prompt` will be empty.

## Troubleshooting
- If the node does not appear, ensure the `.py` file is inside `custom_nodes/ComfyUI_FairyTaler_v2/` and ComfyUI has been restarted.
- Verify Windows path escaping if editing paths; this project uses raw string literals for Windows compatibility.