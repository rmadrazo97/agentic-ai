"""
Email Tool for communication and notifications
Mock implementation for demonstration (replace with real SMTP in production)
"""

import os
import json
from typing import Optional
from datetime import datetime
from langchain.tools import Tool


class EmailSender:
    """
    Email sending functionality (mock implementation for demo)
    In production, integrate with SMTP, SendGrid, or similar service
    """
    
    def __init__(self, smtp_config: Optional[dict] = None):
        self.smtp_config = smtp_config or {}
        # In production, configure real SMTP settings here
        self.mock_mode = True  # Set to False for real email sending
        
        # Create mock outbox directory
        self.outbox_dir = "outputs/email_outbox"
        os.makedirs(self.outbox_dir, exist_ok=True)
    
    def send_email(self, email_request: str) -> str:
        """
        Send an email based on the request
        
        Args:
            email_request: Email details in various formats
            
        Returns:
            Success/failure message
        """
        try:
            # Parse email request
            email_data = self._parse_email_request(email_request)
            
            if not email_data:
                return "Error: Invalid email format. Please provide recipient, subject, and body."
            
            # Validate required fields
            if not email_data.get('to'):
                return "Error: Email recipient (to) is required"
            
            if not email_data.get('subject'):
                return "Error: Email subject is required"
            
            if not email_data.get('body'):
                return "Error: Email body is required"
            
            # Send email (mock or real)
            if self.mock_mode:
                return self._mock_send_email(email_data)
            else:
                return self._real_send_email(email_data)
                
        except Exception as e:
            return f"Email sending failed: {str(e)}"
    
    def _parse_email_request(self, request: str) -> dict:
        """
        Parse email request in various formats
        
        Returns:
            dict with email fields
        """
        request = request.strip()
        
        # Try JSON format first
        try:
            return json.loads(request)
        except json.JSONDecodeError:
            pass
        
        # Try structured text format
        email_data = {}
        lines = request.split('\n')
        
        current_field = None
        current_content = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check for field headers
            if line.lower().startswith('to:'):
                if current_field:
                    email_data[current_field] = '\n'.join(current_content)
                current_field = 'to'
                current_content = [line[3:].strip()]
            elif line.lower().startswith('subject:'):
                if current_field:
                    email_data[current_field] = '\n'.join(current_content)
                current_field = 'subject'
                current_content = [line[8:].strip()]
            elif line.lower().startswith('body:'):
                if current_field:
                    email_data[current_field] = '\n'.join(current_content)
                current_field = 'body'
                current_content = [line[5:].strip()]
            else:
                # Continuation of current field
                if current_field:
                    current_content.append(line)
                else:
                    # No field specified, treat as body
                    current_field = 'body'
                    current_content = [line]
        
        # Add the last field
        if current_field:
            email_data[current_field] = '\n'.join(current_content)
        
        # Set defaults
        if 'to' not in email_data and 'recipient' in email_data:
            email_data['to'] = email_data['recipient']
        
        if 'to' not in email_data:
            # Extract email-like patterns from the text
            import re
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            emails = re.findall(email_pattern, request)
            if emails:
                email_data['to'] = emails[0]
        
        return email_data
    
    def _mock_send_email(self, email_data: dict) -> str:
        """
        Mock email sending - saves to file instead of actually sending
        """
        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"email_{timestamp}.json"
        filepath = os.path.join(self.outbox_dir, filename)
        
        # Add metadata
        email_with_metadata = {
            "timestamp": datetime.now().isoformat(),
            "status": "mock_sent",
            "to": email_data.get('to'),
            "from": email_data.get('from', 'agent@localhost'),
            "subject": email_data.get('subject'),
            "body": email_data.get('body'),
            "cc": email_data.get('cc'),
            "bcc": email_data.get('bcc')
        }
        
        # Save to file
        with open(filepath, 'w') as f:
            json.dump(email_with_metadata, f, indent=2)
        
        return f"""✅ Email sent successfully (MOCK MODE)!
        
To: {email_data['to']}
Subject: {email_data['subject']}
Body Length: {len(email_data['body'])} characters

📁 Email saved to: {filepath}
💡 This is a mock implementation. In production, integrate with real SMTP service."""
    
    def _real_send_email(self, email_data: dict) -> str:
        """
        Real email sending implementation (placeholder)
        """
        # TODO: Implement real SMTP sending
        # Example with smtplib:
        # import smtplib
        # from email.mime.text import MIMEText
        # from email.mime.multipart import MIMEMultipart
        
        # msg = MIMEMultipart()
        # msg['From'] = self.smtp_config['from']
        # msg['To'] = email_data['to']
        # msg['Subject'] = email_data['subject']
        # msg.attach(MIMEText(email_data['body'], 'plain'))
        
        # server = smtplib.SMTP(self.smtp_config['smtp_server'], self.smtp_config['port'])
        # server.starttls()
        # server.login(self.smtp_config['username'], self.smtp_config['password'])
        # server.send_message(msg)
        # server.quit()
        
        return "Real email sending not implemented yet. Set mock_mode=True"
    
    def list_sent_emails(self) -> str:
        """
        List all sent emails (mock outbox)
        """
        try:
            email_files = [f for f in os.listdir(self.outbox_dir) if f.endswith('.json')]
            
            if not email_files:
                return "No emails found in outbox"
            
            result = ["📧 Email Outbox:"]
            
            for filename in sorted(email_files, reverse=True):
                filepath = os.path.join(self.outbox_dir, filename)
                with open(filepath, 'r') as f:
                    email_data = json.load(f)
                
                timestamp = email_data.get('timestamp', 'Unknown')
                to = email_data.get('to', 'Unknown')
                subject = email_data.get('subject', 'No Subject')
                
                result.append(f"  • {timestamp}: To {to} - '{subject}'")
            
            return "\n".join(result)
            
        except Exception as e:
            return f"Error listing emails: {str(e)}"


def create_email_tool() -> Tool:
    """
    Create an email sending tool
    
    Returns:
        LangChain Tool object for email operations
    """
    email_sender = EmailSender()
    
    def email_operations(operation_input: str) -> str:
        """
        Handle email operations
        
        Formats:
        - Send: 'to: user@example.com\nsubject: Hello\nbody: Message content'
        - Send JSON: '{"to": "user@example.com", "subject": "Hello", "body": "Message"}'
        - List: 'list'
        """
        operation_input = operation_input.strip()
        
        if operation_input.lower() == 'list':
            return email_sender.list_sent_emails()
        else:
            return email_sender.send_email(operation_input)
    
    return Tool.from_function(
        name="email_sender",
        description="""Send emails and manage outbox. MOCK MODE - emails are saved to files instead of actually sent.
        
        Formats:
        - 'to: recipient@example.com\\nsubject: Your Subject\\nbody: Your message content'
        - '{"to": "recipient@example.com", "subject": "Subject", "body": "Message"}'
        - 'list' - show sent emails
        
        Use for notifications, reports, or communication tasks.""",
        func=email_operations
    )


# Test function
def test_email_tool():
    """Test the email tool"""
    print("📧 Testing Email Tool...")
    
    tool = create_email_tool()
    
    # Test 1: Send structured email
    print("\nTest 1: Send structured email")
    email_request = """to: alice@example.com
subject: Test Report
body: This is a test email with a report attached.
The agent has completed the requested task successfully."""
    
    result = tool.func(email_request)
    print(result)
    
    # Test 2: Send JSON email
    print("\nTest 2: Send JSON email")
    json_email = '{"to": "bob@example.com", "subject": "Data Analysis Complete", "body": "The analysis has been completed. Please find the results in the attached CSV file."}'
    result = tool.func(json_email)
    print(result)
    
    # Test 3: List sent emails
    print("\nTest 3: List sent emails")
    result = tool.func("list")
    print(result)
    
    print("\n✅ Email tool test completed")


if __name__ == "__main__":
    test_email_tool()