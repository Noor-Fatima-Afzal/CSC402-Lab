# Lab 4: 1D Convolution Filter using OpenGL & Shaders

This lab demonstrates how to apply **1D convolution filters** (such as blur, sharpen, and edge detection) to a generated texture using **OpenGL shaders**.  
It uses **Python + GLFW + PyOpenGL + NumPy** for rendering and texture manipulation.

---
## How It Works

### 1. **Shaders**

- **`vertex.glsl`**: Defines how vertices are positioned and passes texture coordinates to the fragment shader.  
- **`fragment.glsl`**: Applies the selected convolution filter (original, blur, sharpen, or edge detection) along a chosen direction.

### 2. **Python (`main.py`)**

- Initializes **GLFW** and creates an **OpenGL** window.  
- Compiles and links shaders into a **shader program**.  
- Creates a **test texture** using NumPy with colorful patterns.  
- Sends texture data and uniforms (filter type, direction, etc.) to the **GPU**.  
- Listens for **keyboard input** to switch between filters and directions.  
- Renders the filtered texture **in real-time**.

---

## Uniform Variables in Shaders

| **Uniform Name** | **Type** | **Description** |
|------------------|----------|-----------------|
| `filterType`     | `int`    | Selects which convolution filter to apply |
| `direction`      | `int`    | `0` for horizontal, `1` for vertical |
| `textureWidth`   | `float`  | Width of the input texture |
| `textureHeight`  | `float`  | Height of the input texture |
| `inputTexture`   | `sampler2D` | The texture being filtered |

---

## Example Filters Explained

- **Original** — Displays the texture without modification.  
- **Gaussian Blur** — Smoothens the image by averaging neighboring pixels.  
- **Sharpen** — Enhances edges and details in the image.  
- **Edge Detection** — Highlights boundaries and transitions in color or brightness.

---

## Learning Objectives

By completing this lab, students will:

- Understand how **fragment shaders** can perform image processing operations.  
- Learn about **1D convolution** in both horizontal and vertical directions.  
- Gain experience with **OpenGL buffer setup (VBO, VAO, EBO)**.  
- Practice **shader compilation and linking** in Python using **PyOpenGL**.

---

## Cleanup

The program deletes all allocated OpenGL objects and terminates **GLFW** properly when closed.

---

## 📚 References

- [OpenGL Shaders Overview](https://www.khronos.org/opengl/wiki/OpenGL_Shading_Language)  
- [PyOpenGL Documentation](http://pyopengl.sourceforge.net/documentation/)  
- [GLFW Python Wrapper](https://pypi.org/project/glfw/)  
- [NumPy Documentation](https://numpy.org/doc/)
