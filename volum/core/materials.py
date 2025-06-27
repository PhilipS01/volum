from volum.config.constants import MaterialColors

class Material:
    def __init__(self, color: str, texture, opacity: float):
        self.color = color
        self.texture = texture
        self.opacity = opacity

    def to_dict(self):
        raise NotImplementedError("Subclasses must implement to_dict method")
    
    def __repr__(self):
        return f"Material(color={self.color}, texture={self.texture}, opacity={self.opacity})"

class MeshMaterial(Material):
    def __init__(self, color, texture, wireframe: bool, opacity):
        super().__init__(color, texture, opacity)
        self.wireframe = wireframe

    def to_dict(self):
        raise NotImplementedError("Subclasses must implement to_dict method")
    
class BasicMaterial(MeshMaterial):
    def __init__(self, color=MaterialColors.DEFAULT, texture=None, wireframe=False, opacity=1.0):
        super().__init__(color, texture, wireframe, opacity)

    def to_dict(self):
        return {
            "type": "BasicMaterial",
            "color": self.color,
            "texture": self.texture,
            "wireframe": self.wireframe,
            "opacity": self.opacity
        }
    
    def __repr__(self):
        return f"BasicMaterial(color={self.color}, texture={self.texture}, wireframe={self.wireframe}, opacity={self.opacity})"
    
class StandardMaterial(MeshMaterial):
    def __init__(self, color=MaterialColors.DEFAULT, texture=None, wireframe=False, roughness: float=0.5, metalness: float=0.5, opacity=1.0):
        super().__init__(color, texture, wireframe, opacity)
        self.roughness = roughness
        self.metalness = metalness

    def to_dict(self):
        return {
            "type": "StandardMaterial",
            "color": self.color,
            "texture": self.texture,
            "wireframe": self.wireframe,
            "opacity": self.opacity,
            "roughness": self.roughness,
            "metalness": self.metalness
        }
    
    def __repr__(self):
        return f"StandardMaterial(color={self.color}, texture={self.texture}, wireframe={self.wireframe}, opacity={self.opacity}, roughness={self.roughness}, metalness={self.metalness})"

class PhongMaterial(MeshMaterial):
    def __init__(self, color=MaterialColors.DEFAULT, texture=None, wireframe=False, shininess: float=30, specular_color: str=MaterialColors.SPECULAR, opacity=1.0):
        super().__init__(color, texture, wireframe, opacity)
        self.shininess = shininess
        self.specular_color = specular_color

    def to_dict(self):
        return {
            "type": "PhongMaterial",
            "color": self.color,
            "texture": self.texture,
            "wireframe": self.wireframe,
            "opacity": self.opacity,
            "shininess": self.shininess,
            "specular_color": self.specular_color
        }
    
    def __repr__(self):
        return f"PhongMaterial(color={self.color}, texture={self.texture}, wireframe={self.wireframe}, opacity={self.opacity}, shininess={self.shininess}, specular_color={self.specular_color})"

class LineMaterial(Material):
    def __init__(self, color, texture, opacity, width: float):
        super().__init__(color, texture, opacity)
        self.width = width

    def to_dict(self):
        raise NotImplementedError("Subclasses must implement to_dict method")

class LineBasicMaterial(LineMaterial):
    def __init__(self, color=MaterialColors.DEFAULT, texture=None, width=1.0, opacity=1.0):
        super().__init__(color, texture, opacity, width)

    def to_dict(self):
        return {
            "type": "LineBasicMaterial",
            "color": self.color,
            "width": self.width,
            "opacity": self.opacity
        }
    
    def __repr__(self):
        return f"LineBasicMaterial(color={self.color}, width={self.width}, opacity={self.opacity})"
    
class LineDashedMaterial(LineMaterial):
    def __init__(self, color=MaterialColors.DEFAULT, texture=None, width=1.0, dash_size: float=3, gap_size: float=1, opacity=1.0):
        super().__init__(color, texture, opacity, width)
        self.dash_size = dash_size
        self.gap_size = gap_size

    def to_dict(self):
        return {
            "type": "LineDashedMaterial",
            "color": self.color,
            "width": self.width,
            "dash_size": self.dash_size,
            "gap_size": self.gap_size,
            "opacity": self.opacity
        }
    
    def __repr__(self):
        return f"LineDashedMaterial(color={self.color}, width={self.width}, dash_size={self.dash_size}, gap_size={self.gap_size}, opacity={self.opacity})"