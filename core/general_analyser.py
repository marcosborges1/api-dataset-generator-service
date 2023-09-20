# from tkinter import NO
from turtle import color

# from unittest import result
from core.syntactic import SyntacticAnalysis
from collections import defaultdict
from rich.console import Console
from rich.table import Table
import json
import pandas as pd

# from tabulate import tabulate
# import matplotlib.pyplot as plt
# import matplotlib
import numpy as np


def get_attributes_list(data) -> list:
    if type(data) == type(list()):
        return data
    else:
        if type(data) == type(dict()):
            for d in data.values():
                return get_attributes_list(d)
        else:
            pass
    return list()


def get_leaves_nodes(data, array_aux) -> list:
    if type(data) == type(dict()):
        for dt in data.values():
            if not isinstance(dt, (dict, list)):
                array_aux.append(data)
                return data
            return get_leaves_nodes(dt, array_aux)
    elif type(data) == type(list()):
        for dt in data:
            get_leaves_nodes(dt, array_aux)


def get_leaves_with_parents(data, array_aux, array_parent, parent=""):
    if type(data) == type(dict()):
        for key, dt in data.items():
            if isinstance(dt, (dict)):
                print("Dict key", key)
                return get_leaves_with_parents(dt, array_aux, array_parent, parent)
            if isinstance(dt, (list)):
                if len(dt) > 1:
                    print("List key", key, dt, parent, len(dt))
                    return get_leaves_with_parents(dt, array_aux, array_parent, key)
                else:
                    print(f"XXXX {data} {key} parent {parent}")
                    array_aux.append(data)
                    array_parent.append({key: parent})
                    return
            if not isinstance(dt, (dict, list)):
                array_aux.append(data)
                array_parent.append({key: parent})
                print(f"Attributes only {data} {key} parent {parent}")
                pass
    elif type(data) == type(list()):
        print(f"Items of {parent} {data}")
        # get_leaves_with_parents(data, array_aux, array_parent, parent)
        for dt in data:
            print(f"Each data {dt}")
            get_leaves_with_parents(dt, array_aux, array_parent, parent)


def new_get_leaves_with_parents(data, array_aux, parent=""):
    if type(data) == type(dict()):
        for key, dt in data.items():
            if isinstance(dt, (dict)):
                # print("Dict key", key)
                return new_get_leaves_with_parents(dt, array_aux, parent)
            if isinstance(dt, (list)):
                if len(dt) >= 1:
                    # print("List key", key, dt, parent, len(dt))
                    return new_get_leaves_with_parents(dt, array_aux, key)
                else:
                    if len(key) > 2:
                        # print(f"ZZZZZZ {data} {key} parent {parent}")
                        array_aux.append(attribute_with_info(key, dt, parent))

                    return
            if not isinstance(dt, (dict, list)):
                if len(key) > 2:
                    if parent in ["get", "post", "put", "delete"]:
                        parent = "*no parent"
                    array_aux.append(attribute_with_info(key, dt, parent))
                    # print(f"Attributes only {data} {key} parent {parent}")
                pass
    elif type(data) == type(list()):
        # print(f"Items of {parent} {data}")
        # get_leaves_with_parents(data, array_aux, array_parent, parent)
        for dt in data:
            # print(f"Each data {dt}")
            new_get_leaves_with_parents(dt, array_aux, parent)


def attribute_with_info(key, dt, parent):
    if isinstance(dt, int):
        i = 0
        return json.loads(
            f"""{{
                "{key}": {{
                    "data_type": {i},
                    "parent": "{parent}"
                }}
            }}"""
        )
    elif isinstance(dt, bool):
        b = True
        return json.loads(
            f"""{{
                "{key}": {{
                    "data_type": {b},
                    "parent": "{parent}"
                }}
            }}"""
        )
    else:
        return json.loads(
            f"""{{
                "{key}": {{
                    "data_type": "{dt}",
                    "parent": "{parent}"
                }}
            }}"""
        )


def analyse_apis(
    file_content, similarities_analysis_array: defaultdict, order_by: str = "ASC"
):
    if order_by.__eq__("ASC") or order_by.__eq__("DESC"):
        for x in range(0, len(file_content) - 1):
            for y in range(1, len(file_content)):
                if x != y and x < y:
                    origin_api = (
                        file_content[x] if order_by == "ASC" else file_content[y]
                    )
                    target_api = (
                        file_content[y] if order_by == "ASC" else file_content[x]
                    )

                    for origin_api_responses in origin_api["responses"]:
                        new_origin_api_response_attribute = []
                        origin_api_response_attributes_test = []

                        new_get_leaves_with_parents(
                            origin_api_responses, new_origin_api_response_attribute
                        )

                        for target_api_requests in target_api["requests"]:
                            endpoints = {}
                            endpoints["origin"] = create_object_enpoint(
                                origin_api_responses
                            )
                            endpoints["target"] = create_object_enpoint(
                                target_api_requests
                            )
                            new_target_api_requests_attributes = []
                            new_get_leaves_with_parents(
                                target_api_requests, new_target_api_requests_attributes
                            )
                            syn = SyntacticAnalysis()
                            syn.analyze_similarities_2(
                                origin_api["name"],
                                target_api["name"],
                                new_origin_api_response_attribute,
                                new_target_api_requests_attributes,
                                endpoints,
                                similarities_analysis_array,
                            )
    else:
        raise Exception("Choice order_by attribute 'ASC' or 'DESC'")


def create_object_enpoint(api):
    endpoint = {}
    endpoint["url"] = list(api.keys())[0]
    endpoint["method"] = list(list(api.values())[0].keys())[0]
    return endpoint


def show_results(similarities, thereshold=0):
    array_data = []
    headers_data = []
    table = Table(title="Syntactic Analysis")
    fixed_columns = ["Origin API (OA)", "Target API (TA)", "OA Out Attr", "TA In Attr"]
    data_types = ["OA Out Attr dt", "TA In Attr dt"]
    parents = ["OA Out Attr parent", "TA In Attr parent"]
    data_endpoints = ["OA Url", "OA Method", "TA Url", "TA Method"]
    metric_columns = [
        "hamming",
        "levenshtein",
        "jaro_winkler",
        "jaccard",
        "sorensen",
        "ratcliff_obershelp",
    ]

    for column in (
        fixed_columns + data_types + parents + data_endpoints + metric_columns
    ):
        table.add_column(column)
        headers_data.append(column)

    array_each_data = defaultdict(list)

    for key_apis, val_apis in similarities.items():
        for val in val_apis:
            for key_attrs, metric_attrs in val.items():
                array_each_data["attrs"] = key_attrs.split("->")
                array_each_data["data_type"] = []
                array_each_data["parent"] = []
                array_each_data["endpoints"] = []
                array_each_data["similarity_metric"] = []

                # Data type
                for dt in metric_attrs["data_type"]:
                    array_each_data["data_type"].append(list(dt.values())[0])

                # Parent
                for parent in metric_attrs["parent"]:
                    array_each_data["parent"].append(list(parent.values())[0])

                # Endpoint
                array_each_data["endpoints"].append(
                    metric_attrs["endpoints"]["origin"]["url"]
                )
                array_each_data["endpoints"].append(
                    metric_attrs["endpoints"]["origin"]["method"]
                )
                array_each_data["endpoints"].append(
                    metric_attrs["endpoints"]["target"]["url"]
                )
                array_each_data["endpoints"].append(
                    metric_attrs["endpoints"]["target"]["method"]
                )

                # Metrics
                for metric in metric_attrs["similarity_metric"].values():
                    array_each_data["similarity_metric"].append(str(metric))
                for item in [
                    key_apis.split("->")
                    + array_each_data["attrs"]
                    + array_each_data["data_type"]
                    + array_each_data["parent"]
                    + array_each_data["endpoints"]
                    + array_each_data["similarity_metric"]
                ]:
                    for i in range(0, len(array_each_data["similarity_metric"])):
                        if float(array_each_data["similarity_metric"][i]) > thereshold:
                            array_data.append(item)
                            table.add_row(*item)
                            break

    console = Console()
    console.print(table)

    return headers_data, array_data


# def print_table_in_pandas(header, data):
#     df = pd.DataFrame(data, columns=header)
#     print(tabulate(df, headers="keys", tablefmt="simple_grid"))


def gini(x):
    print(len(x))
    # print(x.shape)
    arr = np.array([[1, 2, 3, 4, 5], [5, 1, 2, 2, 1]])
    # The column to be added
    col = np.array([[6], [0]], dtype="f")

    for i in range(len(arr)):
        col[i] = g(x[i])
    print(col)


def g(x):
    total = 0
    for i, xi in enumerate(x[:-1], 1):
        total += np.sum(np.abs(xi - x[i:]))
    return total / (len(x) ** 2 * np.mean(x))


def gini(array):
    array = array.flatten()  # all values are treated equally, arrays must be 1d
    array = np.sort(array)  # values must be sorted
    index = np.arange(1, array.shape[0] + 1)  # index per array element
    n = array.shape[0]  # number of array elements
    return (np.sum((2 * index - n - 1) * array)) / (n * np.sum(array))


def save_table(header, body, path):
    df = pd.DataFrame(body, columns=header)
    # gini(
    #     df[
    #         [
    #             "hamming",
    #             "levenshtein",
    #             "jaro_winkler",
    #             "jaccard",
    #             "sorensen",
    #             "ratcliff_obershelp",
    #         ]
    #     ]
    #     .astype(float)
    #     .to_numpy()
    # )
    # print(df["gini"])
    # print(df[["hamming","levenshtein"]].astype(num))
    with open(path, "w") as csv_file:
        df.to_csv(path_or_buf=csv_file,index_label="index")


# def _show_line_chart(header, body):
#     df2 = pd.DataFrame(body, columns=header)
#     df = pd.read_csv("data/result.csv")
#     print(df, df2)
#     df["mean"] = df[
#         [
#             "hamming",
#             "levenshtein",
#             "jaro_winkler",
#             "jaccard",
#             "sorensen",
#             "ratcliff_obershelp",
#         ]
#     ].mean(numeric_only=True, axis=1)
#     df["median"] = df[
#         [
#             "hamming",
#             "levenshtein",
#             "jaro_winkler",
#             "jaccard",
#             "sorensen",
#             "ratcliff_obershelp",
#         ]
#     ].median(numeric_only=True, axis=1)

#     fig, ax = plt.subplots(facecolor=("#ffffff"))
#     ax.set_facecolor("#ffffff")
#     ax.set_xlabel("", color="#000")
#     ax.set_ylabel("metrics", color="#000")
#     ax.plot(df["Index"], df["hamming"], color="#dedbd2", marker=".", label="hamming")
#     ax.plot(
#         df["Index"], df["levenshtein"], color="#a2d2ff", marker=".", label="levenshtein"
#     )
#     ax.plot(
#         df["Index"],
#         df["jaro_winkler"],
#         color="#f72585",
#         marker=".",
#         label="jaro_winkler",
#     )
#     ax.plot(df["Index"], df["jaccard"], color="#00bbf9", marker=".", label="jaccard")
#     ax.plot(df["Index"], df["sorensen"], color="#57cc99", marker=".", label="sorensen")
#     ax.plot(
#         df["Index"],
#         df["ratcliff_obershelp"],
#         color="#9f86c0",
#         marker=".",
#         label="haratcliff_obershelpmming",
#     )
#     ax.plot(
#         df["Index"], df["mean"], color="#999", marker=".", label="Mean", linestyle="--"
#     )
#     ax.legend(
#         loc="upper center",
#         bbox_to_anchor=(0.465, -0.1),
#         fancybox=True,
#         shadow=False,
#         ncol=4,
#         fontsize=8,
#     )
#     plt.show()


# def show_line_chart(path):
#     df = pd.read_csv(path)
#     df.insert(0, "Index", range(1, 1 + len(df)))
#     df["mean"] = df[
#         [
#             "hamming",
#             "levenshtein",
#             "jaro_winkler",
#             "jaccard",
#             "sorensen",
#             "ratcliff_obershelp",
#         ]
#     ].mean(numeric_only=True, axis=1)
#     df["median"] = df[
#         [
#             "hamming",
#             "levenshtein",
#             "jaro_winkler",
#             "jaccard",
#             "sorensen",
#             "ratcliff_obershelp",
#         ]
#     ].median(numeric_only=True, axis=1)

#     plt.plot(df["Index"], df["hamming"], color="#dedbd2", marker=".", label="hamming")
#     plt.plot(
#         df["Index"], df["levenshtein"], color="#a2d2ff", marker=".", label="levenshtein"
#     )
#     plt.plot(
#         df["Index"],
#         df["jaro_winkler"],
#         color="#f72585",
#         marker=".",
#         label="jaro_winkler",
#     )
#     plt.plot(df["Index"], df["jaccard"], color="#00bbf9", marker=".", label="jaccard")
#     plt.plot(df["Index"], df["sorensen"], color="#57cc99", marker=".", label="sorensen")
#     plt.plot(
#         df["Index"],
#         df["ratcliff_obershelp"],
#         color="#9f86c0",
#         marker=".",
#         label="haratcliff_obershelpmming",
#     )
#     plt.plot(
#         df["Index"], df["mean"], color="#000", marker=".", label="Mean", linestyle="--"
#     )
#     plt.xlabel("Tuple of attributes")
#     plt.ylabel("Metrics")
#     plt.legend(loc="best", bbox_to_anchor=(1.0, 1.02), fontsize=8)

#     fig = matplotlib.pyplot.gcf()
#     fig.set_size_inches(10.5, 7.5, forward=True)

#     plt.show()


def show_json_similarities(similarities_analysis_array, ind=2):
    print(json.dumps(similarities_analysis_array, indent=ind))


def save_cartesian_products(
    cartesian_products: defaultdict(list), path: str, format: str = "json"
):
    ext_allowed = ["json", "csv"]
    if not format in ext_allowed:
        raise ValueError(f"Only formats ({','.join(ext_allowed)}) are supported")
    else:
        if format == "json":
            with open(path, "w") as outfile:
                json.dump(cartesian_products, outfile, indent=2)
        elif format == "csv":
            save_csv(cartesian_products, path)


def save_csv(cartesian_products, path):
    array_data = []
    headers_data = []
    # table = Table(title="Syntactic Analysis")
    # index_column = ["index"]
    fixed_columns = ["origin_api", "target_api", "oa_out_attr", "ta_in_attr"]
    data_types = ["oa_out_attr_dt", "ta_in_attr_dt"]
    parents = ["oa_out_attr_parent", "ta_in_attr_parent"]
    data_endpoints = ["oa_url", "oa_method", "ta_url", "ta_method"]
    metric_columns = [
        "hamming",
        "levenshtein",
        "jaro_winkler",
        "jaccard",
        "sorensen",
        "ratcliff_obershelp",
    ]

    for column in (
        fixed_columns + data_types + parents + data_endpoints + metric_columns
    ):
        # table.add_column(column)
        headers_data.append(column)

    array_each_data = defaultdict(list)

    for key_apis, val_apis in cartesian_products.items():
        for val in val_apis:
            for key_attrs, metric_attrs in val.items():
                array_each_data["attrs"] = key_attrs.split("->")
                array_each_data["data_type"] = []
                array_each_data["parent"] = []
                array_each_data["endpoints"] = []
                array_each_data["similarity_metric"] = []

                # Data type
                for dt in metric_attrs["data_type"]:
                    array_each_data["data_type"].append(list(dt.values())[0])

                # Parent
                for parent in metric_attrs["parent"]:
                    array_each_data["parent"].append(list(parent.values())[0])

                # Endpoint
                array_each_data["endpoints"].append(
                    metric_attrs["endpoints"]["origin"]["url"]
                )
                array_each_data["endpoints"].append(
                    metric_attrs["endpoints"]["origin"]["method"]
                )
                array_each_data["endpoints"].append(
                    metric_attrs["endpoints"]["target"]["url"]
                )
                array_each_data["endpoints"].append(
                    metric_attrs["endpoints"]["target"]["method"]
                )

                # Metrics
                for metric in metric_attrs["similarity_metric"].values():
                    array_each_data["similarity_metric"].append(str(metric))
                for item in [
                    key_apis.split("->")
                    + array_each_data["attrs"]
                    + array_each_data["data_type"]
                    + array_each_data["parent"]
                    + array_each_data["endpoints"]
                    + array_each_data["similarity_metric"]
                ]:
                    array_data.append(item)
                    # for i in range(0, len(array_each_data["similarity_metric"])):
                    #     # if (
                    #     #     float(array_each_data["similarity_metric"][i])
                    #     #     > thereshold
                    #     # ):
                    #         # print(*item)
                    #         # print(metric_attrs)
                    #     array_data.append(item)
                    #     # table.add_row(*item)
    save_table(headers_data, array_data, path)


def remove_all_null_endpoints(file_content):
    new_file_content = remove_null_endpoints(file_content, "requests", "responses")

    new_file_content = remove_null_endpoints(new_file_content, "responses", "requests")

    return new_file_content


def remove_null_endpoints(file_content, type_solicitation1, type_solicitation2):
    for indice in range(0, len(file_content)):
        for solicitation in file_content[indice][type_solicitation1].copy():
            for k_r, v_r in solicitation.items():
                for k, v in v_r.items():
                    if v is None:
                        # print(solicitation)
                        file_content[indice][type_solicitation1].remove(solicitation)
                        for response in file_content[indice][type_solicitation2]:
                            for k_res, v_res in response.items():
                                if k_r == k_res and k == list(v_res.keys())[0]:
                                    file_content[indice][type_solicitation2].remove(
                                        response
                                    )
    return file_content


def get_endpoints_numbers(file_content):
    array_dict_apis = []
    for indice in range(0, len(file_content)):
        dict_apis = defaultdict(list)
        dict_apis[file_content[indice]["name"]] = {
            "requests": len(file_content[indice]["requests"]),
            "responses": len(file_content[indice]["responses"]),
        }
        array_dict_apis.append(dict_apis)
    return array_dict_apis


def remove_duplicated_endpoints(file_content):
    for indice in range(0, len(file_content)):
        new_list = []
        for solicitation_req in file_content[indice]["requests"]:
            if solicitation_req not in new_list:
                new_list.append(solicitation_req)

        file_content[indice]["requests"] = new_list

        new_list_res = []
        for solicitation_res in file_content[indice]["responses"]:
            if solicitation_res not in new_list_res:
                new_list_res.append(solicitation_res)

        file_content[indice]["responses"] = new_list_res

    return file_content
