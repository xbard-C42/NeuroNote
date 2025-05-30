# run_app.py
# Convenience script to launch both the FastAPI backend and the Streamlit front-end
import subprocess
import sys
import signal

def main():
    # Start FastAPI (uvicorn)
    backend_cmd = [sys.executable, '-m', 'uvicorn', 'api:app', '--reload']
    print(f"Starting backend: {' '.join(backend_cmd)}")
    backend_proc = subprocess.Popen(
        backend_cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    # Start Streamlit front-end
    frontend_cmd = [sys.executable, '-m', 'streamlit', 'run', 'app.py']
    print(f"Starting frontend: {' '.join(frontend_cmd)}")
    frontend_proc = subprocess.Popen(
        frontend_cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    procs = [backend_proc, frontend_proc]

    def shutdown(signum, frame):
        print("\nShutting down processes...")
        for p in procs:
            p.terminate()
        sys.exit(0)

    # Handle CTRL+C gracefully
    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    # Relay logs from both processes
    try:
        while True:
            for p in procs:
                if p.stdout:
                    line = p.stdout.readline()
                    if line:
                        prefix = "[BACKEND] " if p is backend_proc else "[FRONTEND]"
                        print(f"{prefix} {line.strip()}")
            # If any process has exited, break
            if any(p.poll() is not None for p in procs):
                print("One of the processes exited. Shutting down...")
                break
    finally:
        shutdown(None, None)

if __name__ == '__main__':
    main()
