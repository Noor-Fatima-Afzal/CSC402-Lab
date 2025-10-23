import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import math
from PIL import Image

class Camera:
    def __init__(self):
        self.position = np.array([0.0, 2.0, 8.0])
        self.yaw = -90.0
        self.pitch = -15.0
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

def generate_procedural_texture(width, height, pattern='checkerboard'):
    """Generate procedural textures"""
    image = np.zeros((height, width, 3), dtype=np.uint8)
    
    if pattern == 'checkerboard':
        for i in range(height):
            for j in range(width):
                if (i // 32 + j // 32) % 2 == 0:
                    image[i, j] = [255, 255, 255]
                else:
                    image[i, j] = [50, 50, 50]
    
    elif pattern == 'brick':
        brick_height = 32
        brick_width = 64
        mortar = 4
        
        for i in range(height):
            for j in range(width):
                row = i // brick_height
                offset = (row % 2) * (brick_width // 2)
                col = (j + offset) % (brick_width + mortar)
                
                if i % brick_height < mortar or col < mortar:
                    image[i, j] = [200, 200, 200]  # Mortar
                else:
                    # Brick color with variation
                    variation = (i % brick_height + j % brick_width) % 30
                    image[i, j] = [180 + variation, 80 + variation // 2, 50]
    
    elif pattern == 'grid':
        grid_size = 64
        line_width = 4
        
        for i in range(height):
            for j in range(width):
                if i % grid_size < line_width or j % grid_size < line_width:
                    image[i, j] = [0, 255, 255]  # Cyan lines
                else:
                    image[i, j] = [30, 30, 50]  # Dark background
    
    elif pattern == 'dots':
        for i in range(height):
            for j in range(width):
                x = j % 64 - 32
                y = i % 64 - 32
                dist = math.sqrt(x*x + y*y)
                if dist < 20:
                    image[i, j] = [255, 100, 200]  # Pink dots
                else:
                    image[i, j] = [240, 240, 255]  # Light background
    
    return image

def load_texture(pattern='checkerboard', use_mipmaps=True):
    """Load texture with mipmapping support"""
    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    
    # Generate procedural texture
    img_data = generate_procedural_texture(512, 512, pattern)
    
    # Texture parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    
    if use_mipmaps:
        # Enable mipmapping with trilinear filtering
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        
        # Upload texture and generate mipmaps
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, 512, 512, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
        glGenerateMipmap(GL_TEXTURE_2D)
    else:
        # No mipmapping, just bilinear filtering
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, 512, 512, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
    
    return texture

def create_cube_vertices(tex_scale=1.0):
    """Create cube with texture coordinates (tiling controlled by tex_scale)"""
    vertices = np.array([
        # positions          # normals           # tex coords
        # Front face
        -0.5, -0.5,  0.5,    0.0,  0.0,  1.0,    0.0, 0.0,
         0.5, -0.5,  0.5,    0.0,  0.0,  1.0,    tex_scale, 0.0,
         0.5,  0.5,  0.5,    0.0,  0.0,  1.0,    tex_scale, tex_scale,
        -0.5,  0.5,  0.5,    0.0,  0.0,  1.0,    0.0, tex_scale,
        
        # Back face
         0.5, -0.5, -0.5,    0.0,  0.0, -1.0,    0.0, 0.0,
        -0.5, -0.5, -0.5,    0.0,  0.0, -1.0,    tex_scale, 0.0,
        -0.5,  0.5, -0.5,    0.0,  0.0, -1.0,    tex_scale, tex_scale,
         0.5,  0.5, -0.5,    0.0,  0.0, -1.0,    0.0, tex_scale,
        
        # Top face
        -0.5,  0.5,  0.5,    0.0,  1.0,  0.0,    0.0, 0.0,
         0.5,  0.5,  0.5,    0.0,  1.0,  0.0,    tex_scale, 0.0,
         0.5,  0.5, -0.5,    0.0,  1.0,  0.0,    tex_scale, tex_scale,
        -0.5,  0.5, -0.5,    0.0,  1.0,  0.0,    0.0, tex_scale,
        
        # Bottom face
        -0.5, -0.5, -0.5,    0.0, -1.0,  0.0,    0.0, 0.0,
         0.5, -0.5, -0.5,    0.0, -1.0,  0.0,    tex_scale, 0.0,
         0.5, -0.5,  0.5,    0.0, -1.0,  0.0,    tex_scale, tex_scale,
        -0.5, -0.5,  0.5,    0.0, -1.0,  0.0,    0.0, tex_scale,
        
        # Right face
         0.5, -0.5,  0.5,    1.0,  0.0,  0.0,    0.0, 0.0,
         0.5, -0.5, -0.5,    1.0,  0.0,  0.0,    tex_scale, 0.0,
         0.5,  0.5, -0.5,    1.0,  0.0,  0.0,    tex_scale, tex_scale,
         0.5,  0.5,  0.5,    1.0,  0.0,  0.0,    0.0, tex_scale,
        
        # Left face
        -0.5, -0.5, -0.5,   -1.0,  0.0,  0.0,    0.0, 0.0,
        -0.5, -0.5,  0.5,   -1.0,  0.0,  0.0,    tex_scale, 0.0,
        -0.5,  0.5,  0.5,   -1.0,  0.0,  0.0,    tex_scale, tex_scale,
        -0.5,  0.5, -0.5,   -1.0,  0.0,  0.0,    0.0, tex_scale,
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

def create_plane_vertices(size=10.0, tex_scale=10.0):
    """Create a large plane for demonstrating perspective-correct texturing"""
    vertices = np.array([
        # positions                    # normals           # tex coords
        -size, 0.0, -size,    0.0,  1.0,  0.0,    0.0, 0.0,
         size, 0.0, -size,    0.0,  1.0,  0.0,    tex_scale, 0.0,
         size, 0.0,  size,    0.0,  1.0,  0.0,    tex_scale, tex_scale,
        -size, 0.0,  size,    0.0,  1.0,  0.0,    0.0, tex_scale,
    ], dtype=np.float32)
    
    indices = np.array([0, 1, 2, 2, 3, 0], dtype=np.uint32)
    
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
    
    stride = 8 * vertices.itemsize
    
    # Position
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)
    
    # Normal
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(3 * vertices.itemsize))
    glEnableVertexAttribArray(1)
    
    # Texture coords
    glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(6 * vertices.itemsize))
    glEnableVertexAttribArray(2)
    
    glBindVertexArray(0)
    
    return vao, len(indices)

def main():
    pygame.init()
    display = (1280, 720)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Lab6 - Texture Mapping with Mipmapping and Tiling")
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)
    
    # Enable depth testing
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    
    # Set up projection
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, (display[0] / display[1]), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    
    # Create shader program
    shader = create_shader_program()
    
    # Load multiple textures with different patterns
    textures = {
        'checkerboard': load_texture('checkerboard', use_mipmaps=True),
        'brick': load_texture('brick', use_mipmaps=True),
        'grid': load_texture('grid', use_mipmaps=True),
        'dots': load_texture('dots', use_mipmaps=True),
    }
    
    # Create geometry with different tiling amounts
    cube_vao1, cube_indices1 = setup_vertex_buffer(*create_cube_vertices(tex_scale=1.0))
    cube_vao2, cube_indices2 = setup_vertex_buffer(*create_cube_vertices(tex_scale=2.0))
    cube_vao3, cube_indices3 = setup_vertex_buffer(*create_cube_vertices(tex_scale=4.0))
    plane_vao, plane_indices = setup_vertex_buffer(*create_plane_vertices(size=10.0, tex_scale=10.0))
    
    # Create camera
    camera = Camera()
    
    # Objects with different textures and tiling
    objects = [
        {'vao': cube_vao1, 'indices': cube_indices1, 'pos': (-3.0, 1.0, 0.0), 
         'rotation': 0.0, 'texture': 'checkerboard', 'label': '1x tiling'},
        {'vao': cube_vao2, 'indices': cube_indices2, 'pos': (0.0, 1.0, 0.0), 
         'rotation': 0.0, 'texture': 'brick', 'label': '2x tiling'},
        {'vao': cube_vao3, 'indices': cube_indices3, 'pos': (3.0, 1.0, 0.0), 
         'rotation': 0.0, 'texture': 'grid', 'label': '4x tiling'},
        {'vao': plane_vao, 'indices': plane_indices, 'pos': (0.0, 0.0, 0.0), 
         'rotation': 0.0, 'texture': 'dots', 'label': 'Ground plane - 10x tiling'},
    ]
    
    clock = pygame.time.Clock()
    last_x, last_y = display[0] // 2, display[1] // 2
    first_mouse = True
    
    # Font for UI
    font = pygame.font.Font(None, 24)
    
    running = True
    show_info = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_h:
                    show_info = not show_info
        
        # Mouse input
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if first_mouse:
            last_x, last_y = mouse_x, mouse_y
            first_mouse = False
        
        xoffset = mouse_x - last_x
        yoffset = last_y - mouse_y
        last_x, last_y = mouse_x, mouse_y
        
        camera.process_mouse(xoffset, yoffset)
        
        # Keyboard input
        keys = pygame.key.get_pressed()
        camera.process_keyboard(keys)
        
        # Clear buffers
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0.2, 0.3, 0.4, 1.0)
        
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
        tex_loc = glGetUniformLocation(shader, "textureSampler")
        
        glUniformMatrix4fv(view_loc, 1, GL_FALSE, modelview)
        glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)
        glUniform1i(tex_loc, 0)
        
        # Draw objects
        for i, obj in enumerate(objects):
            glPushMatrix()
            
            glTranslatef(*obj['pos'])
            if i < 3:  # Rotate cubes only
                glRotatef(obj['rotation'], 0, 1, 0)
                obj['rotation'] += 0.5
            
            model = glGetFloatv(GL_MODELVIEW_MATRIX)
            glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
            
            # Bind texture
            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, textures[obj['texture']])
            
            # Draw
            glBindVertexArray(obj['vao'])
            glDrawElements(GL_TRIANGLES, obj['indices'], GL_UNSIGNED_INT, None)
            
            glPopMatrix()
        
        # Draw UI
        if show_info:
            glUseProgram(0)
            glMatrixMode(GL_PROJECTION)
            glPushMatrix()
            glLoadIdentity()
            glOrtho(0, display[0], display[1], 0, -1, 1)
            glMatrixMode(GL_MODELVIEW)
            glPushMatrix()
            glLoadIdentity()
            
            glDisable(GL_DEPTH_TEST)
            
            # Render text
            info_texts = [
                "Lab 6 - Texture Mapping Features:",
                "• Mipmapping: Enabled (trilinear filtering)",
                "• Tiling: Multiple scales demonstrated",
                "• Perspective-correct interpolation: Automatic in shaders",
                "",
                "Controls: W/A/S/D - Move, Mouse - Look, Space/Shift - Up/Down",
                "Press H to toggle this info, ESC to exit"
            ]
            
            y_offset = 10
            for text in info_texts:
                surface = font.render(text, True, (255, 255, 255))
                text_data = pygame.image.tostring(surface, "RGBA", True)
                glRasterPos2f(10, y_offset)
                glDrawPixels(surface.get_width(), surface.get_height(), 
                           GL_RGBA, GL_UNSIGNED_BYTE, text_data)
                y_offset += 25
            
            glEnable(GL_DEPTH_TEST)
            
            glMatrixMode(GL_PROJECTION)
            glPopMatrix()
            glMatrixMode(GL_MODELVIEW)
            glPopMatrix()
        
        pygame.display.flip()
        clock.tick(60)
    
    # Cleanup
    for texture in textures.values():
        glDeleteTextures(1, [texture])
    glDeleteProgram(shader)
    pygame.quit()

if __name__ == "__main__":
    main()