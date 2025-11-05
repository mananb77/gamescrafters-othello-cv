# Othello CV Demo Website

This directory contains the demo website for the Othello Computer Vision project.

## Structure

```
docs/
├── index.html              # Main website page
├── css/
│   └── custom.css         # Custom styles
├── js/
│   └── main.js            # Interactive JavaScript
├── assets/
│   ├── videos/            # Sample processed videos
│   ├── images/            # Sample outputs, screenshots
│   └── data/
│       └── test-results.json  # Test metrics
├── _config.yml            # GitHub Pages configuration
└── README.md              # This file
```

## Local Development

### Run Locally

**Option 1: Python**
```bash
cd docs
python3 -m http.server 8000
```
Visit: http://localhost:8000

**Option 2: Node.js**
```bash
npm install -g http-server
cd docs
http-server
```
Visit: http://localhost:8080

**Option 3: VS Code Live Server**
- Install Live Server extension
- Right-click `index.html`
- Select "Open with Live Server"

## Deployment

This website automatically deploys to GitHub Pages when code is pushed to the `main` branch.

**Setup:**
1. Repository Settings → Pages
2. Source: Deploy from a branch
3. Branch: main, Folder: /docs
4. Save

See [DEPLOYMENT.md](../DEPLOYMENT.md) for complete deployment guide.

## Features

- ✨ Modern, responsive design with Tailwind CSS
- 🎨 Interactive demo with mock file upload
- 📊 Real test results and performance metrics
- 🖼️ Sample outputs gallery
- 📚 Complete documentation
- 🚀 Auto-deployment with GitHub Actions

## Customization

### Update Content
- Edit `index.html` for page content
- Modify `css/custom.css` for styling
- Update `js/main.js` for functionality

### Add Media
Place files in:
- `assets/images/` - Images
- `assets/videos/` - Videos
- `assets/data/` - Data files

### Add Pages
Create new HTML files in this directory and link from navigation.

## Technologies Used

- **Tailwind CSS** - Utility-first CSS framework
- **Font Awesome** - Icons
- **Google Fonts** - Inter font family
- **Vanilla JavaScript** - No framework dependencies

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers

## License

Part of the GamesCrafters Othello CV project.
Built at UC Berkeley under Professor Dan Garcia.

---

**Questions?** See [DEPLOYMENT.md](../DEPLOYMENT.md) or [DEMO_INSTRUCTIONS.md](../DEMO_INSTRUCTIONS.md)
