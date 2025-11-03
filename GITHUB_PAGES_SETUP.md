# GitHub Pages Setup Guide

This guide explains how to enable GitHub Pages for the subgrid_emu package documentation website.

## Prerequisites

- The `docs/` directory with the website files must be pushed to your GitHub repository
- You need admin access to the repository settings

## Setup Steps

### 1. Push the Documentation to GitHub

Make sure all files in the `docs/` directory are committed and pushed:

```bash
cd /path/to/subgrid_emu
git add docs/
git commit -m "Add GitHub Pages documentation website"
git push origin main
```

### 2. Enable GitHub Pages

1. Go to your repository on GitHub: `https://github.com/nesar/subgrid_emu`

2. Click on **Settings** (in the repository menu)

3. In the left sidebar, click on **Pages**

4. Under **Source**:
   - Select **Deploy from a branch**
   - Choose your branch (typically `main` or `master`)
   - Select the `/docs` folder
   - Click **Save**

5. GitHub will start building your site. This may take a few minutes.

### 3. Access Your Website

Once deployed, your website will be available at:

```
https://nesar.github.io/subgrid_emu/
```

You can find the exact URL in the GitHub Pages settings after deployment.

## Updating the Website

To update the website:

1. Edit the files in the `docs/` directory
2. Commit and push your changes:
   ```bash
   git add docs/
   git commit -m "Update documentation website"
   git push origin main
   ```
3. GitHub Pages will automatically rebuild and deploy the updated site (usually within a few minutes)

## Custom Domain (Optional)

If you want to use a custom domain:

1. In the GitHub Pages settings, enter your custom domain in the **Custom domain** field
2. Add the appropriate DNS records with your domain provider
3. Enable **Enforce HTTPS** for security

## Troubleshooting

### Site Not Loading

- Wait a few minutes after enabling GitHub Pages - initial deployment can take time
- Check that the `docs/` folder exists in your repository
- Verify that `index.html` exists in the `docs/` folder

### 404 Error

- Ensure the branch and folder are correctly selected in GitHub Pages settings
- Check that all files are properly committed and pushed

### Styling Issues

- Clear your browser cache
- Check browser console for any errors
- Verify that `styles.css` and `script.js` are in the `docs/` folder

## Website Features

The documentation website includes:

- **Responsive Design**: Optimized for desktop, tablet, and mobile devices
- **Interactive Navigation**: Smooth scrolling and active section highlighting
- **Code Examples**: Syntax-highlighted code blocks with copy-to-clipboard functionality
- **Comprehensive Documentation**: 
  - Package overview
  - Available summary statistics
  - Installation instructions
  - Usage examples
  - Complete API reference
  - Citation information

## Local Development

To preview the website locally before pushing:

```bash
cd docs
python -m http.server 8000
```

Then open `http://localhost:8000` in your browser.

## File Structure

```
docs/
├── index.html       # Main webpage
├── styles.css       # Styling
├── script.js        # Interactive features
├── _config.yml      # GitHub Pages configuration
└── README.md        # Documentation about the docs
```

## Support

For issues with the website or GitHub Pages setup:

- Check the [GitHub Pages documentation](https://docs.github.com/en/pages)
- Open an issue in the repository
- Contact the package maintainer
