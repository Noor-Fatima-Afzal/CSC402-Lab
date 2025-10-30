# Lab 7: 3D Model Rendering with Phong Lighting (OpenGL & Shaders)

This lab demonstrates **3D model loading, transformation, and real-time lighting** using the **Phong reflection model**.  
It uses **Python + PyGame + PyOpenGL + NumPy** to render 3D objects with realistic shading and interactive camera controls.

---

## How It Works

### 1. **Shaders**

- **`vertex.glsl`**: Transforms vertex positions and normals into view space. Passes lighting vectors and normal data to the fragment shader.  
- **`fragment.glsl`**: Implements the **Phong lighting model** combining ambient, diffuse, and specular components for realistic shading.

### 2. **Python (`main.py`)**

- Initializes **PyGame** and sets up an **OpenGL context** with depth testing and back-face culling.  
- Loads or creates a 3D model (from `model.obj` or a default cube if no file is found).  
- Compiles and links **vertex and fragment shaders** into a shader program.  
- Implements a **Camera class** for first-person style movement and mouse-based orientation.  
- Sets up **projection**, **view**, and **model** matrices to transform 3D objects in the scene.  
- Defines and updates **lighting parameters** (light position, color, and strength) and **material properties** (ambient, diffuse, specular).  
- Continuously rotates the 3D object and renders it with **Phong shading** in real time.

---

## Uniform Variables in Shaders

| **Uniform Name** | **Type** | **Description** |
|------------------|----------|-----------------|
| `model`              | `mat4`   | Object transformation matrix |
| `view`               | `mat4`   | Camera view matrix |
| `projection`         | `mat4`   | Perspective projection matrix |
| `lightPos`           | `vec3`   | World-space position of the light source |
| `viewPos`            | `vec3`   | Camera position for specular reflection |
| `lightColor`         | `vec3`   | Color/intensity of the light |
| `objectColor`        | `vec3`   | Base color of the 3D object |
| `ambientStrength`    | `float`  | Controls the brightness of ambient lighting |
| `specularStrength`   | `float`  | Intensity of specular highlights |
| `shininess`          | `float`  | Controls the size/sharpness of specular reflections |

---

## Example Features Explained

- **3D Model Loading** — Loads `.obj` models with vertex and normal data; falls back to a built-in cube if the file is missing.  
- **Phong Lighting** — Combines ambient, diffuse, and specular lighting components for realistic rendering.  
- **Camera System** — Allows movement (`W/A/S/D`, `SPACE`, `SHIFT`) and mouse look-around.  
- **Matrix Transformations** — Uses model, view, and projection matrices for accurate 3D transformations.  
- **Dynamic Rotation** — Continuously rotates the model around the Y-axis for demonstration.  
- **Back-Face Culling** — Improves performance by discarding faces not visible to the camera.  
- **Adjustable Light and Material Settings** — Parameters such as light position, color, and shininess can be tuned easily.

---

## Learning Objectives

By completing this lab, students will:

- Understand the **Phong lighting model** and how it simulates realistic light reflection.  
- Learn how to **load 3D models** from `.obj` files and parse vertex/normal data.  
- Implement **matrix transformations** (model, view, projection) manually in OpenGL.  
- Develop an understanding of **camera control systems** using keyboard and mouse input.  
- Gain experience with **shader programming** and the GPU lighting pipeline.  
- Learn how to combine **lighting, movement, and transformations** in real-time 3D rendering.

---

## Cleanup

The program deletes all OpenGL buffers, vertex arrays, and shader programs, and properly terminates **PyGame** when closed.

---

## 📚 References

- [Phong Lighting Model (OpenGL Wiki)](https://www.khronos.org/opengl/wiki/Phong_reflection_model)  
- [PyOpenGL Documentation](http://pyopengl.sourceforge.net/documentation/)  
- [PyGame Documentation](https://www.pygame.org/docs/)  
- [LearnOpenGL - Lighting](https://learnopengl.com/Lighting/Basic-Lighting)  
- [NumPy Documentation](https://numpy.org/doc/)
