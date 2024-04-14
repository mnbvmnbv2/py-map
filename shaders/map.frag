#version 330 core

in vec3 pos;

out vec4 fragColor;


void main() {
    float height = pos.z;
    if (height < 0.5) {
        fragColor = vec4(0.0, 0.0, 1.0, 1.0);
    } else {
        fragColor = vec4(0.0, 1.0, 0.0, 1.0);
    }
    //fragColor = vec4(pos.z, 0, 0, 1.0);
}