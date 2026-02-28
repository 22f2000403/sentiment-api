import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
import json

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class CommentRequest(BaseModel):
    comment: str

class SentimentResponse(BaseModel):
    sentiment: str
    rating: int

@app.get("/")
def root():
    return {"message": "Sentiment API ready!"}

@app.post("/comment")
async def analyze_comment(request: CommentRequest):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": f"""
Analyze the sentiment of this comment and respond ONLY in JSON:

{{
  "sentiment": "positive|negative|neutral",
  "rating": 1-5
}}

Comment: {request.comment}
"""
                }
            ],
            response_format={"type": "json_object"}
        )

        return json.loads(response.choices[0].message.content)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))