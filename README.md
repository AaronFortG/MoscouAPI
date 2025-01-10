# MoscouAPI

```bash
# Run the app
uvicorn main:app --reload

# Run the app on a directory
uvicorn app.main:app --reload

# Run on specific port
uvicorn app.main:app --reload --port 8080

# Run and bind it to an internet IP
uvicorn app.main:app --reload --host 192.168.1.140 --port 8080
```