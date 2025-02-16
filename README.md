# Screen Recorder with S3 Upload

A professional-grade screen recording application built with Python, featuring audio capture and automatic S3 upload capabilities.

## 🚀 Features

- 🎥 High-quality screen recording with audio capture
- ⏯️ Intuitive pause/resume functionality
- ⌨️ Keyboard shortcuts (F9, F10, F11)
- 🎚️ Real-time recording duration display
- ☁️ Automatic upload to Amazon S3
- 🔗 Instant shareable links (valid for 2 minutes)
- 📝 Built-in logging system
- 🎨 Modern GUI using ttkbootstrap

## 🛠️ Prerequisites

- Python 3.8 or higher
- FFmpeg installed and added to system PATH
- AWS account with S3 access
- Windows 10/11 (for audio capture)

## 📦 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/screen-recorder.git
cd screen-recorder
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Configure AWS credentials:
```bash
# Option 1: Environment variables
export AWS_ACCESS_KEY_ID='your_access_key'
export AWS_SECRET_ACCESS_KEY='your_secret_key'

# Option 2: AWS CLI
aws configure
```

## 🎧 Audio Setup

1. Open Windows Sound settings
2. Go to Recording tab
3. Enable "Stereo Mix"
4. Set as default device

If "Stereo Mix" is not available:
- Install [VB-Cable](https://vb-audio.com/Cable/)
- Use it as your recording device

## 🎮 Usage

1. Start the application:
```bash
python main.py
```

2. Recording Controls:
   - **F9**: Start Recording
   - **F10**: Pause/Resume
   - **F11**: Stop Recording

3. After stopping:
   - Recording saves to Desktop/ScreenRecordings
   - Automatically uploads to S3
   - Generates shareable link (valid for 2 minutes)

## 🗂️ Project Structure

```
screen_recorder/
├── core/           # Core functionality
│   ├── recorder.py     # Recording logic
│   └── s3_uploader.py  # S3 upload handling
├── gui/            # User interface
│   ├── app.py         # Main window
│   └── components.py  # UI components
└── utils/          # Utilities
    └── logger.py      # Logging system
```

## ⚙️ Configuration

Update S3 settings in `core/s3_uploader.py`:
```python
self.bucket_name = "your-bucket-name"
self.s3_config = Config(
    region_name='your-region',
    signature_version='s3v4'
)
```

## 🐛 Troubleshooting

1. **No Audio Recording**
   - Check if "Stereo Mix" is enabled
   - Try installing VB-Cable

2. **Upload Fails**
   - Verify AWS credentials
   - Check S3 bucket permissions
   - Ensure internet connectivity

3. **Black Screen**
   - Try running as administrator
   - Disable hardware acceleration in apps

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- ttkbootstrap for the modern GUI elements
- moviepy for video processing
- boto3 for AWS integration
- The open-source community

## 📞 Support

For support, please open an issue in the GitHub repository or contact the maintainers.

## Dependencies

- ttkbootstrap
- numpy
- sounddevice
- mss
- moviepy
- boto3
- soundfile
- pynput

## Contact

Project Link: [https://github.com/yourusername/screen-recorder](https://github.com/yourusername/screen-recorder) 
