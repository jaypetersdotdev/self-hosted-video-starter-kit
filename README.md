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
curl -F "file=@your-audio-file.mp3" \
  "http://localhost:9000/transcribe?returnTimestamps=true&transcriptType=word"
```

- `transcriptType`: `segment` (default) or `word` for word-level timestamps (if supported by your Whisper version)
- `returnTimestamps`: `true` to include timestamps in the response

#### Using n8n

- Use the "HTTP Request" node
- Method: `POST`
- URL: `http://whisper:9000/transcribe?returnTimestamps=true&transcriptType=word` (inside n8n container) or `http://localhost:9000/transcribe?...` (from your host)
- Body Content Type: `Form-Data`
- Add only the `file` parameter as form-data

#### Response

You will receive a JSON object with the transcription and, if requested, timestamps:

```json
{
  "transcription": "...your transcribed text...",
  "timestamps": [
    { "word": "Hello", "start": 0.0, "end": 0.5 },
    { "word": "world", "start": 0.5, "end": 1.0 }
  ]
}
```

---

### Run custom ffmpeg commands

You can run any custom ffmpeg command inside the container using the `/ffmpeg` endpoint. This is useful for advanced video/audio processing, filtering, or conversion.

**Security Warning:** Only commands starting with `ffmpeg` are allowed. The command is executed inside the container. Use with caution.

#### Example request

POST to `http://localhost:9000/ffmpeg` with a JSON body:

```json
{
  "command": "ffmpeg -i /shared/input.mp4 -vf scale=320:240 /shared/output.mp4"
}
```

- `/shared` refers to the `shared-data` directory on your host, mounted in the container.
- You can use any valid ffmpeg command, including complex filters.

#### Example response

```json
{
  "stdout": "...ffmpeg standard output...",
  "stderr": "...ffmpeg error/output log...",
  "returncode": 0
}
```

If the command does not start with `ffmpeg`, you will receive an error.

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
