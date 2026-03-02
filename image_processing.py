import cv2
import numpy as np
import os

def mark_tumor_in_image(image_path, confidence, output_dir='uploads'):
    """
    Mark potential tumor areas in the image based on confidence level
    This is a simplified approach for demonstration
    """
    # Read the image
    img = cv2.imread(image_path)
    if img is None:
        return None
    
    # Convert to grayscale for processing
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Apply threshold to find potential tumor regions
    # Adjust threshold based on confidence level
    threshold_value = int(255 * (1 - confidence/100))
    _, thresh = cv2.threshold(blurred, threshold_value, 255, cv2.THRESH_BINARY)
    
    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Create a copy of the original image for marking
    marked_img = img.copy()
    
    if confidence > 50:  # Only mark if tumor is detected with reasonable confidence
        # Sort contours by area and take the largest ones
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        
        # Mark the largest contours (potential tumor areas)
        for i, contour in enumerate(contours[:3]):  # Mark top 3 largest areas
            area = cv2.contourArea(contour)
            if area > 100:  # Only mark significant areas
                # Draw contour in red
                cv2.drawContours(marked_img, [contour], -1, (0, 0, 255), 2)
                
                # Get bounding rectangle
                x, y, w, h = cv2.boundingRect(contour)
                
                # Draw bounding box
                cv2.rectangle(marked_img, (x, y), (x + w, y + h), (0, 255, 255), 2)
                
                # Add label
                label = f"Potential Tumor {i+1}"
                cv2.putText(marked_img, label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 
                           0.6, (0, 255, 255), 2)
    
    # Add confidence text
    confidence_text = f"Confidence: {confidence:.1f}%"
    cv2.putText(marked_img, confidence_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
               0.8, (255, 255, 255), 2)
    
    # Save marked image
    filename = os.path.basename(image_path)
    name, ext = os.path.splitext(filename)
    marked_filename = f"{name}_marked{ext}"
    marked_path = os.path.join(output_dir, marked_filename)
    
    cv2.imwrite(marked_path, marked_img)
    return marked_path

def enhance_image_for_analysis(image_path):
    """
    Enhance image for better analysis
    """
    img = cv2.imread(image_path)
    if img is None:
        return None
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    enhanced = clahe.apply(gray)
    
    # Convert back to BGR for consistency
    enhanced_bgr = cv2.cvtColor(enhanced, cv2.COLOR_GRAY2BGR)
    
    return enhanced_bgr