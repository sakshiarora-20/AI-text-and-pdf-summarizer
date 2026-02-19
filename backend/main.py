from fastapi import FastAPI, UploadFile, File, HTTPException
from transformers import pipeline
from utils import clean_text, read_pdf

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


summarizer = pipeline(
    task="summarization",
    model="sshleifer/distilbart-cnn-12-6"  
)

@app.post("/summarize")
async def summarize(file: UploadFile = File(...)):
    try:
        
        if file.filename.endswith(".txt"):
            raw_text = (await file.read()).decode("utf-8")
        elif file.filename.endswith(".pdf"):
            raw_text = read_pdf(file.file)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")

        if not raw_text or len(raw_text.strip()) == 0:
            raise HTTPException(status_code=400, detail="File is empty or unreadable")

        
        cleaned_text = clean_text(raw_text)

        
        cleaned_text = cleaned_text[:1500]

        summary = summarizer(
            cleaned_text,
            max_length=130,
            min_length=40,
            do_sample=False
        )[0]["summary_text"]

        return {
            "word_count": len(cleaned_text.split()),
            "summary": summary
        }

    except Exception as e:
        print("ERROR:", str(e))  
        raise HTTPException(status_code=500, detail=str(e))
