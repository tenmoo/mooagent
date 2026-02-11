# Deployment Guide

This guide covers deploying MooAgent to production using Fly.io (backend) and Vercel (frontend).

## Prerequisites

- [Fly.io account](https://fly.io/app/sign-up) (free tier available)
- [Vercel account](https://vercel.com/signup) (free tier available)
- Groq API key
- Both backend and frontend tested locally

## Part 1: Deploy Backend to Fly.io

### 1.1 Install Fly CLI

**On macOS/Linux:**
```bash
curl -L https://fly.io/install.sh | sh
```

**On Windows (PowerShell):**
```powershell
iwr https://fly.io/install.ps1 -useb | iex
```

### 1.2 Login to Fly

```bash
fly auth login
```

This will open a browser window for authentication.

### 1.3 Navigate to Backend Directory

```bash
cd backend
```

### 1.4 Launch Your App

```bash
fly launch
```

You'll be prompted with several questions:

- **App Name**: Choose a unique name (e.g., `mooagent-backend-yourname`)
- **Region**: Choose the region closest to you
- **Database**: Select "No" (we're using in-memory storage for demo)
- **Deploy now**: Select "No" (we need to set secrets first)

This creates a `fly.toml` file (already included in the project).

### 1.5 Set Environment Secrets

```bash
fly secrets set GROQ_API_KEY="your_groq_api_key"
fly secrets set SECRET_KEY="your_generated_secret_key"
fly secrets set ALLOWED_ORIGINS="https://your-frontend-domain.vercel.app"
```

**Note**: You'll update `ALLOWED_ORIGINS` again after deploying the frontend.

### 1.6 Deploy

```bash
fly deploy
```

This will:
1. Build your application
2. Create a Docker container
3. Deploy to Fly.io infrastructure
4. Start your app

### 1.7 Verify Deployment

```bash
fly status
fly logs
```

Visit your app at: `https://your-app-name.fly.dev`

Check the health endpoint: `https://your-app-name.fly.dev/health`

You should see: `{"status": "healthy"}`

### 1.8 View API Documentation

Visit: `https://your-app-name.fly.dev/docs`

## Part 2: Deploy Frontend to Vercel

### 2.1 Install Vercel CLI (Optional)

```bash
npm install -g vercel
```

### 2.2 Login to Vercel

```bash
vercel login
```

### 2.3 Navigate to Frontend Directory

```bash
cd frontend
```

### 2.4 Deploy to Vercel

**Option A: Using CLI**

```bash
vercel
```

Follow the prompts:
- **Set up and deploy**: Yes
- **Link to existing project**: No
- **Project name**: Accept default or customize
- **Directory**: `./` (current directory)
- **Override settings**: No

Then deploy to production:

```bash
vercel --prod
```

**Option B: Using Git (Recommended)**

1. Push your code to GitHub:
```bash
git add .
git commit -m "Initial commit"
git push origin main
```

2. Go to [Vercel Dashboard](https://vercel.com/dashboard)

3. Click "Add New" → "Project"

4. Import your GitHub repository

5. Configure project:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`

6. Add environment variable:
   - **Name**: `VITE_API_URL`
   - **Value**: `https://your-backend-app.fly.dev`

7. Click "Deploy"

### 2.5 Verify Deployment

Visit your deployed frontend URL (provided by Vercel).

You should see the MooAgent login page.

## Part 3: Connect Frontend and Backend

### 3.1 Update Backend CORS Settings

Now that you have your frontend URL, update the backend CORS settings:

```bash
cd backend
fly secrets set ALLOWED_ORIGINS="https://your-frontend-domain.vercel.app"
```

### 3.2 Restart Backend

```bash
fly deploy
```

### 3.3 Test the Integration

1. Visit your frontend URL
2. Sign up for a new account
3. Try chatting with the agent
4. Verify everything works

## Part 4: Custom Domains (Optional)

### 4.1 Add Custom Domain to Fly.io

```bash
fly domains add api.yourdomain.com
```

Follow the instructions to configure DNS.

### 4.2 Add Custom Domain to Vercel

1. Go to Vercel Dashboard → Your Project → Settings → Domains
2. Add your domain
3. Configure DNS according to Vercel's instructions

### 4.3 Update CORS Settings

```bash
fly secrets set ALLOWED_ORIGINS="https://yourdomain.com"
```

## Monitoring and Maintenance

### Backend Monitoring (Fly.io)

**View logs:**
```bash
fly logs
```

**View metrics:**
```bash
fly dashboard
```

**Scale your app:**
```bash
fly scale count 2  # Run 2 instances
fly scale vm shared-cpu-1x --memory 512  # Change VM size
```

### Frontend Monitoring (Vercel)

1. Visit [Vercel Dashboard](https://vercel.com/dashboard)
2. Click on your project
3. View deployments, analytics, and logs

### Update Environment Variables

**Fly.io:**
```bash
fly secrets set VARIABLE_NAME="new_value"
```

**Vercel:**
1. Dashboard → Project → Settings → Environment Variables
2. Edit or add variables
3. Redeploy for changes to take effect

## Troubleshooting

### Backend Deployment Issues

**Build fails:**
- Check `requirements.txt` is complete
- Verify Python version in `fly.toml`
- Review build logs: `fly logs`

**App crashes:**
- Check logs: `fly logs`
- Verify environment variables: `fly secrets list`
- Check app status: `fly status`

**API not accessible:**
- Verify deployment: `fly status`
- Check health: `curl https://your-app.fly.dev/health`
- Review firewall/network settings

### Frontend Deployment Issues

**Build fails:**
- Check `package.json` dependencies
- Verify build command in Vercel settings
- Review build logs in Vercel dashboard

**Environment variables not working:**
- Ensure variables start with `VITE_`
- Redeploy after adding variables
- Check spelling and values

### CORS Errors

**"Access to fetch has been blocked by CORS policy"**

1. Verify `ALLOWED_ORIGINS` in backend:
```bash
fly secrets list
```

2. Make sure it matches your frontend URL exactly (including https://)

3. Update if needed:
```bash
fly secrets set ALLOWED_ORIGINS="https://your-frontend.vercel.app"
```

4. Redeploy backend:
```bash
fly deploy
```

### Authentication Issues

**JWT errors or "401 Unauthorized":**
- Verify `SECRET_KEY` is set in backend
- Check token expiration settings
- Clear browser localStorage and re-login

## Cost Estimation

### Fly.io (Backend)
- **Free tier**: 3 shared-cpu-1x VMs with 256MB RAM each
- **Paid**: ~$1.94/month for shared-cpu-1x with 256MB RAM
- [Pricing details](https://fly.io/docs/about/pricing/)

### Vercel (Frontend)
- **Free tier**: Unlimited personal projects with bandwidth limits
- **Paid**: Pro tier starts at $20/month
- [Pricing details](https://vercel.com/pricing)

### Groq API
- **Free tier**: Generous rate limits for development
- **Paid**: Pay-as-you-go pricing
- [Pricing details](https://groq.com/pricing)

## Security Checklist

Before going to production:

- [ ] Change `DEBUG` to `False` in backend
- [ ] Use strong `SECRET_KEY` (32+ random characters)
- [ ] Set restrictive `ALLOWED_ORIGINS`
- [ ] Enable HTTPS (automatic with Fly.io and Vercel)
- [ ] Review API rate limits
- [ ] Add input validation
- [ ] Implement request logging
- [ ] Set up monitoring/alerts
- [ ] Regular dependency updates
- [ ] Backup strategy for user data

## Next Steps

- Set up monitoring (Sentry, LogRocket, etc.)
- Add analytics (Google Analytics, PostHog, etc.)
- Implement rate limiting
- Add more features to your agent
- Scale based on usage

## Support

- Fly.io: https://community.fly.io/
- Vercel: https://vercel.com/support
- Project issues: Open an issue on GitHub

---

Congratulations! Your MooAgent is now live! 🎉
