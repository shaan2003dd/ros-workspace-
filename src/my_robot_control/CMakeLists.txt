cmake_minimum_required(VERSION 3.5)
project(my_robot_control)

find_package(ament_cmake REQUIRED)

# Uncomment the following section if you have dependencies
# find_package(<dependency> REQUIRED)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  set(ament_cmake_copyright_FOUND TRUE)
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

# -----------------------------
# Install launch files
# -----------------------------
install(DIRECTORY launch
  DESTINATION share/${PROJECT_NAME}/
)

ament_package()
