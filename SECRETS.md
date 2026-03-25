# spockpm Secret Management Guidelines

## Overview
This document outlines best practices for managing API keys, secrets, and sensitive configuration in the spockpm project.

## Core Principles
1. **Never commit real secrets to git** - This includes API keys, database passwords, tokens, etc.
2. **Use platform-specific secret management** - Leverage built-in systems from Vercel, Supabase, etc.
3. **Use environment variables** - Access secrets via `process.env` (Node.js) or `os.environ` (Python)
4. **Different secrets for different environments** - Development, staging, and production should use separate credentials

## Local Development

### .env.local File
Create a `.env.local` file in the project root for development secrets. This file is automatically ignored by git due to our `.gitignore` rules.

```env
# Supabase ConfigurationSUPABASE_URL=http://127.0.0.1:54321
SUPABASE_ANON_KEY=your-local-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-local-service-role-key# Cloudflare R2 Configuration (for local development if needed)
CLOUDFLARE_R2_ACCOUNT_ID=your-account-id
CLOUDFLARE_R2_ACCESS_KEY_ID=your-access-key-id
CLOUDFLARE_R2_SECRET_ACCESS_KEY=your-secret-access-key
CLOUDFLARE_R2_BUCKET_NAME=spockpm-storage

# Optional API Keys
OPENAI_API_KEY=your-openai-key-for-local-dev
```

### Accessing Secrets in Code
**Python (Vercel API):**
```pythonimport os

supabase_url = os.environ.get('SUPABASE_URL')
supabase_key = os.environ.get('SUPABASE_ANON_KEY')
```

**Node.js (if applicable):**
```javascript
const supabaseUrl = process.env.SUPABASE_URL;
const supabaseKey = process.env.SUPABASE_ANON_KEY;
```

## Vercel Production Deployment

### Setting Environment Variables
1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Select your spockpm project
3. Navigate to Settings → Environment Variables
4. Add each variable:
   - Name: Variable name (e.g., `SUPABASE_URL`)
   - Value: The actual secret value
   - Environment: Choose Production, Preview, or Development as needed
5. Click Save

### Important Notes for Vercel
- Vercel encrypts environment variables at rest
- Variables are injected into the runtime environment
- No need to worry about `.env` files in production
- Changes require a redeployment to take effect

## Supabase Secrets

### API Keys (Non-Secret)
- **anon key**: Safe to expose to clients (found in Supabase Dashboard → Settings → API)
- **public**: Can be shared publicly

### Service Role Key (SECRET)
- **Never expose to clients**
- **Only use in secure backend contexts**
- Store in Vercel Environment Variables for server-side use

### Supabase Vault (Optional - for Pro plans)
For additional security on Supabase Pro plans, consider using the Vault feature for storing secrets.

## Cloudflare R2 Credentials

### Local Development with Wrangler
When you run `wrangler login` and configure R2, credentials are stored locally in:
- `.wrangler/credentials.toml` (or similar)
- This file is NOT committed to git (included in default git ignores)

### Production Access
For Vercel production access to R2:
1. Create API tokens in Cloudflare Dashboard
2. Store as Environment Variables in Vercel:
   - `CLOUDFLARE_R2_ACCOUNT_ID`
   - `CLOUDFLARE_R2_ACCESS_KEY_ID`
   - `CLOUDFLARE_R2_SECRET_ACCESS_KEY`
3. Access in your code as shown above## .gitignore Rules
Our `.gitignore` includes:
```
.env
.env.*
!.env.example
```
This means:
- All `.env` files are ignored (including `.env.local`, `.env.production`, etc.)
- EXCEPT `.env.example` which IS committed as a template

## Adding New Secrets
When you need to add a new API key or secret:
1. Add it to `.env.example` with a placeholder value (commit this)
2. Add the actual value to your local `.env.local` (do NOT commit)
3. Add it to Vercel Environment Variables for production
4. Update any documentation or code that needs to use it

## Rotation and Security
- Regularly rotate API keys and secrets
- Immediately revoke and replace any suspected compromised credentials
- Use least-privilege principle: create keys with only necessary permissions
- Audit access logs when available

## CI/CD Considerations
If you set up automated testing or deployment pipelines:
- Configure secret injection in your CI/CD system
- Never log or expose secrets in build outputs
- Use protected variables/features in your CI/CD platform

## Emergency Procedures
If a secret is accidentally committed:
1. Immediately revoke/regenerate the secret
2. Check git history to see if it was pushed3. If pushed, treat as compromised and rotate immediately
4. Consider using tools like `git-secrets` or pre-commit hooks to prevent future accidents

## Summary for spockpm
- **Local**: Use `.env.local` (gitignored)
- **Vercel**: Use Platform Environment Variables
- **Supabase**: Use Dashboard settings + Vercel Env Vars for service keys
- **Cloudflare R2**: Use Vercel Env Vars for production access
- **Never**: Commit real secrets, API keys, or tokens to git