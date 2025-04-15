import requests
import os
import json

class AIService:
    def __init__(self):
        self.mistral_api_key = os.environ.get("MISTRAL_API_KEY")
        self.mistral_api_url = "https://api.mistral.ai/v1/chat/completions"
    
    def generate_script(self, topic, tone="informative", length=1000, youtube_data=None, tags=None, category=None):
        """
        Generate a script using Mistral 7B
        """
        if not self.mistral_api_key:
            # Fallback to mock script if API key is not available
            return self._generate_mock_script(topic, tone, length, youtube_data, tags, category)
        
        # Create a prompt that includes YouTube trend data if available
        trend_info = ""
        if youtube_data:
            trend_info = "Based on YouTube trend analysis:\n"
            
            if "categories" in youtube_data:
                trend_info += "- Popular categories: " + ", ".join(list(youtube_data["categories"].keys())[:3]) + "\n"
            
            if "tags" in youtube_data:
                trend_info += "- Popular tags: " + ", ".join(list(youtube_data["tags"].keys())[:5]) + "\n"
            
            if "avg_views" in youtube_data:
                trend_info += f"- Average views: {youtube_data['avg_views']}\n"
            
            if "video_length" in youtube_data:
                trend_info += "- Popular video lengths: " + ", ".join(youtube_data["video_length"].keys()) + "\n"
            
            if "top_videos" in youtube_data and youtube_data["top_videos"]:
                trend_info += "- Top trending video titles:\n"
                for i, video in enumerate(youtube_data["top_videos"][:3]):
                    trend_info += f"  {i+1}. {video['title']}\n"
        
        # Add specific tags if provided
        tag_info = ""
        if tags and len(tags) > 0:
            tag_info = "- Incorporate these specific tags: " + ", ".join(tags) + "\n"
        
        # Add category if provided
        category_info = ""
        if category and category != "0":
            from services.youtube_service import YouTubeService
            youtube_service = YouTubeService()
            categories = youtube_service.get_categories()
            category_name = categories.get(category, "Unknown")
            category_info = f"- This script is for the '{category_name}' category on YouTube\n"
        
        prompt = f"""Generate an interactive and engaging YouTube script about "{topic}" with a {tone} tone. 

The script should be approximately {length} words long and include:
- An attention-grabbing introduction with a strong hook
- Main content with key points, examples, and engaging questions for viewers
- Interactive elements like questions to the audience, calls for comments, etc.
- Practical tips or actionable advice that viewers can implement
- A compelling conclusion with a clear call to action

{trend_info}
{tag_info}
{category_info}

Format the script with clear sections:
1. INTRO
2. MAIN CONTENT (with subsections)
3. CONCLUSION

Use conversational language, include places for [B-ROLL], [ZOOM IN], [CUT TO], etc. where appropriate.
Include timestamps and approximate duration for each section.
Make the script feel personal and authentic, as if the creator is speaking directly to their audience.
"""
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.mistral_api_key}"
        }
        
        data = {
            "model": "mistral-7b-instruct-v0.2",
            "messages": [
                {"role": "system", "content": "You are an expert YouTube script writer who specializes in creating engaging, interactive scripts that keep viewers watching. Your scripts are conversational, include hooks, audience engagement techniques, and follow best practices for YouTube content. You understand what makes content go viral and how to incorporate current trends."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 2000
        }
        
        try:
            response = requests.post(self.mistral_api_url, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"Error generating script: {e}")
            return self._generate_mock_script(topic, tone, length, youtube_data, tags, category)
    
    def _generate_mock_script(self, topic, tone, length, youtube_data=None, tags=None, category=None):
        """
        Fallback mock script generator
        """
        # Include some trend data in the mock script if available
        trend_mention = ""
        if youtube_data and "tags" in youtube_data:
            popular_tags = list(youtube_data["tags"].keys())[:3]
            if popular_tags:
                trend_mention = f"\n\nAccording to current YouTube trends, topics like {', '.join(popular_tags)} are performing well. Let's incorporate some of these elements into our discussion of {topic}."
        
        # Include specific tags if provided
        tag_mention = ""
        if tags and len(tags) > 0:
            tag_mention = f"\n\nI'll be sure to cover {', '.join(tags)} in this video as these are topics you're interested in."
        
        return f"""# {topic.upper()} - YouTube Script

## INTRO [00:00-01:30]

Hey everyone, welcome back to the channel! Today we're diving deep into {topic}, something I've been really excited to share with you all. If you're new here, make sure to hit that subscribe button and notification bell so you don't miss any future videos.{trend_mention}{tag_mention}

[ZOOM IN]
So why is {topic} so important right now? Well, I've been researching this topic for weeks, and what I found will probably surprise you...

[B-ROLL: Show relevant imagery]
Let me know in the comments if you've ever wondered about {topic} before, and stick around until the end because I'm sharing 3 actionable tips you can implement today!

## MAIN CONTENT

### The Basics [01:30-03:45]
[CUT TO MAIN CAMERA]
{topic} has been gaining a lot of attention lately, and for good reason. Let's break down why this matters and how you can benefit from understanding it better.

First, let's talk about the fundamentals. {topic} is essentially about connecting ideas and creating value through innovative approaches. Many creators overlook the importance of this concept, but it's absolutely crucial for growth in today's landscape.

[GRAPHICS OVERLAY: Key points about {topic}]
What do you think about this approach? Drop your thoughts in the comments below!

### Why It Matters [03:45-06:30]
[SIDE ANGLE]
One of the most interesting aspects of {topic} is how it relates to audience engagement. Studies have shown that channels focusing on this area see up to 40% higher retention rates and significantly better comment activity.

[B-ROLL: Show examples]
Think about your own experience with {topic}. Have you noticed these patterns too? Let me know!

### Practical Application [06:30-09:15]
[BACK TO MAIN CAMERA]
Now let's get into the practical stuff - how can you actually use this information?

Here are three actionable tips you can implement today:

1. Start by analyzing your current strategy and identify areas where {topic} could be better integrated
   [ZOOM IN]
   This is crucial, so take notes!

2. Experiment with different approaches to see what resonates best with your specific audience
   [CUT TO B-ROLL]
   I've tried this myself and the results were amazing.

3. Create a feedback loop where you can measure the impact of these changes
   [GRAPHICS: Show feedback loop diagram]
   This is what separates amateurs from professionals!

## CONCLUSION [09:15-10:30]
[CLOSE UP SHOT]
That's it for today's video on {topic}! If you found this helpful, please hit that like button and subscribe for more content like this. 

[ZOOM OUT]
Remember, mastering {topic} isn't something that happens overnight, but with the tips I've shared today, you're already ahead of 90% of people.

[CALL TO ACTION]
Drop your questions in the comments below, share your own experiences with {topic}, and let me know what topics you'd like me to cover next!

[OUTRO CARD]
Thanks for watching, and I'll see you in the next one!
"""
