# GitHub Pages Setup Guide

This guide explains how to enable GitHub Pages for the subgrid_emu package documentation website.

## Important: Repository Structure

The `subgrid_emu` directory is part of the `Hydro_runs` repository. Therefore, the GitHub Pages URL will be:

```
https://nesar.github.io/Hydro_runs/subgrid_emu/
```

NOT `https://nesar.github.io/subgrid_emu/` (which would require a separate repository).

## Prerequisites

- The `subgrid_emu/docs/` directory with the website files must be pushed to the Hydro_runs repository
- You need admin access to the repository settings

## Setup Steps

### 1. Push the Documentation to GitHub

Make sure all files in the `subgrid_emu/docs/` directory are committed and pushed:

```bash
cd /path/to/Hydro_runs
git add subgrid_emu/docs/
git commit -m "Add GitHub Pages documentation website for subgrid_emu"
git push origin main
```

### 2. Enable GitHub Pages

1. Go to your repository on GitHub: `https://github.com/nesar/Hydro_runs`

2. Click on **Settings** (in the repository menu)

3. In the left sidebar, click on **Pages**

4. Under **Source**:
   - Select **Deploy from a branch**
   - Choose your branch (typically `main` or `master`)
   - Select the **/ (root)** folder (NOT /docs since docs is inside subgrid_emu)
   - Click **Save**

5. GitHub will start building your site. This may take a few minutes.

### 3. Access Your Website

Once deployed, your website will be available at:

```
https://nesar.github.io/Hydro_runs/subgrid_emu/
```

The full path includes `/subgrid_emu/` because the docs are in a subdirectory.

## Alternative: Separate Repository (Recommended for Production)

For a cleaner URL like `https://nesar.github.io/subgrid_emu/`, you should:

1. Create a new repository called `subgrid_emu`
2. Move the subgrid_emu package to that repository
3. Then enable GitHub Pages from the `/docs` folder in that repository

This would give you the URL: `https://nesar.github.io/subgrid_emu/`

## Updating the Website

To update the website:

1. Edit the files in the `subgrid_emu/docs/` directory
2. Commit and push your changes:
   ```bash
   git add subgrid_emu/docs/
   git commit -m "Update documentation website"
   git push origin main
   ```
3. GitHub Pages will automatically rebuild and deploy the updated site (usually within a few minutes)

## Troubleshooting

### Site Not Loading

- Wait a few minutes after enabling GitHub Pages - initial deployment can take time
- Check that the `subgrid_emu/docs/` folder exists in your repository
- Verify that `index.html` exists in the `subgrid_emu/docs/` folder
- Make sure you're accessing the correct URL with `/subgrid_emu/` in the path

### 404 Error

- Ensure the branch and folder are correctly selected in GitHub Pages settings
- Check that all files are properly committed and pushed
- Verify the URL includes the subdirectory: `/Hydro_runs/subgrid_emu/`

### Styling Issues

- Clear your browser cache
- Check browser console for any errors
- Verify that `styles.css` and `script.js` are in the `subgrid_emu/docs/` folder

## Local Development

To preview the website locally before pushing:

```bash
cd subgrid_emu/docs
python -m http.server 8000
```

Then open `http://localhost:8000` in your browser.

## File Structure

```
Hydro_runs/
└── subgrid_emu/
    ├── docs/
    │   ├── index.html       # Main webpage
    │   ├── styles.css       # Styling (dark theme)
    │   ├── script.js        # Interactive features
    │   ├── _config.yml      # GitHub Pages configuration
    │   └── README.md        # Documentation about the docs
    ├── subgrid_emu/         # Python package
    ├── setup.py
    └── README.md
```

## Support

For issues with the website or GitHub Pages setup:

- Check the [GitHub Pages documentation](https://docs.github.com/en/pages)
- Open an issue in the repository
- Contact the package maintainer
