email_confirm = """Hi there {username},

Thank you for signing up to Murof! Please click the link below to verify your email:

{verification_link}

This link will expire in 24 hours. If you did not sign up for Murof, you can safely ignore this email.

Best,
The Murof Team
"""

email_warning = """Hi there {username},

We noticed that someone tried to sign up for Murof using your email address.

What now?
- If this was not you, you can safely ignore this email.
- If this was you, please login using your existing account: https://murof.net/auth/login
- If you've forgotten your password and can't login, reset your password: https://murof.net/auth/reset/request
- If you have any questions or concerns, please contact us: contact@murof.net

Best,
The Murof Team
"""

password_reset = """Hi there {username},

We received a request to reset your password on Murof. Please click the link below to reset your password:

{reset_link}

This link will expire in 10 minutes. If you did not request a password reset, you can safely ignore this email.

Best,
The Murof Team
"""