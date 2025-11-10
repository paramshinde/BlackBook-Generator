import os
from google import genai
from google.genai.errors import APIError as GeminiAPIError

# --- Configuration ---
# Your actual Gemini API Key value (replace with your full key)
# NOTE: Using a literal key is only for quick testing; use an environment variable in app.py.
LITERAL_API_KEY_VALUE = "AIzaSyDY4oLTvk3BKX28-iHnG5Pzj-T-jBtDwlo" 

# Use the literal value for testing the API connection itself
API_KEY = LITERAL_API_KEY_VALUE

PROJECT_NAME = "Timetable Generator Application"
DIAGRAM_TYPE = "Entity Relationship Diagram"

def test_ai_diagram_generation(project_name, diagram_type, api_key):
    """
    Calls the Google Gemini API with a prompt designed for diagram code generation
    and prints the response.
    """
    if not api_key or api_key == "GEMINI-DUMMY-KEY": # Changed check for simplicity
        print("🔴 ERROR: API Key not set correctly.")
        print("Please ensure the API key variable holds the correct value.")
        return

    # CORRECTED LINE: Use the correct variable name, DIAGRAM_TYPE
    print(f"🟢 Attempting Gemini API call for: {DIAGRAM_TYPE} on '{project_name}'...")
    
    try:
        # Initialize the Gemini client
        client = genai.Client(api_key=api_key)

        # Generate the specific prompt used in your main application
        prompt = (
            f"Generate a brief, valid Mermaid diagram code for a '{diagram_type}' "
            f"for a project titled '{project_name}'. Only return the Mermaid code block itself "
            f"(```mermaid ... ```) and nothing else. Ensure the diagram is simple but logically correct."
        )

        # Make the API call using the fast and capable gemini-2.5-flash model
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config={
                'temperature': 0.7,
            }
        )
        
        # Extract the content
        mermaid_code = response.text.strip()

        print("\n✅ API Call Successful! Response:\n")
        print("=" * 50)
        print(mermaid_code)
        print("=" * 50)
        #print(f"\nModel used: {response.model}")

    except GeminiAPIError as e:
        print("\n❌ Gemini API Call Failed!")
        print(f"Details: {e}")
        print("\nCheck if your API key is correct and has a valid, active quota/billing plan.")

    except Exception as e:
        print("\n❌ An unexpected error occurred!")
        print(f"Details: {e}")

if __name__ == "__main__":
    test_ai_diagram_generation(PROJECT_NAME, DIAGRAM_TYPE, API_KEY)