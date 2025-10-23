#version 330 core

in vec3 FragPos;
in vec3 Normal;
in vec2 TexCoord;

out vec4 FragColor;

uniform sampler2D textureSampler;

void main()
{
    // Sample texture with mipmapping
    // The GPU automatically selects the appropriate mipmap level
    // based on the screen-space derivative of texture coordinates
    vec4 texColor = texture(textureSampler, TexCoord);
    
    // Simple directional lighting
    vec3 lightDir = normalize(vec3(0.5, 1.0, 0.3));
    vec3 norm = normalize(Normal);
    
    // Ambient component
    float ambientStrength = 0.4;
    vec3 ambient = ambientStrength * texColor.rgb;
    
    // Diffuse component
    float diff = max(dot(norm, lightDir), 0.0);
    vec3 diffuse = diff * texColor.rgb;
    
    // Combine lighting with texture
    vec3 result = ambient + diffuse;
    
    FragColor = vec4(result, texColor.a);
}