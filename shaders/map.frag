#version 330 core

in vec3 pos;
in vec3 norm;
in vec3 sun_dir_out;

out vec4 fragColor;


void main() {
    float height = pos.z;

    vec3 normal_vec = vec3(-norm.x, -norm.y, 1.0);
    vec3 sun_dir = normalize(sun_dir_out);
    float light = dot(normal_vec, sun_dir);
    vec3 color = vec3(0.0, 0.0, 0.0);
    // if (height < 0.5) {
    //     color = vec3(0.0, 0.5, 1.0);
    // } else {
    //     color = vec3(1.0, 1.0, smoothstep(0.5, 1.0, 0.0) - 0.5);
    // }
    // color = vec3(pos.z, pos.x, pos.y);
    color = vec3(0.7, 0.5, 0.2);
    color *= light;
    fragColor = vec4(color, 1.0);
}