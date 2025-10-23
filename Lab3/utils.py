from OpenGL.GL import *
import numpy as np

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
