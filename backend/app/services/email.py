import logging
import resend
from datetime import datetime
from app.core.config import settings

logger = logging.getLogger(__name__)

def send_welcome_email(to_email: str, name: str = None) -> bool:
    """
    Sends a beautifully formatted welcome email to a new user using Resend.
    Fails gracefully by simulating success in dev environment if RESEND_API_KEY is not set.
    """
    if not settings.RESEND_API_KEY:
        logger.warning("RESEND_API_KEY is not configured. Simulating welcome email dispatch.")
        print(f"[SIMULATED EMAIL] To: {to_email}, Subject: Welcome to FlowSpace 🌲")
        return True

    resend.api_key = settings.RESEND_API_KEY
    display_name = name or to_email.split("@")[0]
    client_url = "http://localhost:5173"  # Standard frontend URL
    current_year = datetime.now().year

    # Nordic Cabin Theme design aligned HTML
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Welcome to FlowSpace</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,600;1,9..144,400&display=swap');
    body {{
      margin: 0;
      padding: 0;
      width: 100% !important;
      background-color: #F4F1EB;
      font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
      -webkit-font-smoothing: antialiased;
    }}
    table {{
      border-collapse: collapse;
    }}
    .wrapper {{
      width: 100%;
      table-layout: fixed;
      background-color: #F4F1EB;
      padding: 40px 0;
    }}
    .container {{
      max-width: 600px;
      margin: 0 auto;
      background-color: #FCFBF9;
      border: 1px solid #E2DDD6;
      border-radius: 16px;
      overflow: hidden;
      box-shadow: 0 4px 12px rgba(44, 53, 40, 0.04);
    }}
    .header {{
      padding: 32px 32px 16px 32px;
      text-align: center;
    }}
    .logo-container {{
      display: inline-block;
      background-color: #7D8C74;
      border-radius: 8px;
      padding: 8px 16px;
      margin-bottom: 24px;
    }}
    .logo-text {{
      font-family: 'Fraunces', Georgia, serif;
      font-size: 20px;
      font-weight: 600;
      color: #FCFBF9;
      text-decoration: none;
      letter-spacing: 0.02em;
    }}
    .greeting {{
      font-family: 'Fraunces', Georgia, serif;
      font-size: 28px;
      font-weight: 600;
      color: #2C3528;
      margin: 0 0 16px 0;
      line-height: 1.2;
    }}
    .subtitle {{
      font-size: 16px;
      color: #6B7A65;
      margin: 0;
      line-height: 1.5;
    }}
    .content {{
      padding: 0 32px 32px 32px;
    }}
    .divider {{
      height: 1px;
      background-color: #E2DDD6;
      margin: 24px 0;
    }}
    .feature-list {{
      margin: 24px 0;
      padding: 0;
      list-style-type: none;
    }}
    .feature-item {{
      margin-bottom: 20px;
      padding-left: 36px;
      position: relative;
    }}
    .feature-icon {{
      position: absolute;
      left: 0;
      top: 2px;
      font-size: 20px;
    }}
    .feature-title {{
      font-size: 16px;
      font-weight: 700;
      color: #2C3528;
      margin: 0 0 4px 0;
    }}
    .feature-desc {{
      font-size: 14px;
      color: #6B7A65;
      margin: 0;
      line-height: 1.5;
    }}
    .cta-container {{
      text-align: center;
      margin: 32px 0 16px 0;
    }}
    .btn-primary {{
      display: inline-block;
      background-color: #B66D49;
      color: #FFFFFF !important;
      font-family: 'DM Sans', sans-serif;
      font-size: 15px;
      font-weight: 500;
      text-decoration: none;
      padding: 12px 32px;
      border-radius: 12px;
      box-shadow: 0 2px 4px rgba(182, 109, 73, 0.2);
    }}
    .signoff {{
      font-family: 'Fraunces', Georgia, serif;
      font-style: italic;
      font-size: 16px;
      color: #2C3528;
      margin: 24px 0 8px 0;
    }}
    .footer {{
      text-align: center;
      padding: 24px;
      font-size: 12px;
      color: #A3AE9E;
      line-height: 1.5;
    }}
  </style>
</head>
<body>
  <div class="wrapper">
    <div class="container">
      <div class="header">
        <div class="logo-container">
          <span class="logo-text">🌲 FlowSpace</span>
        </div>
        <h1 class="greeting">Good to have you here, {display_name}.</h1>
        <p class="subtitle">Welcome to FlowSpace — your cozy digital sanctuary for focused, calm, and intentional work.</p>
      </div>
      
      <div class="content">
        <div class="divider"></div>
        
        <p style="font-size: 15px; color: #2C3528; line-height: 1.6; margin: 0 0 20px 0;">
          Step into a workspace designed to feel like sitting at a warm wooden desk in a quiet cabin. No clinical dashboards. No high-density clutter. Just breathing room to focus on what matters most to you.
        </p>

        <p style="font-size: 15px; color: #2C3528; line-height: 1.6; margin: 0 0 20px 0;">
          Here are a few cozy spots in your new space to help you find your flow:
        </p>

        <ul class="feature-list">
          <li class="feature-item">
            <span class="feature-icon">⏱️</span>
            <h3 class="feature-title">The Focus Timer</h3>
            <p class="feature-desc">A customizable, beautifully minimalist timer that transitions the entire environment into focus mode, gently removing non-essential visual noise.</p>
          </li>
          <li class="feature-item">
            <span class="feature-icon">🪴</span>
            <h3 class="feature-title">The Task Garden</h3>
            <p class="feature-desc">A spacious, clean canvas to cultivate your daily tasks. Add subtasks, set priorities (from Low to Terracotta-tinted High), and watch your garden grow.</p>
          </li>
          <li class="feature-item">
            <span class="feature-icon">🌧️</span>
            <h3 class="feature-title">Cozy Ambient Sounds</h3>
            <p class="feature-desc">Mix background sounds like soft rain, crackling firewood, or forest birds to build a warm auditory bubble around your screen.</p>
          </li>
        </ul>

        <div class="cta-container">
          <a href="{client_url}" class="btn-primary">Enter FlowSpace</a>
        </div>

        <div class="divider"></div>

        <p class="signoff">With warmth,<br>The FlowSpace Team</p>
      </div>
    </div>
    
    <div class="footer">
      <p>Sit back, take a breath, and find your flow.</p>
      <p style="margin-top: 8px;">© {current_year} FlowSpace. All rights reserved.</p>
    </div>
  </div>
</body>
</html>
"""

    try:
        r = resend.Emails.send({
            "from": settings.FROM_EMAIL,
            "to": [to_email],
            "subject": "Welcome to FlowSpace 🌲",
            "html": html_content
        })
        logger.info(f"Welcome email successfully sent to {to_email}. Response ID: {r.get('id') if isinstance(r, dict) else r}")
        return True
    except Exception as e:
        logger.error(f"Failed to send welcome email to {to_email} via Resend: {str(e)}")
        return False
