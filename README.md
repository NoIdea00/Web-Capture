# 🌐 Web Snapshot Automation Tool

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)
![Selenium](https://img.shields.io/badge/Selenium-Automation-brightgreen?logo=selenium)
![Playwright](https://img.shields.io/badge/Playwright-E2E%20Testing-orange?logo=microsoft)
![License](https://img.shields.io/badge/License-MIT-purple)

This tool captures screenshots and page sources of websites using **Selenium** and **Playwright** with fallback capabilities. It auto-generates a detailed HTML report with previews and links for easy reference.

---

## 📦 Features

- 📸 Takes screenshots using **Selenium** (headless Chrome)
- 🔁 Falls back to **Playwright** if Selenium fails
- 🧾 Saves page source (`HTML`) for each URL
- 🧰 Generates an auto-styled **HTML report**
- ⚙️ Auto-installs missing dependencies (pip-based)

---

## 🚀 Installation & Usage

### ✅ Prerequisites

- Python 3.8+
- Google Chrome installed
- ChromeDriver in PATH (optional; auto-managed in most setups)

---

### 🧪 Steps to Run

1. **Clone this repo**

   ```bash
   git clone https://github.com/NoIdea00/web-snapshot-tool.git
   cd web-snapshot-tool
   ```

2. **Prepare your URLs**

   Add your list of target URLs in `input.txt`, one per line:

   ```
   example.com
   https://openai.com
   github.com
   ```

3. **Run the tool**

   ```bash
   python web-snapshot-tool.py
   ```

4. **View the results**

   Open `report.html` in your browser.

---

## 📁 Output Structure

```
.
├── screenshots/
│   ├── example_com/
│   │   ├── screenshot.png
│   │   └── page_source.html
│   └── ...
├── input.txt
├── report.html
└── main.py
```

---

## 📌 Notes

- Ensure internet connectivity to load external websites.
- You can toggle `headless` mode in both Selenium and Playwright sections.
- Chrome options can be customized for advanced use cases (e.g., proxies, user agents).

---

## 🛠 Troubleshooting

- **`WebDriverException`**: Ensure Chrome is installed and compatible with your `chromedriver`.
- **Timeouts**: Increase wait times if pages are slow to load.

---

## 🧑‍💻 Author

Made with ❤️ by [Your Name](https://github.com/yourusername)

---

## 📜 License

This project is licensed under the MIT License.
