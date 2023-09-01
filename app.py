from collections import defaultdict
from aux import utils
from core import general_analyser

# Paths configurations
# identification = "jira_github"
identification = "nfmirror_cfq"
path_input = f"data/{identification}.json"
path_output_in_json = f"data/cartesian_products_{identification}_fields.json"
path_output_in_csv = f"data/cartesian_products_{identification}_fields.csv"

file_content = utils.open_file(path_input)

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

# Save results from Analyse of APIS in file
general_analyser.save_cartesian_products(
    cartesian_products, path_output_in_json, "json"
)
general_analyser.save_cartesian_products(cartesian_products, path_output_in_csv, "csv")


# Print Before and After numbers of api endpoints
# print(json.dumps((get_endpoints_numbers_before, get_endpoints_numbers_later),indent=2))

# print(json.dumps((get_endpoints_numbers_before, get_endpoints_after),indent=2))

# general_analyser.analyse_apis(new_clean_file_content, cartesian_products
# )
# general_analyser.analyse_apis(
#     new_clean_file_content, cartesian_products
# , order_by="DESC")

# general_analyser.save_cartesian_products(,path_to_save_similarities,"json")

# print(json.dumps(cartesian_products
# ,indent=2))
# general_analyser.show_json_similarities(cartesian_products
# )
# general_analyser.save_similarities(
#     cartesian_products
# , path_to_save_similarities)

# table_header, table_body = general_analyser.show_results(cartesian_products
# , thereshold=0)

# general_analyser.save_table(table_header, table_body, path="data/result.csv")

# general_analyser.show_line_chart(path="data/result.csv")
