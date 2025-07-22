# Self-Hosted Video Starter Kit

A local, extensible video automation and transcription stack using Docker Compose. Includes OpenAI's Whisper speech-to-text model (via FastAPI), n8n for workflow automation, and Postgres for data storage.

---

## Features

- **No API keys required** – runs entirely on your machine.
- **Transcribe large files** – not limited by OpenAI's 25MB API restriction.
- **Simple HTTP API** – upload audio/video files and get JSON transcriptions.
- **Workflow automation** – use n8n to automate video/audio processing.
- **Persistent storage** – all data stored locally via Docker volumes.

---

## Services

- **n8n**: Low-code workflow automation tool (http://localhost:5678)
- **Whisper API**: FastAPI server for local Whisper transcription (http://localhost:9000)
- **Postgres**: Database for n8n
- **shared-data**: Host directory for sharing files between services and your machine

---

## Quick Start

### 1. Clone the repository

```sh
git clone <your-repo-url>
cd self-hosted-video-starter-kit
```

### 2. Create a `.env` file

Copy `.env.example` to `.env` and fill in the required secrets (Postgres user/password, n8n secrets, etc).

### 3. Start the stack

```sh
docker-compose up --build
```

- n8n will be available at [http://localhost:5678](http://localhost:5678)
- Whisper API will be available at [http://localhost:9000/transcribe](http://localhost:9000/transcribe)

---

## Usage

### Transcribe an audio or video file

Send a POST request with your file as form-data (field name: `file`) to the Whisper API:

#### Using `curl`:

```sh
curl -F "file=@your-audio-file.mp3" http://localhost:9000/transcribe
```

#### Using n8n

- Use the "HTTP Request" node
- Method: `POST`
- URL: `http://whisper:9000/transcribe` (inside n8n container) or `http://localhost:9000/transcribe` (from your host)
- Request Format: `Form-Data`
- Field Name: `file`
- Type: `File`
- Value: (reference to your binary file, e.g. `{{$binary.data}}`)

#### Response

You will receive a JSON object with the transcription:

```json
{
  "transcription": "...your transcribed text..."
}
```

---

## File Storage

- The `shared-data` directory on your host is mounted into all containers as `/shared`.
- Files uploaded via the API are saved to `/shared` (i.e., `shared-data` on your host).
- You can also manually place files in `shared-data` for use by other services.

---

## Requirements

- Docker & Docker Compose
- (No OpenAI API key required)
- Sufficient CPU and RAM for Whisper (large files/models require more resources)

---

## Notes

- This stack is for local or trusted use only. The API is not hardened for public internet exposure.
- The default Whisper model is `base`. You can change this in `whisper/app/main.py`.
- For GPU acceleration, see the commented section in `docker-compose.yml`.

---

## Community & Support

- **n8n Tutorials YouTube channel:** [Jay Peters - @jaypetersdotdev](https://www.youtube.com/@jaypetersdotdev)
- **FREE workflows and resources:** [Learn Automation & AI](https://www.skool.com/learn-automation-ai/about?ref=1c7ba6137dfc45878406f6f6fcf2c316)

---

## License

MIT (or your preferred license)

---

## Contributing

Pull requests and issues welcome!
