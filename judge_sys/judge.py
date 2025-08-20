import subprocess
import os

def compile_and_run_java():
    subprocess.run(["javac", "Main.java"], check=True)
    result = subprocess.run(["java", "Main"], input="1\n2\n3\n4\n", text=True, capture_output=True)
    print("Java Output:")
    print(result.stdout)

def compile_and_run_cpp():
    subprocess.run(["g++", "-o", "main", "main.cpp"], check=True)
    result = subprocess.run(["./main"], input="1\n2\n3\n4\n", text=True, capture_output=True)
    print("C++ Output:")
    print(result.stdout)

def run_python():
    result = subprocess.run(["python3", "main.py"], input="1\n2\n3\n4\n", text=True, capture_output=True)
    print("Python Output:")
    print(result.stdout)

if __name__ == "__main__":
    os.chdir("/judge/test_cases")
    compile_and_run_java()
    compile_and_run_cpp()
    run_python()

