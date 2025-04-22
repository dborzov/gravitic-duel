import os
import pygame

def load_image(filename, img_dir):
    """
    Load an image and make white pixels (255,255,255) transparent.
    
    Args:
        filename (str): The filename of the image to load
        img_dir (str): The directory containing the image
        
    Returns:
        pygame.Surface: The loaded image with white pixels made transparent
    """
    try:
        # Join the directory path with the filename
        full_path = os.path.join(img_dir, filename)
        
        # Load the image and convert it to support transparency
        image = pygame.image.load(full_path).convert_alpha()
        
        # Create a surface with alpha channel
        surface = pygame.Surface(image.get_size(), pygame.SRCALPHA)
        
        # Copy the image to the surface
        surface.blit(image, (0, 0))
        
        # Make white pixels transparent
        for x in range(surface.get_width()):
            for y in range(surface.get_height()):
                r, g, b, a = surface.get_at((x, y))
                if r == 255 and g == 255 and b == 255:
                    surface.set_at((x, y), (r, g, b, 0))  # Set alpha to 0 for white pixels
        
        return surface
    except (pygame.error, FileNotFoundError) as e:
        print(f"Error loading image {filename}: {e}")
        # Return a placeholder surface if image loading fails
        return pygame.Surface((50, 50), pygame.SRCALPHA) 