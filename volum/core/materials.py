import warnings, base64, requests
from volum.config.constants import MaterialColors, TerminalColors

class MaterialWarning(Warning):
    """Base class for material-related warnings."""
    pass

class Material:
    """Base class for materials, providing common properties like color and opacity."""
    def __init__(self, color: str, opacity: float, name=None, **kwargs):
        self.color = color
        self.opacity = opacity
        self.name = name

    def to_dict(self):
        raise NotImplementedError("Subclasses must implement to_dict method")
    
    def __repr__(self):
        return f"Material(color={self.color}, opacity={self.opacity})"

class MeshMaterial(Material):
    """Base class for mesh materials, providing common properties like color, map, wireframe, and opacity."""
    def __init__(self, color, map, wireframe: bool, opacity, **kwargs):
        super().__init__(color, opacity, **kwargs)
        self.wireframe = wireframe
        self.map = map

    def to_dict(self):
        raise NotImplementedError("Subclasses must implement to_dict method")
    
    def __repr__(self):
        return f"MeshMaterial(color={self.color}, map={self.map}, wireframe={self.wireframe}, opacity={self.opacity})"

class BasicMaterial(MeshMaterial):
    """Basic material for simple shading, allowing customization of color, map, wireframe, and opacity."""
    def __init__(self, color=MaterialColors.DEFAULT, map=None, wireframe=False, opacity=1.0, **kwargs):
        super().__init__(color, map, wireframe, opacity, **kwargs)

    def to_dict(self):
        return {
            "type": "BasicMaterial",
            "name": self.name if self.name else self.__class__.__name__,
            "color": self.color,
            "map": self.map,
            "wireframe": self.wireframe,
            "opacity": self.opacity
        }
    
    def __repr__(self):
        return f"BasicMaterial(color={self.color}, map={self.map}, wireframe={self.wireframe}, opacity={self.opacity})"

class StandardMaterial(MeshMaterial):
    """Material that simulates standard shading, allowing for roughness and metalness properties."""
    def __init__(self, color=MaterialColors.DEFAULT, map=None, wireframe=False, roughness: float=0.5, metalness: float=0.5, opacity=1.0, **kwargs):
        super().__init__(color, map, wireframe, opacity, **kwargs)
        self.roughness = roughness
        self.metalness = metalness

    def to_dict(self):
        return {
            "type": "StandardMaterial",
            "name": self.name if self.name else self.__class__.__name__,
            "color": self.color,
            "map": self.map,
            "wireframe": self.wireframe,
            "opacity": self.opacity,
            "roughness": self.roughness,
            "metalness": self.metalness
        }
    
    def __repr__(self):
        return f"StandardMaterial(color={self.color}, map={self.map}, wireframe={self.wireframe}, opacity={self.opacity}, roughness={self.roughness}, metalness={self.metalness})"

class PhongMaterial(MeshMaterial):
    """Material that simulates Phong shading, allowing for shininess and specular highlights."""
    def __init__(self, color=MaterialColors.DEFAULT, map=None, wireframe=False, shininess: float=30.0, specular_color: str=MaterialColors.SPECULAR, opacity=1.0, **kwargs):
        super().__init__(color, map, wireframe, opacity, **kwargs)
        self.shininess = shininess
        self.specular_color = specular_color

    def to_dict(self):
        return {
            "type": "PhongMaterial",
            "name": self.name if self.name else self.__class__.__name__,
            "color": self.color,
            "map": self.map,
            "wireframe": self.wireframe,
            "opacity": self.opacity,
            "shininess": self.shininess,
            "specular_color": self.specular_color
        }
    
    def __repr__(self):
        return f"PhongMaterial(color={self.color}, map={self.map}, wireframe={self.wireframe}, opacity={self.opacity}, shininess={self.shininess}, specular_color={self.specular_color})"

class LineMaterial(Material):
    """Base class for line materials, providing common properties like color, opacity, and width."""
    def __init__(self, color, opacity, width: float, **kwargs):
        super().__init__(color, opacity, **kwargs)
        self.width = width

    def to_dict(self):
        raise NotImplementedError("Subclasses must implement to_dict method")

class LineBasicMaterial(LineMaterial):
    """Material for basic lines, allowing customization of color, width, and opacity."""
    def __init__(self, color=MaterialColors.DEFAULT, width=1.0, opacity=1.0, **kwargs):
        super().__init__(color, opacity, width, **kwargs)

    def to_dict(self):
        return {
            "type": "LineBasicMaterial",
            "name": self.name if self.name else self.__class__.__name__,
            "color": self.color,
            "width": self.width,
            "opacity": self.opacity
        }
    
    def __repr__(self):
        return f"LineBasicMaterial(color={self.color}, width={self.width}, opacity={self.opacity})"
    
class LineDashedMaterial(LineMaterial):
    """Material for dashed lines, allowing customization of dash and gap sizes."""
    def __init__(self, color=MaterialColors.DEFAULT, width=1.0, dash_size: float=3.0, gap_size: float=1.0, opacity=1.0, **kwargs):
        super().__init__(color, opacity, width, **kwargs)
        self.dash_size = dash_size
        self.gap_size = gap_size

    def to_dict(self):
        return {
            "type": "LineDashedMaterial",
            "name": self.name if self.name else self.__class__.__name__,
            "color": self.color,
            "width": self.width,
            "dash_size": self.dash_size,
            "gap_size": self.gap_size,
            "opacity": self.opacity
        }
    
    def __repr__(self):
        return f"LineDashedMaterial(color={self.color}, width={self.width}, dash_size={self.dash_size}, gap_size={self.gap_size}, opacity={self.opacity})"
    
class PhysicalMaterial(MeshMaterial):
    """Material that simulates realistic physical properties, including roughness, metalness, and more."""
    def __init__(
        self,
        color=MaterialColors.DEFAULT,
        map=None,
        wireframe=False,
        roughness: float=0.5,
        metalness: float=0.5,
        emissive_color: str="#000000",
        ior: float= 1.5,
        reflectivity: float=0.5,
        iridescence: float = 0.0,
        iridescence_ior: float=1.3,
        transmission: float=0.0,
        sheen: float=0.0,
        sheen_roughness: float=1.0,
        sheen_color: str="#000000",
        clearcoat: float=0.0,
        clearcoat_roughness: float=0.0,
        specular_intensity: float=1.0,
        specular_color: str=MaterialColors.SPECULAR,
        flat_shading=False,
        opacity=1.0,
        **kwargs
    ):
        super().__init__(color, map, wireframe, opacity, **kwargs)
        self.roughness = roughness
        self.metalness = metalness
        self.emissive_color = emissive_color
        self.ior = ior
        self.reflectivity = reflectivity
        self.iridescence = iridescence
        self.iridescence_ior = iridescence_ior
        self.transmission = transmission
        self.sheen = sheen
        self.sheen_roughness = sheen_roughness
        self.sheen_color = sheen_color
        self.clearcoat = clearcoat
        self.clearcoat_roughness = clearcoat_roughness
        self.specular_intensity = specular_intensity
        self.specular_color = specular_color
        self.flat_shading = flat_shading

    def to_dict(self):
        return {    
            "type": "PhysicalMaterial",
            "name": self.name if self.name else self.__class__.__name__,
            "color": self.color,
            "map": self.map,
            "wireframe": self.wireframe,
            "opacity": self.opacity,
            "roughness": self.roughness,
            "metalness": self.metalness,
            "emissive_color": self.emissive_color,
            "ior": self.ior,
            "reflectivity": self.reflectivity,
            "iridescence": self.iridescence,
            "iridescence_ior": self.iridescence_ior,
            "transmission": self.transmission,
            "sheen": self.sheen,
            "sheen_roughness": self.sheen_roughness,
            "sheen_color": self.sheen_color,
            "clearcoat": self.clearcoat,
            "clearcoat_roughness": self.clearcoat_roughness,
            "specular_intensity": self.specular_intensity,
            "specular_color": self.specular_color,
            "flat_shading": self.flat_shading
        }
    
    def __repr__(self):
        return f"PhysicalMaterial(color={self.color}, map={self.map}, wireframe={self.wireframe}, opacity={self.opacity}, roughness={self.roughness}, metalness={self.metalness}, emissive_color={self.emissive_color}, ior={self.ior}, reflectivity={self.reflectivity}, iridescence={self.iridescence}, iridescence_ior={self.iridescence_ior}, sheen={self.sheen}, sheen_roughness={self.sheen_roughness}, sheen_color={self.sheen_color}, clearcoat={self.clearcoat}, clearcoatRoughness={self.clearcoat_roughness}, specular_intensity={self.specular_intensity}, specular_color={self.specular_color}, flat_shading={self.flat_shading})"


class MatcapMaterial(MeshMaterial):
    """Material that uses a matcap texture for shading, typically used for stylized rendering."""
    def __init__(self, color=MaterialColors.DEFAULT, map=None, wireframe=False, matcap=None, opacity=1.0, **kwargs):
        if color is not MaterialColors.DEFAULT:
            warnings.warn(
                f"{TerminalColors.WARNING}MatcapMaterial color is set to {color}, but matcap texture will override it.{TerminalColors.ENDC}",
                category=MaterialWarning,
                stacklevel=2
            )
        
        super().__init__(color, map, wireframe, opacity, **kwargs)
        self.matcap = matcap

    def to_dict(self):
        return {
            "type": "MatcapMaterial",
            "name": self.name if self.name else self.__class__.__name__,
            "color": self.color,
            "map": self.map,
            "wireframe": self.wireframe,
            "matcap": self.matcap,
            "opacity": self.opacity
        }
    
    def __repr__(self):
        return f"MatcapMaterial(color={self.color}, map={self.map}, wireframe={self.wireframe}, matcap={self.matcap}, opacity={self.opacity})"

class NormalMaterial(MeshMaterial):
    """Material that uses normals for shading, typically used for debugging or visualizing normals."""
    def __init__(self, color=MaterialColors.DEFAULT, map=None, wireframe=False, flat_shading=False, opacity=1.0, **kwargs):
        if color is not MaterialColors.DEFAULT:
            warnings.warn(
                f"{TerminalColors.WARNING}NormalMaterial color is set to {color}, but it will be ignored.{TerminalColors.ENDC}",
                category=MaterialWarning,
                stacklevel=2
            )

        super().__init__(color, map, wireframe, opacity, **kwargs)
        self.flat_shading = flat_shading

    def to_dict(self):
        return {
            "type": "NormalMaterial",
            "name": self.name if self.name else self.__class__.__name__,
            "color": self.color,
            "map": self.map,
            "wireframe": self.wireframe,
            "flat_shading": self.flat_shading,
            "opacity": self.opacity
        }
    
    def __repr__(self):
        return f"NormalMaterial(color={self.color}, map={self.map}, wireframe={self.wireframe}, flat_shading={self.flat_shading}, opacity={self.opacity})"

class ToonMaterial(MeshMaterial):
    """Material that simulates a toon shading effect, allowing for a gradient map and flat shading."""
    def __init__(self, color=MaterialColors.DEFAULT, map=None, wireframe=False, gradient_map=None, opacity=1.0, **kwargs):
        super().__init__(color, map, wireframe, opacity, **kwargs)
        self.gradient_map = gradient_map
        
    def to_dict(self):
        return {
            "type": "ToonMaterial",
            "name": self.name if self.name else self.__class__.__name__,
            "color": self.color,
            "map": self.map,
            "wireframe": self.wireframe,
            "gradient_map": self.gradient_map,
            "opacity": self.opacity
        }
    
    def __repr__(self):
        return f"ToonMaterial(color={self.color}, map={self.map}, wireframe={self.wireframe}, gradient_map={self.gradient_map}, opacity={self.opacity})"
    
class ImageMaterial(MeshMaterial):
    """Material that uses an image texture."""
    def __init__(self, image_path: str="https://raw.githubusercontent.com/PhilipS01/volum/90af00489989d70374ed29e45c32f310740daca2/docs/static/volum_banner.png", color="white", wireframe=False, opacity=1.0, **kwargs):
        """Initialize the ImageMaterial.

        Args:
            image_path (str, optional): The path to the image file. Defaults to Volum banner.
            color (str, optional): The color of the material. Defaults to MaterialColors.DEFAULT.
            wireframe (bool, optional): Whether to render the material as a wireframe. Defaults to False.
            opacity (float, optional): The opacity of the material. Defaults to 1.0.

        Raises:
            ValueError: If the image_path is invalid or does not point to a valid file.
        """

        if image_path is None or not isinstance(image_path, str):
            raise ValueError(f"{TerminalColors.ERROR}ImageMaterial requires a valid image path, got {image_path}{TerminalColors.ENDC}")

        self.image_path = image_path

        # check if map is in kwargs first (built by volum.core.builder)
        if kwargs.get('map') is not None and isinstance(kwargs['map'], str):
            super().__init__(color, wireframe=wireframe, opacity=opacity, **kwargs)
        else:
            kwargs.pop('map', None)  # remove map from kwargs if it exists but is not a string
            map = None
            if self.image_path.startswith("http://") or self.image_path.startswith("https://"):
                warnings.warn(
                    f"{TerminalColors.WARNING}ImageMaterial image_path is set to a remote URL. Ensure the image is accessible.{TerminalColors.ENDC}",
                    category=MaterialWarning,
                    stacklevel=2
                )
                # get image data from URL
                try:
                    response = requests.get(self.image_path)
                    response.raise_for_status()  # raise an error for bad responses
                    img_data = response.content
                    img_base64 = base64.b64encode(img_data).decode('utf-8')
                    map = f"data:image/png;base64,{img_base64}"
                except requests.RequestException as e:
                    raise ValueError(f"{TerminalColors.ERROR}ImageMaterial failed to fetch image from {self.image_path}: {e}{TerminalColors.ENDC}")

            elif not self.image_path.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                warnings.warn(
                    f"{TerminalColors.WARNING}ImageMaterial image_path is set to {self.image_path}, which does not have a recognized image file extension.{TerminalColors.ENDC}",
                    category=MaterialWarning,
                    stacklevel=2
                )

            else:
                try:
                    with open(self.image_path, 'rb') as f:
                        img_data = f.read()
                        img_base64 = base64.b64encode(img_data).decode('utf-8')
                        map = f"data:image/png;base64,{img_base64}"
                except FileNotFoundError:
                    raise ValueError(f"{TerminalColors.ERROR}ImageMaterial image_path {self.image_path} does not point to a valid file.{TerminalColors.ENDC}")

            if map is not None:
                super().__init__(color, map=map, wireframe=wireframe, opacity=opacity, **kwargs)
            

    def to_dict(self):
        return {
            "type": "ImageMaterial",
            "name": self.name if self.name else self.__class__.__name__,
            "image_path": self.image_path, # stores the original image path
            "color": self.color,
            "map": self.map, # stores base64 encoded image data
            "wireframe": self.wireframe,
            "opacity": self.opacity
        }
    
    def __repr__(self):
        return f"ImageMaterial(color={self.color}, map={self.map}, wireframe={self.wireframe}, opacity={self.opacity})"