import time
import os
import requests
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from tools import run_python_file

class BugWatcherHandler(FileSystemEventHandler):
    def on_modified(self, event):
        
        print(f"👀 System detected change in: {event.src_path}")
        
        # Check if the change is actually our buggy file
        if event.src_path.endswith("buggy_code.py"):
            print(f"🚀 MATCH! Processing bug in buggy_code.py...")
            
            success, output = run_python_file("buggy_code.py")
            if success:
                print("✨ Code is clean. No action needed.")
                return

            print("📡 Sending bug to FastAPI...")
            try:
                with open("buggy_code.py", "r") as f:
                    code_content = f.read()

                payload = {
                    "file_path": "buggy_code.py",
                    "code": code_content,
                    "error": output
                }
                
                response = requests.post("http://localhost:8000/trigger-fix", json=payload)
                print(f"✅ API Response: {response.status_code}")
            except Exception as e:
                print(f"❌ API Communication Error: {e}")

if __name__ == "__main__":
  
    current_dir = os.path.dirname(os.path.abspath(__file__))
    event_handler = BugWatcherHandler()
    observer = Observer()
    
    observer.schedule(event_handler, current_dir, recursive=False)
    
    print(f"🔥 ACTIVE: Watching for bugs in: {current_dir}")
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()