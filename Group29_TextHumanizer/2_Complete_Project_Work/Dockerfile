# Use stable Debian Bookworm Python 3.11 image
FROM python:3.11-slim-bookworm

# Environment settings
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    USE_MODEL=true \
    HF_MODEL=humarin/chatgpt_paraphraser_on_T5_base \
    JWT_SECRET=supersecret_text_humanizer_key_change_me_if_needed \
    GATEWAY_HOST=0.0.0.0 \
    PORT=5000

WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies (cached from previous step)
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose Gateway port
EXPOSE 5000

# Start all microservices together using python runner
# The AI service automatically downloads and caches the model on first launch/runtime in the background
CMD ["python", "run_all.py"]
