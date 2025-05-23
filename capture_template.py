#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Utility script for capturing and testing template images for CorahBot
"""

import sys
import time
from airtest.core.api import auto_setup, exists
from corahbot.config import DEVICE
from corahbot.logger import get_logger
from corahbot.screen_capture import ScreenCapture
from corahbot.templates import TemplateManager

log = get_logger("TemplateCapture")

def print_menu():
    """Print the main menu options"""
    print("\n=== CorahBot Template Capture Utility ===")
    print("1. Capture full screen")
    print("2. Capture region")
    print("3. Capture sequence")
    print("4. Test existing template")
    print("5. List existing templates")
    print("q. Quit")
    print("=====================================")

def capture_full_screen(screen_capture):
    """Handle full screen capture"""
    name = input("Enter name for the template (or press Enter for timestamp): ").strip()
    try:
        filepath = screen_capture.capture_screen(name if name else None)
        print(f"\nTemplate saved to: {filepath}")
        return filepath
    except Exception as e:
        print(f"\nError capturing screen: {e}")
        return None

def capture_region(screen_capture):
    """Handle region capture"""
    try:
        print("\nEnter region coordinates:")
        x1 = int(input("X1 (top-left): "))
        y1 = int(input("Y1 (top-left): "))
        x2 = int(input("X2 (bottom-right): "))
        y2 = int(input("Y2 (bottom-right): "))
        name = input("Enter name for the template (or press Enter for timestamp): ").strip()
        
        filepath = screen_capture.capture_region(x1, y1, x2, y2, name if name else None)
        print(f"\nTemplate saved to: {filepath}")
        return filepath
    except ValueError:
        print("\nError: Please enter valid numbers for coordinates")
    except Exception as e:
        print(f"\nError capturing region: {e}")
    return None

def capture_sequence(screen_capture):
    """Handle sequence capture"""
    try:
        interval = float(input("Enter interval between captures (seconds): "))
        count = int(input("Enter number of captures: "))
        prefix = input("Enter prefix for filenames (default: seq): ").strip() or "seq"
        
        print(f"\nStarting sequence capture ({count} images)...")
        paths = screen_capture.capture_sequence(interval, count, prefix)
        print(f"\nCaptured {len(paths)} images:")
        for path in paths:
            print(f"- {path}")
        return paths
    except ValueError:
        print("\nError: Please enter valid numbers for interval and count")
    except Exception as e:
        print(f"\nError capturing sequence: {e}")
    return None

def test_template(template_manager):
    """Test an existing template"""
    try:
        print("\nAvailable templates:")
        for key in template_manager.templates.keys():
            print(f"- {key}")
        
        key = input("\nEnter template name to test: ").strip()
        template = template_manager.get(key)
        
        if template is None:
            print(f"\nTemplate '{key}' not found")
            return
            
        print("\nTesting template for 10 seconds...")
        end_time = time.time() + 10
        
        while time.time() < end_time:
            if exists(template):
                print(f"\nTemplate '{key}' found on screen!")
                return True
            time.sleep(0.5)
            
        print(f"\nTemplate '{key}' not found on screen during test period")
        return False
        
    except Exception as e:
        print(f"\nError testing template: {e}")
        return False

def list_templates(template_manager):
    """List all available templates"""
    print("\nAvailable templates:")
    for key, template in template_manager.templates.items():
        try:
            filename = template.filename if hasattr(template, 'filename') else 'Unknown'
            threshold = template.threshold if hasattr(template, 'threshold') else 'Default'
            print(f"- {key}:")
            print(f"  File: {filename}")
            print(f"  Threshold: {threshold}")
        except Exception as e:
            print(f"- {key}: Error reading template info: {e}")

def main():
    """Main function"""
    try:
        # Initialize Airtest
        auto_setup(__file__, devices=[DEVICE])
        log.info("Connected to device successfully")
        
        # Initialize components
        screen_capture = ScreenCapture()
        template_manager = TemplateManager()
        
        while True:
            print_menu()
            choice = input("Enter your choice: ").strip().lower()
            
            if choice == 'q':
                break
            elif choice == '1':
                capture_full_screen(screen_capture)
            elif choice == '2':
                capture_region(screen_capture)
            elif choice == '3':
                capture_sequence(screen_capture)
            elif choice == '4':
                test_template(template_manager)
            elif choice == '5':
                list_templates(template_manager)
            else:
                print("\nInvalid choice, please try again")
                
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        log.exception("An error occurred")
        print(f"\nError: {e}")
    finally:
        print("\nTemplate capture utility closed")

if __name__ == "__main__":
    main()
