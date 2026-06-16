# Security Policy

## Project Status

⚠️ **This is currently a personal project and is NOT ready for production use.**

This project is under active development and has not been security audited. Use at your own risk in non-production environments only.

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |
| 0.1.x   | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability, please report it responsibly:

### How to Report

1. **Do NOT** open a public issue
2. Email security reports to: [info@fahdjud.com]
3. Include the following information:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

### What to Expect

- **Response Time**: As this is a personal project, response times may vary
- **Updates**: I'll do my best to address critical security issues
- **Disclosure**: Security fixes will be documented in release notes

### Security Best Practices

If you're experimenting with this project:

- Keep your dependencies up to date
- Use strong, unique values for `SECRET_KEY`
- Never commit `.env` files or credentials to version control
- Set `DEBUG = False` if testing in any public environment
- Follow Flask security guidelines: https://flask.palletsprojects.com/en/stable/web-security/

## Disclaimer

This project is provided "as is" without warranty of any kind. It is not intended for production use until a stable 1.0.0 release is announced.

Thank you for your understanding!