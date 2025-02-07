<p align="center">
  <img src="images/voxrad_logo.jpg" alt="VOXRAD Logo" />
</p>

<div align="center">
  
[![Python Badge](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff&style=for-the-badge)](#)
[![FFmpeg Badge](https://img.shields.io/badge/FFmpeg-007808?logo=ffmpeg&logoColor=fff&style=for-the-badge)](https://github.com/drankush/voxrad/blob/main/docs/FFmpeg.md)
[![GitBook Badge](https://img.shields.io/badge/GitBook-BBDDE5?logo=gitbook&logoColor=000&style=for-the-badge)](https://voxrad.gitbook.io/voxrad)

[![Release](https://img.shields.io/github/v/release/drankush/voxrad?include_prereleases&color=blue)](https://github.com/drankush/voxrad/releases)
[![License](https://flat.badgen.net/badge/license/GPLv3/green?icon=github)](https://github.com/drankush/voxrad/blob/main/LICENSE)
[![Python Version](https://flat.badgen.net/badge/python/3.11%20|%203.12/blue?icon=github)](#)

[![Open Issues](https://img.shields.io/github/issues/drankush/voxrad.svg?color=orange)](https://github.com/drankush/voxrad/issues)
[![Closed Issues](https://img.shields.io/github/issues-closed/drankush/voxrad.svg?color=red)](https://github.com/drankush/voxrad/issues?q=is%3Aissue+is%3Aclosed)


[![Apple](https://flat.badgen.net/badge/icon/apple?icon=apple&label)](https://github.com/drankush/VoxRad/releases/download/v0.3.0-beta/VoxRad_macOS_v0.3.0-beta.zip)
[![Windows](https://flat.badgen.net/badge/icon/windows?icon=windows&label)](https://github.com/drankush/VoxRad/releases/download/v0.1.0-alpha/VoxRad_winOS_v0.1.0-alpha.zip)


</div>

# 🚀 VOXRAD 

VOXRAD is a voice transcription application for radiologists leveraging voice transcription and large language models to restructure and format reports as per predefined user instruction templates.

**Welcome to The VOXRAD App! 🌟 🎙**

This application leverages the power of generative AI to efficiently transcribe and format radiology reports from audio inputs. Designed for radiologists and radiology residents, it transforms spoken content into structured, readable reports.

**Etymology:**

-  **VoxRad** /vɒks-ræd/ *noun*

1. A portmanteau derived from **Vox** (Latin for *voice*) and **Rad** (*radiology*), symbolizing the fusion of voice recognition with radiology. Represents the integration of voice recognition technology with radiological imaging and reporting.

2. An AI-driven app transforming radiology reporting through voice transcription, enhancing accuracy in medical documentation.

## ✨ Features 

- 🎤 Voice transcription
- 📝 Report formatting
- 🤖 Integration with large language models
- ⚙️ Customizable templates
- 📈 Potential to extend the application for dictating other structured notes (discharge notes, OT notes or legal paperwork)

## 🏗️ Architecture

<p align="center">
<img src="images/voxrad_architecture.png" alt="VOXRAD Logo" />
</p>
<p align="center">
<i>Modified figure from Ankush et al. for v0.4.0-beta [1]</i>
</p>

## 🛠️ Getting Set Up

### 💻 Installation 

- Download the `.app` file for Mac or the `.exe` file for Windows from the [releases](https://github.com/drankush/voxrad/releases).

### 🔄 Understanding Workflow
VOXRAD uses two ways to transcribe audio to report.

- Use a combination of using a transcription model to first transcribe audio and then format and restructure the transcript using instruction template.
- Use a multimodal model to directly input the audio and instruction template to provide output (experimental).

Read more about the supported models [here](https://voxrad.gitbook.io/voxrad/fundamentals/getting-set-up/understanding-workflow#supported-llms).

### 📄 Customizing Templates and Guidelines

- Click ⚙️ Settings button at bottom right corner of the application interface.

  -  In the first Tab  🛠 General click Browse and select your desired working directory. 

  -  Here your templates files (predefined CoT-like systematic instructions such as HRCT_Thorax.txt, CT_Head.txt etc.) and guidelines (such as BIRADS.md, TIRADS.md, PIRADS.md etc.) will be kept.

Read more about [Customizing templates and guidelines](https://voxrad.gitbook.io/voxrad/fundamentals/getting-set-up/customizing-templates).


### 🔐 Managing Keys

- You can encrypt keys of transcription, text and multimodal models with password and even lock and unlock them while the application is in use. The application will ask for this password every time you start the applicaiton if encrypted keys are stored.
- In the "Base URL" field,  enter the base URL in OpenAI compatible format. Enter API key in the in the "API Key" field.
- You can use any OpenAI-compatible API key and Base URL and even locally deployed models which create OpenAI compatible endpoints.
- Click **Fetch Model** to see the available models and choose one.
- Click **Save Settings** to save your selected model and Base URL (these are not encrypted).
Read more about managing keys, best practices and troubleshooting [here](https://voxrad.gitbook.io/voxrad/fundamentals/getting-set-up/managing-keys).

### 🖥️ Running Models Locally

- There are [various ways](https://voxrad.gitbook.io/voxrad/running-models-locally) to run models locally and create OpenAI compatible endpoints which can then used with this application.
- You can also input OpenAI compatible Base URL and API key of [any remotely hosted service](https://voxrad.gitbook.io/voxrad/running-models-locally#remotely-hosted-models), however this is not recommended for sensitive data. For example: Groq: https://api.groq.com/openai/v1

## 🖱️ Usage 

### 🎙 Main App Window 

<!--
<p align="center">
  <img src="images/voxrad_gui.jpg" alt="VOXRAD Logo" />
</p>
-->



- Press the **Record 🔴** button and start dictating your report, keep it around max 15 minutes, as the file sent limit is 25 MB (the application will try to reduce the bitrate to accommodate this size for longer audios). You will see a waveform while the audio is recorded.

- Press **Stop ⬜️** to stop recording. Your audio will be processed.

- The final formatted and structured report will be automatically posted on your clipboard. You can then directly paste using secure paste shortcut key defined in the General Settings (in macOS) or  (Ctrl + V in windows application) it into your application, word processor, or PACS.

Read detailed documentation of generating a report [here](https://voxrad.gitbook.io/voxrad/user-guide/generating-a-report).

## 📚 Documentation 

Read comprehensive VOXRAD documentation [here](http://voxrad.gitbook.io/voxrad).

## 🌟 Contributing 

VOXRAD is a community-driven project, and we're grateful for the contributions of our team members. Read about the [key contributors](https://voxrad.gitbook.io/voxrad/support-and-contact/contributors). Please read the [contributing guidelines](CONTRIBUTING.md) before getting started.

## 📜 License 

This project is licensed under the GPLv3 License - see the [LICENSE](LICENSE) file for details. Till v0.3.0-beta, the application uses FFmpeg, which is licensed under the GNU General Public License (GPL) version 2 or later. For more details, please refer to the [documentation](https://github.com/drankush/voxrad/docs/FFmpeg.md/) in the repository.

## 🐞 Support 

To report bugs or issues, please follow [this guide](https://github.com/drankush/voxrad/blob/main/contributing.md#reporting-bugs) on how to report bugs.

### 📧 Contact 

For any other questions, support or appreciation, please contact [here](mailto:voxrad@drankush.com).

## 🚨 Disclaimer 

This is a pure demonstrative application for the capabilities of AI and may not be compliant with local regulations of handling sensitive and private data. This is not intended for any diagnostic and clinical use. Please read the terms of use of the API keys that you will be using.

- The application is not intended to replace professional medical advice, diagnosis, or treatment.
- Users must ensure they comply with all relevant local laws and regulations when using the application, especially concerning data privacy and security.
- Users are advised to locally host voice transcription and text models and use its endpoints for sensitive data.
- The developers are not responsible for any misuse of the application or any data breaches that may occur.
- The application does not encrypt data by default; users must take additional steps to secure their data.
- Always verify the accuracy of the transcriptions and generated reports manually.

## 🔖 Cite
```
@article{ankush_voxrad_2025,
	title = {{VoxRad}: {Building} an open-source locally-hosted radiology reporting system},
	volume = {119},
	issn = {0899-7071, 1873-4499},
	shorttitle = {{VoxRad}},
	url = {https://www.clinicalimaging.org/article/S0899-7071(25)00014-2/abstract},
	doi = {10.1016/j.clinimag.2025.110414},
	language = {English},
	urldate = {2025-02-01},
	journal = {Clinical Imaging},
	author = {Ankush, Ankush},
	month = mar,
	year = {2025},
	pmid = {39884167},
	note = {Publisher: Elsevier},
	keywords = {Artificial intelligence, Efficiency, Informatics, Natural language processing, Speech recognition software},
}
```
[1] Ankush A. (2025). VoxRad: Building an open-source locally-hosted radiology reporting system. Clinical imaging, 119, 110414. Advance online publication. https://doi.org/10.1016/j.clinimag.2025.110414 PMID:[39884167](https://pubmed.ncbi.nlm.nih.gov/39884167/)

