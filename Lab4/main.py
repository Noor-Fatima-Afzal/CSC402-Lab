import glfw
from OpenGL.GL import *
import numpy as np
import ctypes

def load_shader(shader_file, shader_type):
    with open(shader_file, 'r') as f:
        shader_src = f.read()
    shader = glCreateShader(shader_type)
    glShaderSource(shader, shader_src)
    glCompileShader(shader)
    if not glGetShaderiv(shader, GL_COMPILE_STATUS):
        raise RuntimeError(glGetShaderInfoLog(shader).decode())
    return shader

def load_program(vs_path, fs_path):
    vertex_shader = load_shader(vs_path, GL_VERTEX_SHADER)
    fragment_shader = load_shader(fs_path, GL_FRAGMENT_SHADER)
    program = glCreateProgram()
    glAttachShader(program, vertex_shader)
    glAttachShader(program, fragment_shader)
    glLinkProgram(program)
    if not glGetProgramiv(program, GL_LINK_STATUS):
        raise RuntimeError(glGetProgramInfoLog(program).decode())
    glDeleteShader(vertex_shader)
    glDeleteShader(fragment_shader)
    return program

def create_test_texture(width, height):
    data = np.zeros((height, width, 3), dtype=np.uint8)
    
    for y in range(height):
        for x in range(width):
            if x % 40 < 20:
                data[y, x] = [255, 0, 0]
            else:
                data[y, x] = [0, 255, 255]
            
            if y % 60 < 30:
                data[y, x] = data[y, x] // 2 + np.array([0, 0, 128], dtype=np.uint8)
            
            if (x + y) % 80 < 40:
                data[y, x] = data[y, x] // 2 + np.array([128, 128, 0], dtype=np.uint8)
    
    return data

def main():
    if not glfw.init():
        raise Exception("GLFW initialization failed")
    
    width, height = 1200, 600
    window = glfw.create_window(width, height, "1D Convolution Filter Lab", None, None)
    if not window:
        glfw.terminate()
        raise Exception("Window creation failed")
    
    glfw.make_context_current(window)
    
    program = load_program("shaders/vertex.glsl", "shaders/fragment.glsl")
    
    vertices = np.array([
        -1.0, -1.0,     0.0, 0.0,
         1.0, -1.0,     1.0, 0.0,
         1.0,  1.0,     1.0, 1.0,
        -1.0,  1.0,     0.0, 1.0,
    ], dtype=np.float32)
    
    indices = np.array([0, 1, 2, 2, 3, 0], dtype=np.uint32)
    
    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)
    
    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
    
    ebo = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)
    
    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 16, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)
    
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 16, ctypes.c_void_p(8))
    glEnableVertexAttribArray(1)
    
    tex_width, tex_height = 512, 512
    texture_data = create_test_texture(tex_width, tex_height)
    
    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, tex_width, tex_height, 0, 
                 GL_RGB, GL_UNSIGNED_BYTE, texture_data)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    
    glUseProgram(program)
    
    filter_loc = glGetUniformLocation(program, "filterType")
    width_loc = glGetUniformLocation(program, "textureWidth")
    height_loc = glGetUniformLocation(program, "textureHeight")
    direction_loc = glGetUniformLocation(program, "direction")
    texture_loc = glGetUniformLocation(program, "inputTexture")
    
    glUniform1i(texture_loc, 0)
    glUniform1f(width_loc, float(tex_width))
    glUniform1f(height_loc, float(tex_height))
    
    current_filter = 0
    current_direction = 0
    
    filter_names = ["Original", "Blur", "Sharpen", "Edge Detection"]
    direction_names = ["Horizontal", "Vertical"]
    
    def key_callback(window, key, scancode, action, mods):
        nonlocal current_filter, current_direction
        if action == glfw.PRESS:
            if key == glfw.KEY_1:
                current_filter = 0
                print(f"Filter: {filter_names[current_filter]}")
            elif key == glfw.KEY_2:
                current_filter = 1
                print(f"Filter: {filter_names[current_filter]} ({direction_names[current_direction]})")
            elif key == glfw.KEY_3:
                current_filter = 2
                print(f"Filter: {filter_names[current_filter]} ({direction_names[current_direction]})")
            elif key == glfw.KEY_4:
                current_filter = 3
                print(f"Filter: {filter_names[current_filter]} ({direction_names[current_direction]})")
            elif key == glfw.KEY_SPACE:
                current_direction = 1 - current_direction
                print(f"Direction: {direction_names[current_direction]}")
            elif key == glfw.KEY_ESCAPE:
                glfw.set_window_should_close(window, True)
    
    glfw.set_key_callback(window, key_callback)
    
    print("\n" + "="*40)
    print("  1D CONVOLUTION FILTER LAB")
    print("="*40)
    print("\nControls:")
    print("  1 - Original (no filter)")
    print("  2 - Gaussian Blur")
    print("  3 - Sharpen")
    print("  4 - Edge Detection")
    print("  SPACE - Toggle direction (Horizontal/Vertical)")
    print("  ESC - Exit")
    print("\n" + "="*40)
    print(f"Current: {filter_names[current_filter]}")
    print("="*40 + "\n")
    
    while not glfw.window_should_close(window):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)
        
        glUniform1i(filter_loc, current_filter)
        glUniform1i(direction_loc, current_direction)
        
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, texture)
        
        glBindVertexArray(vao)
        glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)
        
        glfw.swap_buffers(window)
        glfw.poll_events()
    
    glDeleteVertexArrays(1, [vao])
    glDeleteBuffers(1, [vbo])
    glDeleteBuffers(1, [ebo])
    glDeleteTextures(1, [texture])
    glDeleteProgram(program)
    glfw.terminate()

if __name__ == "__main__":
    main()