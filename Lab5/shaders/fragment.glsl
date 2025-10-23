#version 330 core

in vec3 FragPos;
in vec3 Normal;
in vec3 Color;

out vec4 FragColor;

void main()
{
    // Simple directional lighting
    vec3 lightDir = normalize(vec3(0.5, 1.0, 0.3));
    vec3 norm = normalize(Normal);
    
    // Ambient
    float ambientStrength = 0.3;
    vec3 ambient = ambientStrength * Color;
    
    // Diffuse
    float diff = max(dot(norm, lightDir), 0.0);
    vec3 diffuse = diff * Color;
    
    // Combine
    vec3 result = ambient + diffuse;
    
    FragColor = vec4(result, 1.0);
}