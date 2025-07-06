class UIColors:
    """Class to hold color constants for the UI and materials."""
    PRIMARY = "#008080"  # Primary color for the UI
    LIGHT = "#b2d8d8"  # Light color for the UI
    LIGHTER = "#66b2b2"  # Lighter shade for the UI
    DARKER = "#006666"  # Darker shade for the UI
    DARK = "#004c4c" # Dark color for the UI
    ACCENT = "#F5A623"  # Accent color for the UI
    ERROR = "#D0021B"  # Error color for the UI
    WARNING = "#F8E71C"  # Warning color for the UI
    SUCCESS = "#7ED321"  # Success color for the UI
    
class MaterialColors:
    """Class to hold color constants for materials."""
    DEFAULT = "#4ee050"  # Default color for materials
    METALLIC = "#C0C0C0"  # Metallic color for materials
    MATTE = "#808080"  # Matte color for materials
    SPECULAR = "#FFFFFF"  # Specular color for materials

class TerminalColors:
    """Class to hold color constants for terminal output."""
    INFO = "\033[94m"  # Blue
    WARNING = "\033[93m"  # Yellow
    SUCCESS = "\033[92m"  # Green
    ERROR = "\033[91m"  # Red

    INFO_BOLD = "\033[1;94m"  # Bold Blue
    WARNING_BOLD = "\033[1;93m"  # Bold Yellow
    SUCCESS_BOLD = "\033[1;92m"  # Bold Green
    ERROR_BOLD = "\033[1;91m"  # Bold Red

    BOLD = "\033[1m"  # Bold
    ENDC = "\033[0m"  # Reset to default color