#!/usr/bin/env python3
"""
Test email configuration
"""

from app.utils.email import email_service
from app.config import settings
import sys


def test_email():
    """Test email sending"""
    
    print("=" * 60)
    print("HireWave - Email Configuration Test")
    print("=" * 60)
    
    # Check if SMTP is configured
    if not settings.SMTP_USER or not settings.SMTP_PASSWORD:
        print("\n❌ SMTP not configured!")
        print("\nPlease update your .env file with:")
        print("   SMTP_USER=your-email@gmail.com")
        print("   SMTP_PASSWORD=your-app-password")
        print("\nSee EMAIL_SETUP_GUIDE.md for instructions")
        sys.exit(1)
    
    print(f"\n📧 SMTP Configuration:")
    print(f"   Host: {settings.SMTP_HOST}")
    print(f"   Port: {settings.SMTP_PORT}")
    print(f"   User: {settings.SMTP_USER}")
    print(f"   From: {email_service.from_name} <{email_service.from_email}>")
    
    # Get test email
    test_email_address = input("\n📬 Enter email address to send test email to: ").strip()
    
    if not test_email_address:
        print("❌ No email address provided")
        sys.exit(1)
    
    print(f"\n🚀 Sending test email to {test_email_address}...")
    
    # Send test email
    subject = "HireWave - Test Email"
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
            .container { max-width: 600px; margin: 0 auto; padding: 20px; }
            .header { background: linear-gradient(135deg, #2563eb, #1e40af); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }
            .content { background: #f8fafc; padding: 30px; border-radius: 0 0 10px 10px; }
            .success-box { background: #d1fae5; padding: 20px; border-radius: 10px; text-align: center; margin: 20px 0; border: 3px solid #10b981; }
            .footer { text-align: center; margin-top: 30px; color: #64748b; font-size: 14px; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>✅ Email Configuration Test</h1>
            </div>
            <div class="content">
                <div class="success-box">
                    <h2 style="color: #059669; margin: 0;">Success!</h2>
                    <p style="margin: 10px 0 0 0;">Your email configuration is working correctly</p>
                </div>
                
                <p>If you're seeing this email, it means:</p>
                <ul>
                    <li>✅ SMTP settings are correct</li>
                    <li>✅ Authentication is working</li>
                    <li>✅ Emails can be sent successfully</li>
                    <li>✅ HireWave is ready to send notifications</li>
                </ul>
                
                <p><strong>Next Steps:</strong></p>
                <ol>
                    <li>Start the HireWave application</li>
                    <li>Test real notifications (apply to jobs, etc.)</li>
                    <li>Check spam folder if emails don't arrive</li>
                </ol>
                
                <p>Happy hiring! 🚀</p>
                
                <p>Best regards,<br>The HireWave Team</p>
            </div>
            <div class="footer">
                <p>&copy; 2026 HireWave. AI-Powered Recruitment.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    text_content = """
    Email Configuration Test
    
    Success! Your email configuration is working correctly.
    
    If you're seeing this email, it means:
    - SMTP settings are correct
    - Authentication is working
    - Emails can be sent successfully
    - HireWave is ready to send notifications
    
    Next Steps:
    1. Start the HireWave application
    2. Test real notifications (apply to jobs, etc.)
    3. Check spam folder if emails don't arrive
    
    Happy hiring!
    
    Best regards,
    The HireWave Team
    """
    
    success = email_service.send_email(test_email_address, subject, html_content, text_content)
    
    if success:
        print("\n✅ Test email sent successfully!")
        print(f"\n📬 Check your inbox at: {test_email_address}")
        print("   (Don't forget to check spam folder)")
        print("\n" + "=" * 60)
        print("✅ Email configuration is working!")
        print("=" * 60)
    else:
        print("\n❌ Failed to send test email")
        print("\nPossible issues:")
        print("   1. Check SMTP credentials in .env")
        print("   2. Verify App Password (not regular password)")
        print("   3. Check internet connection")
        print("   4. Review logs for error details")
        print("\nSee EMAIL_SETUP_GUIDE.md for troubleshooting")
        sys.exit(1)


if __name__ == "__main__":
    test_email()
