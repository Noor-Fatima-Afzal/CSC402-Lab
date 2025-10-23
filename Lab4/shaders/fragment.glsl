#version 330 core
in vec2 fragTexCoord;
out vec4 outColor;

uniform sampler2D inputTexture;
uniform int filterType;
uniform float textureWidth;
uniform float textureHeight;
uniform int direction;

const float blur[5] = float[](0.06, 0.24, 0.4, 0.24, 0.06);
const float sharpen[5] = float[](0.0, -1.0, 3.0, -1.0, 0.0);
const float edge[5] = float[](-1.0, -1.0, 4.0, -1.0, -1.0);

vec4 applyConvolution1D(float kernel[5])
{
    vec4 result = vec4(0.0);
    vec2 offset;
    
    if (direction == 0) {
        offset = vec2(1.0 / textureWidth, 0.0);
    } else {
        offset = vec2(0.0, 1.0 / textureHeight);
    }
    
    result += texture(inputTexture, fragTexCoord - 2.0 * offset) * kernel[0];
    result += texture(inputTexture, fragTexCoord - 1.0 * offset) * kernel[1];
    result += texture(inputTexture, fragTexCoord) * kernel[2];
    result += texture(inputTexture, fragTexCoord + 1.0 * offset) * kernel[3];
    result += texture(inputTexture, fragTexCoord + 2.0 * offset) * kernel[4];
    
    return result;
}

void main()
{
    if (filterType == 0) {
        outColor = texture(inputTexture, fragTexCoord);
    }
    else if (filterType == 1) {
        outColor = applyConvolution1D(blur);
    }
    else if (filterType == 2) {
        outColor = applyConvolution1D(sharpen);
    }
    else if (filterType == 3) {
        vec4 edgeColor = applyConvolution1D(edge);
        outColor = vec4(vec3(length(edgeColor.rgb)), 1.0);
    }
    else {
        outColor = texture(inputTexture, fragTexCoord);
    }
    
    outColor = clamp(outColor, 0.0, 1.0);
}