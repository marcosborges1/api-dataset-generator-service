from core import general_analyser, utils
from collections import defaultdict
from urllib.parse import urlparse
import os

BASE_URL = f"http://localhost:{os.getenv('PORT')}"

async def resolve_generate_dataset(_, info, generatedExtractedFile):

    # print(generatedExtractedFile)
    # return {"generatedDatasetFile": "adf", "information": "adsf"}

    parsed_url = urlparse(generatedExtractedFile)
    filename = parsed_url.path.split('/')[-1]
    file_content = await utils.open_file(generatedExtractedFile)
    cartesian_products = defaultdict(list)

    # Get numbers of API endpoints before Analysis
    get_endpoints_numbers_before = general_analyser.get_endpoints_numbers(file_content)

    # Cleanning file content
    new_clean_file_content = general_analyser.remove_duplicated_endpoints(file_content)
    new_clean_file_content = general_analyser.remove_all_null_endpoints(
        new_clean_file_content
    )

    # Get numbers of API endpoints after Analysis
    get_endpoints_numbers_later = general_analyser.get_endpoints_numbers(
        new_clean_file_content
    )

    # Analyse APIS
    general_analyser.analyse_apis(
        new_clean_file_content, cartesian_products, order_by="ASC"
    )
    general_analyser.analyse_apis(
        new_clean_file_content, cartesian_products, order_by="DESC"
    )
    csv_filename = filename.replace('.json', '.csv')
    output_file_path = f"data/{csv_filename}"
    # Save results from Analyse of APIS in file
    general_analyser.save_cartesian_products(
        cartesian_products, output_file_path, "csv"
    )
    information = f"Dataset generated saved to {output_file_path}"
    return {"generatedDatasetFile": f"{BASE_URL}/{output_file_path}", "information": information}
