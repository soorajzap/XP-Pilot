import docker

client = docker.from_env()
CONTAINER_NAME = "agent_sandbox"

def run_python_file(file_path):
    try:
        container = client.containers.get(CONTAINER_NAME)
        
        with open(file_path, 'r') as f:
            local_code = f.read()

  
        container.exec_run("touch /app/test_script.py")


        command = [
            "sh", "-c",
            f"cat << 'EOF' > /app/test_script.py\n{local_code}\nEOF"
        ]
        container.exec_run(command)

        result = container.exec_run("python /app/test_script.py")
        
        output = result.output.decode('utf-8')
        
        if result.exit_code == 0:
            return True, "Execution Passed"
        else:
            return False, output
            
    except Exception as e:
        return False, f"Docker Error: {str(e)}"