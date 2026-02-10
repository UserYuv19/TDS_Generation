from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import asyncio
import json
import time

app = FastAPI()

# ---------------------------
# CORS
# ---------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------
# Root endpoint
# ---------------------------
@app.get("/")
async def root():
    return {
        "status": "ok",
        "service": "Streaming LLM API"
    }

# ---------------------------
# Streaming endpoint
# ---------------------------
@app.post("/")
async def stream_endpoint(request: Request):
    try:
        body = await request.json()
    except Exception:
        body = {}

    prompt = body.get("prompt", "space exploration")

    async def event_generator():
        try:
            chunks = [
                "Space exploration has fundamentally transformed humanity’s understanding of the universe, ",
                "enabling scientists to study distant planets, stars, and galaxies that were once beyond reach. ",
                "Modern missions rely heavily on data analysis, as spacecraft and satellites collect massive volumes ",
                "of telemetry, imagery, and sensor readings that must be processed and interpreted on Earth. ",
                "These datasets help researchers understand planetary atmospheres, gravitational forces, and ",
                "the potential for life beyond our planet, while also improving climate models and weather prediction. ",
                "In addition to scientific discovery, space exploration drives technological innovation across industries. ",
                "Advances in materials science, robotics, artificial intelligence, and communications have emerged ",
                "directly from space programs and later benefited healthcare, transportation, and consumer electronics. ",
                "From an economic perspective, investment in space creates high-skilled jobs and stimulates private-sector growth. ",
                "Looking forward, experts recommend continued collaboration between governments and commercial partners, ",
                "as well as sustained funding for long-term missions to the Moon, Mars, and beyond. ",
                "Such efforts will expand scientific knowledge, strengthen global cooperation, and inspire future generations ",
                "to pursue careers in science, engineering, and data-driven exploration."
            ]

            for chunk in chunks:
                yield f"data: {json.dumps({'choices': [{'delta': {'content': chunk}}]})}\n\n"
                await asyncio.sleep(0.25)

            yield "data: [DONE]\n\n"

        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )
