# shader.py
from OpenGL.GL import *
import ctypes

def compile_shader(source, shader_type):
    shader = glCreateShader(shader_type)
    glShaderSource(shader, source)
    glCompileShader(shader)
    # check compile status
    status = glGetShaderiv(shader, GL_COMPILE_STATUS)
    if not status:
        log = glGetShaderInfoLog(shader).decode()
        shader_type_str = {GL_VERTEX_SHADER: "VERTEX", GL_FRAGMENT_SHADER: "FRAGMENT"}.get(shader_type, "UNKNOWN")
        raise RuntimeError(f"{shader_type_str} shader compile error:\n{log}")
    return shader

def create_program_from_files(vertex_path, fragment_path):
    with open(vertex_path, 'r') as f:
        vsrc = f.read()
    with open(fragment_path, 'r') as f:
        fsrc = f.read()

    vert = compile_shader(vsrc, GL_VERTEX_SHADER)
    frag = compile_shader(fsrc, GL_FRAGMENT_SHADER)

    prog = glCreateProgram()
    glAttachShader(prog, vert)
    glAttachShader(prog, frag)
    glLinkProgram(prog)

    # check link status
    linked = glGetProgramiv(prog, GL_LINK_STATUS)
    if not linked:
        log = glGetProgramInfoLog(prog).decode()
        raise RuntimeError("Shader program link error:\n" + log)

    # shaders can be deleted after linking
    glDeleteShader(vert)
    glDeleteShader(frag)
    return prog
