# from transformers import GPT2LMHeadModel, GPT2Tokenizer
# model_name = "gpt2-medium"  # or any other model from the Hugging Face model hub
# tokenizer = GPT2Tokenizer.from_pretrained(model_name)
# model = GPT2LMHeadModel.from_pretrained(model_name)
# prompt = "Give me recipe for pizza"
# input_ids = tokenizer.encode(prompt, return_tensors="pt")
#
# # Generate text
# output = model.generate(input_ids, max_length=100, num_return_sequences=1, temperature=0.7)
# generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
# print(generated_text)
# # output = model.generate(input_ids, max_length=150, num_return_sequences=3, temperature=0.8)


from transformers import Conversation, AutoModelForCausalLM, AutoTokenizer

# Load pretrained model and tokenizer
model_name = "microsoft/DialoGPT-medium"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Start conversation
conversation = Conversation("Give me a recipe for pizza", 0)

# Generate response
input_ids = tokenizer.encode(conversation, return_tensors="pt")
response_ids = model.generate(input_ids, max_length=100, pad_token_id=tokenizer.eos_token_id)
response_text = tokenizer.decode(response_ids[:, input_ids.shape[-1]:][0], skip_special_tokens=True)

print(response_text)
