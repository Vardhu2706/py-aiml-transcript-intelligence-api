from app.pipeline.summarizer import summarize_text
from app.pipeline.sentiment import analyze_sentiment

text = '''Meeting Chairman (Mark): Good morning, everyone. Thank you for coming. We have a packed agenda today, so let’s get started. First, let’s address the updates to our sales reporting system. These were discussed in our last meeting on May 30th, and today we’ll review their implementation progress. Afterward, we’ll dive into our main focus: brainstorming strategies to enhance our customer support. But before we start, does anyone have any pressing updates to share?

Tom Robbins: Just a quick note, Mark. The adjustments to our reporting system seem to be running smoothly. Teams are adapting well, and we’re already seeing more consistent data inputs.

Meeting Chairman: That’s great to hear, Tom. Anyone else?

Jennifer Miles: Yes, Mark. I wanted to mention that I received some feedback from our regional managers about the new reporting process. They suggested a few tweaks that could make it even more user-friendly. I’ll email you the details later.

Meeting Chairman: Perfect. Let’s make sure we address those points after this meeting. For now, let’s move on to the brainstorming session. We’re here to generate actionable ideas to enhance our customer support. I want everyone to feel free to share their thoughts—no idea is too small or too big. Let’s start with the basics: What’s the one thing you think we’re currently missing in our customer support strategy?

Meeting Chairman (Mark): So, let’s start with the basics: What’s the one thing you think we’re currently missing in our customer support strategy? I want everyone to think about their own experiences, feedback from clients, or anything that’s been bugging you about how we currently operate.

Alice Linnes: Well, I think one of our biggest gaps is responsiveness. Customers today expect faster answers, especially when issues arise. Our current system relies too much on email, which, let’s be honest, isn’t ideal for quick resolutions.

Donald Peters: I completely agree, Alice. I’ve noticed that even though we try to respond within 24 hours, that’s not fast enough for many customers. Some of our competitors promise responses within an hour—or even instantly in some cases. We’re falling behind in terms of speed.

John Ruting: While speed is definitely important, I think there’s more to the issue. Customers don’t just want fast responses; they want meaningful ones. Sometimes our replies are generic or lack the depth that customers are looking for. It’s not just about responding quickly but also ensuring that the response truly addresses their concerns.

Jennifer Miles: That’s a great point, John. Customers can tell when they’re being given a canned response, and it doesn’t build trust. I’ve heard feedback from clients who said they felt like they were being “passed around” between departments without anyone really understanding their issue. It’s not just about speed but also about clarity and ownership.

Jack Peterson: I think responsiveness and meaningful interactions go hand in hand. One way to address both might be by introducing a multi-channel support system. Right now, email and phone are our primary methods of communication. But if we added live chat or even social media support, we’d not only be more accessible but could also address issues faster and more directly.

Donald Peters: That’s an interesting idea, Jack. But wouldn’t adding more channels make it harder to maintain consistency in how we handle customer issues? We already have trouble ensuring that every agent is on the same page when dealing with complex problems.

Alice Linnes: That’s a valid concern, Donald, but I think consistency is something we can address through better training and more robust internal communication tools. If our agents have access to a centralized knowledge base or customer database, it shouldn’t matter which channel the customer uses to reach out. The agent can still provide a consistent experience.

'''
print("Sentiment:", analyze_sentiment(text))
print("Summary:", summarize_text(text))
