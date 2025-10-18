#version 330 core

layout(location = 0) in vec3 aPos;    // position (x,y,z)
layout(location = 1) in vec3 aColor;  // vertex color (r,g,b)

uniform mat4 uMVP; // model-view-projection

out vec3 vColor;

void main()
{
    vColor = aColor;
    gl_Position = uMVP * vec4(aPos, 1.0);
}
