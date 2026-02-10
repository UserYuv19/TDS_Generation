from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import time
import json

app = FastAPI()

def generate_space_report():
    chunks = [
        "Space exploration has transformed humanity’s understanding of the universe, ",
        "driving scientific discovery, technological innovation, and global collaboration. ",
        "From early satellite launches to modern deep-space missions, exploration programs ",
        "have enabled precise data collection about planets, stars, and cosmic radiation. ",
        "These datasets help scientists analyze planetary atmospheres, orbital mechanics, ",
        "and the potential for life beyond Earth. ",
        "Advanced telescopes and probes now generate petabytes of structured data, ",
        "requiring sophisticated analytics pipelines and AI-driven interpretation. ",
        "Based on current findings, agencies recommend increased investment in reusable launch systems, ",
        "autonomous navigation, and long-duration life-support technologies. ",
        "Private-public partnerships are also advised to reduce costs and accelerate innovation. ",
        "In conclusion, sustained space exploration delivers scientific insight, economic value, ",
        "and strategic advantages while inspiring future generations of researchers and engineers."
    ]

    for chunk in chunks:
        payload = {
            "choices": [
                {"delta": {"content": chunk}}
            ]
        }
        yield f"data: {json.dumps(payload)}\n\n"
        time.sleep(0.25)

    yield "data: [DONE]\n\n"

@app.post("/")
async def stream_endpoint(request: Request):
    body = await request.json()
    if not body.get("stream", False):
        return {"error": "stream must be true"}

    return StreamingResponse(
        generate_space_report(),
        media_type="text/event-stream"
    )

@app.get("/")
def health():
    return {"status": "ok", "message": "Streaming API running"}
