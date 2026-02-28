from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
from typing import Literal

app = FastAPI()
client = OpenAI(api_key="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")  # ← API KEY DALO!

class CommentRequest(BaseModel):
    comment: str

class SentimentResponse(BaseModel):
    sentiment: Literal["positive", "negative", "neutral"]
    rating: int

@app.post("/comment", response_model=SentimentResponse)
async def analyze_comment(request: CommentRequest):
    try:
        response_schema = {
            "type": "object",
            "properties": {
                "sentiment": {"type": "string", "enum": ["positive", "negative", "neutral"]},
                "rating": {"type": "integer", "minimum": 1, "maximum": 5}
            },
            "required": ["sentiment", "rating"],
            "additionalProperties": False
        }
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": f"Analyze this comment: {request.comment}"}],
            response_format={"type": "json_schema", "json_schema": response_schema}
        )
        
        return SentimentResponse(**response.choices[0].message.content)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI analysis failed: {str(e)}")
