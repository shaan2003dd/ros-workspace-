from setuptools import setup

package_name = 'stm32_bridge'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    py_modules=[],
    install_requires=['setuptools'],
    zip_safe=True,
    author='administrator',
    author_email='administrator@todo.todo',
    description='STM32 bridge package',
    license='MIT',
    entry_points={
        'console_scripts': [
            'uart_node = stm32_bridge.uart:main',
        ],
    },
)

