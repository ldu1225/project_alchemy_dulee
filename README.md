# Loading Data into BigQuery

This section describes how to load customer contact information from a CSV file into the BigQuery table `gemini_demo.customer_contact_info` using the `bq` command-line tool. It utilizes an external JSON file (`alchemy_data1.json`) to define the table's schema.

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

3.  **Required Files:**
    * You will need the following files:
        * `alchemy_data1.csv`: This is your data file containing the customer records in CSV format.
        * `alchemy_data1.json`: This is your **schema definition file** in JSON format. It should contain the content you provided (defining `customer_id`, `customer_name`, etc.).
    * Both files should be located in the directory where you run the `bq load` command, or you must update the paths in the command to point to their correct locations.

## Loading Data from a CSV File (Using an External JSON Schema File)

To load data from your `alchemy_data1.csv` file into the `gemini_demo.customer_contact_info` table, using `alchemy_data1.json` as the schema definition, use the following command. This command assumes the CSV file has a header row (which will be skipped) and will replace the table if it already exists.

```bash
bq load \
    --source_format=CSV \
    --skip_leading_rows=1 \
    --replace=true \
    gemini_demo.customer_contact_info \
    ./alchemy_data1.csv \
    ./alchemy_data1.json
