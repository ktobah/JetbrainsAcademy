def what_to_do(instructions):
    if instructions.startswith("Simon says") or instructions.endswith("Simon says"):
        return f"I {instructions.replace('Simon says', '').strip()}"
    else:
        return "I won't do it!"


what_to_do("make a wish Simon says")