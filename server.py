from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json, os, asyncio, aiohttp

# Server Configuration
PORT = 8080
DATA_FILE = "users.json"
TEMPLATE_FILE = "templates/askme.html"
OPENROUTER_API_KEY = "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"
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
AI_NAME = "SparkyAI-1"  # AI Model Name
STUDIO_NAME = "RC4 Studio"  # Branding Name

# Ensure users.json exists
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump([], f)

class MyHandler(SimpleHTTPRequestHandler):
    def set_headers(self, status=200, content_type="application/json"):
        """Set response headers"""
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.end_headers()

    def do_OPTIONS(self):
        self.set_headers(200)

    def do_GET(self):
        if self.path == "/":
            try:
                with open(TEMPLATE_FILE, "rb") as f:
                    self.set_headers(200, "text/html")
                    self.wfile.write(f.read())
            except FileNotFoundError:
                self.send_error(404, "File not found: askme.html")
        else:
            super().do_GET()

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        try:
            if content_length == 0:
                raise ValueError("Empty request body")
            post_data = json.loads(self.rfile.read(content_length).decode())
            print(f"Received POST request on: {self.path}")  # Debugging output

            if self.path == "/login":
                self.handle_login(post_data)
            elif self.path == "/register":
                self.handle_registration(post_data)
            elif self.path == "/chat":
                asyncio.run(self.handle_chat_request(post_data))
            else:
                self.send_error(404, f"Not Found: {self.path}")
        except json.JSONDecodeError:
            self.send_error(400, "Invalid JSON format")
        except ValueError as e:
            self.send_error(400, str(e))
        except Exception as e:
            self.send_error(500, f"Server Error: {str(e)}")

    def handle_login(self, data):
        """Handle user login using username and password"""
        username = data.get("username", "").strip()
        password = data.get("password", "").strip()
        
        print(f"Login attempt: username='{username}', password='{password}'")
        if not username or not password:
            self.send_error(400, "Missing username or password")
            return

        try:
            with open(DATA_FILE, "r") as f:
                users = json.load(f)
            print("Current users:", users)
        except Exception as e:
            self.send_error(500, f"Error reading users data: {str(e)}")
            return

        # Match exactly on username and password
        user = next((u for u in users if u.get("username") == username and u.get("password") == password), None)

        if user:
            self.set_headers()
            response = {
                "success": True,
                "message": "Login successful",
                "user": user
            }
            self.wfile.write(json.dumps(response).encode())
        else:
            # Sending error as JSON instead of HTML error page
            self.set_headers(401)
            self.wfile.write(json.dumps({
                "success": False,
                "message": "User not found or incorrect credentials"
            }).encode())

    def handle_registration(self, data):
        """Handle user registration using only username and password"""
        username = data.get("username", "").strip()
        password = data.get("password", "").strip()

        if not username or not password:
            self.send_error(400, "Missing registration details (username and password required)")
            return

        try:
            with open(DATA_FILE, "r") as f:
                users = json.load(f)
        except Exception as e:
            users = []

        if any(u.get("username") == username for u in users):
            self.set_headers(400)
            self.wfile.write(json.dumps({
                "success": False,
                "message": "User already exists"
            }).encode())
            return

        new_user = {"username": username, "password": password}
        users.append(new_user)

        try:
            with open(DATA_FILE, "w") as f:
                json.dump(users, f)
        except Exception as e:
            self.send_error(500, f"Error saving user: {str(e)}")
            return

        self.set_headers()
        self.wfile.write(json.dumps({
            "success": True,
            "message": "Registration successful",
            "user": new_user
        }).encode())

    async def handle_chat_request(self, data):
        """Handle chat request asynchronously"""
        user_message = data.get("message", "").strip().lower()
        if not user_message:
            self.send_error(400, "Missing message")
            return

        if "which model are you" in user_message or "what model are you based on" in user_message:
            response = f"I am based on {AI_NAME}, developed by {STUDIO_NAME}."
        elif "who built you" in user_message or "who trained you" in user_message or "who build you" in user_message:
            response = f"I was built and trained by {STUDIO_NAME}."
        else:
            response = await self.get_ai_response(user_message)

        self.set_headers()
        self.wfile.write(json.dumps({"response": response}).encode())

    async def get_ai_response(self, message):
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        system_prompt = f"You are {AI_NAME}, an AI assistant. Never mention any other AI model name or system. Always introduce yourself as {AI_NAME}."
        prefixed_message = f"I am {AI_NAME}. {message}"
        
        data = {
            "model": "google/gemini-2.0-flash-001",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prefixed_message}
            ]
        }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(OPENROUTER_API_URL, headers=headers, json=data) as response:
                    if response.status == 200:
                        result = await response.json()
                        ai_response = result.get("choices", [{}])[0].get("message", {}).get("content", "Error: No response")
                        return ai_response.replace("Gemini", AI_NAME).replace("Google AI", AI_NAME)
                    else:
                        return f"Error: {response.status} - {await response.text()}"
        except Exception as e:
            return f"Error: Failed to connect to OpenRouter ({str(e)})"

if __name__ == "__main__":
    print(f"🚀 Server running on http://localhost:{PORT}")
    server = ThreadingHTTPServer(("0.0.0.0", PORT), MyHandler)
    server.serve_forever()
