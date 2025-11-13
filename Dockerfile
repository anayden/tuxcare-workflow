FROM python:3.11-slim

LABEL maintainer="TuxCare <support@tuxcare.com>"
LABEL description="Automatically dismiss Dependabot security alerts based on TuxCare VEX data"

# Set working directory
WORKDIR /action

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/

# Copy entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Set Python to run in unbuffered mode (better for logs)
ENV PYTHONUNBUFFERED=1

# Add the action directory to Python path
ENV PYTHONPATH=/action

# Run the action via entrypoint script
ENTRYPOINT ["/entrypoint.sh"]

