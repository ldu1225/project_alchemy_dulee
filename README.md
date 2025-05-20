# Loading Data into BigQuery

This section describes how to load customer contact information into the BigQuery table `gemini_demo.customer_contact_info` using the `bq` command-line tool.

## Prerequisites

Before you begin, ensure you have the following:

1.  **Google Cloud SDK:**
    * The Google Cloud SDK (which includes the `gcloud` CLI and `bq` tool) must be installed and configured.
    * Authenticate and set your default project by running:
        ```bash
        gcloud auth login
        gcloud config set project [YOUR_PROJECT_ID]
        ```
        Replace `[YOUR_PROJECT_ID]` with your actual Google Cloud Project ID.

2.  **BigQuery Dataset:**
    * The target dataset `gemini_demo` must exist in your BigQuery project. If it doesn't, create it using the command:
        ```bash
        bq mk gemini_demo
        ```

3.  **Data Files:**
    * Prepare your data files: `alchemy_data1.csv` for CSV import and `alchemy_data1.json` for JSON import.
    * These files should be located in the directory where you run the `bq load` commands, or you must update the paths in the commands to point to the correct file locations.
    * The data in these files should conform to the following schema:
        * `customer_id`: INT64
        * `customer_name`: STRING
        * `phone_number`: STRING
        * `email_address`: STRING

## Loading Data from a CSV File

To load data from a CSV file (e.g., `alchemy_data1.csv`) into the `gemini_demo.customer_contact_info` table, use the following command. This command assumes the CSV file has a header row (which will be skipped) and will replace the table if it already exists.

```bash
bq load \
    --source_format=CSV \
    --skip_leading_rows=1 \
    --replace=true \
    gemini_demo.customer_contact_info \
    ./alchemy_data1.csv \
    customer_id:INT64,customer_name:STRING,phone_number:STRING,email_address:STRING
Command Options Explained:
```

```bash

bq load \
    --source_format=JSON \
    --replace=true \
    gemini_demo.customer_contact_info \
    ./alchemy_data1.json \
    customer_id:INT64,customer_name:STRING,phone_number:STRING,email_address:STRING
Command Options Explained:
```
