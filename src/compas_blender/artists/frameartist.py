from typing import Any
from typing import List
from typing import Optional
from typing import Union

import bpy

from compas.geometry import Frame

import compas_blender
from compas.artists import PrimitiveArtist
from .artist import BlenderArtist


class FrameArtist(BlenderArtist, PrimitiveArtist):
    """Artist for drawing frames.

    Parameters
    ----------
    frame: :class:`compas.geometry.Frame`
        A COMPAS frame.
    collection: str or :class:`bpy.types.Collection`
        The name of the collection the object belongs to.
    scale: float, optional
        Scale factor that controls the length of the axes.

    Attributes
    ----------
    frame: :class:`compas.geometry.Frame`
        A COMPAS frame.
    collection: str
        The name of the frame's collection.
    scale : float
        Scale factor that controls the length of the axes.
        Default is ``1.0``.
    color_origin : tuple of 3 int between 0 and 255
        Default is ``(0, 0, 0)``.
    color_xaxis : tuple of 3 int between 0 and 255
        Default is ``(255, 0, 0)``.
    color_yaxis : tuple of 3 int between 0 and 255
        Default is ``(0, 255, 0)``.
    color_zaxis : tuple of 3 int between 0 and 255
        Default is ``(0, 0, 255)``.
    """
    def __init__(self,
                 frame: Frame,
                 collection: Optional[Union[str, bpy.types.Collection]] = None,
                 scale: float = 1.0,
                 **kwargs: Any):

        super().__init__(primitive=frame, collection=collection or frame.name, **kwargs)

        self.scale = scale or 1.0
        self.color_origin = (0, 0, 0)
        self.color_xaxis = (255, 0, 0)
        self.color_yaxis = (0, 255, 0)
        self.color_zaxis = (0, 0, 255)

    def draw(self) -> List[bpy.types.Object]:
        """Draw the frame.

        Returns
        -------
        list of :class:`bpy.types.Object`
        """
        self.clear()
        objects = []
        objects += self.draw_origin()
        objects += self.draw_axes()
        return objects

    def draw_origin(self) -> List[bpy.types.Object]:
        """Draw the origin of the frame.

        Returns
        -------
        list of :class:`bpy.types.Object`
        """
        points = [{
                'pos': self.primitive.point,
                'name': f"{self.primitive.name}.origin",
                'color': self.color_origin,
                'radius': 0.01
            }]
        return compas_blender.draw_points(points, self.collection)

    def draw_axes(self) -> List[bpy.types.Object]:
        """Draw the axes of the frame.

        Returns
        -------
        list of :class:`bpy.types.Object`
        """
        origin = list(self.primitive.point)
        X = list(self.primitive.point + self.primitive.xaxis.scaled(self.scale))
        Y = list(self.primitive.point + self.primitive.yaxis.scaled(self.scale))
        Z = list(self.primitive.point + self.primitive.zaxis.scaled(self.scale))
        lines = [
            {'start': origin, 'end': X, 'color': self.color_xaxis, 'name': f"{self.primitive.name}.xaxis"},
            {'start': origin, 'end': Y, 'color': self.color_yaxis, 'name': f"{self.primitive.name}.yaxis"},
            {'start': origin, 'end': Z, 'color': self.color_zaxis, 'name': f"{self.primitive.name}.zaxis"},
        ]
        return compas_blender.draw_lines(lines, self.collection)
