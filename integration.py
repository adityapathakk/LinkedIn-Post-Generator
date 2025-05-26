import ollama
from transformers import T5TokenizerFast, pipeline
from prompts import careerSpecific_promptDict

print("\n--- [integration.py starting] ---\n")

print("\n--- [Loading SLM tokenizer and model pipeline] ---\n")
pre_tokenizer = T5TokenizerFast.from_pretrained("slm_preproc_final")
pre_pipe = pipeline(
    "text2text-generation",
    model="slm_preproc_final",
    tokenizer=pre_tokenizer,
)

print("\n--- [SLM pipeline ready] ---\n")

def generate_linkedin_post(idea: str, career: str = None) -> str:
    """
    Given a raw idea, runs the SLM preprocessor followed by Llama 3.2-3B via Ollama to produce a LinkedIn-ready post.
    """
    # 1) preprocess the idea into a refined prompt
    refined = pre_pipe(idea, max_length=96)[0]["generated_text"]
    print(f"\n--- [SLM refinement output: {refined}...] ---\n")
    # return refined if refined else None # for testing only the SLM output

    # 2) retrieve career-specific prompt if applicable
    career_prompt = "not selected"
    if career and career != "None":
        career = career.lower()
        career_prompt = careerSpecific_promptDict[f"{career}"]
        print(f"\n--- [Retrieved career prompt for '{career}'] ---\n")
    else:
        print("\n--- [No career prompt applied] ---\n")

    # 3) build the LLM input with instructions
    common_prompt = f"""YOU'RE THE PERFECT LINKEDIN POST WRITER. YOUR PRIMARY OBJECTIVE IS TO WRITE A LINKEDIN POST BASED ON THE IDEA THAT'S PROVIDED TO YOU BELOW.
    ### BASIC INSTRUCTIONS TO WRITE THE PERFECT LINKEDIN POST ### 
    - USE EXTREMELY PROFESSIONAL AND RICH VOCABULARY, BUT OCCASIONALLY USE INFORMAL ONE-LINERS, WHICH WILL HELP MAKE THE POST SOUND MORE PERSONAL AND LESS PREACHY!
    - PRIORITIZE HAVING
        - CLEAR PARAGRAPH STRUCTURE
        - CLEAN GRAMMAR
        - EMOTIONALLY RESONANT CONTENT
        - REALISTIC AND HUMANE TONE
    - SPRINKLE EMOJIS EVERY NOW AND THEN TO MAKE THE CONTENT MORE VISUALLY APPEALING.
    - LIMIT YOUR OUTPUT TO 150-300 WORDS.
    - AT THE END OF YOUR RESPONSE, YOU *MUST* INCLUDE THE FOLLOWING
        - A THOUGHT-PROVOKING QUESTION TO THE AUDIENCE
        - A HOPEFUL MESSAGE CENTRED AROUND THE IDEA OF THE POST
        - AT LEAST 5 RELEVANT HASHTAGS THAT WILL DRIVE ENGAGEMENT FOR THE POST
    - CRITICALLY ANALYZE THE IDEA SHARED BY THE USER AND ENSURE THAT YOU DO NOT STRAY AWAY FROM THE TOPIC OF THE IDEA.\n
    HERE'S THE IDEA SHARED BY THE USER, '{refined}'. 
    """

    llm_input = f"""
    {common_prompt}
    THE USER HAS ALSO SHARED THEIR PROFESSION - {career}. HERE ARE FURTHER INSTRUCTIONS FOR YOU TO WRITE CONTENT THAT'S TAILORED FOR THE USER'S JOB:
    {career_prompt} 
""" if career_prompt != "not selected" else common_prompt

    print(f"\n--- [Built LLM input: {llm_input[:100]}...] ---\n")
    
    # 4) generate the post via Ollama
    print("\n--- [Calling ollama.generate()] ---\n")
    response = ollama.generate(
        model="llama3.2:3b",
        prompt=llm_input,
    )
    post = response["response"]
    print(f"\n--- [Ollama response received: {post[:100]}...] ---\n")
    return post, llm_input

if __name__ == "__main__": # for testing only the SLM output
    test_post, test_prompt = generate_linkedin_post("branding, college, talk", "Student")
    print(f"\n--- [Test input prompt] ---\n{len(test_prompt)}]\n")
    print(f"\n--- [Test output post] ---\n{len(test_post)}\n")