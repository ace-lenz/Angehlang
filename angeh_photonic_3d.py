"""
🧊 ANGEH PHOTONIC 3D/4D ENGINE
A proprietary Native Math Engine for projecting Hyperspace Geometry.
Zero Dependencies. Pure Math.
Output: Scalable Vector Graphics (SVG) "Holograms".
"""

import math
from typing import List, Tuple

class Vector4D:
    def __init__(self, x, y, z, w):
        self.x, self.y, self.z, self.w = x, y, z, w

class Matrix4:
    @staticmethod
    def rotation_xy(angle):
        c, s = math.cos(angle), math.sin(angle)
        return [[c,-s,0,0], [s,c,0,0], [0,0,1,0], [0,0,0,1]]

    @staticmethod
    def rotation_zw(angle):
        c, s = math.cos(angle), math.sin(angle)
        return [[1,0,0,0], [0,1,0,0], [0,0,c,-s], [0,0,s,c]]
        
    @staticmethod
    def rotation_xw(angle):
        c, s = math.cos(angle), math.sin(angle)
        return [[c,0,0,-s], [0,1,0,0], [0,0,1,0], [s,0,0,c]]

class PhotonicRenderer:
    def __init__(self):
        self.vertices: List[Vector4D] = []
        self.edges: List[Tuple[int, int]] = []
        self._init_tesseract()

    def _init_tesseract(self):
        # Generate 16 vertices of a Hypercube
        for i in range(16):
            x = -1 if (i & 1) else 1
            y = -1 if (i & 2) else 1
            z = -1 if (i & 4) else 1
            w = -1 if (i & 8) else 1
            self.vertices.append(Vector4D(x/2, y/2, z/2, w/2))

        # Generate 32 edges
        for i in range(16):
            for j in range(4):
                neighbor = i ^ (1 << j) # Flip one bit
                if i < neighbor:
                    self.edges.append((i, neighbor))

    def _multiply(self, v: Vector4D, m: List[List[float]]) -> Vector4D:
        # Matrix vector multiplication
        x = v.x*m[0][0] + v.y*m[0][1] + v.z*m[0][2] + v.w*m[0][3]
        y = v.x*m[1][0] + v.y*m[1][1] + v.z*m[1][2] + v.w*m[1][3]
        z = v.x*m[2][0] + v.y*m[2][1] + v.z*m[2][2] + v.w*m[2][3]
        w = v.x*m[3][0] + v.y*m[3][1] + v.z*m[3][2] + v.w*m[3][3]
        return Vector4D(x, y, z, w)

    def render_animated_svg(self) -> str:
        """Render a self-animating SVG (Browser-native animation)"""
        # Generate base frame at angle 0
        base_svg = self.render_frame(0.0, header=False)
        
        container = f"""
        <svg width="200" height="200" viewBox="0 0 200 200" style="background:rgba(0,0,0,0.2); border-radius:10px; border:1px solid #00f5ff">
            <defs>
                <filter id="glow">
                    <feGaussianBlur stdDeviation="2.5" result="coloredBlur"/>
                    <feMerge>
                        <feMergeNode in="coloredBlur"/>
                        <feMergeNode in="SourceGraphic"/>
                    </feMerge>
                </filter>
            </defs>
            <g filter="url(#glow)">
                <animateTransform 
                    attributeName="transform" 
                    attributeType="XML" 
                    type="rotate" 
                    from="0 100 100" 
                    to="360 100 100" 
                    dur="10s" 
                    repeatCount="indefinite"/>
                {base_svg}
            </g>
            <text x="10" y="190" fill="#00f5ff" font-family="monospace" font-size="10">🧊 4D HYPERCUBE</text>
        </svg>
        """
        return container

    def render_frame(self, angle: float, header=True) -> str:
        """Render a single frame as SVG string"""
        projected_2d = []
        
        # 1. Rotate in 4D Hyperspace
        rot_xy = Matrix4.rotation_xy(angle)
        rot_zw = Matrix4.rotation_zw(angle * 0.5)
        rot_xw = Matrix4.rotation_xw(angle * 0.3)
        
        for v in self.vertices:
            # Apply rotations
            r = self._multiply(v, rot_xy)
            r = self._multiply(r, rot_zw)
            r = self._multiply(r, rot_xw)
            
            # 2. Project 4D -> 3D (Stereographic)
            distance = 2.0
            w_factor = 1 / (distance - r.w)
            p3 = Vector4D(r.x * w_factor, r.y * w_factor, r.z * w_factor, 0)
            
            # 3. Project 3D -> 2D (Perspective)
            z_factor = 1 / (distance - p3.z)
            x_2d = p3.x * z_factor * 400 + 100 # Scale & Offset (200x200 canvas)
            y_2d = p3.y * z_factor * 400 + 100
            
            projected_2d.append((x_2d, y_2d, p3.z)) 
            
        # 4. Draw SVG
        svg = ""
        if header:
            svg += '<svg width="200" height="200" style="background:transparent; overflow:visible">'
        
        # Draw Edges (Neon Style)
        for i, j in self.edges:
            p1 = projected_2d[i]
            p2 = projected_2d[j]
            
            # Depth coloring (holographic effect)
            depth = (p1[2] + p2[2]) / 2
            opacity = max(0.2, 1.0 - abs(depth))
            color = f"rgba(0, 245, 255, {opacity})" # Cyan Neon
            if depth > 0.1: color = f"rgba(255, 0, 245, {opacity})" # Magenta Neon (Shift)
            
            svg += f'<line x1="{p1[0]}" y1="{p1[1]}" x2="{p2[0]}" y2="{p2[1]}" stroke="{color}" stroke-width="2" />'
            
        # Draw Vertices (Particle Glow)
        for p in projected_2d:
             svg += f'<circle cx="{p[0]}" cy="{p[1]}" r="2" fill="white" />'
             
        if header:
             svg += '</svg>'
        return svg

if __name__ == "__main__":
    renderer = PhotonicRenderer()
    print(renderer.render_frame(0.5))
