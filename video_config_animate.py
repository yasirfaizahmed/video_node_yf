# custom_nodes/video_config_animate.py
import re

try:
    from server import PromptServer
except Exception:
    PromptServer = None


class VideoConfig:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "preset": ([
                	"640x352",
                	"960x544",
                    "1280x720",
                    "1536x864",
                    "1920x1080",
                ], {"default": "1280x720"}),
                "custom_width":  ("INT", {"default": 0, "min": 0, "max": 8192, "step": 8}),
                "custom_height": ("INT", {"default": 0, "min": 0, "max": 8192, "step": 8}),
                "invert":        ("BOOLEAN", {"default": False}),
                "custom_frames": ("INT", {"default": 0, "min": 0, "max": 100000, "step": 1}),
                "fps":           ("INT", {"default": 30, "min": 1, "max": 240, "step": 1}),
                "frame_load_cap":    ("INT", {"default": 0, "min": 0, "max": 100000, "step": 1}),
                "skip_first_frames": ("INT", {"default": 0, "min": 0, "max": 100000, "step": 1}),
            },
            "hidden": {
                "unique_id": "UNIQUE_ID",
            },
        }

    RETURN_TYPES = ("INT", "INT", "INT", "FLOAT", "INT", "INT")
    RETURN_NAMES = ("width", "height", "frame_count", "fps", "frame_load_cap", "skip_first_frames")
    FUNCTION = "select"
    CATEGORY = "utils"

    def select(self, preset, custom_width, custom_height, custom_frames, fps, invert, frame_load_cap, skip_first_frames, unique_id=None):
        # Parse preset resolution
        m = re.match(r"^(\d+)x(\d+)$", preset)
        if not m:
            raise ValueError(f"Invalid preset format: {preset}")
        w, h = int(m.group(1)), int(m.group(2))
        f = 150  # Default frame count

        # Override with custom values
        if custom_width  > 0: w = custom_width
        if custom_height > 0: h = custom_height
        if custom_frames > 0: f = custom_frames

        # Invert width/height
        if invert:
            w, h = h, w

        return (w, h, f, float(fps), frame_load_cap, skip_first_frames)


NODE_CLASS_MAPPINGS = {
    "VideoConfigAnimate": VideoConfig
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "VideoConfigAnimate": "Video Config (Animate)"
}
