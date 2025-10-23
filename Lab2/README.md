# CSC402 - Computer Graphics Labs

## Lab 1: OpenGL Primitives - Triangle, Square, and Cube

![OpenGL](https://img.shields.io/badge/OpenGL-3.3-blue.svg)
![Python](https://img.shields.io/badge/Python-3.x-green.svg)
![License](https://img.shields.io/badge/License-Educational-orange.svg)

### Overview
An introductory OpenGL lab demonstrating fundamental 3D graphics programming concepts using PyOpenGL. This project renders basic geometric primitives (triangle, square, cube) with vertex colors and transformations.

### Learning Objectives
- Understand the OpenGL rendering pipeline
- Master vertex buffer objects (VBO) and vertex array objects (VAO)
- Implement GLSL shader programs
- Apply model-view-projection (MVP) transformations
- Render 2D and 3D primitives with depth testing

### Features
- **2D Triangle** - Simple colored triangle with RGB vertex interpolation
- **2D Square** - Quad rendered using indexed drawing (EBO)
- **3D Rotating Cube** - Perspective projection with camera view and animated rotation
- **Interactive Controls** - Switch between primitives with keyboard
- 🎨 **Vertex Colors** - Smooth color gradients via attribute interpolation

### Prerequisites
- Python 3.x
- Basic understanding of linear algebra (matrices, vectors)
- Familiarity with 3D coordinate systems
- OpenGL 3.3+ compatible graphics card

### Installation

#### 1. Install dependencies
```bash
pip install PyOpenGL PyOpenGL_accelerate glfw numpy pyrr
```

Or use the requirements file:
```bash
pip install -r requirements.txt
```

### Project Structure
```
Lab1/
├── main.py              # Main application file
├── shaders/
│   ├── basic.vert.glsl  # Vertex shader
│   └── basic.frag.glsl  # Fragment shader
├── common/
│   └── shader.py        # Shader compilation utilities
├── README.md            # This file
└── requirements.txt     # Python dependencies
```

### Controls
| Key | Action |
|-----|--------|
| `1` | Display 2D Triangle |
| `2` | Display 2D Square |
| `3` | Display 3D Rotating Cube |
| `ESC` | Exit Application |

### Running the Program
```bash
python main.py
```

### Key Concepts

#### Vertex Data Structure
```python
# Each vertex: [x, y, z, r, g, b]
# Position (3 floats) + Color (3 floats) = 6 floats per vertex
```

#### Transformation Pipeline
- **Triangle**: Identity transforms (no projection)
- **Square**: Orthographic projection (aspect-corrected)
- **Cube**: Perspective projection + View matrix + Model rotation

#### OpenGL Features Used
- Vertex Buffer Objects (VBOs)
- Element Buffer Objects (EBOs)
- Vertex Array Objects (VAOs)
- Depth Testing (`GL_DEPTH_TEST`)
- GLSL Shader Programs
- Matrix Transformations (MVP)

### Code Walkthrough

#### Creating a VAO
```python
def create_vao(vertices, indices=None):
    """
    Creates a Vertex Array Object with interleaved position and color data
    - Position: location 0 (vec3)
    - Color: location 1 (vec3)
    """
    vao = glGenVertexArrays(1)
    vbo = glGenBuffers(1)
    # ... setup code
```

#### Rendering Loop
```python
while not glfw.window_should_close(window):
    # 1. Clear color and depth buffers
    # 2. Calculate MVP matrix
    # 3. Bind appropriate VAO
    # 4. Draw call (glDrawArrays or glDrawElements)
    # 5. Swap buffers and poll events
```

### Assignment Tasks

1. **Understand** - Trace through the rendering pipeline
2. **Modify** - Change vertex colors or positions
3. **Extend** - Add new geometric primitives (pyramid, octahedron, etc.)
4. **Experiment** - Adjust rotation speeds, camera positions, or projections
5. **Document** - Record observations about different projection types

### Troubleshooting

| Issue | Solution |
|-------|----------|
| **Black screen** | Verify shader files exist in `shaders/` directory |
| **Import errors** | Reinstall dependencies: `pip install -r requirements.txt` |
| **OpenGL errors** | Check GPU supports OpenGL 3.3+ |
| **Window not responding** | Verify GLFW initialization succeeds |

### Technical Notes
- Uses OpenGL 3.3 Core Profile
- VSync enabled (60 FPS cap)
- Depth testing for proper 3D occlusion
- Matrix operations via `pyrr` library
- Window management via `glfw`

### Extensions & Challenges

Try implementing:
- [ ] Pyramid or octahedron primitive
- [ ] Texture mapping
- [ ] Basic lighting (Phong/Blinn-Phong)
- [ ] Interactive camera controls (mouse/keyboard)
- [ ] Wireframe mode toggle
- [ ] Multiple objects in scene
- [ ] Object picking with mouse
- [ ] Shadow mapping
- [ ] Normal mapping

### Resources

- [LearnOpenGL](https://learnopengl.com/) - Comprehensive modern OpenGL tutorial
- [OpenGL Documentation](https://www.opengl.org/documentation/) - Official API reference
- [PyOpenGL Documentation](http://pyopengl.sourceforge.net/documentation/) - Python bindings
- [Pyrr Documentation](https://pyrr.readthedocs.io/) - Matrix/vector math
- [GLFW Documentation](https://www.glfw.org/documentation.html) - Window/input management
- [OpenGL Wiki](https://www.khronos.org/opengl/wiki/) - Community knowledge base

### Discussion Questions

1. What's the difference between `glDrawArrays` and `glDrawElements`?
2. Why do we need separate Model, View, and Projection matrices?
3. What happens if depth testing is disabled for the cube?
4. How does GPU interpolate vertex attributes across triangles?
5. What's the purpose of binding and unbinding VAOs?
6. Why use indexed rendering for the square and cube?

### Course Information

**Course**: CSC402 - Computer Graphics  
**Instructor**: Dr. Sheraz Aslam  
**Lab**: 1 - OpenGL Primitives  
**Institution**: CTL eurocollege, Limassol, Cyprus 

### Contributing

This is an educational repository. Students are encouraged to:
- Fork the repository
- Experiment with modifications
- Share interesting extensions
- Submit pull requests with improvements

### License

This project is for educational purposes only. All rights reserved for course materials.


### Acknowledgments

- OpenGL community for excellent documentation
- PyOpenGL developers for Python bindings
- Students of CSC402 for feedback and contributions

---

**Made with ❤️ for CSC402 Students**
