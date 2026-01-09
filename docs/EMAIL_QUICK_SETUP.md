# Email Setup - Quick Guide (5 Minutes)

## ✅ Yes, It's FREE!

Gmail SMTP is **completely free** for up to **500 emails per day**.

Perfect for HireWave!

---

## 🚀 Quick Setup (Gmail)

### Step 1: Enable 2-Factor Authentication (2 minutes)

1. Go to: https://myaccount.google.com/security
2. Click "2-Step Verification"
3. Follow the setup (use your phone)
4. ✅ Done!

### Step 2: Generate App Password (1 minute)

1. Go to: https://myaccount.google.com/apppasswords
2. Select app: **Mail**
3. Select device: **Other (Custom name)**
4. Type: **HireWave**
5. Click **Generate**
6. **Copy the 16-character password** (looks like: `abcd efgh ijkl mnop`)

### Step 3: Update .env File (1 minute)

```bash
# Open .env file
nano .env

# Add these lines (replace with your info):
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=abcdefghijklmnop  # Remove spaces!
SMTP_FROM_EMAIL=your-email@gmail.com
SMTP_FROM_NAME=HireWave

# Save and exit (Ctrl+X, then Y, then Enter)
```

**Important**: Remove spaces from the app password!
- ❌ Wrong: `abcd efgh ijkl mnop`
- ✅ Right: `abcdefghijklmnop`

### Step 4: Test Email (1 minute)

```bash
python3 test_email.py
```

Enter your email when prompted, then check your inbox!

---

## 📧 What Emails Will Be Sent?

### For Candidates:
1. ✅ **Application Confirmation** - When they apply
2. ✅ **Assessment Invitation** - When assessment is ready
3. ✅ **Results Notification** - When results are available
4. ✅ **Shortlist Notification** - If they're selected

### For Recruiters:
1. ✅ **New Application** - When someone applies
2. ✅ **Assessment Completed** - When candidate finishes

---

## 💰 Cost Breakdown

| Provider | Free Limit | Cost |
|----------|-----------|------|
| **Gmail** | 500/day | **FREE** ✅ |
| Outlook | 300/day | FREE |
| SendGrid | 100/day | FREE |
| Mailgun | 100/day | FREE |

**Recommendation**: Use Gmail (500/day is plenty!)

---

## 🧪 Testing

### Test 1: Configuration
```bash
python3 test_email.py
```

### Test 2: Real Flow
1. Apply to a job as candidate
2. Check candidate email ✅
3. Complete assessment
4. Check recruiter email ✅

---

## 🐛 Troubleshooting

### "Authentication failed"
**Fix**: 
1. Make sure 2FA is enabled
2. Generate new App Password
3. Remove spaces from password
4. Update .env file

### "Connection refused"
**Fix**:
1. Check SMTP_HOST=smtp.gmail.com
2. Check SMTP_PORT=587
3. Check internet connection

### Emails not received
**Fix**:
1. Check spam folder
2. Wait 1-2 minutes
3. Verify email address
4. Check logs for errors

---

## ✅ Checklist

- [ ] 2FA enabled on Gmail
- [ ] App Password generated
- [ ] .env file updated
- [ ] Spaces removed from password
- [ ] Test email sent successfully
- [ ] Test email received
- [ ] Application restarted

---

## 🎯 Quick Commands

```bash
# 1. Test email
python3 test_email.py

# 2. Restart app
./run.sh

# 3. Test real notification
# (Apply to a job and check email)
```

---

## 📱 Alternative: Outlook (Also FREE)

If you prefer Outlook:

```bash
SMTP_HOST=smtp-mail.outlook.com
SMTP_PORT=587
SMTP_USER=your-email@outlook.com
SMTP_PASSWORD=your-regular-password  # No app password needed
SMTP_FROM_EMAIL=your-email@outlook.com
SMTP_FROM_NAME=HireWave
```

---

## 💡 Pro Tips

1. **Use a dedicated email** for HireWave (not your personal)
2. **Check spam folder** initially
3. **Whitelist HireWave** in your email client
4. **Monitor usage** (Gmail shows in account settings)
5. **Keep credentials secure** (never commit .env to Git)

---

## 🚀 Ready?

1. Follow steps 1-4 above
2. Takes only 5 minutes
3. Completely FREE
4. Works perfectly!

**Need help?** Check `EMAIL_SETUP_GUIDE.md` for detailed instructions.

---

**That's it! Email notifications are now set up! 🎉**
