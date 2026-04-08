"""FastAPI server with WebSocket for realtime training updates."""

import asyncio
import json

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from backend.snake_game import SnakeGame
from backend.q_learning import QLearningAgent
from backend.trainer import Trainer

app = FastAPI(title="Snake AI Q-Learning")

# Global instances
game = SnakeGame()
agent = QLearningAgent()
trainer = Trainer(game, agent)


class TrainRequest(BaseModel):
    episodes: int = Field(default=1000, ge=1, le=50000)


@app.post("/api/train")
async def start_training(req: TrainRequest):
    """Start training in background."""
    if trainer.is_training():
        return {"status": "already_training"}

    async def run():
        await trainer.train(req.episodes)

    asyncio.create_task(run())
    return {"status": "started", "episodes": req.episodes}


@app.post("/api/stop")
async def stop_training():
    """Stop training."""
    trainer.stop()
    return {"status": "stopped"}


@app.get("/api/stats")
async def get_stats():
    """Get training history."""
    return {
        "stats": trainer.get_stats(),
        "is_training": trainer.is_training(),
        "total_episodes": len(trainer.stats),
    }


@app.get("/api/config")
async def get_config():
    """Get game and agent configuration."""
    return {
        "grid": {"width": game.width, "height": game.height},
        "agent": {
            "lr": agent.lr, "gamma": agent.gamma,
            "epsilon": agent.epsilon,
            "state_size": agent.state_size,
            "action_size": agent.action_size,
        },
    }


@app.websocket("/ws/train")
async def ws_train(ws: WebSocket):
    """Stream training stats every 10 episodes."""
    await ws.accept()

    if trainer.is_training():
        await ws.send_json({"type": "error", "data": "already_training"})
        await ws.close()
        return

    try:
        # Wait for start message with episode count
        data = await ws.receive_json()
        episodes = min(max(data.get("episodes", 1000), 1), 50000)

        async def callback(stats):
            try:
                await ws.send_json({"type": "train_update", "data": stats})
            except Exception:
                trainer.stop()

        result = await trainer.train(episodes, callback=callback)
        await ws.send_json({"type": "train_complete", "data": result})
    except WebSocketDisconnect:
        trainer.stop()


@app.websocket("/ws/play")
async def ws_play(ws: WebSocket):
    """Stream game frames for live replay."""
    await ws.accept()

    try:
        # Optional speed config from client
        speed_ms = 100
        try:
            data = await asyncio.wait_for(ws.receive_json(), timeout=1.0)
            speed_ms = max(10, min(data.get("speed_ms", 100), 1000))
        except (asyncio.TimeoutError, Exception):
            pass

        frames = trainer.play_episode()
        for frame in frames:
            await ws.send_json({"type": "play_frame", "data": frame})
            await asyncio.sleep(speed_ms / 1000)

        await ws.send_json({
            "type": "play_complete",
            "data": {"final_score": frames[-1]["score"] if frames else 0},
        })
    except WebSocketDisconnect:
        pass


# Serve frontend static files — mount LAST so API routes take priority
app.mount("/static", StaticFiles(directory="frontend"), name="static")


@app.get("/")
async def serve_index():
    return FileResponse("frontend/index.html")
