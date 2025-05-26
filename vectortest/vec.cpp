#include <glm/ext/vector_float3.hpp>
#include <glm/trigonometric.hpp>
#include <iostream>
#include <glm/glm.hpp>

int main() {
    float angle = glm::radians(45.0f);
    glm::vec2 target(glm::cos(angle), glm::sin(angle));

    return 0;
}

