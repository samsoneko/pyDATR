import datr_cli
import json

def debug_clean(pretty_result):
    pretty_result = pretty_result.replace("oia", "oja")
    pretty_result = pretty_result.replace("oie", "oje")
    pretty_result = pretty_result.replace("uia", "uja")
    pretty_result = pretty_result.replace("uie", "uje")
    pretty_result = pretty_result.replace("aia", "aja")
    pretty_result = pretty_result.replace("aie", "aje")
    pretty_result = pretty_result.replace("öiä", "öjä")
    pretty_result = pretty_result.replace("öie", "öje")
    pretty_result = pretty_result.replace("yiä", "yjä")
    pretty_result = pretty_result.replace("yie", "yje")
    pretty_result = pretty_result.replace("äiä", "äjä")
    pretty_result = pretty_result.replace("äie", "äje")
    pretty_result = pretty_result.replace("eia", "eja")
    pretty_result = pretty_result.replace("eiä", "ejä")
    pretty_result = pretty_result.replace("eie", "eje")

    return pretty_result

json_to_datr_dict = {
    "nominative": "nom",
    "partitive": "part",
    "genitive": "gen",
    "illative": "ill",
    "inessive": "iness",
    "elative": "ela",
    "allative": "all",
    "adessive": "adess",
    "ablative": "abl",
    "essive": "ess",
    "translative": "trans",
    "abessive": "abess",
    "instructive": "instr",
    "singular": "sg",
    "plural": "pl"
}

# Get the test data
test_file = open("datr_files/fi_test_data.json", 'r', encoding='utf-8')
test_dict = json.load(test_file)

# Compile the theory
theory = datr_cli.compile_theory("datr_files/fi_datr.dtr")

words_to_test = [key for key in test_dict]

results_dict = {}
working_results = 0
error_results = 0
correct_results = 0

for word in words_to_test:
    declination_table = test_dict[word]["declination"]
    results_dict[word] = {}

    for case in [key for key in declination_table]:
        datr_case = json_to_datr_dict[case]
        results_dict[word][case] = {}

        for number in [key for key in declination_table[case]]:
            datr_number = json_to_datr_dict[number]
            
            # Skip instructive singular
            if case == "instructive" and number == "singular":
                continue

            # Start the query
            try:
                result = theory.query(word.capitalize() + ":<" + datr_number + " " + datr_case + ">")
                pretty_result = ""
                for element in result:
                    pretty_result += element
                
                if "xxx" in pretty_result:
                    variants = pretty_result.split("xxx")
                    results_dict[word][case][number] = [variant for variant in variants]
                    pretty_result = [debug_clean(variant) for variant in variants]
                else:
                    # DEBUG only temporary fix for triple vowels
                    results_dict[word][case][number] = pretty_result
                    pretty_result = debug_clean(pretty_result)

                working_results += 1
                if type(pretty_result) == str:
                    if type(declination_table[case][number]) == str:
                        if pretty_result == declination_table[case][number]:
                            correct_results += 1
                        else:
                            results_dict[word][case][number].append("WRONGNE")
                    elif type(declination_table[case][number]) == list:
                        if pretty_result in declination_table[case][number]:
                            correct_results += 1
                        else:
                            results_dict[word][case][number].append("WRONGNI")
                elif type(pretty_result) == list:
                    for variant in pretty_result:
                        if variant in declination_table[case][number]:
                            correct_results += 1/len(pretty_result)
                        else:
                            results_dict[word][case][number].append("WRONGLNI")
            except:
                results_dict[word][case][number] = "ERROR"
                error_results += 1
    
print(results_dict)
print("Total stability: " + str(working_results / (working_results+error_results)))
print("Total correctness: " + str(correct_results / (working_results+error_results)))

# Save the results to a json file
with open("output.json", 'w', encoding='utf-8') as f:
    json.dump(results_dict, f, ensure_ascii=False, indent=4)