# main.py
import glfw
from OpenGL.GL import *
import numpy as np
from shader import create_program_from_files
from pyrr import Matrix44, Vector3
import time
import os

# ----- Helper: create VAO from vertex data -----
def create_vao(vertices, indices=None):
    # vertices: numpy array float32 (pos3,color3 interleaved)
    vao = glGenVertexArrays(1)
    vbo = glGenBuffers(1)
    glBindVertexArray(vao)

    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    if indices is not None:
        ebo = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)
    else:
        ebo = None

    # location 0 = position (vec3), location 1 = color (vec3)
    stride = vertices.strides[0]
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(12))

    glBindVertexArray(0)
    return vao, vbo, ebo

# ----- Vertex data -----
# Triangle (2D, z=0)
triangle_vertices = np.array([
    # x, y, z,    r, g, b
    -0.6, -0.4, 0.0,  1.0, 0.0, 0.0,
     0.6, -0.4, 0.0,  0.0, 1.0, 0.0,
     0.0,  0.6, 0.0,  0.0, 0.0, 1.0,
], dtype=np.float32)

# Square (two triangles)
square_vertices = np.array([
    # x, y, z,    r, g, b
    -0.5, -0.5, 0.0,  1.0, 0.5, 0.0,
     0.5, -0.5, 0.0,  0.0, 1.0, 0.5,
     0.5,  0.5, 0.0,  0.5, 0.0, 1.0,
    -0.5,  0.5, 0.0,  1.0, 1.0, 0.0,
], dtype=np.float32)
square_indices = np.array([0,1,2,  2,3,0], dtype=np.uint32)

# Cube (3D) - 8 vertices, colors
cube_vertices = np.array([
    # x,y,z       r,g,b
    -0.5,-0.5,-0.5,  1,0,0,
     0.5,-0.5,-0.5,  0,1,0,
     0.5, 0.5,-0.5,  0,0,1,
    -0.5, 0.5,-0.5,  1,1,0,
    -0.5,-0.5, 0.5,  1,0,1,
     0.5,-0.5, 0.5,  0,1,1,
     0.5, 0.5, 0.5,  1,1,1,
    -0.5, 0.5, 0.5,  0.2,0.6,0.9,
], dtype=np.float32)

cube_indices = np.array([
    # back face
    0,1,2, 2,3,0,
    # front face
    4,5,6, 6,7,4,
    # left
    0,4,7, 7,3,0,
    # right
    1,5,6, 6,2,1,
    # bottom
    0,1,5, 5,4,0,
    # top
    3,2,6, 6,7,3
], dtype=np.uint32)

# ----- Main -----
def main():
    if not glfw.init():
        raise RuntimeError("glfw init failed")
    # Request OpenGL 3.3 core
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    window = glfw.create_window(800, 600, "pyOpenGL primitives", None, None)
    if not window:
        glfw.terminate()
        raise RuntimeError("Failed to create window")

    glfw.make_context_current(window)
    # vsync on
    glfw.swap_interval(1)

    # compile shader program from files
    here = os.path.dirname(os.path.abspath(__file__))
    vert_path = os.path.join(here, "shaders", "basic.vert.glsl")
    frag_path = os.path.join(here, "shaders", "basic.frag.glsl")
    program = create_program_from_files(vert_path, frag_path)

    # create VAOs
    tri_vao, tri_vbo, _ = create_vao(triangle_vertices)
    quad_vao, quad_vbo, quad_ebo = create_vao(square_vertices, square_indices)
    cube_vao, cube_vbo, cube_ebo = create_vao(cube_vertices, cube_indices)

    # enable depth for 3D cube
    glEnable(GL_DEPTH_TEST)

    # uniform location
    uMVP_loc = glGetUniformLocation(program, "uMVP")

    start_time = time.time()
    current_prim = 1  # 1=triangle, 2=square, 3=cube

    def key_callback(window, key, scancode, action, mods):
        nonlocal current_prim
        if action == glfw.PRESS:
            if key == glfw.KEY_1:
                current_prim = 1
            elif key == glfw.KEY_2:
                current_prim = 2
            elif key == glfw.KEY_3:
                current_prim = 3
            elif key == glfw.KEY_ESCAPE:
                glfw.set_window_should_close(window, True)

    glfw.set_key_callback(window, key_callback)

    while not glfw.window_should_close(window):
        now = time.time()
        t = now - start_time

        width, height = glfw.get_framebuffer_size(window)
        aspect = width / height if height > 0 else 1.0
        glViewport(0,0,width,height)
        glClearColor(0.12, 0.12, 0.15, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glUseProgram(program)

        if current_prim == 1:
            # Triangle: orthographic-ish, no depth
            proj = Matrix44.identity()
            view = Matrix44.identity()
            model = Matrix44.from_scale([1.0, 1.0, 1.0])
            mvp = proj * view * model
            glUniformMatrix4fv(uMVP_loc, 1, GL_FALSE, mvp.astype('float32').flatten())
            glBindVertexArray(tri_vao)
            glDrawArrays(GL_TRIANGLES, 0, 3)

        elif current_prim == 2:
            # Square: use orthographic projection mapping to aspect
            proj = Matrix44.orthogonal_projection(-aspect, aspect, -1, 1, -1, 1)
            view = Matrix44.identity()
            model = Matrix44.identity()
            mvp = proj * view * model
            glUniformMatrix4fv(uMVP_loc, 1, GL_FALSE, mvp.astype('float32').flatten())
            glBindVertexArray(quad_vao)
            glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)

        else:
            # Cube: perspective + basic rotation
            proj = Matrix44.perspective_projection(45.0, aspect, 0.1, 100.0)
            cam_pos = Vector3([3.0, 3.0, 3.0])
            view = Matrix44.look_at(eye=cam_pos, target=Vector3([0.0,0.0,0.0]), up=Vector3([0.0,1.0,0.0]))
            rot = Matrix44.from_y_rotation(t * 0.9) * Matrix44.from_x_rotation(t * 0.6)
            model = rot
            trans = Matrix44.from_translation([0.0, 0.0, 0.0])
            mvp = proj * view * trans * model
            glUniformMatrix4fv(uMVP_loc, 1, GL_FALSE, mvp.astype('float32').flatten())
            glBindVertexArray(cube_vao)
            glDrawElements(GL_TRIANGLES, len(cube_indices), GL_UNSIGNED_INT, None)

        glBindVertexArray(0)
        glUseProgram(0)

        glfw.swap_buffers(window)
        glfw.poll_events()

    # cleanup
    glDeleteVertexArrays(1, [tri_vao])
    glDeleteVertexArrays(1, [quad_vao])
    glDeleteVertexArrays(1, [cube_vao])
    glDeleteProgram(program)

    glfw.terminate()

if __name__ == "__main__":
    main()
