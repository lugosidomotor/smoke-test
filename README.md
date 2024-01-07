# 🩺 Automated Website Monitoring System

This repository contains a Python script for automated website monitoring, leveraging the power of Selenium and GitHub Actions. It's designed to ensure the reliability and efficiency of your website by regularly testing and monitoring its performance.

## Overview

In today's digital age, the health of your website is paramount. This system provides a dependable and cost-effective solution to monitor your website's functionality. Using Selenium for browser automation and GitHub Actions for workflow automation, this script performs regular checks on your website, including console error detection, page load time measurements, and screenshot captures.

## Features

- **Automated Testing:** Regularly checks for console errors and measures page load times.
- **Screenshot Capturing:** Takes screenshots of the website for visual inspection.
- **Flexible Execution:** Set to run automatically on an hourly basis or can be triggered manually for specific URLs.
- **Automatic Notifications:** Sends email notifications via GitHub if any issues are detected during a run. Can be configured to send notifications through Microsoft Teams or Slack.
- **CI/CD Integration:** Can be integrated into continuous integration and deployment pipelines.

## Setup and Usage

1. **Fork the Repository:** 
   Fork this repository to your GitHub account

2. **Configure the Script:**
   Update the URL in two places in the script to point to your website. Lines 10 and 24 in .github/workflows/SMOKE_TEST.yml.

3. **GitHub Actions:**
   Once set up, use the Actions tab on GitHub to view the script's performance. It displays loading speed, logs, and screenshots.
