# Asset Analysis Database (lazy naming, TODO improve)

## Overview

The Asset Analysis Database is a project designed to manage and analyze various assets. This repository contains the codebase for the database and related tools.

## Features

- Asset management
- Data analysis
- Reporting tools

## Installation

To install the project, follow these steps:

1. Clone the repository:
    ```sh
    git clone https://github.com/bjahnke/asset-analysis-db.git
    ```

2. Install the required Python packages:
    ```sh
    pip install -r requirements.txt
    ```

3. Ensure `invoke` is installed:
    ```sh
    pip install invoke
    ```

4. Build the Docker image:
    ```sh
    inv build
    ```

5. Start the Docker container:
    ```sh
    inv start
    ```

6. If you wish to stop the container:
   ```sh
   inv stop
   ```

## Project Structure

## Details

TODO - include ERD

# Features

The database design allows for the storage of historical price data from innumerable assets. It further distinguishes data by
several parameters such as interval (1 day, 1 hour, etc.), security/asset type, data source, etc. You could store price history
for the same asset at 1 day and 1 hour intervals, or perhaps store the prices of the same asset listed on multiple exchanges.

From a technical standpoint, the `stock` contains the keys where each row has unique combination of search values. Pushing price 
history to the database using the builtin method will trigger a search of the `stock` table, where it will either get an id from 
an exact match of all columns or create a new entry if none is found. The new data is assigned this `id` as the foreign key `stock_id` 
and added to the `stock_data` table. 

If there is existing data for the given `stock_id` in the `stock_data` table, there are 2 options to handle this:
- `replace`: delete all rows in the table associated with the given `stock_id` add all of the new rows. 
- `append`: this appends new data while preventing duplicate data from being added. Only new rows with a unique `stock_id` and `timestamp`
combination will be added to the table.
