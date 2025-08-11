# LM Studio Integration Setup Guide

Your resume application has been successfully configured to use your local LM Studio instance instead of OpenAI's API. Here's how to set it up and use it.

## Configuration Changes Made

✅ **Modified OpenAI client initialization** to point to your local LM Studio endpoint
✅ **Updated model configuration** to work with local models  
✅ **Created test scripts** to verify connectivity

## LM Studio Setup Requirements

### 1. Start LM Studio
- Open LM Studio application
- Load your preferred language model (recommended: 7B+ parameter model for good results)
- Go to the "Local Server" tab
- Click "Start Server" to begin hosting the model

### 2. Verify Server Settings
Make sure these settings match in LM Studio:
```
Host: 0.0.0.0 (to allow external connections)
Port: 1234
```

### 3. Test Connectivity
Run the connectivity test to verify everything is working:
```bash
# From the src directory
source venv/bin/activate
python3 test_http_client.py
```

## Environment Variables (Optional)

You can set these environment variables to customize the integration:

```bash
# Optional: Specify your model name (defaults to "local-model")
export LOCAL_MODEL_NAME="your-model-name"

# Optional: Keep for compatibility (not required for local models) 
export OPENAI_API_KEY="local-key"
```

## Updated Code Files

The following files have been modified to use your local AI:

### `app.py` (Lines 217-220)
```python
client = OpenAI(
    api_key="local-key",  # LM Studio doesn't require real API key
    base_url="http://172.28.144.1:1234/v1"  # LM Studio local endpoint
)
```

### Model Configuration (Lines 299-300)
```python
# LM Studio typically uses the loaded model name or "local-model"
model_name = os.getenv('LOCAL_MODEL_NAME', 'local-model')
```

## Testing Your Setup

### 1. Basic Connectivity Test
```bash
source venv/bin/activate
python3 test_http_client.py
```

### 2. OpenAI Client Test
```bash 
source venv/bin/activate
python3 test_local_ai.py
```

### 3. Full Application Test
Start your resume application and try the text-to-JSON parsing feature:
```bash
source venv/bin/activate
python3 app.py
```

## Troubleshooting

### Connection Errors
If you see connection errors:

1. **Verify LM Studio is running** and has a model loaded
2. **Check the Local Server is started** in LM Studio
3. **Confirm the IP address** - use `ipconfig` or `ip addr` to verify `172.28.144.1` is correct
4. **Test with localhost first** - try changing the endpoint to `http://127.0.0.1:1234/v1`

### Model Not Found Errors
If you get model-related errors:

1. **Check the model name** - run the connectivity test to see available models
2. **Set LOCAL_MODEL_NAME** environment variable to the exact model name from LM Studio

### Performance Considerations

- **Model Size**: Larger models (7B+) provide better results but require more resources
- **Temperature**: Set to 0.1 for consistent JSON formatting
- **Max Tokens**: Set to 4000+ for full resume parsing
- **Timeout**: The application uses 30-second timeouts for AI requests

## Expected Behavior

Once properly configured:

1. **Resume text parsing** will use your local model instead of OpenAI
2. **All other features** remain unchanged (HTML generation, ATS scoring, etc.)
3. **No internet connection** required for AI features
4. **Privacy**: All data stays on your local machine

## Next Steps

1. Start LM Studio and load a model
2. Start the local server in LM Studio
3. Run the connectivity tests
4. Start your resume application

The resume optimizer will now use your local AI model for converting text resumes to structured JSON format!