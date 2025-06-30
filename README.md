# Chen Group Homepage

This repository contains the source code for The Chen Group's homepage, built with Astro and deployed via GitHub Pages.

Live Site: https://TheChenGroup.github.io

[![Open in Codeflow](https://developer.stackblitz.com/img/open_in_codeflow.svg)](https:///pr.new/TheChenGroup/TheChenGroup.github.io)

## 📝 Content Management

### Page Structure

All pages are located at `src/pages`. Each page is a [MDX](https://mdxjs.com/) document. MDX is similar to Markdown, but can import components from `src/components` directory for a more customized display.

Folder structure in `src/`:

- `images/`
  - `members/`: Individual headshots (3:4 aspect ratio)
  - `photos/`: Group photos
  - `research/`: Research illustrations
- `pages/`
  - `index.mdx`: Home page ([Web Publisher](https://pr.new/github.com/TheChenGroup/TheChenGroup.github.io/edit/main/src/pages/index.mdx), [GitHub](https://github.com/TheChenGroup/TheChenGroup.github.io/edit/main/src/pages/index.mdx))
  - `research.mdx`: Research and important papers ([Web Publisher](https://pr.new/github.com/TheChenGroup/TheChenGroup.github.io/edit/main/src/pages/research.mdx), [GitHub](https://github.com/TheChenGroup/TheChenGroup.github.io/edit/main/src/pages/research.mdx))
  - `group.mdx`: Team members ([Web Publisher](https://pr.new/github.com/TheChenGroup/TheChenGroup.github.io/edit/main/src/pages/group.mdx), [GitHub](https://github.com/TheChenGroup/TheChenGroup.github.io/edit/main/src/pages/group.mdx))
  - `publications.mdx`: List of research papers ([Web Publisher](https://pr.new/github.com/TheChenGroup/TheChenGroup.github.io/edit/main/src/pages/publication.mdx), [GitHub](https://github.com/TheChenGroup/TheChenGroup.github.io/edit/main/src/pages/publication.mdx))
  - `teaching.mdx`: Courses information ([Web Publisher](https://pr.new/github.com/TheChenGroup/TheChenGroup.github.io/edit/main/src/pages/teaching.mdx), [GitHub](https://github.com/TheChenGroup/TheChenGroup.github.io/edit/main/src/pages/teaching.mdx))
  - `photos.mdx`: Group photos ([Web Publisher](https://pr.new/github.com/TheChenGroup/TheChenGroup.github.io/edit/main/src/pages/photos.mdx), [GitHub](https://github.com/TheChenGroup/TheChenGroup.github.io/edit/main/src/pages/photos.mdx))

You can click the "Web Publisher" link in Chromium-based browser to edit a single file with live preview. To edit multiple files, please use [Codeflow](https:///pr.new/TheChenGroup/TheChenGroup.github.io). Alternatively, you can directly edit the files with GitHub UI by clicking the "GitHub" link.

### Adding a New Paper to Publication List

This project uses a custom format to store publication information. The easiest way is to use GitHub workflows. Go to [Add new publication workflow page](https://github.com/TheChenGroup/TheChenGroup.github.io/actions/workflows/new-paper.yml), click on "Run workflow", and enter the DOI (e.g. `10.1038/s43588-024-00730-4`). A new pull request will automatically be created.

Alternatively, you can use the following command to generate it from DOI:

```bash
python scripts/doi2yaml.py 10.1038/s43588-024-00730-4
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

Stackblitz provides a seamless way to run Node.js programs directly in your browser. To get started, click the button below (Chrome browser is recommended):

[![Open in Codeflow](https://developer.stackblitz.com/img/open_in_codeflow.svg)](https:///pr.new/TheChenGroup/TheChenGroup.github.io)

This will launch an Online VS Code editor where you can make your changes. Follow these steps to set up and contribute:

1. **Log in to GitHub**:
   After opening the project in Stackblitz, click the GitHub icon on the sidebar to authenticate your GitHub account.

2. **Install extensions**:
   For a smoother workflow, consider installing the following extensions in the editor:
   - **Astro**: Provides support for Astro framework features.
   - **MDX**: Enhances editing capabilities for MDX files.

3. **Make Your Changes**:
   Modify the files as needed. After that, go to the Git sidebar to create a new branch and commit your changes. Please don't commit the `pnpm-lock.yaml` file. Remember to commit and push your changes before closing the page.

4. **Create a Pull Request**:
   Open the command palette (accessible via `Ctrl/Cmd + Shift + P`) and type `> create pull request`. Follow the prompts to submit your changes.

5. **Verify Your Pull Request**:
   If everything is set up correctly, your pull request will appear in the GitHub UI:

   ![PR Screenshot](https://github.com/user-attachments/assets/6e09f59a-c055-45b9-812a-fb7b4451db01)

6. **Await Review and Approval**:
   The pull request will be reviewed by the repository admins. Once approved, it will be merged into the main branch.

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
