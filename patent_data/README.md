# Patent Data Processing Project

This folder contains scripts for downloading and processing granted patent data from the United States Patent and Trademark Office (USPTO) for the years 2005 to 2023.

## Data Source

The patent data is sourced from the [USPTO Patent Grant Full Text Data](https://developer.uspto.gov/product/patent-grant-full-text-dataxml), provided by the USPTO.

### About USPTO

The United States Patent and Trademark Office (USPTO) is a federal agency under the Department of Commerce, responsible for issuing patents for inventions and registering trademarks. It is a vital resource for securing intellectual property rights in the United States.

### Patent Grant Data

The dataset includes comprehensive information about patents, encompassing various aspects such as:

- **Publication and Application References:** Details of publication and initial application of the patents.
- **Classification Details:** Categorization of patents according to international and national classification systems, like IPC and CPC.
- **Inventor and Examiner Information:** Names and details of inventors, along with information about the USPTO examiners.
- **Abstracts and Titles of Inventions:** Summary and official titles of the patented inventions.
- **Legal and Procedural Information:** Important legal data including grant dates, patent terms, and legal status.
- **Citations:** References to prior patents or literature cited in the patent document.
- **Applicant Data:** Information about the applicants, including organizations or individuals.
- **Inventor Details:** Comprehensive details of the inventors including their names, addresses, and nationalities.
- **Agent and Assignee Information:** Details about the patent agents and assignees, including names and addresses.
- **Claim Statements:** Detailed claims defining the scope of the patent protection.
- **US Field of Classification Search:** Information about the classification search conducted by the USPTO.
- **Drawings and Diagrams:** Visual representations or diagrams illustrating the invention.

This rich dataset is valuable for various stakeholders including researchers, legal professionals, entrepreneurs, and policy makers, offering insights into technological trends, innovation patterns, and intellectual property strategies.

### Timeframe

The scripts focus on patent data from the year 2005 to 2023, providing a broad range for analysis in various fields such as technology, legal studies, and innovation.

## Usage

### Downloading Patent Data

`patent_data_download.py` automates the downloading of patent data from the USPTO site, including handling file downloads, extraction, and error management.

### Processing Patent Data

`patent_data_integration.py` processes the downloaded XML files, extracting relevant information and saving it in a JSONL format.



