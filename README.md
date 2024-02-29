# Remote Monitoring System

![Screenshot at 2024-03-01 03-11-20](https://github.com/gautam132002/remote-monitring/assets/68372911/778a6aa0-dd7f-4c85-8478-f33fccad1fd9)


## Overview

This project aims to provide a comprehensive solution for remotely monitoring systems and servers. The application accurately monitors processes running at every instance, network usage, CPU usage, memory usage, and disk usage. One of the key features is the ability to *detect abnormal processes and provide a direct kill link for quick intervention*.

The system is designed to be OS-independent, ensuring flexibility and compatibility across different operating systems.

## Installation

1. Install the required dependencies using the following command:

    ```bash
    pip install -r requirements.txt
    ```

2. Navigate to the backend application and run the bash script:

    ```bash
    bash execute.sh
    ```

   Alternatively, you can run the individual scripts:

    - `fetch_process.py`
    - `kill.py`
    - `monitor_sys.py`

3. Record your system's data by running the script `recordpc.py` inside the `./backend/dataset` directory:

    ```bash
    python recordpc.py
    ```

4. Once you obtain the CSV file named `result_statistics.csv`, move it to the main directory.

5. Deploy the frontend application by pushing all code to GitHub. Then, go to the Streamlit Community Cloud, deploy the `ui.py` file, and make the application live.

6. Ensure to add `config.json` (your Firebase authentication JSON) with real-time database activation.

## Usage

- **Monitoring:**
  - Run the backend scripts to monitor system processes and resource usage.
  
- **Data Recording:**
  - Record system data using `recordpc.py` to generate `result_statistics.csv`.

- **Frontend Deployment:**
  - Deploy the frontend application by pushing code to GitHub and using Streamlit Community Cloud.

## Advantages

- Accurate monitoring of processes and resource usage.
- Quick detection of abnormal processes with a direct kill link.
- OS-independent design for broad compatibility.

## Contribution

Contributions to this project are welcome. Please follow these guidelines:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them with clear messages.
4. Create a pull request, detailing the changes and improvements.
