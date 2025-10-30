# Lab 6: Texture Mapping with Mipmapping and Tiling (OpenGL & Shaders)

This lab demonstrates **advanced texture mapping techniques** such as **mipmapping**, **texture tiling**, and **procedural texture generation** using **OpenGL shaders**.  
It uses **Python + PyGame + PyOpenGL + NumPy + Pillow (PIL)** to render textured 3D objects with efficient filtering and perspective-correct interpolation.

---

## How It Works

### 1. **Shaders**

- **`vertex.glsl`**: Transforms 3D vertices, passes normals and texture coordinates to the fragment shader for proper lighting and texture interpolation.  
- **`fragment.glsl`**: Samples the texture using mipmaps and applies trilinear filtering for smooth and realistic texture detail.

### 2. **Python (`main.py`)**

- Initializes **PyGame** and sets up an **OpenGL rendering context**.  
- Compiles and links **vertex** and **fragment shaders** into a shader program.  
- Implements a **Camera** class for first-person movement and mouse look-around.  
- Generates **procedural textures** (checkerboard, brick, grid, dots) dynamically using NumPy.  
- Demonstrates **texture tiling** (1x, 2x, 4x, 10x) and **mipmapping** for smooth texture scaling.  
- Renders multiple textured cubes and a large ground plane in 3D space.  
- Displays an **on-screen HUD** with key information and controls (toggle with `H`).  

---

## Uniform Variables in Shaders

| **Uniform Name** | **Type** | **Description** |
|------------------|----------|-----------------|
| `model`          | `mat4`   | Model transformation matrix for each object |
| `view`           | `mat4`   | View (camera) matrix |
| `projection`     | `mat4`   | Perspective projection matrix |
| `textureSampler` | `sampler2D` | Texture sampler for the object’s surface |

---

## Example Features Explained

- **Procedural Textures** — Generated in code (checkerboard, brick, grid, dots) without external image files.  
- **Mipmapping** — Uses trilinear filtering (`GL_LINEAR_MIPMAP_LINEAR`) for smoother transitions at varying distances.  
- **Tiling** — Demonstrates multiple texture repetition levels (`1x`, `2x`, `4x`, and `10x`) for visual comparison.  
- **Perspective-Correct Interpolation** — Ensures textures look realistic on surfaces angled from the camera.  
- **Multiple Textures in One Scene** — Different objects use unique procedural textures simultaneously.  
- **Interactive Camera** — Move freely in 3D using `W/A/S/D`, mouse look, and vertical motion (`Space`/`Shift`).  
- **Toggleable Information Overlay** — Press `H` to show or hide instructions and rendering details.

---

## Learning Objectives

By completing this lab, students will:

- Understand how **texture mapping** works in OpenGL and how to apply it to 3D geometry.  
- Learn the concept and benefits of **mipmapping** and **trilinear filtering**.  
- Explore **procedural texture generation** techniques using **NumPy arrays**.  
- Learn how to control **texture wrapping and tiling** with `GL_REPEAT`.  
- Implement **interactive camera control** for navigating textured 3D scenes.  
- Gain hands-on experience combining multiple **OpenGL rendering techniques** in a single program.

---

## Cleanup

The program deletes all loaded textures and shader programs, clears VAOs/VBOs, and properly terminates **PyGame** when the window is closed.

---

## 📚 References

- [OpenGL Texture Mapping](https://www.khronos.org/opengl/wiki/Texture_Mapping)  
- [Mipmapping Explained](https://learnopengl.com/Getting-started/Textures)  
- [PyOpenGL Documentation](http://pyopengl.sourceforge.net/documentation/)  
- [PyGame Documentation](https://www.pygame.org/docs/)  
- [NumPy Documentation](https://numpy.org/doc/)  
- [Pillow (PIL) Documentation](https://pillow.readthedocs.io/en/stable/)
