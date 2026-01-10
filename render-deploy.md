# Render Deployment Guide for HireWave

## Issue Fixed
- ✅ Fixed bcrypt version compatibility (pinned to 4.0.1)
- ✅ Added password truncation for bcrypt 72-byte limit
- ✅ Added email-validator dependency

## Quick Redeploy Steps

### Option 1: Automatic Redeploy (Recommended)
If you have auto-deploy enabled on Render:

1. **Commit and push changes:**
```bash
git add .
git commit -m "Fix bcrypt compatibility and password hashing"
git push origin main
```

2. Render will automatically detect the changes and redeploy.

### Option 2: Manual Redeploy

1. Go to your Render dashboard: https://dashboard.render.com
2. Select your HireWave service
3. Click "Manual Deploy" → "Deploy latest commit"

### Option 3: Clear Build Cache (If issues persist)

1. Go to Render dashboard
2. Select your service
3. Go to "Settings"
4. Click "Clear build cache & deploy"

## Verify Deployment

Once deployed, check:

1. **Service Status**: Should show "Live" in green
2. **Logs**: Check for any errors
   ```
   No bcrypt errors
   No password length errors
   ```

3. **Test Login**: Try logging in at https://hivewave.onrender.com

## Environment Variables to Check

Make sure these are set in Render:

```
MONGODB_URL=your_mongodb_connection_string
JWT_SECRET_KEY=your_secret_key
GEMINI_API_KEY=your_gemini_api_key
REDIS_URL=redis://red-xxxxx:6379
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
```

## Test Credentials

After deployment, you can test with these seeded accounts:

**Recruiter:**
- Email: recruiter@techcorp.com
- Password: recruiter123

**Candidate:**
- Email: john.doe@email.com
- Password: candidate123

## Troubleshooting

### If login still fails:

1. **Check logs in Render:**
   - Go to your service → Logs tab
   - Look for specific error messages

2. **Reseed database:**
   ```bash
   # SSH into Render shell (if available) or use MongoDB Compass
   # Run seed_data.py to recreate users with new password hashing
   ```

3. **Clear Redis cache:**
   - Restart the Redis service in Render
   - Or clear cache manually if you have access

### Common Issues:

**Issue**: "Module not found" errors
**Solution**: Make sure requirements.txt is updated and committed

**Issue**: Database connection errors
**Solution**: Check MONGODB_URL environment variable

**Issue**: Still getting bcrypt errors
**Solution**: Clear build cache and redeploy

## Production Checklist

- ✅ requirements.txt updated with bcrypt==4.0.1
- ✅ email-validator added
- ✅ Password hashing fixed with truncation
- ✅ Environment variables configured
- ✅ Database seeded with test data
- ✅ Redis configured
- ✅ SMTP configured for emails

## Support

If issues persist:
1. Check Render logs for specific errors
2. Verify all environment variables are set
3. Try clearing build cache
4. Ensure MongoDB is accessible from Render
