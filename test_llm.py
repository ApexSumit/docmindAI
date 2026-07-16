from backend.llm_interface import generate_response

# Mock data (simulates what the database would return)
mock_chunks = [
    {"text": "The termination notice period is 30 days.", "page": 4, "clause": "Section 3.2"},
    {"text": "Penalty for late payment is $500 per day.", "page": 7, "clause": "Section 5.1"}
]

print("🚀 Testing Q&A Chain...")
answer = generate_response("What is the notice period?", mock_chunks, mode="qa", user_role="HR Manager")
print(answer)

print("\n📝 Testing Summary Chain...")
summary = generate_response("", mock_chunks, mode="summary", user_role="General Counsel")
print(summary)

print("\n🔑 Testing Key-Terms Chain...")
terms = generate_response("", mock_chunks, mode="terms")
print(terms)

print("\n📅 Testing Date-Finding Chain...")
dates = generate_response("", mock_chunks, mode="dates")
print(dates)
