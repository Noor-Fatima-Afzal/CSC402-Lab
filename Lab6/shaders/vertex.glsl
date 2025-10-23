#version 330 core

layout (location = 0) in vec3 aPos;
layout (location = 1) in vec3 aNormal;
layout (location = 2) in vec2 aTexCoord;

out vec3 FragPos;
out vec3 Normal;
out vec2 TexCoord;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

void main()
{
    // Transform position to world space
    FragPos = vec3(model * vec4(aPos, 1.0));
    
    // Transform normal to world space
    Normal = mat3(transpose(inverse(model))) * aNormal;
    
    // Pass texture coordinates to fragment shader
    // Perspective-correct interpolation is automatic in modern OpenGL
    // The GPU automatically divides by w (perspective divide) for varying variables
    TexCoord = aTexCoord;
    
    // Calculate final position with perspective divide
    gl_Position = projection * view * model * vec4(aPos, 1.0);
}