import numpy as np

def look_at(eye, target, up):
    zaxis = (eye - target)
    zaxis /= np.linalg.norm(zaxis)
    xaxis = np.cross(up, zaxis)
    xaxis /= np.linalg.norm(xaxis)
    yaxis = np.cross(zaxis, xaxis)

    view = np.eye(4, dtype=np.float32)
    view[0, :3] = xaxis
    view[1, :3] = yaxis
    view[2, :3] = zaxis
    view[0, 3] = -np.dot(xaxis, eye)
    view[1, 3] = -np.dot(yaxis, eye)
    view[2, 3] = -np.dot(zaxis, eye)
    return view

def perspective(fov, aspect, near, far):
    f = 1.0 / np.tan(fov / 2)
    proj = np.zeros((4, 4), dtype=np.float32)
    proj[0, 0] = f / aspect
    proj[1, 1] = f
    proj[2, 2] = (far + near) / (near - far)
    proj[2, 3] = (2 * far * near) / (near - far)
    proj[3, 2] = -1
    return proj