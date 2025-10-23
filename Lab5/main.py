import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import math

class Camera:
    def __init__(self):
        self.position = np.array([0.0, 0.0, 5.0])
        self.yaw = -90.0
        self.pitch = 0.0
        self.speed = 0.05
        self.sensitivity = 0.1
        
    def get_view_matrix(self):
        front = np.array([
            math.cos(math.radians(self.yaw)) * math.cos(math.radians(self.pitch)),
            math.sin(math.radians(self.pitch)),
            math.sin(math.radians(self.yaw)) * math.cos(math.radians(self.pitch))
        ])
        front = front / np.linalg.norm(front)
        
        target = self.position + front
        up = np.array([0.0, 1.0, 0.0])
        
        glLoadIdentity()
        gluLookAt(self.position[0], self.position[1], self.position[2],
                  target[0], target[1], target[2],
                  up[0], up[1], up[2])
    
    def process_keyboard(self, keys):
        front = np.array([
            math.cos(math.radians(self.yaw)) * math.cos(math.radians(self.pitch)),
            math.sin(math.radians(self.pitch)),
            math.sin(math.radians(self.yaw)) * math.cos(math.radians(self.pitch))
        ])
        front = front / np.linalg.norm(front)
        right = np.cross(front, np.array([0.0, 1.0, 0.0]))
        right = right / np.linalg.norm(right)
        
        if keys[K_w]:
            self.position += front * self.speed
        if keys[K_s]:
            self.position -= front * self.speed
        if keys[K_a]:
            self.position -= right * self.speed
        if keys[K_d]:
            self.position += right * self.speed
        if keys[K_SPACE]:
            self.position[1] += self.speed
        if keys[K_LSHIFT]:
            self.position[1] -= self.speed
    
    def process_mouse(self, xoffset, yoffset):
        xoffset *= self.sensitivity
        yoffset *= self.sensitivity
        
        self.yaw += xoffset
        self.pitch += yoffset
        
        if self.pitch > 89.0:
            self.pitch = 89.0
        if self.pitch < -89.0:
            self.pitch = -89.0

def load_shader(shader_file, shader_type):
    with open(shader_file, 'r') as f:
        shader_source = f.read()
    
    shader = glCreateShader(shader_type)
    glShaderSource(shader, shader_source)
    glCompileShader(shader)
    
    if not glGetShaderiv(shader, GL_COMPILE_STATUS):
        error = glGetShaderInfoLog(shader).decode()
        print(f"Shader compilation error: {error}")
        raise Exception(f"Shader compilation failed")
    
    return shader

def create_shader_program():
    vertex_shader = load_shader('shaders/vertex.glsl', GL_VERTEX_SHADER)
    fragment_shader = load_shader('shaders/fragment.glsl', GL_FRAGMENT_SHADER)
    
    program = glCreateProgram()
    glAttachShader(program, vertex_shader)
    glAttachShader(program, fragment_shader)
    glLinkProgram(program)
    
    if not glGetProgramiv(program, GL_LINK_STATUS):
        error = glGetProgramInfoLog(program).decode()
        print(f"Program linking error: {error}")
        raise Exception(f"Program linking failed")
    
    glDeleteShader(vertex_shader)
    glDeleteShader(fragment_shader)
    
    return program

def create_cube_vertices():
    # Shared vertex buffer for cube with positions, normals, and colors
    vertices = np.array([
        # positions          # normals           # colors
        # Front face (red)
        -0.5, -0.5,  0.5,    0.0,  0.0,  1.0,    1.0, 0.0, 0.0,
         0.5, -0.5,  0.5,    0.0,  0.0,  1.0,    1.0, 0.0, 0.0,
         0.5,  0.5,  0.5,    0.0,  0.0,  1.0,    1.0, 0.0, 0.0,
        -0.5,  0.5,  0.5,    0.0,  0.0,  1.0,    1.0, 0.0, 0.0,
        
        # Back face (green)
        -0.5, -0.5, -0.5,    0.0,  0.0, -1.0,    0.0, 1.0, 0.0,
         0.5, -0.5, -0.5,    0.0,  0.0, -1.0,    0.0, 1.0, 0.0,
         0.5,  0.5, -0.5,    0.0,  0.0, -1.0,    0.0, 1.0, 0.0,
        -0.5,  0.5, -0.5,    0.0,  0.0, -1.0,    0.0, 1.0, 0.0,
        
        # Top face (blue)
        -0.5,  0.5, -0.5,    0.0,  1.0,  0.0,    0.0, 0.0, 1.0,
         0.5,  0.5, -0.5,    0.0,  1.0,  0.0,    0.0, 0.0, 1.0,
         0.5,  0.5,  0.5,    0.0,  1.0,  0.0,    0.0, 0.0, 1.0,
        -0.5,  0.5,  0.5,    0.0,  1.0,  0.0,    0.0, 0.0, 1.0,
        
        # Bottom face (yellow)
        -0.5, -0.5, -0.5,    0.0, -1.0,  0.0,    1.0, 1.0, 0.0,
         0.5, -0.5, -0.5,    0.0, -1.0,  0.0,    1.0, 1.0, 0.0,
         0.5, -0.5,  0.5,    0.0, -1.0,  0.0,    1.0, 1.0, 0.0,
        -0.5, -0.5,  0.5,    0.0, -1.0,  0.0,    1.0, 1.0, 0.0,
        
        # Right face (magenta)
         0.5, -0.5, -0.5,    1.0,  0.0,  0.0,    1.0, 0.0, 1.0,
         0.5,  0.5, -0.5,    1.0,  0.0,  0.0,    1.0, 0.0, 1.0,
         0.5,  0.5,  0.5,    1.0,  0.0,  0.0,    1.0, 0.0, 1.0,
         0.5, -0.5,  0.5,    1.0,  0.0,  0.0,    1.0, 0.0, 1.0,
        
        # Left face (cyan)
        -0.5, -0.5, -0.5,   -1.0,  0.0,  0.0,    0.0, 1.0, 1.0,
        -0.5,  0.5, -0.5,   -1.0,  0.0,  0.0,    0.0, 1.0, 1.0,
        -0.5,  0.5,  0.5,   -1.0,  0.0,  0.0,    0.0, 1.0, 1.0,
        -0.5, -0.5,  0.5,   -1.0,  0.0,  0.0,    0.0, 1.0, 1.0,
    ], dtype=np.float32)
    
    indices = np.array([
        0,  1,  2,  2,  3,  0,   # front
        4,  5,  6,  6,  7,  4,   # back
        8,  9,  10, 10, 11, 8,   # top
        12, 13, 14, 14, 15, 12,  # bottom
        16, 17, 18, 18, 19, 16,  # right
        20, 21, 22, 22, 23, 20,  # left
    ], dtype=np.uint32)
    
    return vertices, indices

def setup_vertex_buffer(vertices, indices):
    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)
    
    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
    
    ebo = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)
    
    stride = 9 * vertices.itemsize
    
    # Position attribute
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)
    
    # Normal attribute
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(3 * vertices.itemsize))
    glEnableVertexAttribArray(1)
    
    # Color attribute
    glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(6 * vertices.itemsize))
    glEnableVertexAttribArray(2)
    
    glBindVertexArray(0)
    
    return vao, len(indices)

def main():
    pygame.init()
    display = (1280, 720)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Lab4 - Multiple Objects with Camera Control")
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)
    
    # Enable depth testing and handle z-fighting with polygon offset
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)  # Use LEQUAL to handle equal depth values better
    glEnable(GL_POLYGON_OFFSET_FILL)  # Enable polygon offset to reduce z-fighting
    
    # Set up projection
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, (display[0] / display[1]), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    
    # Create shader program
    shader = create_shader_program()
    
    # Create shared vertex buffer
    vertices, indices = create_cube_vertices()
    vao, index_count = setup_vertex_buffer(vertices, indices)
    
    # Create camera
    camera = Camera()
    
    # Object positions
    objects = [
        {'pos': (0.0, 0.0, 0.0), 'rotation': 0.0, 'axis': (1, 1, 0), 'offset': 0.0},
        {'pos': (2.0, 0.5, -1.0), 'rotation': 0.0, 'axis': (0, 1, 1), 'offset': 0.001},
        {'pos': (-2.0, -0.5, -1.5), 'rotation': 0.0, 'axis': (1, 0, 1), 'offset': 0.002},
        {'pos': (0.0, 2.0, -2.0), 'rotation': 0.0, 'axis': (1, 1, 1), 'offset': 0.003},
        {'pos': (1.5, -1.5, -0.5), 'rotation': 0.0, 'axis': (0, 1, 0), 'offset': 0.004},
    ]
    
    clock = pygame.time.Clock()
    last_x, last_y = display[0] // 2, display[1] // 2
    first_mouse = True
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        # Mouse input
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if first_mouse:
            last_x, last_y = mouse_x, mouse_y
            first_mouse = False
        
        xoffset = mouse_x - last_x
        yoffset = last_y - mouse_y  # Reversed
        last_x, last_y = mouse_x, mouse_y
        
        camera.process_mouse(xoffset, yoffset)
        
        # Keyboard input
        keys = pygame.key.get_pressed()
        camera.process_keyboard(keys)
        
        # Clear buffers
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0.1, 0.1, 0.15, 1.0)
        
        # Use shader
        glUseProgram(shader)
        
        # Set view matrix
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        camera.get_view_matrix()
        
        # Get matrices for shader
        modelview = glGetFloatv(GL_MODELVIEW_MATRIX)
        projection = glGetFloatv(GL_PROJECTION_MATRIX)
        
        model_loc = glGetUniformLocation(shader, "model")
        view_loc = glGetUniformLocation(shader, "view")
        proj_loc = glGetUniformLocation(shader, "projection")
        
        glUniformMatrix4fv(view_loc, 1, GL_FALSE, modelview)
        glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)
        
        # Bind shared vertex array
        glBindVertexArray(vao)
        
        # Draw multiple objects using shared vertex buffer
        for i, obj in enumerate(objects):
            # Apply polygon offset to reduce z-fighting
            glPolygonOffset(obj['offset'], obj['offset'])
            
            glPushMatrix()
            
            # Transform for this object
            glTranslatef(*obj['pos'])
            glRotatef(obj['rotation'], *obj['axis'])
            
            # Get model matrix and send to shader
            model = glGetFloatv(GL_MODELVIEW_MATRIX)
            glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
            
            # Draw
            glDrawElements(GL_TRIANGLES, index_count, GL_UNSIGNED_INT, None)
            
            glPopMatrix()
            
            # Update rotation
            obj['rotation'] += 0.5 + i * 0.1
        
        pygame.display.flip()
        clock.tick(60)
    
    # Cleanup
    glDeleteVertexArrays(1, [vao])
    glDeleteProgram(shader)
    pygame.quit()

if __name__ == "__main__":
    main()