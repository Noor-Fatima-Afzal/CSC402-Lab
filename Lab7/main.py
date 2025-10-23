import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import math

class Camera:
    def __init__(self):
        self.position = np.array([0.0, 2.0, 5.0])
        self.yaw = -90.0
        self.pitch = 0.0
        self.front = np.array([0.0, 0.0, -1.0])
        self.up = np.array([0.0, 1.0, 0.0])
        self.right = np.array([1.0, 0.0, 0.0])
        self.world_up = np.array([0.0, 1.0, 0.0])
        self.movement_speed = 2.5
        self.mouse_sensitivity = 0.1
        self.update_camera_vectors()
    
    def update_camera_vectors(self):
        front = np.array([
            math.cos(math.radians(self.yaw)) * math.cos(math.radians(self.pitch)),
            math.sin(math.radians(self.pitch)),
            math.sin(math.radians(self.yaw)) * math.cos(math.radians(self.pitch))
        ])
        self.front = front / np.linalg.norm(front)
        self.right = np.cross(self.front, self.world_up)
        self.right = self.right / np.linalg.norm(self.right)
        self.up = np.cross(self.right, self.front)
        self.up = self.up / np.linalg.norm(self.up)
    
    def process_mouse_movement(self, xoffset, yoffset):
        xoffset *= self.mouse_sensitivity
        yoffset *= self.mouse_sensitivity
        self.yaw += xoffset
        self.pitch += yoffset
        self.pitch = max(-89.0, min(89.0, self.pitch))
        self.update_camera_vectors()
    
    def process_keyboard(self, keys, delta_time):
        velocity = self.movement_speed * delta_time
        if keys[K_w]:
            self.position += self.front * velocity
        if keys[K_s]:
            self.position -= self.front * velocity
        if keys[K_a]:
            self.position -= self.right * velocity
        if keys[K_d]:
            self.position += self.right * velocity
        if keys[K_SPACE]:
            self.position += self.up * velocity
        if keys[K_LSHIFT]:
            self.position -= self.up * velocity
    
    def get_view_matrix(self):
        return self.look_at(self.position, self.position + self.front, self.up)
    
    @staticmethod
    def look_at(position, target, up):
        z = position - target
        z = z / np.linalg.norm(z)
        x = np.cross(up, z)
        x = x / np.linalg.norm(x)
        y = np.cross(z, x)
        
        view = np.identity(4)
        view[0, :3] = x
        view[1, :3] = y
        view[2, :3] = z
        view[0, 3] = -np.dot(x, position)
        view[1, 3] = -np.dot(y, position)
        view[2, 3] = -np.dot(z, position)
        return view

class ModelLoader:
    @staticmethod
    def load_obj(filename):
        vertices = []
        normals = []
        faces = []
        
        temp_vertices = []
        temp_normals = []
        
        try:
            with open(filename, 'r') as f:
                for line in f:
                    if line.startswith('v '):
                        parts = line.split()
                        temp_vertices.append([float(parts[1]), float(parts[2]), float(parts[3])])
                    elif line.startswith('vn '):
                        parts = line.split()
                        temp_normals.append([float(parts[1]), float(parts[2]), float(parts[3])])
                    elif line.startswith('f '):
                        parts = line.split()[1:]
                        face = []
                        for part in parts:
                            indices = part.split('/')
                            v_idx = int(indices[0]) - 1
                            n_idx = int(indices[2]) - 1 if len(indices) > 2 and indices[2] else v_idx
                            face.append((v_idx, n_idx))
                        faces.append(face)
            
            # Build vertex data with normals
            for face in faces:
                for v_idx, n_idx in face:
                    vertices.extend(temp_vertices[v_idx])
                    if n_idx < len(temp_normals):
                        normals.extend(temp_normals[n_idx])
                    else:
                        normals.extend([0.0, 1.0, 0.0])
            
            return np.array(vertices, dtype=np.float32), np.array(normals, dtype=np.float32)
        
        except FileNotFoundError:
            print(f"Model file {filename} not found. Creating default cube.")
            return ModelLoader.create_cube()
    
    @staticmethod
    def create_cube():
        vertices = np.array([
            # Front face
            -1, -1,  1,  -1,  1,  1,   1,  1,  1,
            -1, -1,  1,   1,  1,  1,   1, -1,  1,
            # Back face
            -1, -1, -1,   1,  1, -1,  -1,  1, -1,
            -1, -1, -1,   1, -1, -1,   1,  1, -1,
            # Top face
            -1,  1, -1,  -1,  1,  1,   1,  1,  1,
            -1,  1, -1,   1,  1,  1,   1,  1, -1,
            # Bottom face
            -1, -1, -1,   1, -1,  1,  -1, -1,  1,
            -1, -1, -1,   1, -1, -1,   1, -1,  1,
            # Right face
             1, -1, -1,   1,  1, -1,   1,  1,  1,
             1, -1, -1,   1,  1,  1,   1, -1,  1,
            # Left face
            -1, -1, -1,  -1,  1,  1,  -1,  1, -1,
            -1, -1, -1,  -1, -1,  1,  -1,  1,  1,
        ], dtype=np.float32)
        
        normals = np.array([
            # Front
            0, 0, 1,  0, 0, 1,  0, 0, 1,  0, 0, 1,  0, 0, 1,  0, 0, 1,
            # Back
            0, 0, -1,  0, 0, -1,  0, 0, -1,  0, 0, -1,  0, 0, -1,  0, 0, -1,
            # Top
            0, 1, 0,  0, 1, 0,  0, 1, 0,  0, 1, 0,  0, 1, 0,  0, 1, 0,
            # Bottom
            0, -1, 0,  0, -1, 0,  0, -1, 0,  0, -1, 0,  0, -1, 0,  0, -1, 0,
            # Right
            1, 0, 0,  1, 0, 0,  1, 0, 0,  1, 0, 0,  1, 0, 0,  1, 0, 0,
            # Left
            -1, 0, 0,  -1, 0, 0,  -1, 0, 0,  -1, 0, 0,  -1, 0, 0,  -1, 0, 0,
        ], dtype=np.float32)
        
        return vertices, normals

def load_shader(shader_file, shader_type):
    with open(shader_file, 'r') as f:
        shader_source = f.read()
    
    shader = glCreateShader(shader_type)
    glShaderSource(shader, shader_source)
    glCompileShader(shader)
    
    if not glGetShaderiv(shader, GL_COMPILE_STATUS):
        error = glGetShaderInfoLog(shader).decode()
        print(f"Shader compilation error: {error}")
        raise RuntimeError(f"Shader compilation failed: {error}")
    
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
        raise RuntimeError(f"Program linking failed: {error}")
    
    glDeleteShader(vertex_shader)
    glDeleteShader(fragment_shader)
    
    return program

def setup_model(vertices, normals):
    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)
    
    vbo_vertices = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo_vertices)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(0)
    
    vbo_normals = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo_normals)
    glBufferData(GL_ARRAY_BUFFER, normals.nbytes, normals, GL_STATIC_DRAW)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(1)
    
    glBindVertexArray(0)
    
    return vao, len(vertices) // 3

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("3D Model with Phong Lighting")
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)
    
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)
    glEnable(GL_CULL_FACE)
    glCullFace(GL_BACK)
    
    # Create shader program
    shader_program = create_shader_program()
    
    # Load model (tries to load model.obj, falls back to cube)
    vertices, normals = ModelLoader.load_obj('model.obj')
    vao, vertex_count = setup_model(vertices, normals)
    
    # Setup camera
    camera = Camera()
    
    # Setup projection matrix
    projection = perspective(45.0, display[0] / display[1], 0.1, 100.0)
    
    # Lighting properties
    light_pos = np.array([5.0, 5.0, 5.0], dtype=np.float32)
    light_color = np.array([1.0, 1.0, 1.0], dtype=np.float32)
    
    # Material properties
    ambient_strength = 0.2
    specular_strength = 0.5
    shininess = 32.0
    object_color = np.array([0.8, 0.3, 0.3], dtype=np.float32)
    
    clock = pygame.time.Clock()
    last_x, last_y = display[0] / 2, display[1] / 2
    first_mouse = True
    rotation_angle = 0.0
    
    running = True
    while running:
        delta_time = clock.tick(60) / 1000.0
        
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            elif event.type == MOUSEMOTION:
                x, y = event.pos
                if first_mouse:
                    last_x, last_y = x, y
                    first_mouse = False
                
                xoffset = x - last_x
                yoffset = last_y - y
                last_x, last_y = x, y
                
                camera.process_mouse_movement(xoffset, yoffset)
        
        keys = pygame.key.get_pressed()
        camera.process_keyboard(keys, delta_time)
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0.1, 0.1, 0.15, 1.0)
        
        glUseProgram(shader_program)
        
        # Update rotation
        rotation_angle += 20.0 * delta_time
        
        # Model matrix (rotation)
        model = np.identity(4, dtype=np.float32)
        model = rotate(model, rotation_angle, np.array([0.0, 1.0, 0.0]))
        
        # View matrix
        view = camera.get_view_matrix().astype(np.float32)
        
        # Set uniforms
        model_loc = glGetUniformLocation(shader_program, "model")
        view_loc = glGetUniformLocation(shader_program, "view")
        proj_loc = glGetUniformLocation(shader_program, "projection")
        
        glUniformMatrix4fv(model_loc, 1, GL_TRUE, model)
        glUniformMatrix4fv(view_loc, 1, GL_TRUE, view)
        glUniformMatrix4fv(proj_loc, 1, GL_TRUE, projection)
        
        # Lighting uniforms
        glUniform3fv(glGetUniformLocation(shader_program, "lightPos"), 1, light_pos)
        glUniform3fv(glGetUniformLocation(shader_program, "viewPos"), 1, camera.position.astype(np.float32))
        glUniform3fv(glGetUniformLocation(shader_program, "lightColor"), 1, light_color)
        glUniform3fv(glGetUniformLocation(shader_program, "objectColor"), 1, object_color)
        glUniform1f(glGetUniformLocation(shader_program, "ambientStrength"), ambient_strength)
        glUniform1f(glGetUniformLocation(shader_program, "specularStrength"), specular_strength)
        glUniform1f(glGetUniformLocation(shader_program, "shininess"), shininess)
        
        # Draw model
        glBindVertexArray(vao)
        glDrawArrays(GL_TRIANGLES, 0, vertex_count)
        glBindVertexArray(0)
        
        pygame.display.flip()
    
    pygame.quit()

def perspective(fov, aspect, near, far):
    f = 1.0 / math.tan(math.radians(fov) / 2.0)
    nf = 1.0 / (near - far)
    
    return np.array([
        [f / aspect, 0, 0, 0],
        [0, f, 0, 0],
        [0, 0, (far + near) * nf, 2 * far * near * nf],
        [0, 0, -1, 0]
    ], dtype=np.float32)

def rotate(matrix, angle, axis):
    c = math.cos(math.radians(angle))
    s = math.sin(math.radians(angle))
    axis = axis / np.linalg.norm(axis)
    x, y, z = axis
    
    rotation = np.array([
        [c + x*x*(1-c), x*y*(1-c) - z*s, x*z*(1-c) + y*s, 0],
        [y*x*(1-c) + z*s, c + y*y*(1-c), y*z*(1-c) - x*s, 0],
        [z*x*(1-c) - y*s, z*y*(1-c) + x*s, c + z*z*(1-c), 0],
        [0, 0, 0, 1]
    ], dtype=np.float32)
    
    return np.dot(matrix, rotation)

if __name__ == "__main__":
    main()