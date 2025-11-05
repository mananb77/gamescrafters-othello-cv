# Deployment Guide - Othello CV Demo Website

Complete guide for deploying the Othello Computer Vision demo website to GitHub Pages with automated deployment.

---

## Table of Contents
- [Quick Deployment](#quick-deployment)
- [GitHub Pages Setup](#github-pages-setup)
- [Automated Deployment](#automated-deployment)
- [Custom Domain (Optional)](#custom-domain-optional)
- [Troubleshooting](#troubleshooting)
- [Local Testing](#local-testing)

---

## Quick Deployment

### Prerequisites
- GitHub repository created
- Code pushed to `main` branch
- GitHub Pages enabled

### Deployment Steps (5 minutes)

**1. Push Code to GitHub**
```bash
git add .
git commit -m "Add demo website and deployment workflow"
git push origin main
```

**2. Enable GitHub Pages**
1. Go to your GitHub repository
2. Click `Settings` → `Pages`
3. Under "Build and deployment":
   - **Source:** Deploy from a branch
   - **Branch:** Select `main`
   - **Folder:** Select `/docs`
4. Click `Save`

**3. Wait for Deployment**
- GitHub Actions will automatically build and deploy
- Check progress: `Actions` tab in your repository
- Website will be live at: `https://[username].github.io/[repo-name]/`

**That's it!** Your website is now live.

---

## GitHub Pages Setup

### Method 1: Deploy from `/docs` Folder (Recommended)

This method uses the `/docs` folder directly without additional build steps.

**Steps:**
1. Repository Settings → Pages
2. Source: **Deploy from a branch**
3. Branch: **main**
4. Folder: **/docs**
5. Save

**Advantages:**
- Simple setup
- No build process needed
- Fast deployment
- Static files served directly

### Method 2: GitHub Actions (Automated)

Uses the provided `.github/workflows/deploy.yml` for automated deployment.

**Steps:**
1. Ensure `.github/workflows/deploy.yml` exists in your repository
2. Repository Settings → Pages
3. Source: **GitHub Actions**
4. Save

**Workflow Configuration:**
```yaml
# .github/workflows/deploy.yml is already configured!
# - Triggers on push to main branch
# - Can be manually triggered
# - Auto-deploys to GitHub Pages
```

**Advantages:**
- Automated deployment on every push
- Can add build/optimization steps
- Better control over deployment process

---

## Automated Deployment

### How It Works

The GitHub Actions workflow (`.github/workflows/deploy.yml`) automatically:

1. **Triggers** when code is pushed to `main` branch
2. **Checks out** the repository code
3. **Sets up** GitHub Pages environment
4. **Builds** the site from `/docs` folder
5. **Deploys** to GitHub Pages hosting

### Workflow File Structure

```yaml
name: Deploy Othello CV Demo to GitHub Pages

on:
  push:
    branches: ["main"]
  workflow_dispatch:

jobs:
  build:
    # Builds the site from docs/ folder
  deploy:
    # Deploys to GitHub Pages
```

### Manual Deployment Trigger

You can also manually trigger deployment:

1. Go to `Actions` tab in GitHub
2. Select "Deploy Othello CV Demo to GitHub Pages"
3. Click `Run workflow`
4. Select `main` branch
5. Click `Run workflow`

### Monitoring Deployment

**Check deployment status:**
1. Go to `Actions` tab
2. View running/completed workflows
3. Click on a workflow to see detailed logs

**Deployment typically takes:**
- Build: ~30 seconds
- Deploy: ~30 seconds
- **Total:** ~1 minute

---

## Custom Domain (Optional)

### Using a Custom Domain

If you have a custom domain (e.g., `demo.yoursite.com`):

**1. Configure DNS**

Add a CNAME record in your DNS provider:
```
Type:  CNAME
Name:  demo (or subdomain of your choice)
Value: [username].github.io
TTL:   3600
```

**2. Configure GitHub Pages**

1. Repository Settings → Pages
2. Custom domain: Enter `demo.yoursite.com`
3. Check **Enforce HTTPS** (recommended)
4. Save

**3. Add CNAME File**

Create `docs/CNAME` file:
```
demo.yoursite.com
```

**4. Wait for DNS Propagation**
- Can take 24-48 hours
- Check status: https://www.whatsmydns.net/

---

## Troubleshooting

### Common Issues

#### Issue 1: 404 Page Not Found

**Symptoms:**
- Website shows 404 error
- `index.html` not loading

**Solutions:**
1. Verify `/docs` folder contains `index.html`
2. Check GitHub Pages settings → folder is set to `/docs`
3. Wait 2-3 minutes for deployment to complete
4. Clear browser cache and try again

#### Issue 2: Deployment Failed

**Symptoms:**
- Red X on GitHub Actions workflow
- Deployment fails in Actions tab

**Solutions:**
1. Click on failed workflow to view logs
2. Common causes:
   - Permission issues (check workflow permissions)
   - Invalid YAML syntax
   - Missing files
3. Fix the issue and push again

**Check Permissions:**
```yaml
# Ensure these permissions are in deploy.yml:
permissions:
  contents: read
  pages: write
  id-token: write
```

#### Issue 3: CSS/JS Not Loading

**Symptoms:**
- Website loads but no styling
- JavaScript not working

**Solutions:**
1. Check browser console for errors (F12)
2. Verify paths in `index.html`:
   - `href="css/custom.css"` (not `/css/custom.css`)
   - `src="js/main.js"` (not `/js/main.js`)
3. For custom domain, use absolute paths or configure baseurl
4. Clear browser cache (Ctrl+Shift+R)

#### Issue 4: Workflow Not Triggering

**Symptoms:**
- Push to main but no deployment
- No workflow showing in Actions

**Solutions:**
1. Verify `.github/workflows/deploy.yml` exists
2. Check file is named exactly `deploy.yml` (not `deploy.yaml`)
3. Ensure file is in correct directory
4. Check GitHub Actions are enabled:
   - Settings → Actions → Allow all actions

#### Issue 5: HTTPS Not Working

**Symptoms:**
- "Not Secure" in browser
- HTTP instead of HTTPS

**Solutions:**
1. Go to Settings → Pages
2. Check "Enforce HTTPS"
3. Wait 5-10 minutes for SSL certificate
4. If still not working, uncheck and re-check "Enforce HTTPS"

---

## Local Testing

### Test Before Deploying

**Method 1: Python Simple Server**

```bash
cd docs
python3 -m http.server 8000
```

Open: http://localhost:8000

**Method 2: Node.js http-server**

```bash
npm install -g http-server
cd docs
http-server
```

Open: http://localhost:8080

**Method 3: VS Code Live Server**

1. Install "Live Server" extension
2. Right-click `docs/index.html`
3. Select "Open with Live Server"

### Testing Checklist

Before deploying, verify:

- [ ] All sections load correctly
- [ ] Navigation links work
- [ ] Demo tabs switch properly
- [ ] Sample selection works
- [ ] Results display correctly
- [ ] Gallery filters function
- [ ] All external links open
- [ ] Responsive design works (mobile/tablet)
- [ ] Console has no errors (F12)
- [ ] All images load
- [ ] Smooth scrolling works

---

## Updating the Website

### Make Changes

1. Edit files in `docs/` folder:
   - `docs/index.html` - Main page
   - `docs/css/custom.css` - Styles
   - `docs/js/main.js` - Interactivity

2. Test locally (see Local Testing above)

3. Commit and push:
```bash
git add docs/
git commit -m "Update website: [description]"
git push origin main
```

4. GitHub Actions will automatically deploy
5. Changes live in ~1 minute

### Quick Updates

For small changes (text, links):
- Edit directly on GitHub
- Click "Commit changes"
- Auto-deploys immediately

---

## Advanced Configuration

### Adding Analytics

**Google Analytics:**

Add to `<head>` in `index.html`:
```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

### Adding More Pages

Create new pages in `docs/`:
```
docs/
├── index.html
├── about.html        # New page
├── contact.html      # New page
└── ...
```

Link from navigation:
```html
<a href="about.html">About</a>
```

### Optimizing Assets

**Compress Images:**
```bash
# Using ImageMagick
convert input.png -quality 85 output.png

# Using TinyPNG
https://tinypng.com/
```

**Minify CSS/JS:**
```bash
# Online tools
https://cssminifier.com/
https://javascript-minifier.com/
```

---

## Deployment Checklist

Before going live:

- [ ] Test all features locally
- [ ] Check responsive design
- [ ] Verify all links work
- [ ] Test on multiple browsers
- [ ] Optimize images
- [ ] Review content for typos
- [ ] Test GitHub Actions workflow
- [ ] Verify GitHub Pages settings
- [ ] Test deployed site
- [ ] Share URL with team

---

## Support Resources

### GitHub Pages Documentation
- [GitHub Pages Docs](https://docs.github.com/en/pages)
- [Custom Domains](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site)
- [GitHub Actions](https://docs.github.com/en/actions)

### Community Support
- [GitHub Pages Forum](https://github.community/c/pages/44)
- [Stack Overflow - GitHub Pages](https://stackoverflow.com/questions/tagged/github-pages)

### Project Resources
- Main README: [README.md](README.md)
- Demo Instructions: [DEMO_INSTRUCTIONS.md](DEMO_INSTRUCTIONS.md)
- Test Report: [TEST_REPORT.md](TEST_REPORT.md)

---

## Summary

✅ **Deployment is now automated!**

**What happens when you push code:**
1. Code pushed to `main` branch
2. GitHub Actions workflow triggered
3. Website built from `/docs` folder
4. Deployed to GitHub Pages
5. Live at `https://[username].github.io/[repo-name]/`

**Typical deployment time:** ~1 minute

**No manual steps required** after initial setup!

---

**Need help?** Check the troubleshooting section or open an issue on GitHub.

**Website live?** Share the link with your team! 🚀
