# Light Fault Detection (LampDetection)

This project, known as Light Fault Detection or LampDetection, aims to detect faults in lighting systems.

For comprehensive documentation, detailed setup instructions, and a deeper understanding of the project, please refer to the Notion page:

📖 Full Documentation on Notion: https://www.notion.so/Light-Fault-Detection-1ca8897d2c908026ba9aea6ffcdd6c29?pvs=4

The code for this project is hosted on GitHub:

repository GitHub Repository: https://github.com/engKIKO/LampDetection

---

## Quick Start

Follow these steps for a quick way to run the project:

1.  **Create a Python Virtual Environment:**
    ```bash
    python -m venv venv
    ```
    *(Note: The command might vary slightly depending on your system. Refer to the Notion page or online resources for specific instructions if needed.)*

2.  **Activate the Virtual Environment:**
    * On Linux/macOS:
        ```bash
        source venv/bin/activate
        ```
    * On Windows:
        ```bash
        .\venv\Scripts\activate
        ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables:**
    Set up your configuration by creating and populating a .env file in the root directory of the project.
    *(Refer to the Notion page for details on required variables.)*

5.  **Run the Application:**
    * If running on a standard PC:
        ```bash
        python app.py
        ```
    * If running on a Raspberry Pi:
        ```bash
        python appRas.py
        ```

---

⚠️ **Important Setup Information**

**Please note:** The steps above provide a quick run guide. It is crucial to follow the detailed step-by-step instructions in the https://www.notion.so/Light-Fault-Detection-1ca8897d2c908026ba9aea6ffcdd6c29?pvs=4 documentation to properly set up the environment system and ensure the project runs correctly. This includes essential prerequisites and environment configuration details not covered in the quick start.