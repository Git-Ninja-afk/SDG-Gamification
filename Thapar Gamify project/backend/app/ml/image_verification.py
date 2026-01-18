"""Image verification using AI/ML"""
import cv2
import numpy as np
from datetime import datetime

class ImageVerificationEngine:
    @staticmethod
    def verify_task_proof(image_path: str, task_type: str) -> dict:
        """
        Verify task proof image using computer vision
        Supports: tree_planted, plastic_collected, clean_environment
        """
        try:
            # Read image
            image = cv2.imread(image_path)
            if image is None:
                return {"verified": False, "confidence": 0, "error": "Invalid image"}
            
            # Convert to HSV for color detection
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            
            verification_result = {"task_type": task_type, "timestamp": datetime.utcnow()}
            
            if task_type == "tree_planted":
                verification_result.update(ImageVerificationEngine._detect_tree(image, hsv))
            elif task_type == "plastic_collected":
                verification_result.update(ImageVerificationEngine._detect_plastic(image, hsv))
            elif task_type == "clean_environment":
                verification_result.update(ImageVerificationEngine._detect_cleanliness(image, hsv))
            else:
                verification_result["verified"] = False
                verification_result["confidence"] = 0
                verification_result["message"] = "Unknown task type"
            
            return verification_result
        
        except Exception as e:
            return {"verified": False, "confidence": 0, "error": str(e)}

    @staticmethod
    def _detect_tree(image, hsv):
        """Detect if image contains a tree/plant"""
        # Green color range in HSV
        lower_green = np.array([40, 40, 40])
        upper_green = np.array([80, 255, 255])
        
        mask = cv2.inRange(hsv, lower_green, upper_green)
        green_pixels = cv2.countNonZero(mask)
        total_pixels = image.shape[0] * image.shape[1]
        
        green_percentage = (green_pixels / total_pixels) * 100
        
        # If at least 15% of image is green, likely contains vegetation
        confidence = min(green_percentage / 15, 1.0) if green_percentage > 5 else 0
        
        return {
            "verified": confidence > 0.5,
            "confidence": round(confidence, 2),
            "message": f"Detected {green_percentage:.1f}% green areas"
        }

    @staticmethod
    def _detect_plastic(image, hsv):
        """Detect if image contains plastic waste"""
        # Detect dark colors (plastic typically appears dark)
        lower_dark = np.array([0, 0, 0])
        upper_dark = np.array([180, 100, 100])
        
        mask = cv2.inRange(hsv, lower_dark, upper_dark)
        dark_pixels = cv2.countNonZero(mask)
        total_pixels = image.shape[0] * image.shape[1]
        
        dark_percentage = (dark_pixels / total_pixels) * 100
        
        # Detect common plastic colors (blue, black, clear)
        lower_blue = np.array([100, 100, 100])
        upper_blue = np.array([130, 255, 255])
        
        blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)
        blue_pixels = cv2.countNonZero(blue_mask)
        blue_percentage = (blue_pixels / total_pixels) * 100
        
        confidence = min((dark_percentage + blue_percentage) / 30, 1.0)
        
        return {
            "verified": confidence > 0.4,
            "confidence": round(confidence, 2),
            "message": f"Detected {dark_percentage:.1f}% dark areas and {blue_percentage:.1f}% blue areas"
        }

    @staticmethod
    def _detect_cleanliness(image, hsv):
        """Detect if environment appears clean"""
        # Clean environment should have good lighting and less clutter
        # Analyze brightness
        brightness = np.mean(image)
        
        # If image is mostly bright, likely clean
        cleanliness_score = min(brightness / 150, 1.0)
        
        return {
            "verified": cleanliness_score > 0.5,
            "confidence": round(cleanliness_score, 2),
            "message": f"Environment brightness: {brightness:.1f}/255"
        }

    @staticmethod
    def extract_image_features(image_path: str) -> dict:
        """Extract features from image for ML model training"""
        try:
            image = cv2.imread(image_path)
            if image is None:
                return {}
            
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            
            features = {
                "brightness": float(np.mean(image)),
                "contrast": float(np.std(image)),
                "saturation": float(np.mean(hsv[:,:,1])),
                "dimensions": image.shape,
                "file_path": image_path,
            }
            
            return features
        except Exception as e:
            return {"error": str(e)}
