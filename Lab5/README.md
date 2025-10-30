# Lab 5: Multiple 3D Objects with Camera Control (OpenGL & Shaders)

This lab demonstrates how to render **multiple 3D objects** in a scene with **real-time camera control** using the keyboard and mouse.  
It uses **Python + PyGame + PyOpenGL + NumPy** to create an interactive 3D environment where the user can move, look around, and observe multiple rotating cubes.

---

## How It Works

### 1. **Shaders**

- **`vertex.glsl`**: Transforms 3D vertices into clip space and passes lighting and color information to the fragment shader.  
- **`fragment.glsl`**: Computes the final color of each pixel using interpolated attributes (color, lighting, and normals).

### 2. **Python (`main.py`)**

- Initializes **PyGame** and sets up an **OpenGL rendering window**.  
- Loads and compiles **vertex and fragment shaders** into a shader program.  
- Creates a **shared vertex buffer** containing cube vertices, normals, and colors.  
- Defines multiple **3D cube objects** with unique positions, rotations, and colors.  
- Implements a **Camera class** that handles movement (`W`, `A`, `S`, `D`, `SPACE`, `SHIFT`) and mouse-based view rotation.  
- Renders all cubes in the scene with **depth testing** and **polygon offset** to reduce z-fighting.  
- Continuously updates cube rotations and camera movement in real time.

---

## Uniform Variables in Shaders

| **Uniform Name** | **Type** | **Description** |
|------------------|----------|-----------------|
| `model`          | `mat4`   | Model transformation matrix for each object |
| `view`           | `mat4`   | Camera view matrix (from `Camera` class) |
| `projection`     | `mat4`   | Perspective projection matrix |
| `normalMatrix`   | `mat3`   | Transformed normals for lighting calculations (optional) |

---

## Example Features Explained

- **Multiple Objects** — Several colored cubes are drawn using a single vertex buffer and indexed rendering.  
- **Camera Control** — The user can move freely in 3D space using keyboard and mouse.  
- **Depth Testing** — Ensures correct visibility of overlapping objects.  
- **Polygon Offset** — Minimizes z-fighting between overlapping faces.  
- **Dynamic Rotation** — Each cube rotates continuously around different axes.  

---

## Learning Objectives

By completing this lab, students will:

- Understand how to render **multiple 3D objects** efficiently using a **shared vertex buffer**.  
- Learn how to implement a **camera system** with first-person movement and mouse look.  
- Explore how to **pass matrices** (model, view, projection) to shaders for 3D rendering.  
- Practice **shader program compilation and linking** in Python using **PyOpenGL**.  
- Learn to manage **depth testing and z-fighting** in complex 3D scenes.

---

## Cleanup

The program deletes all OpenGL objects (VAOs, VBOs, shader programs) and properly terminates **PyGame** when the window is closed.

---

## 📚 References

- [OpenGL Shaders Overview](https://www.khronos.org/opengl/wiki/OpenGL_Shading_Language)  
- [PyOpenGL Documentation](http://pyopengl.sourceforge.net/documentation/)  
- [PyGame Documentation](https://www.pygame.org/docs/)  
- [GLU and Matrix Transformations](https://www.khronos.org/opengl/wiki/GLU)  
- [NumPy Documentation](https://numpy.org/doc/)
