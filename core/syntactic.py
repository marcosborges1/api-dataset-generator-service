from array import array
from email.policy import default
from nis import match
from operator import truediv
import string
from xmlrpc.client import Boolean
import textdistance
import json
import re
from collections import defaultdict


class SyntacticAnalysis:
    hamming = levenshtein = jaro_winkler = jaccard = sorensen = ratcliff_obershelp = 0
    
    def similarity(self, source_attribute: str, target_attribute: str):
        self.hamming = round(textdistance.hamming.normalized_similarity(
            source_attribute, target_attribute), 3)
        self.levenshtein = round(textdistance.levenshtein.normalized_similarity(
            source_attribute, target_attribute), 3)
        self.jaro_winkler = round(textdistance.jaro_winkler.normalized_similarity(
            source_attribute, target_attribute), 3)
        self.jaccard = round(textdistance.jaccard.normalized_similarity(
            source_attribute, target_attribute), 3)
        self.sorensen = round(textdistance.sorensen.normalized_similarity(
            source_attribute, target_attribute), 3)
        self.ratcliff_obershelp = round(textdistance.ratcliff_obershelp.normalized_similarity(
            source_attribute, target_attribute), 3)

    def analyze_similarities(self, orgin_api_name: str, target_api_name: str, attrs_res: list, attrs_req: list, endpoints:dict, similarities_analysis_array: defaultdict):
        for attr_res in attrs_res:
            for key_res, val_res in attr_res.items():
                for attr_req in attrs_req:
                    for key_req, val_req in attr_req.items():
                        type_res = self.get_type_by_extense(val_res)
                        type_req = self.get_type_by_extense(val_req)
                        self.similarity(key_res.lower(), key_req.lower())

                        similarities_analysis_array[f'{orgin_api_name}->{target_api_name}'].append(json.loads(f"""{{
                        			"{key_res}->{key_req}": {{
                        				"data_type": {{
                        					"{key_res}": "{type_res}",
                        					"{key_req}": "{type_req}"
                        				}},
                                        "endpoints": {json.dumps(endpoints)},
                        				"is_same_data_type": {json.dumps(type_res==type_req)},
                        				"similarity_metric":{{
                        					"hamming": {self.hamming},
                        					"levenshtein":{self.levenshtein},
                        					"jaro_winkler": {self.jaro_winkler},
                        					"jaccard": {self.jaccard},
                        					"sorensen": {self.sorensen},
                        					"ratcliff_obershelp": {self.ratcliff_obershelp}
                        				}}
                        			}}
                        }}"""))

    
    def analyze_similarities_2(self, orgin_api_name: str, target_api_name: str, attrs_res: list, attrs_req: list, endpoints:dict, similarities_analysis_array: defaultdict):
        for attr_res in attrs_res:
            for key_res, val_res in attr_res.items():
                # print(val_res["data_type"])
                for attr_req in attrs_req:
                    for key_req, val_req in attr_req.items():
                        type_res = self.get_type_by_extense(val_res["data_type"])
                        type_req = self.get_type_by_extense(val_req["data_type"])
                        self.similarity(key_res.lower(), key_req.lower())

                        similarities_analysis_array[f'{orgin_api_name}->{target_api_name}'].append(json.loads(f"""{{
                        			"{key_res}->{key_req}": {{
                        				"data_type": [
                                            {{"{key_res}": "{type_res}" }},
                        					{{"{key_req}": "{type_req}" }} 
                        				],
                                        "parent": [
                        					{{"{key_res}": "{val_res["parent"]}" }}, 
                        					{{"{key_req}": "{val_req["parent"]}" }}
                        				],
                                        "endpoints": {json.dumps(endpoints)},
                        				"is_same_data_type": {json.dumps(type_res==type_req)},
                        				"similarity_metric":{{
                        					"hamming": {self.hamming},
                        					"levenshtein":{self.levenshtein},
                        					"jaro_winkler": {self.jaro_winkler},
                        					"jaccard": {self.jaccard},
                        					"sorensen": {self.sorensen},
                        					"ratcliff_obershelp": {self.ratcliff_obershelp}
                        				}}
                        			}}
                        }}"""))

    def get_type_by_extense(self, class_type):
        if isinstance(class_type, str):
            return "string"
        elif isinstance(class_type, int or float):
            return "number"
        elif isinstance(class_type, list):
            return "list"
        elif isinstance(class_type, dict):
            return "object"
        elif isinstance(class_type, bool):
            return "Boolean"

    def is_any_similarities_greater_thereshold(self, threshold):
        if ((self.hamming or self.levenshtein or self.jaro_winkler or self.jaccard or self.sorensen or self.ratcliff_obershelp) >= threshold):
            return True
        else:
            return False

    def create_similarity(self, api_origin: str, api_target: str, attrs1: tuple, attrs2: tuple):
        k1, v1 = attrs1
        k2, v2 = attrs2

        return f"""{{
					"{api_origin}->{api_target}": {{
							"{k1}->{k2}": {{
								"type": "{type(v1)}",
								"similarity_metric":{{
									"hamming":{self.hamming},
									"levenshtein":{self.levenshtein},
									"jaro_winkler": {self.jaro_winkler},
									"jaccard": {self.jaccard},
									"sorensen": {self.sorensen},
									"ratcliff_obershelp": {self.ratcliff_obershelp}
								}}
							}}
					}}
			}}"""

    def __str__(self):
        return ("Similarities\n"
                f'{self.hamming=}\n'
                f'{self.levenshtein=}\n'
                f'{self.jaro_winkler=}\n'
                f'{self.jaccard=}\n'
                f'{self.sorensen=}\n'
                f'{self.ratcliff_obershelp=}')
