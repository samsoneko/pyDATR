import datr_cli

# A quick helper script to auto generate the finnish prompt list for the datr cli
words_to_prompt = ["Valo", "Katu"]
prompts = []

for word in words_to_prompt:
    sg_template = word + ":<" + "sg"
    pl_template = word + ":<" + "pl"
    cases = ["nom", "part", "gen", "ill", "iness", "ela", "all", "adess", "abl", "ess", "trans"]
    for case in cases:
        prompts.append(sg_template + " " + case + ">")
        prompts.append(pl_template + " " + case + ">")
print(prompts)

print("-----")

for prompt in prompts:
    print(prompt, end='')
    print(", ", end='')