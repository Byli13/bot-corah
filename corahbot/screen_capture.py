"""
Screen capture utility for selecting trigger images
"""

import os
import time
from datetime import datetime
from PIL import Image
import numpy as np
from airtest.core.api import snapshot
from airtest.core.helper import G
from corahbot.config import IMG_DIR
from corahbot.logger import get_logger

log = get_logger(__name__)

class ScreenCapture:
    """Handles screen capture and template image creation"""
    
    def __init__(self):
        self.img_dir = IMG_DIR
        os.makedirs(self.img_dir, exist_ok=True)
        
    def capture_screen(self, name: str = None) -> str:
        """
        Capture the current screen and save it as a template
        
        Args:
            name: Optional name for the template image
            
        Returns:
            str: Path to the saved image
        """
        try:
            # Take screenshot using Airtest
            screen = snapshot()
            
            # Convert to PIL Image
            screen_pil = Image.fromarray(np.uint8(screen))
            
            # Generate filename
            if name is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"template_{timestamp}.png"
            else:
                filename = f"{name}.png"
            
            filepath = os.path.join(self.img_dir, filename)
            
            # Save image
            screen_pil.save(filepath)
            log.info(f"Screen captured and saved as: {filepath}")
            
            return filepath
            
        except Exception as e:
            log.error(f"Failed to capture screen: {str(e)}")
            raise
            
    def capture_region(self, x1: int, y1: int, x2: int, y2: int, name: str = None) -> str:
        """
        Capture a specific region of the screen
        
        Args:
            x1, y1: Top-left corner coordinates
            x2, y2: Bottom-right corner coordinates
            name: Optional name for the template image
            
        Returns:
            str: Path to the saved image
        """
        try:
            # Take screenshot
            screen = snapshot()
            
            # Crop the region
            region = screen[y1:y2, x1:x2]
            
            # Convert to PIL Image
            region_pil = Image.fromarray(np.uint8(region))
            
            # Generate filename
            if name is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"region_{timestamp}.png"
            else:
                filename = f"{name}.png"
                
            filepath = os.path.join(self.img_dir, filename)
            
            # Save image
            region_pil.save(filepath)
            log.info(f"Region captured and saved as: {filepath}")
            
            return filepath
            
        except Exception as e:
            log.error(f"Failed to capture region: {str(e)}")
            raise
            
    def capture_sequence(self, interval: float = 1.0, count: int = 5, prefix: str = "seq") -> list:
        """
        Capture a sequence of screenshots at regular intervals
        
        Args:
            interval: Time between captures in seconds
            count: Number of screenshots to take
            prefix: Prefix for the filenames
            
        Returns:
            list: Paths to the saved images
        """
        paths = []
        try:
            for i in range(count):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{prefix}_{timestamp}.png"
                filepath = self.capture_screen(filename)
                paths.append(filepath)
                
                if i < count - 1:  # Don't sleep after the last capture
                    time.sleep(interval)
                    
            log.info(f"Captured sequence of {count} screenshots")
            return paths
            
        except Exception as e:
            log.error(f"Failed to capture sequence: {str(e)}")
            raise
