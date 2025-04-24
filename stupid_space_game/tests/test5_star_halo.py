import pygame
import random
import math
import sys # Import sys for sys.exit()

# --- Constants ---
# Window
WIDTH, HEIGHT = 400, 400 # Window size
WINDOW_TITLE = "Lava Lamp Star Corona"
FPS = 30 # Frames per second

# Colors (Orange/Yellow Palette for a hot, pixel-art feel)
COLOR_DARK_ORANGE = (200, 80, 0)
COLOR_ORANGE = (255, 140, 0)
COLOR_LIGHT_ORANGE = (255, 180, 50)
COLOR_YELLOW = (255, 220, 100)
COLOR_BRIGHT_YELLOW = (255, 255, 150)
BACKGROUND_COLOR = (10, 0, 20) # Dark space background

# Corona Properties
CENTER_X, CENTER_Y = 140, 185 # Center coordinates on the main screen
BASE_RADIUS = 25 # Base radius of the corona core
MAX_RADIUS_VARIATION = 10 # How much the main corona radius pulses (increased slightly)
PULSATION_SPEED = 0.06 # Speed of the pulsation cycle (radians per frame, slowed down)
NUM_CORONA_LAYERS = 6 # More layers for smoother gradient

# Blob (Flare) Properties
NUM_BLOBS = 8 # Renamed from NUM_FLARES, maybe fewer blobs
BLOB_MIN_MAX_LEN = 10 # Minimum 'length' or travel distance potential
BLOB_MAX_MAX_LEN = 35 # Maximum 'length' or travel distance potential
BLOB_MIN_WIDTH = 4    # Base width of the blob
BLOB_MAX_WIDTH = 8
BLOB_MIN_HEIGHT_FACTOR = 0.8 # Factor to scale width to get height at max length
BLOB_MAX_HEIGHT_FACTOR = 1.5
BLOB_LIFETIME_MIN = 0.8 # seconds (longer lifetime for slower feel)
BLOB_LIFETIME_MAX = 2.5 # seconds
BLOB_SPAWN_RADIUS_OFFSET = 5 # How far from the base radius blobs start
BLOB_GRADIENT_LAYERS = 3 # Number of layers for blob gradient effect

# --- Helper Functions ---
def oscillate(time_val, speed, amplitude, base):
    """ Calculates a value oscillating sinusoidally around a base value. """
    return base + math.sin(time_val * speed) * amplitude

def lerp_color(color1, color2, factor):
    """ Linearly interpolate between two RGB colors. Factor 0 = color1, 1 = color2. """
    r = color1[0] + factor * (color2[0] - color1[0])
    g = color1[1] + factor * (color2[1] - color1[1])
    b = color1[2] + factor * (color2[2] - color1[2])
    return (int(r), int(g), int(b))

# --- Blob Class ---
class Blob:
    """ Represents a single blob ejecting from the corona, like a lava lamp bubble. """
    def __init__(self, surface_center_x, surface_center_y):
        """ Initializes a Blob object relative to the center of the surface. """
        self.surface_center_x = surface_center_x
        self.surface_center_y = surface_center_y
        self.reset()

    def reset(self):
        """ Initialize or re-initialize the blob's properties. """
        self.angle = random.uniform(0, 2 * math.pi) # Random direction
        self.max_travel_dist = random.uniform(BLOB_MIN_MAX_LEN, BLOB_MAX_MAX_LEN) # How far it can travel
        self.base_width = random.uniform(BLOB_MIN_WIDTH, BLOB_MAX_WIDTH)
        self.height_factor = random.uniform(BLOB_MIN_HEIGHT_FACTOR, BLOB_MAX_HEIGHT_FACTOR)
        self.lifetime = random.uniform(BLOB_LIFETIME_MIN, BLOB_LIFETIME_MAX) * FPS
        self.life = self.lifetime # Current life remaining in frames
        self.color = random.choice([COLOR_LIGHT_ORANGE, COLOR_YELLOW, COLOR_BRIGHT_YELLOW])
        self.current_progress = 0 # How far along its path (0 to 1)
        self.phase_offset = random.uniform(0, math.pi) # Desynchronize movement

    def update(self, current_base_radius):
        """ Update blob state (life, position, size) for the current frame. """
        self.life -= 1
        if self.life <= 0:
            self.reset() # Respawn

        # Calculate current progress using a sine wave for smooth acceleration/deceleration
        self.current_progress = (self.lifetime - self.life) / self.lifetime # Ranges from 0 to 1
        scale_factor = math.sin(self.current_progress * math.pi + self.phase_offset) # Controls size/speed
        scale_factor = max(0, scale_factor) # Ensure non-negative

        # Calculate current distance travelled
        current_dist_travelled = self.max_travel_dist * scale_factor

        # Calculate center position of the blob relative to the surface center
        # It starts near the corona edge and moves outwards
        dist_from_center = current_base_radius + BLOB_SPAWN_RADIUS_OFFSET + current_dist_travelled
        self.center_x = self.surface_center_x + math.cos(self.angle) * dist_from_center
        self.center_y = self.surface_center_y + math.sin(self.angle) * dist_from_center

        # Calculate current blob dimensions (width/height)
        # Width might stay relatively constant, height stretches with progress
        self.current_width = self.base_width * (1 + scale_factor * 0.2) # Slight width pulse
        self.current_height = self.base_width * self.height_factor * scale_factor # Height scales more significantly

    def draw(self, surface):
        """ Draw the blob with a gradient effect onto the provided Pygame surface. """
        if self.current_progress > 0.01 and self.current_width > 1 and self.current_height > 1: # Only draw if visible
            # Calculate base alpha based on remaining life (fades out)
            # Make fade-out less aggressive than fade-in
            fade_factor = math.sin(self.current_progress * math.pi) # Peaks at 1 mid-life
            base_alpha = int(220 * fade_factor) # Max alpha slightly less than 255
            base_alpha = max(0, min(255, base_alpha))

            if base_alpha > 10: # Don't draw if too faint
                try:
                    # Draw gradient layers (from outside in, or inside out - let's try outside in)
                    size_scale = 1.0 + (BLOB_GRADIENT_LAYERS - 1) * 0.4 # Start larger for outer layer
                    alpha_scale = 0.4 # Start fainter for outer layer

                    for i in range(BLOB_GRADIENT_LAYERS):
                        layer_width = self.current_width * size_scale
                        layer_height = self.current_height * size_scale

                        # Ensure dimensions are positive
                        if layer_width < 1 or layer_height < 1:
                            continue

                        rect_left = self.center_x - layer_width / 2
                        rect_top = self.center_y - layer_height / 2
                        ellipse_rect = pygame.Rect(rect_left, rect_top, layer_width, layer_height)

                        current_alpha = int(base_alpha * alpha_scale)
                        current_alpha = max(0, min(255, current_alpha))

                        if current_alpha > 5: # Skip drawing very faint layers
                             # Add alpha to the blob's base color
                            color_with_alpha = self.color + (current_alpha,)
                            pygame.draw.ellipse(surface, color_with_alpha, ellipse_rect)

                        # Prepare for next layer (smaller, brighter)
                        size_scale -= 0.4 # Decrease size
                        alpha_scale += 0.3 # Increase alpha (adjust factors as needed)


                except Exception as e:
                    print(f"Error drawing blob: {e} with color {self.color}", file=sys.stderr)


# --- Main Game Setup ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(WINDOW_TITLE)
clock = pygame.time.Clock()

# Create a dedicated surface for the corona effect (SRCALPHA for transparency)
# Recalculate size needed based on new blob properties
max_effect_radius = BASE_RADIUS + MAX_RADIUS_VARIATION + BLOB_MAX_MAX_LEN + BLOB_SPAWN_RADIUS_OFFSET + BLOB_MAX_WIDTH # Approximate
corona_surface_size = int(max_effect_radius * 2 * 1.2) # Increased safety margin
corona_surface = pygame.Surface((corona_surface_size, corona_surface_size), pygame.SRCALPHA)
surface_center_x = corona_surface_size // 2
surface_center_y = corona_surface_size // 2

# Create blob objects
blobs = [Blob(surface_center_x, surface_center_y) for _ in range(NUM_BLOBS)]

# --- Game Loop ---
running = True
time_counter = 0 # Frame counter for animation timing

while running:
    # --- Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                 running = False

    # --- Updates ---
    time_counter += 1
    current_time_rad = time_counter * PULSATION_SPEED

    # Calculate current pulsating radius for the main corona body
    pulsating_radius_core = oscillate(current_time_rad, 1.0, MAX_RADIUS_VARIATION, BASE_RADIUS)

    # Update all blob objects
    for blob in blobs:
        blob.update(pulsating_radius_core) # Pass the core radius

    # --- Drawing ---
    # 1. Clear the main screen
    screen.fill(BACKGROUND_COLOR)

    # 2. Clear the transparent corona surface
    corona_surface.fill((0, 0, 0, 0))

    # 3. Draw the corona layers onto the dedicated corona_surface for a soft gradient
    # Draw from outermost (faintest, largest) to innermost (brightest, smallest)
    max_corona_visual_radius = BASE_RADIUS * 1.8 # Visual extent of the soft edge
    min_corona_visual_radius = BASE_RADIUS * 0.4 # Innermost core extent
    max_corona_alpha = 80  # Alpha for the outermost layer
    min_corona_alpha = 220 # Alpha for the innermost layer (bright core)

    for i in range(NUM_CORONA_LAYERS):
        # layer_fraction: 0 for outermost, 1 for innermost
        layer_fraction = i / (NUM_CORONA_LAYERS - 1)

        # Interpolate base properties for this layer
        base_radius_layer = max_corona_visual_radius - layer_fraction * (max_corona_visual_radius - min_corona_visual_radius)
        base_alpha_layer = max_corona_alpha + layer_fraction * (min_corona_alpha - max_corona_alpha) # Alpha increases inwards

        # Oscillation parameters per layer (more variation outer, less inner)
        amplitude_radius_layer = MAX_RADIUS_VARIATION * (1.1 - 0.8 * layer_fraction)
        amplitude_alpha_layer = 60 * (1.0 - 0.6 * layer_fraction)
        # Slightly different speeds for a more 'wobbly' effect
        speed_layer = PULSATION_SPEED * (0.9 + 0.3 * layer_fraction + math.sin(i) * 0.05) # Add slight variation

        # Calculate current oscillating values
        current_radius = oscillate(current_time_rad, speed_layer, amplitude_radius_layer, base_radius_layer)
        current_alpha = oscillate(current_time_rad, speed_layer, amplitude_alpha_layer, base_alpha_layer)
        current_radius = max(1, current_radius) # Ensure positive radius
        current_alpha = max(0, min(255, current_alpha)) # Clamp alpha

        # Interpolate color from Orange (outer) to Bright Yellow (inner)
        interp_color = lerp_color(COLOR_ORANGE, COLOR_BRIGHT_YELLOW, layer_fraction)
        current_color = interp_color + (int(current_alpha),) # Add alpha

        # Draw the circle for this layer
        pygame.draw.circle(corona_surface, current_color, (surface_center_x, surface_center_y), int(current_radius))

    # 4. Draw all active blobs onto the corona_surface
    for blob in blobs:
        blob.draw(corona_surface)

    # 5. Blit the finished corona_surface onto the main screen at the target coordinates
    screen.blit(corona_surface, corona_surface.get_rect(center=(CENTER_X, CENTER_Y)))

    # --- Display Update ---
    pygame.display.flip()

    # --- Frame Rate Control ---
    clock.tick(FPS)

# --- Cleanup ---
pygame.quit()
sys.exit()
