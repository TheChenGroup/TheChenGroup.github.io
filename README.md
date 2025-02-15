# Chen Group Homepage

This repository contains the source code for The Chen Group's homepage, built with Astro and deployed via GitHub Pages.

Live Site: https://TheChenGroup.github.io

[![Open in Codeflow](https://developer.stackblitz.com/img/open_in_codeflow.svg)](https:///pr.new/TheChenGroup/TheChenGroup.github.io)

## 📝 Content Management

### Page Structure

All pages are located at `src/pages`. Each page is a [MDX](https://mdxjs.com/) document. MDX is similar to Markdown, but can import components from `src/components` directory for a more customized display.

```
src
├── images
│   ├── members          # Individual headshots (3:4 aspect ratio)
│   ├── photos           # Group photos
│   └── research         # Research illustrations
└── pages
    ├── group.mdx        # Team members
    ├── index.mdx        # Home page
    ├── photos.mdx       # Group photos
    ├── publications.mdx # List of research papers
    ├── research.mdx     # Research and important papers
    └── teaching.mdx     # Courses information
```

### Adding a New Paper to Publication List

This project uses a custom format to store publication information. Use the following command to generate it from DOI:

```bash
node scripts/doi2yaml.mjs 10.1038/s43588-024-00730-4
```

Example output:

```yaml
- title: >-
    Spin-symmetry-enforced solution of the many-body Schrödinger equation with a
    deep neural network
  doi: 10.1038/s43588-024-00730-4
  authors:
    - Zhe Li
    - Zixiang Lu
    - Ruichen Li
    - Xuelan Wen
    - Xiang Li
    - Liwei Wang
    - Ji Chen
    - Weiluo Ren
  journal: Nat Comput Sci
  volume: "4"
  page: 910-919
  year: 2024
```

Paste the output YAML to `src/pages/publications.mdx` frontmatter.

### Adding a New Research Highlight

The "Research Highlights" section on the home page (`src/pages/index.mdx`) showcases the most recent research highlight paper, serving a similar function to a news feature. To incorporate a new highlight, follow these steps:

1. Add an image to the `images/research/` folder, using a naming convention such as `2025-research-short-name.avif`. AVIF images are preferred due to their small size.
2. Update the existing highlight directly within `src/pages/index.mdx` with the new information.
3. Duplicate the details of the new research highlight in `src/pages/research.mdx`.

### Managing Team Members

1. Add headshot to `src/images/members/` (example filename: `san.zhang.avif`)
2. Update `src/pages/group.mdx`:

```html
<Member
  image="members/san.zhang.avif"
  name="姓名"
  nameEn="English name"
  year="2023"
  email="1234@pku.edu.cn"
  interest="QMC"
/>
```

## 🌐 Online Development Guide

The online approach is simpler but is not as flexible as the local version.

### Option 1: Directly edit files with GitHub UI

You can only edit one file at a time using this approach. This is best suited for small edits on the texts.

### Option 2: Stackblitz

Stackblitz allows you to run Node.js programs directly in your browser. Click the following button and login with your GitHub account:

[![Open in Codeflow](https://developer.stackblitz.com/img/open_in_codeflow.svg)](https:///pr.new/TheChenGroup/TheChenGroup.github.io)

This will start an Online VS Code editor. You can install the "Astro" and "MDX" for better editing experiences. After making changes, remember to create a new pull request.

## 🖥️ Local Development Guide

### 1. Environment Setup

#### 1.1 Install Node.js

For Windows:

1. Download installer from [nodejs.org](https://nodejs.org)
2. Run the installer (check "Add to PATH" during installation)
3. Verify installation in Command Prompt:

```bash
node --version
# Should show v22.x or higher
```

For macOS:

```bash
# Using Homebrew (recommended)
brew install node
# Or download directly from nodejs.org
```

#### 1.2 Install pnpm Package Manager

After Node.js installation:

```bash
# Enable corepack
corepack enable
# Verify pnpm installation
pnpm --version
# Should show 10.x or higher
# If you get "command not found", try:
# npm install -g corepack
```

### 2. First-Time Setup

#### 2.1 Clone Repository

```bash
git clone https://github.com/TheChenGroup/TheChenGroup.github.io.git
cd TheChenGroup.github.io
```

#### 2.2 Configure Registry

```bash
# For faster downloads in China
pnpm config set registry http://mirrors.cloud.tencent.com/npm/
```

#### 2.3 Install Dependencies

```bash
pnpm install
# Expected successful output:
#  Packages: +X
# +++ X
# Progress: resolved X, reused X, downloaded X, added X
# Done
```

#### 2.4 Editor setup

While you can use any editors you like, VS Code has the best support for Astro and MDX editing. Simply download the "Astro" and "MDX" extension and you are ready to go.

#### 2.5 Git setup

Make sure you have configured Git. You can follow [GitHub documentation](https://docs.github.com/en/get-started/getting-started-with-git/set-up-git) or ask your favorite AI.

### 3. Running Local Server

#### 3.1 Start Development Mode

```bash
pnpm dev --open
```

What happens:

1. Starts local server at `http://localhost:4321`
2. Automatically opens browser
3. Watches for file changes (save to see updates)

#### 3.2 Production Preview

Optionally, build the page and view the production version:

```bash
# Build optimized version
pnpm build
# Preview production build
pnpm preview
# Now visit http://localhost:4321
```

### 4. Make and Upload Your Changes

All changes should be pushed to a separate branch. Therefore, before making changes, run the following command to create and checkout to a new branch.

```bash
git checkout -b your-branch-name  # Change the branch name!
```

After making the changes, use `git add .` to add the changes and `git commit -m 'your message'` to create a commit. Run the following command to upload:

```bash
git push -u origin your-branch-name  # Change the branch name!
```

After that, navigate to GitHub web UI to create a pull request.
