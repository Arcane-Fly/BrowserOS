<div align="center">

#

<img src="https://cdn.browseros.com/resources/banner.png" alt="backed-by-yc" >
<strong>(previously Nxtscape)</strong>

### Your browser, with AI superpowers 🚀

[![Discord](https://img.shields.io/badge/Discord-Join%20us-blue)](https://discord.gg/YKwjt5vuKr)
[![Twitter](https://img.shields.io/twitter/follow/browswerOS_ai?style=social)](https://twitter.com/browseros_ai)
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](LICENSE)
<a href="https://bit.ly/nxtscape">
  <img src="https://img.shields.io/badge/Download-macOS-black?style=flat&logo=apple&logoColor=white" alt="Download for macOS (beta)" />
</a>
<a href="https://bit.ly/browseros-windows">
  <img src="https://img.shields.io/badge/Download-Windows-0078D4?style=flat&logo=windows&logoColor=white" alt="Download for Windows (beta)" />
</a>
<a href="#linux-installation">
  <img src="https://img.shields.io/badge/Download-Linux-FCC624?style=flat&logo=linux&logoColor=black" alt="Available for Linux" />
</a>
<br />

<br />
<img src="resources/media/backed-by-yc.png" alt="backed-by-yc" width="140px">

</div>

🌐 EyeBrowserOS is an open-source agentic browser that runs AI agents locally. **Your privacy-first alternative to Perplexity Comet**.

🔒 Privacy first - use your own API keys or run local models with Ollama. Your data stays on your computer.

💡 Join our [Discord](https://discord.gg/YKwjt5vuKr) and help us build! Have feature requests? [Suggest anonymously here](https://dub.sh/nxtscape-feature-request).

## Quick start

1. Download and install EyeBrowserOS:
   - [macOS](https://bit.ly/nxtscape)
   - [Windows](https://cdn.browseros.com/win/EyeBrowserOS-installer.zip)
   - Linux: Build from source (see [Linux Installation](#linux-installation) below)
2. Import your Chrome data (optional)
3. Connect your AI provider (OpenAI, Anthropic, or local Ollama)
4. Start automating!

## What makes EyeBrowserOS special

<div align="center">
<img src="https://cdn.browseros.com/resources/usecase.png" alt="example-use-cases" width="85%">
</div>

## Features

- 🏠 Feels like home - same familiar interface as Google Chrome, works with all your extensions
- 🤖 AI agents that run on YOUR browser, not in the cloud
- 🔒 Privacy first - bring your own keys or use local models with Ollama. Your browsing history stays on your computer
- 🚀 Open source and community driven - see exactly what's happening under the hood
- 🤝 (coming soon) MCP store to one-click install popular MCPs and use them directly in the browser bar
- 🛡️ (coming soon) Built-in AI ad blocker that works across more scenarios!  

## Demos

### 🤖 AI Agents in Action ([watch video](https://storage.googleapis.com/felafax-public/nxtscape/nxtscape-agent-demo.mp4))

<div align="center">
<img src="resources/media/nxtscape-agent.gif" alt="AI Agents in Action" width="80%">
</div>

### 💬 Local AI Chat ([watch video](https://storage.googleapis.com/felafax-public/nxtscape/nxtscape-chat.mp4))

<div align="center">
<img src="resources/media/nxtscape-chat.gif" alt="Local AI Chat" width="80%">
</div>

### ⚡ Productivity Tools ([watch video](https://storage.googleapis.com/felafax-public/nxtscape/nxtscape-productivity.mp4))

<div align="center">
<img src="resources/media/nxtscape-productivity.gif" alt="Productivity" width="80%">
</div>

## Why we're building this

For the first time since Netscape in 1994, it feels like we can reimagine browsers from scratch. We saw how Cursor gave developers a 10x productivity boost, yet browsers feel stuck in the past.

You probably have 70+ tabs open right now. You're constantly fighting your browser instead of it helping you. Simple tasks like "order Tide Pods from my Amazon order history" should just work with AI agents.

We believe AI agents should automate your work locally and securely, not send your data to some search or ad company.

## How we compare

<details>
<summary><b>vs Chrome</b></summary>
<br>
While we're grateful for Google open-sourcing Chromium, but Chrome hasn't evolved much in 10 years. No AI features, no automation, no MCP support.
</details>

<details>
<summary><b>vs Brave</b></summary>
<br>
We love what Brave started, but they've spread themselves too thin with crypto, search, VPNs. We're laser-focused on AI-powered browsing.
</details>

<details>
<summary><b>vs Arc/Dia</b></summary>
<br>
Many loved Arc, but it was closed source. When they abandoned users, there was no recourse. We're 100% open source - fork it anytime!
</details>

<details>
<summary><b>vs Perplexity Comet</b></summary>
<br>
They're a search/ad company. Your browser history becomes their product. We keep everything local.
</details>

## Linux Installation

EyeBrowserOS now supports Linux! You can build it from source using our build system.

### Prerequisites

- Ubuntu 20.04+ / Debian 11+ / Fedora 35+ (or equivalent)
- Python 3.8+
- Git
- Chromium source code (see [build instructions](docs/BUILD.md))

### Quick Build

1. Clone the repository:

   ```bash
   git clone https://github.com/Arcane-Fly/EyeBrowserOS.git
   cd EyeBrowserOS
   ```

2. Install Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Build packages:

   ```bash
   python build/build.py --package --chromium-src /path/to/chromium/src --arch x64
   ```

### Package Formats

The build system creates multiple Linux package formats:

- **Tarball** (`.tar.gz`): Universal Linux package, works on any distribution
- **DEB package** (`.deb`): For Debian/Ubuntu systems with proper system integration
- **AppImage** (planned): Portable application format

### Installation

**From Tarball:**

```bash
tar -xzf EyeBrowserOS_*_linux.tar.gz
cd EyeBrowserOS
./browseros
```

**From DEB package:**

```bash
sudo dpkg -i browseros_*.deb
# Launch from applications menu or run 'browseros' in terminal
```

## Contributing

We'd love your help making EyeBrowserOS better!

- 🐛 [Report bugs](https://github.com/nxtscape/nxtscape/issues)
- 💡 [Suggest features](https://dub.sh/nxtscape-feature-request)
- 💬 [Join Discord](https://discord.gg/YKwjt5vuKr)
- 🐦 [Follow on Twitter](https://twitter.com/nxtscape)

## License

EyeBrowserOS is open source under the [AGPL-3.0 license](LICENSE).

---

<p align="center">
Built with ❤️ from San Francisco. Inspired by <a href="https://github.com/browser-use/browser-use">browser-use</a>, <a href="https://github.com/browserbase/stagehand">Stagehand</a>, <a href="https://github.com/nanobrowser/nanobrowser">Nanobrowser</a> and of course only possible because of <a href="https://github.com/chromium/chromium">Chromium</a>.
</p>
