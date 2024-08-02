<p align="center">
  <img src="images/voxrad_logo.jpg" alt="VOXRAD Logo" />
</p>

# VOXRAD 🚀

VOXRAD is a voice transcription application for radiologists leveraging voice transcription models and large language models to restructure and format reports as per predefined user instruction templates.

**Welcome to The VOXRAD App! 🌟 🎙**

This application leverages the power of generative AI to efficiently transcribe and format radiology reports from audio inputs. Designed for radiologists and radiology residents, it transforms spoken content into structured, readable reports.

**Etymology:**

-  **VoxRad** /vɒks-ræd/ *noun*

1. A portmanteau derived from **Vox** (Latin for *voice*) and **Rad** (*radiology*), symbolizing the fusion of voice recognition with radiology. Represents the integration of voice recognition technology with radiological imaging and reporting.

2. An AI-driven app transforming radiology reporting through voice transcription, enhancing accuracy in medical documentation.

## Features ✨

- 🎤 Voice transcription

- 📝 Report formatting

- 🤖 Integration with large language models

- ⚙️ Customizable templates
- 📈 Potential to extend the application for dictating other structured notes (discharge notes, OT notes or legal paperwork)


## Installation 💻

To install VOXRAD, follow these steps:

1. Download the `.app` file for Mac or the `.exe` file for Windows from the [releases](https://github.com/drankush/voxrad/releases).

## Usage 🛠️

### Settings ⚙️
#### General Tab

- Click and choose the working directory. Here your encrypted keys, templates, and last recorded audio file will be kept.

- There is a **Templates** folder that you can open by clicking the button **Open Templates Folder** in the General tab of settings. Here you can place `.txt` and `.md` template instruction files for various reports like HRCT Thorax, CECT Abdomen. Do trial and error to figure out how much instruction is required for your desired performance by the chosen model. 
- You can insert a dictionary of words separated by commas between `[correct spellings] word1, word2, word3 [correct spellings]` inside your template `.txt` and `.md` files. These will be extracted and passed to the voice model to focus on specific words that can be mistaken.

#### Transcription Model Tab 🎙️

- Insert the OpenAI compatible  **Base URL** and **API Key** here and press **Fetch Models**. The application only fetches **Whisper** models. To ask for support for other models, [suggest enhancement](https://github.com/drankush/voxrad/issues?q=label%3Aenhancement+).
- Click **Save Settings** to save your selected model and Base URL (these are not encrypted).

#### Text Model Tab 📝

- Use any OpenAI compatible API key and Base URL. 
- You can directly use any OpenAI compatible API. Read docs of your API provider.  For instance, use Base URL for
  

  - [OpenAI](https://platform.openai.com/docs/api-reference/introduction): ```https://api.openai.com/v1/```
  - [Gemini](https://github.com/PublicAffairs/openai-gemini): ```https://my-openai-gemini-henna.vercel.app/v1```
    <br>❗️Cannot fetch models, model choice is set to Gemini-1.5-pro.</br>
  - [Groq](https://console.groq.com/docs/openai): ```https://api.groq.com/openai/v1```
  - [Ollama](https://ollama.com/blog/openai-compatibility): ```http://localhost:11434/v1```
      
- Search github for repositories that support transforming your provider to OpenAI compatible API. Please deploy your own instance. This way, you can keep your API key secure.</br>
  
- Click **Fetch Model** to see the available models and choose one.

- Click **Save Settings** to save your selected model and Base URL (these are not encrypted).

- You can encrypt and save your keys by giving a password in the settings. The application will ask for this password every time you open it to unlock the API keys for the transcription model and text model separately.

### Main App Window 🎙

- Press the **Record 🔴** button and start dictating your report, keep it around max 15 minutes, as the file sent limit is 25 MB (the application will try to reduce the bitrate to accommodate this size for longer audios). You will see a waveform while the audio is recorded.

- Press **Stop ⬜️** to stop recording. Your audio will be processed.

- The final formatted and structured report will be automatically posted on your clipboard. You can then directly paste (Ctrl/Cmd + V) it into your application, word processor, or PACS.

## Documentation 📚

Read comprehensive VOXRAD documentation [here](http://voxrad.gitbook.io/voxrad).

## Contributing 🌟

Contributions are welcome! Please read the [contributing guidelines](CONTRIBUTING.md) before getting started.

## License 📜

This project is licensed under the GPLv3 License - see the [LICENSE](LICENSE) file for details.

## Support 🐞

To report bugs or issues, please follow [this guide](https://github.com/drankush/voxrad/blob/main/contributing.md#reporting-bugs) on how to report bugs.

## Contact 📧

For any other questions, support or appreciation, please contact [Dr. Ankush](mailto:voxrad@drankush.com).

## Disclaimer 🚨

This is a pure demonstrative application for the capabilities of AI and may not be compliant with local regulations of handling sensitive and private data. This is not intended for any diagnostic and clinical use. Please read the terms of use of the API keys that you will be using.

- The application is not intended to replace professional medical advice, diagnosis, or treatment.
- Users must ensure they comply with all relevant local laws and regulations when using the application, especially concerning data privacy and security.
- Users are advised to locally host voice transcription and text models and use its endpoints for sensitive data.
- The developers are not responsible for any misuse of the application or any data breaches that may occur.
- The application does not encrypt data by default; users must take additional steps to secure their data.
- Always verify the accuracy of the transcriptions and generated reports manually.

