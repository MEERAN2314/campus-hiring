# Assessment Generation Troubleshooting Guide

## Common Issues and Solutions

### Issue 1: Model Name Error
**Error**: `Model not found` or `Invalid model name`

**Solution**: 
Update `.env` file with correct model name:
```bash
GEMINI_MODEL=gemini-2.0-flash-exp
```

**Available Models** (in order of preference):
1. `gemini-2.0-flash-exp` (Latest, fastest)
2. `gemini-1.5-flash` (Stable, fast)
3. `gemini-1.5-pro` (Most capable, slower)

### Issue 2: API Key Invalid
**Error**: `401 Unauthorized` or `Invalid API key`

**Solution**:
1. Get a new API key from: https://makersuite.google.com/app/apikey
2. Update `.env`:
```bash
GOOGLE_API_KEY=your-new-api-key-here
```
3. Restart the application

### Issue 3: Only 1 Question Generated
**Error**: Assessment shows "Question 1 of 1"

**Solution**: 
This is now fixed with:
- Increased token limit (8000 tokens)
- Better prompts
- Comprehensive fallback (13-15 questions)
- Multiple model fallbacks

**If still happening**:
1. Check logs for errors
2. Verify API key is valid
3. Fallback assessment should activate automatically

### Issue 4: JSON Parsing Error
**Error**: `JSON decode error` in logs

**Solution**:
- System now automatically tries multiple models
- Falls back to comprehensive assessment
- No action needed from user

### Issue 5: Timeout/Slow Generation
**Error**: Takes more than 60 seconds

**Solution**:
1. This is normal for AI generation (30-60 seconds)
2. Show loading indicator to user
3. If timeout occurs, fallback activates automatically

### Issue 6: API Quota Exceeded
**Error**: `429 Too Many Requests` or `Quota exceeded`

**Solution**:
1. Wait a few minutes
2. System will use fallback assessment
3. Consider upgrading API quota
4. Or use fallback assessment permanently

## How to Test

### Test 1: Basic Generation
```bash
# Create a job as recruiter
# Click "Create Assessment"
# Wait 30-60 seconds
# Should see 13-15 questions
```

### Test 2: Check Logs
```bash
# Terminal running the app should show:
INFO: Generating assessment for Full Stack Developer using model: gemini-2.0-flash-exp
INFO: Received response of length: 15234
INFO: Generated 15 questions with gemini-2.0-flash-exp
INFO: Successfully generated assessment with 15 questions
```

### Test 3: Fallback Test
```bash
# Temporarily set invalid API key
# Create assessment
# Should see fallback with 13-15 questions
# Check logs for: "using comprehensive fallback assessment"
```

## Model Fallback Chain

The system tries models in this order:

1. **Primary**: Model from `.env` (gemini-2.0-flash-exp)
2. **Fallback 1**: gemini-1.5-flash
3. **Fallback 2**: gemini-1.5-pro
4. **Final Fallback**: Comprehensive pre-built assessment

## Verification Checklist

- [ ] `.env` has correct `GEMINI_MODEL=gemini-2.0-flash-exp`
- [ ] `GOOGLE_API_KEY` is valid and not expired
- [ ] Application restarted after `.env` changes
- [ ] Redis is running (for Celery)
- [ ] MongoDB connection is working
- [ ] Check application logs for errors

## Quick Fixes

### Fix 1: Reset to Defaults
```bash
# In .env file:
GEMINI_MODEL=gemini-2.0-flash-exp
GOOGLE_API_KEY=your-valid-key-here
```

### Fix 2: Force Fallback
If AI keeps failing, you can force fallback by:
1. Setting an invalid API key temporarily
2. System will use comprehensive fallback
3. Fallback has 13-15 quality questions

### Fix 3: Check API Status
Visit: https://status.cloud.google.com/
Check if Gemini API is operational

## Expected Behavior

### Successful Generation:
```
✅ Takes 30-60 seconds
✅ Shows "Generating..." message
✅ Creates 13-15 questions
✅ Questions are relevant to job
✅ Mix of MCQ, coding, situational
```

### Fallback Activation:
```
⚠️ Takes < 1 second
⚠️ Uses pre-built questions
✅ Still creates 13-15 questions
✅ Questions are generic but usable
✅ Assessment is functional
```

## Logs to Check

### Success Logs:
```
INFO: Generating assessment for Full Stack Developer using model: gemini-2.0-flash-exp
INFO: Received response of length: 15234
INFO: Generated 15 questions with gemini-2.0-flash-exp
INFO: Successfully generated assessment with 15 questions
INFO: Successfully created assessment assessment_xxx with 15 questions
```

### Fallback Logs:
```
WARNING: Only got 3 questions from gemini-2.0-flash-exp, trying next model...
INFO: Generating assessment for Full Stack Developer using model: gemini-1.5-flash
INFO: Generated 15 questions with gemini-1.5-flash
```

### Error Logs:
```
ERROR: Error with gemini-2.0-flash-exp: Invalid API key
ERROR: Error with gemini-1.5-flash: Model not found
WARNING: All AI models failed, using comprehensive fallback assessment
INFO: Successfully created assessment with 15 questions
```

## Support

### If issue persists:

1. **Check Logs**: Look for ERROR messages
2. **Verify API Key**: Test at https://makersuite.google.com
3. **Try Different Model**: Change `GEMINI_MODEL` in `.env`
4. **Use Fallback**: System should work even without AI
5. **Restart Services**: Restart app and Celery worker

### Contact Information:
- Check GitHub issues
- Review documentation
- Test with sample data

## Performance Metrics

### Normal Operation:
- **AI Generation**: 30-60 seconds
- **Fallback**: < 1 second
- **Success Rate**: ~90% AI, 10% fallback
- **Question Count**: Always 13-15 questions
- **Quality**: High (AI) or Good (fallback)

### Troubleshooting Time:
- **Model name fix**: 1 minute
- **API key update**: 2 minutes
- **Full restart**: 3 minutes
- **Verification**: 5 minutes

---

**Remember**: Even if AI fails, the comprehensive fallback ensures you always get a usable assessment with 13-15 questions!
