"""
Email utility for sending notifications
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import settings
import logging

logger = logging.getLogger(__name__)


class EmailService:
    def __init__(self):
        self.smtp_host = settings.SMTP_HOST
        self.smtp_port = settings.SMTP_PORT
        self.smtp_user = settings.SMTP_USER
        self.smtp_password = settings.SMTP_PASSWORD
        self.from_email = getattr(settings, 'SMTP_FROM_EMAIL', settings.SMTP_USER)
        self.from_name = getattr(settings, 'SMTP_FROM_NAME', 'HireWave')
    
    def send_email(self, to_email: str, subject: str, html_content: str, text_content: str = None):
        """Send an email"""
        
        # Skip if SMTP not configured
        if not self.smtp_user or not self.smtp_password:
            logger.warning("SMTP not configured, skipping email")
            return False
        
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = f"{self.from_name} <{self.from_email}>"
            msg['To'] = to_email
            
            # Add text version (fallback)
            if text_content:
                part1 = MIMEText(text_content, 'plain')
                msg.attach(part1)
            
            # Add HTML version
            part2 = MIMEText(html_content, 'html')
            msg.attach(part2)
            
            # Send email
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
            
            logger.info(f"Email sent successfully to {to_email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {e}")
            return False
    
    def send_application_confirmation(self, candidate_email: str, candidate_name: str, job_title: str, company_name: str):
        """Send application confirmation to candidate"""
        
        subject = f"Application Received - {job_title}"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #2563eb, #1e40af); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f8fafc; padding: 30px; border-radius: 0 0 10px 10px; }}
                .button {{ display: inline-block; padding: 12px 30px; background: #2563eb; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
                .footer {{ text-align: center; margin-top: 30px; color: #64748b; font-size: 14px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🎉 Application Received!</h1>
                </div>
                <div class="content">
                    <p>Hi {candidate_name},</p>
                    
                    <p>Thank you for applying to <strong>{job_title}</strong> at <strong>{company_name}</strong>!</p>
                    
                    <p>Your application has been successfully submitted and is now under review.</p>
                    
                    <h3>Next Steps:</h3>
                    <ul>
                        <li>Complete the assessment (if not done already)</li>
                        <li>We'll review your submission</li>
                        <li>You'll receive results within 24-48 hours</li>
                    </ul>
                    
                    <p style="text-align: center;">
                        <a href="http://localhost:8000/dashboard" class="button">View Dashboard</a>
                    </p>
                    
                    <p>Good luck! 🚀</p>
                    
                    <p>Best regards,<br>The HireWave Team</p>
                </div>
                <div class="footer">
                    <p>&copy; 2026 HireWave. AI-Powered Recruitment.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        text_content = f"""
        Hi {candidate_name},
        
        Thank you for applying to {job_title} at {company_name}!
        
        Your application has been successfully submitted and is now under review.
        
        Next Steps:
        - Complete the assessment (if not done already)
        - We'll review your submission
        - You'll receive results within 24-48 hours
        
        Good luck!
        
        Best regards,
        The HireWave Team
        """
        
        return self.send_email(candidate_email, subject, html_content, text_content)
    
    def send_assessment_invitation(self, candidate_email: str, candidate_name: str, job_title: str, assessment_link: str):
        """Send assessment invitation to candidate"""
        
        subject = f"Assessment Ready - {job_title}"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #2563eb, #1e40af); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f8fafc; padding: 30px; border-radius: 0 0 10px 10px; }}
                .button {{ display: inline-block; padding: 12px 30px; background: #10b981; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
                .info-box {{ background: #dbeafe; padding: 15px; border-radius: 5px; margin: 20px 0; }}
                .footer {{ text-align: center; margin-top: 30px; color: #64748b; font-size: 14px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>📝 Assessment Ready!</h1>
                </div>
                <div class="content">
                    <p>Hi {candidate_name},</p>
                    
                    <p>Your assessment for <strong>{job_title}</strong> is now ready!</p>
                    
                    <div class="info-box">
                        <strong>⏱️ Duration:</strong> 60 minutes<br>
                        <strong>📊 Format:</strong> MCQ, Coding, and Situational questions<br>
                        <strong>💡 Tip:</strong> Find a quiet place and ensure stable internet
                    </div>
                    
                    <p style="text-align: center;">
                        <a href="{assessment_link}" class="button">Start Assessment →</a>
                    </p>
                    
                    <p><strong>Important:</strong> Once you start, the timer begins. Make sure you're ready!</p>
                    
                    <p>Best of luck! 🍀</p>
                    
                    <p>Best regards,<br>The HireWave Team</p>
                </div>
                <div class="footer">
                    <p>&copy; 2026 HireWave. AI-Powered Recruitment.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        text_content = f"""
        Hi {candidate_name},
        
        Your assessment for {job_title} is now ready!
        
        Duration: 60 minutes
        Format: MCQ, Coding, and Situational questions
        
        Start Assessment: {assessment_link}
        
        Important: Once you start, the timer begins. Make sure you're ready!
        
        Best of luck!
        
        Best regards,
        The HireWave Team
        """
        
        return self.send_email(candidate_email, subject, html_content, text_content)
    
    def send_results_notification(self, candidate_email: str, candidate_name: str, job_title: str, score: float, results_link: str):
        """Send results notification to candidate"""
        
        subject = f"Assessment Results - {job_title}"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #2563eb, #1e40af); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f8fafc; padding: 30px; border-radius: 0 0 10px 10px; }}
                .score-box {{ background: white; padding: 20px; border-radius: 10px; text-align: center; margin: 20px 0; border: 3px solid #2563eb; }}
                .score {{ font-size: 48px; font-weight: bold; color: #2563eb; }}
                .button {{ display: inline-block; padding: 12px 30px; background: #2563eb; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
                .footer {{ text-align: center; margin-top: 30px; color: #64748b; font-size: 14px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>📊 Your Results Are Ready!</h1>
                </div>
                <div class="content">
                    <p>Hi {candidate_name},</p>
                    
                    <p>Your assessment for <strong>{job_title}</strong> has been evaluated!</p>
                    
                    <div class="score-box">
                        <div class="score">{score}%</div>
                        <p>Overall Score</p>
                    </div>
                    
                    <p>We've prepared a detailed feedback report including:</p>
                    <ul>
                        <li>✅ Skill-wise breakdown</li>
                        <li>💪 Your strengths</li>
                        <li>📈 Areas for improvement</li>
                        <li>📚 Learning resources</li>
                        <li>🎯 Personalized improvement plan</li>
                    </ul>
                    
                    <p style="text-align: center;">
                        <a href="{results_link}" class="button">View Detailed Results →</a>
                    </p>
                    
                    <p>Thank you for your time and effort!</p>
                    
                    <p>Best regards,<br>The HireWave Team</p>
                </div>
                <div class="footer">
                    <p>&copy; 2026 HireWave. AI-Powered Recruitment.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        text_content = f"""
        Hi {candidate_name},
        
        Your assessment for {job_title} has been evaluated!
        
        Overall Score: {score}%
        
        View your detailed feedback report: {results_link}
        
        The report includes:
        - Skill-wise breakdown
        - Your strengths
        - Areas for improvement
        - Learning resources
        - Personalized improvement plan
        
        Thank you for your time and effort!
        
        Best regards,
        The HireWave Team
        """
        
        return self.send_email(candidate_email, subject, html_content, text_content)
    
    def send_shortlist_notification(self, candidate_email: str, candidate_name: str, job_title: str, company_name: str):
        """Send shortlist notification to candidate"""
        
        subject = f"🎉 Congratulations! You've been shortlisted - {job_title}"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #10b981, #059669); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f8fafc; padding: 30px; border-radius: 0 0 10px 10px; }}
                .congrats-box {{ background: #d1fae5; padding: 20px; border-radius: 10px; text-align: center; margin: 20px 0; border: 3px solid #10b981; }}
                .button {{ display: inline-block; padding: 12px 30px; background: #10b981; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
                .footer {{ text-align: center; margin-top: 30px; color: #64748b; font-size: 14px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🏆 Congratulations!</h1>
                </div>
                <div class="content">
                    <p>Hi {candidate_name},</p>
                    
                    <div class="congrats-box">
                        <h2 style="color: #059669; margin: 0;">You've Been Shortlisted!</h2>
                        <p style="margin: 10px 0 0 0;">for <strong>{job_title}</strong> at <strong>{company_name}</strong></p>
                    </div>
                    
                    <p>Great news! Based on your excellent performance in the assessment, you've been shortlisted for the next round.</p>
                    
                    <h3>What's Next?</h3>
                    <ul>
                        <li>📞 The recruiter will contact you soon</li>
                        <li>💼 Prepare for the interview</li>
                        <li>📧 Keep an eye on your email</li>
                        <li>📱 Ensure your phone is reachable</li>
                    </ul>
                    
                    <p style="text-align: center;">
                        <a href="http://localhost:8000/dashboard" class="button">View Dashboard →</a>
                    </p>
                    
                    <p>We're excited about your potential and look forward to the next steps!</p>
                    
                    <p>Best regards,<br>The HireWave Team</p>
                </div>
                <div class="footer">
                    <p>&copy; 2026 HireWave. AI-Powered Recruitment.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        text_content = f"""
        Hi {candidate_name},
        
        Congratulations! You've been shortlisted for {job_title} at {company_name}!
        
        Based on your excellent performance in the assessment, you've been selected for the next round.
        
        What's Next?
        - The recruiter will contact you soon
        - Prepare for the interview
        - Keep an eye on your email
        - Ensure your phone is reachable
        
        We're excited about your potential!
        
        Best regards,
        The HireWave Team
        """
        
        return self.send_email(candidate_email, subject, html_content, text_content)
    
    def send_new_application_notification(self, recruiter_email: str, recruiter_name: str, candidate_name: str, job_title: str, candidate_skills: list):
        """Send new application notification to recruiter"""
        
        subject = f"New Application - {job_title}"
        
        skills_html = ", ".join(candidate_skills[:5])
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #2563eb, #1e40af); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f8fafc; padding: 30px; border-radius: 0 0 10px 10px; }}
                .candidate-box {{ background: white; padding: 20px; border-radius: 10px; margin: 20px 0; border-left: 4px solid #2563eb; }}
                .button {{ display: inline-block; padding: 12px 30px; background: #2563eb; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
                .footer {{ text-align: center; margin-top: 30px; color: #64748b; font-size: 14px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>👤 New Application Received</h1>
                </div>
                <div class="content">
                    <p>Hi {recruiter_name},</p>
                    
                    <p>You have a new application for <strong>{job_title}</strong>!</p>
                    
                    <div class="candidate-box">
                        <h3 style="margin-top: 0;">{candidate_name}</h3>
                        <p><strong>Skills:</strong> {skills_html}</p>
                    </div>
                    
                    <p>The candidate will complete the assessment soon. You'll be notified once it's ready for review.</p>
                    
                    <p style="text-align: center;">
                        <a href="http://localhost:8000/recruiter/jobs" class="button">View Applications →</a>
                    </p>
                    
                    <p>Best regards,<br>The HireWave Team</p>
                </div>
                <div class="footer">
                    <p>&copy; 2026 HireWave. AI-Powered Recruitment.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        text_content = f"""
        Hi {recruiter_name},
        
        You have a new application for {job_title}!
        
        Candidate: {candidate_name}
        Skills: {skills_html}
        
        The candidate will complete the assessment soon.
        
        View Applications: http://localhost:8000/recruiter/jobs
        
        Best regards,
        The HireWave Team
        """
        
        return self.send_email(recruiter_email, subject, html_content, text_content)


# Create singleton instance
email_service = EmailService()
