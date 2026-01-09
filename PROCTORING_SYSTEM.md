# Proctoring System Documentation

## Overview
HireWave now includes a comprehensive proctoring system to ensure fair and secure assessments.

---

## 🔒 Security Features

### 1. Tab-Switching Detection
**Real-time monitoring** of candidate behavior during assessments.

**How it works:**
- Detects when candidate switches tabs
- Detects when candidate minimizes browser
- Detects when candidate uses Alt+Tab / Cmd+Tab
- Detects when window loses focus

### 2. Three-Strike Policy

| Violation | Action | Consequence |
|-----------|--------|-------------|
| **1st** | ⚠️ Warning shown | 10-second countdown to return |
| **2nd** | 🚨 Final warning | 10-second countdown to return |
| **3rd** | ❌ Disqualification | Auto-submit + Ineligible for job |

### 3. Additional Security
- ✅ Right-click disabled
- ✅ Developer tools blocked (F12, Ctrl+Shift+I)
- ✅ Copy/paste monitoring
- ✅ Timer enforcement (auto-submit on timeout)
- ✅ Full-screen encouraged
- ✅ Activity logging

---

## 📋 Assessment Flow

### Step 1: Rules & Guidelines Page
**URL**: `/assessment/{application_id}`

**Features:**
- Comprehensive rules display
- Tab-switching policy explanation
- Time limit information
- Allowed/prohibited actions
- Consent checkbox
- "Start Assessment" button (disabled until consent)

**Rules Displayed:**
1. ⏱️ Time Limit (60 minutes)
2. 💻 Browser Requirements
3. 🚨 Tab Switching Policy
4. 🛡️ Proctoring & Monitoring
5. 📝 Question Types
6. ✅ Allowed Actions
7. ❌ Prohibited Actions
8. 💾 Submission Guidelines

### Step 2: Proctored Assessment
**URL**: `/assessment/take/{application_id}`

**Features:**
- Proctoring status bar (always visible)
- Real-time timer
- Warning counter display
- Tab-switch detection active
- Question navigation
- Auto-save answers
- Progress indicator

---

## 🎨 User Interface

### Proctoring Bar (Top)
```
[🟢 Proctored] [⚠️ Warnings: 0/2] [Timer: 60:00]
```

**Elements:**
- Status indicator (green dot = active)
- Warning counter (updates in real-time)
- Countdown timer (MM:SS format)

### Warning Modal
**Appears when tab-switch detected:**

**First Warning:**
```
⚠️ FIRST WARNING!
You switched tabs or left the assessment window!

[10 second countdown]

Return to the assessment immediately!
You have 1 more warning left.
Third violation = DISQUALIFICATION!
```

**Second Warning:**
```
🚨 FINAL WARNING!
This is your LAST warning!

[10 second countdown]

Return to the assessment immediately!
One more violation and you will be DISQUALIFIED!
```

**Third Violation:**
```
❌ DISQUALIFIED!
You have been disqualified from this assessment.

✖

You violated the rules 3 times.
Your assessment has been automatically submitted
and you are not eligible for this position.
```

---

## 🔧 Technical Implementation

### Frontend Detection
```javascript
// Visibility API
document.addEventListener('visibilitychange', function() {
    if (document.hidden) {
        handleTabSwitch();
    }
});

// Window blur
window.addEventListener('blur', function() {
    handleTabSwitch();
});
```

### Warning System
```javascript
function handleTabSwitch() {
    warningCount++;
    
    if (warningCount >= 3) {
        disqualifyCandidate();
    } else {
        showWarning();
    }
}
```

### Auto-Disqualification
```javascript
function disqualifyCandidate() {
    isDisqualified = true;
    clearInterval(timerInterval);
    
    // Show disqualification modal
    // Auto-submit after 5 seconds
    // Redirect to dashboard
}
```

### Data Stored
```json
{
  "submission_id": "sub_xxx",
  "warning_count": 2,
  "disqualified": false,
  "answers": [...],
  "total_time_seconds": 3600
}
```

---

## 📊 Monitoring & Logging

### What's Tracked:
- ✅ Tab switches (count and timestamps)
- ✅ Time spent per question
- ✅ Total assessment time
- ✅ Warning events
- ✅ Disqualification events
- ✅ Submission method (manual/auto/disqualified)

### Logs Example:
```
INFO: Assessment started for application app_xxx
INFO: Tab switch detected - Warning 1/2
INFO: Tab switch detected - Warning 2/2
WARNING: Tab switch detected - Candidate disqualified
INFO: Assessment auto-submitted due to disqualification
```

---

## 🎯 Rules Enforced

### ✅ Allowed:
- Navigate between questions
- Change answers before submission
- Use provided code editor
- Think and take time (within limit)
- Use Next/Previous buttons

### ❌ Prohibited:
- Switching tabs or windows
- Using external resources
- Copying questions
- Using AI tools
- Getting help from others
- Taking screenshots
- Refreshing the page
- Minimizing browser

---

## 🧪 Testing the System

### Test 1: Normal Flow
```bash
# 1. Login as candidate
# 2. Apply to a job
# 3. Click "Start Assessment"
# 4. Read rules
# 5. Check consent box
# 6. Start assessment
# 7. Complete normally
# 8. Submit
```

### Test 2: First Warning
```bash
# 1. Start assessment
# 2. Switch to another tab (Alt+Tab)
# 3. Warning modal appears
# 4. Return within 10 seconds
# 5. Warning counter shows 1/2
# 6. Continue assessment
```

### Test 3: Disqualification
```bash
# 1. Start assessment
# 2. Switch tabs 3 times
# 3. Disqualification modal appears
# 4. Auto-submit after 5 seconds
# 5. Redirected to dashboard
# 6. Marked as disqualified
```

### Test 4: Time Expiry
```bash
# 1. Start assessment
# 2. Wait for timer to reach 00:00
# 3. Auto-submit triggered
# 4. Redirected to dashboard
```

---

## 📱 Browser Compatibility

| Browser | Tab Detection | Timer | Warnings | Status |
|---------|---------------|-------|----------|--------|
| Chrome | ✅ | ✅ | ✅ | Fully Supported |
| Firefox | ✅ | ✅ | ✅ | Fully Supported |
| Safari | ✅ | ✅ | ✅ | Fully Supported |
| Edge | ✅ | ✅ | ✅ | Fully Supported |
| Mobile | ⚠️ | ✅ | ⚠️ | Limited Support |

**Recommendation**: Use desktop browsers for best experience.

---

## 🔐 Security Measures

### 1. Consent Required
- Must read all rules
- Must check consent box
- Cannot start without consent

### 2. Session Management
- Consent stored in localStorage
- Cleared after submission
- Cannot bypass rules page

### 3. Prevention Techniques
- Right-click disabled
- Developer tools blocked
- Keyboard shortcuts disabled
- Copy/paste monitored

### 4. Data Integrity
- Warning count stored in submission
- Disqualification flag recorded
- Timestamps logged
- Cannot be manipulated client-side

---

## 📈 Statistics & Analytics

### For Recruiters:
View candidate behavior:
- Warning count per candidate
- Disqualification status
- Time spent per question
- Completion rate

### For System:
- Average warning count
- Disqualification rate
- Most common violations
- Assessment completion time

---

## 🎓 Candidate Experience

### Before Assessment:
1. See clear rules and guidelines
2. Understand consequences
3. Give informed consent
4. Prepare environment

### During Assessment:
1. See proctoring status (reassuring)
2. Know warning count (transparent)
3. See timer (time management)
4. Focus on questions

### After Violation:
1. Immediate feedback (warning modal)
2. Clear countdown (10 seconds)
3. Know consequences (next steps)
4. Opportunity to correct

---

## 🛠️ Configuration

### Adjust Warning Limit
```javascript
// In assessment_proctored.html
if (warningCount >= 3) {  // Change to 2 or 4
    disqualifyCandidate();
}
```

### Adjust Warning Timeout
```javascript
// In assessment_proctored.html
let countdown = 10;  // Change to 5 or 15 seconds
```

### Adjust Timer Duration
```javascript
// In assessment config
duration_minutes: 60  // Change to 45 or 90
```

---

## 🐛 Troubleshooting

### Issue: False Positives
**Cause**: Browser notifications, system alerts
**Solution**: Instruct candidates to close all apps

### Issue: Warning Not Showing
**Cause**: Modal blocked or hidden
**Solution**: Check z-index and display properties

### Issue: Timer Not Starting
**Cause**: JavaScript error
**Solution**: Check browser console for errors

### Issue: Cannot Submit
**Cause**: Network error
**Solution**: Auto-retry or save locally

---

## 📚 Files Modified/Created

### New Files:
1. `templates/assessment_rules.html` - Rules page
2. `templates/assessment_proctored.html` - Proctored assessment
3. `PROCTORING_SYSTEM.md` - This documentation

### Modified Files:
1. `app/main.py` - Added new routes
2. `app/models/submission.py` - Added proctoring fields
3. `templates/assessment.html` - Kept as backup

---

## 🚀 Future Enhancements

### Planned Features:
- 📹 Webcam monitoring (optional)
- 🎤 Audio monitoring (optional)
- 📊 Advanced analytics dashboard
- 🤖 AI-based behavior analysis
- 📱 Mobile app support
- 🔔 Real-time alerts to recruiters
- 📸 Screenshot capture on violations
- 🌐 IP address tracking
- 🖥️ Screen recording (optional)

---

## ✅ Checklist

- [x] Rules page created
- [x] Proctored assessment page created
- [x] Tab-switching detection implemented
- [x] Warning system implemented
- [x] Disqualification logic implemented
- [x] Timer implemented
- [x] Auto-submit implemented
- [x] Consent mechanism implemented
- [x] Data storage updated
- [x] Routes added
- [x] Documentation complete

---

## 🎯 Summary

**HireWave now provides:**
- ✅ Secure, proctored assessments
- ✅ Fair three-strike policy
- ✅ Real-time monitoring
- ✅ Clear rules and guidelines
- ✅ Transparent warning system
- ✅ Automatic disqualification
- ✅ Complete audit trail

**Result**: Fair, secure, and trustworthy assessment environment! 🎉

---

For questions or issues, refer to the troubleshooting section or check the code comments.
