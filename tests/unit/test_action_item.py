from app.pipeline.action_item_extractor import extract_action_items

def test_simple_action():
    text = "We will send the proposal by 10/10/2025. Please follow up next week."
    items = extract_action_items(text)
    assert any('send' in it.lower() for it in items)