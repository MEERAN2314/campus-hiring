# Email Notification Setup Guide

## Overview
Set up free email notifications for HireWave using Gmail SMTP.

## ✅ Free Options

### 1. Gmail (Recommended)
- **Cost**: FREE
- **Limit**: 500 emails/day
- **Setup**: 5 minutes
- **Reliability**: Excellent

### 2. Outlook/Hotmail
- **Cost**: FREE
- **Limit**: 300 emails/day
- **Setup**: 5 minutes
- **Reliability**: Good

### 3. SendGrid
- **Cost**: FREE tier available
- **Limit**: 100 emails/day
- **Setup**: 10 minutes (requires signup)
- **Reliability**: Excellent

### 4. Mailgun
- **Cost**: FREE tier available
- **Limit**: 100 emails/day
- **Setup**: 10 minutes (requires signup)
- **Reliability**: Excellent

---

## 🚀 Quick Setup: Gmail SMTP (FREE)

### Step 1: Enable 2-Factor Authentication

1. Go to: https://myaccount.google.com/security
2. Click "2-Step Verification"
3. Follow the setup process
4. Enable 2FA (required for App Passwords)

### Step 2: Generate App Password

1. Go to: https://myaccount.google.com/apppasswords
2. Select "Mail" as the app
3. Select "Other" as the device
4. Name it: "HireWave"
5. Click "Generate"
6. **Copy the 16-character password** (e.g., `abcd efgh ijkl mnop`)

### Step 3: Update .env File

```bash
# Email Configuration
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=abcd efgh ijkl mnop  # Your app password (remove spaces)
SMTP_FROM_EMAIL=your-email@gmail.com
SMTP_FROM_NAME=HireWave
```

**Important**: Remove spaces from the app password!
- ❌ Wrong: `abcd efgh ijkl mnop`
- ✅ Right: `abcdefghijklmnop`

---

## 📝 Alternative: Outlook/Hotmail (FREE)

### Configuration:
```bash
SMTP_HOST=smtp-mail.outlook.com
SMTP_PORT=587
SMTP_USER=your-email@outlook.com
SMTP_PASSWORD=your-password
SMTP_FROM_EMAIL=your-email@outlook.com
SMTP_FROM_NAME=HireWave
```

**Note**: Use your regular Outlook password (no app password needed)

---

## 🔧 Email Notifications in HireWave

### When Emails Are Sent:

1. **Candidate Applied**
   - To: Recruiter
   - Subject: "New Application for [Job Title]"
   - Content: Candidate details

2. **Assessment Created**
   - To: Recruiter
   - Subject: "Assessment Created for [Job Title]"
   - Content: Assessment details

3. **Assessment Completed**
   - To: Candidate
   - Subject: "Assessment Submitted Successfully"
   - Content: Next steps

4. **Results Available**
   - To: Candidate
   - Subject: "Your Assessment Results"
   - Content: Score and feedback link

5. **Shortlisted**
   - To: Candidate
   - Subject: "Congratulations! You've been shortlisted"
   - Content: Next steps

6. **Rejected**
   - To: Candidate
   - Subject: "Application Update"
   - Content: Feedback and encouragement

---

## 🧪 Testing Email Setup

### Test 1: Send Test Email
```bash
python3 test_email.py
```

### Test 2: Check Logs
```bash
# Should see:
INFO: Email sent successfully to test@example.com
```

### Test 3: Real Flow
1. Apply to a job as candidate
2. Check recruiter email
3. Complete assessment
4. Check candidate email

---

## 🔒 Security Best Practices

### ✅ DO:
- Use App Passwords (not your real password)
- Keep credentials in .env (not in code)
- Add .env to .gitignore
- Use environment variables

### ❌ DON'T:
- Commit passwords to Git
- Share your .env file
- Use your main Gmail password
- Hardcode credentials

---

## 📊 Email Limits

| Provider | Free Limit | Cost for More |
|----------|-----------|---------------|
| Gmail | 500/day | N/A (use SendGrid) |
| Outlook | 300/day | N/A (use SendGrid) |
| SendGrid | 100/day | $15/month for 40k |
| Mailgun | 100/day | $35/month for 50k |

**For HireWave**: Gmail's 500/day is more than enough!

---

## 🐛 Troubleshooting

### Error: "Authentication failed"
**Solution:**
1. Check 2FA is enabled
2. Generate new App Password
3. Remove spaces from password
4. Update .env file

### Error: "Connection refused"
**Solution:**
1. Check SMTP_HOST is correct
2. Check SMTP_PORT is 587
3. Check firewall settings
4. Try port 465 (SSL)

### Error: "Sender address rejected"
**Solution:**
1. Verify email address
2. Check SMTP_FROM_EMAIL matches SMTP_USER
3. Ensure email is verified

### Emails not received
**Solution:**
1. Check spam folder
2. Verify recipient email
3. Check email logs
4. Test with different email

---

## 💡 Tips

### For Development:
- Use your personal Gmail
- Check spam folder initially
- Enable "Less secure app access" if needed
- Use MailHog for local testing

### For Production:
- Use dedicated email account
- Consider SendGrid/Mailgun
- Set up SPF/DKIM records
- Monitor email delivery

### For Testing:
- Use temporary email services
- Check logs for errors
- Test all notification types
- Verify email templates

---

## 📧 Email Templates

HireWave includes professional email templates for:
- ✅ Application confirmation
- ✅ Assessment invitation
- ✅ Results notification
- ✅ Shortlist notification
- ✅ Rejection with feedback

All templates are:
- Mobile-responsive
- Professional design
- Personalized content
- Action buttons included

---

## 🚀 Quick Start Commands

```bash
# 1. Update .env with Gmail credentials
nano .env

# 2. Test email configuration
python3 test_email.py

# 3. Restart application
./run.sh

# 4. Test by applying to a job
# Check your email!
```

---

## 📱 Mobile App Passwords

### Gmail App Password:
1. Google Account → Security
2. 2-Step Verification → App passwords
3. Generate password
4. Copy and use in .env

### Outlook:
- Use regular password
- No app password needed

---

## 🎯 Recommended Setup

**For HireWave (Small to Medium Scale):**
```
Provider: Gmail
Cost: FREE
Limit: 500 emails/day
Setup Time: 5 minutes
Reliability: Excellent
```

**This is perfect for:**
- Development
- Testing
- Small companies
- MVP/Demo
- Up to 100 users/day

---

## 📈 Scaling Up

**When to upgrade:**
- More than 400 emails/day
- Need better deliverability
- Want detailed analytics
- Professional domain email

**Recommended:**
- SendGrid (40,000 emails/month for $15)
- Mailgun (50,000 emails/month for $35)
- AWS SES (62,000 emails/month for $6.20)

---

## ✅ Checklist

- [ ] Gmail account with 2FA enabled
- [ ] App Password generated
- [ ] .env file updated
- [ ] Spaces removed from password
- [ ] Test email sent successfully
- [ ] Application restarted
- [ ] Real notification tested
- [ ] Spam folder checked

---

**Ready to set up? Follow the Quick Setup guide above!**

For questions, check the Troubleshooting section.
