"""modules/common/math/aaboxkdtree2d.h"""

from typing import List, Optional

from shapely.geometry import Point, Polygon, box
from shapely.geometry.base import BaseGeometry

from .kdtree_node import KDTreeNode
from .kdtree_params import KDTreeParams


class KDTree:
    root: Optional[KDTreeNode] = None

    def __init__(self, objects: List[BaseGeometry], params: KDTreeParams) -> None:
        assert len(objects) > 0, "No objects provided"
        if len(objects) > 0:
            self.root = KDTreeNode(objects, params, 0)

    def get_nearest_object(self, point: Point) -> BaseGeometry:
        if self.root is None:
            return None
        else:
            return self.root.get_nearest_object(point)

    def get_objects(self, point: Point, distance: float) -> List[BaseGeometry]:
        if self.root is None:
            return []
        return self.root.get_objects(point, distance)

    def get_bounding_box(self) -> Polygon:
        if self.root is None:
            return box(0, 0, 0, 0)
        return self.root.get_bounding_box()
