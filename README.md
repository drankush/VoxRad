
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


## Installation 💻

To install VOXRAD, follow these steps:

1. Download the `.app` file for Mac or the `.exe` file for Windows from the [releases](https://github.com/drankush/voxrad/releases).

## Usage 🛠️

### Settings ⚙️
#### General Tab

- Click and choose the working directory. Here your encrypted keys, templates, and last recorded audio file will be kept.

- There is a **Templates** folder that you can open by clicking the button **Open Templates Folder** in the General tab of settings. Here you can place `.txt` and `.md` template instruction files for various reports like HRCT Thorax, CECT Abdomen. Do trial and error to figure out how much instruction is required for your desired performance by the chosen model. You can download sample templates from the template folder of this repository.

- You can insert a dictionary of words separated by commas between `[correct spellings] word1, word2, word3 [correct spellings]` inside your template `.txt` and `.md` files. These will be extracted and passed to the voice model to focus on specific words that can be mistaken.

#### Transcription Model Tab 🎙️

- Insert the Groq API key here. Get your Groq API key for transcription and text models from [Groq Console](https://console.groq.com/keys).

#### Text Model Tab 📝

- Use `https://api.groq.com/openai/v1` as the Base URL for the text model. For the text model, you can use any OpenAI compatible API key and Base URL.

- Click **Fetch Model** to see the available models and choose one.

- Click **Save Settings** to save your selected model and Base URL (these are not encrypted).

- You can encrypt and save your keys by giving a password in the settings. The application will ask for this password every time you open it to unlock the API keys for the transcription model and text model separately.

### Main App Window 🎙

- Press the **Record 🔴** button and start dictating your report, keep it around max 15 minutes, as the file sent limit is 25 MB (the application will try to reduce the bitrate to accommodate this size for longer audios). You will see a waveform while the audio is recorded.

- Press **Stop ⬜️** to stop recording. Your audio will be processed.

- The final formatted and structured report will be automatically posted on your clipboard. You can then directly paste (Ctrl/Cmd + V) it into your application, word processor, or PACS.

## Contributing 🌟

Contributions are welcome! Please read the [contributing guidelines](CONTRIBUTING.md) before getting started.

## License 📜

This project is licensed under the GPLv3 License - see the [LICENSE](LICENSE) file for details.

## Contact 📧

For any questions or support, please contact [Dr. Ankush](mailto:voxrad@drankush.com).

  

## Acknowledgments 🙏

- [Groq](https://groq.com) for providing API for Whisper-large-v3 voice-to-text model and LLaMA3-70b-8192 and other LLMs.
