# Subgrid Emulator Documentation Website

This directory contains the GitHub Pages website for the subgrid_emu package.

## Files

- `index.html` - Main webpage with complete documentation
- `styles.css` - Styling for the website (sleek, modern design)
- `script.js` - Interactive features (smooth scrolling, copy buttons, animations)
- `_config.yml` - GitHub Pages configuration

## Viewing Locally

To view the website locally, you can use Python's built-in HTTP server:

```bash
cd docs
python -m http.server 8000
```

Then open your browser to `http://localhost:8000`

## Deploying to GitHub Pages

1. Push the `docs` directory to your GitHub repository
2. Go to your repository settings on GitHub
3. Navigate to "Pages" in the left sidebar
4. Under "Source", select "Deploy from a branch"
5. Select the branch (e.g., `main`) and the `/docs` folder
6. Click "Save"

Your site will be available at: `https://nesar.github.io/subgrid_emu/`

## Features

The website includes:

- **Responsive Design**: Works on desktop, tablet, and mobile
- **Smooth Navigation**: Sticky navbar with smooth scrolling
- **Interactive Elements**: 
  - Copy-to-clipboard buttons for code blocks
  - Fade-in animations on scroll
  - Hover effects on cards
- **Comprehensive Documentation**:
  - Overview of the package
  - Available summary statistics
  - Installation instructions
  - Usage examples
  - Complete API reference
  - Citation information

## Customization

To customize the website:

- **Colors**: Edit CSS variables in `styles.css` (`:root` section)
- **Content**: Edit `index.html`
- **Interactivity**: Modify `script.js`

## Design Philosophy

The website follows a minimal, informative, sleek, and classy design:

- Clean typography with Inter and JetBrains Mono fonts
- Professional color scheme with blue accents
- Card-based layout for easy scanning
- Generous whitespace for readability
- Smooth animations for polish
