import glfw
from OpenGL.GL import *
import numpy as np
import math
from utils import load_program
import my_camera

def main():
    # Initialize GLFW
    if not glfw.init():
        raise Exception("GLFW initialization failed")
    
    # Create window
    window = glfw.create_window(800, 600, "Transformations Lab", None, None)
    if not window:
        glfw.terminate()
        raise Exception("Window creation failed")
    
    glfw.make_context_current(window)
    glEnable(GL_DEPTH_TEST)

    # Load shader program
    program = load_program("shaders/vertex.glsl", "shaders/fragment.glsl")

    # Cube vertices (position + color)
    vertices = np.array([
        # positions        # colors
        -0.5, -0.5, -0.5,  1, 0, 0,
         0.5, -0.5, -0.5,  0, 1, 0,
         0.5,  0.5, -0.5,  0, 0, 1,
        -0.5,  0.5, -0.5,  1, 1, 0,
        -0.5, -0.5,  0.5,  1, 0, 1,
         0.5, -0.5,  0.5,  0, 1, 1,
         0.5,  0.5,  0.5,  1, 1, 1,
        -0.5,  0.5,  0.5,  0, 0, 0
    ], dtype=np.float32)

    # Cube indices
    indices = np.array([
        0,1,2, 2,3,0,  # back
        4,5,6, 6,7,4,  # front
        0,4,7, 7,3,0,  # left
        1,5,6, 6,2,1,  # right
        3,2,6, 6,7,3,  # top
        0,1,5, 5,4,0   # bottom
    ], dtype=np.uint32)

    # Create VAO
    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)

    # Create VBO
    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    # Create EBO
    ebo = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

    # Position attribute
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)
    
    # Color attribute
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
    glEnableVertexAttribArray(1)

    # Use shader program
    glUseProgram(program)

    # Get uniform locations
    model_loc = glGetUniformLocation(program, "model")
    view_loc = glGetUniformLocation(program, "view")
    proj_loc = glGetUniformLocation(program, "projection")

    # Camera setup
    eye = np.array([1.5, 1.5, 2.5], dtype=np.float32)
    target = np.array([0, 0, 0], dtype=np.float32)
    up = np.array([0, 1, 0], dtype=np.float32)
    aspect = 800.0 / 600.0
    projection = my_camera.perspective(math.radians(45), aspect, 0.1, 100.0)

    # Transformation variables
    angle_x, angle_y = 0.0, 0.0
    pos = np.array([0.0, 0.0, 0.0], dtype=np.float32)

    # Key callback for controls
    def key_callback(window, key, scancode, action, mods):
        nonlocal pos, angle_x, angle_y
        if action == glfw.PRESS or action == glfw.REPEAT:
            if key == glfw.KEY_UP: 
                pos[1] += 0.1
            elif key == glfw.KEY_DOWN: 
                pos[1] -= 0.1
            elif key == glfw.KEY_LEFT: 
                pos[0] -= 0.1
            elif key == glfw.KEY_RIGHT: 
                pos[0] += 0.1
            elif key == glfw.KEY_W: 
                angle_x += 5
            elif key == glfw.KEY_S: 
                angle_x -= 5
            elif key == glfw.KEY_A: 
                angle_y += 5
            elif key == glfw.KEY_D: 
                angle_y -= 5

    glfw.set_key_callback(window, key_callback)

    # Main render loop
    while not glfw.window_should_close(window):
        # Clear buffers
        glClearColor(0.1, 0.1, 0.15, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Create model matrix (Translation * Rotation)
        # Rotation around X-axis
        rad_x = math.radians(angle_x)
        rot_x = np.array([
            [1, 0, 0, 0],
            [0, math.cos(rad_x), -math.sin(rad_x), 0],
            [0, math.sin(rad_x), math.cos(rad_x), 0],
            [0, 0, 0, 1]
        ], dtype=np.float32)
        
        # Rotation around Y-axis
        rad_y = math.radians(angle_y)
        rot_y = np.array([
            [math.cos(rad_y), 0, math.sin(rad_y), 0],
            [0, 1, 0, 0],
            [-math.sin(rad_y), 0, math.cos(rad_y), 0],
            [0, 0, 0, 1]
        ], dtype=np.float32)
        
        # Translation matrix
        trans = np.eye(4, dtype=np.float32)
        trans[:3, 3] = pos
        
        # Combine transformations
        model = trans @ rot_x @ rot_y

        # Create view matrix
        view = my_camera.look_at(eye, target, up)

        # Upload matrices to shaders (transpose for OpenGL)
        glUniformMatrix4fv(model_loc, 1, GL_TRUE, model)
        glUniformMatrix4fv(view_loc, 1, GL_TRUE, view)
        glUniformMatrix4fv(proj_loc, 1, GL_TRUE, projection)

        # Draw cube
        glBindVertexArray(vao)
        glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)

        # Swap buffers and poll events
        glfw.swap_buffers(window)
        glfw.poll_events()

    # Cleanup
    glDeleteVertexArrays(1, [vao])
    glDeleteBuffers(1, [vbo])
    glDeleteBuffers(1, [ebo])
    glDeleteProgram(program)
    glfw.terminate()

if __name__ == "__main__":
    main()