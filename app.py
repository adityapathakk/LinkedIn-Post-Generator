import streamlit as st
from integration import generate_linkedin_post

print("\n--- [app.py starting] ---\n")

intro = f"""
Made by Aditya Pathak!

<a href="https://github.com/adityapathakk">My GitHub</a> | <a href="https://linkedin.com/in/adityapathakk">My LinkedIn</a> | <a href="https://linktree.com/adityapathakk">My LinkTree</a><br><br><br><br><br>
"""

# --- Streamlit UI setup ---
st.set_page_config(page_title="LinkedIn Post Generator", layout="wide")
st.title("🔗 LinkedIn Post Generator")
st.markdown(intro, unsafe_allow_html=True)

# --- Initialize session state ---
for key in ("ideas", "generated", "llm_prompts"):
    if key not in st.session_state:
        st.session_state[key] = []

# --- Input form ---
idea = st.text_input("Enter your post idea:")
career = st.selectbox(
    "Your profession:",
    ["None","Designer","Coach","Web Developer","AI Expert","Founder","Student","Product Manager","Scientist"]
)

if st.button("Generate Post"):
    print(f"\n--- [Calling generate_linkedin_post with idea='{idea.strip()}', career='{career}'] ---\n")
    if not idea.strip():
        st.warning("Please provide a post idea to generate.")
    else:
        with st.spinner("Generating your LinkedIn post..."):
            post, llm_input = generate_linkedin_post(idea.strip(), career)
        # Save to session
        st.session_state.ideas.append(idea)
        st.session_state.generated.append(post)
        st.session_state.llm_prompts.append(llm_input)
        print(f"\n--- [Appended to history, total count={len(st.session_state.generated)}] ---\n")

# --- Display latest result ---
if st.session_state.generated:
    st.subheader("📝 Your Latest LinkedIn-Ready Post")
    st.markdown(st.session_state.generated[-1])
    with st.expander("▶️ View the LLM prompt"):
        st.code(st.session_state.llm_prompts[-1])

# --- Show history ---
if st.session_state.generated:
    st.subheader("📚 Previously Generated Posts")
    choice = st.selectbox(
        "Select a post to view",
        list(range(1, len(st.session_state.generated) + 1)),
        format_func=lambda i: f"Post #{i}", index=None
    )
    if choice:
        idx = choice - 1
        st.markdown(f"**Idea:** {st.session_state.ideas[idx]}")
        st.markdown(st.session_state.generated[idx])
        with st.expander("▶️ View its LLM prompt"):
            st.code(st.session_state.llm_prompts[idx])
