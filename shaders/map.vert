#version 330 core

layout (location = 0) in vec3 in_position;
layout (location = 1) in vec3 in_normal;

out vec3 pos;
out vec3 norm;

void main() {
    pos = in_position;
    norm = in_normal;
    gl_Position = vec4(in_position, 1.0);
}